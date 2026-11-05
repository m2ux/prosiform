"""Drive one native Codex app-server session with workspace files and `pf`.

The bridge preserves native events, response boundaries and child-thread
reports. Its file tools resolve every path within the prepared workspace;
its `pf` tool runs an argv vector through the server's own sandbox.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import sys
from pathlib import Path
from subprocess import PIPE, Popen, TimeoutExpired
from typing import Any

START_TOOLS = {"spawnAgent", "sendInput", "followupTask"}
FINAL = "final_answer"
CONFIG = {
    "project_doc_max_bytes": 0,
    "memories.use_memories": False,
    "memories.generate_memories": False,
    "skills.bundled.enabled": False,
    "skills.include_instructions": False,
    "web_search": "disabled",
    "features.skip_host_skill_discovery": True,
}
DISABLED = ("apps", "plugins", "remote_plugin", "memories", "hooks", "shell_tool")


def configuration(result: dict[str, Any], root: Path, home: Path) -> dict[str, Any]:
    """Verify effective capabilities and loaded layers without logging their content."""
    config = result["config"]
    layers = result["layers"]
    if not isinstance(config, dict) or not isinstance(layers, list):
        raise ProtocolError("Codex supplied no complete configuration-layer readback")
    for layer in layers:
        if layer.get("disabledReason"):
            continue
        source = layer["name"]
        if source.get("type") == "project" and not Path(
            source["dotCodexFolder"]
        ).resolve().is_relative_to(root):
            raise ProtocolError("Codex loaded an ancestor project configuration")
        if source.get("type") == "user" and not Path(
            source["file"]
        ).resolve().is_relative_to(home):
            raise ProtocolError("Codex loaded caller configuration")
    if config.get("instructions") or config.get("developer_instructions"):
        raise ProtocolError("Codex carries instructions the eval did not supply")
    if any(
        server.get("enabled", True)
        for server in (config.get("mcp_servers") or {}).values()
    ):
        raise ProtocolError("Codex carries an enabled MCP server")
    features = config.get("features", {})
    if any(features.get(name) is not False for name in DISABLED):
        raise ProtocolError(
            "Codex did not disable an external capability or native shell"
        )
    if (
        features.get("skip_host_skill_discovery") is not True
        or config.get("project_doc_max_bytes") != 0
    ):
        raise ProtocolError("Codex did not isolate host skills and instruction files")
    canonical = json.dumps(layers, sort_keys=True, separators=(",", ":"))
    return {
        "type": "codex_config",
        "layers": len(layers),
        "fingerprint": hashlib.sha256(canonical.encode()).hexdigest(),
    }


class ProtocolError(ValueError):
    """Native evidence or isolation needed by the eval is unavailable."""


def workspace_path(root: Path, named: str) -> Path:
    """Resolve a file-tool path within its workspace, including every symlink."""
    path = (root / named).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("the path is outside this session's workspace")
    return path


def schema(properties: dict[str, object], required: list[str]) -> dict[str, object]:
    """One dynamic tool's object arguments."""
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


TOOLS = [
    {
        "type": "function",
        "name": "read_file",
        "description": "Read a UTF-8 file in this workspace, using its relative path.",
        "inputSchema": schema({"path": {"type": "string"}}, ["path"]),
    },
    {
        "type": "function",
        "name": "list_files",
        "description": "List workspace files recursively; use '.' for all files.",
        "inputSchema": schema({"path": {"type": "string"}}, ["path"]),
    },
    {
        "type": "function",
        "name": "write_file",
        "description": "Write or append a UTF-8 workspace file, creating directories.",
        "inputSchema": schema(
            {
                "path": {"type": "string"},
                "content": {"type": "string"},
                "append": {"type": "boolean"},
            },
            ["path", "content", "append"],
        ),
    },
    {
        "type": "function",
        "name": "pf",
        "description": (
            "Run pf with any arguments; [] prints its guide. cwd is a workspace "
            "directory; stdout/stderr paths redirect output relative to cwd."
        ),
        "inputSchema": schema(
            {
                "args": {"type": "array", "items": {"type": "string"}},
                "cwd": {"type": ["string", "null"]},
                "stdout": {"type": ["string", "null"]},
                "stderr": {"type": ["string", "null"]},
                "append": {"type": "boolean"},
                "stderr_to_stdout": {"type": "boolean"},
            },
            ["args", "cwd", "stdout", "stderr", "append", "stderr_to_stdout"],
        ),
    },
]


