"""Hold the scorer to its pass rule and its failure classes.

Each test lays out a workspace by hand: a trace, and the action files a run
that did every action of the states it entered would leave. A scenario's
own path passes; each failure class is reached by one trace built to
depart from its scenario in that way and no other.
"""

import json
from pathlib import Path

import pytest
from score import TRACE, Failure, Verdict, read_trace, score
from workflow import DIAGRAM, Scenario, Workflow, workflows

CORPUS = {workflow.name: workflow for workflow in workflows()}


def scenario(workflow: str, name: str) -> Scenario:
    """One scenario of one workflow, by name."""
    return next(item for item in CORPUS[workflow].scenarios if item.name == name)


def workspace(
    tmp_path: Path, workflow: Workflow, trace: list[str], log: str | None = None
) -> Path:
    """A workspace holding a trace and every action of the states it names."""
    if log is None:
        log = "".join(f"{state}\n" for state in trace)
    (tmp_path / TRACE).write_text(log)
    (tmp_path / "actions").mkdir()
    for state in set(trace) & workflow.diagram.states:
        name, value = workflow.sections[DIAGRAM][state].action
        (tmp_path / "actions" / name).write_text(f"{value}\n")
    return tmp_path


def run(tmp_path: Path, workflow: str, name: str, trace: list[str]) -> Verdict:
    """The verdict on a hand-made trace for one scenario."""
    held = CORPUS[workflow]
    return score(held, scenario(workflow, name), workspace(tmp_path, held, trace))


@pytest.mark.parametrize(
    ("workflow", "item"),
    [(workflow, item) for workflow in CORPUS.values() for item in workflow.scenarios],
    ids=lambda item: item.name,
)
def test_a_run_walking_its_scenario_path_with_every_action_passes(
    tmp_path: Path, workflow: Workflow, item: Scenario
) -> None:
    verdict = score(workflow, item, workspace(tmp_path, workflow, list(item.path)))
    assert verdict == Verdict(True, None, None, item.path, item.path, ())


@pytest.mark.parametrize(
    ("workflow", "name", "trace", "failure", "divergence"),
    [
        (
            "branching",
            "high-severity",
            ["Intake", "Triage", "Queue", "Resolve"],
            Failure.WRONG_BRANCH,
            2,
        ),
        (
            "linear",
            "straight-through",
            ["Plan", "Test", "Ship"],
            Failure.SKIPPED_STATE,
            1,
        ),
        (
            "linear",
            "straight-through",
            ["Plan", "Build", "Deploy", "Ship"],
            Failure.INVENTED_STATE,
            2,
        ),
        (
            "linear",
            "straight-through",
            ["Plan", "Build", "Plan"],
            Failure.INVALID_TRANSITION,
            2,
        ),
        (
            "looping",
            "two-rounds",
            ["Draft", "Review", "Revise", "Check", "Review", "Publish"],
            Failure.LOOP_MISCOUNT,
            5,
        ),
        ("linear", "straight-through", ["Plan", "Build"], Failure.UNFINISHED, 2),
    ],
    ids=[
        "wrong-branch",
        "skipped-state",
        "invented-state",
        "invalid-transition",
        "loop-miscount",
        "unfinished",
    ],
)
def test_a_trace_departing_from_its_path_is_classified_at_the_first_divergence(
    tmp_path: Path,
    workflow: str,
    name: str,
    trace: list[str],
    failure: Failure,
    divergence: int,
) -> None:
    verdict = run(tmp_path, workflow, name, trace)
    assert (verdict.passed, verdict.failure, verdict.divergence) == (
        False,
        failure,
        divergence,
    )
    assert verdict.actual == tuple(trace)
    assert verdict.actions == ()


def test_a_right_path_with_an_action_absent_or_wrong_is_a_missing_action(
    tmp_path: Path,
) -> None:
    linear = CORPUS["linear"]
    item = scenario("linear", "straight-through")
    held = workspace(tmp_path, linear, list(item.path))
    (held / "actions" / "build.txt").unlink()
    (held / "actions" / "ship.txt").write_text("shipped later\n")
    verdict = score(linear, item, held)
    assert (verdict.failure, verdict.divergence, verdict.actions) == (
        Failure.MISSING_ACTION,
        1,
        ("build.txt", "ship.txt"),
    )


