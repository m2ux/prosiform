"""Run the diagram-following eval: give each workflow form to agent sessions.

A run starts one headless agent session per model, workflow, scenario, form
and repetition. Each session works in a fresh temporary workspace holding
only its form's material as `workflow.md`, and `inputs/` holding the
scenario's inputs, each as the value followed by a newline. The forms are:

- `bundle`: the diagram form bundled by `pf`, as one file;
- `tree`: the diagram form's source tree as it is, entered at `workflow.md`;
- `prose`: the prose form bundled by `pf`, as one file;
- `linked`: the linked form's source tree as it is, entered at `workflow.md`.

The session is the agent command run in its workspace with the shared
instruction on standard input, its tools limited to reading, writing and
searching files and to starting a sub-agent, with no MCP server and no
shell. `acceptEdits` lets it change files only within its workspace.

Sessions run under the eval root, `--eval-root`. `<root>/config/` is the
eval's own Claude configuration directory, holding its login, settings and
memory apart from the caller's; each session receives it as
`CLAUDE_CONFIG_DIR`, in an environment holding no other `CLAUDE*` or
`ANTHROPIC_*` variable. A run whose configuration directory holds no login
fails before it starts a session, naming the one-time login command, and so
does one whose directory installs a plugin or whose remote settings enable
one, naming the file that says so: a plugin's hooks reach a session before
its first turn and no flag the runner passes suppresses them.

What a session's agent did carry is read back from its transcript, so the
boundary is observed rather than assumed. A hook's response, an appended
system prompt or a memory file is context the run did not supply, and a run
one of whose sessions carries one fails, naming the session and what it
carried.
`<root>/workspaces/<run-id>/` holds the run's workspaces, each at its
session's place in the matrix and removed once its records are kept.

Each session's records go to `results/<run-id>/<model>/<workflow>/
<scenario>/<form>/<repetition>/`: `transcript.jsonl`, the stream-json the
agent printed; `stderr.log` when it printed any; `subagents.json`, the
sub-agent starts the transcript records, in order, with what each returned;
the final workspace's `trace.log` and `actions/`; and `session.json`,
holding the session's identity, exit status, duration, the stream's
`result` message with its `usage` and `total_cost_usd`, and the scorer's
verdict record. `run.json`
holds the run's date, options, recorded cost, the sessions it did not
start and the run's state. Once `run.json` is written, `report.py` writes
the run's report beside it, compared with the committed baseline.

A run every session of which took the `errored` verdict is `refused`: no
session entered a state, so the matrix is no result and its pass rates
would read a spent login as a matrix of failing agents. The reason it
records is one session's own `result` text, so a reader sees the limit the
agent reported. The state is decided here, once the sessions have settled
and before `run.json` is written, and the report reads it from there: the
whole matrix must have started and every session must have errored, so a
run its budget stopped part way, and one where some sessions errored on a
genuine fault beside passing ones, is a result rather than a refusal.

A session runs for at most `--session-timeout-seconds`. On expiry its
process group, the agent and every process it started, is killed; its exit
status is recorded as `timeout`, and what its workspace holds by then is
kept and scored like any other session's.

The spending cap holds a run's recorded cost within `--budget-usd`. A run
whose budget does not cover every session of its matrix at the session cap,
`--session-budget-usd`, is refused before it starts a session, naming both.
The agent checks its session cap between calls, so a session can record
more than its cap, and the run guards its budget against that: a
session starts only when the recorded cost, plus the session cap reserved
for each session in flight, plus its own session cap, is within the
budget; while it is not and a session is in flight, the next one waits for
it to settle. When it is not and none is in flight, the run starts no more
sessions and lists the rest as not started. A session settles at the cost
its `result` message reports, or at its session cap when it reports none.
"""

import argparse
import json
import os
import shlex
import shutil
import signal
import sys
import tempfile
import threading
import time
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from subprocess import PIPE, Popen, TimeoutExpired
from typing import IO, Any

