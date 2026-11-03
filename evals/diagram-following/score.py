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
- every set the scenario states started in one message, its opener first
  and each later member alongside it: otherwise *sequential_set*;
- each start's return is the scenario's: otherwise *unrelayed_question*,
  which is a question the sub-agent returned and the session answered in
  its place.

The checks are read in that order, after the run is held to its path and
its actions, so a trace that stopped short is *unfinished* however few
sub-agents it started, and a record failing two checks takes the earlier.
A scenario that dispatches nothing passes all three, and a record absent
from a session that dispatches nothing names no start.

A start the scenario states may also name the actions its sub-agent does,
which only the material a `pf` run on a deferred line of its bundle
compiles states. A run passing the dispatch checks is held to those files
as a state's action is, whatever its harness reports of the sub-agent's
commands: one absent or wrong is *missing action*, so a sub-agent that ran
no `pf` on its line fails though no stream carries what it ran.

A scenario also states the `pf` runs a correct run makes, so a run that
passes the dispatch checks and its sub-agents' actions is held to them
wherever its harness reports the commands a session ran. The record holds
the session's commands beside its starts, and each start the commands its
own sub-agent ran. A command is a
`pf` run in each segment `;`, `&&`, `||` or `|` separate whose first word is
`pf` or a path ending `/pf`, and the run's references are its words other
than options and their values. A reference names a stated one when it is that
reference or ends `/` and that reference, so a run from another directory
names the same document. Each agent's runs, the session's and each started
sub-agent's, are held to the runs stated for it:

- every stated run was made: otherwise *uncompiled*;
- every run naming a reference is a stated one: otherwise *overcompiled*,
  as a run on a deferred line the path did not reach is. A bare `pf` beyond
  those stated prints the guide and compiles nothing, so it is no departure;
- the stated runs were made in their order: otherwise *misordered_compile*.

The checks are read in that order, after the dispatch checks, so a sub-agent
that never started fails *undispatched* rather than leaving its runs unmade.

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
import shlex
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path

from harness import Harness, Start

__all__ = [
    "ACTIONS",
    "SUBAGENTS",
    "SUB_AGENT_TRACE",
    "TRACE",
    "TRACES",
    "Failure",
    "Start",
    "Verdict",
    "pf_runs",
    "read_commands",
    "read_starts",
    "read_trace",
    "record_calls",
    "score",
]
from workflow import FEWER, START, Dispatch, Scenario, Workflow

PF = "pf"
SEPARATORS = re.compile(r"&&|\|\||[;|\n]")
"""What separates one command of a shell line from the next."""
VALUED = frozenset({"-o", "-d", "--budget"})
"""The `pf` options taking a value as the next word, which is no reference."""

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
    UNCOMPILED = "uncompiled"
    OVERCOMPILED = "overcompiled"
    MISORDERED_COMPILE = "misordered_compile"
    ERRORED = "errored"


@dataclass(frozen=True)
class Verdict:
    """One run's score.

    `divergence` is the first index at which the trace and the expected path
    differ; for a missing action, the first index whose state has not done
    its action, or none where a sub-agent's is the one undone; for an
    unfinished run, the trace's length. A pass carries no failure and no
    divergence. `actions` names the action files absent or wrong among the
    diagram states the trace entered, in trace order, or, where those are
    done, among the sub-agents' actions the scenario states.
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


def sub_agent_undone(scenario: Scenario, workspace: Path) -> tuple[str, ...]:
    """The action files a scenario's sub-agents leave undone, in trace order."""
    return tuple(
        dict.fromkeys(
            name
            for entry in scenario.trace
            for name, value in entry.actions
            if not (
                (written := workspace / ACTIONS / name).is_file()
                and written.read_text().strip() == value
            )
        )
    )


