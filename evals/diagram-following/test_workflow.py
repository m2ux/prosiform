"""Hold the diagram-following corpus to what the eval relies on.

Every workflow document declares `prosiform` as a mapping of presets;
every form a workflow is written in bundles cleanly, reporting only the
warnings it declares, and carries every state's section, and its entry
carries only what its form allows; the forms' sections differ only in their
transition paragraphs, and a dispatch form's in the step handing a section
to a sub-agent too; and each scenario's path is a walk of the diagram from
its start to a terminal state that every form's sections lead through for
the scenario's inputs, and the diagram form's bundle states, with the
dispatch trace its sources state, `pf` runs naming documents its sources
hold, and each sub-agent's actions the material its own runs compile
states. Each property is a function returning the faults it finds, so the
corpus is held to an empty list and a copy of it broken on purpose is held
to a fault.
"""

import itertools
import json
import re
import shlex
import shutil
import sys
from dataclasses import replace
from pathlib import Path

import pytest
from harness import Start
from ruamel.yaml import YAML
from run import errored
from score import ACTIONS, SUB_AGENT_TRACE, SUBAGENTS, TRACE, Failure, score
from workflow import (
    ACTION,
    AUTHORED_FORM,
    BOOTSTRAP,
    BOOTSTRAP_DIR,
    COMPILED_FORM,
    COMPILED_STEP,
    DIAGRAM,
    DISPATCH_FORMS,
    EDGE,
    ENTRY,
    FENCE,
    FEWER,
    FORMS,
    FRONTMATTER,
    LINKED_FORM,
    MARKED_FORMS,
    PROSE,
    SKILL_ENTRY,
    STATES,
    STEP_ONE,
    STEP_SET,
    TRANSITION,
    UNDECLARED,
    UNDRAWN,
    UNLABELLED,
    WORKFLOWS,
    Compile,
    CorpusError,
    Scenario,
    Workflow,
    activated,
    authored,
    bundle,
    bundle_walk,
    bundled,
    bundled_sections,
    compile_faults,
    compile_reference,
    compiled_walk,
    deferred_links,
    dispatch_starts,
    dispatch_walk,
    dispatched,
    effective_presets,
    entry_bundle,
    fragment_links,
    inline_lines,
    inputs_read,
    instruction,
    markdown_links,
    read_compile,
    read_dispatch,
    read_workflow,
    reported,
    section_body,
    stray,
    walk,
    workflows,
)

BUNDLED_HEADING = re.compile(r"^#+ (\w+)$", re.MULTILINE)
RUN_PF = "Run `pf`, then follow the guidance it prints."
"""The instruction `pf` writes under every bundle's `§ Instructions` heading."""
INSTRUCTIONS = "# § Instructions"


def opens_with_run_pf(text: str) -> bool:
    """Whether a bundle opens with `pf`'s instruction group and its run-pf line.

    `pf` puts the line in a generated `§ Instructions` group ahead of the
    document it compiled, so the line follows that heading rather than being
    the file's first line.
    """
    lines = [line for line in text.splitlines() if line.strip()]
    return (
        len(lines) > 1
        and lines[0].strip() == INSTRUCTIONS
        and lines[1].strip().startswith(RUN_PF)
    )


DISPATCH_LINK = re.compile(r"\[⇉ [^\]]*\]\(([^)]+)\)")
"""A link a bundle publishes to the file `pf` compiled for a dispatched target."""
CORPUS = workflows()
DISPATCHING = [workflow for workflow in CORPUS if AUTHORED_FORM in workflow.forms]
DRAWING = [workflow for workflow in CORPUS if DIAGRAM in workflow.forms]
COMPILING = [workflow for workflow in CORPUS if COMPILED_FORM in workflow.forms]
BOOTSTRAPPING = [workflow for workflow in CORPUS if BOOTSTRAP in workflow.forms]
LINKING = [workflow for workflow in CORPUS if LINKED_FORM in workflow.forms]
FEATURES = ["group-placement", "preset-selection", "subst-redirect"]
"""The workflows whose sources use a feature that changes what `pf` emits."""


def document(state: str) -> str:
    """The path of a state's document within a form."""
    return f"{STATES}/{state.lower()}.md"


def declaration_faults(root: Path) -> list[str]:
    """How the workflow documents under `root` fall short of declaring.

    Every document opens with a declaration block whose `prosiform` is a
    mapping, and each key of that mapping names a preset holding a mapping
    of its settings, so `pf` carries the document and reads its settings as
    the build reads a preset. A document under an `undeclared/` directory
    declares nothing, so a link to it is left as written. A skill's
    `SKILL.md` is the entry its agent CLI reads rather than a source `pf`
    compiles, so it may declare nothing too.
    """
    faults = []
    for path in sorted(root.rglob("*.md")):
        where = path.relative_to(root)
        block = FRONTMATTER.match(path.read_text())
        front = YAML(typ="safe", pure=True).load(block.group()[4:-4]) if block else None
        if skill_entry(path) and not (isinstance(front, dict) and "prosiform" in front):
            continue
        if UNDECLARED in where.parts:
            if isinstance(front, dict) and "prosiform" in front:
                faults.append(f"{where} declares prosiform under {UNDECLARED}/")
            continue
        if not isinstance(front, dict) or "prosiform" not in front:
            faults.append(f"{where} declares no prosiform")
            continue
        declared = front["prosiform"]
        if not isinstance(declared, dict):
            faults.append(f"{where} declares prosiform as {declared!r}, not presets")
            continue
        for preset, settings in declared.items():
            if not isinstance(settings, dict):
                faults.append(f"{where} declares prosiform.{preset} outside a preset")
    return faults


def skill_entry(path: Path) -> bool:
    """Whether a document is a bootstrap skill's entry, its `SKILL.md`."""
    return path.name == SKILL_ENTRY and path.parent.name == BOOTSTRAP_DIR


def bundle_faults(workflow: Workflow, form: str, output: Path) -> list[str]:
    """How one form's bundle set falls short of a clean run under `output`.

    The run must exit 0, report each warning its workflow declares and no
    other diagnostic, and write the entry's bundle
    carrying every state. A dispatch form must publish a bundle for each
    document its steps dispatch, and a form that dispatches nothing must
    publish the entry's bundle alone.
    """
    run = bundle(workflow, form, output)
    faults = []
    if run.returncode != 0:
        faults.append(f"pf exited {run.returncode}")
    if extra := stray(workflow, run.stderr):
        faults.append(f"pf reported {extra!r}")
    for code in sorted(workflow.warnings - reported(run.stderr)):
        faults.append(f"pf reported no {code}")
    bundled_written = bundled(output)
    if output / workflow.entry_bundle not in bundled_written:
        faults.append(f"pf wrote {[path.name for path in bundled_written]}")
        return faults
    carried = set(BUNDLED_HEADING.findall((output / workflow.entry_bundle).read_text()))
    for state in sorted(workflow.diagram.states - carried):
        faults.append(f"the {form} bundle carries no section for {state}")
    published = {
        path.name.split("__")[0]
        for path in bundled_written
        if path != output / workflow.entry_bundle
    }
    if form in MARKED_FORMS:
        targets = {
            target.partition("#")[0].replace("/", "_")
            for section in workflow.sections[form].values()
            for _, targets in dispatched(
                section.body, section.path.parent, workflow.form(form), form
            )
            for target in targets
        }
        for target in sorted(targets - published):
            faults.append(f"the {form} set publishes no bundle for {target}")
    elif published:
        faults.append(f"the {form} form publishes bundles for {sorted(published)}")
    return faults


def section_faults(workflow: Workflow) -> list[str]:
    """How a form differs from the diagram beyond its transition paragraphs.

    Every form carries the diagram's states. The prose and linked forms
    carry the same bodies as the diagram and differ in their transitions
    alone. A dispatch form carries the diagram's body with the step handing
    a section to a sub-agent added, so the two dispatch forms' bodies differ
    in that step's operator and the protocol's sentences.
    """
    faults = []
    states = workflow.diagram.states
    for form in workflow.forms:
        if set(workflow.sections[form]) != states:
            faults.append(f"the {form} form's states are not the diagram's")
    if DIAGRAM not in workflow.forms:
        return faults
    drawn = workflow.sections[DIAGRAM]
    for form in (PROSE, LINKED_FORM):
        if form not in workflow.forms:
            continue
        for state in sorted(states & set(workflow.sections[form])):
            written = workflow.sections[form][state]
            if drawn[state].path.name != written.path.name:
                faults.append(f"{state}: the {form} section names another document")
            if drawn[state].body != written.body:
                faults.append(f"{state}: the {form} section differs from the diagram's")
            drawn_section, written_section = drawn[state], written
            # A prose section is the only statement of its transition, so it
            # states one wherever the diagram draws an edge. A diagram section
            # may leave its single edge unstated, and a terminal state states
            # no transition in either form.
            if (
                written_section.transition is None
                and state not in workflow.diagram.terminals
                and len(workflow.diagram.leaving(state)) != 1
            ):
                faults.append(
                    f"{state}: the {form} section states no transition the "
                    f"diagram draws"
                )
            elif (
                drawn_section.transition is not None
                and written_section.transition is not None
                and drawn_section.transition.condition
                != written_section.transition.condition
            ):
                faults.append(
                    f"{state}: the {form} form and the diagram decide on"
                    f" different conditions"
                )
    if (
        PROSE in workflow.forms
        and "```mermaid" in (workflow.form(PROSE) / ENTRY).read_text()
    ):
        faults.append("the prose form carries a diagram")
    return faults


def step_faults(workflow: Workflow, form: str) -> list[str]:
    """How a dispatch form's steps fall short of the sections they name.

    Every target a step names must resolve from the section writing it to a
    document of the same form holding the heading it names, and the compiled
    form must state a step, since a form dispatching nothing states no trace.
    """
    faults = []
    root = workflow.form(form)
    steps = 0
    for state, section in sorted(workflow.sections[form].items()):
        listed = [
            line
            for line in section.body.splitlines()
            if (
                COMPILED_STEP.match(line)
                if form == COMPILED_FORM
                else STEP_ONE.match(line) or STEP_SET.match(line)
            )
        ]
        steps += len(listed)
        try:
            dispatched(section.body, section.path.parent, root, form)
        except CorpusError as error:
            faults.append(f"{state}: {error}")
    if form == COMPILED_FORM and not steps:
        faults.append(f"the {form} form dispatches nothing")
    return faults


def condition_faults(workflow: Workflow) -> list[str]:
    """How a diagram's conditions fall short of the sections they name.

    A decision's edges reach conditions, each condition is clicked to a
    section, and that section states exactly one criterion. A state carries no
    transition of its own, since the diagram is the only statement of routing.
    """
    diagram = workflow.diagram
    faults = []
    for state in sorted(diagram.states):
        for form in workflow.forms:
            if state in workflow.sections.get(form, {}) and (
                workflow.sections[form][state].transition is not None
            ):
                faults.append(f"{state}: the {form} section states its own routing")
    for decision in sorted(diagram.decisions):
        escapes = diagram.leaving(decision)
        if not escapes:
            faults.append(f"{decision}: the decision reaches no condition")
        for escape in escapes:
            if escape.target not in diagram.conditions:
                faults.append(
                    f"{decision}: it reaches {escape.target}, not a condition"
                )
    for condition in sorted(diagram.conditions):
        onward = diagram.leaving(condition)
        if len(onward) != 1:
            faults.append(f"{condition}: it reaches {len(onward)} states, not one")
        if condition not in workflow.conditions:
            faults.append(f"{condition}: no section states its criterion")
    return faults


