"""Hold the runner to its sessions, its records and its spending cap.

Every run here starts the stub agent beside this file in place of the real
one, so no test starts a paid session. The stub writes what it found in its
workspace to a log, walks the workflow it finds there, and reports a cost
the test chooses.
"""

import json
import sys
import time
from pathlib import Path
from typing import Any

import pytest
from run import (
    BUNDLE,
    CREDENTIAL,
    FORMS,
    PROSE_BUNDLE,
    RUN,
    SESSION,
    TIMEOUT,
    TRANSCRIPT,
    TREE,
    Session,
    matrix,
    options,
    run,
)
from score import ACTIONS, TRACE
from workflow import DIAGRAM, ENTRY, CorpusError, workflows

STUB = Path(__file__).resolve().parent / "stub_agent.py"
CORPUS = {workflow.name: workflow for workflow in workflows()}
SESSIONS_PER_REPETITION = sum(len(item.scenarios) for item in CORPUS.values()) * 3


@pytest.fixture
def log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The directory the stub agent writes what it saw to, one file a session."""
    directory = tmp_path / "log"
    directory.mkdir()
    monkeypatch.setenv("STUB_AGENT_LOG", str(directory))
    monkeypatch.setenv(CREDENTIAL, "stub")
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
    """The files a session's workspace holds on starting."""
    workflow = CORPUS[session.workflow]
    scenario = next(i for i in workflow.scenarios if i.name == session.scenario)
    inputs = {f"inputs/{name}" for name in scenario.inputs}
    if session.form != TREE:
        return {ENTRY} | inputs
    tree = workflow.form(FORMS[TREE])
    return {
        str(path.relative_to(tree)) for path in tree.rglob("*") if path.is_file()
    } | inputs


def test_the_matrix_holds_one_session_per_model_form_scenario_and_repetition() -> None:
    sessions = matrix(list(CORPUS.values()), ["a", "b"], list(FORMS), 5)
    assert len(sessions) == len(set(sessions)) == 2 * 5 * SESSIONS_PER_REPETITION


def test_each_session_starts_in_a_fresh_workspace_of_its_form_and_inputs(
    tmp_path: Path, log: Path
) -> None:
    record = eval_run(
        tmp_path, "--repetitions", "2", "--budget-usd", "100", "--parallel", "3"
    )
    sessions = matrix(list(CORPUS.values()), ["stub-model"], list(FORMS), 2)
    assert record["started"] == len(sessions) == 2 * SESSIONS_PER_REPETITION
    entries = seen(log)
    assert len(entries) == len(sessions)
    assert len({entry["workspace"] for entry in entries}) == len(sessions)
    found = sorted(sorted(entry["files"]) for entry in entries)
    assert found == sorted(sorted(material(session)) for session in sessions)
    for entry in entries:
        argv = entry["argv"]
        assert argv[argv.index("--tools") + 1] == "Read,Write,Edit,Glob,Grep"
        assert "--bare" in argv and "--allowedTools" not in argv
        assert "Bash" not in " ".join(argv)
        assert ENTRY in entry["prompt"]
        assert not Path(entry["workspace"]).exists()


def test_a_bundled_form_is_one_file_and_the_tree_its_sources(
    tmp_path: Path, log: Path
) -> None:
    eval_run(
        tmp_path, "--workflows", "looping", "--repetitions", "1", "--budget-usd", "1"
    )
    by_form: dict[str, list[str]] = {}
    for entry in seen(log):
        files = [name for name in entry["files"] if not name.startswith("inputs/")]
        by_form.setdefault("tree" if len(files) > 1 else "bundled", []).append(
            str(files)
        )
    looping = CORPUS["looping"]
    assert len(by_form["bundled"]) == 2 * len(looping.scenarios)
    assert len(by_form["tree"]) == len(looping.scenarios)