def file_tool(root: Path, name: str, arguments: dict[str, Any]) -> str:
    """Carry out one confined file operation, with no shell execution."""
    path = workspace_path(root, arguments["path"])
    if name == "read_file":
        return path.read_text()
    if name == "list_files":
        paths = sorted(path.rglob("*")) if path.is_dir() else [path]
        return "\n".join(
            str(workspace_path(root, str(found)).relative_to(root))
            for found in paths
            if found.is_file()
        )
    if name == "write_file":
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a" if arguments["append"] else "w") as output:
            output.write(arguments["content"])
        return "Written."
    raise ValueError(f"no file tool {name!r}")


def policy(root: Path) -> dict[str, object]:
    """The server sandbox for the workspace and each actual `pf` invocation."""
    return {
        "type": "workspaceWrite",
        "writableRoots": [str(root)],
        "networkAccess": False,
        "excludeTmpdirEnvVar": True,
        "excludeSlashTmp": True,
    }


def pf_command(arguments: dict[str, Any]) -> str:
    """The canonical command a structured `pf` invocation actually runs."""
    command = shlex.join(["pf", *arguments["args"]])
    for key, operator in (("stdout", ">"), ("stderr", "2>")):
        if arguments.get(key) is not None:
            redirect = operator + (">" if arguments.get("append") else "")
            command += f" {redirect} {shlex.quote(arguments[key])}"
    if arguments.get("stderr_to_stdout"):
        command += " 2>&1"
    return command