def transition_faults(workflow: Workflow) -> list[str]:
    """How a section's transition or a click disagrees with the diagram.

    A section naming an edge's label is held to the labels the diagram draws
    leaving its state, and a prose section naming a state, or a linked
    decision's rules naming one, to the states those edges lead to. A
    dispatch form writes its transitions as the diagram form does, so it is
    held to the labels too.
    """
    diagram = workflow.diagram
    faults = []
    if diagram.decisions:
        return condition_faults(workflow)
    for form in workflow.forms:
        for state in sorted(diagram.states & set(workflow.sections[form])):
            leaving = diagram.leaving(state)
            labels = {edge.label for edge in leaving}
            drawn = workflow.sections[form][state].transition
            if workflow.sections[form][state].deferred:
                continue
            if drawn is None:
                # A plain state states no transition: its one edge is the
                # diagram's. A state that ends the workflow states completion.
                if state not in diagram.terminals:
                    if len(leaving) != 1:
                        faults.append(
                            f"{state}: the {form} section states no transition "
                            f"and the diagram draws {len(leaving)} edges"
                        )
                continue
            if state in diagram.terminals:
                faults.append(
                    f"{state}: the diagram ends at a state whose section does not"
                )
            if TRANSITION[form] == PROSE:
                named = {drawn.then, drawn.otherwise} - {None}
                if named != {edge.target for edge in leaving}:
                    faults.append(
                        f"{state}: the prose names states the diagram does not"
                    )
            elif TRANSITION[form] == LINKED_FORM and drawn.condition is not None:
                if {drawn.then, drawn.otherwise} != {edge.target for edge in leaving}:
                    faults.append(
                        f"{state}: the linked rules name states the diagram does not"
                    )
            elif drawn.condition is None and labels != {None}:
                faults.append(f"{state}: no one unlabelled edge leaves it")
            elif drawn.condition is not None and labels != {
                drawn.then,
                drawn.otherwise,
            }:
                faults.append(f"{state}: its labels are not the edges leaving it")
    for node, destination in sorted(diagram.clicks.items()):
        if destination != document(node):
            faults.append(f"the click on {node} links {destination}, not its document")
    return faults


def drawn_edges(drawings: list[str]) -> list[re.Match[str]]:
    """Every edge the Mermaid diagrams draw, one match per line drawing one."""
    return [
        edge
        for body in drawings
        for line in body.splitlines()
        if (edge := EDGE.match(line)) is not None
    ]


def entry_faults(workflow: Workflow, form: str) -> list[str]:
    """How one form's entry document carries more than its form allows.

    A prose entry draws no diagram, and a linked entry draws the diagram
    form's edges with no branch label, so the rule a linked decision names
    is the only statement of the edge its branch takes.
    """
    entry = workflow.form(form) / ENTRY
    drawings = [
        body for kind, body in FENCE.findall(entry.read_text()) if kind == "mermaid"
    ]
    if form in UNDRAWN:
        return [f"the {form} entry draws a diagram"] if drawings else []
    if form not in UNLABELLED:
        return []
    faults = []
    edges = drawn_edges(drawings)
    for edge in edges:
        source, label, target = edge.groups()
        if label is not None:
            faults.append(
                f"the {form} entry labels the edge {source} to {target} {label!r}"
            )
    drawn = {(edge.source, edge.target) for edge in workflow.diagram.edges}
    if {(edge.group(1), edge.group(3)) for edge in edges} != drawn:
        faults.append(f"the {form} entry draws edges the diagram does not")
    return faults


def reached(workflow: Workflow, state: str) -> set[str]:
    """Every state one state's edges may enter, through a decision or alone."""
    found: set[str] = set()
    for edge in workflow.diagram.leaving(state):
        if edge.target in workflow.diagram.decisions:
            for escape in workflow.diagram.leaving(edge.target):
                found |= {
                    onward.target for onward in workflow.diagram.leaving(escape.target)
                }
        else:
            found.add(edge.target)
    return found


def scenario_faults(workflow: Workflow, scenario: Scenario) -> list[str]:
    """How a scenario's path, trace or runs fail to be what its sources state."""
    diagram = workflow.diagram
    path = scenario.path
    faults = compile_faults(workflow, scenario)
    if not path or path[0] != diagram.start:
        faults.append(f"{scenario.name}: the path does not open at {diagram.start}")
    # A state reaches the next state through a decision and a condition, so a
    # step is held to the states a path reaches, not to one drawn edge.
    for step in zip(path, path[1:], strict=False):
        if step[1] not in reached(workflow, step[0]):
            faults.append(
                f"{scenario.name}: the diagram reaches no {step[1]} from {step[0]}"
            )
    if path and path[-1] not in diagram.terminals:
        faults.append(f"{scenario.name}: the path ends at {path[-1]}, not terminal")
    read = inputs_read(workflow, workflow.forms[0])
    if set(scenario.inputs) != read:
        faults.append(f"{scenario.name}: its inputs are not the files decisions read")
        return faults
    # A form deferring a transition states its walk only through the runs
    # activating it, which the compiled walk holds the path to.
    for form in workflow.forms:
        if any(section.deferred for section in workflow.sections[form].values()):
            continue
        walked = walk(workflow, form, scenario.inputs)
        if walked != path:
            faults.append(f"{scenario.name}: the {form} sections lead {walked}")
    dispatching = [
        form for form in (*DISPATCH_FORMS, BOOTSTRAP) if form in workflow.forms
    ]
    if not dispatching:
        if scenario.trace:
            faults.append(f"{scenario.name}: a form that dispatches names a trace")
        return faults
    for form in dispatching:
        stated = dispatch_walk(workflow, form, path, scenario.inputs)
        named = tuple((entry.section, entry.together) for entry in scenario.trace)
        if named != stated:
            faults.append(
                f"{scenario.name}: the {form} form dispatches {[s for s, _ in stated]}"
                f", not the [section, set] pairs the trace names: {list(named)}"
            )
    return faults


def compiled_bundle(workflow: Workflow, output: Path) -> str:
    """The entry bundle `pf` compiles from a workflow's diagram form."""
    run = bundle(workflow, DIAGRAM, output)
    assert run.returncode == 0, run.stderr.decode()
    return (output / workflow.entry_bundle).read_text()


def bundle_path_faults(
    workflow: Workflow, scenario: Scenario, output: Path
) -> list[str]:
    """How a scenario's path fails to be the walk the diagram form's bundle states."""
    walked, faults = bundle_walk(
        workflow, compiled_bundle(workflow, output), scenario.inputs
    )
    if not faults and walked != scenario.path:
        faults.append(f"the bundle leads {walked}")
    return [f"{scenario.name}: {fault}" for fault in faults]


def compiled_faults(workflow: Workflow, scenario: Scenario, output: Path) -> list[str]:
    """How a compiled scenario's path or own runs fail to be what its bundles state.

    The walk runs `pf` on each `↳` line a state's steps reach, as a correct
    session does, so the session's stated runs are the walk's, and the path
    is the one the entry's bundle and the bundles those runs write state.
    """
    walked, runs, faults = compiled_walk(workflow, scenario.inputs, output)
    if not faults and walked != scenario.path:
        faults.append(f"the compiled bundles lead {walked}")
    stated = tuple(run for run in scenario.compile if run.by is None)
    root = workflow.form(COMPILED_FORM)
    if [run.selection(root) for run in runs] != [run.selection(root) for run in stated]:
        faults.append(f"the walk runs pf on {[run.args for run in runs]}")
    return [f"{scenario.name}: {fault}" for fault in faults]


def dispatched_bundle(section: str) -> str:
    """The path `pf` gives the bundle it compiles for a dispatched section.

    `pf` writes each target's bundle into a folder named for the document it
    is compiled from, `<document>__<heading>.bundles`, holding
    `<document>__<heading>.bundle.md`. The section may name its document with
    or without the Markdown suffix.
    """
    return entry_bundle(section).as_posix()


def sub_agent_faults(workflow: Workflow, scenario: Scenario, output: Path) -> list[str]:
    """How a compiled scenario's sub-agent runs and actions fail its bundles.

    Each sub-agent follows the bundle `pf` wrote for its section, in the
    entry's set or in the set a run on a `↳` line wrote, and runs `pf` on
    each deferred line its steps reach, as the session does. The runs the
    scenario states `by` a section are those its sub-agents make, in order,
    and the actions a trace entry states are the ones the material those
    runs compile states, none of them stated by the bundle itself. Each
    dispatched bundle opens with the run-pf line, each `⇉` link it carries,
    inline or as an dispatch-set item, names a file its run wrote beside it,
    and each bundle a sub-agent follows is one a `⇉` link names.
    """
    walked, _, faults = compiled_walk(workflow, scenario.inputs, output)
    if faults:
        return [f"{scenario.name}: {fault}" for fault in faults]
    followed: dict[str, Path] = {}
    runs: list[Compile] = []
    made: dict[str, list[Compile]] = {entry.section: [] for entry in scenario.trace}

    def activate(request: Compile) -> str:
        runs.append(request)
        reference = request.entry
        assert reference is not None
        folder = output / f"sub-{len(runs)}"
        root = workflow.form(COMPILED_FORM)
        made = compile_reference(root, reference, folder, request.presets)
        assert made.returncode == 0, made.stderr.decode()
        return (
            folder / entry_bundle(reference, effective_presets(root, request))
        ).read_text()

    for entry in scenario.trace:
        # `pf` writes every target's bundle beside the entry that dispatches
        # it, in that entry's own `.bundles` folder, so a target is found
        # there and in the set of any run a later document makes.
        wanted = entry_bundle(entry.section, entry.presets).name
        written = sorted(output.rglob(wanted))
        if not written:
            faults.append(f"no run writes the bundle {entry.section} follows")
            continue
        text = written[0].read_text()
        followed[wanted] = written[0].resolve()
        if not opens_with_run_pf(text):
            faults.append(f"{entry.section}'s bundle opens with no run-pf line")
        before = len(runs)
        compiled = activated(text, text, scenario.inputs, list(walked), activate)
        made[entry.section] += runs[before:]
        # A section states its sub-agent's action itself, and the material a
        # run on a deferred line compiles states the action where the section
        # carries none, so the action is whichever of the two states it. A
        # scenario stating answers has its sub-agent write the answer it was
        # handed, so that section names the file and states the answer in
        # prose rather than as a value.
        stated = tuple(ACTION.findall(text)) + tuple(ACTION.findall(compiled))
        expected = () if entry.action is None else (entry.action,)
        if scenario.answers and expected:
            name = expected[0][0]
            bodies = text + compiled
            if f"`actions/{name}`" not in bodies:
                faults.append(f"{entry.section}'s runs write no actions/{name}")
        elif stated != expected:
            faults.append(f"{entry.section}'s runs compile the actions {list(stated)}")
    for section, ran in made.items():
        stated_runs = [
            replace(run, by=None) for run in scenario.compile if run.by == section
        ]
        root = workflow.form(COMPILED_FORM)
        if [run.selection(root) for run in ran] != [
            run.selection(root) for run in stated_runs
        ]:
            faults.append(
                f"{section}'s sub-agents run pf on {[run.args for run in ran]}"
            )
    links = [
        (bundle, target)
        for bundle in sorted(output.rglob("*.bundle.md"))
        for link in markdown_links(bundle.read_text())
        if link.label.startswith("⇉ ")
        for target in (link.destination,)
    ]
    faults += [
        f"{bundle.name} links {target}, which no run writes"
        for bundle, target in links
        if not (bundle.parent / target).is_file()
    ]
    linked = {(bundle.parent / target).resolve() for bundle, target in links}
    faults += [
        f"no bundle links the bundle {section} follows"
        for section, bundle in followed.items()
        if bundle not in linked
    ]
    return [f"{scenario.name}: {fault}" for fault in faults]


def bootstrap_faults(workflow: Workflow, scenario: Scenario, output: Path) -> list[str]:
    """How a bootstrap scenario fails to state its skill's runs and their walk.

    The skill's `SKILL.md` holds one `↳` line, titled as the document it
    names is headed, so a correct session runs bare `pf` for the guide, then
    `pf` on that line's reference, and walks the bundle it writes. A drawn
    decision is read from the sources, which the bundle walk does not read,
    so a workflow drawing one is held to its runs and title alone.
    """
    root = workflow.directory / BOOTSTRAP_DIR
    lines = inline_lines(authored(root / SKILL_ENTRY))
    if len(lines) != 1:
        return [f"{scenario.name}: the skill holds {len(lines)} inline lines"]
    [link] = lines
    title, reference = link.label, link.destination
    faults = []
    request = Compile(None, reference, link.tags)
    if [run.selection(root) for run in scenario.compile] != [
        run.selection(root) for run in (Compile(None), request)
    ]:
        faults.append(
            f"it states {scenario.compile}, not pf, then pf --entry {reference}"
        )
    headed = re.search(r"^# (.+)$", authored(root / reference), re.MULTILINE)
    if headed is None or headed.group(1) != title:
        faults.append(f"the line is titled {title!r}, not as {reference} is headed")
    run = compile_reference(root, reference, output, request.presets)
    if run.returncode != 0:
        faults.append(f"pf {reference} exited {run.returncode}")
    elif not workflow.diagram.decisions:
        compiled = (
            output / entry_bundle(reference, effective_presets(root, request))
        ).read_text()
        walked, walk_faults = bundle_walk(workflow, compiled, scenario.inputs)
        faults += walk_faults
        if not walk_faults and walked != scenario.path:
            faults.append(f"the compiled target leads {walked}")
    return [f"{scenario.name}: {fault}" for fault in faults]


