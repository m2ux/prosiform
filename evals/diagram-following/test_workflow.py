"""Hold the diagram-following corpus to what the eval relies on.

Every workflow document declares `prosiform` as a mapping of presets;
every form a workflow is written in bundles cleanly, reporting only the
warnings it declares, and carries every state's section, and its entry
carries only what its form allows; the forms' sections differ only in their
transition paragraphs, and a dispatch form's in the step handing a section
to a sub-agent too; and each scenario's path is a walk of the diagram from
its start to a terminal state that every form's sections lead through for
the scenario's inputs, and the diagram form's bundle states, with the
dispatch trace its sources state. Each property is a function returning the faults it
finds, so the corpus is held to an empty list and a copy of it broken on
purpose is held to a fault.
"""

import re
import shutil
from pathlib import Path

import pytest
from ruamel.yaml import YAML
from score import SUB_AGENT_TRACE
from workflow import (
    AUTHORED_FORM,
    BOOTSTRAP,
    COMPILED_FORM,
    COMPILED_STEP,
    DIAGRAM,
    DISPATCH_FORMS,
    EDGE,
    ENTRY,
    ENTRY_BUNDLE,
    FENCE,
    FORMS,
    FRONTMATTER,
    LINKED_FORM,
    MARKED_FORMS,
    PROSE,
    STATES,
    STEP_ONE,
    STEP_SET,
    TRANSITION,
    UNDRAWN,
    UNLABELLED,
    WORKFLOWS,
    CorpusError,
    Scenario,
    Workflow,
    bundle,
    bundle_walk,
    bundled,
    bundled_sections,
    dispatch_walk,
    dispatched,
    inputs_read,
    instruction,
    read_workflow,
    reported,
    stray,
    walk,
    workflows,
)

BUNDLED_HEADING = re.compile(r"^#+ (\w+)$", re.MULTILINE)
CORPUS = workflows()
DISPATCHING = [workflow for workflow in CORPUS if COMPILED_FORM in workflow.forms]
DRAWING = [workflow for workflow in CORPUS if DIAGRAM in workflow.forms]
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
    the build reads a preset.
    """
    faults = []
    for path in sorted(root.rglob("*.md")):
        where = path.relative_to(root)
        block = FRONTMATTER.match(path.read_text())
        front = YAML(typ="safe", pure=True).load(block.group()[4:-4]) if block else None
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


def bundle_faults(workflow: Workflow, form: str, output: Path) -> list[str]:
    """How one form's bundle set falls short of a clean run under `output`.

    The run must exit 0, report each warning its workflow declares and no
    other diagnostic, and write the entry's bundle
    carrying every state. A dispatch form must publish a bundle for each
    document its steps dispatch, and a form that dispatches nothing must
    publish the entry's bundle alone.
    """
    run = bundle(workflow.form(form), output)
    faults = []
    if run.returncode != 0:
        faults.append(f"pf exited {run.returncode}")
    if extra := stray(workflow, run.stderr):
        faults.append(f"pf reported {extra!r}")
    for code in sorted(workflow.warnings - reported(run.stderr)):
        faults.append(f"pf reported no {code}")
    bundled_written = bundled(output)
    if output / ENTRY_BUNDLE not in bundled_written:
        faults.append(f"pf wrote {[path.name for path in bundled_written]}")
        return faults
    carried = set(BUNDLED_HEADING.findall((output / ENTRY_BUNDLE).read_text()))
    for state in sorted(workflow.diagram.states - carried):
        faults.append(f"the {form} bundle carries no section for {state}")
    published = {
        path.name.split("__")[0]
        for path in bundled_written
        if path != output / ENTRY_BUNDLE
    }
    if form in MARKED_FORMS:
        targets = {
            target.partition("#")[0].split("/")[-1]
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
            if (drawn_section.transition is None) != (
                written_section.transition is None
            ):
                faults.append(
                    f"{state}: the {form} form and the diagram disagree on ending"
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
            if drawn is None:
                if leaving or state not in diagram.terminals:
                    faults.append(
                        f"{state}: the {form} section ends a workflow the diagram"
                        f" does not"
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
    """How a scenario's path or trace fails to be what its sources state."""
    diagram = workflow.diagram
    path = scenario.path
    faults = []
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
    for form in workflow.forms:
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
    if not scenario.trace:
        faults.append(f"{scenario.name}: it names no dispatch trace")
        return faults
    for form in dispatching:
        stated = dispatch_walk(workflow, form, scenario.inputs)
        named = tuple((entry.section, entry.together) for entry in scenario.trace)
        if named != stated:
            faults.append(
                f"{scenario.name}: the {form} form dispatches {[s for s, _ in stated]}"
                f", not the [section, set] pairs the trace names: {list(named)}"
            )
    return faults


