"""Hold the runner to its sessions, its records, its spending cap and its classes.

Every run here starts the stub agent beside this file in place of the real
one, so no test starts a paid session. The stub writes what it found in its
workspace to a log, walks the workflow it finds there, and reports a cost
the test chooses.

The dispatch corpus is also held as a matrix: each departure the stub can
state runs every dispatch scenario in both forms, and each cell is asserted
against the class that departure predicts, so a check that fires for the
wrong reason fails where it fires.
"""

import json
import sys
import time
from pathlib import Path
from typing import Any

import pytest
from harness import DONE, HARNESSES
from report import REPORT_JSON, REPORT_MD, RUN, SESSION, TIMEOUT, main
from run import (
    AUTHORED_SET,
    BUNDLE,
    BUNDLED,
    COMPILED_SET,
    FORMS,
    LINKED_TREE,
    PROSE_BUNDLE,
    TRANSCRIPT,
    Ledger,
    Session,
    bundles_of,
    injected,
    matrix,
    observable,
    options,
    run,
)
from score import (
    ACTIONS,
    SUBAGENTS,
    TRACE,
    Failure,
    Start,
    read_starts,
)
from workflow import (
    ENTRY,
    ENTRY_BUNDLE,
    LINKED_FORM,
    CorpusError,
    workflows,
)

STUB = Path(__file__).resolve().parent / "stub_agent.py"
CORPUS = {workflow.name: workflow for workflow in workflows()}
CALLER_VARIABLES = (
    "CLAUDECODE",
    "CLAUDE_CODE_ENTRYPOINT",
    "CLAUDE_CONFIG_DIR",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
)
DISPATCHING = ("dispatch-beside", "dispatch-chain", "dispatch-question", "dispatch-set")
DISPATCH_FORMS = (COMPILED_SET, AUTHORED_SET)
DISPATCH_SCENARIOS = tuple(
    scenario.name for name in DISPATCHING for scenario in CORPUS[name].scenarios
)
"""The dispatch corpus's scenario names, one per dispatch workflow."""

DEPARTURES: dict[str, tuple[str, dict[str, Failure | None]]] = {
    "STUB_AGENT_NO_DISPATCH": (
        "1",
        dict.fromkeys(DISPATCH_SCENARIOS, Failure.UNDISPATCHED),
    ),
    "STUB_AGENT_SEQUENTIAL": (
        "1",
        {
            "chain": None,
            "parallel-set": Failure.SEQUENTIAL_SET,
            "set-beside-a-dispatch": Failure.SEQUENTIAL_SET,
            "returned-question": None,
        },
    ),
    "STUB_AGENT_ANSWER": (
        DONE,
        {
            "chain": None,
            "parallel-set": None,
            "set-beside-a-dispatch": None,
            "returned-question": Failure.UNRELAYED_QUESTION,
        },
    ),
    "STUB_AGENT_STOP": ("1", dict.fromkeys(DISPATCH_SCENARIOS, Failure.UNFINISHED)),
}
"""Each departure script, the value it reads, and the class it predicts per cell.

A script states one departure, and a scenario states which of the checks that
departure changes. A scenario whose trace the departure leaves as the
scenario states predicts a pass, so a class that fires where its departure is
absent fails here as surely as one that does not fire where it is present.
"""


def every_session(models: list[str], forms: list[str], repetitions: int) -> int:
    """The sessions a run of the whole corpus starts."""
    return len(matrix(list(CORPUS.values()), models, forms, repetitions))


def test_a_matrix_holds_no_cell_a_harness_cannot_observe() -> None:
    """A scenario whose trace outruns the path's own starts is beyond Cursor."""
    corpus = list(CORPUS.values())
    forms = [COMPILED_SET, AUTHORED_SET]
    cursor = matrix(corpus, ["m"], forms, 1, HARNESSES["cursor"])
    claude = matrix(corpus, ["m"], forms, 1, HARNESSES["claude"])
    assert len(cursor) < len(claude)
    assert all(item.workflow != "dispatch-chain" for item in cursor)
    assert any(item.workflow == "dispatch-chain" for item in claude)
    workflow = CORPUS["dispatch-set"]
    scenario = workflow.scenarios[0]
    assert observable(workflow, scenario, COMPILED_SET, HARNESSES["cursor"]) is True