from harness import HARNESSES, Harness, harness_named
from report import (
    BASELINE,
    COMPLETED,
    REASON,
    REFUSED,
    RUN,
    SESSION,
    STATE,
    TIMEOUT,
    names,
    write,
)
from score import (
    ACTIONS,
    TRACE,
    Failure,
    Verdict,
    read_trace,
    record_starts,
    score,
)
from workflow import (
    AUTHORED_FORM,
    BOOTSTRAP,
    BOOTSTRAP_DIR,
    COMPILED_FORM,
    DIAGRAM,
    ENTRY,
    ENTRY_BUNDLE,
    LINKED_FORM,
    PROSE,
    ROOT,
    SHELL_FORMS,
    CorpusError,
    Scenario,
    Workflow,
    bundle,
    bundled,
    dispatched,
    instruction,
    sections_of,
    workflows,
)

RESULTS = ROOT / "results"
INPUTS = "inputs"
TRANSCRIPT = "transcript.jsonl"
STDERR = "stderr.log"
EVAL_ROOT = Path("~/projects/eval/prosiform")
CONFIG = "config"
WORKSPACES = "workspaces"
HOOK_RESPONSE = "hook_response"
SYSTEM = "system"
CARRIED = ("additionalContext", "appendSystemPrompt", "memory")

BUNDLE = "bundle"
TREE = "tree"
PROSE_BUNDLE = "prose"
LINKED_TREE = "linked"
COMPILED_SET = "compiled"
AUTHORED_SET = "authored"
BOOTSTRAP_SET = "bootstrap"
FORMS = {
    BUNDLE: DIAGRAM,
    TREE: DIAGRAM,
    PROSE_BUNDLE: PROSE,
    LINKED_TREE: LINKED_FORM,
    COMPILED_SET: COMPILED_FORM,
    AUTHORED_SET: AUTHORED_FORM,
    BOOTSTRAP_SET: BOOTSTRAP,
}
BUNDLED = {BUNDLE, PROSE_BUNDLE, COMPILED_SET, AUTHORED_SET}
BUILD = "build"
BIN = "bin"
SKILL = "SKILL.md"
SKILL_HOME = Path(".claude") / "skills"
"""Where an agent CLI discovers a skill, walked up from its workspace.

A skill sits at `<root>/.claude/skills/<name>/SKILL.md`, and the session's
workspace is the root it walks up from, so the skill is found without the
instruction naming it.
"""
SKILL_FILES = (SKILL,)
"""The files a bootstrap skill carries beside the documents it compiles."""
"""The existing folder a bootstrapping session compiles into."""
SUMMARY = ("run_id", "harness", "state", "sessions", "started", "tokens", "not_started")

DEFAULT_MODELS = ("claude-haiku-5-5", "claude-sonnet-5-5")
DEFAULT_REPETITIONS = 5
DEFAULT_PARALLEL = 4
DEFAULT_SESSION_BUDGET = 60_000
DEFAULT_SESSION_TIMEOUT = 600.0


@dataclass(frozen=True)
class Session:
    """One session's place in the run's matrix."""

    model: str
    workflow: str
    scenario: str
    form: str
    repetition: int

    def directory(self, run_directory: Path) -> Path:
        """Where this session's records go within its run's directory."""
        return (
            run_directory
            / self.model
            / self.workflow
            / self.scenario
            / self.form
            / str(self.repetition)
        )


