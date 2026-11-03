"""A stand-in for the agent command, which the runner's tests start instead.

It runs in a session's workspace and takes the agent's options, which it
records and otherwise ignores. It recognises the workflow by the state
headings its workspace's documents hold, at whatever level a group placed
them, walks the path of the scenario whose inputs `inputs/` holds, or else
that workflow's diagram for those inputs, and writes the walk to
`trace.log` with every state's action, as a correct agent would. A state
deferring its transition is followed only through the scenario's path. It
then prints a stream-json transcript ending in a `result` message carrying
usage and a cost.

A workflow that dispatches takes a `Task` call per sub-agent start the
scenario states, each naming its section as `<document>#<heading>`, with
the outcome the scenario gives it. The entries a scenario marks `together`
share one assistant message, so they read as started at once, and each
call is answered by a `tool_result` carrying `question` or `done`. Where its
instruction names the sub-agent trace, each call's prompt hands that name on,
and each sub-agent writes the trace its prompt names and no other, and the
actions the scenario states for it.

Where its `--tools` names `Bash`, it makes each `pf` run the scenario
states as a `Bash` call: the session's own in a message of its own, and a
sub-agent's in a message naming that sub-agent's `Task` call as
`parent_tool_use_id`, as the CLI prints a sub-agent's calls. A session whose
workspace holds `bin/pf` and whose scenario states no run of its own runs
bare `pf`, as its bundle's first line asks.

The environment scripts it:

- `STUB_AGENT_COST`: the cost its `result` message reports, in USD;
- `STUB_AGENT_TOKENS`: the tokens its `result` message reports, each kind set so
  their sum is this number;
- `STUB_AGENT_STOP`: a number of states after which it stops walking;
- `STUB_AGENT_NO_DISPATCH`: when set, it starts no sub-agent, as an agent
  that read the protocol and ignored it does;
- `STUB_AGENT_SEQUENTIAL`: when set, it starts every sub-agent in a message
  of its own, as an agent running a set one after another does;
- `STUB_AGENT_ANSWER`: when set, every sub-agent returns `done`, as one
  whose question the session answered in the sub-agent's place does;
- `STUB_AGENT_LOG`: a directory to which it writes, per session, the files
  its workspace held on starting, its arguments, its prompt, the names of
  its environment's variables, its `CLAUDE_CONFIG_DIR` and the `pf` its path
  resolves to;
- `STUB_AGENT_SILENT`: when set, it prints no `result` message;
- `STUB_AGENT_ERROR`: when set, its `result` message reports `is_error` true,
  as a refusal or a crashed agent does;
- `STUB_AGENT_ERROR_ONCE`: a file the first session to find it absent creates,
  then reports `is_error` true, so a run mixes an errored session with passing
  ones on a real fault;
- `STUB_AGENT_REASON`: the text its `result` message carries, as a refused
  agent's message states the limit it hit;
- `STUB_AGENT_INJECT`: text the agent prints as a hook response before its
  first turn, as a plugin's `SessionStart` hook delivers one;
- `STUB_AGENT_HANG`: a file the first session to find it absent creates,
  then hangs after writing its trace, printing nothing more.
"""

import json
import os
import re
import shutil
import sys
import time
import uuid
from pathlib import Path

from harness import PARENT, SHELL_TOOL
from harness import QUESTION as RETURNED_QUESTION
from score import ACTIONS, SUB_AGENT_TRACE, TRACE
from workflow import Scenario, Workflow, walk, workflows

STATED_TRACE = SUB_AGENT_TRACE.format(section="<section>")
"""The sub-agent trace as an instruction states it."""

HANDED_TRACE = re.compile(re.escape(SUB_AGENT_TRACE).replace(r"\{section\}", r"(\S+?)"))
"""The sub-agent trace a `Task` prompt names, the section's name its group."""

HEADING = re.compile(r"^#+ (\w+)$", re.MULTILINE)


def held(workspace: Path) -> list[str]:
    """Every file under a workspace, as paths relative to it."""
    return sorted(
        str(path.relative_to(workspace))
        for path in workspace.rglob("*")
        if path.is_file()
    )


def recognised(headings: set[str], corpus: list[Workflow]) -> Workflow:
    """The workflow a workspace holds, from the headings its documents carry.

    It is the workflow with the most states, each heading a section there,
    since one whose states are a subset of another's is headed in that one's
    workspace too.
    """
    return max(
        (item for item in corpus if item.diagram.states <= headings),
        key=lambda item: len(item.diagram.states),
    )


