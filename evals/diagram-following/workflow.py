"""Read the diagram-following corpus: its workflows, their forms and scenarios.

A workflow is a directory under `workflows/` holding two source trees and
its scenarios. Each tree's entry document is `workflow.md`, and each state
is a document of its own under `states/`, named for the state in lower
case and headed with the state's name.

- `diagram/` holds the workflow as a Mermaid flowchart. A node is a state,
  named by its node id; `start` points at the first state, and each
  terminal state points at `stop`. A click on a node links that state's
  document, and a state reached through a link inside another state's
  section carries no click.
- `prose/` holds the same state documents and no diagram. Its entry
  document links the first state, and each section names the state that
  comes next.
- `linked/` holds the same state documents and no diagram, and a decision
  section names a branch by a document instead of a label. Each rule
  document states one label, so the label a branch takes is reachable only
  by following the link, and it is held to the edge the diagram draws all
  the same. A label that names an edge exists on the diagram alone.

A state's section states its action, then a paragraph opening `**Next.**`
that states its transition, and that paragraph alone differs between the
forms. A diagram section names the label of the edge to take, or takes the
one edge out of its state; a prose section names the next state; a linked
section names the document stating the label of the edge to take. A
terminal section says the workflow is complete. A decision is written as
one condition with a branch for when it holds and one for when it does
not, and a condition is one of two sentences: an input file reads a value,
or `trace.log` holds a state's line fewer times than the number an input
file holds.

The diagram is the one statement of the workflow's edges: the scenarios
name inputs and a path, and the path is held to the edges parsed here.
`scenarios.toml` lists each scenario's name, its inputs as file name and
value, and the path a correct run walks. A run writes each input to
`inputs/<name>` as the value followed by a newline, and a condition reads
the file with surrounding whitespace removed.

A form is bundled by the `pf` command the environment provides, run from
the form's directory, so the bundle is the one this checkout builds. `pf`
writes its bundle set into `workflow.bundles/` under the output folder it is
given, and the entry's bundle there is `workflow.bundle.md`. No form
dispatches, so that bundle is the whole set.
"""

import re
import shutil
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKFLOWS = ROOT / "workflows"
INSTRUCTION = ROOT / "instruction.md"

ENTRY = "workflow.md"
ENTRY_BUNDLE = Path("workflow.bundles", "workflow.bundle.md")
STATES = "states"
SCENARIOS = "scenarios.toml"
DIAGRAM = "diagram"
PROSE = "prose"
LINKED_FORM = "linked"
FORMS = (DIAGRAM, PROSE, LINKED_FORM)

START = "start"
STOP = "stop"
ENTRY_PLACEHOLDER = "ENTRY"
STEP_LIMIT = 100

FENCE = re.compile(r"^```(\w*)\n(.*?)^```", re.MULTILINE | re.DOTALL)
NODE = r"(\w+)(?:\(+[^)]*\)+)?"
EDGE = re.compile(rf"^\s*{NODE}\s*-->\s*(?:\|([^|]*)\|\s*)?{NODE}\s*$")
CLICK = re.compile(r'^\s*click\s+(\w+)\s+(?:href\s+)?"([^"]*)"')
HEADING = re.compile(r"^# (\w+)\n")
NEXT = "**Next.** "
ACTION = re.compile(r"^Write `actions/([^`]+)` containing `([^`]*)`\.$", re.MULTILINE)
TERMINAL = "The workflow is complete."
ONLY_EDGE = "Take the transition out of this state."
LABEL = r"take the transition labelled `([^`]+)`"
GO_TO = r"go to \[(\w+)\]\([^)]+\)"
LINKED = r"take the transition labelled in \[([^\]]+)\]\(([^)]+)\)"
LABEL_STATEMENT = re.compile(
    r"^The transition labelled `([^`]+)` applies\.$", re.MULTILINE
)
DECISION = {
    DIAGRAM: re.compile(rf"^If (.+), {LABEL}\. Otherwise, {LABEL}\.$"),
    PROSE: re.compile(rf"^If (.+), {GO_TO}\. Otherwise, {GO_TO}\.$"),
    LINKED_FORM: re.compile(rf"^If (.+), {LINKED}\. Otherwise, {LINKED}\.$"),
}
UNCONDITIONAL = {
    DIAGRAM: re.compile(rf"^{re.escape(ONLY_EDGE)}$"),
    PROSE: re.compile(r"^Go to \[(\w+)\]\([^)]+\)\.$"),
    LINKED_FORM: re.compile(rf"^{re.escape(ONLY_EDGE)}$"),
}
READS = re.compile(r"^`inputs/([^`]+)` reads `([^`]*)`$")
FEWER = re.compile(
    r"^`trace\.log` holds the line `(\w+)` fewer times than the number in "
    r"`inputs/([^`]+)`$"
)


class CorpusError(Exception):
    """A corpus file the reader cannot read as the corpus states it."""


