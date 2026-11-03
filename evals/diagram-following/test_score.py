"""Hold the scorer to its pass rule, its failure classes and its dispatch checks.

Each test lays out a workspace by hand: a trace, the action files a run
that did every action of the states it entered would leave, and for a
dispatch scenario the sub-agent record its transcript would produce. A
scenario's own path passes; each failure class is reached by one trace
built to depart from its scenario in that way and no other, and each
dispatch class by one record built to fail that check and no earlier one.
"""

import json
from dataclasses import replace
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
    pf_runs,
    read_starts,
    read_trace,
    record_calls,
    score,
)
from workflow import Compile, Scenario, Workflow, workflows

CORPUS = {workflow.name: workflow for workflow in workflows()}


def scenario(workflow: str, name: str) -> Scenario:
    """One scenario of one workflow, by name."""
    return next(item for item in CORPUS[workflow].scenarios if item.name == name)


def starts_of(item: Scenario) -> list[Start]:
    """The sub-agent starts a correct run of one scenario makes."""
    return [
        Start(entry.section, entry.returned, entry.together) for entry in item.trace
    ]


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
    """A workspace holding a trace, every action, and the sub-agent record."""
    if log is None:
        log = "".join(f"{state}\n" for state in trace)
    (tmp_path / TRACE).write_text(log)
    (tmp_path / ACTIONS).mkdir(exist_ok=True)
    for state in set(trace) & workflow.diagram.states:
        name, value = workflow.walked[state].action
        (tmp_path / ACTIONS / name).write_text(f"{value}\n")
    record(tmp_path, list(starts or []))
    return tmp_path


def done_by_sub_agents(held: Path, item: Scenario) -> Path:
    """Write the actions a scenario states its sub-agents do, as they would."""
    for entry in item.trace:
        for name, value in entry.actions:
            (held / ACTIONS / name).write_text(f"{value}\n")
    return held


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
    done_by_sub_agents(held, item)
    assert score(workflow, item, held) == Verdict(
        True, None, None, item.path, item.path, ()
    )


@pytest.mark.parametrize(
    ("workflow", "name"),
    [
        (workflow, item.name)
        for workflow in CORPUS
        if workflow.startswith("dispatch")
        for item in CORPUS[workflow].scenarios
    ],
)
def test_a_dispatch_scenario_passes_on_its_path_and_its_record(
    tmp_path: Path, workflow: str, name: str
) -> None:
    """AC3: every bundle a scenario names reached a sub-agent, in its order."""
    held = CORPUS[workflow]
    item = scenario(workflow, name)
    verdict = score(
        held, item, workspace(tmp_path, held, list(item.path), starts=starts_of(item))
    )
    assert (verdict.passed, verdict.failure, len(read_starts(tmp_path))) == (
        True,
        None,
        len(item.trace),
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
            Start(second.section, second.returned, False),
            Start(first.section, first.returned, False),
        ],
        tmp_path,
    )
    assert verdict.failure == Failure.UNDISPATCHED


def test_a_set_started_one_after_another_is_sequential_set(
    tmp_path: Path,
) -> None:
    """AC3: a set's bundles reached sub-agents, but not together."""
    [first, second] = CORPUS["dispatch-set"].scenarios[0].trace
    verdict = dispatched(
        "dispatch-set",
        [
            Start(first.section, first.returned, False),
            Start(second.section, second.returned, False),
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
            Start(first.section, first.returned, False),
            Start("read the material", "done", False),
            Start(second.section, second.returned, True),
        ],
        "opener beside an earlier start": [
            Start("read the material", "done", False),
            Start(first.section, first.returned, True),
            Start(second.section, second.returned, False),
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
        Start(first.section, first.returned, True),
        Start(second.section, second.returned, True),
    ]
    assert dispatched("dispatch-set", beside, together).passed


def test_a_question_answered_in_the_sub_agents_place_is_unrelayed(
    tmp_path: Path,
) -> None:
    """AC3: a returned question the session answered takes `unrelayed_question`."""
    [first, second] = CORPUS["dispatch-question"].scenarios[0].trace
    assert first.returned != second.returned
    verdict = dispatched(
        "dispatch-question",
        [
            Start(first.section, second.returned, False),
            Start(second.section, second.returned, False),
        ],
        tmp_path,
    )
    assert (verdict.passed, verdict.failure) == (False, Failure.UNRELAYED_QUESTION)


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
    """One `Task` call naming the section it hands over."""
    return {
        "type": "tool_use",
        "id": identifier,
        "name": "Task",
        "input": {"description": target, "prompt": f"Follow {target}."},
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
                "message": {"content": [answer("b", "question: which source?")]},
            },
            {"type": "user", "message": {"content": [answer("c", "done: read")]}},
        ],
    )
    records = tmp_path / "records"
    records.mkdir()
    record_calls(held, records, Claude())
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