def record_calls(
    transcript: Path, records: Path, harness: Harness
) -> tuple[Start, ...]:
    """Read a session's transcript for its commands and starts and record them.

    The record is `subagents.json` beside the trace and the session's tokens:
    `commands`, the shell commands the session ran, null where the harness
    gives it no shell, and `starts`, one entry per start in the order the
    transcript made them, each naming its parent start and its sub-agent's
    commands. The scorer reads it instead of the transcript. The harness
    reads its own stream, so one record shape serves every agent CLI.
    """
    starts = harness.starts(transcript)
    commands = harness.commands(transcript)
    held = {
        "commands": None if commands is None else list(commands),
        "starts": [start.record() for start in starts],
    }
    (records / SUBAGENTS).write_text(json.dumps(held, indent=2) + "\n")
    return starts


def _held(workspace: Path) -> dict[str, object]:
    """The record a workspace holds, or nothing where it holds none readable."""
    path = workspace / SUBAGENTS
    if not path.is_file():
        return {}
    try:
        held = json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}
    return held if isinstance(held, dict) else {}


def _texts(value: object) -> tuple[str, ...]:
    """The strings a record's list holds, in order."""
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str))


def read_commands(workspace: Path) -> tuple[str, ...] | None:
    """The shell commands a workspace's record says the session ran.

    A record naming no list says the harness reports no command, so nothing
    can be asked of what the session ran.
    """
    commands = _held(workspace).get("commands")
    return _texts(commands) if isinstance(commands, list) else None


def read_starts(workspace: Path) -> tuple[Start, ...]:
    """The sub-agent starts a workspace's record holds, in order.

    The record is read as the runner wrote it, so the scorer takes no second
    read of the transcript, and a workspace with no record names no start.
    """
    rows = _held(workspace).get("starts", [])
    return tuple(
        Start(
            str(row.get("target", "")),
            str(row.get("returned", "")),
            bool(row.get("together")),
            row["parent"] if isinstance(row.get("parent"), int) else None,
            _texts(row.get("commands")),
        )
        for row in (rows if isinstance(rows, list) else [])
        if isinstance(row, dict)
    )


def _words(segment: str) -> list[str]:
    """One command's words, as the shell splits them where it can."""
    try:
        return shlex.split(segment)
    except ValueError:
        return segment.split()


def pf_runs(commands: tuple[str, ...]) -> list[tuple[str, ...]]:
    """The `pf` runs a list of shell commands makes, each as its references.

    A run is a command whose first word is `pf` or a path ending `/pf`, since
    a command may name the build by a directory. Its references are its words
    other than an option and the value an option takes.
    """
    runs: list[tuple[str, ...]] = []
    for command in commands:
        for segment in SEPARATORS.split(command):
            words = _words(segment)
            if not words or words[0].rsplit("/", 1)[-1] != PF:
                continue
            references: list[str] = []
            skip = False
            for word in words[1:]:
                if skip:
                    skip = False
                elif word in VALUED:
                    skip = True
                elif not word.startswith("-"):
                    references.append(word.removeprefix("./"))
            runs.append(tuple(references))
    return runs


def _names(made: tuple[str, ...], stated: tuple[str, ...]) -> bool:
    """Whether a run's references are a stated run's, from any directory."""
    return len(made) == len(stated) and all(
        reference == due or reference.endswith(f"/{due}")
        for reference, due in zip(made, stated, strict=True)
    )


def _held_to(
    made: list[tuple[str, ...]], stated: list[tuple[str, ...]]
) -> Failure | None:
    """The first run check one agent's runs fail, or nothing when they pass."""
    if not all(any(_names(run, due) for run in made) for due in stated):
        return Failure.UNCOMPILED
    if any(run and not any(_names(run, due) for due in stated) for run in made):
        return Failure.OVERCOMPILED
    cursor = 0
    for run in made:
        if cursor < len(stated) and _names(run, stated[cursor]):
            cursor += 1
    return None if cursor == len(stated) else Failure.MISORDERED_COMPILE


