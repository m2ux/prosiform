"""Run the diagram-following eval: give each workflow form to agent sessions.

A run starts one headless agent session per model, workflow, scenario, form
and repetition. Each session works in a fresh temporary workspace holding
only its form's material as `workflow.md`, and `inputs/` holding the
scenario's inputs, each as the value followed by a newline. The forms are:

- `bundle`: the diagram form bundled by `pf`, as one file;
- `tree`: the diagram form's source tree as it is, entered at `workflow.md`;
- `prose`: the prose form bundled by `pf`, as one file.

The session is the agent command run in its workspace with the shared
instruction on standard input, its tools limited to reading, writing and
searching files, with no MCP server and no skill. `acceptEdits` lets it
change files only within its workspace.

Sessions run under the eval root, `--eval-root`. `<root>/config/` is the
eval's own Claude configuration directory, holding its login, settings and
memory apart from the caller's; each session receives it as
`CLAUDE_CONFIG_DIR`, in an environment holding no other `CLAUDE*` or
`ANTHROPIC_*` variable. A run whose configuration directory holds no login
fails before it starts a session, naming the one-time login command.
`<root>/workspaces/<run-id>/` holds the run's workspaces, each at its
session's place in the matrix and removed once its records are kept.

Each session's records go to `results/<run-id>/<model>/<workflow>/
<scenario>/<form>/<repetition>/`: `transcript.jsonl`, the stream-json the
agent printed; `stderr.log` when it printed any; the final workspace's
`trace.log` and `actions/`; and `session.json`, holding the session's
identity, exit status, duration, the stream's `result` message with its
`usage` and `total_cost_usd`, and the scorer's verdict record. `run.json`
holds the run's date, options, recorded cost, and the sessions it did not
start. Once `run.json` is written, `report.py` writes the run's report
beside it, compared with the committed baseline.

A session runs for at most `--session-timeout-seconds`. On expiry its
process group, the agent and every process it started, is killed; its exit
status is recorded as `timeout`, and what its workspace holds by then is
kept and scored like any other session's.

The spending cap holds a run's recorded cost within `--budget-usd`. A
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
import threading
import time
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from subprocess import PIPE, Popen, TimeoutExpired
from typing import IO

from report import BASELINE, RUN, SESSION, TIMEOUT, names, write
from score import ACTIONS, TRACE, score
from workflow import (
    DIAGRAM,
    ENTRY,
    PROSE,
    ROOT,
    CorpusError,
    Scenario,
    Workflow,
    bundle,
    instruction,
    workflows,
)

RESULTS = ROOT / "results"
INPUTS = "inputs"
TRANSCRIPT = "transcript.jsonl"
STDERR = "stderr.log"
EVAL_ROOT = Path("~/projects/eval/prosiform")
CONFIG = "config"
WORKSPACES = "workspaces"
LOGIN = ".credentials.json"
CONFIG_VARIABLE = "CLAUDE_CONFIG_DIR"
SCRUBBED = ("CLAUDE", "ANTHROPIC_")

BUNDLE = "bundle"
TREE = "tree"
PROSE_BUNDLE = "prose"
FORMS = {BUNDLE: DIAGRAM, TREE: DIAGRAM, PROSE_BUNDLE: PROSE}
BUNDLED = {BUNDLE, PROSE_BUNDLE}
SUMMARY = ("run_id", "sessions", "started", "cost_usd", "not_started")

TOOLS = "Read,Write,Edit,Glob,Grep"
DEFAULT_MODELS = ("claude-haiku-5-5", "claude-sonnet-5-5")
DEFAULT_REPETITIONS = 5
DEFAULT_PARALLEL = 4
DEFAULT_SESSION_BUDGET = 0.50
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
    """The run's recorded cost and the session caps reserved in flight."""

    def __init__(self, budget: float, session_cap: float) -> None:
        self.budget = budget
        self.session_cap = session_cap
        self.spent = 0.0
        self.reserved = 0.0
        self.stopped = False
        self.condition = threading.Condition()

    def fits(self) -> bool:
        """Whether one more session's cap fits within the budget."""
        return self.spent + self.reserved + self.session_cap <= self.budget

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

    def settle(self, cost: float) -> None:
        """Replace a session's reserved cap with the cost it recorded."""
        with self.condition:
            self.reserved -= self.session_cap
            self.spent += cost
            self.condition.notify_all()


