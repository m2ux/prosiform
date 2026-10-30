"""Read the diagram-following corpus: its workflows, their forms and scenarios.

A workflow is a directory under `workflows/` holding its source trees and
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
- `compiled/` and `authored/` hold the same workflow with its states
  dispatching targets of their own, so a state's section names a step that
  hands another document to a sub-agent. `compiled/` writes the step with
  the dispatch operator the `pf` guide states, `⇉` for one target and `⫽`
  for a set of them, so `pf` compiles each target into a bundle of its own.
  `authored/` writes the same step with the protocol as prose and only
  ordinary links, so it publishes one bundle and the protocol an agent
  reads is the corpus's text rather than the profile's.

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
value, and the path a correct run walks. A dispatch form's scenario also
lists the trace a correct run produces: one `[[scenario.trace]]` table per
sub-agent start, in the order the walk dispatches them, naming the section
the sub-agent follows as the document and heading it was compiled from,
what it returned, and `together` on each entry of a set started at once.
A run writes each input to `inputs/<name>` as the value followed by a
newline, and a condition reads the file with surrounding whitespace removed.

A form is bundled by the `pf` command the environment provides, run from
the form's directory, so the bundle is the one this checkout builds. `pf`
writes its bundle set into `workflow.bundles/` under the output folder it is
given, and the entry's bundle there is `workflow.bundle.md`. A form that
dispatches publishes one bundle per target beside the entry's, so its set
is every bundle `pf` writes; a form that does not publishes the entry's
alone.
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
INSTRUCTION_BOOTSTRAP = ROOT / "instruction-bootstrap.md"

ENTRY = "workflow.md"
ENTRY_BUNDLE = Path("workflow.bundles", "workflow.bundle.md")
STATES = "states"
SCENARIOS = "scenarios.toml"
DIAGRAM = "diagram"
PROSE = "prose"
LINKED_FORM = "linked"
COMPILED_FORM = "compiled"
AUTHORED_FORM = "authored"
BOOTSTRAP = "bootstrap"
FORMS = (DIAGRAM, PROSE, LINKED_FORM, COMPILED_FORM, AUTHORED_FORM, BOOTSTRAP)
BOOTSTRAP_DIR = "skill"
"""The directory a bootstrap form's SKILL.md sits in, beside its documents."""

SOURCE_DIR = "sources"
"""The directory a bootstrap skill's documents sit in, inside the skill."""

FORM_DIR = {form: form for form in FORMS} | {BOOTSTRAP: BOOTSTRAP_DIR}
"""The directory each form's tree sits in.

A bootstrap form's tree is its skill, which carries the documents it names.
"""
"""The directory each form's document tree sits in.

A bootstrap form's documents sit beside its skill, so the workflow is read
from them while the skill that names them sits apart.
"""
SHELL_FORMS = (BOOTSTRAP,)
"""The forms a session runs a command to read, which no other form needs."""

BUNDLES = "workflow.bundles"
DISPATCH_FORMS = (COMPILED_FORM, AUTHORED_FORM)
DRAWN = (DIAGRAM, COMPILED_FORM)
"""The forms whose entry documents draw the workflow, in the order they are tried.

A workflow drawing a diagram form holds it there; one written in the two
dispatch forms holds the same diagram in its compiled form's entry, since
both forms draw the workflow and only the compiled one's entry dispatches.
"""

TRANSITION = {
    DIAGRAM: DIAGRAM,
    PROSE: PROSE,
    LINKED_FORM: LINKED_FORM,
    COMPILED_FORM: DIAGRAM,
    AUTHORED_FORM: DIAGRAM,
    BOOTSTRAP: DIAGRAM,
}
"""The form whose transition sentences a form's sections are written in.

A dispatch form draws the workflow as its diagram form does, so each
section's transition names the edge's label or takes the one edge out of
its state, and only the step handing a section to a sub-agent is its own.
"""

START = "start"
STOP = "stop"
ENTRY_PLACEHOLDER = "ENTRY"
SKILL_ENTRY = "SKILL.md"
"""The document a bootstrap session is told to read."""
STEP_LIMIT = 100

