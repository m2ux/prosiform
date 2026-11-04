"""Hold the scorer to its pass rule, its failure classes and its dispatch checks.

Each test lays out a workspace by hand: a trace, the action files a run
that did every action of the states it entered would leave, and for a
dispatch scenario the sub-agent record its transcript would produce. A
scenario's own path passes; each failure class is reached by one trace
built to depart from its scenario in that way and no other, and each
dispatch class by one record built to fail that check and no earlier one.
"""

import json
from pathlib import Path

import pytest
from harness import Claude, Opencode
from score import (
    ACTIONS,
    SUBAGENTS,
    TRACE,
    Failure,
    Start,
    Verdict,
    names,
    read_starts,
    read_trace,
    record_starts,
    score,
)
from workflow import Scenario, Workflow, workflows

CORPUS = {workflow.name: workflow for workflow in workflows()}


def scenario(workflow: str, name: str) -> Scenario:
    """One scenario of one workflow, by name."""
    return next(item for item in CORPUS[workflow].scenarios if item.name == name)


def starts_of(item: Scenario) -> list[Start]:
    """The sub-agent starts a correct run of one scenario makes.

    A scenario stating answers has each sub-agent ask, and the session start
    it again with the answers.
    """
    made: list[Start] = []
    for entry in item.trace:
        if item.answers:
            made.append(Start(entry.section, "question", entry.together))
            made.append(Start(entry.section, "done", False))
        else:
            made.append(Start(entry.section, "done", entry.together))
    return made


def record(held: Path, starts: list[Start]) -> Path:
    """Write a workspace's sub-agent record, as the runner writes it."""
    (held / SUBAGENTS).write_text(
        json.dumps({"starts": [start.record() for start in starts]}, indent=2) + "\n"
    )
    return held


def workspace(
    tmp_path: Path,
    workflow: Workflow,
    trace: list[str],
    log: str | None = None,
    starts: list[Start] | None = None,
) -> Path:
    """A workspace holding a trace, every action, and the sub-agent record.

    Every action is the path's states' and the sub-agents' the workflow's
    scenarios state.
    """
    if log is None:
        log = "".join(f"{state}\n" for state in trace)
    (tmp_path / TRACE).write_text(log)
    (tmp_path / ACTIONS).mkdir(exist_ok=True)
    for state in set(trace) & workflow.diagram.states:
        action = workflow.walked[state].action
        if action is None:
            continue
        name, value = action
        (tmp_path / ACTIONS / name).write_text(f"{value}\n")
    for item in workflow.scenarios:
        for entry in item.trace:
            if entry.action is not None:
                name, value = entry.action
                (tmp_path / ACTIONS / name).write_text(f"{value}\n")
    record(tmp_path, list(starts or []))
    return tmp_path


def run(tmp_path: Path, workflow: str, name: str, trace: list[str]) -> Verdict:
    """The verdict on a hand-made trace for one scenario."""
    held = CORPUS[workflow]
    item = scenario(workflow, name)
    return score(held, item, workspace(tmp_path, held, trace, starts=starts_of(item)))


@pytest.mark.parametrize(
    ("workflow", "item"),
    [(workflow, item) for workflow in CORPUS.values() for item in workflow.scenarios],
    ids=lambda item: item.name,
)
def test_a_run_walking_its_scenario_path_with_every_action_passes(
    tmp_path: Path, workflow: Workflow, item: Scenario
) -> None:
    """AC3: a dispatch scenario's own record passes beside its path."""
    held = workspace(tmp_path, workflow, list(item.path), starts=starts_of(item))
    assert score(workflow, item, held) == Verdict(
        True, None, None, item.path, item.path, ()
    )