@dataclass(frozen=True)
class Edge:
    """One transition the diagram draws, with its label when it carries one."""

    source: str
    target: str
    label: str | None


@dataclass(frozen=True)
class Diagram:
    """The workflow the diagram form draws."""

    start: str
    edges: tuple[Edge, ...]
    terminals: frozenset[str]
    clicks: dict[str, str]

    @property
    def states(self) -> frozenset[str]:
        """Every node of the diagram except the start and stop markers."""
        nodes = {edge.source for edge in self.edges} | {
            edge.target for edge in self.edges
        }
        return frozenset(nodes - {START, STOP})

    def leaving(self, state: str) -> tuple[Edge, ...]:
        """The edges out of one state, the edge to the stop marker excepted."""
        return tuple(
            edge for edge in self.edges if edge.source == state and edge.target != STOP
        )


@dataclass(frozen=True)
class Transition:
    """A section's transition: where to go, under which condition.

    `then` and `otherwise` are edge labels in the diagram form and state
    names in the prose form. An unconditional transition carries no
    condition and no `otherwise`; in the diagram form it carries no label
    either, since it takes the one edge out of its state.
    """

    condition: str | None
    then: str | None
    otherwise: str | None


@dataclass(frozen=True)
class Section:
    """One state's document: its action and its transition.

    `body` is the document up to the transition paragraph, which is the part
    the two forms share. A terminal section carries no transition.
    """

    state: str
    path: Path
    body: str
    action: tuple[str, str]
    transition: Transition | None


@dataclass(frozen=True)
class Scenario:
    """One run's inputs and the path a correct run walks."""

    name: str
    inputs: dict[str, str]
    path: tuple[str, ...]


@dataclass(frozen=True)
class Workflow:
    """One workflow: its diagram, each form's sections and its scenarios."""

    name: str
    directory: Path
    diagram: Diagram
    sections: dict[str, dict[str, Section]]
    scenarios: tuple[Scenario, ...]

    def form(self, form: str) -> Path:
        """The directory holding one form's source tree."""
        return self.directory / form


def mermaid(entry: Path) -> str:
    """The one Mermaid diagram an entry document holds."""
    blocks: list[str] = [
        body for kind, body in FENCE.findall(entry.read_text()) if kind == "mermaid"
    ]
    if len(blocks) != 1:
        raise CorpusError(f"{entry} holds {len(blocks)} mermaid diagrams, not one")
    return blocks[0]


def read_diagram(entry: Path) -> Diagram:
    """The diagram's edges, start state, terminal states and clicks."""
    edges: list[Edge] = []
    clicks: dict[str, str] = {}
    for line in mermaid(entry).splitlines():
        if edge := EDGE.match(line):
            source, label, target = edge.groups()
            edges.append(Edge(source, target, label))
        elif click := CLICK.match(line):
            clicks[click.group(1)] = click.group(2)
    starts = [edge.target for edge in edges if edge.source == START]
    if len(starts) != 1:
        raise CorpusError(f"{entry}: {START} points at {len(starts)} states, not one")
    terminals = frozenset(edge.source for edge in edges if edge.target == STOP)
    return Diagram(starts[0], tuple(edges), terminals, clicks)


def labelled_rule(directory: Path, destination: str) -> str:
    """The label a rule document states, as one backticked edge label.

    A linked transition names a document rather than a label, so the label
    a branch takes is the one that document states. It sits outside the
    diagram form's sections, so a bundle carries it and a diagram does not.
    `directory` is that of the section writing the link, which is where the
    document resolves from.
    """
    target = directory / destination
    if not target.is_file():
        raise CorpusError(f"a transition links {destination}, which is no document")
    found = None
    for match in LABEL_STATEMENT.finditer(target.read_text()):
        if found is not None:
            raise CorpusError(f"{destination} states more than one label")
        found = match.group(1)
    if found is None:
        raise CorpusError(f"{destination} states no label")
    return found


def parse_transition(
    form: str, text: str, directory: Path | None = None
) -> Transition | None:
    """A transition paragraph's meaning, in the form it is written for."""
    if text == TERMINAL:
        return None
    if decision := DECISION[form].match(text):
        if form == LINKED_FORM:
            condition, _, then_path, _, otherwise_path = decision.groups()
            input_read(condition)
            if directory is None:
                raise CorpusError(f"a linked transition reads {text!r} with no root")
            return Transition(
                condition,
                labelled_rule(directory, then_path),
                labelled_rule(directory, otherwise_path),
            )
        condition, then, otherwise = decision.groups()
        input_read(condition)
        return Transition(condition, then, otherwise)
    if unconditional := UNCONDITIONAL[form].match(text):
        target = unconditional.group(1) if unconditional.groups() else None
        return Transition(None, target, None)
    raise CorpusError(f"no {form} transition reads as {text!r}")