def summarize(events: list[dict[str, Any]], root: str) -> dict[str, Any]:
    """Read native dispatch, response groups, reports and cumulative usage."""
    pending: dict[tuple[str, str], list[str]] = {}
    groups: dict[str, tuple[str, str]] = {}
    starts: dict[str, tuple[int, dict[str, Any]]] = {}
    reports: dict[str, list[tuple[int, str]]] = {}
    waited: dict[str, set[int]] = {}
    turn_first: dict[tuple[str, str], int] = {}
    turn_done: dict[tuple[str, str], int] = {}
    turn_text: dict[tuple[str, str], str] = {}
    usage: dict[str, dict[str, Any]] = {}
    raw_usage: dict[tuple[str, str], int] = {}
    commands = []
    final = ""
    status = None
    turn_error = None
    for index, event in enumerate(events):
        method = event.get("method")
        params = event.get("params", {})
        thread = params.get("threadId", "")
        key = (thread, params.get("turnId", ""))
        if thread and key[1]:
            turn_first.setdefault(key, index)
        if method in {"turn/started", "turn/completed"} and thread:
            turn_key = (thread, params["turn"]["id"])
            turn_first.setdefault(turn_key, index)
            if method == "turn/completed":
                turn_done[turn_key] = index
        if event.get("type") == "pf":
            commands.append(event["command"])
        elif method == "rawResponseItem/completed":
            item = params.get("item", {})
            if item.get("type") in {"function_call", "custom_tool_call"}:
                pending.setdefault(key, []).append(item["call_id"])
        elif method == "rawResponse/completed":
            if isinstance(params.get("usage"), dict):
                raw_usage[(thread, params["responseId"])] = params["usage"][
                    "totalTokens"
                ]
            for call in pending.pop(key, []):
                groups[call] = (thread, params["responseId"])
        elif method == "thread/tokenUsage/updated":
            usage[thread] = params["tokenUsage"]["total"]
        elif method in {"item/started", "item/completed"}:
            item = params.get("item", {})
            if item.get("type") == "collabAgentToolCall":
                if item.get("tool") in START_TOOLS and item.get("prompt"):
                    held = starts.get(item["id"])
                    starts[item["id"]] = (held[0] if held else index, item)
                if method == "item/completed":
                    for agent, state in item.get("agentsStates", {}).items():
                        if state.get("status") == "completed" and isinstance(
                            state.get("message"), str
                        ):
                            reports.setdefault(agent, []).append(
                                (index, state["message"])
                            )
                            if item.get("tool") == "wait":
                                waited.setdefault(agent, set()).add(index)
            elif (
                method == "item/completed"
                and item.get("type") == "agentMessage"
                and item.get("phase") == FINAL
            ):
                reports.setdefault(thread, []).append((index, item["text"]))
                turn_text[key] = item["text"]
                if thread == root:
                    final = item["text"]
        elif method == "turn/completed" and thread == root:
            status = params["turn"]["status"]
            turn_error = params["turn"].get("error")
    made = []
    last_group: dict[str, tuple[str, str]] = {}
    child_threads: set[str] = set()
    ordered = sorted(starts.items(), key=lambda entry: entry[1][0])
    for identifier, (position, item) in ordered:
        receivers = item.get("receiverThreadIds", [])
        if item.get("status") != "completed" or not receivers:
            continue
        if identifier not in groups:
            raise ProtocolError(
                f"dispatch {identifier} has no native response boundary"
            )
        group = groups[identifier]
        returned = []
        for agent in receivers:
            child_threads.add(agent)
            next_start = next(
                (
                    later
                    for _, (later, call) in ordered
                    if later > position and agent in call.get("receiverThreadIds", [])
                ),
                len(events),
            )
            child_turn = next(
                (
                    key
                    for key, first in turn_first.items()
                    if key[0] == agent and position <= first < next_start
                ),
                None,
            )
            ended = turn_done.get(child_turn) if child_turn is not None else None
            complete_reports = [
                (at, text)
                for at, text in reports.get(agent, [])
                if position <= at < next_start
            ]
            if ended is None:
                if any(at in waited.get(agent, set()) for at, _ in complete_reports):
                    raise ProtocolError(
                        "a completed child report has no native completed-turn evidence"
                    )
                report = None
            else:
                report = next(
                    (text for at, text in complete_reports if ended <= at < next_start),
                    turn_text.get(child_turn, "") if child_turn is not None else "",
                )
            lines = (
                [line.strip() for line in report.splitlines() if line.strip()]
                if report is not None
                else []
            )
            returned.append(
                "unfinished"
                if report is None
                else "question"
                if lines and lines[0].startswith("Question:")
                else "done"
            )
        disposition = (
            "unfinished"
            if "unfinished" in returned
            else "question"
            if "question" in returned
            else "done"
        )
        made.append(
            {
                "target": item["prompt"],
                "returned": disposition,
                "together": group == last_group.get(group[0]),
                "actor": group[0],
                "group": group[1],
            }
        )
        last_group[group[0]] = group
    observed = {root, *child_threads}
    missing = observed - usage.keys()
    if (
        missing
        and status == "completed"
        and not any(start["returned"] == "unfinished" for start in made)
    ):
        raise ProtocolError(
            f"{len(missing)} thread(s) have no native cumulative token usage"
        )
    tokens = (
        None
        if missing or any(start["returned"] == "unfinished" for start in made)
        else sum(usage[thread]["totalTokens"] for thread in observed)
    )
    raw_tokens = (
        sum(raw_usage.values())
        if {thread for thread, _ in raw_usage} == observed
        else None
    )
    if tokens is not None and raw_tokens is not None and tokens != raw_tokens:
        raise ProtocolError(
            "native response tokens disagree with cumulative thread tokens"
        )
    return {
        "type": "result",
        "harness": "codex",
        "result": str(turn_error) if turn_error else final,
        "is_error": status not in {"completed", "interrupted"},
        "usage": {
            "threads": len(observed),
            "totalTokens": tokens,
            "rawResponseTokens": raw_tokens,
        },
        "tokens": tokens,
        "starts": made,
        "commands": commands,
    }