def test_each_session_records_its_transcript_usage_cost_and_verdict(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_COST", "0.125")
    eval_run(tmp_path, "--repetitions", "1", "--budget-usd", "100")
    written = records(tmp_path)
    assert len(written) == SESSIONS_PER_REPETITION
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
        assert record["cost_usd"] == 0.125
        trace = (directory / TRACE).read_text().split()
        assert record["usage"] == {
            "input_tokens": 100 * len(trace),
            "output_tokens": 10,
        }
        verdict = record["verdict"]
        assert verdict["passed"] is True
        assert trace == verdict["actual"]
        action_files = {path.name for path in (directory / ACTIONS).iterdir()}
        workflow = CORPUS[session.workflow]
        assert action_files == {
            workflow.sections[DIAGRAM][state].action[0] for state in trace
        }


def test_a_failing_session_is_recorded_with_its_failure(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_STOP", "1")
    eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "1"),
        *("--budget-usd", "1"),
    )
    [record] = records(tmp_path)
    verdict = record["verdict"]
    assert verdict["failure"] == "unfinished"
    assert verdict["actual"] == ["Plan"]


def test_a_run_stops_before_its_cost_would_pass_its_cap(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_COST", "0.125")
    record = eval_run(
        tmp_path,
        *("--repetitions", "1", "--parallel", "1"),
        *("--budget-usd", "1", "--session-budget-usd", "0.25"),
    )
    sessions = matrix(list(CORPUS.values()), ["stub-model"], list(FORMS), 1)
    assert record["started"] == 7
    assert record["cost_usd"] == 0.875
    assert len(seen(log)) == len(records(tmp_path)) == 7
    not_started = record["not_started"]
    assert not_started == [
        {
            "model": session.model,
            "workflow": session.workflow,
            "scenario": session.scenario,
            "form": session.form,
            "repetition": session.repetition,
        }
        for session in sessions[7:]
    ]
    written = json.loads((tmp_path / "results" / "test" / RUN).read_text())
    assert written["not_started"] == not_started


def test_parallel_sessions_reserve_their_cap_within_the_budget(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_COST", "0.125")
    record = eval_run(
        tmp_path,
        *("--repetitions", "2", "--parallel", "4"),
        *("--budget-usd", "1", "--session-budget-usd", "0.25"),
    )
    assert record["cost_usd"] <= 1 < record["cost_usd"] + 0.25
    assert record["started"] == len(records(tmp_path)) == 7
    assert len(record["not_started"]) == 2 * SESSIONS_PER_REPETITION - 7


def test_a_session_reporting_no_cost_is_charged_its_cap(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_SILENT", "1")
    record = eval_run(
        tmp_path,
        *("--repetitions", "1", "--parallel", "1", "--forms", PROSE_BUNDLE),
        *("--budget-usd", "0.5", "--session-budget-usd", "0.25"),
    )
    assert record["started"] == 2
    assert record["cost_usd"] == 0.5
    assert all(item["cost_usd"] is None for item in records(tmp_path))


def test_a_run_without_a_credential_starts_no_session(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(CREDENTIAL)
    with pytest.raises(CorpusError, match=CREDENTIAL):
        eval_run(tmp_path, "--budget-usd", "1")
    assert seen(log) == []
    assert not (tmp_path / "results").exists()


def test_a_session_past_its_timeout_is_ended_scored_and_charged(
    tmp_path: Path, log: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STUB_AGENT_HANG", str(tmp_path / "hung"))
    monkeypatch.setenv("STUB_AGENT_STOP", "2")
    monkeypatch.setenv("STUB_AGENT_COST", "0.125")
    began = time.monotonic()
    record = eval_run(
        tmp_path,
        *("--workflows", "linear", "--forms", BUNDLE, "--repetitions", "2"),
        *("--parallel", "1", "--session-timeout-seconds", "1"),
        *("--budget-usd", "1", "--session-budget-usd", "0.25"),
    )
    assert time.monotonic() - began < 60
    assert record["started"] == 2 and record["not_started"] == []
    assert record["cost_usd"] == 0.25 + 0.125
    hung, finished = sorted(records(tmp_path), key=lambda item: item["repetition"])
    assert hung["exit_status"] == TIMEOUT and hung["cost_usd"] is None
    assert hung["verdict"]["failure"] == "unfinished"
    assert hung["verdict"]["actual"] == ["Plan", "Build"]
    assert finished["exit_status"] == 0 and finished["cost_usd"] == 0.125
