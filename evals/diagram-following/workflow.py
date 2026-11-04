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
- `linked/` holds the same state documents beneath the diagram's
  flowchart drawn with no branch label, and a decision section names each
  branch by a rule document. Each rule document states the one state its
  branch enters, so the edge a branch takes is reachable only by following
  the link, and it is held to an edge the diagram draws out of the deciding
  state all the same.
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
section names the document stating the state its edge enters. A
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
`together` on each entry of a set started at once, and the `action` its
section states, as the `file` under `actions/` and the `value` it holds. A
scenario whose sub-agent returns a question states its `answers`, the text
a run writes to `answers.txt` for the session to hand back.
A run writes each input to `inputs/<name>` as the value followed by a
newline, and a condition reads the file with surrounding whitespace removed.

A form is bundled by the `pf` command the environment provides, run from
the form's directory, so the bundle is the one this checkout builds. The
reference `pf` is given is the workflow's entry: `workflow.md`, or the
section of it a top-level `entry` key in `scenarios.toml` names as
`workflow.md#<fragment>`, which leaves the document's other sections out.
`pf` writes its bundle set into a folder named for that entry under the
output folder it is given, `workflow.bundles/` holding `workflow.bundle.md`
for the whole document. A form that dispatches publishes one bundle per
target beside the entry's, so its set is every bundle `pf` writes; a form
that does not publishes the entry's alone. A run reports no diagnostic
beyond the warning codes the workflow's `scenarios.toml` declares under
`warnings`, which a feature such as `subst` raises wherever it is used.

The diagram form's bundle states a path of its own: a state's section is
the heading the previous section's link or the bundle's diagram names, and
what `pf` placed into a group or redirected through `subst` is what that
section holds. A scenario's path is held to that walk as well as to the
sources', so a workflow built on a feature states the path its bundle
states.

A document under an `undeclared/` directory declares no `prosiform`, so a
link to it is left as written rather than followed; every other document
declares.
"""

import re
import shutil
import subprocess
import tomllib
from dataclasses import dataclass, field, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKFLOWS = ROOT / "workflows"
INSTRUCTION = ROOT / "instruction.md"
INSTRUCTION_BOOTSTRAP = ROOT / "instruction-bootstrap.md"

ENTRY = "workflow.md"
UNDECLARED = "undeclared"
"""The directory whose documents declare no `prosiform`, so a link to one stays text."""
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
MARKED_FORMS = (COMPILED_FORM, BOOTSTRAP)
"""The forms whose dispatch steps are written as marked links and no prose.

A bootstrap skill's documents are the ones its compiled bundle carries, so a
step states its dispatch by its marks there as it does in the compiled form.
"""
SHELL_FORMS = (BOOTSTRAP,)
"""The forms a session runs a command to read, which no other form needs."""

DISPATCH_FORMS = (COMPILED_FORM, AUTHORED_FORM)
UNDRAWN = (PROSE,)
"""The forms whose entry document draws no diagram.

A prose section names the state that comes next, so a diagram beside it
would be a second statement of every edge and the form would no longer
isolate what the diagram adds.
"""
UNLABELLED = (LINKED_FORM,)
"""The forms whose entry document draws no branch label.

