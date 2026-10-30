"""Score one finished run of the diagram-following eval against its scenario.

A run leaves a workspace holding `trace.log`, one line per state the agent
entered, and `actions/`, the files the states' actions write. The trace is
the log's lines with surrounding whitespace removed and blank lines dropped;
a name is otherwise read exactly, so one differing in case or punctuation is
a name the diagram does not hold, and a workspace with no `trace.log` holds
an empty trace. An action is done when its file exists and holds the value
its section states, surrounding whitespace removed.

A run passes when its trace is the scenario's path and every state on it
has done its action. A session whose agent reported an error, or printed
no `result` message, is *errored*: it entered no state, so its trace is no
evidence of how it followed the workflow. A failing run is otherwise
classified from the first index at which its trace and the path differ,
the classes taken in this order:

- the trace is the path, and a state on it has not done its action:
  *missing action*;
- the trace is a proper prefix of the path, the empty trace included:
  *unfinished*;
- the state entered there, against the one before it (the `start` marker
  at the first index), is a name the diagram does not hold:
  *invented state*;
- it is a state an edge leads to from a decision on how often `trace.log`
  holds a line, the loop's decision: *loop miscount*;
- it is a state an edge leads to from any other decision: *wrong branch*;
- it is another state a walk of two or more edges reaches, entered with
  the states between omitted: *skipped state*;
- it is any other state the diagram holds, which no edge leads to from the
  one before it: a step back, a state entered after a terminal one, or the
  one before it repeated: *invalid transition*.

A dispatch scenario also states the sub-agents a correct run starts, so a
run whose trace is the path and whose actions are done is held to that
record before it passes. The record is `subagents.json` beside the trace,
written from the session's transcript when the session settles, so the
scorer reads no transcript and takes no second read:

- the sections the record names, in order, are the scenario's: otherwise
  *undispatched*, since a bundle the scenario dispatches reached no
  sub-agent or reached one in another order;
- every start the scenario marks as opening a set beside the one above it
  is recorded beside it: otherwise *sequential_set*;
- each start's return is the scenario's: otherwise *unrelayed_question*,
  which is a question the sub-agent returned and the session answered in
  its place.

The checks are read in that order, after the run is held to its path and
its actions, so a trace that stopped short is *unfinished* however few
sub-agents it started, and a record failing two checks takes the earlier.
A scenario that dispatches nothing passes all three, and a record absent
from a session that dispatches nothing names no start.

A start is a `Task` tool call in the transcript, which names the section
it hands over in the call's `description` as `<document>#<heading>`; its
return is the text of the answer to that call, read as `question` when
that text opens with the word and as `done` otherwise. Two starts in one
message are together, since they were dispatched at once. Which message
and answer a harness's stream records that in is the harness's to read, as
`harness.py` states: the scorer reads only the record either harness writes.

The verdict's `record` is the form the runner writes and the report reads.
"""

import json
import re
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path

from harness import Claude, Cursor, Start

__all__ = [
    "ACTIONS",
    "SUBAGENTS",
    "TRACE",
    "Failure",
    "Start",
    "Verdict",
    "read_starts",
    "read_trace",
    "record_starts",
    "score",
]
from workflow import FEWER, START, Scenario, Workflow

TRACE = "trace.log"
ACTIONS = "actions"
SUBAGENTS = "subagents.json"
TRANSCRIPT = "transcript.jsonl"
BUNDLE_SUFFIX = ".bundle.md"
BUNDLE_JOIN = "__"


class Failure(StrEnum):
    """How a failing run departed from its scenario."""

    WRONG_BRANCH = "wrong_branch"
    SKIPPED_STATE = "skipped_state"
    INVENTED_STATE = "invented_state"
    INVALID_TRANSITION = "invalid_transition"
    LOOP_MISCOUNT = "loop_miscount"
    MISSING_ACTION = "missing_action"
    UNFINISHED = "unfinished"
    UNDISPATCHED = "undispatched"
    SEQUENTIAL_SET = "sequential_set"
    UNRELAYED_QUESTION = "unrelayed_question"
    ERRORED = "errored"


@dataclass(frozen=True)
class Verdict:
    """One run's score.

    `divergence` is the first index at which the trace and the expected path
    differ; for a missing action, the first index whose state has not done
    its action; for an unfinished run, the trace's length. A pass carries no
    failure and no divergence. `actions` names the action files absent or
    wrong among the diagram states the trace entered, in trace order.
    """

    passed: bool
    failure: Failure | None
    divergence: int | None
    expected: tuple[str, ...]
    actual: tuple[str, ...]
    actions: tuple[str, ...]

    def record(self) -> dict[str, object]:
        """The verdict as plain values `json.dumps` writes unchanged."""
        record = asdict(self)
        record["failure"] = None if self.failure is None else str(self.failure)
        record["expected"] = list(self.expected)
        record["actual"] = list(self.actual)
        record["actions"] = list(self.actions)
        return record


def read_trace(workspace: Path) -> tuple[str, ...]:
    """The state names a workspace's `trace.log` holds, in order."""
    log = workspace / TRACE
    if not log.is_file():
        return ()
    lines = (line.strip() for line in log.read_text().splitlines())
    return tuple(line for line in lines if line)


