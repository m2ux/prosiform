"""The agent CLI one eval session runs, and what its stream says.

A harness names the command line that starts one headless session, the
environment and preflight its isolation rests on, and how its stream records
a sub-agent start, a session's end and the tokens it spent. The run's matrix,
workspaces, budget, timeout and scoring are the same for every harness, so
the harness is the whole of what an agent CLI differs in.

`HARNESSES` declares three:

- `claude`, the Claude Code CLI, whose session stream is a sequence of
  `assistant` and `user` messages carrying `tool_use` and `tool_result`
  blocks, and whose last message carries `total_cost_usd`;
- `cursor`, the Cursor agent CLI, whose stream is `tool_call` events
  carrying `taskToolCall`, whose two starts in one message share a
  `model_call_id`, and which reports tokens but no cost;
- `opencode`, the opencode CLI, whose stream is events each holding a
  `part`, a sub-agent start being a `tool` part naming `task`, and which
  reports tokens and cost on each model step's `step_finish` part;
- `codex`, the native app-server, whose bridge records response boundaries,
  child-thread reports and cumulative tokens, with no reported dollar cost.

A harness reads its own stream: `starts()` returns the same `Start` values
from any of them, so the scorer above it is unaware of which CLI produced
them. Each start names the start whose sub-agent made it and the shell
commands its own sub-agent ran, wherever the stream attributes a call to a
sub-agent; `nested_starts` declares whether it does, as read from what
each CLI prints.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import textwrap
from dataclasses import asdict, dataclass, field
from pathlib import Path

from workflow import CorpusError

QUESTION = "question"
DONE = "done"

SKILL_HOME = ".claude/skills"
"""Where the Claude and Cursor CLIs discover a bootstrap skill.

Each scans `<workspace>/.claude/skills/<name>/SKILL.md`; opencode's own root
is `.opencode/skills`, which its harness names instead.
"""

MANAGED_SETTINGS = {
    "linux": "/etc/claude-code/managed-settings.json",
    "darwin": "/Library/Application Support/ClaudeCode/managed-settings.json",
    "win32": "C:/Program Files/ClaudeCode/managed-settings.json",
}
"""The file Claude Code reads the host's managed settings from, by platform."""

MESSAGE = "message"
ASSISTANT = "assistant"
USER = "user"
TOOL_USE = "tool_use"
TOOL_RESULT = "tool_result"
CALL_ID = "tool_use_id"
AGENT = "Agent"
PROMPT = "prompt"
PARENT = "parent_tool_use_id"
"""The `Agent` call a Claude message runs under, null for the session's own."""
SHELL_TOOL = "Bash"
"""The Claude Code tool that runs a command line."""
RESULT = "result"
IS_ERROR = "is_error"
USAGE = "usage"
MODEL_USAGE = "modelUsage"

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
OUTPUT = "output"
TASK_TEXT = re.compile(r"<(task_result|task_error)>\s*(.*?)\s*</\1>", re.DOTALL)
"""The sub-agent's own text within a `task` call's output.

opencode wraps what a sub-agent returned in `<task id=… state=…>`, its text
in `<task_result>`, or `<task_error>` where the sub-agent failed.
"""
TOKEN_KINDS = ("input", "output", "reasoning")
CACHE_KINDS = ("write", "read")
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


@dataclass(frozen=True)
class Start:
    """One sub-agent start a session's transcript records.

    `target` is the prompt the dispatching call carried, naming the file or
    section it handed over; `returned` is what the sub-agent gave back, and `together`
    says whether it started in the same message as the start above it.
    `parent` is the index of the start whose sub-agent made this one, or
    nothing for a start the session made itself, so each sub-agent's own
    starts sit under the section it followed at whatever depth. `commands`
    are the shell commands this start's sub-agent ran, in order, as the
    stream attributes them to it. `actor` is the sub-agent a native response
    group belongs to, and `group` that group's identity: two starts sharing
    both were dispatched together, wherever a harness reports that natively.
    """

    target: str
    returned: str
    together: bool
    parent: int | None = None
    commands: tuple[str, ...] = ()
    actor: str | None = None
    group: str | None = None

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


HANDBACK = "The report follows:"
"""The words closing the frame Claude Code puts around a sub-agent's report.

The report follows them, each of its lines indented, and the frame's own
text precedes them, so a return is read from what follows.
"""


def unframed(content: object) -> str:
    """A sub-agent's report, taken from inside the CLI's hand-back frame.

    A return carrying no frame is the report whole.
    """
    if isinstance(content, list):
        content = " ".join(
            part.get(TEXT, "") for part in content if isinstance(part, dict)
        )
    text = content if isinstance(content, str) else ""
    _, framed, report = text.partition(HANDBACK)
    return textwrap.dedent(report) if framed else text