def compiles(
    scenario: Scenario, commands: tuple[str, ...], starts: tuple[Start, ...]
) -> Failure | None:
    """The first run check a session's record fails, or nothing when it passes.

    The session's runs are read from its own commands, and a sub-agent's from
    the commands of every start naming its section, so a section dispatched
    again keeps one sequence of runs. Each check is read over every agent
    before the next, so a record failing two takes the earlier.
    """
    agents: dict[str | None, list[tuple[str, ...]]] = {None: pf_runs(commands)}
    for section in dict.fromkeys(entry.section for entry in scenario.trace):
        agents[section] = pf_runs(
            tuple(
                command
                for start in starts
                if names(start.target, section)
                for command in start.commands
            )
        )
    stated = {
        agent: [run.args for run in scenario.compile if run.by == agent]
        for agent in agents
    }
    found = [_held_to(made, stated[agent]) for agent, made in agents.items()]
    order = (Failure.UNCOMPILED, Failure.OVERCOMPILED, Failure.MISORDERED_COMPILE)
    return next((failure for failure in order if failure in found), None)


def names(target: str, section: str) -> bool:
    """Whether a start's target names a section, as a section or as its bundle.

    A compiled form hands over `pf`'s bundle for the section, named
    `<document>__<heading>` with each `/` of the document's path written as
    `_`, and written beside the entry; an authored form
    hands over the section itself, named `<document>#<heading>`. Both spell
    one section, since the bundle's name is compiled from it.

    A session's call text is its own wording, so the section may be named by
    its heading alone: an agent handing over `plan#work` writes "the Plan
    Work section" as readily as the path. The heading is therefore matched as
    a word of the text, beside the two spellings that pin it exactly.
    """
    document, _, heading = section.partition("#")
    for spelled in (
        f"{document}#{heading}",
        f"{document.replace('/', '_')}{BUNDLE_JOIN}{heading}{BUNDLE_SUFFIX}",
    ):
        if re.search(rf"{re.escape(spelled)}(?![\w#-])", target):
            return True
    return re.search(rf"\b{re.escape(heading)}\b", target, re.IGNORECASE) is not None


def dispatched(scenario: Scenario, starts: tuple[Start, ...]) -> Failure | None:
    """The first dispatch check a run's record fails, or nothing when it passes.

    A session may start a sub-agent for work of its own, as reading the
    material before dispatching is, so a start naming no section the scenario
    expects is not a dispatch and is passed over. What is held is that every
    dispatch the scenario states happened, in its order, each together or
    returning as the scenario says.

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
    matched: list[tuple[Start, Dispatch]] = []
    cursor = 0
    for unit in units(expected):
        found: list[tuple[int, Start, Dispatch]] = []
        for due in unit:
            index = next(
                (
                    position
                    for position in range(cursor, len(starts))
                    if position not in taken
                    and names(starts[position].target, due.section)
                ),
                None,
            )
            if index is None:
                return Failure.UNDISPATCHED
            found.append((index, starts[index], due))
        matched.extend((start, due) for _, start, due in found)
        cursor = max(index for index, _, _ in found) + 1
        for index, _, _ in found:
            taken.add(index)
        if len(found) > 1:
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
    if any(start.returned != due.returned for start, due in matched):
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
) -> Verdict:
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
        starts = read_starts(workspace)
        commands = read_commands(workspace)
        order = dispatched(scenario, starts)
        if order is None and (undone_by := sub_agent_undone(scenario, workspace)):
            return Verdict(
                False, Failure.MISSING_ACTION, None, expected, actual, undone_by
            )
        if order is None and commands is not None:
            order = compiles(scenario, commands, starts)
        if order is None:
            return Verdict(True, None, None, expected, actual, actions)
        failure, at = order, None
    elif divergence == len(actual):
        failure, at = Failure.UNFINISHED, divergence
    else:
        previous = actual[divergence - 1] if divergence else START
        failure, at = departure(workflow, previous, actual[divergence]), divergence
    return Verdict(False, failure, at, expected, actual, actions)