@pytest.mark.parametrize(
    "workflow",
    [workflow for workflow in CORPUS if workflow.startswith("dispatch")],
)
def test_a_dispatch_scenario_passes_on_its_path_and_its_record(
    tmp_path: Path, workflow: str
) -> None:
    """AC3: every bundle a scenario names reached a sub-agent, in its order."""
    held = CORPUS[workflow]
    [item] = held.scenarios
    verdict = score(
        held, item, workspace(tmp_path, held, list(item.path), starts=starts_of(item))
    )
    assert (verdict.passed, verdict.failure, len(read_starts(tmp_path))) == (
        True,
        None,
        len(starts_of(item)),
    )


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
            ["Entry", "Plan", "Test", "Ship", "Exit"],
            Failure.SKIPPED_STATE,
            2,
        ),
        (
            "linear",
            "straight-through",
            ["Entry", "Plan", "Build", "Deploy", "Ship", "Exit"],
            Failure.INVENTED_STATE,
            3,
        ),
        (
            "linear",
            "straight-through",
            ["Entry", "Plan", "Build", "Plan"],
            Failure.INVALID_TRANSITION,
            3,
        ),
        (
            "looping",
            "two-rounds",
            ["Draft", "Review", "Revise", "Check", "Review", "Publish"],
            Failure.LOOP_MISCOUNT,
            5,
        ),
        (
            "linear",
            "straight-through",
            ["Entry", "Plan", "Build"],
            Failure.UNFINISHED,
            3,
        ),
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
        2,
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
    """The linked form's path is the one its rule documents name."""
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
        (
            "linear",
            "straight-through",
            ["Entry", "Plan", "Build", "Test", "Ship", "Exit", "Plan"],
            6,
        ),
        ("looping", "no-rework", ["Draft", "Review", "Publish", "Review"], 3),
        ("looping", "two-rounds", ["Draft", "Review", "Revise", "Check", "Draft"], 4),
        (
            "linear",
            "straight-through",
            ["Entry", "Plan", "Build", "Build", "Test", "Ship", "Exit"],
            3,
        ),
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
    log = "\n  Entry \nPlan\n\n\tBuild\nTest\nShip\nExit"
    held = workspace(
        tmp_path, linear, ["Entry", "Plan", "Build", "Test", "Ship", "Exit"], log
    )
    assert read_trace(held) == ("Entry", "Plan", "Build", "Test", "Ship", "Exit")
    assert score(linear, scenario("linear", "straight-through"), held).passed


def test_a_name_in_another_case_is_a_state_the_diagram_does_not_hold(
    tmp_path: Path,
) -> None:
    verdict = run(
        tmp_path, "linear", "straight-through", ["Entry", "Plan", "Build", "build"]
    )
    assert (verdict.failure, verdict.divergence) == (Failure.INVENTED_STATE, 3)


def test_the_record_is_plain_json_values(tmp_path: Path) -> None:
    verdict = run(tmp_path, "linear", "straight-through", ["Entry", "Plan", "Build"])
    assert json.loads(json.dumps(verdict.record())) == {
        "passed": False,
        "failure": "unfinished",
        "divergence": 3,
        "expected": ["Entry", "Plan", "Build", "Test", "Ship", "Exit"],
        "actual": ["Entry", "Plan", "Build"],
        "actions": [],
    }


def dispatched(workflow: str, starts: list[Start], tmp_path: Path) -> Verdict:
    """The verdict on a dispatch scenario's own path with a chosen record."""
    held = CORPUS[workflow]
    [item] = held.scenarios
    return score(held, item, workspace(tmp_path, held, list(item.path), starts=starts))


def test_a_bundle_that_reached_no_sub_agent_is_undispatched(
    tmp_path: Path,
) -> None:
    """AC3: a bundle set the agent read and did not dispatch is `undispatched`."""
    verdict = dispatched("dispatch-chain", [], tmp_path)
    assert (verdict.passed, verdict.failure) == (False, Failure.UNDISPATCHED)


def test_a_bundle_dispatched_after_another_is_undispatched(
    tmp_path: Path,
) -> None:
    """A record naming the sections in another order reached one out of turn."""
    [first, second] = CORPUS["dispatch-chain"].scenarios[0].trace
    verdict = dispatched(
        "dispatch-chain",
        [
            Start(second.section, "done", False),
            Start(first.section, "done", False),
        ],
        tmp_path,
    )
    assert verdict.failure == Failure.UNDISPATCHED


