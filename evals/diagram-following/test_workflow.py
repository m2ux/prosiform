"""Hold the diagram-following corpus to what the eval relies on.

Every form a workflow is written in bundles cleanly and carries every
state's section; the forms' sections differ only in their transition
paragraphs, and a dispatch form's in the step handing a section to a
sub-agent too; and each scenario's path is a walk of the diagram from its
start to a terminal state that every form's sections lead through for the
scenario's inputs, with the dispatch trace its sources state. Each property
is a function returning the faults it finds, so the corpus is held to an
empty list and a copy of it broken on purpose is held to a fault.
"""

import re
import shutil
from pathlib import Path

import pytest
from workflow import (
    AUTHORED_FORM,
    BOOTSTRAP,
    COMPILED_FORM,
    COMPILED_STEP,
    DIAGRAM,
    DISPATCH_FORMS,
    ENTRY,
    ENTRY_BUNDLE,
    FORMS,
    LINKED_FORM,
    MARKED_FORMS,
    PROSE,
    STATES,
    STEP_ONE,
    STEP_SET,
    TRANSITION,
    WORKFLOWS,
    CorpusError,
    Scenario,
    Workflow,
    bundle,
    bundled,
    dispatch_walk,
    dispatched,
    inputs_read,
    instruction,
    read_workflow,
    walk,
    workflows,
)

BUNDLED_HEADING = re.compile(r"^# (\w+)$", re.MULTILINE)
CORPUS = workflows()
DISPATCHING = [workflow for workflow in CORPUS if COMPILED_FORM in workflow.forms]


def document(state: str) -> str:
    """The path of a state's document within a form."""
    return f"{STATES}/{state.lower()}.md"


def bundle_faults(workflow: Workflow, form: str, output: Path) -> list[str]:
    """How one form's bundle set falls short of a clean run under `output`.

    The run must exit 0 with no diagnostic and write the entry's bundle
    carrying every state. A dispatch form must publish a bundle for each
    document its steps dispatch, and a form that dispatches nothing must
    publish the entry's bundle alone.
    """
    run = bundle(workflow.form(form), output)
    faults = []
    if run.returncode != 0:
        faults.append(f"pf exited {run.returncode}")
    if run.stderr:
        faults.append(f"pf reported {run.stderr.decode()!r}")
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
    leaving its state, and a prose section naming a state to the states those
    labels lead to. A dispatch form writes its transitions as the diagram
    form does, so it is held to the labels too.
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
            elif drawn.condition is None and labels != {None}:
                faults.append(f"{state}: no one unlabelled edge leaves it")
            elif drawn.condition is not None and labels != {
                drawn.then,
                drawn.otherwise,
            }:
                faults.append(f"{state}: its labels are not the edges leaving it")
            if TRANSITION[form] == LINKED_FORM:
                stated = {drawn.then, drawn.otherwise} - {None}
                if stated != labels - {None}:
                    faults.append(
                        f"{state}: the linked rules state labels the diagram does not"
                    )
    for node, destination in sorted(diagram.clicks.items()):
        if destination != document(node):
            faults.append(f"the click on {node} links {destination}, not its document")
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
        "linear",
        "looping",
    ]


def test_every_form_is_written_by_some_workflow() -> None:
    assert {form for workflow in CORPUS for form in workflow.forms} == set(FORMS)


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
    ("workflow", "scenario"),
    [(workflow, scenario) for workflow in CORPUS for scenario in workflow.scenarios],
    ids=lambda item: item.name,
)
def test_each_scenario_path_is_the_walk_its_inputs_determine(
    workflow: Workflow, scenario: Scenario
) -> None:
    assert scenario_faults(workflow, scenario) == []


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


def test_a_linked_rule_stating_another_label_is_a_fault(tmp_path: Path) -> None:
    workflow = broken(
        tmp_path,
        "branching",
        "linked/rules/escalation.md",
        "The transition labelled `high` applies.",
        "The transition labelled `low` applies.",
    )
    assert "Triage: the linked rules state labels the diagram does not" in (
        transition_faults(workflow)
    )


def test_a_linked_rule_that_states_no_label_is_a_fault(tmp_path: Path) -> None:
    with pytest.raises(CorpusError, match="states no label"):
        broken(
            tmp_path,
            "branching",
            "linked/rules/queue.md",
            "The transition labelled `low` applies.",
            "Queue the incident.",
        )


def test_a_linked_decision_must_state_a_label_outside_its_sections(
    tmp_path: Path,
) -> None:
    """Stating a branch's label in the section itself is not a linked transition."""
    with pytest.raises(CorpusError, match="no linked transition reads as"):
        broken(
            tmp_path,
            "branching",
            f"{LINKED_FORM}/{document('Triage')}",
            "Otherwise, take the transition labelled in [the queue rule]"
            "(../rules/queue.md).",
            "Otherwise, take the transition labelled `low`.",
        )


def test_a_linked_decision_resolves_the_label_through_the_document(
    tmp_path: Path,
) -> None:
    """The linked form walks the path only when each rule states its label."""
    workflow = broken(
        tmp_path,
        "looping",
        "linked/rules/rework.md",
        "The transition labelled `revise` applies.",
        "The transition labelled `approve` applies.",
    )
    faults = scenario_faults(workflow, workflow.scenarios[1])
    assert any("two-rounds" in fault for fault in faults)


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