def test_a_start_naming_a_section_by_its_heading_is_that_section() -> None:
    """A session writes its own wording, so the heading alone names the section."""
    assert names("Follow Plan Work section", "plan#work") is True
    assert names("Dispatch plan work bundle", "plan#work") is True
    assert names("Dispatch plan__work.bundle.md", "plan#work") is True
    assert names("Follow the Review section", "plan#work") is False


def test_a_bundle_of_a_document_in_a_folder_names_its_section() -> None:
    """`pf` writes each `/` of a dispatched document's path as `_` in its bundle."""
    assert names("Dispatch ask_enquiry__pose.bundle.md", "ask/enquiry#pose") is True
    assert names("Dispatch ask_probe__probe.bundle.md", "ask/enquiry#pose") is False


@pytest.mark.parametrize(
    ("name", "undone"),
    [
        ("first-hop-run", ("closing.txt",)),
        ("deep-hop-runs", ("weighing.txt", "ruling.txt")),
    ],
)
def test_a_sub_agent_running_no_pf_on_its_line_misses_its_action(
    tmp_path: Path, name: str, undone: tuple[str, ...]
) -> None:
    """AC17, AC18: only the line's compiled material states the sub-agent's action.

    Each start is recorded, and the session's path and its states' actions are
    done, so a sub-agent that ran no `pf` on its line leaves only the action
    that material states undone, which no harness's stream need carry.
    """
    held = CORPUS["subagent-first-run"]
    item = scenario("subagent-first-run", name)
    workspace(tmp_path, held, list(item.path), starts=starts_of(item))
    verdict = score(held, item, tmp_path)
    assert verdict == Verdict(
        False, Failure.MISSING_ACTION, None, item.path, item.path, undone
    )
    done_by_sub_agents(tmp_path, item)
    assert score(held, item, tmp_path).passed is True


