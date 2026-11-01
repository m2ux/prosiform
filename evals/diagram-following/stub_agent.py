"""A stand-in for the agent command, which the runner's tests start instead.

It runs in a session's workspace and takes the agent's options, which it
records and otherwise ignores. It recognises the workflow by the state
headings its workspace's documents hold, walks that workflow's diagram for
the inputs under `inputs/`, and writes the walk to `trace.log` with every
state's action, as a correct agent would. It then prints a stream-json
transcript ending in a `result` message carrying usage and a cost.

A workflow that dispatches takes a `Task` call per sub-agent start the
scenario states, each naming its section as `<document>#<heading>`, with
the outcome the scenario gives it. The entries a scenario marks `together`
share one assistant message, so they read as started at once, and each
call is answered by a `tool_result` carrying `question` or `done`.

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
  its environment's variables and its `CLAUDE_CONFIG_DIR`;
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
import sys
import time
import uuid
from pathlib import Path

from harness import QUESTION as RETURNED_QUESTION
from score import ACTIONS, TRACE
from workflow import Scenario, Workflow, walk, workflows

HEADING = re.compile(r"^# (\w+)$", re.MULTILINE)


def held(workspace: Path) -> list[str]:
    """Every file under a workspace, as paths relative to it."""
    return sorted(
        str(path.relative_to(workspace))
        for path in workspace.rglob("*")
        if path.is_file()
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


def message(identifier: str, start: tuple[str, str, bool]) -> dict[str, object]:
    """One `Task` call, its description naming the section it hands over."""
    section, _, _ = start
    return {
        "type": "tool_use",
        "id": identifier,
        "name": "Task",
        "input": {"description": section, "prompt": f"Follow {section}."},
    }


def transcript_of(started: list[tuple[str, str, bool]]) -> list[dict[str, object]]:
    """The assistant and user messages a session's sub-agent starts print.

    Two starts together share one assistant message, and each call is
    answered on its own, so a reader recovers both the order and what each
    sub-agent returned.
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
        group.append(message(identifier, start))
        made.append((identifier, returned))
    flush()
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
        entry["prompt"] = prompt
        entry["variables"] = sorted(os.environ)
        entry["config"] = os.environ.get("CLAUDE_CONFIG_DIR")
        (Path(log) / f"{uuid.uuid4()}.json").write_text(json.dumps(entry))
    headings = {
        heading
        for name in files
        if name.endswith(".md")
        for heading in HEADING.findall((workspace / name).read_text())
    }
    workflow = next(item for item in workflows() if item.diagram.states <= headings)
    inputs = {path.name: path.read_text() for path in (workspace / "inputs").iterdir()}
    path = walk(workflow, workflow.forms[0], inputs)
    if stop := os.environ.get("STUB_AGENT_STOP"):
        path = path[: int(stop)]
    (workspace / ACTIONS).mkdir()
    with (workspace / TRACE).open("w") as trace:
        for state in path:
            trace.write(f"{state}\n")
            name, value = workflow.walked[state].action
            (workspace / ACTIONS / name).write_text(f"{value}\n")
    dispatch = starts(scenario_of(workflow, inputs))
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
    if dispatch:
        for said in transcript_of(dispatch):
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