def scenario_of(workflow: Workflow, inputs: dict[str, str]) -> Scenario | None:
    """The scenario whose inputs a session's workspace holds, when one does."""
    wanted = {name: value.strip() for name, value in inputs.items()}
    for item in workflow.scenarios:
        if {name: value.strip() for name, value in item.inputs.items()} == wanted:
            return item
    return None


def usage(path: tuple[str, ...]) -> dict[str, int]:
    """The usage a session reports, its kinds summing to STUB_AGENT_TOKENS."""
    total = os.environ.get("STUB_AGENT_TOKENS")
    return (
        {"input_tokens": int(total), "output_tokens": 0}
        if total
        else {"input_tokens": 100 * len(path), "output_tokens": 10}
    )


def starts(item: Scenario | None) -> list[tuple[str, str, bool]]:
    """The sub-agent starts a session makes: a section, its return and a set flag.

    The flag marks an entry the scenario states started beside the one above
    it, which is where a set's members share one message. An agent that ran
    the set in sequence or skipped every dispatch is scripted here, so the
    scorer's checks have a trace to classify.
    """
    if item is None or os.environ.get("STUB_AGENT_NO_DISPATCH"):
        return []
    answer = os.environ.get("STUB_AGENT_ANSWER")
    sequential = bool(os.environ.get("STUB_AGENT_SEQUENTIAL"))
    return [
        (
            entry.section,
            answer or entry.returned,
            entry.together and not sequential,
        )
        for entry in item.trace
    ]


def shell_runs(item: Scenario | None, argv: list[str]) -> list[tuple[str | None, str]]:
    """Each stated `pf` run as the agent making it and its command line.

    A session whose `--tools` names no shell runs none.
    """
    tools = argv[argv.index("--tools") + 1] if "--tools" in argv else ""
    if item is None or SHELL_TOOL not in tools.split(","):
        return []
    return [(run.by, " ".join(["pf", *run.args])) for run in item.compile]


def shell_call(command: str, owner: str | None) -> dict[str, object]:
    """One assistant message making a `Bash` call, under `owner`'s `Task` call."""
    return {
        "type": "assistant",
        PARENT: owner,
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "id": f"toolu_{uuid.uuid4().hex[:12]}",
                    "name": SHELL_TOOL,
                    "input": {"command": command},
                }
            ]
        },
    }


def handed(section: str, instruction: str) -> str:
    """The prompt a session's `Task` call gives the sub-agent following a section.

    A sub-agent reads only this prompt, so it learns its trace's name only
    where the session's instruction stated that name for the session to hand on.
    """
    if STATED_TRACE not in instruction:
        return f"Follow {section}."
    document, _, heading = section.partition("#")
    trace = SUB_AGENT_TRACE.format(section=heading or document)
    return f"Follow {section}. Append each state you enter to {trace}."


def write_sub_agent_traces(workspace: Path, prompts: list[str]) -> None:
    """Record each dispatched sub-agent's own path, where its prompt names one.

    A sub-agent writes the trace its prompt names and nothing else, so a
    prompt naming none leaves no trace. The path holds the section's name as
    its one state; what a nested chart draws is the sub-agent's own material,
    which this stub does not read.
    """
    for prompt in prompts:
        if named := HANDED_TRACE.search(prompt):
            (workspace / named.group(0)).write_text(f"{named.group(1).title()}\n")


def message(
    identifier: str, start: tuple[str, str, bool], instruction: str
) -> dict[str, object]:
    """One `Task` call, its description naming the section it hands over."""
    section, _, _ = start
    return {
        "type": "tool_use",
        "id": identifier,
        "name": "Task",
        "input": {"description": section, "prompt": handed(section, instruction)},
    }