def test_a_native_parallel_set_keeps_its_response_group_across_child_events(
    tmp_path: Path,
) -> None:
    first, second = CORPUS["dispatch-set"].scenarios[0].trace
    verdict = dispatched(
        "dispatch-set",
        [
            Start(first.section, "done", False, "root", "response-1"),
            Start(
                "a child starts unrelated work",
                "done",
                False,
                "child",
                "child-response",
            ),
            Start(second.section, "done", True, "root", "response-1"),
        ],
        tmp_path,
    )
    assert verdict.passed


def test_native_starts_from_separate_responses_are_sequential(tmp_path: Path) -> None:
    first, second = CORPUS["dispatch-set"].scenarios[0].trace
    verdict = dispatched(
        "dispatch-set",
        [
            Start(first.section, "done", False, "root", "response-1"),
            Start(second.section, "done", True, "root", "response-2"),
        ],
        tmp_path,
    )
    assert verdict.failure == Failure.SEQUENTIAL_SET


def test_a_parent_ending_before_its_subagent_returns_is_unfinished(
    tmp_path: Path,
) -> None:
    first, second = CORPUS["dispatch-chain"].scenarios[0].trace
    verdict = dispatched(
        "dispatch-chain",
        [
            Start(first.section, "done", False),
            Start(second.section, "unfinished", False),
        ],
        tmp_path,
    )
    assert verdict.failure == Failure.UNFINISHED


def test_a_set_started_one_after_another_is_sequential_set(
    tmp_path: Path,
) -> None:
    """AC3: a set's bundles reached sub-agents, but not together."""
    [first, second] = CORPUS["dispatch-set"].scenarios[0].trace
    verdict = dispatched(
        "dispatch-set",
        [
            Start(first.section, "done", False),
            Start(second.section, "done", False),
        ],
        tmp_path,
    )
    assert (verdict.passed, verdict.failure) == (False, Failure.SEQUENTIAL_SET)


def test_a_set_split_across_two_messages_is_sequential_set(tmp_path: Path) -> None:
    """A set passes only where its opener starts first and the rest beside it.

    `together` says a start shares a message with the start above it, which
    may be one the scenario does not expect. Each record below holds one
    member opening no message, yet its set reached two messages.
    """
    [first, second] = CORPUS["dispatch-set"].scenarios[0].trace
    split = {
        "second message opened by another start": [
            Start(first.section, "done", False),
            Start("read the material", "done", False),
            Start(second.section, "done", True),
        ],
        "opener beside an earlier start": [
            Start("read the material", "done", False),
            Start(first.section, "done", True),
            Start(second.section, "done", False),
        ],
    }
    for name, starts in split.items():
        held = tmp_path / name.replace(" ", "-")
        held.mkdir()
        verdict = dispatched("dispatch-set", starts, held)
        assert (verdict.passed, verdict.failure) == (
            False,
            Failure.SEQUENTIAL_SET,
        ), name
    together = tmp_path / "together"
    together.mkdir()
    beside = [
        Start("read the material", "done", False),
        Start(first.section, "done", True),
        Start(second.section, "done", True),
    ]
    assert dispatched("dispatch-set", beside, together).passed


def test_a_question_answered_in_the_sub_agents_place_is_unrelayed(
    tmp_path: Path,
) -> None:
    """AC3: a returned question not started again takes `unrelayed_question`.

    The protocol has the session put a returned question to the user and
    start the sub-agent again with the answers; a session that went on
    answered it in the sub-agent's place or left it unanswered.
    """
    [entry] = CORPUS["dispatch-question"].scenarios[0].trace
    verdict = dispatched(
        "dispatch-question", [Start(entry.section, "question", False)], tmp_path
    )
    assert (verdict.passed, verdict.failure) == (False, Failure.UNRELAYED_QUESTION)