def enclosing(bundle_text: str, title: str, occurrence: int = 0) -> list[str]:
    """The headings enclosing one heading of a bundle, outermost first.

    `occurrence` picks among headings carrying the same text, in bundle order.
    """
    stack: list[tuple[int, str]] = []
    seen = 0
    for section in bundled_sections(bundle_text).values():
        while stack and stack[-1][0] >= section.level:
            stack.pop()
        if section.title == title:
            if seen == occurrence:
                return [text for _, text in stack]
            seen += 1
        stack.append((section.level, section.title))
    raise AssertionError(f"the bundle carries no {title} #{occurrence}")


def broken(
    tmp_path: Path, name: str, path: str, old: str, new: str, count: int = 1
) -> Workflow:
    """A copy of one workflow with a string of one file replaced."""
    copy = tmp_path / name
    shutil.copytree(WORKFLOWS / name, copy)
    target = copy / path
    text = target.read_text()
    assert old in text, f"{path} carries no {old!r} to break"
    target.write_text(text.replace(old, new, count))
    return read_workflow(copy)


def test_the_corpus_holds_the_graded_workflows() -> None:
    assert [workflow.name for workflow in CORPUS] == [
        "bootstrap-audit",
        "branching",
        "conditional-composition",
        "declared-inclusion",
        "deferred-composition",
        "deferred-dispatch",
        "directive-labels",
        "dispatch-beside",
        "dispatch-chain",
        "dispatch-depth",
        "dispatch-question",
        "dispatch-set",
        "group-placement",
        "inline-bootstrap",
        "linear",
        "looping",
        "preset-deferral",
        "preset-selection",
        "pricing",
        "rework",
        "section-composition",
        "section-entry",
        "subagent-first-run",
        "subst-redirect",
    ]


def test_every_form_is_written_by_some_workflow() -> None:
    assert {form for workflow in CORPUS for form in workflow.forms} == set(FORMS)


def test_every_workflow_document_declares_presets() -> None:
    assert declaration_faults(WORKFLOWS) == []


@pytest.mark.parametrize(
    ("old", "new", "fault"),
    [
        ("---\nprosiform: {}\n---\n", "", "declares no prosiform"),
        ("prosiform: {}", "prosiform: true", "declares prosiform as True, not presets"),
        (
            "prosiform: {}",
            "prosiform: {group: [modes]}",
            "declares prosiform.group outside a preset",
        ),
    ],
)
def test_a_document_declaring_outside_presets_is_a_fault(
    tmp_path: Path, old: str, new: str, fault: str
) -> None:
    broken(tmp_path, "linear", f"{DIAGRAM}/{document('Plan')}", old, new)
    assert declaration_faults(tmp_path) == [f"linear/{DIAGRAM}/states/plan.md {fault}"]


@pytest.mark.parametrize(
    ("workflow", "form"),
    [(workflow, form) for workflow in CORPUS for form in workflow.forms],
    ids=lambda item: getattr(item, "name", item),
)
def test_each_form_bundles_cleanly_carrying_every_state(
    workflow: Workflow, form: str, tmp_path: Path
) -> None:
    assert bundle_faults(workflow, form, tmp_path) == []


@pytest.mark.parametrize(
    ("workflow", "form"),
    [(workflow, form) for workflow in DISPATCHING for form in DISPATCH_FORMS],
    ids=lambda item: getattr(item, "name", item),
)
def test_each_dispatch_form_states_steps_naming_their_targets(
    workflow: Workflow, form: str
) -> None:
    """AC1: each dispatch scenario's compiled and authored forms are whole."""
    assert step_faults(workflow, form) == []


@pytest.mark.parametrize("workflow", DISPATCHING, ids=lambda item: item.name)
def test_each_dispatch_scenario_bundles_clean_in_both_its_forms(
    workflow: Workflow, tmp_path: Path
) -> None:
    """AC1: both forms bundle with `pf` at exit 0 and report no diagnostic."""
    for form in DISPATCH_FORMS:
        output = tmp_path / form
        output.mkdir()
        run = bundle(workflow, form, output)
        assert run.returncode == 0, (workflow.name, form, run.stderr.decode())
        assert run.stderr == b"", (workflow.name, form, run.stderr.decode())
        assert (output / workflow.entry_bundle).is_file(), (workflow.name, form)


@pytest.mark.parametrize("workflow", CORPUS, ids=lambda workflow: workflow.name)
def test_the_forms_differ_only_in_their_transitions(workflow: Workflow) -> None:
    assert section_faults(workflow) == []


@pytest.mark.parametrize("workflow", CORPUS, ids=lambda workflow: workflow.name)
def test_each_section_states_the_transition_the_diagram_draws(
    workflow: Workflow,
) -> None:
    assert transition_faults(workflow) == []


@pytest.mark.parametrize(
    ("workflow", "form"),
    [(workflow, form) for workflow in CORPUS for form in workflow.forms],
    ids=lambda item: getattr(item, "name", item),
)
def test_each_entry_carries_only_what_its_form_allows(
    workflow: Workflow, form: str
) -> None:
    assert entry_faults(workflow, form) == []


@pytest.mark.parametrize(
    ("workflow", "scenario"),
    [(workflow, scenario) for workflow in CORPUS for scenario in workflow.scenarios],
    ids=lambda item: item.name,
)
def test_each_scenario_path_is_the_walk_its_inputs_determine(
    workflow: Workflow, scenario: Scenario
) -> None:
    assert scenario_faults(workflow, scenario) == []


@pytest.mark.parametrize(
    ("workflow", "scenario"),
    [(workflow, scenario) for workflow in DRAWING for scenario in workflow.scenarios],
    ids=lambda item: item.name,
)
def test_each_scenario_path_is_the_walk_its_bundle_states(
    workflow: Workflow, scenario: Scenario, tmp_path: Path
) -> None:
    """AC23, AC24, AC25: the path is the one the bundle `pf` compiles states."""
    assert bundle_path_faults(workflow, scenario, tmp_path) == []


@pytest.mark.parametrize(
    ("workflow", "scenario"),
    [(workflow, scenario) for workflow in COMPILING for scenario in workflow.scenarios],
    ids=lambda item: item.name,
)
def test_each_compiled_scenario_states_the_runs_and_path_its_bundles_state(
    workflow: Workflow, scenario: Scenario, tmp_path: Path
) -> None:
    """AC7, AC8, AC9: each run is on a line the path reaches, and the path theirs."""
    assert compiled_faults(workflow, scenario, tmp_path) == []


@pytest.mark.parametrize(
    ("workflow", "scenario"),
    [(workflow, scenario) for workflow in COMPILING for scenario in workflow.scenarios],
    ids=lambda item: item.name,
)
def test_each_compiled_sub_agent_states_the_actions_its_runs_compile(
    workflow: Workflow, scenario: Scenario, tmp_path: Path
) -> None:
    """AC17, AC18, AC27: a sub-agent's actions are what its own `pf` runs compile.

    Each bundle a sub-agent follows opens with the run-pf line and is one a
    `⇉` link names, and each `⇉` link names a file its run wrote.
    """
    assert sub_agent_faults(workflow, scenario, tmp_path) == []


RETIRED = re.compile(r"\[¬[⇉⫽]|\[¬?→\]\(")
"""A deferred dispatch, a deferred set member, or an arrow-labelled link."""


def test_no_edge_workflow_source_writes_a_retired_mark() -> None:
    """AC27: every composition is `↳` or `¬↳`, and no source defers a dispatch."""
    written = [
        f"{source.relative_to(WORKFLOWS)}: {line}"
        for workflow in CORPUS
        for source in sorted(workflow.directory.rglob("*.md"))
        for line in source.read_text().splitlines()
        if RETIRED.search(line)
    ]
    assert written == []
    composing = {
        workflow.name
        for workflow in COMPILING
        if any(
            "↳ " in path.read_text()
            for path in workflow.form(COMPILED_FORM).rglob("*.md")
        )
    }
    assert composing == {
        "conditional-composition",
        "deferred-composition",
        "deferred-dispatch",
        "directive-labels",
        "preset-deferral",
        "subagent-first-run",
    }


def test_a_set_publishes_parallel_items_linking_bundles_opening_with_the_run_pf_line(
    tmp_path: Path,
) -> None:
    """AC27: `dispatch-set`'s set is an dispatch-set section of `⇉` items.

    Each item names the file `pf` wrote for its target beside the entry, and
    that file opens with the run-pf line, as the chain's inline `⇉` link
    names the bundle it hands on.
    """
    workflow = CORPUS_BY_NAME["dispatch-set"]
    text, _ = compiled_entry(workflow, tmp_path / "set")
    folder = tmp_path / "set" / workflow.entry_bundle.parent
    assert opens_with_run_pf(text)
    parallel = next(
        section.text
        for name, section in bundled_sections(text).items()
        if DISPATCH_LINK.search(section.text) and section.title.startswith("⫽")
    )
    assert DISPATCH_LINK.findall(parallel) == [
        "review__source.bundle.md",
        "review__tests.bundle.md",
    ]
    for name in DISPATCH_LINK.findall(parallel):
        assert opens_with_run_pf((folder / name).read_text())
    chain = CORPUS_BY_NAME["dispatch-chain"]
    text, _ = compiled_entry(chain, tmp_path / "chain")
    assert DISPATCH_LINK.findall(text) == ["plan__work.bundle.md"]