def transcript_of(
    started: list[tuple[str, str, bool]],
    instruction: str,
    runs: list[tuple[str | None, str]],
) -> list[dict[str, object]]:
    """The assistant and user messages a session's sub-agent starts print.

    Two starts together share one assistant message, and each call is
    answered on its own, so a reader recovers both the order and what each
    sub-agent returned. A sub-agent's run is printed under the first start
    of the section it states, before any call is answered.
    """
    messages: list[dict[str, object]] = []
    made: list[tuple[str, str]] = []
    group: list[dict[str, object]] = []

    def flush() -> None:
        if group:
            messages.append({"type": "assistant", "message": {"content": list(group)}})
            group.clear()

    for start in started:
        _, returned, together = start
        identifier = f"toolu_{uuid.uuid4().hex[:12]}"
        if not together:
            flush()
        group.append(message(identifier, start, instruction))
        made.append((identifier, returned))
    flush()
    first: dict[str, str] = {}
    for (section, _, _), (identifier, _) in zip(started, made, strict=True):
        first.setdefault(section, identifier)
    messages.extend(
        shell_call(command, first.get(by)) for by, command in runs if by is not None
    )
    for identifier, returned in made:
        text = (
            "question: which provider should the draft name?"
            if returned == RETURNED_QUESTION
            else "done: the section is complete."
        )
        messages.append(
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": identifier,
                            "content": text,
                        }
                    ]
                },
            }
        )
    return messages


def main() -> int:
    """Act as an agent following the workflow in the current directory."""
    workspace = Path.cwd()
    prompt = sys.stdin.read()
    files = held(workspace)
    if log := os.environ.get("STUB_AGENT_LOG"):
        entry: dict[str, object] = {"workspace": str(workspace), "files": files}
        entry["argv"] = sys.argv[1:]
        entry["pf"] = (workspace / "bin" / "pf").is_file()
        entry["prompt"] = prompt
        entry["variables"] = sorted(os.environ)
        entry["config"] = os.environ.get("CLAUDE_CONFIG_DIR")
        entry["which_pf"] = shutil.which("pf")
        (Path(log) / f"{uuid.uuid4()}.json").write_text(json.dumps(entry))
    headings = {
        heading
        for name in files
        if name.endswith(".md")
        for heading in HEADING.findall((workspace / name).read_text())
    }
    workflow = recognised(headings, workflows())
    inputs = {path.name: path.read_text() for path in (workspace / "inputs").iterdir()}
    item = scenario_of(workflow, inputs)
    path = item.path if item else walk(workflow, workflow.forms[0], inputs)
    if stop := os.environ.get("STUB_AGENT_STOP"):
        path = path[: int(stop)]
    (workspace / ACTIONS).mkdir()
    with (workspace / TRACE).open("w") as trace:
        for state in path:
            trace.write(f"{state}\n")
            name, value = workflow.walked[state].action
            (workspace / ACTIONS / name).write_text(f"{value}\n")
    dispatch = starts(item)
    write_sub_agent_traces(
        workspace, [handed(section, prompt) for section, _, _ in dispatch]
    )
    if item is not None and dispatch:
        for due in item.trace:
            for name, value in due.actions:
                (workspace / ACTIONS / name).write_text(f"{value}\n")
    hang = os.environ.get("STUB_AGENT_HANG")
    if hang and not Path(hang).exists():
        Path(hang).touch()
        time.sleep(3600)
    print(json.dumps({"type": "system", "subtype": "init", "cwd": str(workspace)}))
    if inject := os.environ.get("STUB_AGENT_INJECT"):
        print(
            json.dumps(
                {
                    "type": "system",
                    "subtype": "hook_response",
                    "hook_event": "SessionStart:startup",
                    "additionalContext": inject,
                }
            )
        )
    runs = shell_runs(item, sys.argv[1:])
    own = [command for by, command in runs if by is None]
    if not own and (workspace / "bin" / "pf").is_file():
        own = ["pf"]
    for command in own:
        print(json.dumps(shell_call(command, None)))
    if dispatch:
        for said in transcript_of(dispatch, prompt, runs):
            print(json.dumps(said))
    else:
        print(json.dumps({"type": "assistant", "message": {"content": list(path)}}))
    if not os.environ.get("STUB_AGENT_SILENT"):
        once = os.environ.get("STUB_AGENT_ERROR_ONCE")
        errored = bool(os.environ.get("STUB_AGENT_ERROR"))
        if once and not Path(once).exists():
            Path(once).touch()
            errored = True
        result = {
            "type": "result",
            "subtype": "success",
            "is_error": errored,
            "result": os.environ.get("STUB_AGENT_REASON", ""),
            "num_turns": len(path),
            "total_cost_usd": float(os.environ.get("STUB_AGENT_COST", "0.01")),
            "usage": usage(path),
        }
        print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
