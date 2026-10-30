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

from workflow import CorpusError

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
SHELL_CALL = "shellToolCall"
COMMAND = "command"
OPENCODE_PART = "part"
OPENCODE_TOOL = "tool"
"""The part type a session's tool call carries, as distinct from its text."""
STEP_FINISH = "step_finish"
TOKENS = "tokens"
CACHE = "cache"
COST = "cost"
STATE = "state"
INPUT = "input"
OPENCODE_CALL_ID = "callID"
OPENCODE_MESSAGE_ID = "messageID"
BASH = "bash"
TASK_TOOL = "task"
"""The opencode tool whose call hands a section to a sub-agent."""
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
    settings: str = "settings.json"
    hooks: str = "hooks"
    default_agent: str = "claude"
    tools: str = "Read,Write,Edit,Glob,Grep,Task"
    shell: bool = False
    """Whether a session may run a command, which a shell form needs.

    The tool allowlist above names no shell, so this harness cannot run one.
    A form whose material a session must compile cannot be measured here.
    """
    prompt_on_argv: bool = False
    """Whether the task text is an argument rather than the session's input."""
    nested_starts: bool = True
    """Whether a sub-agent's own dispatch reaches the parent's transcript."""
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

    def argv(
        self, agent: list[str], model: str, budget: int, workspace: Path | None = None
    ) -> list[str]:
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
        declared = config / self.settings
        hooks = _record(declared).get(self.hooks)
        if isinstance(hooks, dict):
            events = sorted(str(event) for event, commands in hooks.items() if commands)
            if events:
                return (
                    f"{declared} declares a hook for {', '.join(events)}, which "
                    f"reaches every session before its first turn; remove "
                    f"{declared} before this run"
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

    def commands(self, transcript: Path) -> tuple[str, ...] | None:
        """The shell commands a session ran, or nothing where it can run none."""
        return None

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
    shell: bool = True
    """Whether a session may run a command, which a shell form needs.

    The CLI carries a shell, so a session can compile its material. The
    command it runs is confined by workspace trust alone, which is wider than
    a form that only reads files needs.
    """
    prompt_on_argv: bool = False
    """Whether the task text is an argument rather than the session's input."""
    nested_starts: bool = False
    """Whether a sub-agent's own dispatch reaches the parent's transcript.

    It does not: the CLI reports a sub-agent's final text and the steps it
    took, and no tool call it made. A scenario whose trace names a start
    made inside a sub-agent cannot be observed on this harness.
    """
    usage: tuple[str, str, str, str] = (
        "inputTokens",
        "outputTokens",
        "cacheWriteTokens",
        "cacheReadTokens",
    )

    def argv(
        self, agent: list[str], model: str, budget: int, workspace: Path | None = None
    ) -> list[str]:
        """One session's command line, the workspace given as its argument.

        The CLI has no session spend cap and no tool allowlist, so the run's
        own token guard is the whole budget, and the workspace the run laid
        out is what a session is confined to.

        A workspace must be trusted for the CLI to run in it at all, since
        it prompts otherwise and a prompt is no session. `--sandbox` is left
        unset: the CLI's sandbox is unavailable on some hosts and refuses
        every session there, so a run states the trust it gives rather than
        an isolation it may silently lack.
        """
        return [
            *agent,
            "-p",
            "--model",
            model,
            "--output-format",
            "stream-json",
            "--trust",
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
        """What a run under this harness cannot guarantee, stated as a refusal.

        The CLI declares no configuration directory, no MCP switch, no
        slash-command switch and no session spend cap, and it runs only in a
        workspace it is told to trust. A run therefore draws no isolation
        boundary beyond the workspace itself, and this harness refuses to
        pretend otherwise: the caller names the config directory it means as
        the boundary and accepts that a session shares the caller's
        configuration.
        """
        if not config.is_dir():
            return (
                f"{config} is no directory; this harness reads the caller's "
                f"configuration and trusts its workspace, so name an eval root "
                f"whose config records that boundary"
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

        Only the starts a session made itself are readable: a sub-agent's own
        stream is not part of its parent's transcript, so a dispatch nested
        inside a sub-agent leaves its parent's record silent about it. A
        scenario stating such a start is beyond what this harness reports,
        which `observes` states.
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

    def commands(self, transcript: Path) -> tuple[str, ...]:
        """The shell commands a session ran, in order.

        A `shellToolCall` carries the command line it ran. A session whose
        material must be compiled with a command is held to having run it,
        so what the stream states about commands is read rather than assumed.
        """
        found: list[str] = []
        for held in messages(transcript):
            if held.get("type") != TOOL_CALL:
                continue
            held_call = held.get(TOOL_CALL)
            tool = held_call.get(SHELL_CALL) if isinstance(held_call, dict) else None
            if not isinstance(tool, dict):
                continue
            args = tool.get(ARGS)
            command = args.get(COMMAND) if isinstance(args, dict) else None
            if held.get("subtype") == STARTED and isinstance(command, str):
                found.append(command)
        return tuple(found)

    def tokens(self, result: dict[str, object] | None) -> int | None:
        """The tokens one session processed, from the usage it reported."""
        return _tokens(result, self.usage)

    def cost(self, result: dict[str, object] | None) -> float | None:
        """The cost a session reported, which this harness does not."""
        return None


def _record(path: Path) -> dict[str, object]:
    """One settings file read as JSON, or nothing where it is absent.

    A file present but unreadable is refused rather than read as empty: an
    empty answer would let a hook it declares reach a session unobserved.
    """
    if not path.is_file():
        return {}
    try:
        held = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        raise CorpusError(f"{path} is not JSON: {error}") from error
    return held if isinstance(held, dict) else {}


@dataclass(frozen=True)
class Opencode:
    """The opencode CLI: `run` with a stream of parts.

    A session prints one JSON object a line, each holding a `part` whose
    `type` names what happened. A tool a session ran is a `tool_use` part,
    distinct from an assistant message, so a start and a command are read from
    what the session did rather than from prose. Tokens and cost are reported
    on each `step_finish` part and summed over the session.
    """

    name: str = "opencode"
    config_variable: str = "OPENCODE_CONFIG_DIR"
    scrubbed: tuple[str, ...] = ("OPENCODE",)
    default_agent: str = "~/.opencode/bin/opencode"
    """Where the CLI installs itself, which is not on a login shell's path."""
    tools: str = ""
    shell: bool = True
    """Whether a session may run a command, which a shell form needs.

    The CLI carries a shell, so a session can compile its material.
    """
    prompt_on_argv: bool = True
    """Whether the task text is an argument rather than the session's input.

    The CLI reads its prompt from its arguments, so a run appends it there.
    A prompt written to its input instead is read by nothing.
    """
    nested_starts: bool = True
    """Whether a sub-agent's own dispatch reaches the parent's stream.

    It does: a session's `tool_use` parts include those its sub-agents made,
    so a trace naming a nested start is observable here.
    """
    usage: tuple[str, str, str, str] = ("input", "output", "cache", "cache")

    def argv(
        self, agent: list[str], model: str, budget: int, workspace: Path | None = None
    ) -> list[str]:
        """One session's command line, its prompt given as its argument.

        The CLI prints one JSON object a line, so a session's parts are read
        rather than its prose. It has no session spend cap, so the run's token
        guard is the whole budget.

        `--auto` approves what the CLI would otherwise prompt for. Without it
        a non-interactive run rejects every permission it asks, so a session
        writes nothing and the cell would record the refusal as the agent's
        failure.

        `--dir` names the workspace outright. The CLI otherwise takes its
        project from remembered state as readily as from its working
        directory, and a session that names no workspace of its own can run
        in the repository this file was written in.
        """
        return [
            *agent,
            "run",
            "--format",
            "json",
            "--model",
            model,
            "--auto",
            "--dir",
            str(workspace) if workspace else ".",
        ]

    def environment(self, config: Path, held: dict[str, str]) -> dict[str, str]:
        """The caller's environment without its agent variables."""
        return {
            name: value
            for name, value in held.items()
            if not name.startswith(self.scrubbed)
        }

    def preflight(self, config: Path) -> str | None:
        """What this harness cannot guarantee, stated as a refusal.

        The CLI has no configuration directory of its own and reads plugins
        from the caller's installation, so a session is confined by its
        working directory alone.
        """
        if not config.is_dir():
            return (
                f"{config} is no directory; this harness reads the caller's "
                f"configuration, so name an eval root whose config records that"
            )
        return None

    def result(self, transcript: Path) -> dict[str, object] | None:
        """The session's last step, holding what it reported spending.

        The CLI prints no closing `result` message, so the last `step_finish`
        part is the session's last word on what it did.
        """
        found = None
        for held in messages(transcript):
            if held.get("type") == STEP_FINISH:
                found = held
        return found

    def starts(self, transcript: Path) -> tuple[Start, ...]:
        """The sub-agents a session started, in order.

        A `tool_use` part naming `task` is one start; its input's
        `description` is the text the dispatching call carried. Two starts
        sharing a `messageID` were dispatched in one message.
        """
        found: list[tuple[str, str, bool]] = []
        seen: set[str] = set()
        for held in messages(transcript):
            part = held.get(OPENCODE_PART)
            if not isinstance(part, dict) or part.get("type") != OPENCODE_TOOL:
                continue
            if part.get("tool") != TASK_TOOL:
                continue
            state = part.get(STATE)
            carried_input = state.get(INPUT) if isinstance(state, dict) else None
            target = (
                carried_input.get(DESCRIPTION)
                if isinstance(carried_input, dict)
                else None
            )
            key = part.get(OPENCODE_CALL_ID)
            message = part.get(OPENCODE_MESSAGE_ID)
            if not isinstance(target, str) or not isinstance(key, str):
                continue
            together = isinstance(message, str) and message in seen
            seen.add(message if isinstance(message, str) else key)
            found.append((key, target, together))
        return tuple(Start(target, DONE, together) for _, target, together in found)

    def commands(self, transcript: Path) -> tuple[str, ...]:
        """The shell commands a session ran, in order."""
        found: list[str] = []
        for held in messages(transcript):
            part = held.get(OPENCODE_PART)
            if not isinstance(part, dict) or part.get("type") != OPENCODE_TOOL:
                continue
            if part.get("tool") != BASH:
                continue
            state = part.get(STATE)
            carried_input = state.get(INPUT) if isinstance(state, dict) else None
            command = (
                carried_input.get(COMMAND) if isinstance(carried_input, dict) else None
            )
            if isinstance(command, str):
                found.append(command)
        return tuple(found)

    def tokens(self, result: dict[str, object] | None) -> int | None:
        """The tokens one session processed, summed over its steps."""
        if result is None:
            return None
        part = result.get(OPENCODE_PART)
        tokens = part.get(TOKENS) if isinstance(part, dict) else None
        if not isinstance(tokens, dict):
            return None
        counts = [tokens.get(kind) for kind in ("input", "output", "reasoning")]
        cache = tokens.get(CACHE)
        if isinstance(cache, dict):
            counts += [cache.get("write"), cache.get("read")]
        if not any(isinstance(count, int | float) for count in counts):
            return None
        return int(sum(count for count in counts if isinstance(count, int | float)))

    def cost(self, result: dict[str, object] | None) -> float | None:
        """The cost the session reported, in USD."""
        if result is None:
            return None
        part = result.get(OPENCODE_PART)
        cost = part.get(COST) if isinstance(part, dict) else None
        return float(cost) if isinstance(cost, int | float) else None


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


Harness = Claude | Cursor | Opencode
"""Any declared harness, as the runner and the scorer accept one."""

HARNESSES = {harness.name: harness for harness in (Claude(), Cursor(), Opencode())}


def harness_named(name: str) -> Harness:
    """The declared harness with the supplied name."""
    if name not in HARNESSES:
        raise KeyError(f"the harnesses are {', '.join(HARNESSES)}, not {name}")
    return HARNESSES[name]