class Bridge:
    """One ephemeral native thread and the protocol requests it needs."""

    def __init__(
        self, command: list[str], model: str, effort: str, budget: int
    ) -> None:
        self.command = command
        self.model = model
        self.effort = effort
        self.budget = budget
        self.root = Path.cwd().resolve()
        self.events: list[dict[str, Any]] = []
        self.pending: dict[int, tuple[str, Any]] = {}
        self.next_id = 0
        self.thread: str | None = None
        self.children: set[str] = set()
        self.turns: dict[str, str] = {}
        self.usage: dict[str, int] = {}
        self.interrupted = False

    def emit(self, event: dict[str, Any]) -> None:
        self.events.append(event)
        print(json.dumps(event), flush=True)

    def send(self, message: dict[str, Any]) -> None:
        assert self.process.stdin is not None
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()
        self.emit({"type": "codex_request", "message": message})

    def request(
        self, kind: str, method: str, params: dict[str, Any], data: Any = None
    ) -> None:
        self.next_id += 1
        self.pending[self.next_id] = (kind, data)
        self.send({"id": self.next_id, "method": method, "params": params})

    def tool_result(self, identifier: int | str, text: str, success: bool) -> None:
        self.send(
            {
                "id": identifier,
                "result": {
                    "contentItems": [{"type": "inputText", "text": text}],
                    "success": success,
                },
            }
        )

    def thread_start(self) -> None:
        config: dict[str, Any] = {**CONFIG, "model_reasoning_effort": self.effort}
        self.request(
            "thread",
            "thread/start",
            {
                "model": self.model,
                "allowProviderModelFallback": False,
                "cwd": str(self.root),
                "runtimeWorkspaceRoots": [str(self.root)],
                "approvalPolicy": "never",
                "sandbox": "workspace-write",
                "ephemeral": True,
                "experimentalRawEvents": True,
                "config": config,
                "environments": [],
                "dynamicTools": TOOLS,
            },
        )

    def subscribed(self, result: dict[str, Any]) -> None:
        if result.get("model") != self.model:
            raise ProtocolError("Codex selected a model other than the requested model")
        if any(
            not Path(path).resolve().is_relative_to(self.root)
            for path in result.get("instructionSources", [])
        ):
            raise ProtocolError(
                "Codex loaded instructions outside the prepared workspace"
            )

    def handle_tool(self, event: dict[str, Any]) -> None:
        params = event["params"]
        arguments = params.get("arguments")
        if not isinstance(arguments, dict):
            self.tool_result(event["id"], "Tool arguments must be an object.", False)
            return
        try:
            if params["tool"] != "pf":
                text = file_tool(self.root, params["tool"], arguments)
                self.tool_result(event["id"], text, True)
                return
            if not isinstance(arguments.get("args"), list) or not all(
                isinstance(arg, str) for arg in arguments["args"]
            ):
                raise ValueError("pf arguments must be a list of strings")
            directory = workspace_path(self.root, arguments.get("cwd") or ".")
            for stream in ("stdout", "stderr"):
                if arguments.get(stream) is not None:
                    workspace_path(self.root, str(directory / arguments[stream]))
            if arguments.get("stderr") is not None and arguments.get(
                "stderr_to_stdout"
            ):
                raise ValueError("stderr names either a file or stdout")
            build = shutil.which("pf")
            if build is None:
                raise ValueError("no pf command is on the session path")
            self.request(
                "pf",
                "command/exec",
                {
                    "command": [build, *arguments["args"]],
                    "cwd": str(directory),
                    "sandboxPolicy": policy(self.root),
                    "disableOutputCap": True,
                    "timeoutMs": 60_000,
                },
                (
                    event["id"],
                    params["threadId"],
                    params["callId"],
                    arguments,
                    directory,
                ),
            )
        except (OSError, ValueError, KeyError, TypeError) as error:
            self.tool_result(event["id"], str(error), False)

    def pf_result(
        self,
        result: dict[str, Any],
        data: tuple[int | str, str, str, dict[str, Any], Path],
    ) -> None:
        identifier, thread, call, arguments, directory = data
        self.emit(
            {
                "type": "pf",
                "threadId": thread,
                "callId": call,
                "cwd": str(directory.relative_to(self.root)),
                "command": pf_command(arguments),
                "exit_status": result["exitCode"],
            }
        )
        streams = {key: result[key] for key in ("stdout", "stderr")}
        if arguments.get("stderr_to_stdout"):
            streams["stdout"] += streams["stderr"]
            streams["stderr"] = ""
        try:
            for stream, text in streams.items():
                if arguments.get(stream) is not None:
                    path = workspace_path(self.root, str(directory / arguments[stream]))
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with path.open("a" if arguments.get("append") else "w") as output:
                        output.write(text)
                    streams[stream] = ""
            self.tool_result(
                identifier,
                json.dumps({"exit_code": result["exitCode"], **streams}),
                result["exitCode"] == 0,
            )
        except (OSError, ValueError) as error:
            self.tool_result(identifier, str(error), False)

    def response(self, event: dict[str, Any], prompt: str) -> None:
        kind, data = self.pending.pop(event["id"])
        if "error" in event:
            if kind == "config":
                raise ProtocolError("Codex configuration readback was refused")
            if kind == "pf":
                self.tool_result(data[0], json.dumps(event["error"]), False)
                return
            raise ProtocolError(f"Codex {kind} refused: {event['error']}")
        result = event["result"]
        if kind == "initialize":
            self.send({"method": "initialized"})
            self.request(
                "config", "config/read", {"includeLayers": True, "cwd": str(self.root)}
            )
        elif kind == "config":
            self.emit(
                configuration(
                    result, self.root, Path(os.environ["CODEX_HOME"]).resolve()
                )
            )
            self.thread_start()
        elif kind == "thread":
            self.subscribed(result)
            self.thread = result["thread"]["id"]
            self.request(
                "turn",
                "turn/start",
                {
                    "threadId": self.thread,
                    "input": [{"type": "text", "text": prompt, "text_elements": []}],
                    "effort": self.effort,
                    "sandboxPolicy": policy(self.root),
                    "environments": [],
                },
            )
        elif kind == "subscribe":
            self.subscribed(result)
        elif kind == "pf":
            self.pf_result(result, data)

    def notice(self, event: dict[str, Any]) -> bool:
        method = event.get("method")
        params = event.get("params", {})
        thread = params.get("threadId")
        if method in {"hook/started", "hook/completed"}:
            raise ProtocolError("Codex carried a hook the eval did not supply")
        if method in {"item/started", "item/completed"}:
            item = params.get("item", {})
            if item.get("type") == "collabAgentToolCall":
                if item.get("model") not in {None, self.model}:
                    raise ProtocolError("a sub-agent selected another model")
                for child in item.get("receiverThreadIds", []):
                    if child not in self.children and child != self.thread:
                        self.children.add(child)
                        self.request(
                            "subscribe",
                            "thread/resume",
                            {"threadId": child, "excludeTurns": True},
                        )
        if thread and params.get("turnId"):
            self.turns[thread] = params["turnId"]
        if method == "thread/tokenUsage/updated":
            self.usage[thread] = params["tokenUsage"]["total"]["totalTokens"]
            if not self.interrupted and sum(self.usage.values()) >= self.budget:
                self.interrupted = True
                for agent, turn in self.turns.items():
                    self.request(
                        "interrupt",
                        "turn/interrupt",
                        {"threadId": agent, "turnId": turn},
                    )
        return method == "turn/completed" and thread == self.thread

    def run(self, prompt: str) -> int:
        command = [*self.command, "app-server", "--strict-config"]
        for feature in DISABLED:
            command.extend(["--disable", feature])
        for key, value in CONFIG.items():
            command.extend(["--config", f"{key}={json.dumps(value)}"])
        self.process = Popen(
            command, stdin=PIPE, stdout=PIPE, stderr=sys.stderr, text=True, bufsize=1
        )
        result: dict[str, Any]
        try:
            self.request(
                "initialize",
                "initialize",
                {
                    "clientInfo": {"name": "prosiform_eval", "version": "1"},
                    "capabilities": {
                        "experimentalApi": True,
                        "requestAttestation": False,
                    },
                },
            )
            assert self.process.stdout is not None
            for line in self.process.stdout:
                event = json.loads(line)
                if self.pending.get(event.get("id"), (None,))[0] != "config":
                    self.emit(event)
                if "id" in event and "method" not in event:
                    self.response(event, prompt)
                elif event.get("method") == "item/tool/call":
                    self.handle_tool(event)
                elif "id" in event:
                    raise ProtocolError(
                        f"Codex requested unsupported {event.get('method')}"
                    )
                elif self.notice(event):
                    break
            else:
                raise ProtocolError("Codex ended without completing the root turn")
            if self.thread is None:
                raise ProtocolError("Codex created no root thread")
            result = summarize(self.events, self.thread)
            if self.interrupted:
                result["result"] = "The session reached its token cap."
        except (OSError, ValueError, KeyError, TypeError) as error:
            result = {
                "type": "result",
                "harness": "codex",
                "is_error": True,
                "result": str(error),
                "tokens": None,
                "starts": [],
                "commands": [],
            }
        finally:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except TimeoutExpired:
                self.process.kill()
                self.process.wait()
        self.emit(result)
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--command", required=True, help="the native Codex argv as JSON"
    )
    parser.add_argument("--model", required=True)
    parser.add_argument("--reasoning-effort", required=True)
    parser.add_argument("--session-budget-tokens", required=True, type=int)
    arguments = parser.parse_args()
    return Bridge(
        json.loads(arguments.command),
        arguments.model,
        arguments.reasoning_effort,
        arguments.session_budget_tokens,
    ).run(sys.stdin.read())


if __name__ == "__main__":
    sys.exit(main())
