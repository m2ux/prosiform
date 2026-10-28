"""Hold the diagram-following corpus to what the eval relies on.

Each workflow's diagram and prose forms bundle cleanly and carry every
state's section; the two forms' sections differ only in their transition
paragraphs; and each scenario's path is a walk of the diagram from its
start to a terminal state that both forms' sections lead through for the
scenario's inputs. Each property is a function returning the faults it
finds, so the corpus is held to an empty list and a copy of it broken on
purpose is held to a fault.
"""

import re
import shutil
from pathlib import Path

import pytest
from workflow import (
    DIAGRAM,
    ENTRY,
    ENTRY_BUNDLE,
    FORMS,
    PROSE,
    STATES,
    WORKFLOWS,
    Scenario,
    Workflow,
    bundle,
    inputs_read,
    instruction,
    read_workflow,
    walk,
    workflows,
)

BUNDLED_HEADING = re.compile(r"^# (\w+)$", re.MULTILINE)
CORPUS = workflows()


def document(state: str) -> str:
    """The path of a state's document within a form."""
    return f"{STATES}/{state.lower()}.md"


def bundle_faults(workflow: Workflow, form: str, output: Path) -> list[str]:
    """How one form's bundle falls short of a clean run, written under
    `output` as the one bundle of its set, carrying every state."""
    run = bundle(workflow.form(form), output)
    faults = []
    if run.returncode != 0:
        faults.append(f"pf exited {run.returncode}")
    if run.stderr:
        faults.append(f"pf reported {run.stderr.decode()!r}")
    written = sorted(path for path in output.rglob("*") if path.is_file())
    if written != [output / ENTRY_BUNDLE]:
        faults.append(f"pf wrote {[str(p.relative_to(output)) for p in written]}")
        return faults
    carried = set(BUNDLED_HEADING.findall((output / ENTRY_BUNDLE).read_text()))
    for state in sorted(workflow.diagram.states - carried):
        faults.append(f"the {form} bundle carries no section for {state}")
    return faults


def section_faults(workflow: Workflow) -> list[str]:
    """How the prose form's sections differ from the diagram form's beyond
    their transition paragraphs."""
    faults = []
    states = workflow.diagram.states
    for form in FORMS:
        if set(workflow.sections[form]) != states:
            faults.append(f"the {form} form's states are not the diagram's")
    for state in sorted(states & set(workflow.sections[PROSE])):
        drawn = workflow.sections[DIAGRAM].get(state)
        written = workflow.sections[PROSE][state]
        if drawn is None:
            continue
        if drawn.path.name != written.path.name or drawn.body != written.body:
            faults.append(f"{state}: the prose section differs from the diagram's")
        if (drawn.transition is None) != (written.transition is None):
            faults.append(f"{state}: one form ends the workflow and the other does not")
        elif drawn.transition and written.transition:
            if drawn.transition.condition != written.transition.condition:
                faults.append(f"{state}: the forms decide on different conditions")
    if "```mermaid" in (workflow.form(PROSE) / ENTRY).read_text():
        faults.append("the prose form carries a diagram")
    return faults


def transition_faults(workflow: Workflow) -> list[str]:
    """How a section's transition or a click disagrees with the diagram."""
    diagram = workflow.diagram
    faults = []
    for state in sorted(diagram.states & set(workflow.sections[DIAGRAM])):
        leaving = diagram.leaving(state)
        labels = {edge.label for edge in leaving}
        drawn = workflow.sections[DIAGRAM][state].transition
        written = workflow.sections[PROSE].get(state)
        if drawn is None:
            if leaving or state not in diagram.terminals:
                faults.append(
                    f"{state}: the section ends a workflow the diagram does not"
                )
            continue
        if state in diagram.terminals:
            faults.append(
                f"{state}: the diagram ends at a state whose section does not"
            )
        if drawn.condition is None and labels != {None}:
            faults.append(f"{state}: no one unlabelled edge leaves it")
        if drawn.condition is not None and labels != {drawn.then, drawn.otherwise}:
            faults.append(f"{state}: its labels are not the edges leaving it")
        if written is not None and written.transition is not None:
            named = {written.transition.then, written.transition.otherwise} - {None}
            if named != {edge.target for edge in leaving}:
                faults.append(f"{state}: the prose names states the diagram does not")
    for node, destination in sorted(diagram.clicks.items()):
        if destination != document(node):
            faults.append(f"the click on {node} links {destination}, not its document")
    return faults


def scenario_faults(workflow: Workflow, scenario: Scenario) -> list[str]:
    """How a scenario's path fails to be the walk its inputs determine."""
    diagram = workflow.diagram
    path = scenario.path
    faults = []
    if not path or path[0] != diagram.start:
        faults.append(f"{scenario.name}: the path does not open at {diagram.start}")
    edges = {(edge.source, edge.target) for edge in diagram.edges}
    for step in zip(path, path[1:], strict=False):
        if step not in edges:
            faults.append(f"{scenario.name}: the diagram draws no edge {step}")
    if path and path[-1] not in diagram.terminals:
        faults.append(f"{scenario.name}: the path ends at {path[-1]}, not terminal")
    if set(scenario.inputs) != inputs_read(workflow, DIAGRAM):
        faults.append(f"{scenario.name}: its inputs are not the files decisions read")
        return faults
    for form in FORMS:
        walked = walk(workflow, form, scenario.inputs)
        if walked != path:
            faults.append(f"{scenario.name}: the {form} sections lead {walked}")
    return faults


def broken(tmp_path: Path, name: str, path: str, old: str, new: str) -> Workflow:
    """A copy of one workflow with one string of one file replaced."""
    copy = tmp_path / name
    shutil.copytree(WORKFLOWS / name, copy)
    target = copy / path
    text = target.read_text()
    assert old in text, f"{path} carries no {old!r} to break"
    target.write_text(text.replace(old, new, 1))
    return read_workflow(copy)


def test_the_corpus_holds_the_graded_workflows() -> None:
    assert [workflow.name for workflow in CORPUS] == ["branching", "linear", "looping"]


@pytest.mark.parametrize("form", FORMS)
@pytest.mark.parametrize("workflow", CORPUS, ids=lambda workflow: workflow.name)
def test_each_form_bundles_cleanly_carrying_every_state(
    workflow: Workflow, form: str, tmp_path: Path
) -> None:
    assert bundle_faults(workflow, form, tmp_path) == []


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


def test_every_decision_is_exercised_both_ways() -> None:
    for workflow in CORPUS:
        for state, section in workflow.sections[DIAGRAM].items():
            if section.transition is None or section.transition.condition is None:
                continue
            taken = {
                path[index + 1]
                for path in (scenario.path for scenario in workflow.scenarios)
                for index, step in enumerate(path[:-1])
                if step == state
            }
            leaving = {edge.target for edge in workflow.diagram.leaving(state)}
            assert taken == leaving, f"{workflow.name}: {state} is not taken both ways"


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
    assert "no-rework: the diagram draws no edge ('Draft', 'Publish')" in faults


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
    assert [fault.split(":")[0] for fault in faults] == ["low-severity"] * len(FORMS)