@pytest.fixture
def log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The directory the stub agent writes what it saw to, one file a session."""
    directory = tmp_path / "log"
    directory.mkdir()
    monkeypatch.setenv("STUB_AGENT_LOG", str(directory))
    for name in CALLER_VARIABLES:
        monkeypatch.setenv(name, "caller")
    login = tmp_path / "eval" / "config" / ".credentials.json"
    login.parent.mkdir(parents=True)
    login.touch()
    return directory


def eval_run(tmp_path: Path, *extra: str) -> dict[str, Any]:
    """A run of one model through the stub agent, its records under tmp_path."""
    return run(
        options(
            [
                "--agent-command",
                f"{sys.executable} {STUB}",
                "--models",
                "stub-model",
                "--results",
                str(tmp_path / "results"),
                "--run-id",
                "test",
                "--eval-root",
                str(tmp_path / "eval"),
                "--session-budget-tokens",
                "250",
                *extra,
            ]
        )
    )


def seen(log: Path) -> list[dict[str, Any]]:
    """What each session the stub agent ran in found on starting."""
    return [json.loads(path.read_text()) for path in sorted(log.iterdir())]


def records(tmp_path: Path) -> list[dict[str, Any]]:
    """Every session record the test run wrote."""
    sessions = sorted((tmp_path / "results" / "test").rglob(SESSION))
    return [json.loads(path.read_text()) for path in sessions]


def material(session: Session) -> set[str]:
    """The files a session's workspace holds on starting.

    A bundled form's entry bundle is `workflow.md`, and every other bundle
    of its set sits beside it under the name `pf` gave it. A form read as a
    source tree gives its own files.
    """
    workflow = CORPUS[session.workflow]
    scenario = next(i for i in workflow.scenarios if i.name == session.scenario)
    inputs = {f"inputs/{name}" for name in scenario.inputs}
    if session.form in BUNDLED:
        return (
            {ENTRY}
            | inputs
            | {
                name
                for name in bundles_of(workflow, session.form)
                if name != ENTRY_BUNDLE.name
            }
        )
    tree = workflow.form(FORMS[session.form])
    return {
        str(path.relative_to(tree)) for path in tree.rglob("*") if path.is_file()
    } | inputs


def test_the_matrix_holds_one_session_per_model_form_scenario_and_repetition() -> None:
    sessions = matrix(list(CORPUS.values()), ["a", "b"], list(FORMS), 5)
    assert (
        len(sessions) == len(set(sessions)) == every_session(["a", "b"], list(FORMS), 5)
    )
    assert len(sessions) == 2 * 5 * 28


def test_each_session_starts_in_a_fresh_workspace_of_its_form_and_inputs(
    tmp_path: Path, log: Path
) -> None:
    record = eval_run(
        tmp_path, "--repetitions", "2", "--budget-tokens", "100000", "--parallel", "3"
    )
    sessions = matrix(list(CORPUS.values()), ["stub-model"], list(FORMS), 2)
    workspaces = (tmp_path / "eval" / "workspaces" / "test").resolve()
    expected = every_session(["stub-model"], list(FORMS), 2)
    assert record["started"] == len(sessions) == expected
    entries = seen(log)
    assert len(entries) == len(sessions)
    assert len({entry["workspace"] for entry in entries}) == len(sessions)
    found = sorted(sorted(entry["files"]) for entry in entries)
    assert found == sorted(sorted(material(session)) for session in sessions)
    for entry in entries:
        argv = entry["argv"]
        assert argv[argv.index("--tools") + 1] == "Read,Write,Edit,Glob,Grep,Task"
        assert "--strict-mcp-config" in argv and "--disable-slash-commands" in argv
        assert "--mcp-config" not in argv and "--bare" not in argv
        assert "--allowedTools" not in argv and "Bash" not in " ".join(argv)
        assert ENTRY in entry["prompt"]
        assert Path(entry["workspace"]).is_relative_to(workspaces)
        assert not Path(entry["workspace"]).exists()
        assert entry["config"] == str(tmp_path / "eval" / "config")
        variables = set(entry["variables"])
        assert not variables & (set(CALLER_VARIABLES) - {"CLAUDE_CONFIG_DIR"})
        assert not any(
            name.startswith(("CLAUDE_CODE_", "ANTHROPIC_")) for name in variables
        )
    assert not workspaces.exists()


def test_a_bundled_form_is_one_file_and_the_tree_its_sources(
    tmp_path: Path, log: Path
) -> None:
    """A bundled form gives its set, a tree form its source documents."""
    eval_run(
        tmp_path,
        "--workflows",
        "looping",
        "--repetitions",
        "1",
        "--budget-tokens",
        "4000",
    )
    looping = CORPUS["looping"]
    tree_document = f"states/{looping.diagram.start.lower()}.md"
    bundle_entries = [
        entry
        for entry in seen(log)
        if sorted(name for name in entry["files"] if name.endswith(".md")) == [ENTRY]
    ]
    tree_entries = [entry for entry in seen(log) if tree_document in entry["files"]]
    assert len(bundle_entries) == 2 * len(looping.scenarios)
    assert len(tree_entries) == 2 * len(looping.scenarios)


def test_a_compiled_form_gives_its_whole_bundle_set(tmp_path: Path, log: Path) -> None:
    """A dispatching bundle set reaches the session with every bundle it names."""
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-chain", "--forms", COMPILED_SET),
        *("--repetitions", "1", "--budget-tokens", "4000"),
    )
    [workflow] = [CORPUS["dispatch-chain"]]
    published = (
        name for name in bundles_of(workflow, COMPILED_SET) if name != ENTRY_BUNDLE.name
    )
    expected = {ENTRY, *published}
    for entry in seen(log):
        assert expected <= set(entry["files"])


def test_the_linked_form_walks_every_scenario_of_a_branching_workflow(
    tmp_path: Path, log: Path
) -> None:
    """Both `branching` scenarios reach the path their inputs determine.

    The session's workspace is the linked form's own source tree, so the
    rule document each decision links is present and the stub finds the
    state headings there rather than in a bundle.
    """
    eval_run(
        tmp_path,
        *("--workflows", "branching", "--forms", LINKED_TREE, "--repetitions", "1"),
        *("--budget-tokens", "4000"),
    )
    written = records(tmp_path)
    assert len(written) == len(CORPUS["branching"].scenarios)
    linked = CORPUS["branching"].form(LINKED_FORM)
    rules = {str(path.relative_to(linked)) for path in (linked / "rules").iterdir()}
    assert rules == {"rules/escalation.md", "rules/queue.md"}
    held = {tuple(sorted(entry["files"])) for entry in seen(log)}
    for files in held:
        assert "workflow.md" in files
        assert {"states/triage.md", "states/intake.md"} <= set(files)
        assert rules <= set(files), "the linked form's rule documents are absent"
        assert "scenarios.toml" not in files
    for record in written:
        assert record["form"] == LINKED_TREE
        assert record["verdict"]["passed"] is True, record["verdict"]
        assert record["verdict"]["actual"] == record["verdict"]["expected"]


def test_the_linked_form_walks_every_scenario_of_a_looping_workflow(
    tmp_path: Path, log: Path
) -> None:
    """Both `looping` scenarios reach the path their inputs determine."""
    eval_run(
        tmp_path,
        *("--workflows", "looping", "--forms", LINKED_TREE, "--repetitions", "1"),
        *("--budget-tokens", "4000"),
    )
    written = records(tmp_path)
    assert len(written) == len(CORPUS["looping"].scenarios)
    linked = CORPUS["looping"].form(LINKED_FORM)
    rules = {str(path.relative_to(linked)) for path in (linked / "rules").iterdir()}
    assert rules == {"rules/rework.md", "rules/release.md"}
    held = {tuple(sorted(entry["files"])) for entry in seen(log)}
    for files in held:
        assert "workflow.md" in files
        assert {"states/draft.md", "states/review.md"} <= set(files)
        assert rules <= set(files), "the linked form's rule documents are absent"
        assert "scenarios.toml" not in files
    for record in written:
        assert record["form"] == LINKED_TREE
        assert record["verdict"]["passed"] is True, record["verdict"]
        assert record["verdict"]["actual"] == record["verdict"]["expected"]


def test_each_session_records_its_transcript_usage_cost_and_verdict(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_TOKENS", "125")
    eval_run(tmp_path, "--repetitions", "1", "--budget-tokens", "100000")
    written = records(tmp_path)
    assert len(written) == every_session(["stub-model"], list(FORMS), 1)
    for record in written:
        session = Session(
            record["model"],
            record["workflow"],
            record["scenario"],
            record["form"],
            record["repetition"],
        )
        directory = session.directory(tmp_path / "results" / "test")
        transcript = (directory / TRANSCRIPT).read_text().splitlines()
        assert json.loads(transcript[-1]) == record["result"]
        assert record["exit_status"] == 0
        assert record["tokens"] == 125
        trace = (directory / TRACE).read_text().split()
        assert record["usage"] == {"input_tokens": 125, "output_tokens": 0}
        verdict = record["verdict"]
        assert verdict["passed"] is True
        assert trace == verdict["actual"]
        action_files = {path.name for path in (directory / ACTIONS).iterdir()}
        workflow = CORPUS[session.workflow]
        assert action_files == {workflow.walked[state].action[0] for state in trace}


def test_a_failing_session_is_recorded_with_its_failure(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_STOP", "1")
    eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    [record] = records(tmp_path)
    verdict = record["verdict"]
    assert verdict["failure"] == "unfinished"
    assert verdict["actual"] == ["Plan"]


def test_a_run_ends_by_writing_its_report(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_TOKENS", "125")
    eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "2"),
        *("--budget-tokens", "1000"),
    )
    written = json.loads((tmp_path / "results" / "test" / REPORT_JSON).read_text())
    [cell] = written["cells"]
    assert (cell["model"], cell["form"], cell["scenario"]) == (
        "stub-model",
        BUNDLE,
        "straight-through",
    )
    assert (cell["sessions"], cell["passed"], cell["tokens"]) == (2, 2, 125)
    assert written["tokens"] == 250 and written["not_started"] == []


def test_a_budget_short_of_every_session_at_its_cap_starts_no_session(
    tmp_path: Path, log: Path
) -> None:
    with pytest.raises(
        CorpusError,
        match=r"--budget-tokens 500 does not cover the 12 sessions at "
        r"--session-budget-tokens 250, which need 3000",
    ):
        eval_run(
            tmp_path,
            *("--workflows", "linear,branching", "--repetitions", "1"),
            "--budget-tokens",
            "500",
        )
    assert seen(log) == []
    assert not (tmp_path / "results").exists()


def test_a_run_whose_sessions_pass_their_cap_stops_starting_sessions(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_TOKENS", "500")
    record = eval_run(
        tmp_path,
        *("--repetitions", "1", "--parallel", "1"),
        *("--budget-tokens", "7000", "--session-budget-tokens", "250"),
    )
    sessions = matrix(list(CORPUS.values()), ["stub-model"], list(FORMS), 1)
    assert record["started"] == 14
    assert record["tokens"] == 7000
    assert len(seen(log)) == len(records(tmp_path)) == 14
    not_started = record["not_started"]
    assert not_started == [
        {
            "model": session.model,
            "workflow": session.workflow,
            "scenario": session.scenario,
            "form": session.form,
            "repetition": session.repetition,
        }
        for session in sessions[14:]
    ]
    written = json.loads((tmp_path / "results" / "test" / RUN).read_text())
    assert written["not_started"] == not_started


def test_a_session_in_flight_holds_its_cap_against_the_budget() -> None:
    ledger = Ledger(500, 250)
    assert ledger.reserve() and ledger.reserve()
    assert not ledger.fits()
    ledger.settle(100)
    assert not ledger.fits()
    ledger.settle(100)
    assert ledger.fits()


def test_a_session_reporting_no_cost_is_charged_its_cap(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_SILENT", "1")
    record = eval_run(
        tmp_path,
        *("--repetitions", "1", "--parallel", "1", "--forms", PROSE_BUNDLE),
        *("--budget-tokens", "1250", "--session-budget-tokens", "250"),
    )
    assert record["started"] == 5
    assert record["tokens"] == 0
    assert record["tokens_unknown"] == 5
    assert all(item["tokens"] is None for item in records(tmp_path))


def test_a_refused_agent_is_errored_not_a_trace_failure(
    tmp_path: Path, log: Path
) -> None:
    """An agent that entered no state is recorded apart from one that stopped."""
    record = eval_run(
        tmp_path,
        *("--agent-command", f"{sys.executable} -c 'import sys; sys.exit(1)'"),
        *("--workflows", "linear", "--forms", LINKED_TREE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    assert record["started"] == 1
    [written] = records(tmp_path)
    assert written["verdict"]["failure"] == "errored"
    assert written["verdict"]["actual"] == []


def test_an_agent_reporting_an_error_is_errored_though_it_wrote_a_trace(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A refusal mid-run is `errored`, not a workflow the agent stopped short."""
    monkeypatch.setenv("STUB_AGENT_ERROR", "1")
    eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    [record] = records(tmp_path)
    assert record["exit_status"] == 0
    assert record["verdict"]["failure"] == "errored"