def test_a_dispatched_bundle_opening_without_the_run_pf_line_is_a_fault(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC27: the corpus test reads the line each dispatched bundle opens with."""
    monkeypatch.setattr(sys.modules[__name__], "RUN_PF", "Run nothing.")
    workflow = CORPUS_BY_NAME["dispatch-set"]
    [scenario] = workflow.scenarios
    assert sub_agent_faults(workflow, scenario, tmp_path) == [
        "parallel-set: review#source's bundle opens with no run-pf line",
        "parallel-set: review#tests's bundle opens with no run-pf line",
    ]


@pytest.mark.parametrize(
    ("workflow", "scenario"),
    [
        (workflow, scenario)
        for workflow in BOOTSTRAPPING
        for scenario in workflow.scenarios
    ],
    ids=lambda item: item.name,
)
def test_each_bootstrap_scenario_states_the_guide_its_line_and_the_walk(
    workflow: Workflow, scenario: Scenario, tmp_path: Path
) -> None:
    """AC6: bare `pf`, `pf` on the skill's line, then the compiled target's walk."""
    assert bootstrap_faults(workflow, scenario, tmp_path) == []


def test_a_skill_entry_declaring_nothing_holds_its_line_as_written() -> None:
    """AC6: the inline skill's entry declares no `prosiform`, and holds one line."""
    entry = WORKFLOWS / "inline-bootstrap" / BOOTSTRAP_DIR / SKILL_ENTRY
    block = FRONTMATTER.match(entry.read_text())
    assert block is not None
    assert "prosiform" not in YAML(typ="safe", pure=True).load(block.group()[4:-4])
    assert [
        (link.label, link.destination) for link in inline_lines(entry.read_text())
    ] == [("Release", "sources/workflow.md")]


@pytest.mark.parametrize(
    ("old", "new", "fault"),
    [
        (
            "[↳ Release]",
            "[↳ Cut]",
            "feature-tagged: the line is titled 'Cut', not as"
            " sources/workflow.md is headed",
        ),
    ],
    ids=["title"],
)
def test_a_skill_line_its_scenario_does_not_compile_is_a_fault(
    tmp_path: Path, old: str, new: str, fault: str
) -> None:
    """AC6: the line's title is held to the document it names."""
    workflow = broken(
        tmp_path, "inline-bootstrap", f"{BOOTSTRAP_DIR}/{SKILL_ENTRY}", old, new
    )
    output = tmp_path / "output"
    output.mkdir()
    assert fault in bootstrap_faults(workflow, workflow.scenarios[0], output)


def test_a_bootstrap_scenario_omitting_the_guide_is_a_fault(tmp_path: Path) -> None:
    """AC6: the scenario states bare `pf` before `pf` on the skill's line."""
    workflow = broken(
        tmp_path,
        "inline-bootstrap",
        "scenarios.toml",
        "[[scenario.compile]]\n\n",
        "",
    )
    output = tmp_path / "output"
    output.mkdir()
    assert bootstrap_faults(workflow, workflow.scenarios[0], output) == [
        "feature-tagged: it states (Compile(by=None, entry='sources/workflow.md', "
        "presets=frozenset()),),"
        " not pf, then pf --entry sources/workflow.md"
    ]


def test_a_conditional_deferral_is_run_where_its_step_holds_and_nowhere_else() -> None:
    """AC7, AC8: the outer line reached and passed, the nested needed and not."""
    named = {workflow.name: workflow for workflow in CORPUS}
    migration = Compile(None, "reference/migration.md#steps")
    archive = Compile(None, "reference/archive.md#steps")
    assert {
        scenario.name: scenario.compile
        for scenario in named["deferred-composition"].scenarios
    } == {
        "deferral-reached": (migration,),
        "deferral-passed": (),
        "nested-needed": (migration, archive),
        "nested-unreached": (),
    }


@pytest.mark.parametrize(
    ("old", "new", "fault"),
    [
        (
            '"scope.txt" = "large", "history.txt" = "dropped"',
            '"scope.txt" = "small", "history.txt" = "dropped"',
            "deferral-reached: the walk runs pf on []",
        ),
        (
            '"scope.txt" = "large", "history.txt" = "kept"',
            '"scope.txt" = "large", "history.txt" = "dropped"',
            "nested-needed: the walk runs pf on "
            "[('--entry=reference/migration.md#steps',)]",
        ),
    ],
    ids=["outer-passed", "nested-unneeded"],
)
def test_a_run_on_a_line_the_path_does_not_reach_is_a_fault(
    tmp_path: Path, old: str, new: str, fault: str
) -> None:
    """AC7, AC8: a stated run whose step does not hold is no run of the walk."""
    workflow = broken(tmp_path, "deferred-composition", "scenarios.toml", old, new)
    faults = [
        found
        for index, scenario in enumerate(workflow.scenarios)
        for found in compiled_faults(workflow, scenario, tmp_path / str(index))
    ]
    assert faults == [fault]


def test_the_real_target_of_a_preset_deferral_leads_elsewhere(tmp_path: Path) -> None:
    """AC9: without the preset's stand-in, the path leaves Mirror by `live`."""
    workflow = broken(
        tmp_path,
        "preset-deferral",
        f"{COMPILED_FORM}/reference/fetch.md",
        "prosiform:\n  mirror:\n    subst: [{net.md: cache.md}]\n",
        "prosiform:\n  mirror: {}\n",
    )
    [scenario] = workflow.scenarios
    assert compiled_faults(workflow, scenario, tmp_path / "output") == [
        "stand-in-followed: the compiled bundles lead "
        "('Entry', 'Solicit', 'Mirror', 'Serve', 'Exit')"
    ]


def test_a_preset_deferral_states_the_stand_ins_path() -> None:
    """AC9: the deferral title selects a stand-in and the path it states."""
    workflow = next(item for item in CORPUS if item.name == "preset-deferral")
    [scenario] = workflow.scenarios
    assert scenario.path == ("Entry", "Solicit", "Mirror", "Restore", "Exit")
    assert scenario.compile == (
        Compile(None, "reference/fetch.md#read-mirror", frozenset({"mirror"})),
    )
    assert workflow.sections[COMPILED_FORM]["Mirror"].deferred


def test_dispatch_trace_presets_require_a_string_list() -> None:
    with pytest.raises(CorpusError, match="presets need a string list"):
        read_dispatch({"dispatch": "crew#work", "presets": ["lift"]}, "bad")


@pytest.mark.parametrize("tags", ["", ' "strap"'])
def test_deferred_composition_without_its_required_tags_leads_elsewhere(
    tmp_path: Path, tags: str
) -> None:
    workflow = broken(
        tmp_path,
        "preset-deferral",
        "compiled/states/mirror.md",
        ' "mirror"',
        tags,
    )
    assert any(
        "compiled bundles lead" in fault
        for fault in compiled_faults(workflow, workflow.scenarios[0], tmp_path / "out")
    )


@pytest.mark.parametrize("tags", ["", ' "lift"', ' "wrong"'])
def test_dispatched_selection_without_required_tags_has_no_matching_bundle(
    tmp_path: Path, tags: str
) -> None:
    workflow = broken(
        tmp_path,
        "deferred-dispatch",
        "compiled/reference/loading.md",
        ' "strap"',
        tags,
    )
    faults = sub_agent_faults(workflow, workflow.scenarios[0], tmp_path / "out")
    assert any(
        "no run writes the bundle reference/crew#work follows" in fault
        for fault in faults
    )


def test_equivalent_scenario_preset_requests_name_the_same_compiled_run(
    tmp_path: Path,
) -> None:
    """Expected runs compare matching names, including default and unknown tokens."""
    workflow = broken(
        tmp_path,
        "preset-deferral",
        "scenarios.toml",
        'presets = "mirror"',
        'presets = " UNKNOWN, MIRROR,mirror,default "',
    )
    assert compiled_faults(workflow, workflow.scenarios[0], tmp_path / "out") == []


def test_compile_reference_selects_declared_presets_and_reads_qualified_output(
    tmp_path: Path,
) -> None:
    """The eval's real compiler call preserves title tags and effective naming."""
    (tmp_path / "entry.md").write_text(
        "---\nprosiform:\n  Checks:\n    subst: [{old.md: new.md}]\n---\n"
        "# Entry\n\n[Read](old.md)\n"
    )
    for name in ("old", "new"):
        (tmp_path / f"{name}.md").write_text(
            f"---\nprosiform: {{}}\n---\n# {name.title()}\n{name.title()} body.\n"
        )
    request = Compile(None, "entry.md", frozenset({"checks", "unknown"}))
    output = tmp_path / "out"
    made = compile_reference(tmp_path, "entry.md", output, request.presets)
    assert made.returncode == 0, made.stderr.decode()
    assert effective_presets(tmp_path, request) == frozenset({"Checks"})
    path = output / entry_bundle("entry.md", frozenset({"Checks"}))
    assert bundled(output) == [path]
    assert "New body." in path.read_text()
    assert "Old body." not in path.read_text()


def test_composition_readers_retain_decoded_titles_outside_destinations() -> None:
    """Tags survive source and published-line reads without joining the href."""
    [deferred] = deferred_links(
        '[¬↳ Read](fetch.md#read " Checks, Release Candidate ")'
    )
    [inline] = inline_lines('[↳ Read](fetch.md#read "checks,Release Candidate")')
    assert deferred.destination == inline.destination == "fetch.md#read"
    assert deferred.tags == inline.tags == frozenset({"checks", "release candidate"})
    assert fragment_links('[Read](#read "checks,draft")') == [("Read", "read")]
    assert read_compile(
        {"entry": "fetch.md#read", "presets": " Checks,CHECKS, Release Candidate "},
        "one",
    ) == Compile(None, "fetch.md#read", inline.tags)


def test_a_deferred_dispatch_is_compiled_where_reached_and_its_bundle_dispatches(
    tmp_path: Path,
) -> None:
    """AC13: the `↳` line compiled where Pack's step holds, then its dispatches."""
    workflow = next(item for item in CORPUS if item.name == "deferred-dispatch")
    text, _ = compiled_entry(workflow, tmp_path / "entry")
    assert [(link.label, link.destination) for link in inline_lines(text)] == [
        ("Crew", "reference/loading.md#crew")
    ]
    assert "¬" not in text and "⇉" not in text
    compiled, passed = workflow.scenarios
    assert compiled.compile == (Compile(None, "reference/loading.md#crew"),)
    assert dispatch_starts(workflow, COMPILED_FORM, compiled.path, compiled.inputs) == (
        ("reference/crew#work", False, 0),
        ("reference/crew#work", False, 0),
    )
    assert [entry.section for entry in compiled.trace] == [
        "reference/crew#work",
        "reference/crew#work",
    ]
    assert [entry.presets for entry in compiled.trace] == [
        frozenset({"lift"}),
        frozenset({"strap"}),
    ]
    assert [entry.action for entry in compiled.trace] == [
        ("lift.txt", "lifted"),
        ("strap.txt", "strapped"),
    ]
    assert (passed.compile, passed.trace) == ((), ())
    assert dispatch_walk(workflow, COMPILED_FORM, passed.path, passed.inputs) == ()


@pytest.mark.parametrize(
    ("old", "new", "faults"),
    [
        (
            '"order.txt" = "single"',
            '"order.txt" = "bulk"',
            [
                "deferred-dispatch-passed: the walk runs pf on"
                " [('--entry=reference/loading.md#crew',)]",
                "deferred-dispatch-passed: the compiled form dispatches"
                " ['reference/crew#work', 'reference/crew#work'], not the"
                " [section, set] pairs the trace names: []",
            ],
        ),
        (
            '[[scenario.compile]]\nentry = "reference/loading.md#crew"\n',
            "",
            [
                "deferred-dispatch-compiled: the walk runs pf on"
                " [('--entry=reference/loading.md#crew',)]"
            ],
        ),
    ],
    ids=["passed-reaches", "run-unstated"],
)
def test_a_deferred_dispatch_stated_off_its_walk_is_a_fault(
    tmp_path: Path, old: str, new: str, faults: list[str]
) -> None:
    """AC13: the run and its dispatches are stated where the step holds alone."""
    workflow = broken(tmp_path, "deferred-dispatch", "scenarios.toml", old, new)
    found = [
        fault
        for index, scenario in enumerate(workflow.scenarios)
        for fault in [
            *compiled_faults(workflow, scenario, tmp_path / str(index)),
            *scenario_faults(workflow, scenario),
        ]
    ]
    assert found == faults


def test_a_three_hop_chain_starts_each_hop_in_order_with_no_depth_warning(
    tmp_path: Path,
) -> None:
    """AC14: three hops below the session, each done before its caller goes on."""
    workflow = next(item for item in CORPUS if item.name == "dispatch-depth")
    _, stderr = compiled_entry(workflow, tmp_path)
    assert b"W_DISPATCH_DEPTH" not in stderr and stderr == b""
    chain = next(item for item in workflow.scenarios if item.name == "three-hop-chain")
    assert dispatch_starts(workflow, COMPILED_FORM, chain.path, chain.inputs) == (
        ("line/scope#frame", False, 0),
        ("line/detail#expand", False, 1),
        ("line/tally#count", False, 2),
    )


def test_a_set_three_hops_deep_starts_together_before_the_chain_goes_on() -> None:
    """AC15: the second hop's set starts at once, ahead of the join and the seal."""
    workflow = next(item for item in CORPUS if item.name == "dispatch-depth")
    fan = next(item for item in workflow.scenarios if item.name == "three-hop-set")
    assert dispatch_starts(workflow, COMPILED_FORM, fan.path, fan.inputs) == (
        ("fan/divide#portion", False, 0),
        ("fan/east#east", False, 1),
        ("fan/west#west", True, 1),
        ("fan/join#join", False, 1),
        ("fan/seal#seal", False, 2),
    )
    assert [(entry.section, entry.together) for entry in fan.trace] == [
        (section, together)
        for section, together, _ in dispatch_starts(
            workflow, COMPILED_FORM, fan.path, fan.inputs
        )
    ]


def test_a_question_three_hops_deep_is_relayed_and_the_chain_dispatched_again() -> None:
    """AC16: the question returned up every hop, then the chain run with answers."""
    workflow = next(item for item in CORPUS if item.name == "dispatch-depth")
    asked = next(
        item for item in workflow.scenarios if item.name == "three-hop-question"
    )
    chain = ["ask/enquiry#pose", "ask/probe#probe", "ask/choice#elect"]
    assert [entry.section for entry in asked.trace] == [*chain, *chain]
    assert asked.answers, "a scenario whose sub-agent asks states the answers"
    assert [
        depth
        for _, _, depth in dispatch_starts(
            workflow, COMPILED_FORM, asked.path, asked.inputs
        )
    ] == [0, 1, 2, 0, 1, 2]


def test_a_hop_missing_from_a_deep_trace_is_a_fault(tmp_path: Path) -> None:
    """AC14: a trace stopping a hop short is not the walk its sources state."""
    workflow = broken(
        tmp_path,
        "dispatch-depth",
        "scenarios.toml",
        '[[scenario.trace]]\ndispatch = "line/tally#count"\n',
        "",
    )
    [fault] = [
        fault
        for scenario in workflow.scenarios
        for fault in scenario_faults(workflow, scenario)
    ]
    assert fault.startswith(
        "three-hop-chain: the compiled form dispatches"
        " ['line/scope#frame', 'line/detail#expand', 'line/tally#count']"
    )


def test_a_first_hop_bundle_runs_pf_first_and_its_line_states_its_action(
    tmp_path: Path,
) -> None:
    """AC17: the ledger's bundle opens with the run-pf line; its line, the action."""
    workflow = next(item for item in CORPUS if item.name == "subagent-first-run")
    first = next(item for item in workflow.scenarios if item.name == "first-hop-run")
    compiled_entry(workflow, tmp_path)
    ledger = (
        tmp_path / "workflow.bundles" / "hop_ledger__balance.bundle.md"
    ).read_text()
    assert opens_with_run_pf(ledger)
    assert [(link.label, link.destination) for link in inline_lines(ledger)] == [
        ("Close", "steps/closing.md#close")
    ]
    [entry] = first.trace
    assert (entry.section, entry.action) == (
        "hop/ledger#balance",
        ("closing.txt", "closed"),
    )


def test_each_deep_hop_carrying_a_line_states_the_action_its_run_compiles() -> None:
    """AC18: the review's line and the ruling's line each state one."""
    workflow = next(item for item in CORPUS if item.name == "subagent-first-run")
    deep = next(item for item in workflow.scenarios if item.name == "deep-hop-runs")
    assert [
        (section, depth)
        for section, _, depth in dispatch_starts(
            workflow, COMPILED_FORM, deep.path, deep.inputs
        )
    ] == [("hop/audit#sweep", 0), ("hop/review#scan", 1), ("steps/ruling#rule", 2)]
    assert [(entry.section, entry.action) for entry in deep.trace] == [
        ("hop/audit#sweep", None),
        ("hop/review#scan", ("weighing.txt", "weighed")),
        ("steps/ruling#rule", ("ruling.txt", "ruled")),
    ]


@pytest.mark.parametrize(
    ("path", "old", "new", "fault"),
    [
        (
            "scenarios.toml",
            'file = "closing.txt", value = "closed"',
            'file = "closing.txt", value = "shut"',
            "first-hop-run: hop/ledger#balance's runs compile the actions"
            " [('closing.txt', 'closed')]",
        ),
    ],
    ids=["action-uncompiled"],
)
def test_a_sub_agent_action_its_runs_do_not_alone_state_is_a_fault(
    tmp_path: Path, path: str, old: str, new: str, fault: str
) -> None:
    """AC17: the action a trace entry states is the one its material writes.

    A dispatched section may state its action directly or in material its
    deferred line compiles. The scenario's action must match that material.
    """
    workflow = broken(tmp_path, "subagent-first-run", path, old, new)
    first = next(item for item in workflow.scenarios if item.name == "first-hop-run")
    assert sub_agent_faults(workflow, first, tmp_path / "output") == [fault]


def compiled_entry(workflow: Workflow, output: Path) -> tuple[str, bytes]:
    """The entry bundle `pf` compiles from the compiled form, and its stderr."""
    run = bundle(workflow, COMPILED_FORM, output)
    assert run.returncode == 0, run.stderr.decode()
    return (output / workflow.entry_bundle).read_text(), run.stderr


def test_a_state_composed_under_a_conditional_step_is_entered_where_it_holds(
    tmp_path: Path,
) -> None:
    """AC10: the bundle always carries Convert, and the path enters it on `large`.

    Gauge composes Convert's section with `[↳ Rows]` beneath a step reading
    `scope.txt`, so the bundle holds Convert's action and transition for
    either input, and the diagram clicks no Convert: the directive is the
    only way into it.
    """
    workflow = CORPUS_BY_NAME["conditional-composition"]
    assert "Convert" not in workflow.diagram.clicks
    paths = {
        scenario.name: (scenario.inputs, scenario.path)
        for scenario in workflow.scenarios
    }
    assert paths == {
        "composed-entered": (
            {"scope.txt": "large"},
            ("Entry", "Sample", "Gauge", "Convert", "Finish", "Exit"),
        ),
        "composed-omitted": (
            {"scope.txt": "small"},
            ("Entry", "Sample", "Gauge", "Finish", "Exit"),
        ),
    }
    text, _ = compiled_entry(workflow, tmp_path / "entry")
    assert enclosing(text, "Convert") == ["Gauge", "Rows"]
    for index, scenario in enumerate(workflow.scenarios):
        assert compiled_faults(workflow, scenario, tmp_path / str(index)) == []


@pytest.mark.parametrize(
    ("path", "old", "new", "fault"),
    [
        (
            "scenarios.toml",
            'path = ["Entry", "Sample", "Gauge", "Finish", "Exit"]',
            'path = ["Entry", "Sample", "Gauge", "Convert", "Finish", "Exit"]',
            "composed-omitted: the compiled bundles lead "
            "('Entry', 'Sample', 'Gauge', 'Finish', 'Exit')",
        ),
        (
            f"{COMPILED_FORM}/{document('Gauge')}",
            "[↳ Rows](convert.md#rows)",
            "[the rows](convert.md#rows)",
            "composed-entered: the bundle heads no Convert section at #",
        ),
    ],
    ids=["entered-where-it-fails", "linked-not-composed"],
)
def test_a_composed_state_entered_off_its_condition_is_a_fault(
    tmp_path: Path, path: str, old: str, new: str, fault: str
) -> None:
    """AC10: the path omits Convert where the step fails, and enters it by `↳`."""
    workflow = broken(tmp_path, "conditional-composition", path, old, new)
    faults = [
        found
        for index, scenario in enumerate(workflow.scenarios)
        for found in compiled_faults(workflow, scenario, tmp_path / str(index))
    ]
    assert faults == [fault]


def test_a_footnote_opens_its_target_and_a_composition_composes_in_place(
    tmp_path: Path,
) -> None:
    """AC11: Vet is a document the footnote opens, the style a section in place.

    Compose writes `[↳ Rules]` to the house style's rules and `[†]` to Vet, which
    the diagram clicks nowhere, so the bundle places the rules beneath
    Compose's step and publishes Vet as a document of its own, and the
    `footnote-opened` path enters Vet where the footnote leads.
    """
    workflow = CORPUS_BY_NAME["directive-labels"]
    compose = workflow.sections[COMPILED_FORM]["Compose"].body
    assert "[↳ Rules](../reference/style.md#rules)" in compose
    assert "[†](vet.md#vet)" in compose
    assert "Vet" not in workflow.diagram.clicks
    text, _ = compiled_entry(workflow, tmp_path / "entry")
    assert enclosing(text, "Style") == ["Compose", "Rules"]
    assert enclosing(text, "Vet") == []
    assert "[†](#vet)" in bundled_state(text, "Compose")
    scenario = next(
        item for item in workflow.scenarios if item.name == "footnote-opened"
    )
    assert scenario.path == ("Entry", "Compose", "Vet", "Issue", "Exit")
    assert compiled_faults(workflow, scenario, tmp_path / "walk") == []


def test_a_path_the_footnote_does_not_open_is_a_fault(tmp_path: Path) -> None:
    """AC11: without the footnote, no link in Compose leads to Vet."""
    workflow = broken(
        tmp_path,
        "directive-labels",
        f"{COMPILED_FORM}/{document('Compose')}",
        " [†](vet.md#vet)",
        "",
    )
    scenario = next(
        item for item in workflow.scenarios if item.name == "footnote-opened"
    )
    assert compiled_faults(workflow, scenario, tmp_path / "walk") == [
        "footnote-opened: the bundle heads no Vet section at #"
    ]


def test_a_self_composed_section_warns_and_states_its_bundles_path(
    tmp_path: Path,
) -> None:
    """AC12: Issue composes its own Summary, and the bundle states the path.

    The run publishes with `W_COMPOSE_SELF`, which the workflow declares,
    and the composed copy of the summary stands beneath Issue's Release
    step beside the section it copies.
    """
    workflow = CORPUS_BY_NAME["directive-labels"]
    assert "W_COMPOSE_SELF" in workflow.warnings
    assert "[↳ Summary](#summary)" in workflow.sections[COMPILED_FORM]["Issue"].body
    text, stderr = compiled_entry(workflow, tmp_path / "entry")
    assert reported(stderr) == {"W_COMPOSE_SELF"}
    assert enclosing(text, "Summary") == ["Issue"]
    assert enclosing(text, "Summary", 1) == ["Issue", "Release"]
    scenario = next(item for item in workflow.scenarios if item.name == "self-composed")
    assert scenario.path == ("Entry", "Compose", "Issue", "Exit")
    assert compiled_faults(workflow, scenario, tmp_path / "walk") == []


def test_a_self_composed_scenario_stating_another_path_is_a_fault(
    tmp_path: Path,
) -> None:
    """AC12: the self-composed scenario is held to the walk its bundle states."""
    workflow = broken(
        tmp_path,
        "directive-labels",
        "scenarios.toml",
        'path = ["Entry", "Compose", "Issue", "Exit"]',
        'path = ["Entry", "Compose", "Vet", "Issue", "Exit"]',
    )
    scenario = next(item for item in workflow.scenarios if item.name == "self-composed")
    assert compiled_faults(workflow, scenario, tmp_path / "walk") == [
        "self-composed: the compiled bundles lead ('Entry', 'Compose', 'Issue', 'Exit')"
    ]


def test_the_feature_workflows_are_preset_selection_group_placement_and_subst() -> None:
    """Each holds a scenario per permutation of its feature."""
    named = {workflow.name: workflow for workflow in CORPUS}
    assert [scenario.name for scenario in named["preset-selection"].scenarios] == [
        "default-alone",
        "title-selected",
        "two-presets-one-title",
    ]
    assert [scenario.name for scenario in named["group-placement"].scenarios] == [
        "leaf-group",
        "nested-intermediate",
        "two-presets-one-document",
    ]
    assert [scenario.name for scenario in named["subst-redirect"].scenarios] == [
        "document-redirect",
        "section-redirect",
        "preset-over-default",
    ]
    assert all(named[name].forms == (DIAGRAM,) for name in FEATURES)


def test_the_link_title_tags_select_the_presets_placing_its_document(
    tmp_path: Path,
) -> None:
    """AC23: default alone, one preset selected by a tag, and two selected together.

    Proof's default places it, Patch selects Verify's `patch` preset, and
    `Security Review` selects both Audit's `security` group and its `review`
    pair, which redirects the policy note Audit links.
    """
    workflow = read_workflow(WORKFLOWS / "preset-selection")
    text = compiled_bundle(workflow, tmp_path)
    assert enclosing(text, "Proof") == ["Edit", "Proofs"]
    assert enclosing(text, "Verify") == ["Patch", "Checks"]
    assert enclosing(text, "Audit") == ["Harden", "Audits"]
    assert "[policy](#strict-policy)" in bundled_sections(text)["audit"].text
    assert "# Policy\n" not in text


def test_group_pairs_place_each_file_from_the_leaves_up(tmp_path: Path) -> None:
    """AC24: a leaf group, an intermediate file nested in its parent, two presets.

    Lint and Unit share the leaf group `Checks`. Package stands in a group
    inside Compile's division, and Sign in a group inside Package's, so the
    intermediate file arrives in its parent with its own group composed. Notify
    is reached from the diagram under its default and from Announce under
    `announce`, so it stands in both groups, its section emitted once in each:
    Messages inside the entry's division and Announcements inside Announce's.
    """
    workflow = read_workflow(WORKFLOWS / "group-placement")
    text = compiled_bundle(workflow, tmp_path)
    assert enclosing(text, "Lint") == enclosing(text, "Unit") == ["Delivery", "Checks"]
    assert enclosing(text, "Package") == ["Compile", "Packaging"]
    assert enclosing(text, "Sign") == ["Compile", "Packaging", "Signing"]
    assert enclosing(text, "Notify", 0) == ["Delivery", "Messages"]
    assert enclosing(text, "Notify", 1) == ["Announce", "Announcements"]


def test_subst_pairs_redirect_the_links_a_document_writes(tmp_path: Path) -> None:
    """AC25: a document redirect, a section redirect, a preset holding over default.

    The entry's default sends the diagram's Approve to another document,
    Amend's default sends its Inspect link to one section of the handbook, and
    the link title selects Stage's `release` preset, whose Gate pair holds
    over the default's.
    """
    workflow = read_workflow(WORKFLOWS / "subst-redirect")
    text = compiled_bundle(workflow, tmp_path)
    sections = bundled_sections(text)
    assert "against the release checklist" in sections["approve"].text
    assert enclosing(text, "Inspect") == ["Handbook"]
    assert "against the handbook" in sections["inspect"].text
    assert "Archive" not in text
    assert "against the release checklist" in sections["gate"].text
    assert "as drafted" not in text


def test_a_substitute_stating_another_branch_is_a_fault(tmp_path: Path) -> None:
    """The bundle, not the source, states the path, so a substitute changes it."""
    workflow = broken(
        tmp_path,
        "subst-redirect",
        "diagram/alternates/handbook.md",
        "take the transition labelled `ship`. Otherwise, take the transition"
        " labelled `hold`",
        "take the transition labelled `hold`. Otherwise, take the transition"
        " labelled `ship`",
    )
    output = tmp_path / "output"
    output.mkdir()
    shipped = workflow.scenarios[2]
    assert scenario_faults(workflow, shipped) == []
    assert bundle_path_faults(workflow, shipped, output) == [
        "preset-over-default: the bundle leads ('Entry', 'Outline', 'Amend',"
        " 'Inspect', 'Approve', 'Exit')"
    ]


def test_a_substitute_stating_another_action_is_a_fault(tmp_path: Path) -> None:
    """The scorer reads the source's actions, so the bundle must state the same."""
    workflow = broken(
        tmp_path,
        "subst-redirect",
        "diagram/alternates/release-gate.md",
        "containing `gated`",
        "containing `held`",
    )
    output = tmp_path / "output"
    output.mkdir()
    assert bundle_path_faults(workflow, workflow.scenarios[2], output) == [
        "preset-over-default: the bundle's Gate writes ('gate.txt', 'held'), not"
        " ('gate.txt', 'gated')"
    ]


def test_a_warning_the_workflow_does_not_declare_is_a_fault(tmp_path: Path) -> None:
    workflow = broken(
        tmp_path, "subst-redirect", "scenarios.toml", 'warnings = ["W_SUBST_USED"]', ""
    )
    output = tmp_path / "output"
    output.mkdir()
    [fault] = bundle_faults(workflow, DIAGRAM, output)
    assert fault.startswith('pf reported "W_SUBST_USED: the reference')


def test_a_declared_warning_the_bundle_does_not_raise_is_a_fault(
    tmp_path: Path,
) -> None:
    workflow = broken(
        tmp_path,
        "linear",
        "scenarios.toml",
        "[[scenario]]",
        'warnings = ["W_SUBST_USED"]\n\n[[scenario]]',
    )
    output = tmp_path / "output"
    output.mkdir()
    assert bundle_faults(workflow, DIAGRAM, output) == ["pf reported no W_SUBST_USED"]


def test_the_dispatch_scenarios_are_the_chain_the_set_the_pair_and_the_question() -> (
    None
):
    """The four the epic names, each stating the trace its sources produce."""
    assert [workflow.name for workflow in DISPATCHING] == [
        "dispatch-beside",
        "dispatch-chain",
        "dispatch-question",
        "dispatch-set",
    ]
    for workflow in DISPATCHING:
        [scenario] = workflow.scenarios
        assert scenario.trace, f"{workflow.name}: it names no trace"


def test_a_chain_dispatches_one_target_from_each_of_two_sections() -> None:
    chain = next(item for item in DISPATCHING if item.name == "dispatch-chain")
    [scenario] = chain.scenarios
    assert [entry.section for entry in scenario.trace] == ["plan#work", "review#check"]


def test_a_parallel_set_starts_its_second_target_beside_its_first() -> None:
    set_workflow = next(item for item in DISPATCHING if item.name == "dispatch-set")
    [scenario] = set_workflow.scenarios
    assert [(entry.section, entry.together) for entry in scenario.trace] == [
        ("review#source", False),
        ("review#tests", True),
    ]


def test_a_set_beside_a_dispatch_states_the_dispatch_then_the_set() -> None:
    beside = next(item for item in DISPATCHING if item.name == "dispatch-beside")
    [scenario] = beside.scenarios
    assert [(entry.section, entry.together) for entry in scenario.trace] == [
        ("plan#work", False),
        ("review#source", False),
        ("review#tests", True),
    ]


def test_a_returned_question_is_answered_from_the_scenarios_answers() -> None:
    """The sub-agent asks, and its action shows the answer it was handed back."""
    question = next(item for item in DISPATCHING if item.name == "dispatch-question")
    [scenario] = question.scenarios
    [asked] = scenario.trace
    assert asked.section == "draft#choose"
    assert asked.action is not None
    _, value = asked.action
    assert f"`{value}`" in scenario.answers
    for form in question.forms:
        body = section_body(question.form(form), "draft.md", "choose")
        assert f"`{value}`" in body and "return that question" in body


def test_each_dispatched_section_states_the_action_its_trace_entry_holds() -> None:
    """A sub-agent's evidence is a file it writes, as a state's is."""
    for workflow in DISPATCHING:
        [scenario] = workflow.scenarios
        for entry in scenario.trace:
            assert entry.action is not None, (workflow.name, entry.section)
            name, value = entry.action
            document, _, heading = entry.section.partition("#")
            for form in workflow.forms:
                body = section_body(workflow.form(form), f"{document}.md", heading)
                assert f"`actions/{name}`" in body, (workflow.name, form, name)
                if not scenario.answers:
                    assert f"containing `{value}`" in body, (workflow.name, form)


def test_the_compiled_form_publishes_a_bundle_per_target_and_the_authored_none(
    tmp_path: Path,
) -> None:
    """Compilation adds a bundle per target; the authored form adds none."""
    for workflow in DISPATCHING:
        for form, several in ((COMPILED_FORM, True), (AUTHORED_FORM, False)):
            output = tmp_path / workflow.name / form
            output.mkdir(parents=True)
            run = bundle(workflow, form, output)
            assert run.returncode == 0 and not run.stderr, workflow.name
            written = bundled(output)
            assert (len(written) > 1) is several, (workflow.name, form, written)


def test_every_decision_is_exercised_both_ways() -> None:
    for workflow in CORPUS:
        for form in workflow.forms:
            for state, section in workflow.sections[form].items():
                if section.transition is None or section.transition.condition is None:
                    continue
                taken = {
                    path[index + 1]
                    for path in (scenario.path for scenario in workflow.scenarios)
                    for index, step in enumerate(path[:-1])
                    if step == state
                }
                leaving = {edge.target for edge in workflow.diagram.leaving(state)}
                assert taken == leaving, f"{workflow.name}: {state} is not taken both"


def test_one_state_is_reached_only_through_a_link_in_another_section() -> None:
    looping = next(workflow for workflow in CORPUS if workflow.name == "looping")
    unclicked = looping.diagram.states - set(looping.diagram.clicks)
    assert unclicked == {"Check"}
    linked = f"]({Path(document('Check')).name})"
    assert any(linked in section.body for section in looping.sections[DIAGRAM].values())


def test_the_instruction_names_the_entry_and_nothing_else_varies() -> None:
    assert "workflow.bundle.md describes a workflow" in instruction(
        "workflow.bundle.md"
    )
    assert instruction("a.md").replace("a.md", "b.md") == instruction("b.md")


def test_every_dispatching_form_names_the_sub_agent_trace() -> None:
    """AC25: each instruction tells the session the sub-agent trace to hand on.

    A sub-agent reads only the prompt its session writes, so the name the
    runner keeps reaches it only where the session's instruction states it.
    Every form's instruction states it, the forms that dispatch among them.
    """
    stated = SUB_AGENT_TRACE.format(section="<section>")
    assert {*DISPATCH_FORMS, BOOTSTRAP} <= set(FORMS)
    for form in FORMS:
        text = " ".join(instruction(ENTRY, form).split())
        assert f"append each state it enters as one line to {stated}" in text, form


def test_a_state_the_bundle_does_not_reach_is_a_fault(tmp_path: Path) -> None:
    workflow = broken(
        tmp_path,
        "linear",
        f"{DIAGRAM}/{ENTRY}",
        '    click Ship href "states/ship.md"\n',
        "",
    )
    output = tmp_path / "output"
    output.mkdir()
    assert bundle_faults(workflow, DIAGRAM, output) == [
        "the diagram bundle carries no section for Ship"
    ]


def test_a_dispatch_step_naming_no_document_is_a_fault(tmp_path: Path) -> None:
    workflow = broken(
        tmp_path,
        "dispatch-chain",
        f"{COMPILED_FORM}/{document('Request')}",
        "../plan.md#work",
        "../absent.md#work",
    )
    assert step_faults(workflow, COMPILED_FORM) == [
        "Request: a step dispatches ../absent.md, which is no document"
    ]


def test_a_dispatch_step_naming_no_section_is_a_fault(tmp_path: Path) -> None:
    workflow = broken(
        tmp_path,
        "dispatch-question",
        f"{COMPILED_FORM}/{document('Enquire')}",
        "../draft.md#choose",
        "../draft.md#absent",
    )
    assert step_faults(workflow, COMPILED_FORM) == [
        "Enquire: ../draft.md holds no absent section"
    ]


def test_a_scenario_naming_no_trace_is_a_fault(tmp_path: Path) -> None:
    """A dispatch scenario states the trace, so a table naming none is a fault."""
    workflow = broken(
        tmp_path,
        "dispatch-set",
        "scenarios.toml",
        "[[scenario.trace]]",
        "[[scenario.absent]]",
        count=-1,
    )
    faults = scenario_faults(workflow, workflow.scenarios[0])
    assert faults == [
        f"parallel-set: the {form} form dispatches ['review#source', 'review#tests'],"
        " not the [section, set] pairs the trace names: []"
        for form in (COMPILED_FORM, AUTHORED_FORM)
    ]


def test_a_trace_disagreeing_with_the_source_is_a_fault(tmp_path: Path) -> None:
    """A set's second target started alone is the trace the source denies."""
    workflow = broken(
        tmp_path,
        "dispatch-set",
        "scenarios.toml",
        'dispatch = "review#tests"\ntogether = true\n',
        'dispatch = "review#tests"\n',
    )
    faults = scenario_faults(workflow, workflow.scenarios[0])
    assert len(faults) == len(workflow.forms) and all(
        "parallel-set: the" in fault for fault in faults
    )


def test_a_scenario_states_each_pf_run_in_order_with_its_arguments() -> None:
    """AC1: a run names the agent making it and the references it compiles."""
    named = {workflow.name: workflow for workflow in CORPUS}
    for scenario in named["bootstrap-audit"].scenarios:
        assert scenario.compile == (
            Compile(None),
            Compile(None, "sources/workflow.md"),
        )
    assert [scenario.compile for scenario in named["dispatch-set"].scenarios] == [()]


def test_a_sub_agents_run_is_read_by_the_section_it_follows(tmp_path: Path) -> None:
    """AC1: a run a sub-agent makes names the section of the trace it follows."""
    workflow = broken(
        tmp_path,
        "dispatch-set",
        "scenarios.toml",
        'action = { file = "tests.txt", value = "tested" }\n',
        'action = { file = "tests.txt", value = "tested" }\n'
        '\n[[scenario.compile]]\nby = "review#tests"\n',
    )
    [scenario] = workflow.scenarios
    assert scenario.compile == (Compile("review#tests"),)
    assert compile_faults(workflow, scenario) == []


@pytest.mark.parametrize(
    ("run", "fault"),
    [
        (
            'entry = "absent.md#work"',
            "parallel-set: a run names absent.md#work, no document of its sources",
        ),
        (
            'entry = "#source"',
            "parallel-set: a run names #source, no document of its sources",
        ),
        (
            'by = "review#absent"',
            "parallel-set: a run by review#absent is by no start",
        ),
    ],
)
def test_a_stated_run_naming_no_document_of_the_sources_is_a_fault(
    tmp_path: Path, run: str, fault: str
) -> None:
    """AC1: the corpus test refuses a run naming what the sources do not hold."""
    workflow = broken(
        tmp_path,
        "dispatch-set",
        "scenarios.toml",
        'action = { file = "tests.txt", value = "tested" }\n',
        'action = { file = "tests.txt", value = "tested" }\n'
        f"\n[[scenario.compile]]\n{run}\n",
    )
    [scenario] = workflow.scenarios
    assert scenario_faults(workflow, scenario) == [fault]


def test_a_run_stated_by_a_workflow_running_no_command_is_a_fault(
    tmp_path: Path,
) -> None:
    """AC1: a workflow written in no shell form gives no session a run to make."""
    workflow = broken(
        tmp_path,
        "linear",
        "scenarios.toml",
        "inputs = {}\n",
        'inputs = {}\n\n[[scenario.compile]]\nentry = "workflow.md"\n',
    )
    [scenario] = workflow.scenarios
    assert scenario_faults(workflow, scenario) == [
        "straight-through: it states a pf run, and no form runs one"
    ]


@pytest.mark.parametrize(
    "run",
    [
        'entry = ["workflow.md"]',
        "entry = 1",
        "by = 2",
        "presets = 1",
        'presets = "mirror"',
    ],
    ids=str,
)
def test_a_run_whose_fields_are_not_references_is_refused(
    tmp_path: Path, run: str
) -> None:
    """AC1: one entry and its preset list describe each compiling run."""
    with pytest.raises(CorpusError, match="parallel-set: a run's"):
        broken(
            tmp_path,
            "dispatch-set",
            "scenarios.toml",
            'action = { file = "tests.txt", value = "tested" }\n',
            'action = { file = "tests.txt", value = "tested" }\n'
            f"\n[[scenario.compile]]\n{run}\n",
        )


def test_a_compiled_step_stating_its_dispatch_in_prose_is_a_fault(
    tmp_path: Path,
) -> None:
    """The operator is the statement, so a sentence beside it states it twice."""
    workflow = broken(
        tmp_path,
        "dispatch-chain",
        f"{COMPILED_FORM}/{document('Request')}",
        "1. [⇉ plan](../plan.md#work).",
        "1. Hand the plan to a sub-agent: [⇉ plan](../plan.md#work).",
    )
    assert step_faults(workflow, COMPILED_FORM) == [
        "Request: a compiled step states 'sub-agent', which its protocol states,"
        " rather than its operators alone: '1. Hand the plan to a sub-agent:"
        " [⇉ plan](../plan.md#work).'"
    ]


def test_a_compiled_step_carrying_an_unmarked_link_is_a_fault(
    tmp_path: Path,
) -> None:
    """A compiled step dispatches by its marks, so an unmarked link dispatches none."""
    workflow = broken(
        tmp_path,
        "dispatch-set",
        f"{COMPILED_FORM}/{document('Survey')}",
        "1. [⫽ source](../review.md#source) and [⫽ tests](../review.md#tests).",
        "1. [⫽ source](../review.md#source) and [tests](../review.md#tests).",
    )
    assert step_faults(workflow, COMPILED_FORM) == [
        "Survey: a compiled step carries an unmarked link: '1. [⫽ source]"
        "(../review.md#source) and [tests](../review.md#tests).'"
    ]


def test_a_compiled_step_repeating_its_protocol_is_a_fault(tmp_path: Path) -> None:
    """A step dispatching a set states nothing the parallel protocol does not."""
    workflow = broken(
        tmp_path,
        "dispatch-set",
        f"{COMPILED_FORM}/{document('Survey')}",
        "1. [⫽ source](../review.md#source) and [⫽ tests](../review.md#tests).",
        "1. [⫽ source](../review.md#source) and [⫽ tests](../review.md#tests)"
        " together.",
    )
    assert step_faults(workflow, COMPILED_FORM) == [
        "Survey: a compiled step states 'together', which its protocol states,"
        " rather than its operators alone: '1. [⫽ source](../review.md#source)"
        " and [⫽ tests](../review.md#tests) together.'"
    ]


def test_a_prose_section_edited_beyond_its_transition_is_a_fault(
    tmp_path: Path,
) -> None:
    workflow = broken(
        tmp_path, "branching", f"{PROSE}/{document('Queue')}", "queued", "held"
    )
    assert section_faults(workflow) == [
        "Queue: the prose section differs from the diagram's"
    ]


def test_a_prose_transition_naming_another_state_is_a_fault(tmp_path: Path) -> None:
    workflow = broken(
        tmp_path,
        "linear",
        f"{PROSE}/{document('Build')}",
        "[Test](test.md)",
        "[Ship](ship.md)",
    )
    assert transition_faults(workflow) == [
        "Build: the prose names states the diagram does not"
    ]


def test_a_linked_rule_naming_a_state_its_decision_does_not_reach_is_a_fault(
    tmp_path: Path,
) -> None:
    workflow = broken(
        tmp_path,
        "branching",
        "linked/rules/a.md",
        "The transition into `Escalate` applies.",
        "The transition into `Notify` applies.",
    )
    assert "Triage: the linked rules name states the diagram does not" in (
        transition_faults(workflow)
    )


def test_a_linked_rule_that_states_no_state_is_a_fault(tmp_path: Path) -> None:
    with pytest.raises(CorpusError, match="states no state"):
        broken(
            tmp_path,
            "branching",
            "linked/rules/b.md",
            "The transition into `Queue` applies.",
            "Queue the incident.",
        )


def test_a_linked_decision_must_state_its_branch_outside_its_sections(
    tmp_path: Path,
) -> None:
    """Stating a branch's label in the section itself is not a linked transition."""
    with pytest.raises(CorpusError, match="no linked transition reads as"):
        broken(
            tmp_path,
            "branching",
            f"{LINKED_FORM}/{document('Triage')}",
            "Otherwise, take the transition [rule B](../rules/b.md) names.",
            "Otherwise, take the transition labelled `low`.",
        )


def test_a_linked_decision_resolves_its_branch_through_the_document(
    tmp_path: Path,
) -> None:
    """The linked form walks the path only when each rule states its branch."""
    workflow = broken(
        tmp_path,
        "looping",
        "linked/rules/a.md",
        "The transition into `Revise` applies.",
        "The transition into `Publish` applies.",
    )
    faults = scenario_faults(workflow, workflow.scenarios[1])
    assert any("two-rounds" in fault for fault in faults)


@pytest.mark.parametrize("form", LINKING, ids=lambda item: item.name)
def test_the_linked_bundle_draws_no_branch_label(
    form: Workflow, tmp_path: Path
) -> None:
    """A bundle of the linked form carries its entry's flowchart unlabelled."""
    assert bundle(form, LINKED_FORM, tmp_path).returncode == 0
    drawn = [
        body
        for kind, body in FENCE.findall((tmp_path / form.entry_bundle).read_text())
        if kind == "mermaid"
    ]
    assert len(drawn) == 1
    edges = drawn_edges(drawn)
    assert len(edges) == len(form.diagram.edges)
    assert [edge.group(0).strip() for edge in edges if edge.group(2) is not None] == []


def test_a_linked_entry_labelling_a_branch_is_a_fault(tmp_path: Path) -> None:
    workflow = broken(
        tmp_path,
        "branching",
        f"{LINKED_FORM}/{ENTRY}",
        "    Triage --> Escalate",
        "    Triage -->|high| Escalate",
    )
    assert entry_faults(workflow, LINKED_FORM) == [
        "the linked entry labels the edge Triage to Escalate 'high'"
    ]


def test_a_linked_entry_drawing_another_edge_is_a_fault(tmp_path: Path) -> None:
    workflow = broken(
        tmp_path,
        "branching",
        f"{LINKED_FORM}/{ENTRY}",
        "    Triage --> Queue",
        "    Triage --> Notify",
    )
    assert entry_faults(workflow, LINKED_FORM) == [
        "the linked entry draws edges the diagram does not"
    ]


def test_a_prose_entry_drawing_a_diagram_is_a_fault(tmp_path: Path) -> None:
    workflow = broken(
        tmp_path,
        "linear",
        f"{PROSE}/{ENTRY}",
        "# Release\n",
        "# Release\n\n```mermaid\nflowchart TD\n    Plan --> Build\n```\n",
    )
    assert entry_faults(workflow, PROSE) == ["the prose entry draws a diagram"]


def test_a_scenario_path_with_a_step_the_diagram_does_not_draw_is_a_fault(
    tmp_path: Path,
) -> None:
    workflow = broken(
        tmp_path,
        "looping",
        "scenarios.toml",
        '"Draft",\n    "Review",\n    "Publish",',
        '"Draft",\n    "Publish",',
    )
    faults = scenario_faults(workflow, workflow.scenarios[0])
    assert "no-rework: the diagram reaches no Publish from Draft" in faults


def test_a_scenario_path_its_inputs_do_not_lead_through_is_a_fault(
    tmp_path: Path,
) -> None:
    workflow = broken(
        tmp_path,
        "branching",
        "scenarios.toml",
        '"severity.txt" = "low"',
        '"severity.txt" = "high"',
    )
    faults = scenario_faults(workflow, workflow.scenarios[1])
    assert [fault.split(":")[0] for fault in faults] == ["low-severity"] * len(
        workflow.forms
    )


def bundled_state(text: str, state: str) -> str:
    """One state's section of a bundle, up to the next file heading."""
    start = re.search(rf"^# {state}$", text, re.MULTILINE)
    assert start is not None, f"the bundle carries no section for {state}"
    rest = text[start.end() :]
    end = re.search(r"^# ", rest, re.MULTILINE)
    return rest if end is None else rest[: end.start()]


def permutation_faults(workflow: Workflow, carriers: dict[str, str]) -> list[str]:
    """How a scenario misses the state carrying its permutation.

    Each scenario names one permutation, and the state whose section carries
    it is on that scenario's path and on no other scenario's, so a pass of
    the scenario is a pass through that permutation alone.
    """
    faults = []
    for scenario in workflow.scenarios:
        for name, state in carriers.items():
            if (state in scenario.path) != (name == scenario.name):
                faults.append(f"{scenario.name}: its path and {state} disagree")
    if sorted(carriers) != sorted(scenario.name for scenario in workflow.scenarios):
        faults.append(f"{workflow.name}: the scenarios are not {sorted(carriers)}")
    return faults


CORPUS_BY_NAME = {workflow.name: workflow for workflow in CORPUS}


def test_a_section_entry_compiles_its_section_alone(tmp_path: Path) -> None:
    """AC26: `pf` compiles the handbook from its Onboarding section alone.

    The entry names one section of `workflow.md`, so the bundle carries the
    workflow that section draws, each state its scenario's path enters, and
    none of the handbook's other sections, which the whole document carries.
    """
    workflow = CORPUS_BY_NAME["section-entry"]
    assert workflow.entry == "workflow.md#onboarding"
    assert workflow.entry_bundle == Path(
        "workflow__onboarding.bundles", "workflow__onboarding.bundle.md"
    )
    [scenario] = workflow.scenarios
    assert scenario.name == "document-fragment"
    text = compiled_bundle(workflow, tmp_path / "section")
    for state in scenario.path:
        action = workflow.walked[state].action
        if action is None:
            continue
        name, value = action
        expected = f"Write `actions/{name}` containing `{value}`."
        assert expected in bundled_state(text, state)
    assert "Upkeep" not in text and "# Notes" not in text
    whole = compiled_bundle(replace(workflow, entry=ENTRY), tmp_path / "whole")
    assert "# Notes" in whole


def test_composed_sections_stand_beneath_the_step_naming_them(tmp_path: Path) -> None:
    """AC27: each scenario passes through the step its permutation composes.

    Two sources merge into one destination section beneath `Configure`; a
    deferred directive beneath `Migrate` publishes the `↳` line a later run
    activates; and a directive inside the contribution beneath `Amend`
    composes beneath that contribution.
    """
    workflow = CORPUS_BY_NAME["section-composition"]
    assert (
        permutation_faults(
            workflow,
            {
                "merged-sources": "Configure",
                "deferred-occurrence": "Migrate",
                "nested-composition": "Amend",
            },
        )
        == []
    )
    text = compiled_bundle(workflow, tmp_path / "entry")
    merged = bundled_state(text, "Configure")
    assert merged.count("## Inputs") == 1
    assert merged.index("## Inputs") < merged.index("### Settings")
    assert merged.index("### Settings") < merged.index("### Schema")
    deferred = bundled_state(text, "Migrate")
    assert "### Migration\n\n[↳ Steps](reference/migration.md#steps)" in deferred
    assert "Copy the rows" not in text
    nested = bundled_state(text, "Amend")
    assert nested.index("### Amendment") < nested.index("#### Rules")
    assert nested.index("#### Rules") < nested.index("##### Lint")
    activated = compiled_bundle(
        replace(workflow, entry="reference/migration.md#steps"), tmp_path / "later"
    )
    assert "Copy the rows" in activated


def test_a_declared_link_is_followed_and_an_undeclared_one_left_as_text(
    tmp_path: Path,
) -> None:
    """AC28: a link is compiled by its target's declaration.

    `Inspect` links `Verify`, which declares `prosiform`, so the bundle
    carries `Verify` and the link names its section; `Liaise` links a
    document under `undeclared/`, so the link stays as written and the
    bundle carries none of the document.
    """
    workflow = CORPUS_BY_NAME["declared-inclusion"]
    assert (
        permutation_faults(
            workflow,
            {
                "declared-link-followed": "Verify",
                "undeclared-link-as-text": "Liaise",
            },
        )
        == []
    )
    assert "Verify" not in workflow.diagram.clicks
    text = compiled_bundle(workflow, tmp_path)
    assert "[Verify](#verify)" in bundled_state(text, "Inspect")
    assert "Write `actions/verify.txt`" in bundled_state(text, "Verify")
    link = f"[handover notes](../{UNDECLARED}/handover.md)"
    assert link in bundled_state(text, "Liaise")
    assert "# Handover" not in text


def test_a_document_declaring_under_the_undeclared_directory_is_a_fault(
    tmp_path: Path,
) -> None:
    """A declared document there would be followed, so its link is no longer text."""
    broken(
        tmp_path,
        "declared-inclusion",
        f"{DIAGRAM}/{UNDECLARED}/handover.md",
        "# Handover",
        "---\nprosiform: {}\n---\n# Handover",
    )
    assert declaration_faults(tmp_path) == [
        f"declared-inclusion/{DIAGRAM}/{UNDECLARED}/handover.md declares prosiform"
        f" under {UNDECLARED}/"
    ]


UNHELD = "Unheld"
"""A state name no diagram of the corpus holds, which an invented state enters."""


def scored(
    workflow: Workflow,
    scenario: Scenario,
    workspace: Path,
    trace: tuple[str, ...],
    starts: tuple[Start, ...],
    undone: str = "",
    commands: tuple[str, ...] | None = None,
    withholds: str = "",
) -> Failure | None:
    """The class a workspace holding one trace and its actions is scored.

    `commands` is what the workspace's record says the session ran, and a
    record naming none says the harness reports no command, as a form given
    no shell does. `withholds` names an action file the workspace leaves
    unwritten, whichever agent would have written it.
    """
    workspace.mkdir(parents=True)
    (workspace / TRACE).write_text("".join(f"{state}\n" for state in trace))
    (workspace / ACTIONS).mkdir()
    for state in trace:
        if state in workflow.walked and state != undone:
            action = workflow.walked[state].action
            if action is None:
                continue
            name, value = action
            (workspace / ACTIONS / name).write_text(f"{value}\n")
    held: dict[str, object] = {"starts": [start.record() for start in starts]}
    if commands is not None:
        held["commands"] = list(commands)
    (workspace / SUBAGENTS).write_text(json.dumps(held))
    for due in scenario.trace:
        if due.action is not None and due.action[0] != withholds:
            name, value = due.action
            (workspace / ACTIONS / name).write_text(f"{value}\n")
    return score(workflow, scenario, workspace).failure


def stated_commands(scenario: Scenario) -> list[str]:
    """The session's `pf` runs a scenario states, as shell lines."""
    return [shlex.join(("pf", *run.args)) for run in scenario.compile if run.by is None]


def produced(workflow: Workflow, scenario: Scenario, root: Path) -> set[Failure]:
    """Every class a session of one scenario can be scored.

    A session is given the scenario's path with one departure each: an action
    left undone, the last state left out, a state the diagram does not hold,
    any diagram state entered at any index of the path or after its end, the
    sources followed without compiling them in a form that must, and a
    dispatch record missing, split or answered in a sub-agent's place. A
    session whose agent reported an error is `errored` on any scenario.
    """
    path = scenario.path
    correct = tuple(Start(due.section, "done", due.together) for due in scenario.trace)
    workspaces = (root / str(index) for index in itertools.count())

    def departing(
        trace: tuple[str, ...],
        starts: tuple[Start, ...] = correct,
        undone: str = "",
        commands: tuple[str, ...] | None = None,
        withholds: str = "",
    ) -> Failure | None:
        return scored(
            workflow,
            scenario,
            next(workspaces),
            trace,
            starts,
            undone,
            commands,
            withholds,
        )

    found = {
        errored(workflow, scenario).failure,
        departing(path, undone=path[0]),
        departing(path[:-1]),
        departing((*path[:1], UNHELD)),
    }
    states = sorted(workflow.diagram.states)
    for index in range(len(path) + 1):
        due = path[index] if index < len(path) else None
        found |= {departing((*path[:index], state)) for state in states if state != due}
    # A scenario stating `pf` runs is held to them wherever its record says
    # what the session ran, so the three run classes are produced from the
    # runs the scenario states and one departure from each.
    stated = stated_commands(scenario)
    if stated:
        found.add(departing(path, commands=()))
        found.add(departing(path, commands=("pf --entry absent.md#none", *stated)))
        if len(stated) > 1:
            found.add(departing(path, commands=tuple(reversed(stated))))
    for dispatch in scenario.trace:
        if dispatch.action is not None:
            found.add(departing(path, withholds=dispatch.action[0]))
    if correct:
        found.add(departing(path, ()))
        found.add(departing(path, tuple(replace(s, together=False) for s in correct)))
        found.add(
            departing(path, tuple(replace(s, returned="question") for s in correct))
        )
    return {failure for failure in found if failure is not None}


def unreached(corpus: list[Workflow], root: Path) -> list[str]:
    """Each failure class the scorer defines that no scenario of a corpus produces."""
    reached: set[Failure] = set()
    for workflow in corpus:
        for scenario in workflow.scenarios:
            reached |= produced(
                workflow, scenario, root / workflow.name / scenario.name
            )
    return [
        f"no scenario produces {failure}"
        for failure in Failure
        if failure not in reached
    ]


def test_every_failure_class_is_produced_by_some_scenario(tmp_path: Path) -> None:
    """AC1: each class the scorer defines, and `errored`, has a scenario."""
    assert unreached(CORPUS, tmp_path) == []


def test_a_class_no_scenario_produces_is_named(tmp_path: Path) -> None:
    linear = [workflow for workflow in CORPUS if workflow.name == "linear"]
    assert unreached(linear, tmp_path) == [
        f"no scenario produces {failure}"
        for failure in (
            Failure.LOOP_MISCOUNT,
            Failure.MISSING_ACTION,
            Failure.UNDISPATCHED,
            Failure.SEQUENTIAL_SET,
            Failure.UNRELAYED_QUESTION,
            Failure.UNCOMPILED,
            Failure.OVERCOMPILED,
            Failure.MISORDERED_COMPILE,
        )
    ]


def decided(workflow: Workflow, scenario: Scenario) -> list[str]:
    """The states of a scenario's path whose section decides between two edges."""
    return [
        state
        for state in dict.fromkeys(scenario.path)
        if (transition := workflow.walked[state].transition) is not None
        and transition.condition is not None
    ]


def test_a_path_meets_a_second_decision_after_its_first() -> None:
    """Pricing reads each decision's own input, so a branch is not carried over."""
    pricing = next(workflow for workflow in CORPUS if workflow.name == "pricing")
    for scenario in pricing.scenarios:
        assert decided(pricing, scenario) == ["Screen", "Price"], scenario.name
    branches = {
        tuple(
            scenario.path[scenario.path.index(state) + 1]
            for state in ("Screen", "Price")
        )
        for scenario in pricing.scenarios
    }
    assert branches == {("Hold", "Invoice"), ("Price", "Discount")}


def test_a_loop_counts_four_rounds_of_a_state_reached_only_through_a_link() -> None:
    """Rework's bound counts Retest, which no click names, over four rounds."""
    rework = next(workflow for workflow in CORPUS if workflow.name == "rework")
    transition = rework.walked["Measure"].transition
    assert transition is not None and transition.condition is not None
    counted = FEWER.match(transition.condition)
    assert counted is not None and counted.group(1) == "Retest"
    assert rework.diagram.states - set(rework.diagram.clicks) == {"Retest"}
    linked = f"]({Path(document('Retest')).name})"
    for form in rework.forms:
        assert linked in rework.sections[form]["Rework"].body, form
    assert max(scenario.path.count("Retest") for scenario in rework.scenarios) == 4


def test_a_drawn_state_no_edge_leads_to_is_linked_from_a_terminal_section() -> None:
    """Refund is drawn and linked from Invoice, and no edge leads to it."""
    pricing = next(workflow for workflow in CORPUS if workflow.name == "pricing")
    entered = {edge.target for edge in pricing.diagram.edges}
    assert pricing.diagram.states - entered == {"Entry", "Refund"}
    linked = f"]({Path(document('Refund')).name})"
    for form in pricing.forms:
        assert linked in pricing.sections[form]["Invoice"].body, form
    assert all("Refund" not in scenario.path for scenario in pricing.scenarios)


LINK = re.compile(r"\[[^\]]*\]\(([^)]*)\)")
"""A link a bundle carries, with its destination."""


def link_faults(workflow: Workflow, output: Path) -> list[str]:
    """Each link the linked form's bundle leaves naming a document.

    `pf` follows a link into a document declaring `prosiform` and rewrites it
    to the heading it carries, so a destination still naming a file is a link
    into a document that declares nothing.
    """
    run = bundle(workflow, LINKED_FORM, output)
    if run.returncode != 0:
        return [f"pf exited {run.returncode}"]
    text = (output / workflow.entry_bundle).read_text()
    return [
        f"the linked bundle leaves {destination} as written"
        for destination in LINK.findall(text)
        if not destination.startswith("#")
    ]


@pytest.mark.parametrize("workflow", LINKING, ids=lambda item: item.name)
def test_every_link_the_linked_form_writes_compiles(
    workflow: Workflow, tmp_path: Path
) -> None:
    """AC5: every document a linked form links declares `prosiform`."""
    assert link_faults(workflow, tmp_path) == []


def test_a_linked_rule_declaring_nothing_is_left_as_written(tmp_path: Path) -> None:
    workflow = broken(
        tmp_path,
        "pricing",
        f"{LINKED_FORM}/rules/c.md",
        "---\nprosiform: {}\n---\n",
        "",
    )
    output = tmp_path / "output"
    output.mkdir()
    assert link_faults(workflow, output) == [
        "the linked bundle leaves ../rules/c.md as written"
    ]