class Ledger:
    """The run's recorded tokens and the session caps reserved in flight.

    A budget is held in tokens, since that is the measure both harnesses
    report. A session's own dollar ceiling is the harness's, so this guard
    holds what the run has recorded rather than what a CLI may still spend.
    """

    def __init__(self, budget: int, session_cap: int) -> None:
        self.budget = budget
        self.session_cap = session_cap
        self.spent = 0
        self.reserved = 0
        self.held = 0
        self.unknown = 0
        self.stopped = False
        self.condition = threading.Condition()

    def fits(self) -> bool:
        """Whether one more session's cap fits within the budget.

        A session that reported no usage keeps its cap held against the
        budget, since what it spent is unknown, while its cap is not
        reported as tokens spent.
        """
        return self.spent + self.held + self.reserved + self.session_cap <= self.budget

    def reserve(self) -> bool:
        """Reserve a session's cap, or stop the run when it cannot fit."""
        with self.condition:
            while not self.stopped and not self.fits() and self.reserved > 0:
                self.condition.wait()
            if self.stopped or not self.fits():
                self.stopped = True
                return False
            self.reserved += self.session_cap
            return True

    def settle(self, tokens: int | None) -> None:
        """Replace a session's reserved cap with the tokens it recorded.

        A session reporting no usage contributes no tokens and is counted
        apart, since its cap is what the guard reserved rather than what it
        spent. Reporting the cap as spend would read a spent login as a run
        that consumed its whole budget.
        """
        with self.condition:
            self.reserved -= self.session_cap
            if tokens is None:
                self.unknown += 1
                self.held += self.session_cap
            else:
                self.spent += tokens
            self.condition.notify_all()