QUESTION_LINE = "Question:"
"""How the first line of a returned question opens, as `pf`'s guide prescribes."""


def asked(report: str) -> str:
    """What a sub-agent's report states: `question` where its first line opens
    with the guide's marker, and `done` otherwise."""
    lines = [line.strip() for line in report.splitlines() if line.strip()]
    return QUESTION if lines and lines[0].startswith(QUESTION_LINE) else DONE


def said(text: object) -> str:
    """What a returned block states, as `question` or `done`."""
    if isinstance(text, list):
        text = " ".join(part.get(TEXT, "") for part in text if isinstance(part, dict))
    held = text.strip().lower() if isinstance(text, str) else ""
    return QUESTION if held.startswith(QUESTION) else DONE


def counted(
    plugins: dict[str, str | None], environment: list[str], hooks: list[str]
) -> dict[str, int | str | None]:
    """A managed configuration as `run.json` records it, naming none of it.

    `plugins` maps each managed plugin to its version, `environment` holds
    each key the managed settings add, and `hooks` each event a session's
    transcript shows a managed hook responding to, once per event. The
    hook events come from the transcripts, never the hooks' content. The
    record gives how many of each
    there are and a `fingerprint`: the SHA-256 hex digest of the three
    sorted, as canonical JSON, so two runs on one configuration give one
    fingerprint and a changed plugin, version, key or event gives another.
    A configuration with nothing managed has a null fingerprint.
    """
    held = {
        "plugins": sorted([plugin, version] for plugin, version in plugins.items()),
        "environment": sorted(environment),
        "hooks": sorted(hooks),
    }
    canonical = json.dumps(held, sort_keys=True, separators=(",", ":"))
    return {
        "plugins": len(plugins),
        "environment": len(environment),
        "hooks": len(hooks),
        "fingerprint": hashlib.sha256(canonical.encode()).hexdigest()
        if plugins or environment or hooks
        else None,
    }