def test_a_start_returning_done_moves_the_session_on(tmp_path: Path) -> None:
    """A sub-agent that returned done is not started again, whatever it was asked."""
    [entry] = CORPUS["dispatch-question"].scenarios[0].trace
    verdict = dispatched(
        "dispatch-question", [Start(entry.section, "done", False)], tmp_path
    )
    assert verdict.passed is True


def test_a_sub_agent_that_wrote_no_action_is_missing_action(tmp_path: Path) -> None:
    """Each sub-agent's action is held as a state's is, named in the verdict."""
    held = CORPUS["dispatch-set"]
    [item] = held.scenarios
    workspace(tmp_path, held, list(item.path), starts=starts_of(item))
    (tmp_path / ACTIONS / "tests.txt").write_text("skimmed\n")
    verdict = score(held, item, tmp_path)
    assert (verdict.failure, verdict.divergence, verdict.actions) == (
        Failure.MISSING_ACTION,
        None,
        ("tests.txt",),
    )


def test_a_run_that_stopped_short_is_unfinished_though_nothing_was_dispatched(
    tmp_path: Path,
) -> None:
    """AC3: the completion check is read first, so a short run is `unfinished`."""
    held = CORPUS["dispatch-chain"]
    [item] = held.scenarios
    verdict = score(held, item, workspace(tmp_path, held, list(item.path[:-1])))
    assert (verdict.failure, verdict.divergence) == (Failure.UNFINISHED, 1)


def test_the_dispatch_checks_are_read_in_order(tmp_path: Path) -> None:
    """AC3: a record failing two checks takes the earlier one.

    A record that started too few sub-agents and gave the wrong return is
    `undispatched`, not `unrelayed_question`; one that ran a set in sequence
    and gave the wrong return is `sequential_set`, not the later check.
    """
    chain = CORPUS["dispatch-chain"].scenarios[0]
    corpus = CORPUS["dispatch-chain"]
    too_few = [Start(chain.trace[0].section, "question", False)]
    held = tmp_path / "few"
    held.mkdir()
    verdict = score(
        corpus, chain, workspace(held, corpus, list(chain.path), starts=too_few)
    )
    assert verdict.failure == Failure.UNDISPATCHED

    aset = CORPUS["dispatch-set"].scenarios[0]
    sequenced = [
        Start(aset.trace[0].section, "question", False),
        Start(aset.trace[1].section, "question", False),
    ]
    held = tmp_path / "sequence"
    held.mkdir()
    verdict = score(
        CORPUS["dispatch-set"],
        aset,
        workspace(held, CORPUS["dispatch-set"], list(aset.path), starts=sequenced),
    )
    assert verdict.failure == Failure.SEQUENTIAL_SET


def test_a_scenario_dispatching_nothing_passes_the_dispatch_checks(
    tmp_path: Path,
) -> None:
    """A workflow dispatching nothing states no trace, so all three checks pass."""
    linear = CORPUS["linear"]
    item = scenario("linear", "straight-through")
    held = workspace(tmp_path, linear, list(item.path))
    assert item.trace == ()
    assert score(linear, item, held).passed


def transcript(tmp_path: Path, messages: list[dict[str, object]]) -> Path:
    """A transcript holding the messages given, one per line."""
    path = tmp_path / "transcript.jsonl"
    path.write_text("\n".join(json.dumps(message) for message in messages) + "\n")
    return path


def call(identifier: str, target: str) -> dict[str, object]:
    """One `Agent` call naming the section it hands over."""
    return {
        "type": "tool_use",
        "id": identifier,
        "name": "Agent",
        "input": {"description": "Follow the workflow", "prompt": target},
    }


def answer(identifier: str, text: str) -> dict[str, object]:
    """One `tool_result` answering a call."""
    return {
        "type": "tool_result",
        "tool_use_id": identifier,
        "content": text,
    }