def test_a_run_whose_every_session_errored_is_refused_and_reported_as_such(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A spent login is a refused run, not a matrix of failing agents.

    Every session reports an error, so none entered a state. The run records
    itself refused with one session's own message as the reason, and its
    report names that instead of giving pass rates or a baseline comparison.
    """
    monkeypatch.setenv("STUB_AGENT_ERROR", "1")
    monkeypatch.setenv("STUB_AGENT_REASON", "You've hit your weekly limit")
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "2"),
        *("--budget-tokens", "4000"),
    )
    written = json.loads((tmp_path / "results" / "test" / RUN).read_text())
    assert record["state"] == written["state"] == "refused"
    assert written["reason"] == "You've hit your weekly limit"
    assert record["started"] == written["sessions"] == 2
    assert all(item["verdict"]["failure"] == "errored" for item in records(tmp_path))
    built = json.loads((tmp_path / "results" / "test" / REPORT_JSON).read_text())
    assert built["state"] == "refused"
    assert built["reason"] == "You've hit your weekly limit"
    for name in ("cells", "by_form", "by_model"):
        assert built[name] == [] and built["baseline_only"][name] == []
    assert built["baseline"] is None
    text = (tmp_path / "results" / "test" / REPORT_MD).read_text()
    assert "- **State:** `refused`" in text
    assert "You've hit your weekly limit" in text
    assert "not compared" in text and "Pass rate" not in text


def test_a_refused_run_writes_no_baseline(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_ERROR", "1")
    eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    baseline = tmp_path / "baseline.json"
    with pytest.raises(CorpusError, match="refused, so it has no cells"):
        main(
            [
                str(tmp_path / "results" / "test"),
                "--baseline",
                str(baseline),
                "--write-baseline",
            ]
        )
    assert not baseline.exists()


def test_a_run_with_a_genuine_mix_of_errors_and_states_is_a_result(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A real fault beside sessions that entered a state is not a refusal."""
    monkeypatch.setenv("STUB_AGENT_ERROR_ONCE", str(tmp_path / "errored"))
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "2"),
        *("--parallel", "1", "--budget-tokens", "4000"),
    )
    failures = [item["verdict"]["failure"] for item in records(tmp_path)]
    assert sorted(failures, key=str) == [None, "errored"]
    assert record["state"] == "completed" and record["reason"] is None
    written = json.loads((tmp_path / "results" / "test" / REPORT_JSON).read_text())
    assert written["state"] == "completed"
    assert written["cells"] and written["cells"][0]["passed"] == 1


