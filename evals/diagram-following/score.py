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

A dispatch scenario also states the sub-agents a correct run starts and
the action each one's section states, so a run whose trace is the path and
whose actions are done is held to that record before it passes. The
record is `subagents.json` beside the trace, written from the session's
transcript when the session settles, so the scorer reads no transcript and
takes no second read. The dispatch's shape is held first, then the
session's handling of each return as the dispatch protocol states it, then
what the sub-agents wrote:

- the sections the record names, in order, are the scenario's: otherwise
  *undispatched*, since a bundle the scenario dispatches reached no
  sub-agent or reached one in another order;
- every set the scenario states started in one message, its opener first
  and each later member alongside it: otherwise *sequential_set*;
- each start that returned a question is started again later, with the
  answers: otherwise *unrelayed_question*, which is a question the session
  answered in the sub-agent's place or left unanswered. A start that
  returned `done` moves the session on, and asks nothing further;
- each sub-agent's action file holds the value its trace entry states:
  otherwise *missing_action*, named in the verdict's `actions`.

The checks are read in that order, after the run is held to its path and
its actions, so a trace that stopped short is *unfinished* however few
sub-agents it started, and a record failing two checks takes the earlier.
A scenario that dispatches nothing passes all four, and a record absent
from a session that dispatches nothing names no start.

A start is an `Agent` tool call in the transcript, whose prompt names the
compiled file or authored section it hands over; its
return is the sub-agent's report, read as `question` when its first line opens
`Question:`, as `pf`'s guide prescribes, and as `done` otherwise. Two starts
in one message are together, since they were dispatched at once. Which
message and answer a harness's stream records that in, and what frame its
CLI puts around a report, is the harness's to read, as `harness.py`
states: the scorer reads only the record either harness writes.

The verdict's `record` is the form the runner writes and the report reads.
"""

import json
import re
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path

from harness import QUESTION, Harness, Start

__all__ = [
    "ACTIONS",
    "SUBAGENTS",
    "SUB_AGENT_TRACE",
    "TRACE",
    "TRACES",
    "Failure",
    "Start",
    "Verdict",
    "read_starts",
    "read_trace",
    "record_starts",
    "score",
]
from workflow import (
    FEWER,
    SOURCE_DIR,
    START,
    Dispatch,
    Scenario,
    Workflow,
    entry_bundle,
)

TRACE = "trace.log"
"""The path a session writes its own states to."""
SUB_AGENT_TRACE = "trace-{section}.log"
"""The path a dispatched sub-agent writes its states to, named for its section.

Every instruction states it with `<section>` in place of the name, and tells
the session to hand it to each sub-agent it dispatches.
"""
TRACES = "trace*.log"
"""Every trace a workspace holds: the session's, and a sub-agent's beside it.

Both `TRACE` and every `SUB_AGENT_TRACE` match it, so a finished workspace
carries both and the run keeps them together.
"""
ACTIONS = "actions"
SUBAGENTS = "subagents.json"
TRANSCRIPT = "transcript.jsonl"


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
    UNBOOTSTRAPPED = "unbootstrapped"
    ERRORED = "errored"


@dataclass(frozen=True)
class Verdict:
    """One run's score.

    `divergence` is the first index at which the trace and the expected path
    differ; for a missing action, the first index whose state has not done
    its action, or none where a sub-agent's action is the one missing; for
    an unfinished run, the trace's length. A pass carries no failure and no
    divergence. `actions` names the action files absent or wrong among the
    diagram states the trace entered, in trace order, and, for a sub-agent's
    missing action, its file.
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


def written(action: tuple[str, str], workspace: Path) -> bool:
    """Whether an action file exists and holds the stated value."""
    name, value = action
    path = workspace / ACTIONS / name
    return path.is_file() and path.read_text().strip() == value


def action_done(workflow: Workflow, state: str, workspace: Path) -> bool:
    """Whether a state's action file exists and holds the stated value.

    A state stating no action has nothing to do, so it is done.
    """
    action = workflow.walked[state].action
    return True if action is None else written(action, workspace)


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
    transcript: Path, records: Path, harness: Harness
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
            row.get("actor"),
            row.get("group"),
        )
        for row in held.get("starts", [])
        if isinstance(row, dict)
    )


def names(target: str, section: str, source_directory: str = "") -> bool:
    """Whether a start's prompt names a section's compiled file or authored reference.

    A compiled form hands over `pf`'s bundle for the section, named
    `<document>__<heading>.bundle.md` and written beside the entry; an authored form
    hands over the section itself, named `<document>#<heading>`. Both spell
    one section, since the bundle's name is compiled from it.

    A bootstrap skill compiles the documents it carries, so its sections sit
    under `sources/` inside the skill, and a session reaches them by either
    name: the reference the scenario states, or that reference as the skill
    directory holds it.

    The file or reference identifies the section. Description wording and
    headings alone carry no target identity.
    """
    references = [section]
    if source_directory:
        references.insert(0, f"{source_directory}/{section}")
    for reference in references:
        document, _, heading = reference.partition("#")
        for spelled in (
            f"{document}#{heading}",
            f"{document}.md#{heading}",
            entry_bundle(reference).name,
        ):
            if re.search(rf"(?<![\w#-]){re.escape(spelled)}(?![\w#-]|\.\w)", target):
                return True
    return False