def test_a_start_is_read_from_the_transcript_with_its_position_and_return(
    tmp_path: Path,
) -> None:
    """A start reads its section, its return, and whether it came with another."""
    held = transcript(
        tmp_path,
        [
            {"type": "assistant", "message": {"content": [call("a", "plan#work")]}},
            {
                "type": "assistant",
                "message": {
                    "content": [call("b", "review#source"), call("c", "review#tests")]
                },
            },
            {"type": "user", "message": {"content": [answer("a", "done: complete")]}},
            {
                "type": "user",
                "message": {"content": [answer("b", "Question: which source?")]},
            },
            {"type": "user", "message": {"content": [answer("c", "done: read")]}},
        ],
    )
    records = tmp_path / "records"
    records.mkdir()
    record_starts(held, records, Claude())
    assert read_starts(records) == (
        Start("plan#work", "done", False),
        Start("review#source", "question", False),
        Start("review#tests", "done", True),
    )
    assert Claude().starts(held) == (
        Start("plan#work", "done", False),
        Start("review#source", "question", False),
        Start("review#tests", "done", True),
    )


def test_a_start_names_its_file_or_authored_section_exactly() -> None:
    """Prompt filenames and authored references identify dispatch targets."""
    assert names("Dispatch plan__work.bundle.md", "plan#work") is True
    assert names("Follow /work/plan__work.bundle.md.", "plan#work") is True
    assert names("Follow plan.md#work.", "plan#work") is True
    assert names("Follow plan#work.", "plan#work") is True
    assert names("Follow Plan Work section", "plan#work") is False
    assert names("Dispatch plan work bundle", "plan#work") is False
    assert names("Follow review__work.bundle.md", "plan#work") is False
    assert names("Follow otherplan__work.bundle.md", "plan#work") is False
    assert names("Follow plan__work.bundle.md-copy", "plan#work") is False
    assert names("Follow plan__work.bundle.md.backup", "plan#work") is False
    assert names("Follow the Review section", "plan#work") is False


def test_a_start_naming_its_compiled_bundle_names_the_same_section(
    tmp_path: Path,
) -> None:
    """A compiled form's call names `pf`'s bundle, which spells one section."""
    verdict = dispatched(
        "dispatch-chain",
        [
            Start("plan__work.bundle.md", "done", False),
            Start("review__check.bundle.md", "done", False),
        ],
        tmp_path,
    )
    assert verdict.passed is True


def test_an_absent_transcript_records_no_start(tmp_path: Path) -> None:
    """A session that dispatched nothing, or wrote no transcript, records none."""
    records = tmp_path / "records"
    records.mkdir()
    assert record_starts(tmp_path / "absent.jsonl", records, Claude()) == ()
    assert read_starts(records) == ()
    assert read_starts(tmp_path / "unwritten") == ()


def opencode_task(call: str, message: str, target: str, text: str) -> dict[str, object]:
    """One completed opencode `task` part, its output wrapped as the CLI wraps it."""
    return {
        "type": "tool_use",
        "part": {
            "type": "tool",
            "callID": call,
            "messageID": message,
            "tool": "task",
            "state": {
                "status": "completed",
                "input": {"description": "Follow the workflow", "prompt": target},
                "output": "\n".join(
                    [
                        f'<task id="ses_{call}" state="completed">',
                        "<task_result>",
                        text,
                        "</task_result>",
                        "</task>",
                    ]
                ),
            },
        },
    }


def test_an_opencode_question_left_unanswered_scores_as_a_question(
    tmp_path: Path,
) -> None:
    """AC17: a sub-agent's returned question reads as one when the run is scored.

    The session relayed the question rather than answering it, so its first
    start returns `question`, the second starts it again with the answers,
    and the cell passes.
    """
    corpus = CORPUS["dispatch-question"]
    [item] = corpus.scenarios
    [entry] = item.trace
    held = transcript(
        tmp_path,
        [
            opencode_task("a", "m1", entry.section, "question: which option?"),
            opencode_task("b", "m2", entry.section, "done: chose the first"),
        ],
    )
    records = tmp_path / "records"
    records.mkdir()
    workspace(records, corpus, list(item.path))
    record_starts(held, records, Opencode())
    assert [start.returned for start in read_starts(records)] == [
        "question",
        "done",
    ]
    verdict = score(corpus, item, records)
    assert (verdict.passed, verdict.failure) == (True, None)
