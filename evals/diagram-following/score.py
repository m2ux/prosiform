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

The verdict's `record` is the form the runner writes and the report reads.
"""

from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path

from workflow import FEWER, START, Scenario, Workflow

TRACE = "trace.log"
ACTIONS = "actions"


class Failure(StrEnum):
    """How a failing run departed from its scenario."""

    WRONG_BRANCH = "wrong_branch"
    SKIPPED_STATE = "skipped_state"
    INVENTED_STATE = "invented_state"
    INVALID_TRANSITION = "invalid_transition"
    LOOP_MISCOUNT = "loop_miscount"
    MISSING_ACTION = "missing_action"
    UNFINISHED = "unfinished"
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
    if actual == expected:
        if not missing:
            return Verdict(True, None, None, expected, actual, actions)
        failure, divergence = Failure.MISSING_ACTION, missing[0]
    elif divergence == len(actual):
        failure = Failure.UNFINISHED
    else:
        previous = actual[divergence - 1] if divergence else START
        failure = departure(workflow, previous, actual[divergence])
    return Verdict(False, failure, divergence, expected, actual, actions)