DISPATCH_OPERATOR = "⇉"
PARALLEL_OPERATOR = "⫽"
RETURNED_DONE = "done"
RETURNED_QUESTION = "question"
RETURNED = (RETURNED_DONE, RETURNED_QUESTION)

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
LINK_TARGET = re.compile(
    rf"\[(?:{DISPATCH_OPERATOR}|{PARALLEL_OPERATOR})?\s*([^\]]+)\]"
    r"\(([^)#]*)(?:#([^)]*))?\)"
)
"""One link a step writes, with its text, document and heading.

The link's text may open with a dispatch operator, which the compiled form
writes and the authored form does not, so both forms' steps read alike.
"""
LINKS = r"((?:\[[^\]]*\]\([^)]*\))(?:\s+and\s+\[[^\]]*\]\([^)]*\))*)\."
"""One step's links, joined by `and` where a set states several."""
OPERATOR_LINK_SRC = rf"\[(?:{DISPATCH_OPERATOR}|{PARALLEL_OPERATOR}) [^\]]*\]\("
"""A link of a compiled step that states its operator."""
COMPILED_STEP = re.compile(rf"^\d+\. .*(?:{OPERATOR_LINK_SRC})")
"""A compiled step: a numbered step whose links carry the operator it dispatches by.

The compiled form's steps state no dispatch in prose, since the operator a
link carries and the protocol `pf` publishes from it are the statement. A
step may carry instruction beyond its links; what it may not do is say what
the operator says.
"""
OPERATOR_LINK = re.compile(rf"\[({DISPATCH_OPERATOR}|{PARALLEL_OPERATOR}) [^\]]*\]\(")
"""Every link of a compiled step that states its operator, with the operator."""
RESTATES = ("sub-agent", "together", "from the question it returned")
"""The words a compiled step may not use, since its protocol states them.

The `Dispatch` protocol says a dispatched run returns each question
unanswered, that the dispatching session puts it to the user and dispatches
again with the answers, and the `Parallel dispatch` protocol says how a
set's questions are answered together. A step repeating any of that is a
second statement of it, and a step carrying both a mark and a sentence is
the ambiguity the two forms are meant to isolate.
"""


def restated(line: str) -> str:
    """The protocol text a compiled step states again, or nothing.

    A step states its dispatch by its operators. What a protocol says a
    dispatch does belongs to the protocol, so a step repeating it leaves the
    reader two statements to reconcile, which is the ambiguity the two forms
    differ by.
    """
    return next((word for word in RESTATES if word in line), "")


STEP_ONE = re.compile(rf"^\d+\. Hand the .+? to a sub-agent: {LINKS}")
STEP_SET = re.compile(rf"^\d+\. Hand the .+? to sub-agents of their own: {LINKS}")
"""An authored step: the protocol it states, then the links it applies to.

The authored form has no operator and no published protocol, so its prose is
the whole statement of what a sub-agent follows and how a returned question
is relayed."""
OPERATOR = re.compile(rf"^\[({DISPATCH_OPERATOR}|{PARALLEL_OPERATOR}) ")
"""The operator a link's text opens with, where it opens with one."""
LABEL_STATEMENT = re.compile(
    r"^The transition labelled `([^`]+)` applies\.$", re.MULTILINE
)
_DIAGRAM_DECISION = re.compile(rf"^If (.+), {LABEL}\. Otherwise, {LABEL}\.$")
_DIAGRAM_ONLY_EDGE = re.compile(rf"^{re.escape(ONLY_EDGE)}$")
DECISION = {
    DIAGRAM: _DIAGRAM_DECISION,
    PROSE: re.compile(rf"^If (.+), {GO_TO}\. Otherwise, {GO_TO}\.$"),
    LINKED_FORM: re.compile(rf"^If (.+), {LINKED}\. Otherwise, {LINKED}\.$"),
    BOOTSTRAP: _DIAGRAM_DECISION,
}
UNCONDITIONAL = {
    DIAGRAM: _DIAGRAM_ONLY_EDGE,
    PROSE: re.compile(r"^Go to \[(\w+)\]\([^)]+\)\.$"),
    LINKED_FORM: _DIAGRAM_ONLY_EDGE,
    BOOTSTRAP: _DIAGRAM_ONLY_EDGE,
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
class Dispatch:
    """One sub-agent start a correct run makes.

    `section` is the document and heading the sub-agent follows, as
    `<document>#<heading>`, since an author and the profile both name the
    target's section rather than the bundle it compiles to. `returned` is
    what it gave back, and `together` marks an entry of a set started
    beside the entry above it.
    """

    section: str
    returned: str
    together: bool


@dataclass(frozen=True)
class Scenario:
    """One run's inputs, the path a correct run walks and its dispatch trace.

    `trace` is empty for a form that dispatches nothing.
    """

    name: str
    inputs: dict[str, str]
    path: tuple[str, ...]
    trace: tuple[Dispatch, ...] = ()


@dataclass(frozen=True)
class Workflow:
    """One workflow: its diagram, each form's sections and its scenarios."""

    name: str
    directory: Path
    diagram: Diagram
    sections: dict[str, dict[str, Section]]
    scenarios: tuple[Scenario, ...]

    def form(self, form: str) -> Path:
        """The directory holding one form's source tree.

        A bootstrap form's documents sit under the skill's `sources`, since
        the skill hands over a directory it compiles rather than a tree it
        hands over whole.
        """
        return form_directory(self.directory, form)

    @property
    def forms(self) -> tuple[str, ...]:
        """The forms this workflow is written in."""
        return tuple(form for form in FORMS if self.form(form).is_dir())

    @property
    def walked(self) -> dict[str, Section]:
        """The sections a run of the workflow walks, for its states' actions.

        A workflow drawing a diagram form walks that form's sections; one
        written in the dispatch forms walks the compiled form's, whose
        sections are the diagram's with the step handing a target added. A
        bootstrap workflow walks the skill it hands over, which is the only
        tree its sessions receive.
        """
        form = next((form for form in (*DRAWN, BOOTSTRAP) if form in self.forms), None)
        if form is None:
            raise CorpusError(f"{self.name} holds no form drawing a workflow")
        return self.sections[form]


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
        Scenario(
            entry["name"],
            dict(entry["inputs"]),
            tuple(entry["path"]),
            tuple(
                Dispatch(row["dispatch"], row["returned"], row.get("together", False))
                for row in entry.get("trace", ())
            ),
        )
        for entry in entries
    )