def test_a_loop_taken_once_more_than_its_input_requires_is_a_loop_miscount(
    tmp_path: Path,
) -> None:
    verdict = run(
        tmp_path,
        "looping",
        "no-rework",
        ["Draft", "Review", "Revise", "Check", "Review", "Publish"],
    )
    assert (verdict.failure, verdict.divergence) == (Failure.LOOP_MISCOUNT, 2)


def test_an_empty_or_absent_trace_is_unfinished(tmp_path: Path) -> None:
    linear = CORPUS["linear"]
    item = scenario("linear", "straight-through")
    assert score(linear, item, tmp_path).failure == Failure.UNFINISHED
    verdict = score(linear, item, workspace(tmp_path, linear, []))
    assert (verdict.failure, verdict.divergence) == (Failure.UNFINISHED, 0)


def test_a_linked_decision_passes_on_the_path_its_rules_state(
    tmp_path: Path,
) -> None:
    """The linked form's path is the one its rule documents label."""
    branching = CORPUS["branching"]
    high = scenario("branching", "high-severity")
    low = scenario("branching", "low-severity")
    for item, held in ((high, tmp_path / "high"), (low, tmp_path / "low")):
        held.mkdir()
        verdict = score(branching, item, workspace(held, branching, list(item.path)))
        assert (verdict.passed, verdict.actual) == (True, item.path)


@pytest.mark.parametrize(
    ("workflow", "name", "trace", "divergence"),
    [
        ("linear", "straight-through", ["Plan", "Build", "Test", "Ship", "Plan"], 4),
        ("looping", "no-rework", ["Draft", "Review", "Publish", "Review"], 3),
        ("looping", "two-rounds", ["Draft", "Review", "Revise", "Check", "Draft"], 4),
        ("linear", "straight-through", ["Plan", "Build", "Build", "Test", "Ship"], 2),
        ("looping", "no-rework", ["Draft", "Review", "Review", "Publish"], 2),
    ],
    ids=[
        "past-the-terminal",
        "past-the-terminal-on-a-cycle",
        "step-back",
        "repeat",
        "repeat-on-a-cycle",
    ],
)
def test_a_diagram_state_no_edge_leads_to_is_an_invalid_transition(
    tmp_path: Path, workflow: str, name: str, trace: list[str], divergence: int
) -> None:
    verdict = run(tmp_path, workflow, name, trace)
    assert (verdict.failure, verdict.divergence) == (
        Failure.INVALID_TRANSITION,
        divergence,
    )


def test_a_state_further_along_a_cycle_with_one_omitted_is_skipped(
    tmp_path: Path,
) -> None:
    verdict = run(
        tmp_path, "looping", "two-rounds", ["Draft", "Review", "Check", "Review"]
    )
    assert (verdict.failure, verdict.divergence) == (Failure.SKIPPED_STATE, 2)


def test_a_trace_is_read_stripped_of_blank_lines_and_surrounding_whitespace(
    tmp_path: Path,
) -> None:
    linear = CORPUS["linear"]
    log = "\n  Plan \nBuild\n\n\tTest\nShip"
    held = workspace(tmp_path, linear, ["Plan", "Build", "Test", "Ship"], log)
    assert read_trace(held) == ("Plan", "Build", "Test", "Ship")
    assert score(linear, scenario("linear", "straight-through"), held).passed


def test_a_name_in_another_case_is_a_state_the_diagram_does_not_hold(
    tmp_path: Path,
) -> None:
    verdict = run(tmp_path, "linear", "straight-through", ["Plan", "build"])
    assert (verdict.failure, verdict.divergence) == (Failure.INVENTED_STATE, 1)


def test_the_record_is_plain_json_values(tmp_path: Path) -> None:
    verdict = run(tmp_path, "linear", "straight-through", ["Plan", "Build"])
    assert json.loads(json.dumps(verdict.record())) == {
        "passed": False,
        "failure": "unfinished",
        "divergence": 2,
        "expected": ["Plan", "Build", "Test", "Ship"],
        "actual": ["Plan", "Build"],
        "actions": [],
    }