@dataclass(frozen=True)
class Claude:
    """The Claude Code CLI: `-p` with a stream-json session stream."""

    name: str = "claude"
    config_variable: str = "CLAUDE_CONFIG_DIR"
    scrubbed: tuple[str, ...] = ("CLAUDE", "ANTHROPIC_")
    login: str = ".credentials.json"
    plugins: str = "plugins/installed_plugins.json"
    remote: str = "remote-settings.json"
    signature: str = "remote-settings.json.signature.json"
    enabled: str = "enabledPlugins"
    managed_scope: str = "managed"
    settings: str = "settings.json"
    managed_settings: str = MANAGED_SETTINGS.get(
        sys.platform, MANAGED_SETTINGS["linux"]
    )
    """The host's managed settings file, whose hooks reach every session."""
    project: str = ".claude"
    """The directory holding a project's own settings, in a workspace or above it."""
    project_settings: tuple[str, ...] = ("settings.json", "settings.local.json")
    hooks: str = "hooks"
    default_agent: str = "claude"
    tools: str = "Read,Write,Edit,Glob,Grep,Agent"
    foreground: tuple[str, str] = ("CLAUDE_CODE_DISABLE_BACKGROUND_TASKS", "1")
    """The variable holding each sub-agent within the call that starts it.

    The CLI otherwise starts a sub-agent in the background: the call returns
    at once, the parent ends its turn before the answer arrives, and the
    answer reaches it as a notification rather than as the call's result.
    """
    shell_tool: str = SHELL_TOOL
    """The shell tool a session given `pf` also carries."""
    skill_home: str = ".claude/skills"
    pf_only: str = "Bash(pf:*)"
    """The allowlist rule confining that tool to the build under test."""
    prompt_on_argv: bool = False
    """Whether the task text is an argument rather than the session's input."""
    nested_starts: bool = True
    """Whether a sub-agent's own starts and tool calls reach the session's stream.

    They do: a sub-agent's messages are printed in the session's stream, each
    naming the `Agent` call it runs under as `parent_tool_use_id`, so its
    starts and its shell commands are read under the start it follows.
    """
    session_cap_usd: float = 0.50
    """The price the CLI itself may spend in one session.

    The CLI caps dollars between calls and reports no token ceiling, so a
    run's token budget is held by the run's own guard and this figure holds
    what the CLI alone could spend before that guard sees a result.
    """
    usage: tuple[str, str, str, str] = (
        "inputTokens",
        "outputTokens",
        "cacheCreationInputTokens",
        "cacheReadInputTokens",
    )
    """The token kinds each model's entry in a result's `modelUsage` counts."""

    def argv(
        self,
        agent: list[str],
        model: str,
        budget: int,
        workspace: Path | None = None,
        reasoning_effort: str | None = None,
    ) -> list[str]:
        """One session's command line, its prompt given on standard input.

        A token budget is not a dollar cap, so `--max-budget-usd` is given the
        price a session is allowed to spend rather than the token count: the
        CLI enforces dollars between calls, and the run's own guard holds the
        token budget from what each session reports.

        Every session carries the shell tool, and `--allowedTools` admits
        `pf` with any arguments and output redirects in its workspace.
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
            f"{self.tools},{self.shell_tool}",
            "--allowedTools",
            self.pf_only,
            "--permission-mode",
            "acceptEdits",
            "--no-session-persistence",
            "--strict-mcp-config",
            "--disable-slash-commands",
            "--max-budget-usd",
            str(self.session_cap_usd),
        ]

    def environment(self, config: Path, held: dict[str, str]) -> dict[str, str]:
        """The caller's environment without its agent variables, naming `config`.

        Sub-agents run in the foreground, so each start's result is its answer.
        """
        kept = {
            name: value
            for name, value in held.items()
            if not name.startswith(self.scrubbed)
        }
        variable, value = self.foreground
        return {**kept, self.config_variable: str(config), variable: value}

    def preflight(
        self, config: Path, workspaces: Path, sources: tuple[Path, ...]
    ) -> str | None:
        """How the settings a session reads would let a hook reach it, if they do.

        Claude Code reads a hook from the configuration directory, from each
        project's `.claude` settings at a session's working directory, and from
        such a directory on the path from that working directory to the
        filesystem root. `sources` are the trees a session's workspace is
        copied from, so a project file a tree carries reaches every session of
        that tree; `workspaces` is the run's workspace root, which every
        session's workspace sits under.

        A managed configuration is no refusal: a plugin installed at managed
        scope or enabled by the signed remote settings, and the host's managed
        settings file, reach every session and the run counts them through
        `managed()`. A plugin installed at any other scope, and one an unsigned
        remote settings file enables, is refused.
        """
        if not (config / self.login).is_file():
            return (
                f"{config} holds no login; log in once with "
                f"`{self.config_variable}={config} claude`, then `/login`"
            )
        installing = config / self.plugins
        installed = _record(installing).get("plugins")
        if isinstance(installed, dict):
            for plugin, installs in installed.items():
                entries = installs if isinstance(installs, list) else [installs]
                unmanaged = sorted(
                    {
                        str(entry.get("scope") if isinstance(entry, dict) else None)
                        for entry in entries
                    }
                    - {self.managed_scope}
                )
                if unmanaged:
                    return (
                        f"{installing} installs {plugin} at {', '.join(unmanaged)} "
                        f"scope, whose hooks reach every session before its first "
                        f"turn; remove it before this run"
                    )
        enabling = config / self.remote
        if self._enabled(config) and not (config / self.signature).is_file():
            return (
                f"{enabling} enables a plugin and its environment without a "
                f"signature, so the organisation does not manage it; remove "
                f"{enabling}"
            )
        declared = config / self.settings
        refused = self.hook_refusal(
            declared,
            f"reaches every session before its first turn; remove {declared} "
            f"before this run",
        )
        if refused is not None:
            return refused
        for source in sources:
            for name in self.project_settings:
                held = source / self.project / name
                refused = self.hook_refusal(
                    held,
                    f"reaches every session before its first turn; remove {held} "
                    f"before this run",
                )
                if refused is not None:
                    return refused
        resolved = workspaces.resolve()
        for ancestor in (resolved, *resolved.parents):
            for name in self.project_settings:
                held = ancestor / self.project / name
                refused = self.hook_refusal(
                    held,
                    f"reaches every session under {workspaces}; pass an --eval-root "
                    f"outside {ancestor} before this run",
                )
                if refused is not None:
                    return refused
        return None

    def _enabled(self, config: Path) -> list[str]:
        """The plugins the remote settings enable, in name order."""
        enabled = _record(config / self.remote).get(self.enabled)
        if not isinstance(enabled, dict):
            return []
        return sorted(name for name, value in enabled.items() if value is True)

    def _plugins(self, config: Path) -> dict[str, str | None]:
        """Each managed plugin with its version, in no particular order.

        A managed plugin is one installed at managed scope or enabled by the
        signed remote settings, its version null where it is enabled but not
        installed here.
        """
        installed = _record(config / self.plugins).get("plugins")
        versions: dict[str, str | None] = {}
        if isinstance(installed, dict):
            for plugin, installs in installed.items():
                for entry in installs if isinstance(installs, list) else [installs]:
                    if (
                        isinstance(entry, dict)
                        and entry.get("scope") == self.managed_scope
                    ):
                        versions[plugin] = entry.get("version")
        if (config / self.signature).is_file():
            for plugin in self._enabled(config):
                versions.setdefault(plugin, None)
        return versions

    def prepare(self, config: Path) -> None:
        """Nothing to write: the configuration directory is the CLI's own."""

    def hooked(self, config: Path) -> bool:
        """Whether a managed configuration can deliver a hook to a session.

        A managed plugin can, and so can the host's managed settings file when
        it declares a hook: the administrator owns that file and Claude Code
        reads it wherever the configuration directory points. The preflight
        admits no other hook, so a hook response a session carries is the
        managed configuration's exactly when this holds.
        """
        return bool(self._plugins(config)) or bool(
            self.hook_events(Path(self.managed_settings))
        )

    def managed(self, config: Path, hooks: list[str]) -> dict[str, int | str | None]:
        """The managed configuration every session carries, counted.

        The plugins are `_plugins()`'s. A managed environment setting is a key
        the signed remote settings' `env` adds over the scrubbed environment.
        `hooks` are the hook events the run's transcripts show a hook
        responding to, which the run passes in once its sessions finish, since
        no file the harness reads states every hook a managed plugin brings.
        The run records them through `counted()`.
        """
        signed = (config / self.signature).is_file()
        env = _record(config / self.remote).get("env") if signed else None
        return counted(
            self._plugins(config),
            sorted(env) if isinstance(env, dict) else [],
            hooks,
        )

    def hook_events(self, path: Path) -> list[str]:
        """The events a settings file declares a hook for, in name order."""
        hooks = _record(path).get(self.hooks)
        if not isinstance(hooks, dict):
            return []
        return sorted(str(event) for event, commands in hooks.items() if commands)

    def hook_refusal(self, path: Path, consequence: str) -> str | None:
        """Why a settings file declaring a hook is refused, or nothing if none is."""
        events = self.hook_events(path)
        if not events:
            return None
        return f"{path} declares a hook for {', '.join(events)}, which {consequence}"

    def result(self, transcript: Path) -> dict[str, object] | None:
        """The session's last `result` message, if it printed one."""
        found = None
        for held in messages(transcript):
            if held.get("type") == RESULT:
                found = held
        return found

    def starts(self, transcript: Path) -> tuple[Start, ...]:
        """The sub-agents a session started, in order.

        A `tool_use` block naming `Agent` is one start; two such blocks in one
        assistant message started together. The CLI prints each block of a
        message as an event of its own carrying the message's `id`, so a
        start is together with the one before it when both carry one id. A
        start's target is the `prompt` its input carries, naming the file or
        section handed over, and its return is the report inside the CLI's
        hand-back frame. A start's parent is the start whose `Agent` call the
        message's `parent_tool_use_id` names, and its commands are those of
        the `Bash` calls in messages naming its own `Agent` call that way,
        which its sub-agent made.
        """
        found: dict[str, tuple[str, bool, str | None]] = {}
        returned: dict[str, str] = {}
        ran = _shell_calls(transcript)
        last: object = None
        for index, held in enumerate(messages(transcript)):
            kind = held.get("type")
            carried = held.get(MESSAGE)
            content = carried.get("content") if isinstance(carried, dict) else None
            if not isinstance(content, list) or not isinstance(carried, dict):
                continue
            if kind == ASSISTANT:
                parent = _owner(held)
                named = carried.get("id")
                message: object = named if isinstance(named, str) else index
                for block in content:
                    if not isinstance(block, dict) or block.get("type") != TOOL_USE:
                        continue
                    if block.get("name") != AGENT:
                        continue
                    held_input = block.get("input")
                    target = (
                        held_input.get(PROMPT) if isinstance(held_input, dict) else None
                    )
                    key = block.get("id")
                    if not isinstance(key, str) or not isinstance(target, str):
                        continue
                    found[key] = (target, message == last, parent)
                    last = message
            elif kind == USER:
                for block in content:
                    if not isinstance(block, dict) or block.get("type") != TOOL_RESULT:
                        continue
                    key = block.get(CALL_ID)
                    if isinstance(key, str):
                        returned[key] = asked(unframed(block.get("content")))
        order = {key: index for index, key in enumerate(found)}
        return tuple(
            Start(
                target,
                returned.get(key, DONE),
                together,
                order.get(parent) if parent is not None else None,
                tuple(command for owner, command in ran if owner == key),
            )
            for key, (target, together, parent) in found.items()
        )

    def commands(self, transcript: Path) -> tuple[str, ...]:
        """The shell commands the session itself ran, in order.

        A `Bash` call in a message naming no `parent_tool_use_id` is the
        session's own; one naming a `Task` call is that sub-agent's, and is
        read under its start.
        """
        return tuple(
            command for owner, command in _shell_calls(transcript) if owner is None
        )

    def tokens(self, result: dict[str, object] | None) -> int | None:
        """The tokens one session processed, its sub-agents' among them.

        The last `result` message's `modelUsage` counts each model's tokens
        over the whole session, every turn and every sub-agent included,
        while its `usage` counts the parent's own turns. A result carrying no
        `modelUsage` reports nothing.
        """
        if result is None:
            return None
        models = result.get(MODEL_USAGE)
        if not isinstance(models, dict):
            return None
        counts = [
            count
            for model in models.values()
            if isinstance(model, dict)
            for name in self.usage
            if isinstance(count := model.get(name), int | float)
        ]
        return int(sum(counts)) if counts else None

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
    scrubbed: tuple[str, ...] = ("CURSOR",)
    default_agent: str = "cursor-agent"
    skill_home: str = ".claude/skills"
    prompt_on_argv: bool = False
    """Whether the task text is an argument rather than the session's input."""
    nested_starts: bool = False
    """Whether a sub-agent's own starts and tool calls reach the session's stream.

    They do not: the CLI reports a sub-agent's final text and the steps it
    took, and no tool call it made. A scenario whose trace names a start
    made inside a sub-agent, or which states a sub-agent's `pf` run, cannot
    be observed on this harness.
    """
    usage: tuple[str, str, str, str] = (
        "inputTokens",
        "outputTokens",
        "cacheWriteTokens",
        "cacheReadTokens",
    )

    def argv(
        self,
        agent: list[str],
        model: str,
        budget: int,
        workspace: Path | None = None,
        reasoning_effort: str | None = None,
    ) -> list[str]:
        """One session's command line, the workspace given as its argument.

        The CLI has no session spend cap and no tool allowlist, so the run's
        own token guard is the whole budget, and the workspace the run laid
        out is what a session is confined to. Its shell is there to every
        session, so it is confined to `pf` by what the instruction names alone.

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

    def preflight(
        self, config: Path, workspaces: Path, sources: tuple[Path, ...]
    ) -> str | None:
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

    def prepare(self, config: Path) -> None:
        """Nothing to write: the CLI reads the caller's configuration."""

    def hooked(self, config: Path) -> bool:
        """No managed hook reaches a session: the CLI keeps no managed settings."""
        return False

    def managed(self, config: Path, hooks: list[str]) -> dict[str, int | str | None]:
        """Nothing managed is read: the CLI keeps no configuration directory."""
        return counted({}, [], [])

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
        target is the `prompt` in its args; what it returned is the
        text of the completed call's `conversationSteps`.

        Only the starts a session made itself are readable: a sub-agent's own
        stream is not part of its parent's transcript, so a dispatch nested
        inside a sub-agent leaves its parent's record silent about it. A
        scenario stating such a start is beyond what this harness reports,
        as `nested_starts` declares.
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
                target = args.get(PROMPT)
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

        A `shellToolCall` carries the command line it ran. A session is held
        to the `pf` runs its scenario states, read from these commands,
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