def action_done(workflow: Workflow, state: str, workspace: Path) -> bool:
    """Whether a state's action file exists and holds the stated value."""
    name, value = workflow.walked[state].action
    written = workspace / ACTIONS / name
    return written.is_file() and written.read_text().strip() == value


def undone(workflow: Workflow, trace: tuple[str, ...], workspace: Path) -> list[int]:
    """The trace indices of diagram states whose action is not done."""
    states = workflow.diagram.states
    return [
        index
        for index, state in enumerate(trace)
        if state in states and not action_done(workflow, state, workspace)
    ]


def reachable(workflow: Workflow, source: str) -> set[str]:
    """Every state a walk of one or more edges reaches from a state."""
    reached: set[str] = set()
    frontier = [source]
    while frontier:
        for edge in workflow.diagram.leaving(frontier.pop()):
            if edge.target not in reached:
                reached.add(edge.target)
                frontier.append(edge.target)
    return reached


def departure(workflow: Workflow, previous: str, entered: str) -> Failure:
    """How entering a state other than the expected one departs from the walk."""
    if entered not in workflow.diagram.states:
        return Failure.INVENTED_STATE
    if entered in {edge.target for edge in workflow.diagram.leaving(previous)}:
        transition = workflow.walked[previous].transition
        condition = transition.condition if transition else None
        if condition is not None and FEWER.match(condition):
            return Failure.LOOP_MISCOUNT
        return Failure.WRONG_BRANCH
    if entered != previous and entered in reachable(workflow, previous):
        return Failure.SKIPPED_STATE
    return Failure.INVALID_TRANSITION


def record_starts(
    transcript: Path, records: Path, harness: Claude | Cursor
) -> tuple[Start, ...]:
    """Read a session's transcript for its sub-agent starts and record them.

    The record is `subagents.json` beside the trace and the session's tokens,
    one entry per start in the order the transcript made them, so the scorer
    reads it instead of the transcript. The harness reads its own stream, so
    one record shape serves every agent CLI.
    """
    starts = harness.starts(transcript)
    (records / SUBAGENTS).write_text(
        json.dumps({"starts": [start.record() for start in starts]}, indent=2) + "\n"
    )
    return starts


def read_starts(workspace: Path) -> tuple[Start, ...]:
    """The sub-agent starts a workspace's record holds, in order.

    The record is read as the runner wrote it, so the scorer takes no second
    read of the transcript, and a workspace with no record names no start.
    """
    path = workspace / SUBAGENTS
    if not path.is_file():
        return ()
    try:
        held = json.loads(path.read_text())
    except json.JSONDecodeError:
        return ()
    if not isinstance(held, dict):
        return ()
    return tuple(
        Start(
            str(row.get("target", "")),
            str(row.get("returned", "")),
            bool(row.get("together")),
        )
        for row in held.get("starts", [])
        if isinstance(row, dict)
    )


def names(target: str, section: str) -> bool:
    """Whether a start's target names a section, as a section or as its bundle.

    A compiled form hands over `pf`'s bundle for the section, named
    `<document>__<heading>` and written beside the entry; an authored form
    hands over the section itself, named `<document>#<heading>`. Both spell
    one section, since the bundle's name is compiled from it. A start's
    target is the text the dispatching call carried, so the section may sit
    within a sentence.
    """
    document, _, heading = section.partition("#")
    for spelled in (
        f"{document}#{heading}",
        f"{document}{BUNDLE_JOIN}{heading}{BUNDLE_SUFFIX}",
    ):
        if re.search(rf"{re.escape(spelled)}(?![\w#-])", target):
            return True
    return False


def dispatched(scenario: Scenario, starts: tuple[Start, ...]) -> Failure | None:
    """The first dispatch check a run's record fails, or nothing when it passes."""
    expected = scenario.trace
    if len(starts) < len(expected) or any(
        not names(start.target, due.section)
        for start, due in zip(starts, expected, strict=False)
    ):
        return Failure.UNDISPATCHED
    if any(
        due.together and not start.together
        for start, due in zip(starts, expected, strict=True)
    ):
        return Failure.SEQUENTIAL_SET
    if any(
        start.returned != due.returned
        for start, due in zip(starts, expected, strict=True)
    ):
        return Failure.UNRELAYED_QUESTION
    return None


def score(workflow: Workflow, scenario: Scenario, workspace: Path) -> Verdict:
    """The verdict on one finished workspace for one scenario."""
    expected = scenario.path
    actual = read_trace(workspace)
    missing = undone(workflow, actual, workspace)
    actions = tuple(
        dict.fromkeys(workflow.walked[actual[index]].action[0] for index in missing)
    )
    divergence = next(
        (
            index
            for index, (taken, due) in enumerate(zip(actual, expected, strict=False))
            if taken != due
        ),
        min(len(actual), len(expected)),
    )
    failure: Failure
    at: int | None
    if actual == expected:
        if missing:
            return Verdict(
                False, Failure.MISSING_ACTION, missing[0], expected, actual, actions
            )
        order = dispatched(scenario, read_starts(workspace))
        if order is None:
            return Verdict(True, None, None, expected, actual, actions)
        failure, at = order, None
    elif divergence == len(actual):
        failure, at = Failure.UNFINISHED, divergence
    else:
        previous = actual[divergence - 1] if divergence else START
        failure, at = departure(workflow, previous, actual[divergence]), divergence
    return Verdict(False, failure, at, expected, actual, actions)