def read_section(form: str, path: Path, directory: Path) -> Section:
    """One state's document, split into its shared body and its transition."""
    text = path.read_text()
    heading = HEADING.match(text)
    if heading is None:
        raise CorpusError(f"{path} opens with no state heading")
    body, marker, transition = text.rpartition(f"\n{NEXT}")
    if not marker:
        raise CorpusError(f"{path} carries no {NEXT.strip()} paragraph")
    actions = ACTION.findall(body)
    if len(actions) != 1:
        raise CorpusError(f"{path} states {len(actions)} actions, not one")
    return Section(
        heading.group(1),
        path,
        body,
        actions[0],
        parse_transition(form, transition.strip(), path.parent),
    )


def read_sections(form_directory: Path, form: str) -> dict[str, Section]:
    """Every state document of one form, by state name."""
    sections = [
        read_section(form, path, form_directory)
        for path in sorted((form_directory / STATES).glob("*.md"))
    ]
    return {section.state: section for section in sections}


def read_scenarios(path: Path) -> tuple[Scenario, ...]:
    """The scenarios a workflow's `scenarios.toml` lists."""
    with path.open("rb") as handle:
        entries = tomllib.load(handle)["scenario"]
    return tuple(
        Scenario(entry["name"], dict(entry["inputs"]), tuple(entry["path"]))
        for entry in entries
    )


def read_workflow(directory: Path) -> Workflow:
    """One workflow directory, read whole."""
    return Workflow(
        directory.name,
        directory,
        read_diagram(directory / DIAGRAM / ENTRY),
        {form: read_sections(directory / form, form) for form in FORMS},
        read_scenarios(directory / SCENARIOS),
    )


def workflows(root: Path = WORKFLOWS) -> list[Workflow]:
    """Every workflow the corpus holds, in name order."""
    return [read_workflow(path) for path in sorted(root.iterdir()) if path.is_dir()]


def instruction(entry: str) -> str:
    """The task text a session is given, naming the document it reads."""
    blocks: list[str] = [
        body for kind, body in FENCE.findall(INSTRUCTION.read_text()) if kind == "text"
    ]
    if len(blocks) != 1:
        raise CorpusError(f"{INSTRUCTION} holds {len(blocks)} text blocks, not one")
    return blocks[0].replace(ENTRY_PLACEHOLDER, entry)


def bundle(form_directory: Path, output: Path) -> subprocess.CompletedProcess[bytes]:
    """The `pf` run bundling one form from its entry document under `output`.

    The entry's bundle is `output / ENTRY_BUNDLE` once the run succeeds.
    """
    command = shutil.which("pf")
    if command is None:
        raise CorpusError("no pf command is on the path to bundle a form with")
    return subprocess.run(
        [command, ENTRY, "-o", str(output)],
        cwd=form_directory,
        capture_output=True,
        check=False,
    )


def holds(condition: str, inputs: dict[str, str], trace: list[str]) -> bool:
    """Whether a condition holds for the inputs and the trace so far."""
    if reads := READS.match(condition):
        name, value = reads.groups()
        return inputs[name].strip() == value
    if fewer := FEWER.match(condition):
        state, name = fewer.groups()
        return trace.count(state) < int(inputs[name].strip())
    raise CorpusError(f"no condition reads as {condition!r}")


def input_read(condition: str) -> str:
    """The input file a condition reads."""
    if reads := READS.match(condition):
        return reads.group(1)
    if fewer := FEWER.match(condition):
        return fewer.group(2)
    raise CorpusError(f"no condition reads as {condition!r}")


def inputs_read(workflow: Workflow, form: str) -> set[str]:
    """The input files one form's conditions read."""
    return {
        input_read(section.transition.condition)
        for section in workflow.sections[form].values()
        if section.transition is not None and section.transition.condition is not None
    }


def successor(
    workflow: Workflow, form: str, state: str, inputs: dict[str, str], trace: list[str]
) -> str | None:
    """The state one form's section for a state says comes next, if any."""
    transition = workflow.sections[form][state].transition
    if transition is None:
        return None
    chosen = transition.then
    if transition.condition is not None and not holds(
        transition.condition, inputs, trace
    ):
        chosen = transition.otherwise
    if form == PROSE:
        return chosen
    leaving = workflow.diagram.leaving(state)
    targets = [edge.target for edge in leaving if edge.label == chosen]
    if len(targets) != 1:
        raise CorpusError(
            f"{workflow.name}: {state} has {len(targets)} edges labelled {chosen!r}"
        )
    return targets[0]


def walk(workflow: Workflow, form: str, inputs: dict[str, str]) -> tuple[str, ...]:
    """The path one form's sections lead through for the inputs."""
    trace: list[str] = []
    state: str | None = workflow.diagram.start
    while state is not None:
        if len(trace) == STEP_LIMIT:
            raise CorpusError(f"{workflow.name}: no terminal state in {STEP_LIMIT}")
        trace.append(state)
        state = successor(workflow, form, state, inputs, trace)
    return tuple(trace)