def _owner(held: dict[str, object]) -> str | None:
    """The `Task` call a Claude message runs under, or nothing for the session's."""
    owner = held.get(PARENT)
    return owner if isinstance(owner, str) else None


def _shell_calls(transcript: Path) -> list[tuple[str | None, str]]:
    """Each `Bash` call a Claude stream records, with the `Task` call it runs under."""
    found: list[tuple[str | None, str]] = []
    for held in messages(transcript):
        if held.get("type") != ASSISTANT:
            continue
        carried = held.get(MESSAGE)
        content = carried.get("content") if isinstance(carried, dict) else None
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict) or block.get("type") != TOOL_USE:
                continue
            if block.get("name") != SHELL_TOOL:
                continue
            carried_input = block.get("input")
            command = (
                carried_input.get(COMMAND) if isinstance(carried_input, dict) else None
            )
            if isinstance(command, str):
                found.append((_owner(held), command))
    return found


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
    on each `step_finish` part, one per model step, and summed over the session.
    The parts printed are the started session's alone, so a sub-agent's own
    calls are not among them.
    """

    name: str = "opencode"
    scrubbed: tuple[str, ...] = ("OPENCODE",)
    default_agent: str = "~/.opencode/bin/opencode"
    """Where the CLI installs itself, which is not on a login shell's path."""
    skill_home: str = ".opencode/skills"
    """Where a bootstrap skill sits, which is the root this CLI discovers.

    The CLI discovers `.claude/skills` too, but only through the scan of a
    caller's Claude Code installation that isolation switches off.
    """
    config_variables: tuple[tuple[str, str], ...] = (
        ("XDG_CONFIG_HOME", "config"),
        ("XDG_DATA_HOME", "data"),
        ("XDG_STATE_HOME", "state"),
        ("XDG_CACHE_HOME", "cache"),
    )
    """The directories the CLI otherwise shares with the caller, and their name
    under the eval root: the caller's plugins, remembered projects, credential
    store and cache."""
    settings: str = "harness.json"
    """The configuration file the run writes, the whole of what a session reads."""
    disabled: tuple[str, ...] = (
        "OPENCODE_PURE",
        "OPENCODE_DISABLE_DEFAULT_PLUGINS",
        "OPENCODE_DISABLE_EXTERNAL_SKILLS",
        "OPENCODE_DISABLE_CLAUDE_CODE_SKILLS",
        "OPENCODE_DISABLE_CLAUDE_CODE",
        "OPENCODE_DISABLE_PROJECT_CONFIG",
        "OPENCODE_DISABLE_MODELS_FETCH",
        "OPENCODE_DISABLE_LSP_DOWNLOAD",
        "OPENCODE_DISABLE_AUTOUPDATE",
    )
    """What a session runs without: plugins, a caller's external skills, a
    project's own configuration, the model catalogue and an update check.

    `OPENCODE_PURE` and `OPENCODE_DISABLE_DEFAULT_PLUGINS` keep the caller's
    installed plugins out. The two skill flags keep the caller's Claude Code
    and `.agents` skills out, and `OPENCODE_DISABLE_PROJECT_CONFIG` keeps a
    workflow's own `opencode.json` from adding permissions the run did not
    state. Model-catalogue fetching and update checks reach the network, which
    a session measures nothing by doing.
    """
    permission: dict[str, object] = field(
        default_factory=lambda: {
            "bash": {"*": "deny", "pf *": "allow"},
            "edit": "allow",
            "read": "allow",
            "glob": "allow",
            "grep": "allow",
            "list": "allow",
            "task": "allow",
            "webfetch": "deny",
            "websearch": "deny",
            "external_directory": "deny",
        }
    )
    """What a session may do: write its workspace, read it, dispatch sections,
    and run `pf` with any arguments and output redirects.

    The CLI has no allowlist of the tools a session carries, so every other
    capability is refused here instead. `external_directory` is what confines
    a read, a write and a shell command to the session's own workspace.
    """
    subagent_depth: int = 8
    """How deep a sub-agent's own dispatch may go.

    The CLI refuses a nested start at depth one by default, and a compiled
    bundle dispatches at every hop the workflow states, so a session could
    follow no chain. The figure matches the link depth `pf` compiles to.
    """
    prompt_on_argv: bool = True
    """Whether the task text is an argument rather than the session's input.

    The CLI reads its prompt from its arguments, so a run appends it there.
    A prompt written to its input instead is read by nothing.
    """
    nested_starts: bool = False
    """Whether a sub-agent's own dispatch reaches the parent's stream.

    It does not: a `task` call's parts are its own, and a start either its
    sub-agent made is a part of that sub-agent's session, which the parent's
    stream never carries. A scenario whose trace names one is beyond this
    harness's observation, so the runner leaves it out, and a sub-agent's own
    `pf` runs are read from the commands it ran, which are absent for the
    same reason.
    """

    def argv(
        self,
        agent: list[str],
        model: str,
        budget: int,
        workspace: Path | None = None,
        reasoning_effort: str | None = None,
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
        directory, and a session that names no workspace of its own ran in
        the repository this file was written in. The permissions come from the
        run's own settings file, which confines every command but `pf` and
        every path but the workspace.
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
        """The caller's environment without its agent variables, confined to `config`.

        Each directory the CLI otherwise shares with the caller is named under
        the eval root, so no plugin, remembered project, credential store or
        cache reaches a session. `OPENCODE_CONFIG` names the one file the run
        writes, and every capability the run does not admit is switched off.
        """
        kept = {
            name: value
            for name, value in held.items()
            if not name.startswith(self.scrubbed)
        }
        named = {
            variable: str(config / directory)
            for variable, directory in self.config_variables
        }
        settings = config / self.settings
        return {
            **kept,
            **named,
            "OPENCODE_CONFIG": str(settings),
            **{name: "1" for name in self.disabled},
        }

    def preflight(
        self, config: Path, workspaces: Path, sources: tuple[Path, ...]
    ) -> str | None:
        """What this harness cannot guarantee, stated as a refusal.

        The CLI reaches a provider through the credential store under its data
        directory, which the run names under the eval root, and reads its
        permissions from the one file the run writes. A run without either
        would reach the caller's own installation, so both are required
        before a session starts.
        """
        if not config.is_dir():
            return (
                f"{config} is no directory; this harness writes its settings "
                f"and credential store there, so name an eval root"
            )
        credential = config / "data" / "opencode" / "auth.json"
        if not credential.is_file():
            return (
                f"{credential} holds no login; run "
                f"XDG_DATA_HOME={config / 'data'} opencode auth login once"
            )
        return None

    def prepare(self, config: Path) -> None:
        """Write the one settings file a session reads.

        The file states the run's permissions alone, so a session's
        capabilities are the run's rather than whatever the caller's
        installation would offer.
        """
        config.mkdir(parents=True, exist_ok=True)
        settings = {
            "$schema": "https://opencode.ai/config.json",
            "permission": self.permission,
            "subagent_depth": self.subagent_depth,
        }
        (config / self.settings).write_text(json.dumps(settings, indent=2) + "\n")

    def hooked(self, config: Path) -> bool:
        """No managed hook reaches a session: the CLI reads no managed settings."""
        return False

    def managed(self, config: Path, hooks: list[str]) -> dict[str, int | str | None]:
        """Nothing managed is read: the CLI keeps no configuration directory."""
        return counted({}, [], [])

    def result(self, transcript: Path) -> dict[str, object] | None:
        """The session's spend, one `step_finish` record summing every step.

        The CLI prints no closing `result` message and reports each model
        step's tokens and cost on that step's own part, so a session's spend
        is the sum over its parts. Each token kind and the cost are summed
        where any step reported them, and a session that printed no step
        reports nothing.
        """
        steps = [
            part
            for held in messages(transcript)
            if held.get("type") == STEP_FINISH
            and isinstance(part := held.get(OPENCODE_PART), dict)
        ]
        if not steps:
            return None
        counts = [
            count for step in steps if isinstance(count := step.get(TOKENS), dict)
        ]
        caches = [
            cache for count in counts if isinstance(cache := count.get(CACHE), dict)
        ]
        tokens: dict[str, object] = _summed(counts, TOKEN_KINDS)
        if caches:
            tokens[CACHE] = _summed(caches, CACHE_KINDS)
        summed: dict[str, object] = {"type": STEP_FINISH, TOKENS: tokens}
        costs = [step.get(COST) for step in steps]
        if any(isinstance(cost, int | float) for cost in costs):
            summed[COST] = sum(cost for cost in costs if isinstance(cost, int | float))
        return {"type": STEP_FINISH, OPENCODE_PART: summed, "steps": len(steps)}

    def starts(self, transcript: Path) -> tuple[Start, ...]:
        """The sub-agents a session started, in order.

        A `tool_use` part naming `task` is one start; its input's
        `prompt` is the text the dispatching call carried. Two starts
        sharing a `messageID` were dispatched in one message. What a start
        returned is what the sub-agent's text in the call's `output` states,
        and a call printing no output returned `done`.
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
                carried_input.get(PROMPT) if isinstance(carried_input, dict) else None
            )
            key = part.get(OPENCODE_CALL_ID)
            message = part.get(OPENCODE_MESSAGE_ID)
            if not isinstance(target, str) or not isinstance(key, str):
                continue
            together = isinstance(message, str) and message in seen
            seen.add(message if isinstance(message, str) else key)
            output = state.get(OUTPUT) if isinstance(state, dict) else None
            found.append((said(_returned(output)), target, together))
        return tuple(
            Start(target, returned, together) for returned, target, together in found
        )

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
        """The tokens one session processed, every kind of its summed steps."""
        if result is None:
            return None
        part = result.get(OPENCODE_PART)
        tokens = part.get(TOKENS) if isinstance(part, dict) else None
        if not isinstance(tokens, dict):
            return None
        counts = [tokens.get(kind) for kind in TOKEN_KINDS]
        cache = tokens.get(CACHE)
        if isinstance(cache, dict):
            counts += [cache.get(kind) for kind in CACHE_KINDS]
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


def _returned(output: object) -> str:
    """The sub-agent's text within a `task` call's output, or the whole output."""
    if not isinstance(output, str):
        return ""
    held = TASK_TEXT.search(output)
    return held.group(2) if held else output


def _summed(
    counts: list[dict[str, object]], kinds: tuple[str, ...]
) -> dict[str, object]:
    """Each kind summed over the counts that reported it, a kind none did left out."""
    summed: dict[str, object] = {}
    for kind in kinds:
        held = [count.get(kind) for count in counts]
        numbers = [value for value in held if isinstance(value, int | float)]
        if numbers:
            summed[kind] = sum(numbers)
    return summed


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


@dataclass(frozen=True)
class Codex:
    """Native Codex app-server with confined file tools and structured `pf`."""

    name: str = "codex"
    config_variable: str = "CODEX_HOME"
    scrubbed: tuple[str, ...] = ("CODEX", "OPENAI_")
    default_agent: str = "codex"
    prompt_on_argv: bool = False
    nested_starts: bool = True
    skill_home: str = ".agents/skills"

    def argv(
        self,
        agent: list[str],
        model: str,
        budget: int,
        workspace: Path | None = None,
        reasoning_effort: str | None = None,
    ) -> list[str]:
        """The native bridge, with explicit model, reasoning and token ceiling."""
        if reasoning_effort is None:
            raise CorpusError("the codex harness requires --reasoning-effort")
        return [
            sys.executable,
            str(Path(__file__).with_name("codex_agent.py")),
            "--command",
            json.dumps(agent),
            "--model",
            model,
            "--reasoning-effort",
            reasoning_effort,
            "--session-budget-tokens",
            str(budget),
        ]

    def environment(self, config: Path, held: dict[str, str]) -> dict[str, str]:
        """An eval-owned home, without the caller's Codex or OpenAI variables."""
        kept = {
            name: value
            for name, value in held.items()
            if not name.startswith(self.scrubbed)
        }
        return {**kept, self.config_variable: str(config / self.name)}

    def preflight(
        self, config: Path, workspaces: Path, sources: tuple[Path, ...]
    ) -> str | None:
        """Require the eval's login and refuse caller configuration material."""
        home = config / self.name
        if not (home / "auth.json").is_file():
            return f"{home} holds no login; run CODEX_HOME={home} codex login once"
        for name in (
            "config.toml",
            "AGENTS.md",
            "AGENTS.override.md",
            "rules",
            "skills",
            "memories",
        ):
            if (home / name).exists():
                return (
                    f"{home / name} supplies context outside the eval; "
                    "use an auth-only Codex home"
                )
        for source in sources:
            if (source / ".codex").exists():
                return f"{source / '.codex'} supplies project configuration to the eval"
        return None

    def hooked(self, config: Path) -> bool:
        """Hooks are disabled and any native hook event refuses the session."""
        return False

    def managed(self, config: Path, hooks: list[str]) -> dict[str, int | str | None]:
        """No managed hook or caller context is admitted by this adapter."""
        return counted({}, [], [])

    def result(self, transcript: Path) -> dict[str, object] | None:
        """The bridge's final reading of native completion and usage evidence."""
        return next(
            (
                held
                for held in reversed(messages(transcript))
                if held.get("type") == RESULT and held.get("harness") == self.name
            ),
            None,
        )

    def starts(self, transcript: Path) -> tuple[Start, ...]:
        """Native dispatch prompts, response groups and completed child reports."""
        result = self.result(transcript)
        held = result.get("starts") if result else None
        return (
            tuple(
                Start(
                    str(row["target"]),
                    str(row["returned"]),
                    bool(row["together"]),
                    row.get("actor"),
                    row.get("group"),
                )
                for row in held
                if isinstance(row, dict)
            )
            if isinstance(held, list)
            else ()
        )

    def commands(self, transcript: Path) -> tuple[str, ...]:
        """The `pf` invocations the native command service actually executed."""
        result = self.result(transcript)
        held = result.get("commands") if result else None
        return (
            tuple(command for command in held if isinstance(command, str))
            if isinstance(held, list)
            else ()
        )

    def tokens(self, result: dict[str, object] | None) -> int | None:
        """Every observed thread's cumulative total, each thread counted once."""
        held = result.get("tokens") if result else None
        return int(held) if isinstance(held, int | float) else None

    def cost(self, result: dict[str, object] | None) -> float | None:
        """The native CLI reports no dollar cost."""
        return None


Harness = Claude | Cursor | Opencode | Codex
"""Any declared harness, as the runner and the scorer accept one."""

HARNESSES = {
    harness.name: harness for harness in (Claude(), Cursor(), Opencode(), Codex())
}


def harness_named(name: str) -> Harness:
    """The declared harness with the supplied name."""
    if name not in HARNESSES:
        raise KeyError(f"the harnesses are {', '.join(HARNESSES)}, not {name}")
    return HARNESSES[name]