A linked decision names the rule stating the state its branch enters, so a
label on the entry's flowchart would let a session choose the branch without
opening the rule, and the form would no longer measure whether a decision is
resolved by following its link.
"""
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
NODE = r"(\w+)(?:(?:\(+[^)]*\)+)|(?:\{[^}]*\})|(?:\[[^\]]*\]))?"
EDGE = re.compile(rf"^\s*{NODE}\s*-->\s*(?:\|([^|]*)\|\s*)?{NODE}\s*$")
SHAPE = re.compile(
    r"""^(\w+)(?:(?:\(+(?P<round>.+?)\)+)"""
    r"""|(?:\{(?:["']?)(?P<diamond>.+?)(?:["']?)\})"""
    r"""|(?:\[(?:["']?)(?P<box>.+?)(?:["']?)\]))?$"""
)
"""A node's name and its shape.

A diamond is a decision, a rectangle a state, and a rounded node a marker, so
the shape alone states which kind a node is.
"""
ROUND = 1
DIAMOND = 3
BOX = 2
"""The shape each bracket pair states: a marker, a decision and a state."""
CLICK = re.compile(r'^\s*click\s+(\w+)\s+(?:href\s+)?"([^"]*)"')
HEADING = re.compile(r"^# (\w+)\n")
FRONTMATTER = re.compile(r"\A---\n.*?^---\n", re.DOTALL | re.MULTILINE)
"""The declaration block every workflow document opens with, which `pf` strips."""
NEXT = "**Next.** "
ACTION = re.compile(r"^Write `actions/([^`]+)` containing `([^`]*)`\.$", re.MULTILINE)
TERMINAL = "The workflow is complete."
LABEL = r"take the transition labelled `([^`]+)`"
GO_TO = r"go to \[(\w+)\]\([^)]+\)"
LINKED = r"take the transition \[([^\]]+)\]\(([^)]+)\) names"
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
RULE_STATEMENT = re.compile(r"^The transition into `(\w+)` applies\.$", re.MULTILINE)
_DIAGRAM_DECISION = re.compile(rf"^If (.+), {LABEL}\. Otherwise, {LABEL}\.$")
DECISION = {
    DIAGRAM: _DIAGRAM_DECISION,
    PROSE: re.compile(rf"^If (.+), {GO_TO}\. Otherwise, {GO_TO}\.$"),
    LINKED_FORM: re.compile(rf"^If (.+), {LINKED}\. Otherwise, {LINKED}\.$"),
    BOOTSTRAP: _DIAGRAM_DECISION,
}
UNCONDITIONAL = {
    PROSE: re.compile(r"^Go to \[(\w+)\]\([^)]+\)\.$"),
}
READS = re.compile(r"^`inputs/([^`]+)` reads `([^`]*)`$")
FEWER = re.compile(
    r"^`trace\.log` holds the line `(\w+)` fewer times than the number in "
    r"`inputs/([^`]+)`$"
)
DIAGNOSTIC = re.compile(r"^([EW]_[A-Z_]+):", re.MULTILINE)
"""The code opening each diagnostic `pf` writes to its standard error."""

BUNDLE_HEADING = re.compile(r"^(#{1,6}) (.+?)[ \t]*$", re.MULTILINE)
"""A heading of a bundle, at any level, with its text."""

SLUG_DISCARDED = re.compile("[\u0000-\u001f!-,./:-@[-^`{-~]")
"""The characters a renderer drops from a heading's text in making its slug."""

FRAGMENT_LINK = re.compile(r"\[([^\]]+)\]\(#([^)]+)\)")
"""A link a bundle rewrote to a heading of its own, with its text and fragment."""

NEXT_PARAGRAPH = re.compile(rf"^{re.escape(NEXT)}(.+)$", re.MULTILINE)
"""A section's transition paragraph as a bundle carries it."""


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
    shapes: dict[str, int] = field(default_factory=dict)
    """Each node's shape, as the group `SHAPE` captures its label in."""
    labels: dict[str, str] = field(default_factory=dict)
    """Each node's label, which states whether it is a condition."""

    @property
    def transitions(self) -> frozenset[str]:
        """The nodes stating when an edge applies: a decision's escapes.

        A decision is a diamond, and each edge out of it reaches a condition
        whose name ends `?`, whose section states the criterion for that
        escape. The condition is what a run reads, so the two together are the
        routing the diagram states.
        """
        return frozenset(
            name
            for name in self.conditions
            if any(edge.source == name for edge in self.edges)
        )

    @property
    def conditions(self) -> frozenset[str]:
        """Every node a decision points at, its escape criterion.

        A decision asks its question, and each edge out of it reaches a
        condition whose section states when that escape applies. The
        condition is a plain box: the question mark belongs to the diamond,
        and the box states a condition that is true for the path it begets.
        """
        escapes: set[str] = set()
        for decision in self.decisions:
            escapes |= {edge.target for edge in self.leaving(decision)}
        return frozenset(
            name
            for name in escapes
            if name not in {START, STOP} and self.shapes.get(name) != DIAMOND
        )

    @property
    def decisions(self) -> frozenset[str]:
        """Every node the diagram draws as a diamond, asking what it weighs."""
        return frozenset(node for node in self.shapes if self.shapes[node] == DIAMOND)

    def through(self, node: str) -> bool:
        """Whether a node joins one state to another, one hop either side."""
        return any(edge.target == node for edge in self.edges) and any(
            edge.source == node for edge in self.edges
        )

    @property
    def states(self) -> frozenset[str]:
        """Every state of the diagram, its decisions and conditions excepted."""
        nodes = {edge.source for edge in self.edges} | {
            edge.target for edge in self.edges
        }
        return frozenset(nodes - {START, STOP} - self.transitions - self.decisions)

    def leaving(self, state: str) -> tuple[Edge, ...]:
        """The edges out of one node, the edge to the stop marker excepted.

        A decision's edges reach its conditions, and each condition's own edge
        reaches the state its escape enters, so the diagram's edges are read as
        drawn and the walker follows them node by node.
        """
        return tuple(
            edge for edge in self.edges if edge.source == state and edge.target != STOP
        )


@dataclass(frozen=True)
class Transition:
    """A section's transition: where to go, under which condition.

    `then` and `otherwise` are edge labels in the diagram form and state names
    in the prose form and in the linked form's decisions. An unconditional
    transition carries no condition and no `otherwise`; in the diagram form
    it carries no label either, since it takes the one edge out of its
    state.
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
    target's section rather than the bundle it compiles to. `together` marks
    an entry of a set started beside the entry above it. `action` is the
    file under `actions/` the section has the sub-agent write and the value
    it holds; a section stating no action carries none, and nothing is
    checked for it.
    """

    section: str
    together: bool
    action: tuple[str, str] | None = None


@dataclass(frozen=True)
class Scenario:
    """One run's inputs, the path a correct run walks and its dispatch trace.

    `trace` is empty for a form that dispatches nothing. `answers` is what a
    run writes to `answers.txt`, the user's answers to a question a
    sub-agent returns; it is empty where no sub-agent asks, and no file is
    written.
    """

    name: str
    inputs: dict[str, str]
    path: tuple[str, ...]
    trace: tuple[Dispatch, ...] = ()
    answers: str = ""


@dataclass(frozen=True)
class Workflow:
    """One workflow: its diagram, each form's sections and its scenarios."""

    name: str
    directory: Path
    diagram: Diagram
    sections: dict[str, dict[str, Section]]
    scenarios: tuple[Scenario, ...]
    transitions: dict[str, Transition] = field(default_factory=dict)
    """Each condition's criterion, for a workflow that draws its decisions."""

    conditions: dict[str, Transition] = field(default_factory=dict)
    """Each condition's criterion, keyed by its node's name."""

    nested: tuple[str, ...] = ()
    """Each criterion a nested chart states, read from the section holding it."""

    entry: str = ENTRY
    """The reference every form is compiled from: the entry document or one section."""

    warnings: frozenset[str] = frozenset()
    """The warning codes `pf` reports bundling this workflow, as it declares them."""

    @property
    def entry_bundle(self) -> Path:
        """Where the entry's bundle sits under a form's output folder."""
        return entry_bundle(self.entry)

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
    return mermaid_text(entry.read_text(), str(entry))


def mermaid_text(text: str, named: str = "the bundle") -> str:
    """The one Mermaid diagram a document's text holds."""
    blocks: list[str] = [
        body for kind, body in FENCE.findall(text) if kind == "mermaid"
    ]
    if len(blocks) != 1:
        raise CorpusError(f"{named} holds {len(blocks)} mermaid diagrams, not one")
    return blocks[0]


def node_shape(text: str) -> tuple[str, int, str]:
    """One node's name, the shape its brackets state, and its label.

    Round brackets are a marker, braces a diamond and square brackets a
    rectangle, which is what Mermaid draws for each.
    """
    if not (found := SHAPE.match(text.strip())):
        raise CorpusError(f"no node reads as {text!r}")
    name = found.group(1)
    groups = found.groupdict()
    if groups["round"] is not None:
        return name, ROUND, groups["round"]
    if groups["diamond"] is not None:
        return name, DIAMOND, groups["diamond"]
    return name, BOX, groups["box"] or ""


def read_diagram(entry: Path) -> Diagram:
    """The diagram's edges, start state, terminal states, clicks and shapes."""
    return read_diagram_text(mermaid(entry), entry.parent, str(entry))


def shapes_nodes(edges: list[Edge]) -> set[str]:
    """The nodes an edge leaves, so the one nothing leaves is the entry."""
    return {edge.source for edge in edges}


def read_diagram_text(
    body: str, directory: Path | None = None, named: str = ""
) -> Diagram:
    """One diagram read from its own text, which is a nested chart's form."""
    edges: list[Edge] = []
    clicks: dict[str, str] = {}
    shapes: dict[str, int] = {}
    labels: dict[str, str] = {}
    NODE_SHAPE = re.compile(rf"{NODE}")
    for line in body.splitlines():
        if edge := EDGE.match(line):
            source, label, target = edge.group(1), edge.group(2), edge.group(3)
            edges.append(Edge(source, target, label))
            for match in NODE_SHAPE.finditer(line):
                name, shape, stated = node_shape(match.group(0))
                shapes.setdefault(name, shape)
                labels.setdefault(name, stated)
        elif click := CLICK.match(line):
            clicks[click.group(1)] = click.group(2)
    starts = [edge.target for edge in edges if edge.source == START]
    if len(starts) != 1:
        raise CorpusError(f"{named}: {START} points at {len(starts)} states, not one")
    terminals = frozenset(edge.source for edge in edges if edge.target == STOP)
    return Diagram(starts[0], tuple(edges), terminals, clicks, shapes, labels)


def ruled_state(directory: Path, destination: str) -> str:
    """The state a rule document states its branch enters.

    A linked transition names a document rather than a state or a label, so
    the edge a branch takes is the one into the state that document states.
    `directory` is that of the section writing the link, which is where the
    document resolves from.
    """
    target = directory / destination
    if not target.is_file():
        raise CorpusError(f"a transition links {destination}, which is no document")
    found = None
    for match in RULE_STATEMENT.finditer(target.read_text()):
        if found is not None:
            raise CorpusError(f"{destination} states more than one state")
        found = match.group(1)
    if found is None:
        raise CorpusError(f"{destination} states no state")
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
                ruled_state(directory, then_path),
                ruled_state(directory, otherwise_path),
            )
        condition, then, otherwise = decision.groups()
        input_read(condition)
        return Transition(condition, then, otherwise)
    plain = UNCONDITIONAL.get(form)
    if plain is not None and (unconditional := plain.match(text)):
        target = unconditional.group(1) if unconditional.groups() else None
        return Transition(None, target, None)
    raise CorpusError(f"no {form} transition reads as {text!r}")


CONDITION = re.compile(r"^`inputs/([^`]+)` reads `([^`]*)`\.$", re.MULTILINE)
FEWER_CONDITION = re.compile(
    r"^`trace\.log` holds the line `(\w+)` fewer times than the number in "
    r"`inputs/([^`]+)`\.$",
    re.MULTILINE,
)
"""A transition section's statement of when its edge applies.

A transition drawn as a node is clicked to a section holding one condition and
nothing else, so the condition reads as a sentence about the inputs rather
than as half of a sentence naming two labels.
"""


def authored(path: Path) -> str:
    """One workflow document's text after its declaration block, as bundled."""
    return FRONTMATTER.sub("", path.read_text(), count=1)


def read_condition(path: Path) -> Transition:
    """One transition section's condition, and the edge it takes.

    The section states when its transition applies, and the node it is clicked
    from names the edge: a section naming no condition is the one edge out of
    its state, taken though the diagram draws it as a transition node.
    """
    text = authored(path)
    body = HEADING.sub("", text, count=1).strip()
    if not body:
        return Transition(None, None, None)
    if reads := CONDITION.search(body):
        name, value = reads.groups()
        return Transition(f"`inputs/{name}` reads `{value}`", None, None)
    if fewer := FEWER_CONDITION.search(body):
        state, name = fewer.groups()
        return Transition(
            f"`trace.log` holds the line `{state}` fewer times than the number "
            f"in `inputs/{name}`",
            None,
            None,
        )
    raise CorpusError(f"{path} states no condition, and no absence of one")


def read_section(form: str, path: Path, directory: Path) -> Section:
    """One state's document, split into its shared body and its transition."""
    text = authored(path)
    heading = HEADING.match(text)
    if heading is None:
        raise CorpusError(f"{path} opens with no state heading")
    body, marker, transition = text.rpartition(f"\n{NEXT}")
    if not marker:
        body, transition = text, ""
    actions = ACTION.findall(body)
    if len(actions) != 1:
        raise CorpusError(f"{path} states {len(actions)} actions, not one")
    return Section(
        heading.group(1),
        path,
        body,
        actions[0],
        parse_transition(form, transition.strip(), path.parent) if marker else None,
    )


def read_conditions(
    diagram: Diagram, clicks: dict[str, str], root: Path
) -> dict[str, Transition]:
    """Each condition's criterion, read from the section it clicks.

    A decision weighs something and each of its escapes is a condition whose
    name ends `?`, clicked to the section stating when that escape applies.
    The condition is read, not the decision: the diagram states what is
    decided and the section states the criterion that decides it.
    """
    found: dict[str, Transition] = {}
    for node in sorted(diagram.conditions):
        destination = clicks.get(node)
        if destination is None:
            raise CorpusError(f"{node} is a condition naming no section")
        document = destination.partition("#")[0] or f"{node}.md"
        written = (root / document).resolve()
        if not written.is_file():
            raise CorpusError(f"{node} clicks {destination!r}, which names no document")
        transition = read_condition(written)
        if transition.condition is None:
            raise CorpusError(f"{written} states no criterion for {node}")
        found[node] = Transition(transition.condition, node, None)
    return found


def read_sections(form_directory: Path, form: str) -> dict[str, Section]:
    """Every state document of one form, by state name."""
    sections = [
        read_section(form, path, form_directory)
        for path in sorted((form_directory / STATES).glob("*.md"))
    ]
    return {section.state: section for section in sections}


def entry_bundle(entry: str) -> Path:
    """The entry's bundle under an output folder, by the name `pf` derives.

    A selection's name is its path without the Markdown suffix, each
    separator written as `_`, and a section adds `__` and its fragment. The
    run's folder takes that name with `.bundles`, and the entry's bundle with
    `.bundle.md`.
    """
    document, _, fragment = entry.partition("#")
    name = Path(document).with_suffix("").as_posix().replace("/", "_")
    if fragment:
        name = f"{name}__{fragment}"
    return Path(f"{name}.bundles", f"{name}.bundle.md")


def read_entry(path: Path) -> str:
    """The reference a workflow's `scenarios.toml` names its forms' entry by."""
    with path.open("rb") as handle:
        return str(tomllib.load(handle).get("entry", ENTRY))


def read_warnings(path: Path) -> frozenset[str]:
    """The warning codes a workflow's `scenarios.toml` declares its bundle raises.

    A feature such as `subst` warns wherever it is used, so a workflow built
    on it declares each code it expects, and its bundle is held to raising
    those and no other diagnostic.
    """
    with path.open("rb") as handle:
        return frozenset(tomllib.load(handle).get("warnings", ()))


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
                Dispatch(
                    row["dispatch"],
                    row.get("together", False),
                    (row["action"]["file"], row["action"]["value"])
                    if "action" in row
                    else None,
                )
                for row in entry.get("trace", ())
            ),
            entry.get("answers", ""),
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
    diagram = read_diagram(drawn)
    drawn_root = drawn.parent
    workflow = Workflow(
        directory.name,
        directory,
        diagram,
        {
            form: read_sections(form_directory(directory, form), TRANSITION[form])
            for form in FORMS
            if form_directory(directory, form).is_dir()
        },
        read_scenarios(directory / SCENARIOS),
        conditions=read_conditions(diagram, diagram.clicks, drawn_root)
        if diagram.conditions
        else {},
        entry=read_entry(directory / SCENARIOS),
        warnings=read_warnings(directory / SCENARIOS),
    )
    return replace(workflow, nested=nested_conditions(workflow, drawn_root))


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


def bundle(
    workflow: Workflow, form: str, output: Path
) -> subprocess.CompletedProcess[bytes]:
    """The `pf` run bundling one form from the workflow's entry under `output`.

    The entry's bundle is `output / workflow.entry_bundle` once the run
    succeeds, and every other bundle the run writes sits beside it in the
    same folder.
    """
    command = shutil.which("pf")
    if command is None:
        raise CorpusError("no pf command is on the path to bundle a form with")
    return subprocess.run(
        [command, workflow.entry, "-o", str(output)],
        cwd=workflow.form(form),
        capture_output=True,
        check=False,
    )


def bundled(output: Path) -> list[Path]:
    """Every bundle a form's run wrote under `output`, in name order.

    A run writes one folder of its own, so every bundle sits in the one
    folder under `output`.
    """
    return sorted(output.glob("*.bundles/*.bundle.md"))


def stray(workflow: Workflow, stderr: bytes) -> str:
    """The diagnostics a form's run reported beyond the warnings its workflow declares.

    `pf` writes each diagnostic as a line opening with its code, followed by
    lines of detail, so a diagnostic is the text from one code to the next.
    Text before the first code is stray whatever it says.
    """
    text = stderr.decode()
    starts = [match.start() for match in DIAGNOSTIC.finditer(text)]
    kept = [text[: starts[0]] if starts else text]
    for start, end in zip(starts, [*starts[1:], len(text)], strict=False):
        block = text[start:end]
        if block.partition(":")[0] not in workflow.warnings:
            kept.append(block)
    return "".join(kept)


def reported(stderr: bytes) -> set[str]:
    """Every diagnostic code a run reported."""
    return {match.group(1) for match in DIAGNOSTIC.finditer(stderr.decode())}


@dataclass(frozen=True)
class BundledSection:
    """One heading of a bundle, the fragment naming it and the text it holds.

    `text` runs to the next heading at its level or above, less any subsection
    holding an action of its own, which is another state's section placed
    inside this one.
    """

    level: int
    title: str
    fragment: str
    text: str


def slug(title: str) -> str:
    """The fragment a renderer generates for a heading carrying this text."""
    return SLUG_DISCARDED.sub("", title.lower()).replace(" ", "-")


def bundled_sections(bundle_text: str) -> dict[str, BundledSection]:
    """Every heading a bundle carries outside its code blocks, by its fragment.

    A later heading taking a slug an earlier one took carries the next free
    ordinal, as the renderer numbers it and `pf` rewrites a link to it.
    """
    fenced = [match.span() for match in FENCE.finditer(bundle_text)]
    found = [
        match
        for match in BUNDLE_HEADING.finditer(bundle_text)
        if not any(start <= match.start() < end for start, end in fenced)
    ]
    counted: dict[str, int] = {}
    taken: set[str] = set()
    fragments: list[str] = []
    for match in found:
        name = slug(match.group(2))
        if name in taken:
            ordinal = counted.get(name, 0) + 1
            while f"{name}-{ordinal}" in taken:
                ordinal += 1
            counted[name] = ordinal
            name = f"{name}-{ordinal}"
        else:
            counted[name] = 0
        taken.add(name)
        fragments.append(name)
    levels = [len(match.group(1)) for match in found]
    ends = [
        next(
            (
                found[later].start()
                for later in range(index + 1, len(found))
                if levels[later] <= levels[index]
            ),
            len(bundle_text),
        )
        for index in range(len(found))
    ]
    sections: dict[str, BundledSection] = {}
    for index, match in enumerate(found):
        end = next(
            (
                found[inner].start()
                for inner in range(index + 1, len(found))
                if found[inner].start() < ends[index]
                and ACTION.search(bundle_text, found[inner].end(), ends[inner])
            ),
            ends[index],
        )
        sections[fragments[index]] = BundledSection(
            levels[index],
            match.group(2),
            fragments[index],
            bundle_text[match.end() : end],
        )
    return sections


def bundle_walk(
    workflow: Workflow, bundle_text: str, inputs: dict[str, str]
) -> tuple[tuple[str, ...], list[str]]:
    """The path a diagram form's bundle states for the inputs, and its faults.

    The walk reads the bundle alone, as a session given it does: the
    bundle's diagram names each edge, its clicks name the first state's
    section, and each state is entered at the section the previous state's
    own link names, or else at the one the diagram clicks. Each section
    states its action and its transition, so what `pf` placed, redirected or
    substituted is what the walk follows. A state whose bundled action is
    not the one its source states is a fault, since the scorer holds a
    session to the source's.
    """
    diagram = read_diagram_text(mermaid_text(bundle_text), named="the bundle")
    sections = bundled_sections(bundle_text)
    path: list[str] = []
    state = diagram.start
    fragment = diagram.clicks.get(state, "").removeprefix("#")
    while True:
        if len(path) == STEP_LIMIT:
            return tuple(path), [f"no terminal state in {STEP_LIMIT}"]
        path.append(state)
        section = sections.get(fragment)
        if section is None or section.title != state:
            return tuple(path), [f"the bundle heads no {state} section at #{fragment}"]
        actions = ACTION.findall(section.text)
        if len(actions) != 1:
            return tuple(path), [f"the bundle's {state} states {len(actions)} actions"]
        faults = []
        if actions[0] != workflow.walked[state].action:
            faults.append(
                f"the bundle's {state} writes {actions[0]}, not"
                f" {workflow.walked[state].action}"
            )
        stated = NEXT_PARAGRAPH.findall(section.text)
        # A decision is a node of the diagram in its own right, so the state
        # before one states the branch to take. A plain state has one edge
        # out, which the diagram already states, so its section states no
        # transition. A terminal state has no edge, so it states completion.
        if len(stated) > 1:
            return tuple(path), [
                *faults,
                f"the bundle's {state} states {len(stated)} transitions",
            ]
        deciding = len(diagram.leaving(state)) > 1
        if deciding and not stated:
            return tuple(path), [
                *faults,
                f"the bundle's {state} decides and states no transition",
            ]
        if not stated:
            edges = diagram.leaving(state)
            if not edges:
                # The state leads nowhere: it is terminal, and a terminal
                # state states that the workflow is complete.
                return tuple(path), [
                    *faults,
                    f"the bundle's {state} is terminal and states no completion",
                ]
            if len(edges) != 1:
                return tuple(path), [
                    *faults,
                    f"the bundle's {state} states no transition and has "
                    f"{len(edges)} edges",
                ]
            if faults:
                return tuple(path), faults
            state = edges[0].target
            linked = [
                target
                for text, target in FRAGMENT_LINK.findall(section.text)
                if text == state
            ]
            fragment = (
                linked[0] if linked else diagram.clicks.get(state, "").removeprefix("#")
            )
            continue
        transition = parse_transition(DIAGRAM, stated[0].strip())
        if transition is None:
            return tuple(path), faults
        chosen = transition.then
        if transition.condition is not None and not holds(
            transition.condition, inputs, path
        ):
            chosen = transition.otherwise
        targets = [
            edge.target for edge in diagram.leaving(state) if edge.label == chosen
        ]
        if len(targets) != 1:
            return tuple(path), [*faults, f"the bundle's {state} has no edge {chosen}"]
        if faults:
            return tuple(path), faults
        state = targets[0]
        linked = [
            target
            for text, target in FRAGMENT_LINK.findall(section.text)
            if text == state
        ]
        fragment = (
            linked[0] if linked else diagram.clicks.get(state, "").removeprefix("#")
        )


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
        if form in MARKED_FORMS:
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


def nested_inputs(workflow: Workflow) -> set[str]:
    """The inputs a workflow's nested charts read, beside its own.

    A dispatched section may carry a chart of its own, whose conditions read
    inputs as the outer ones do. Those files are the run's too, so a scenario
    states them beside the outer workflow's.
    """
    found: set[str] = set()
    for condition in workflow.nested:
        found.add(input_read(condition))
    return found


def nested_conditions(workflow: Workflow, root: Path) -> tuple[str, ...]:
    """Every criterion a nested chart states, from the sections it clicks.

    A dispatched section's body may draw a workflow of its own, with the same
    diamonds and `?` conditions the outer diagram uses. Its conditions are read
    as the outer ones are: each hovered node clicks a document stating one
    criterion, resolved from the section that writes the chart.
    """
    found: list[str] = []
    entry = root / ENTRY
    for document in sorted(root.rglob("*.md")):
        if document == entry:
            continue
        text = document.read_text(errors="replace")
        for kind, body in FENCE.findall(text):
            if kind != "mermaid" or "flowchart" not in body:
                continue
            try:
                drawn = read_diagram_text(body, document.parent, str(document))
            except CorpusError:
                continue
            for condition in sorted(drawn.conditions):
                destination = drawn.clicks.get(condition)
                if destination is None:
                    continue
                written = document.parent / destination.partition("#")[0]
                if not written.is_file():
                    continue
                statement = read_condition(written)
                if statement.condition is not None:
                    found.append(statement.condition)
    return tuple(found)


def dispatch_walk(
    workflow: Workflow, form: str, inputs: dict[str, str]
) -> tuple[tuple[str, bool], ...]:
    """The sub-agents a correct run of one form starts, in order.

    Each state on the path dispatches the targets its section's steps name,
    and a dispatched section dispatches its own targets in turn, so the walk
    is the source's statement of which sub-agents start, in what order, and
    which of them start together. What each returns is the sub-agent's to
    give, and a returned question's second start is the session's answer to
    it, so neither is part of the walk.
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
    if workflow.conditions:
        found = {
            input_read(condition.condition)
            for condition in workflow.conditions.values()
            if condition.condition is not None
        }
        return found | nested_inputs(workflow)
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
    if workflow.diagram.decisions:
        return drawn_successor(workflow, state, inputs, trace)
    transition = sections_of(workflow, form)[state].transition
    if transition is None:
        # A plain state states no transition: the diagram's one edge is its
        # transition. A decision's section states the branch it takes, and a
        # terminal state states no edge at all.
        leaving = workflow.diagram.leaving(state)
        if TRANSITION[form] == PROSE or len(leaving) != 1:
            return None
        return leaving[0].target
    chosen = transition.then
    if transition.condition is not None and not holds(
        transition.condition, inputs, trace
    ):
        chosen = transition.otherwise
    if TRANSITION[form] == PROSE:
        return chosen
    leaving = workflow.diagram.leaving(state)
    if TRANSITION[form] == LINKED_FORM and transition.condition is not None:
        targets = [edge.target for edge in leaving if edge.target == chosen]
        named = f"into {chosen!r}"
    else:
        targets = [edge.target for edge in leaving if edge.label == chosen]
        named = f"labelled {chosen!r}"
    if len(targets) != 1:
        raise CorpusError(f"{workflow.name}: {state} has {len(targets)} edges {named}")
    return targets[0]


def drawn_successor(
    workflow: Workflow, state: str, inputs: dict[str, str], trace: list[str]
) -> str | None:
    """The state the diagram's conditions choose out of one state.

    A state's edge goes to a decision, a decision's edges go to its conditions,
    and each condition states the criterion for its escape. The condition whose
    criterion holds decides, and its own edge names the state reached. A state
    whose edge reaches no decision takes that edge.
    """
    edges = workflow.diagram.leaving(state)
    if not edges:
        return None
    for edge in edges:
        if edge.target not in workflow.diagram.decisions:
            return edge.target
        for escape in workflow.diagram.leaving(edge.target):
            condition = workflow.conditions.get(escape.target)
            if condition is None:
                return escape.target
            if holds(condition.condition or "", inputs, trace):
                reached = workflow.diagram.leaving(escape.target)
                return reached[0].target if reached else None
    raise CorpusError(f"{workflow.name}: no condition out of {state} holds")


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