def form_directory(workflow_directory: Path, form: str) -> Path:
    """The directory one form's documents sit in.

    A bootstrap form's tree is its skill, and its documents sit inside it, so
    a session receives one skill that names the material it compiles.
    """
    directory = workflow_directory / FORM_DIR[form]
    return directory / SOURCE_DIR if form == BOOTSTRAP else directory


def read_workflow(directory: Path) -> Workflow:
    """One workflow directory, read whole.

    A bootstrap workflow draws its diagram in the skill it hands over, since
    that is the only tree a session of that form receives.
    """
    bootstrap = directory / BOOTSTRAP_DIR / SOURCE_DIR / ENTRY
    drawn = (
        bootstrap
        if bootstrap.is_file()
        else next(
            directory / FORM_DIR[form] / ENTRY
            for form in DRAWN
            if (directory / FORM_DIR[form] / ENTRY).is_file()
        )
    )
    return Workflow(
        directory.name,
        directory,
        read_diagram(drawn),
        {
            form: read_sections(form_directory(directory, form), TRANSITION[form])
            for form in FORMS
            if form_directory(directory, form).is_dir()
        },
        read_scenarios(directory / SCENARIOS),
    )


def workflows(root: Path = WORKFLOWS) -> list[Workflow]:
    """Every workflow the corpus holds, in name order."""
    return [read_workflow(path) for path in sorted(root.iterdir()) if path.is_dir()]


def instruction(entry: str, form: str = "") -> str:
    """The task text a session is given, naming the document it reads.

    A bootstrap session is given its own text, which names the skill it reads
    rather than a bundle, since that form's document is a skill that states a
    compile rather than a workflow to follow.
    """
    source = INSTRUCTION_BOOTSTRAP if form == BOOTSTRAP else INSTRUCTION
    blocks: list[str] = [
        body for kind, body in FENCE.findall(source.read_text()) if kind == "text"
    ]
    if len(blocks) != 1:
        raise CorpusError(f"{source} holds {len(blocks)} text blocks, not one")
    return blocks[0].replace(ENTRY_PLACEHOLDER, entry)


def bundle(form_directory: Path, output: Path) -> subprocess.CompletedProcess[bytes]:
    """The `pf` run bundling one form from its entry document under `output`.

    The entry's bundle is `output / ENTRY_BUNDLE` once the run succeeds, and
    every other bundle the run writes sits beside it in the same folder.
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


def bundled(output: Path) -> list[Path]:
    """Every bundle a form's run wrote under `output`, in name order."""
    return sorted(path for path in (output / BUNDLES).glob("*.bundle.md"))


def section_body(directory: Path, document: str, heading: str) -> str:
    """One heading's content within a document, and nothing beside it.

    `directory` is that of the section writing the link, which is where the
    document resolves from. A heading is matched without regard to case,
    since a section names it lower case and the document heads it as a
    title.
    """
    path = (directory / document).resolve()
    if not path.is_file():
        raise CorpusError(f"a dispatch names {document}, which is no document")
    text = path.read_text()
    start = re.search(rf"^#+ {re.escape(heading)}$", text, re.MULTILINE | re.IGNORECASE)
    if start is None:
        raise CorpusError(f"{document} holds no {heading} section")
    rest = text[start.end() :]
    end = re.search(r"^#+ ", rest, re.MULTILINE)
    return rest if end is None else rest[: end.start()]


