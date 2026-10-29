"""A stand-in for the agent command, which the runner's tests start instead.

It runs in a session's workspace and takes the agent's options, which it
records and otherwise ignores. It recognises the workflow by the state
headings its workspace's documents hold, walks that workflow's diagram for
the inputs under `inputs/`, and writes the walk to `trace.log` with every
state's action, as a correct agent would. It then prints a stream-json
transcript ending in a `result` message carrying usage and a cost.

The environment scripts it:

- `STUB_AGENT_COST`: the cost its `result` message reports, in USD;
- `STUB_AGENT_STOP`: a number of states after which it stops walking;
- `STUB_AGENT_LOG`: a directory to which it writes, per session, the files
  its workspace held on starting, its arguments, its prompt, the names of
  its environment's variables and its `CLAUDE_CONFIG_DIR`;
- `STUB_AGENT_SILENT`: when set, it prints no `result` message;
- `STUB_AGENT_ERROR`: when set, its `result` message reports `is_error` true,
  as a refusal or a crashed agent does;
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

from score import ACTIONS, TRACE
from workflow import DIAGRAM, walk, workflows

HEADING = re.compile(r"^# (\w+)$", re.MULTILINE)


def held(workspace: Path) -> list[str]:
    """Every file under a workspace, as paths relative to it."""
    return sorted(
        str(path.relative_to(workspace))
        for path in workspace.rglob("*")
        if path.is_file()
    )


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
    path = walk(workflow, DIAGRAM, inputs)
    if stop := os.environ.get("STUB_AGENT_STOP"):
        path = path[: int(stop)]
    (workspace / ACTIONS).mkdir()
    with (workspace / TRACE).open("w") as trace:
        for state in path:
            trace.write(f"{state}\n")
            name, value = workflow.sections[DIAGRAM][state].action
            (workspace / ACTIONS / name).write_text(f"{value}\n")
    hang = os.environ.get("STUB_AGENT_HANG")
    if hang and not Path(hang).exists():
        Path(hang).touch()
        time.sleep(3600)
    print(json.dumps({"type": "system", "subtype": "init", "cwd": str(workspace)}))
    print(json.dumps({"type": "assistant", "message": {"content": list(path)}}))
    if not os.environ.get("STUB_AGENT_SILENT"):
        result = {
            "type": "result",
            "subtype": "success",
            "is_error": bool(os.environ.get("STUB_AGENT_ERROR")),
            "num_turns": len(path),
            "total_cost_usd": float(os.environ.get("STUB_AGENT_COST", "0.01")),
            "usage": {"input_tokens": 100 * len(path), "output_tokens": 10},
        }
        print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