def compiled_bundle(workflow: Workflow, output: Path) -> str:
    """The entry bundle `pf` compiles from a workflow's diagram form."""
    run = bundle(workflow.form(DIAGRAM), output)
    assert run.returncode == 0, run.stderr.decode()
    return (output / ENTRY_BUNDLE).read_text()


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
        "dispatch-beside",
        "dispatch-chain",
        "dispatch-question",
        "dispatch-set",
        "group-placement",
        "linear",
        "looping",
        "preset-selection",
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
        run = bundle(workflow.form(form), output)
        assert run.returncode == 0, (workflow.name, form, run.stderr.decode())
        assert run.stderr == b"", (workflow.name, form, run.stderr.decode())
        assert (output / ENTRY_BUNDLE).is_file(), (workflow.name, form)


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


def test_the_title_linking_a_document_selects_the_presets_placing_it(
    tmp_path: Path,
) -> None:
    """AC23: default alone, one preset a title selects, and two one title selects.

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
    is reached under its default and under `announce`, so it stands in both
    groups, its section emitted once in each.
    """
    workflow = read_workflow(WORKFLOWS / "group-placement")
    text = compiled_bundle(workflow, tmp_path)
    assert enclosing(text, "Lint") == enclosing(text, "Unit") == ["Delivery", "Checks"]
    assert enclosing(text, "Package") == ["Compile", "Packaging"]
    assert enclosing(text, "Sign") == ["Compile", "Packaging", "Signing"]
    assert enclosing(text, "Notify", 0)[-1] == "Messages"
    assert enclosing(text, "Notify", 1)[-1] == "Announcements"


def test_subst_pairs_redirect_the_links_a_document_writes(tmp_path: Path) -> None:
    """AC25: a document redirect, a section redirect, a preset holding over default.

    The entry's default sends the diagram's Approve to another document,
    Amend's default sends its Inspect link to one section of the handbook, and
    the entry's title selects Stage's `release` preset, whose Gate pair holds
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
        "preset-over-default: the bundle leads ('Outline', 'Amend', 'Inspect',"
        " 'Approve')"
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
    assert [(entry.section, entry.returned) for entry in scenario.trace] == [
        ("plan#work", "done"),
        ("review#check", "done"),
    ]


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


def test_a_returned_question_is_dispatched_again_with_the_answers() -> None:
    question = next(item for item in DISPATCHING if item.name == "dispatch-question")
    [scenario] = question.scenarios
    asked, answered = scenario.trace
    assert asked.section == answered.section == "draft#choose"
    assert (asked.returned, answered.returned) == ("question", "done")


def test_the_compiled_form_publishes_a_bundle_per_target_and_the_authored_none(
    tmp_path: Path,
) -> None:
    """Compilation adds a bundle per target; the authored form adds none."""
    for workflow in DISPATCHING:
        for form, several in ((COMPILED_FORM, True), (AUTHORED_FORM, False)):
            output = tmp_path / workflow.name / form
            output.mkdir(parents=True)
            run = bundle(workflow.form(form), output)
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
        assert f"tell it to append each state it enters as one line to {stated}" in text


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
    assert faults == ["parallel-set: it names no dispatch trace"]


def test_a_trace_disagreeing_with_the_source_is_a_fault(tmp_path: Path) -> None:
    """A set's second target started alone is the trace the source denies."""
    workflow = broken(
        tmp_path,
        "dispatch-set",
        "scenarios.toml",
        'dispatch = "review#tests"\nreturned = "done"\ntogether = true\n',
        'dispatch = "review#tests"\nreturned = "done"\n',
    )
    faults = scenario_faults(workflow, workflow.scenarios[0])
    assert len(faults) == len(DISPATCH_FORMS) and all(
        "parallel-set: the" in fault for fault in faults
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


@pytest.mark.parametrize("workflow", ["branching", "looping"])
def test_the_linked_bundle_draws_no_branch_label(workflow: str, tmp_path: Path) -> None:
    """A bundle of the linked form carries its entry's flowchart unlabelled."""
    form = read_workflow(WORKFLOWS / workflow)
    assert bundle(form.form(LINKED_FORM), tmp_path).returncode == 0
    drawn = [
        body
        for kind, body in FENCE.findall((tmp_path / ENTRY_BUNDLE).read_text())
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
        '"Draft", "Review", "Publish"',
        '"Draft", "Publish"',
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
