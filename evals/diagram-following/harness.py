"""The agent CLI one eval session runs, and what its stream says.

A harness names the command line that starts one headless session, the
environment and preflight its isolation rests on, and how its stream records
a sub-agent start, a session's end and the tokens it spent. The run's matrix,
workspaces, budget, timeout and scoring are the same for every harness, so
the harness is the whole of what an agent CLI differs in.

Two harnesses are declared:

- `claude`, the Claude Code CLI, whose session stream is a sequence of
  `assistant` and `user` messages carrying `tool_use` and `tool_result`
  blocks, and whose last message carries `total_cost_usd`;
- `cursor`, the Cursor agent CLI, whose stream is `tool_call` events
  carrying `taskToolCall`, whose two starts in one message share a
  `model_call_id`, and which reports tokens but no cost.

A harness reads its own stream: `starts()` returns the same `Start` values
from either, so the scorer above it is unaware of which CLI produced them.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

QUESTION = "question"
DONE = "done"

MESSAGE = "message"
ASSISTANT = "assistant"
USER = "user"
TOOL_USE = "tool_use"
TOOL_RESULT = "tool_result"
CALL_ID = "tool_use_id"
TASK = "Task"
DESCRIPTION = "description"
RESULT = "result"
IS_ERROR = "is_error"
USAGE = "usage"

TOOL_CALL = "tool_call"
STARTED = "started"
COMPLETED = "completed"
TASK_CALL = "taskToolCall"
MODEL_CALL = "model_call_id"
ARGS = "args"
CONVERSATION = "conversationSteps"
ASSISTANT_MESSAGE = "assistantMessage"
TEXT = "text"

CLAUDE_USAGE = {
    "input": "input_tokens",
    "output": "output_tokens",
    "cache_creation": "cache_creation_input_tokens",
    "cache_read": "cache_read_input_tokens",
}
CURSOR_USAGE = {
    "input": "inputTokens",
    "output": "outputTokens",
    "cache_creation": "cacheWriteTokens",
    "cache_read": "cacheReadTokens",
}


@dataclass(frozen=True)
class Start:
    """One sub-agent start a session's transcript records.

    `target` is the text the dispatching call carried, naming the section it
    handed over; `returned` is what the sub-agent gave back, and `together`
    says whether it started in the same message as the start above it.
    """

    target: str
    returned: str
    together: bool

    def record(self) -> dict[str, object]:
        """The start as plain values `json.dumps` writes unchanged."""
        return asdict(self)


def messages(transcript: Path) -> list[dict[str, object]]:
    """Every JSON object a stream wrote, skipping a line that is not one."""
    if not transcript.is_file():
        return []
    found = []
    for line in transcript.read_text().splitlines():
        try:
            held = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(held, dict):
            found.append(held)
    return found


def said(text: object) -> str:
    """What a returned block states, as `question` or `done`."""
    if isinstance(text, list):
        text = " ".join(part.get(TEXT, "") for part in text if isinstance(part, dict))
    held = text.strip().lower() if isinstance(text, str) else ""
    return QUESTION if held.startswith(QUESTION) else DONE


@dataclass(frozen=True)
class Claude:
    """The Claude Code CLI: `-p` with a stream-json session stream."""

    name: str = "claude"
    config_variable: str = "CLAUDE_CONFIG_DIR"
    scrubbed: tuple[str, ...] = ("CLAUDE", "ANTHROPIC_")
    login: str = ".credentials.json"
    plugins: str = "plugins/installed_plugins.json"
    remote: str = "remote-settings.json"
    enabled: str = "enabledPlugins"
    default_agent: str = "claude"
    tools: str = "Read,Write,Edit,Glob,Grep,Task"
    session_cap_usd: float = 0.50
    """The price the CLI itself may spend in one session.

    The CLI caps dollars between calls and reports no token ceiling, so a
    run's token budget is held by the run's own guard and this figure holds
    what the CLI alone could spend before that guard sees a result.
    """
    usage: tuple[str, str, str, str] = (
        "input_tokens",
        "output_tokens",
        "cache_creation_input_tokens",
        "cache_read_input_tokens",
    )

    def argv(self, agent: list[str], model: str, budget: int) -> list[str]:
        """One session's command line, its prompt given on standard input.

        A token budget is not a dollar cap, so `--max-budget-usd` is given the
        price a session is allowed to spend rather than the token count: the
        CLI enforces dollars between calls, and the run's own guard holds the
        token budget from what each session reports.
        """
        return [
            *agent,
            "-p",
            "--model",
            model,
            "--output-format",
            "stream-json",
            "--verbose",
            "--tools",
            self.tools,
            "--permission-mode",
            "acceptEdits",
            "--no-session-persistence",
            "--strict-mcp-config",
            "--disable-slash-commands",
            "--max-budget-usd",
            str(self.session_cap_usd),
        ]

    def environment(self, config: Path, held: dict[str, str]) -> dict[str, str]:
        """The caller's environment without its agent variables, naming `config`."""
        kept = {
            name: value
            for name, value in held.items()
            if not name.startswith(self.scrubbed)
        }
        return {**kept, self.config_variable: str(config)}

    def preflight(self, config: Path) -> str | None:
        """How a configuration directory fails to isolate a session, if it does."""
        if not (config / self.login).is_file():
            return (
                f"{config} holds no login; log in once with "
                f"`{self.config_variable}={config} claude`, then `/login`"
            )
        installing = config / self.plugins
        if _record(installing).get("plugins"):
            return (
                f"{installing} installs a plugin, whose hooks reach every session "
                f"before its first turn; remove {installing} before this run"
            )
        enabling = config / self.remote
        enabled = _record(enabling).get(self.enabled)
        if isinstance(enabled, dict) and any(
            value is True for value in enabled.values()
        ):
            return (
                f"{enabling} enables a plugin and its environment, which reach "
                f"every session before its first turn; remove {enabling}"
            )
        return None

    def result(self, transcript: Path) -> dict[str, object] | None:
        """The session's last `result` message, if it printed one."""
        found = None
        for held in messages(transcript):
            if held.get("type") == RESULT:
                found = held
        return found

    def starts(self, transcript: Path) -> tuple[Start, ...]:
        """The sub-agents a session started, in order.

        A `tool_use` block naming `Task` is one start; two such blocks in one
        assistant message started together. A start's target is the
        `description` its input carries, naming the section handed over.
        """
        found: dict[str, tuple[str, bool]] = {}
        returned: dict[str, str] = {}
        for held in messages(transcript):
            kind = held.get("type")
            carried = held.get(MESSAGE)
            content = carried.get("content") if isinstance(carried, dict) else None
            if not isinstance(content, list):
                continue
            if kind == ASSISTANT:
                first = None
                for block in content:
                    if not isinstance(block, dict) or block.get("type") != TOOL_USE:
                        continue
                    if block.get("name") != TASK:
                        continue
                    held_input = block.get("input")
                    target = (
                        held_input.get(DESCRIPTION)
                        if isinstance(held_input, dict)
                        else None
                    )
                    key = block.get("id")
                    if not isinstance(key, str) or not isinstance(target, str):
                        continue
                    found[key] = (target, first is not None)
                    if first is None:
                        first = key
            elif kind == USER:
                for block in content:
                    if not isinstance(block, dict) or block.get("type") != TOOL_RESULT:
                        continue
                    key = block.get(CALL_ID)
                    if isinstance(key, str):
                        returned[key] = said(block.get("content"))
        return tuple(
            Start(target, returned.get(key, DONE), together)
            for key, (target, together) in found.items()
        )

    def tokens(self, result: dict[str, object] | None) -> int | None:
        """The tokens one session processed, from the usage it reported."""
        return _tokens(result, self.usage)

    def cost(self, result: dict[str, object] | None) -> float | None:
        """The cost the session reported, in USD."""
        if result is None:
            return None
        held = result.get("total_cost_usd")
        return float(held) if isinstance(held, int | float) else None