def test_a_sub_agent_never_started_is_undispatched_before_its_action(
    tmp_path: Path,
) -> None:
    """AC18: the dispatch checks read first, so an unstarted hop is `undispatched`."""
    held = CORPUS["subagent-first-run"]
    item = scenario("subagent-first-run", "deep-hop-runs")
    workspace(tmp_path, held, list(item.path), starts=starts_of(item)[:2])
    assert score(held, item, tmp_path).failure == Failure.UNDISPATCHED


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
    assert record_calls(tmp_path / "absent.jsonl", records, Claude()) == ()
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
                "input": {"description": target, "prompt": f"Follow {target}."},
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
    start returns `question` and the cell passes; read as `done`, the same
    transcript would score as `unrelayed_question`.
    """
    corpus = CORPUS["dispatch-question"]
    [item] = corpus.scenarios
    [first, second] = item.trace
    held = transcript(
        tmp_path,
        [
            opencode_task("a", "m1", first.section, "question: which option?"),
            opencode_task("b", "m2", second.section, "done: chose the first"),
        ],
    )
    records = tmp_path / "records"
    records.mkdir()
    workspace(records, corpus, list(item.path))
    record_calls(held, records, Opencode())
    assert [start.returned for start in read_starts(records)] == [
        "question",
        "done",
    ]
    verdict = score(corpus, item, records)
    assert (verdict.passed, verdict.failure) == (True, None)


STAGED_RUNS = (
    Compile(None, ()),
    Compile(None, ("fetch.md#implementation",)),
    Compile("review#tests", ()),
    Compile("review#tests", ("net.md#retry",)),
)
"""Runs a staged scenario states: the session's two, then a sub-agent's two."""


def compiling(
    tmp_path: Path,
    session: list[str] | None,
    sub_agent: list[str],
    runs: tuple[Compile, ...] = STAGED_RUNS,
) -> Verdict:
    """The verdict on a correct walk of `dispatch-set` whose record holds commands.

    The scenario states `runs`; the session ran `session`, null where its
    harness reports no command, and the sub-agent following `review#tests` ran
    `sub_agent`.
    """
    workflow = CORPUS["dispatch-set"]
    item = replace(scenario("dispatch-set", "parallel-set"), compile=runs)
    held = workspace(tmp_path, workflow, list(item.path))
    starts = [
        replace(start, commands=tuple(sub_agent))
        if start.target == "review#tests"
        else start
        for start in starts_of(item)
    ]
    (held / SUBAGENTS).write_text(
        json.dumps(
            {"commands": session, "starts": [start.record() for start in starts]}
        )
    )
    return score(workflow, item, held)


CORRECT_SESSION = ["pf", "./bin/pf -o out fetch.md#implementation"]
CORRECT_SUB_AGENT = ["pf && pf -o out 'net.md#retry'"]


def test_a_session_making_its_stated_runs_passes(tmp_path: Path) -> None:
    """AC4: the stated runs, each by its agent and in order, pass."""
    verdict = compiling(tmp_path, CORRECT_SESSION, CORRECT_SUB_AGENT)
    assert (verdict.passed, verdict.failure) == (True, None)


@pytest.mark.parametrize(
    ("session", "sub_agent", "failure"),
    [
        (["pf"], CORRECT_SUB_AGENT, Failure.UNCOMPILED),
        (CORRECT_SESSION, ["pf"], Failure.UNCOMPILED),
        (
            [*CORRECT_SESSION, "pf -o out net.md#retry"],
            CORRECT_SUB_AGENT,
            Failure.OVERCOMPILED,
        ),
        (
            CORRECT_SESSION,
            [*CORRECT_SUB_AGENT, "cd . ; pf fetch.md#implementation"],
            Failure.OVERCOMPILED,
        ),
        (
            list(reversed(CORRECT_SESSION)),
            CORRECT_SUB_AGENT,
            Failure.MISORDERED_COMPILE,
        ),
        (CORRECT_SESSION, ["pf net.md#retry", "pf"], Failure.MISORDERED_COMPILE),
        (["pf other.md"], ["pf"], Failure.UNCOMPILED),
    ],
    ids=[
        "session-omits",
        "sub-agent-omits",
        "session-adds",
        "sub-agent-adds",
        "session-reorders",
        "sub-agent-reorders",
        "omission-before-addition",
    ],
)
def test_a_session_departing_from_its_stated_runs_fails_with_its_class(
    tmp_path: Path, session: list[str], sub_agent: list[str], failure: Failure
) -> None:
    """AC4: a run omitted, added or out of order fails the walk that passed."""
    verdict = compiling(tmp_path, session, sub_agent)
    assert (verdict.passed, verdict.failure, verdict.divergence) == (
        False,
        failure,
        None,
    )


def test_a_run_on_a_line_no_scenario_states_is_overcompiled(tmp_path: Path) -> None:
    """AC4: a scenario stating no run fails a session compiling a deferred line."""
    verdict = compiling(tmp_path, ["pf -o out net.md#retry"], [], runs=())
    assert verdict.failure == Failure.OVERCOMPILED


def test_a_bare_pf_beyond_those_stated_is_no_departure(tmp_path: Path) -> None:
    """A bare `pf` prints the guide and compiles nothing, so it adds no run."""
    verdict = compiling(tmp_path, ["pf", *CORRECT_SESSION], CORRECT_SUB_AGENT)
    assert verdict.passed is True


def test_a_run_from_another_directory_names_the_same_document(tmp_path: Path) -> None:
    """A reference ending in the stated one names it, wherever `pf` ran from."""
    runs = (Compile(None, ("sources/workflow.md",)),)
    named = [
        ".claude/skills/audit/bin/pf -o build"
        " ./.claude/skills/audit/sources/workflow.md"
    ]
    assert compiling(tmp_path, named, [], runs=runs).passed is True
    assert compiling(tmp_path, ["pf other/workflow.md"], [], runs=runs).failure == (
        Failure.UNCOMPILED
    )


def test_a_harness_reporting_no_command_asks_no_run(tmp_path: Path) -> None:
    """A record naming no commands holds the session to none of its runs."""
    assert compiling(tmp_path, None, []).passed is True


def test_the_run_checks_follow_the_dispatch_checks(tmp_path: Path) -> None:
    """A record failing a dispatch check takes it, whatever its runs."""
    workflow = CORPUS["dispatch-set"]
    item = replace(scenario("dispatch-set", "parallel-set"), compile=STAGED_RUNS)
    held = workspace(tmp_path, workflow, list(item.path))
    (held / SUBAGENTS).write_text(json.dumps({"commands": [], "starts": []}))
    assert score(workflow, item, held).failure == Failure.UNDISPATCHED


def test_each_command_splits_into_the_pf_runs_it_makes() -> None:
    """A run is a segment opening with `pf`, its references stripped of options."""
    assert pf_runs(
        (
            "pf",
            "cd build && ../bin/pf -o out -d json --budget files=9 a.md#b | cat",
            "echo pf; ls; pfx a.md || pf -c 'c d.md'",
        )
    ) == [(), ("a.md#b",), ("c d.md",)]