def test_a_run_the_budget_stopped_part_way_is_not_refused(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Sessions it never started leave the matrix incomplete, not refused."""
    monkeypatch.setenv("STUB_AGENT_ERROR", "1")
    monkeypatch.setenv("STUB_AGENT_TOKENS", "500")
    record = eval_run(
        tmp_path,
        *("--repetitions", "1", "--parallel", "1", "--forms", PROSE_BUNDLE),
        *("--budget-tokens", "1250", "--session-budget-tokens", "250"),
    )
    assert record["started"] == 3 and record["sessions"] == 5
    assert len(record["not_started"]) == 2
    assert all(item["verdict"]["failure"] == "errored" for item in records(tmp_path))
    assert record["state"] == "completed" and record["reason"] is None


def test_a_run_without_a_login_starts_no_session(tmp_path: Path, log: Path) -> None:
    (tmp_path / "eval" / "config" / ".credentials.json").unlink()
    with pytest.raises(CorpusError, match="holds no login.*claude`, then `/login`"):
        eval_run(tmp_path, "--budget-tokens", "1000")
    assert seen(log) == []
    assert not (tmp_path / "results").exists()


def test_a_session_past_its_timeout_is_ended_scored_and_charged(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_HANG", str(tmp_path / "hung"))
    monkeypatch.setenv("STUB_AGENT_STOP", "2")
    monkeypatch.setenv("STUB_AGENT_TOKENS", "125")
    began = time.monotonic()
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "2"),
        *("--parallel", "1", "--session-timeout-seconds", "1"),
        *("--budget-tokens", "1000", "--session-budget-tokens", "250"),
    )
    assert time.monotonic() - began < 60
    assert record["started"] == 2 and record["not_started"] == []
    assert record["tokens"] == 125
    assert record["tokens_unknown"] == 1
    hung, finished = sorted(records(tmp_path), key=lambda item: item["repetition"])
    assert hung["exit_status"] == TIMEOUT and hung["tokens"] is None
    assert hung["verdict"]["failure"] == "unfinished"
    assert hung["verdict"]["actual"] == ["Plan", "Build"]
    assert finished["exit_status"] == 0 and finished["tokens"] == 125


def test_the_context_read_finds_each_form_of_injected_context(
    tmp_path: Path,
) -> None:
    """A hook response, an appended prompt and a memory file all read as carried."""
    transcript = tmp_path / TRANSCRIPT
    cases = (
        ("a hook response", {"type": "system", "subtype": "hook_response"}),
        (
            "an appended system prompt",
            {
                "type": "system",
                "subtype": "init",
                "appendSystemPrompt": "obey another repository's rules",
            },
        ),
        (
            "a memory file",
            {
                "type": "system",
                "subtype": "init",
                "memory": "another repository's rules",
            },
        ),
    )
    for kind, message in cases:
        transcript.write_text(json.dumps(message) + "\n")
        carried = injected(transcript)
        assert carried is not None and carried.startswith(kind), (kind, carried)

    transcript.write_text(
        "\n".join(
            json.dumps(message)
            for message in (
                {"type": "system", "subtype": "init", "cwd": "/tmp"},
                {"type": "assistant", "message": {"content": ["Plan"]}},
                {"type": "result", "subtype": "success"},
            )
        )
    )
    assert injected(transcript) is None
    assert injected(tmp_path / "absent.jsonl") is None


def test_a_run_whose_config_installs_a_plugin_hook_starts_no_session(
    tmp_path: Path, log: Path
) -> None:
    """The config directory's plugin is refused before the first session.

    A plugin's `SessionStart` hook reaches a session before its first turn,
    and no flag the runner passes suppresses it, so a directory holding one
    is a run the eval cannot measure a form in.
    """
    installed = tmp_path / "eval" / "config" / "plugins" / "installed_plugins.json"
    installed.parent.mkdir(parents=True)
    installed.write_text(
        json.dumps(
            {
                "version": 2,
                "plugins": {
                    "other-rules@elsewhere": [{"scope": "managed", "version": "0.1.0"}]
                },
            }
        )
    )
    with pytest.raises(CorpusError, match="installs a plugin.*remove .*installed"):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
            "--budget-tokens",
            "1000",
        )
    assert seen(log) == []
    assert not (tmp_path / "results").exists()


def test_a_run_whose_remote_settings_enable_a_plugin_starts_no_session(
    tmp_path: Path, log: Path
) -> None:
    """The plugin need not be installed here for its settings to be refused."""
    remote = tmp_path / "eval" / "config" / "remote-settings.json"
    remote.write_text(
        json.dumps(
            {
                "enabledPlugins": {"other-rules@elsewhere": True},
                "env": {"CLAUDE_CODE_ENABLE_TELEMETRY": "1"},
            }
        )
    )
    with pytest.raises(CorpusError, match="enables a plugin.*remove .*remote-settings"):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
            "--budget-tokens",
            "1000",
        )
    assert seen(log) == []
    assert not (tmp_path / "results").exists()


def test_a_config_with_no_plugin_starts_every_session(
    tmp_path: Path, log: Path
) -> None:
    """A plugin listed but not enabled, and an empty enable map, are clean."""
    plugins = tmp_path / "eval" / "config" / "plugins" / "installed_plugins.json"
    plugins.parent.mkdir(parents=True)
    plugins.write_text(json.dumps({"version": 2, "plugins": {}}))
    (tmp_path / "eval" / "config" / "remote-settings.json").write_text(
        json.dumps({"enabledPlugins": {}})
    )
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    assert record["started"] == 1
    assert len(seen(log)) == 1


def test_a_run_whose_settings_file_declares_a_hook_starts_no_session(
    tmp_path: Path, log: Path
) -> None:
    """The directory's own settings file is refused before the first session.

    A `hooks` block in `settings.json` delivers a `SessionStart` command
    without installing a plugin, so the two files the preflight reads are
    no bound on what reaches a session. The refusal names the file and
    each event it declares, since either one arrives before the first turn.
    """
    settings = tmp_path / "eval" / "config" / "settings.json"
    settings.write_text(
        json.dumps(
            {
                "theme": "dark",
                "hooks": {
                    "SessionStart": [
                        {"hooks": [{"type": "command", "command": "cat rules.md"}]}
                    ],
                    "PreToolUse": [
                        {"hooks": [{"type": "command", "command": "audit.sh"}]}
                    ],
                },
            }
        )
    )
    with pytest.raises(
        CorpusError,
        match=r"settings\.json declares a hook for PreToolUse, SessionStart.*"
        r"remove .*settings\.json before this run",
    ):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
            *("--budget-tokens", "1000"),
        )
    assert seen(log) == []
    assert not (tmp_path / "results").exists()


def test_a_run_whose_settings_file_holds_only_preferences_starts_its_session(
    tmp_path: Path, log: Path
) -> None:
    """A settings file the eval may write itself is no refusal."""
    (tmp_path / "eval" / "config" / "settings.json").write_text(
        json.dumps({"theme": "dark", "model": "claude-haiku-5-5"})
    )
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    assert record["started"] == 1
    assert len(seen(log)) == 1


def test_a_settings_file_that_is_not_json_is_refused(tmp_path: Path, log: Path) -> None:
    """A malformed settings file is refused as the other two files are."""
    (tmp_path / "eval" / "config" / "settings.json").write_text("{not json")
    with pytest.raises(CorpusError, match=r"settings\.json is not JSON"):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
            *("--budget-tokens", "1000"),
        )
    assert seen(log) == [] and not (tmp_path / "results").exists()


def test_a_session_carrying_injected_context_fails_the_run(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A hook response the run did not supply is context it cannot measure through."""
    injected = "For work in elsewhere repositories, apply its rules skill"
    monkeypatch.setenv("STUB_AGENT_INJECT", injected)
    with pytest.raises(
        CorpusError,
        match=r"1 session\(s\) carried context this run did not supply.*carried a "
        r"hook response carrying .*apply its rules skill",
    ):
        eval_run(
            tmp_path,
            *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
            *("--budget-tokens", "1000"),
        )
    [entry] = seen(log)
    assert entry["config"] == str(tmp_path / "eval" / "config")


def test_a_run_naming_every_carrying_session_starts_its_sessions(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The refusal names each session that carried context, not only the first."""
    monkeypatch.setenv("STUB_AGENT_INJECT", "another repository's rules")
    with pytest.raises(CorpusError) as raised:
        eval_run(
            tmp_path,
            *("--workflows", "linear,branching", "--forms", BUNDLE),
            *("--repetitions", "1", "--budget-tokens", "4000"),
        )
    message = str(raised.value)
    assert "3 session(s)" in message
    assert message.count("stub-model/linear/straight-through/bundle/1") == 1
    assert not (tmp_path / "results" / "test" / RUN).exists()


@pytest.mark.parametrize(
    ("workflow", "form"),
    [
        (workflow, form)
        for workflow in DISPATCHING
        for form in (COMPILED_SET, AUTHORED_SET)
    ],
    ids=lambda item: str(item),
)
def test_a_dispatch_scenario_takes_a_session_in_each_of_its_forms(
    tmp_path: Path, log: Path, workflow: str, form: str
) -> None:
    """AC1: each dispatch scenario runs in its compiled and authored forms."""
    eval_run(
        tmp_path,
        *("--workflows", workflow, "--forms", form),
        *("--repetitions", "1", "--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    assert (record["workflow"], record["form"]) == (workflow, form)
    assert record["verdict"]["passed"] is True, record["verdict"]
    assert record["verdict"]["actual"] == record["verdict"]["expected"]
    [scenario] = CORPUS[workflow].scenarios
    assert record["trace"] == [
        {
            "section": entry.section,
            "returned": entry.returned,
            "together": entry.together,
        }
        for entry in scenario.trace
    ]


def test_the_report_gives_each_dispatch_scenarios_pass_rate_per_model_and_form(
    tmp_path: Path, log: Path
) -> None:
    """AC2: the report holds one cell per dispatch scenario, model and form.

    The run takes two models over the four dispatch scenarios in both
    forms, two repetitions each, the stub agent passing every session, so
    each cell reads two sessions and a pass rate of one. A second run over
    the compiled form stops its agent after one state, so its cells read a
    run that did not complete, and the report's per-scenario cells separate
    the rates the two forms give.
    """
    record = eval_run(
        tmp_path,
        *("--models", "stub-a,stub-b"),
        *("--workflows", ",".join(DISPATCHING)),
        *("--repetitions", "2", "--budget-tokens", "20000"),
    )
    built = json.loads((tmp_path / "results" / "test" / REPORT_JSON).read_text())
    assert record["started"] == built["sessions"] == 2 * 4 * 2 * 2
    assert built["state"] == "completed"
    cells = {
        (cell["model"], cell["form"], cell["workflow"], cell["scenario"]): cell
        for cell in built["cells"]
    }
    assert len(cells) == 2 * 2 * 4
    for workflow in DISPATCHING:
        [scenario] = CORPUS[workflow].scenarios
        for model in ("stub-a", "stub-b"):
            for form in (COMPILED_SET, AUTHORED_SET):
                cell = cells[(model, form, workflow, scenario.name)]
                assert (cell["sessions"], cell["passed"]) == (2, 2)
                assert cell["pass_rate"] == 1.0
    text = (tmp_path / "results" / "test" / REPORT_MD).read_text()
    assert text.count("| 100% |") >= 2 * 2 * 4


def session_of(record: dict[str, Any]) -> Session:
    """The session a record was written for."""
    return Session(
        record["model"],
        record["workflow"],
        record["scenario"],
        record["form"],
        record["repetition"],
    )


def test_a_dispatch_session_records_its_sub_agents_beside_its_trace(
    tmp_path: Path, log: Path
) -> None:
    """AC3: the record sits beside the trace and the cost the session recorded.

    A session's sub-agent starts are read from its transcript as it settles
    and written to `subagents.json`, so the scorer reads the record rather
    than opening the transcript again. Each entry names the section the
    sub-agent followed, what it returned and whether it started beside the
    entry above it, and the session passes on its path and its record.
    """
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-question"),
        *("--forms", COMPILED_SET, "--repetitions", "1"),
        *("--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    directory = session_of(record).directory(tmp_path / "results" / "test")
    assert {SUBAGENTS, TRACE, SESSION, TRANSCRIPT} <= {
        path.name for path in directory.iterdir()
    }
    [scenario] = CORPUS["dispatch-question"].scenarios
    assert read_starts(directory) == tuple(
        Start(entry.section, entry.returned, entry.together) for entry in scenario.trace
    )
    assert record["verdict"]["passed"] is True
    stated = json.loads((directory / SUBAGENTS).read_text())
    assert stated["starts"][0]["returned"] == "question"


def test_a_run_starting_no_sub_agent_is_undispatched(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC3: a bundle set read and not dispatched is `undispatched`."""
    monkeypatch.setenv("STUB_AGENT_NO_DISPATCH", "1")
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-chain"),
        *("--forms", COMPILED_SET, "--repetitions", "1"),
        *("--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    assert record["verdict"]["failure"] == "undispatched"
    directory = session_of(record).directory(tmp_path / "results" / "test")
    assert read_starts(directory) == ()


def test_a_run_that_ran_a_set_in_sequence_is_sequential_set(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC3: a set's bundles started, but one after another."""
    monkeypatch.setenv("STUB_AGENT_SEQUENTIAL", "1")
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-set"),
        *("--forms", COMPILED_SET, "--repetitions", "1"),
        *("--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    assert record["verdict"]["failure"] == "sequential_set"
    directory = session_of(record).directory(tmp_path / "results" / "test")
    assert [start.together for start in read_starts(directory)] == [False, False]


def test_a_question_the_session_answered_is_unrelayed_question(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A sub-agent's question returned as done is answered in its place."""
    monkeypatch.setenv("STUB_AGENT_ANSWER", "done")
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-question"),
        *("--forms", AUTHORED_SET, "--repetitions", "1"),
        *("--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    assert record["verdict"]["failure"] == "unrelayed_question"
    directory = session_of(record).directory(tmp_path / "results" / "test")
    assert [start.returned for start in read_starts(directory)] == ["done", "done"]


def test_a_dispatch_run_that_stopped_short_is_unfinished(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC3: the completion check is read before any dispatch check."""
    monkeypatch.setenv("STUB_AGENT_STOP", "1")
    monkeypatch.setenv("STUB_AGENT_NO_DISPATCH", "1")
    eval_run(
        tmp_path,
        *("--workflows", "dispatch-chain"),
        *("--forms", COMPILED_SET, "--repetitions", "1"),
        *("--budget-tokens", "2000"),
    )
    [record] = records(tmp_path)
    assert record["verdict"]["failure"] == "unfinished"
    assert record["verdict"]["actual"] == ["Request"]


def test_a_scenario_dispatching_nothing_records_no_start(
    tmp_path: Path, log: Path
) -> None:
    """A workflow dispatching nothing passes the dispatch checks with no record."""
    eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-tokens", "1000"),
    )
    [record] = records(tmp_path)
    assert record["verdict"]["passed"] is True
    directory = session_of(record).directory(tmp_path / "results" / "test")
    assert (directory / SUBAGENTS).is_file()
    assert read_starts(directory) == ()


def dispatch_run(tmp_path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    """A run over every dispatch scenario in both forms, by scenario and form."""
    eval_run(
        tmp_path,
        *("--workflows", ",".join(DISPATCHING)),
        *("--forms", ",".join(DISPATCH_FORMS)),
        *("--repetitions", "1", "--budget-tokens", "8000"),
    )
    written = records(tmp_path)
    cells = {(record["scenario"], record["form"]): record for record in written}
    assert len(written) == len(cells) == len(DISPATCHING) * len(DISPATCH_FORMS)
    return cells


def test_the_departure_table_names_every_dispatch_scenario() -> None:
    """Each script's predicted class is stated for the corpus the run walks."""
    for departure, (_, predicted) in DEPARTURES.items():
        assert set(predicted) == set(DISPATCH_SCENARIOS), departure


@pytest.mark.parametrize("departure", DEPARTURES, ids=str)
def test_a_departure_is_classified_across_every_dispatch_scenario(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch, departure: str
) -> None:
    """AC4: each scenario in each form takes the class its script predicts."""
    value, predicted = DEPARTURES[departure]
    monkeypatch.setenv(departure, value)
    cells = dispatch_run(tmp_path)
    assert set(cells) == {
        (scenario, form) for scenario in DISPATCH_SCENARIOS for form in DISPATCH_FORMS
    }
    for (scenario, form), record in cells.items():
        verdict = record["verdict"]
        due = predicted[scenario]
        assert verdict["failure"] == (None if due is None else str(due)), (
            f"{departure} over {scenario}/{form}: {verdict}"
        )
        assert verdict["passed"] is (due is None), verdict


def test_a_clean_run_passes_every_dispatch_cell(tmp_path: Path, log: Path) -> None:
    """AC4: with no departure scripted, every scenario in both forms passes."""
    cells = dispatch_run(tmp_path)
    for (scenario, form), record in cells.items():
        verdict = record["verdict"]
        assert verdict["passed"] is True, f"{scenario}/{form}: {verdict}"
        assert verdict["failure"] is None
        assert verdict["actual"] == verdict["expected"]