def options(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """The run's options, defaulting to the eval's full matrix."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--budget-tokens", type=int, required=True, help="the run's token cap"
    )
    parser.add_argument(
        "--session-budget-tokens",
        type=int,
        default=DEFAULT_SESSION_BUDGET,
        help="each session's token cap",
    )
    parser.add_argument(
        "--session-timeout-seconds",
        type=float,
        default=DEFAULT_SESSION_TIMEOUT,
        help="how long a session runs before it is ended",
    )
    parser.add_argument("--models", default=",".join(DEFAULT_MODELS))
    parser.add_argument("--repetitions", type=int, default=DEFAULT_REPETITIONS)
    parser.add_argument("--workflows", help="workflow names; every one by default")
    parser.add_argument("--forms", default=",".join(FORMS))
    parser.add_argument("--parallel", type=int, default=DEFAULT_PARALLEL)
    parser.add_argument(
        "--harness",
        default="claude",
        help="the agent CLI the run drives: claude or cursor",
    )
    parser.add_argument(
        "--agent-command", help="the agent's command line, overriding the harness"
    )
    parser.add_argument("--results", type=Path, default=RESULTS)
    parser.add_argument(
        "--eval-root",
        type=Path,
        default=EVAL_ROOT,
        help="the directory holding the eval's configuration and workspaces",
    )
    parser.add_argument("--run-id", help="the results directory's name")
    return parser.parse_args(argv)


def matrix(
    corpus: list[Workflow],
    models: list[str],
    forms: list[str],
    repetitions: int,
    harness: Harness = HARNESSES["claude"],
) -> list[Session]:
    """Every session a run starts when its budget allows, in start order.

    A workflow gives a session only in the forms it is written in, so the
    dispatch workflows take the two dispatch forms and the others take the
    four forms they hold. A scenario is dropped where its trace names a start
    no harness this run drives can observe: a cell whose correct run could
    not pass measures the harness, not the agent.
    """
    return [
        Session(model, workflow.name, scenario.name, form, repetition)
        for model in models
        for workflow in corpus
        for scenario in workflow.scenarios
        for form in forms
        if FORMS[form] in workflow.forms
        if runnable(form, harness)
        if observable(workflow, scenario, form, harness)
        for repetition in range(1, repetitions + 1)
    ]


def runnable(form: str, harness: Harness) -> bool:
    """Whether a harness can read this form at all.

    A form whose material a session must compile needs a command to run, so a
    harness without a shell cannot measure it: the cell would record a
    refusal as the agent's failure.
    """
    return harness.shell or FORMS[form] not in SHELL_FORMS


def observable(
    workflow: Workflow, scenario: Scenario, form: str, harness: Harness
) -> bool:
    """Whether a scenario's trace is one this harness reports.

    A trace names one start per dispatch a correct run makes, nested ones
    included. A harness that does not surface a sub-agent's own dispatch can
    report only the starts the path's own sections make, so a scenario whose
    trace outruns that count is beyond it.

    The corpus names its forms by what they hold, so the runner's form is
    read as the corpus form it carries before its sections are asked for.
    """
    if harness.nested_starts:
        return True
    written = FORMS[form]
    sections = sections_of(workflow, written)
    root = workflow.form(written)
    top = 0
    for state in scenario.path:
        section = sections[state]
        top += sum(
            len(targets)
            for _, targets in dispatched(
                section.body, section.path.parent, root, written
            )
        )
    return len(scenario.trace) <= top


def bundles_of(workflow: Workflow, form: str) -> dict[str, bytes]:
    """One bundled form's bundle set, each bundle by the name `pf` gave it."""
    with tempfile.TemporaryDirectory() as output:
        built = bundle(workflow.form(FORMS[form]), Path(output))
        if built.returncode != 0 or built.stderr:
            raise CorpusError(
                f"{workflow.name}: pf bundled the {form} form with exit "
                f"{built.returncode} and {built.stderr.decode()!r}"
            )
        written = bundled(Path(output))
        if not written:
            raise CorpusError(f"{workflow.name}: pf bundled the {form} form to no file")
        return {path.name: path.read_bytes() for path in written}


def prepare(
    workspace: Path,
    workflow: Workflow,
    scenario: Scenario,
    form: str,
    sets: dict[tuple[str, str], dict[str, bytes]],
) -> None:
    """Lay out a workspace with one form's material and a scenario's inputs.

    A bundled form's entry bundle is the document the instruction names, and
    every other bundle in its set is written beside it under the name `pf`
    gave it, since a dispatching bundle names the bundles it hands to
    sub-agents by that name.
    """
    if form in BUNDLED:
        for name, content in sets[(workflow.name, form)].items():
            written = ENTRY if name == ENTRY_BUNDLE.name else name
            (workspace / written).write_bytes(content)
    elif form == BOOTSTRAP_SET:
        placed = workspace / SKILL_HOME / workflow.name
        placed.mkdir(parents=True)
        shutil.copytree(workflow.directory / BOOTSTRAP_DIR, placed, dirs_exist_ok=True)
        (workspace / BUILD).mkdir()
        place_pf(workspace)
    else:
        shutil.copytree(workflow.form(FORMS[form]), workspace, dirs_exist_ok=True)
    (workspace / INPUTS).mkdir()
    for name, value in scenario.inputs.items():
        (workspace / INPUTS / name).write_text(f"{value}\n")


def keep(workspace: Path, records: Path) -> None:
    """Copy what the scorer reads out of a finished workspace.

    A dispatching session's path is `trace.log`; a sub-agent's is
    `trace-<section>.log`, so both are kept and a nested workflow's states are
    evidence rather than a file the run discards.
    """
    for path in sorted(workspace.glob(f"{TRACE}*")):
        if path.is_file():
            shutil.copy2(path, records / path.name)
    if (workspace / ACTIONS).is_dir():
        shutil.copytree(workspace / ACTIONS, records / ACTIONS)


def carried_context(message: dict[str, object]) -> str | None:
    """The context one transcript message adds that the run did not supply."""
    if message.get("type") == HOOK_RESPONSE or message.get("subtype") == HOOK_RESPONSE:
        kind = "a hook response"
    elif message.get("type") != SYSTEM:
        return None
    elif message.get("memory"):
        kind = "a memory file"
    elif message.get("appendSystemPrompt") or message.get("additionalContext"):
        kind = "an appended system prompt"
    else:
        return None
    text = next((str(message[key]) for key in CARRIED if message.get(key)), "")
    return f"{kind} carrying {text!r}" if text else kind


def identify(session: Session) -> str:
    """A session's place in the matrix, as one path-like name."""
    return "/".join(
        (
            session.model,
            session.workflow,
            session.scenario,
            session.form,
            str(session.repetition),
        )
    )


def injected(transcript: Path) -> str | None:
    """The context an agent added to its session, which the run did not supply.

    The form and the instruction are all a session is given, so a hook's
    response, an appended system prompt or a memory file is another
    instruction set arriving beside them, whatever its source.
    """
    if not transcript.is_file():
        return None
    for line in transcript.read_text().splitlines():
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(message, dict):
            continue
        carried = carried_context(message)
        if carried is not None:
            return carried
    return None


def converse(
    argv: list[str],
    workspace: Path,
    env: dict[str, str],
    prompt: str,
    transcript: IO[bytes],
    timeout: float,
) -> tuple[int | str, bytes]:
    """Run the agent to its exit or its timeout; give its status and stderr."""
    process = Popen(
        argv,
        cwd=workspace,
        env=env,
        stdin=PIPE,
        stdout=transcript,
        stderr=PIPE,
        start_new_session=True,
    )
    try:
        _, stderr = process.communicate(prompt.encode(), timeout=timeout)
    except TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        _, stderr = process.communicate()
        return TIMEOUT, stderr
    return process.returncode, stderr


def start(
    session: Session,
    workflow: Workflow,
    scenario: Scenario,
    argv: list[str],
    prompt: str,
    sets: dict[tuple[str, str], dict[str, bytes]],
    records: Path,
    workspace: Path,
    env: dict[str, str],
    timeout: float,
    harness: Harness,
) -> int | None:
    """Run one session in a fresh workspace, record it, and return its tokens."""
    records.mkdir(parents=True)
    workspace.mkdir(parents=True)
    try:
        prepare(workspace, workflow, scenario, session.form, sets)
        if session.form == BOOTSTRAP_SET:
            env = {**env, "PATH": f"{workspace / BIN}:{env.get('PATH', '')}"}
        began = time.monotonic()
        with (records / TRANSCRIPT).open("wb") as transcript:
            spoke = [*argv, prompt] if harness.prompt_on_argv else argv
            exit_status, stderr = converse(
                spoke,
                workspace,
                env,
                "" if harness.prompt_on_argv else prompt,
                transcript,
                timeout,
            )
        duration = time.monotonic() - began
        if stderr:
            (records / STDERR).write_bytes(stderr)
        keep(workspace, records)
        record_starts(records / TRANSCRIPT, records, harness)
        result = harness.result(records / TRANSCRIPT)
        ran = read_trace(records)
        compiled = compiled_by(harness, records / TRANSCRIPT, session.form)
        verdict = (
            errored(workflow, scenario)
            if (result is not None and result.get("is_error"))
            or (result is None and not ran)
            else score(workflow, scenario, records, compiled)
        )
    finally:
        shutil.rmtree(workspace)
    tokens = harness.tokens(result)
    record = {
        **asdict(session),
        "command": argv,
        "exit_status": exit_status,
        "duration_seconds": round(duration, 3),
        "usage": result.get("usage") if result else None,
        "tokens": tokens,
        "cost_usd": harness.cost(result),
        "result": result,
        "trace": [asdict(entry) for entry in scenario.trace],
        "verdict": verdict.record(),
    }
    (records / SESSION).write_text(json.dumps(record, indent=2) + "\n")
    return tokens


def place_pf(workspace: Path) -> Path:
    """Put the build under test where a bootstrapping session's shell finds it.

    A session runs its own shell, whose path is the caller's and not this
    run's, so the build is copied into a folder of the workspace's own and
    that folder is named on the session's path. What a session compiles with
    is therefore the build this run was configured with, not whatever `pf` the
    host happens to hold.
    """
    found = shutil.which("pf")
    if found is None:
        raise CorpusError("no pf command is on the path to bundle a form with")
    (workspace / BIN).mkdir()
    placed = workspace / BIN / "pf"
    shutil.copy2(found, placed)
    placed.chmod(placed.stat().st_mode | 0o111)
    return workspace / BIN


def compiled_by(harness: Harness, transcript: Path, form: str) -> bool | None:
    """Whether a session compiled its material, for a form that must.

    A form outside the shell forms needs no compile, so nothing is asked. A
    shell form's session is held to having run `pf`: a command whose first
    word is `pf` or a path ending in `/pf`, since a command may be prefixed
    by a directory or a wrapper.
    """
    if FORMS[form] not in SHELL_FORMS:
        return None
    commands = harness.commands(transcript)
    if commands is None:
        return None
    for command in commands:
        for part in command.replace("&&", ";").replace("|", ";").split(";"):
            words = part.split()
            if words and words[0].rsplit("/", 1)[-1] == "pf":
                return True
    return False


def errored(workflow: Workflow, scenario: Scenario) -> Verdict:
    """The verdict on a session that entered no state and reported an error.

    An agent refused, cut off before it started, or one that printed no
    `result` message and left no trace, is no evidence of how it followed
    the workflow. It is recorded apart from a session that walked and
    stopped, which is what `unfinished` names: a session ended at its
    timeout keeps whatever trace it wrote, and is scored from it.
    """
    return Verdict(False, Failure.ERRORED, None, scenario.path, (), ())


def verdict_of(records: Path) -> dict[str, Any] | None:
    """One finished session's record, if the run wrote one."""
    path = records / SESSION
    if not path.is_file():
        return None
    held = json.loads(path.read_text())
    return held if isinstance(held, dict) else None


def failed(record: dict[str, Any] | None) -> str | None:
    """The failure class a session's record gives, or nothing where it passed."""
    if record is None:
        return None
    verdict = record.get("verdict")
    return verdict.get("failure") if isinstance(verdict, dict) else None


def agent_message(record: dict[str, Any] | None) -> dict[str, Any] | None:
    """The `result` message a session's record kept, when it kept one."""
    if record is None:
        return None
    result = record.get("result")
    return result if isinstance(result, dict) else None


def reason_of(result: dict[str, Any] | None) -> str:
    """The text the agent's `result` message carries, or a stated absence."""
    text = None if result is None else result.get("result")
    if isinstance(text, str) and text.strip():
        return text.strip()
    return "the session reported an error and printed no message"


def outcome(
    sessions: list[Session], started: list[bool], run_directory: Path
) -> tuple[str, str | None]:
    """A run's state, and the reason it records when it is refused.

    A run is refused when it started every session of its matrix and every
    one took the `errored` verdict: no session entered a state, so the
    matrix is no result. A run its budget stopped part way, and one where
    some sessions errored beside others that entered a state, is a
    completed run whose failures are the result. The reason is the first
    errored session's own `result` text, so a reader sees the limit the
    agent reported.
    """
    if not all(started):
        return COMPLETED, None
    records = [
        verdict_of(session.directory(run_directory))
        for session, began in zip(sessions, started, strict=True)
        if began
    ]
    if not records or any(failed(record) != str(Failure.ERRORED) for record in records):
        return COMPLETED, None
    return REFUSED, reason_of(agent_message(records[0]))


def run(arguments: argparse.Namespace) -> dict[str, object]:
    """Run every session the budget allows and return the run's record."""
    harness = harness_named(arguments.harness)
    command = arguments.agent_command or harness.default_agent
    agent = [str(Path(shlex.split(command)[0]).expanduser()), *shlex.split(command)[1:]]
    if not agent or shutil.which(agent[0]) is None:
        raise CorpusError(f"no agent command {command!r} is found")
    eval_root = arguments.eval_root.expanduser()
    config = eval_root / CONFIG
    refused = harness.preflight(config)
    if refused is not None:
        raise CorpusError(refused)
    env = harness.environment(config, dict(os.environ))
    corpus = workflows()
    if arguments.workflows:
        chosen = names(arguments.workflows)
        corpus = [workflow for workflow in corpus if workflow.name in chosen]
        if {workflow.name for workflow in corpus} != set(chosen):
            raise CorpusError(f"the corpus holds no workflow among {chosen}")
    forms = names(arguments.forms)
    if not set(forms) <= set(FORMS):
        raise CorpusError(f"the forms are {', '.join(FORMS)}, not {forms}")
    by_name = {workflow.name: workflow for workflow in corpus}
    sets = {
        (workflow.name, form): bundles_of(workflow, form)
        for workflow in corpus
        for form in forms
        if form in BUNDLED and FORMS[form] in workflow.forms
    }
    sessions = matrix(
        corpus, names(arguments.models), forms, arguments.repetitions, harness
    )
    unobservable = [
        f"{workflow.name}/{scenario.name}/{form}"
        for workflow in corpus
        for scenario in workflow.scenarios
        for form in forms
        if FORMS[form] in workflow.forms
        and not observable(workflow, scenario, form, harness)
    ]
    covered = len(sessions) * arguments.session_budget_tokens
    if covered > arguments.budget_tokens:
        raise CorpusError(
            f"--budget-tokens {arguments.budget_tokens} does not cover the "
            f"{len(sessions)} sessions at --session-budget-tokens "
            f"{arguments.session_budget_tokens}, which need {covered}"
        )
    began = datetime.now(UTC)
    run_id = arguments.run_id or began.strftime("%Y%m%dT%H%M%SZ")
    run_directory = arguments.results / run_id
    run_directory.mkdir(parents=True)
    workspaces = eval_root / WORKSPACES / run_id
    prompts = {form: instruction(ENTRY, FORMS[form]) for form in forms}
    ledger = Ledger(arguments.budget_tokens, arguments.session_budget_tokens)

    def attempt(session: Session) -> bool:
        if not ledger.reserve():
            return False
        workflow = by_name[session.workflow]
        scenario = next(
            item for item in workflow.scenarios if item.name == session.scenario
        )
        tokens: int | None = None
        try:
            tokens = start(
                session,
                workflow,
                scenario,
                harness.argv(
                    agent,
                    session.model,
                    ledger.session_cap,
                    session.directory(workspaces),
                ),
                prompts[session.form],
                sets,
                session.directory(run_directory),
                session.directory(workspaces),
                env,
                arguments.session_timeout_seconds,
                harness,
            )
        finally:
            ledger.settle(tokens)
        return True

    with ThreadPoolExecutor(max_workers=max(1, arguments.parallel)) as pool:
        started = list(pool.map(attempt, sessions))
    shutil.rmtree(workspaces, ignore_errors=True)
    state, reason = outcome(sessions, started, run_directory)
    carried = [
        f"{identify(session)} carried {what}"
        for session in sessions
        if (what := injected(session.directory(run_directory) / TRANSCRIPT)) is not None
    ]
    if carried:
        raise CorpusError(
            f"{len(carried)} session(s) carried context this run did not supply, "
            f"so they measure nothing about how the agent read its form: "
            f"{'; '.join(carried)}"
        )
    record = {
        "run_id": run_id,
        "date": began.isoformat(timespec="seconds"),
        "options": {
            key: str(value) if isinstance(value, Path) else value
            for key, value in vars(arguments).items()
        },
        "harness": harness.name,
        "command": harness.argv(agent, "<model>", ledger.session_cap),
        STATE: state,
        REASON: reason,
        "sessions": len(sessions),
        "started": sum(started),
        "tokens": ledger.spent,
        "tokens_unknown": ledger.unknown,
        "unobservable": unobservable,
        "not_started": [
            asdict(session)
            for session, began in zip(sessions, started, strict=True)
            if not began
        ],
    }
    (run_directory / RUN).write_text(json.dumps(record, indent=2) + "\n")
    write(run_directory, BASELINE)
    return record


def main(argv: Sequence[str] | None = None) -> int:
    """Run the eval from the command line and report what it spent."""
    record = run(options(argv))
    print(json.dumps({key: record[key] for key in SUMMARY}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