def dispatched(
    body: str, directory: Path, root: Path, form: str
) -> list[tuple[bool, list[str]]]:
    """The targets a section's steps dispatch, each step's in order.

    A step hands one document to a sub-agent, or several to sub-agents of
    their own, so the pair says whether the step's targets form one set. A
    target is named as `<document>#<heading>`, the section a sub-agent
    follows, since both forms name the section and neither names the bundle
    it compiles to. The document is named from the form's root, `root`,
    though the step writes its link from `directory`, the directory of the
    section writing it. A link resolving to no document, or to a document
    holding no such heading, is a fault.

    A compiled step is read from its operators alone: its links are the
    statement, so a sentence beside them states the dispatch a second time
    and is a fault. An authored step is read from its prose, which is the
    form's only statement of the dispatch.
    """
    steps: list[tuple[bool, list[str]]] = []
    for line in body.splitlines():
        if form == COMPILED_FORM:
            if COMPILED_STEP.match(line) is None:
                continue
            named = LINK_TARGET.findall(line)
            marks = OPERATOR_LINK.findall(line)
            if len(marks) != len(named):
                raise CorpusError(f"a compiled step carries an unmarked link: {line!r}")
            if stated := restated(line):
                raise CorpusError(
                    f"a compiled step states {stated!r}, which its protocol states,"
                    f" rather than its operators alone: {line!r}"
                )
            together = PARALLEL_OPERATOR in marks
        else:
            found = STEP_ONE.match(line) or STEP_SET.match(line)
            if found is None:
                continue
            named = LINK_TARGET.findall(found.group(1))
            together = STEP_SET.match(line) is not None
        targets: list[str] = []
        for _, document, heading in named:
            written = (directory / document).resolve()
            if not written.is_file():
                raise CorpusError(f"a step dispatches {document}, which is no document")
            if not re.search(
                rf"^#+ {re.escape(heading)}$",
                written.read_text(),
                re.MULTILINE | re.IGNORECASE,
            ):
                raise CorpusError(f"{document} holds no {heading} section")
            named = written.relative_to(root.resolve()).with_suffix("")
            targets.append(f"{named.as_posix()}#{heading.lower()}")
        if not targets:
            raise CorpusError(f"a dispatch step names no document: {line!r}")
        if together and len(targets) < 2:
            raise CorpusError(f"a set states one target: {line!r}")
        steps.append((together, targets))
    return steps


def dispatch_walk(
    workflow: Workflow, form: str, inputs: dict[str, str]
) -> tuple[tuple[str, bool], ...]:
    """The sub-agents a correct run of one form starts, in order.

    Each state on the path dispatches the targets its section's steps name,
    and a dispatched section dispatches its own targets in turn, so the walk
    is the source's statement of which sub-agents start, in what order, and
    which of them start together. What each returned is the scenario's to
    state, since it is the sub-agent's to give.
    """
    root = workflow.form(form)
    trace: list[tuple[str, bool]] = []

    def follow(body: str, directory: Path) -> None:
        for together, targets in dispatched(body, directory, root, form):
            for index, target in enumerate(targets):
                trace.append((target, together and index > 0))
                document, _, heading = target.partition("#")
                written = root / f"{document}.md"
                follow(
                    section_body(written.parent, written.name, heading),
                    written.parent,
                )

    for state in walk(workflow, form, inputs):
        section = sections_of(workflow, form)[state]
        follow(section.body, section.path.parent)
    return tuple(trace)


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
    """The input files one form's conditions read.

    A form's sections are written in the transition sentences of the form
    `TRANSITION` names, and they decide on the same conditions whichever of
    those sentences a form uses, so a form this workflow does not hold is
    read from the one writing the same sentences.
    """
    written = form if form in workflow.sections else TRANSITION[form]
    return {
        input_read(section.transition.condition)
        for section in workflow.sections[written].values()
        if section.transition is not None and section.transition.condition is not None
    }


def sections_of(workflow: Workflow, form: str) -> dict[str, Section]:
    """One form's sections, or the sections of the form it is written in."""
    return workflow.sections[form if form in workflow.sections else TRANSITION[form]]


def successor(
    workflow: Workflow, form: str, state: str, inputs: dict[str, str], trace: list[str]
) -> str | None:
    """The state one form's section for a state says comes next, if any."""
    transition = sections_of(workflow, form)[state].transition
    if transition is None:
        return None
    chosen = transition.then
    if transition.condition is not None and not holds(
        transition.condition, inputs, trace
    ):
        chosen = transition.otherwise
    if TRANSITION[form] == PROSE:
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