def dispatched(
    scenario: Scenario, starts: tuple[Start, ...], source_directory: str = ""
) -> Failure | None:
    """The first dispatch check a run's record fails, or nothing when it passes.

    A session may start a sub-agent for work of its own, as reading the
    material before dispatching is, or start one again with the answers to
    its question, so a start naming no section the scenario expects at that
    point is not a dispatch and is passed over. What is held is that every
    dispatch the scenario states happened, in its order, each together as
    the scenario says, and that each start returning a question was started
    again later with its answers.

    A set states no order among its members: the scenario lists them in the
    order it reads them, and a run may start them in any order so long as they
    start together. Only the sets and the single dispatches are ordered
    against each other.

    The three checks are read over the whole record in order, so a record
    failing two takes the earlier one: a missing dispatch is `undispatched`
    whatever the starts before it returned.
    """
    expected = scenario.trace
    if not expected:
        return None
    taken: set[int] = set()
    matched: list[tuple[int, Start, Dispatch]] = []
    cursor = 0
    for unit in units(expected):
        found: list[tuple[int, Start, Dispatch]] = []
        for due in unit:
            index = next(
                (
                    position
                    for position in range(cursor, len(starts))
                    if position not in taken
                    and names(starts[position].target, due.section, source_directory)
                ),
                None,
            )
            if index is None:
                return Failure.UNDISPATCHED
            found.append((index, starts[index], due))
        matched.extend(found)
        cursor = max(index for index, _, _ in found) + 1
        for index, _, _ in found:
            taken.add(index)
        if len(found) > 1:
            native = [(start.actor, start.group) for _, start, _ in found]
            if any(group is not None for _, group in native):
                if len(set(native)) != 1 or any(
                    actor is None or group is None for actor, group in native
                ):
                    return Failure.SEQUENTIAL_SET
                continue
            # A set states no order, so its opener is whichever member
            # started first. Starts in one message are contiguous, so every
            # later member started alongside it only where no start between
            # them opened a message.
            positions = [index for index, _, _ in found]
            opener, last = min(positions), max(positions)
            if not all(starts[index].together for index in range(opener + 1, last + 1)):
                return Failure.SEQUENTIAL_SET
        elif any(due.together for _, _, due in found):
            return Failure.SEQUENTIAL_SET
    if any(start.returned == "unfinished" for _, start, _ in matched):
        return Failure.UNFINISHED
    if any(
        start.returned == QUESTION
        and not any(
            names(later.target, due.section, source_directory)
            for later in starts[index + 1 :]
        )
        for index, start, due in matched
    ):
        return Failure.UNRELAYED_QUESTION
    return None


def units(expected: tuple[Dispatch, ...]) -> list[list[Dispatch]]:
    """The dispatches a scenario states, a set gathered as one unit.

    A dispatch marked `together` belongs to the set opened by the dispatch
    above it, and a set states no order among its members, so the unit is
    matched as a whole rather than in the order the scenario lists it.
    """
    found: list[list[Dispatch]] = []
    for due in expected:
        if due.together and found:
            found[-1].append(due)
        else:
            found.append([due])
    return found


def score(
    workflow: Workflow,
    scenario: Scenario,
    workspace: Path,
    compiled: bool | None = None,
) -> Verdict:
    """The verdict on one finished workspace for one scenario.

    `compiled` states whether a form whose material must be compiled saw that
    compile run. A session that followed the sources without compiling is
    `unbootstrapped`, since the step the form exists to perform did not
    happen whatever its trace shows.
    """
    expected = scenario.path
    actual = read_trace(workspace)
    missing = undone(workflow, actual, workspace)
    actions = tuple(
        dict.fromkeys(
            name
            for index in missing
            if (found := workflow.walked[actual[index]].action) is not None
            for name in (found[0],)
        )
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
        if compiled is False:
            return Verdict(False, Failure.UNBOOTSTRAPPED, 0, expected, actual, actions)
        order = dispatched(
            scenario, read_starts(workspace), SOURCE_DIR if compiled is not None else ""
        )
        if order is not None:
            return Verdict(False, order, None, expected, actual, actions)
        unwritten = tuple(
            due.action[0]
            for due in scenario.trace
            if due.action is not None and not written(due.action, workspace)
        )
        if unwritten:
            return Verdict(
                False, Failure.MISSING_ACTION, None, expected, actual, unwritten
            )
        return Verdict(True, None, None, expected, actual, actions)
    elif divergence == len(actual):
        failure, at = Failure.UNFINISHED, divergence
    else:
        previous = actual[divergence - 1] if divergence else START
        failure, at = departure(workflow, previous, actual[divergence]), divergence
    return Verdict(False, failure, at, expected, actual, actions)