@dataclass(frozen=True)
class Cursor:
    """The Cursor agent CLI: `-p` with a stream-json session stream."""

    name: str = "cursor"
    config_variable: str = "CURSOR_CONFIG_DIR"
    scrubbed: tuple[str, ...] = ("CURSOR",)
    default_agent: str = "cursor-agent"
    tools: str = ""
    usage: tuple[str, str, str, str] = (
        "inputTokens",
        "outputTokens",
        "cacheWriteTokens",
        "cacheReadTokens",
    )

    def argv(self, agent: list[str], model: str, budget: int) -> list[str]:
        """One session's command line, its prompt given as its argument.

        The CLI has no session spending cap and no tool allowlist, so the
        run's own token guard is the whole budget, and the workspace and
        sandbox are what confine a session: `--sandbox enabled` and a
        workspace the run laid out. `--trust` is withheld, since trusting a
        workspace is what the eval's isolation exists to avoid.
        """
        return [
            *agent,
            "-p",
            "--model",
            model,
            "--output-format",
            "stream-json",
            "--sandbox",
            "enabled",
        ]

    def environment(self, config: Path, held: dict[str, str]) -> dict[str, str]:
        """The caller's environment without its agent variables.

        The CLI reads its own configuration from a fixed location and names
        no variable for it, so `config` is carried for the record and no
        variable is set from it.
        """
        return {
            name: value
            for name, value in held.items()
            if not name.startswith(self.scrubbed)
        }

    def preflight(self, config: Path) -> str | None:
        """How this harness fails to isolate a session, if it does.

        The CLI declares no configuration directory, no MCP server switch and
        no slash-command switch, so a session shares the caller's
        configuration and may load its plugins. A run whose isolation rests
        on those is refused rather than reported as though they held.
        """
        if not config.is_dir():
            return (
                f"{config} is no directory; the cursor harness reads the caller's "
                f"configuration, so name an eval root whose config marks the boundary"
            )
        return None

    def result(self, transcript: Path) -> dict[str, object] | None:
        """The session's last `result` message, if it printed one."""
        found = None
        for held in messages(transcript):
            if held.get("type") == RESULT:
                found = held
        return found

    def starts(self, transcript: Path) -> tuple[Start, ...]:
        """The sub-agents a session started, in order.

        A `tool_call` whose `taskToolCall` started is one start, and two
        sharing a `model_call_id` were dispatched in one message. A start's
        target is the `description` in its args; what it returned is the
        text of the completed call's `conversationSteps`.
        """
        found: list[tuple[str, str, bool]] = []
        returned: dict[str, str] = {}
        seen: dict[str, str] = {}
        for held in messages(transcript):
            if held.get("type") != TOOL_CALL:
                continue
            call = held.get(TOOL_CALL)
            if not isinstance(call, dict):
                continue
            task = call.get(TASK_CALL)
            if not isinstance(task, dict):
                continue
            key = call.get("toolCallId") or held.get("call_id")
            if not isinstance(key, str):
                continue
            if held.get("subtype") == STARTED:
                carried_args = task.get(ARGS)
                args = carried_args if isinstance(carried_args, dict) else {}
                target = args.get(DESCRIPTION)
                if not isinstance(target, str):
                    continue
                carried_message = held.get(MODEL_CALL)
                message = carried_message if isinstance(carried_message, str) else ""
                together = message in seen
                seen[message] = key
                found.append((key, target, together))
            elif held.get("subtype") == COMPLETED:
                carried_result = task.get(RESULT)
                result = carried_result if isinstance(carried_result, dict) else {}
                success = result.get("success")
                carried_steps = (
                    success.get(CONVERSATION) if isinstance(success, dict) else None
                )
                steps = carried_steps if isinstance(carried_steps, list) else []
                texts: list[str] = []
                for step in steps:
                    if not isinstance(step, dict):
                        continue
                    carried_message = step.get(ASSISTANT_MESSAGE)
                    if isinstance(carried_message, dict):
                        text = carried_message.get(TEXT)
                        if isinstance(text, str):
                            texts.append(text)
                returned[key] = said(" ".join(texts))
        return tuple(
            Start(target, returned.get(key, DONE), together)
            for key, target, together in found
        )

    def tokens(self, result: dict[str, object] | None) -> int | None:
        """The tokens one session processed, from the usage it reported."""
        return _tokens(result, self.usage)

    def cost(self, result: dict[str, object] | None) -> float | None:
        """The cost a session reported, which this harness does not."""
        return None


def _record(path: Path) -> dict[str, object]:
    """One settings file read as JSON, or nothing where it is absent or unreadable."""
    if not path.is_file():
        return {}
    try:
        held = json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}
    return held if isinstance(held, dict) else {}


def _tokens(
    result: dict[str, object] | None, fields: tuple[str, str, str, str]
) -> int | None:
    """The sum of one session's usage fields, or nothing where it reported none."""
    if result is None:
        return None
    usage = result.get(USAGE)
    if not isinstance(usage, dict):
        return None
    counts = [usage.get(name) for name in fields]
    if not any(isinstance(count, int | float) for count in counts):
        return None
    return int(sum(count for count in counts if isinstance(count, int | float)))


HARNESSES = {harness.name: harness for harness in (Claude(), Cursor())}


def harness_named(name: str) -> Claude | Cursor:
    """The declared harness with the supplied name."""
    if name not in HARNESSES:
        raise KeyError(f"the harnesses are {', '.join(HARNESSES)}, not {name}")
    return HARNESSES[name]