def options(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """The run's options, defaulting to the eval's full matrix."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--budget-usd", type=float, required=True, help="the run's spending cap"
    )
    parser.add_argument(
        "--session-budget-usd",
        type=float,
        default=DEFAULT_SESSION_BUDGET,
        help="each session's spending cap",
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
        "--agent-command", default="claude", help="the agent's command line"
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
    corpus: list[Workflow], models: list[str], forms: list[str], repetitions: int
) -> list[Session]:
    """Every session a run starts when its budget allows, in start order."""
    return [
        Session(model, workflow.name, scenario.name, form, repetition)
        for model in models
        for workflow in corpus
        for scenario in workflow.scenarios
        for form in forms
        for repetition in range(1, repetitions + 1)
    ]


def bundled(workflow: Workflow, form: str) -> bytes:
    """One bundled form's text, as `pf` writes it."""
    built = bundle(workflow.form(FORMS[form]))
    if built.returncode != 0 or built.stderr:
        raise CorpusError(
            f"{workflow.name}: pf bundled the {form} form with exit "
            f"{built.returncode} and {built.stderr.decode()!r}"
        )
    return built.stdout


def prepare(
    workspace: Path,
    workflow: Workflow,
    scenario: Scenario,
    form: str,
    bundles: dict[tuple[str, str], bytes],
) -> None:
    """Lay out a workspace with one form's material and a scenario's inputs."""
    if form in BUNDLED:
        (workspace / ENTRY).write_bytes(bundles[(workflow.name, form)])
    else:
        shutil.copytree(workflow.form(FORMS[form]), workspace, dirs_exist_ok=True)
    (workspace / INPUTS).mkdir()
    for name, value in scenario.inputs.items():
        (workspace / INPUTS / name).write_text(f"{value}\n")


def agent_argv(agent: list[str], model: str, session_cap: float) -> list[str]:
    """The command line one session runs, its prompt given on standard input."""
    return [
        *agent,
        "-p",
        "--model",
        model,
        "--output-format",
        "stream-json",
        "--verbose",
        "--tools",
        TOOLS,
        "--permission-mode",
        "acceptEdits",
        "--no-session-persistence",
        "--strict-mcp-config",
        "--disable-slash-commands",
        "--max-budget-usd",
        str(session_cap),
    ]


def result_message(transcript: Path) -> dict[str, object] | None:
    """The stream's last `result` message, if it printed one."""
    found = None
    for line in transcript.read_text().splitlines():
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(message, dict) and message.get("type") == "result":
            found = message
    return found


def keep(workspace: Path, records: Path) -> None:
    """Copy what the scorer reads out of a finished workspace."""
    if (workspace / TRACE).is_file():
        shutil.copy2(workspace / TRACE, records / TRACE)
    if (workspace / ACTIONS).is_dir():
        shutil.copytree(workspace / ACTIONS, records / ACTIONS)


def environment(config: Path) -> dict[str, str]:
    """The caller's environment without its Claude variables, naming `config`."""
    kept = {
        name: value
        for name, value in os.environ.items()
        if not name.startswith(SCRUBBED)
    }
    return {**kept, CONFIG_VARIABLE: str(config)}


def preflight(config: Path) -> None:
    """Refuse a run whose configuration directory holds no login."""
    if not (config / LOGIN).is_file():
        raise CorpusError(
            f"{config} holds no login; log in once with "
            f"`{CONFIG_VARIABLE}={config} claude`, then `/login`"
        )


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
    bundles: dict[tuple[str, str], bytes],
    records: Path,
    workspace: Path,
    env: dict[str, str],
    timeout: float,
) -> float | None:
    """Run one session in a fresh workspace, record it, and return its cost."""
    records.mkdir(parents=True)
    workspace.mkdir(parents=True)
    try:
        prepare(workspace, workflow, scenario, session.form, bundles)
        began = time.monotonic()
        with (records / TRANSCRIPT).open("wb") as transcript:
            exit_status, stderr = converse(
                argv, workspace, env, prompt, transcript, timeout
            )
        duration = time.monotonic() - began
        if stderr:
            (records / STDERR).write_bytes(stderr)
        keep(workspace, records)
        verdict = score(workflow, scenario, workspace)
    finally:
        shutil.rmtree(workspace)
    result = result_message(records / TRANSCRIPT)
    cost = result.get("total_cost_usd") if result else None
    cost = float(cost) if isinstance(cost, int | float) else None
    record = {
        **asdict(session),
        "command": argv,
        "exit_status": exit_status,
        "duration_seconds": round(duration, 3),
        "usage": result.get("usage") if result else None,
        "cost_usd": cost,
        "result": result,
        "verdict": verdict.record(),
    }
    (records / SESSION).write_text(json.dumps(record, indent=2) + "\n")
    return cost


def run(arguments: argparse.Namespace) -> dict[str, object]:
    """Run every session the budget allows and return the run's record."""
    agent = shlex.split(arguments.agent_command)
    if not agent or shutil.which(agent[0]) is None:
        raise CorpusError(f"no agent command {arguments.agent_command!r} is found")
    eval_root = arguments.eval_root.expanduser()
    config = eval_root / CONFIG
    preflight(config)
    env = environment(config)
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
    bundles = {
        (workflow.name, form): bundled(workflow, form)
        for workflow in corpus
        for form in forms
        if form in BUNDLED
    }
    sessions = matrix(corpus, names(arguments.models), forms, arguments.repetitions)
    began = datetime.now(UTC)
    run_id = arguments.run_id or began.strftime("%Y%m%dT%H%M%SZ")
    run_directory = arguments.results / run_id
    run_directory.mkdir(parents=True)
    workspaces = eval_root / WORKSPACES / run_id
    prompt = instruction(ENTRY)
    ledger = Ledger(arguments.budget_usd, arguments.session_budget_usd)

    def attempt(session: Session) -> bool:
        if not ledger.reserve():
            return False
        workflow = by_name[session.workflow]
        scenario = next(
            item for item in workflow.scenarios if item.name == session.scenario
        )
        cost: float | None = None
        try:
            cost = start(
                session,
                workflow,
                scenario,
                agent_argv(agent, session.model, ledger.session_cap),
                prompt,
                bundles,
                session.directory(run_directory),
                session.directory(workspaces),
                env,
                arguments.session_timeout_seconds,
            )
        finally:
            ledger.settle(ledger.session_cap if cost is None else cost)
        return True

    with ThreadPoolExecutor(max_workers=max(1, arguments.parallel)) as pool:
        started = list(pool.map(attempt, sessions))
    shutil.rmtree(workspaces, ignore_errors=True)
    record = {
        "run_id": run_id,
        "date": began.isoformat(timespec="seconds"),
        "options": {
            key: str(value) if isinstance(value, Path) else value
            for key, value in vars(arguments).items()
        },
        "command": agent_argv(agent, "<model>", ledger.session_cap),
        "sessions": len(sessions),
        "started": sum(started),
        "cost_usd": ledger.spent,
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
