"""Hold the native Codex adapter to protocol evidence and confined tools."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from codex_agent import (
    DISABLED,
    Bridge,
    ProtocolError,
    configuration,
    file_tool,
    pf_command,
    policy,
    summarize,
)
from harness import Codex
from run import BOOTSTRAP_SET, FORMS, matrix, prepare
from score import names
from workflow import SOURCE_DIR, CorpusError, entry_bundle, workflows


def event(
    method: str, thread: str = "root", turn_id: str = "turn-root", **held: Any
) -> dict[str, Any]:
    return {"method": method, "params": {"threadId": thread, "turnId": turn_id, **held}}


def group(
    *calls: str,
    thread: str = "root",
    turn: str = "turn-root",
    response: str = "response-1",
) -> list[dict[str, Any]]:
    return [
        *[
            event(
                "rawResponseItem/completed",
                thread,
                turn,
                item={
                    "type": "function_call",
                    "call_id": call,
                    "name": "spawn_agent",
                    "arguments": "{}",
                },
            )
            for call in calls
        ],
        event("rawResponse/completed", thread, turn, responseId=response),
    ]


def call(
    identifier: str,
    child: str,
    prompt: str,
    thread: str = "root",
    tool: str = "spawnAgent",
    states: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return event(
        "item/completed",
        thread,
        item={
            "type": "collabAgentToolCall",
            "id": identifier,
            "tool": tool,
            "status": "completed",
            "senderThreadId": thread,
            "receiverThreadIds": [child],
            "prompt": prompt,
            "agentsStates": states or {},
        },
    )


def usage(thread: str, total: int, turn: str = "turn-root") -> dict[str, Any]:
    return event(
        "thread/tokenUsage/updated",
        thread,
        turn,
        tokenUsage={
            "total": {
                "totalTokens": total,
                "inputTokens": total - 10,
                "cachedInputTokens": total - 20,
                "outputTokens": 10,
                "reasoningOutputTokens": 5,
            }
        },
    )


def finished(thread: str, text: str, turn: str = "turn-root") -> list[dict[str, Any]]:
    return [
        event("turn/started", thread, turn, turn={"id": turn, "status": "inProgress"}),
        event(
            "item/completed",
            thread,
            turn,
            item={
                "type": "agentMessage",
                "id": f"message-{turn}",
                "text": text,
                "phase": "final_answer",
            },
        ),
        event(
            "turn/completed",
            thread,
            turn,
            turn={"id": turn, "status": "completed", "error": None},
        ),
    ]


def test_native_response_groups_survive_interleaved_child_starts() -> None:
    events = [
        *group("a", "b"),
        call("a", "first", "Follow review__source.bundle.md"),
        *group("nested", thread="first", turn="child-turn", response="child-response"),
        call("nested", "inner", "Follow deep__work.bundle.md", thread="first"),
        call("b", "second", "Follow review__tests.bundle.md"),
        *finished("inner", "Done.", "inner-turn"),
        *finished("first", "Done.", "child-turn"),
        *finished("second", "Done.", "second-turn"),
        usage("root", 150),
        usage("first", 30),
        usage("inner", 20),
        usage("second", 40),
        *finished("root", "Done."),
    ]
    result = summarize(events, "root")
    assert [
        (row["actor"], row["group"], row["together"]) for row in result["starts"]
    ] == [
        ("root", "response-1", False),
        ("first", "child-response", False),
        ("root", "response-1", True),
    ]
    assert all(row["returned"] == "done" for row in result["starts"])
    assert result["tokens"] == 240


def test_a_question_is_not_reused_as_a_followups_return() -> None:
    events = [
        *group("a"),
        call("a", "child", "Follow draft__choose.bundle.md"),
        *finished("child", "Question: which option?", "first-turn"),
        *group("b", response="response-2"),
        call(
            "b",
            "child",
            "Follow draft__choose.bundle.md with south.",
            tool="followupTask",
            states={
                "child": {"status": "completed", "message": "Question: which option?"}
            },
        ),
        *finished("child", "Done: south.", "next-turn"),
        usage("child", 70, "next-turn"),
        usage("root", 100),
        *finished("root", "Done."),
    ]
    result = summarize(events, "root")
    assert [row["returned"] for row in result["starts"]] == ["question", "done"]
    assert [row["together"] for row in result["starts"]] == [False, False]


def test_a_parent_ending_with_a_running_child_records_unfinished() -> None:
    events = [
        *group("a"),
        call("a", "child", "Follow plan__work.bundle.md"),
        usage("root", 100),
        *finished("root", "Done."),
    ]
    result = summarize(events, "root")
    assert result["is_error"] is False
    assert result["starts"][0]["returned"] == "unfinished"
    assert result["tokens"] is None


def test_missing_native_response_boundaries_are_a_plumbing_fault() -> None:
    events = [
        call("a", "child", "Follow plan__work.bundle.md"),
        *finished("child", "Done."),
        usage("child", 20),
        usage("root", 100),
        *finished("root", "Done."),
    ]
    with pytest.raises(ProtocolError, match="response boundary"):
        summarize(events, "root")


def test_missing_cumulative_tokens_are_a_plumbing_fault() -> None:
    with pytest.raises(ProtocolError, match="token usage"):
        summarize(finished("root", "Done."), "root")


def test_cumulative_usage_counts_each_thread_once_without_cache_double_counting() -> (
    None
):
    result = summarize(
        [usage("root", 100), usage("root", 250), *finished("root", "Done.")], "root"
    )
    assert result["tokens"] == 250
    assert Codex().tokens(result) == 250
    assert Codex().cost(result) is None


def test_raw_response_usage_cross_checks_each_response_once() -> None:
    events = [
        event("rawResponse/completed", responseId="one", usage={"totalTokens": 100}),
        usage("root", 100),
        event("rawResponse/completed", responseId="two", usage={"totalTokens": 150}),
        event("rawResponse/completed", responseId="two", usage={"totalTokens": 150}),
        usage("root", 250),
        *finished("root", "Done."),
    ]
    result = summarize(events, "root")
    assert result["tokens"] == result["usage"]["rawResponseTokens"] == 250
    events.insert(-1, usage("root", 300))
    with pytest.raises(ProtocolError, match="tokens disagree"):
        summarize(events, "root")


@pytest.mark.parametrize("tool", ["read_file", "write_file", "list_files"])
@pytest.mark.parametrize("escape", ["parent", "symlink"])
def test_file_tools_refuse_paths_outside_the_workspace(
    tmp_path: Path, tool: str, escape: str
) -> None:
    root = tmp_path / "workspace"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "kept.txt").write_text("kept")
    (root / "linked").symlink_to(outside, target_is_directory=True)
    path = "../outside/kept.txt" if escape == "parent" else "linked/kept.txt"
    with pytest.raises(ValueError, match="outside"):
        file_tool(root, tool, {"path": path, "content": "changed", "append": False})
    assert (outside / "kept.txt").read_text() == "kept"


def test_workspace_tools_read_list_write_and_append(tmp_path: Path) -> None:
    file_tool(
        tmp_path,
        "write_file",
        {"path": "actions/work.txt", "content": "one\n", "append": False},
    )
    file_tool(
        tmp_path,
        "write_file",
        {"path": "actions/work.txt", "content": "two\n", "append": True},
    )
    assert (
        file_tool(tmp_path, "read_file", {"path": "actions/work.txt"}) == "one\ntwo\n"
    )
    assert file_tool(tmp_path, "list_files", {"path": "."}) == "actions/work.txt"


def test_pf_arguments_and_redirects_are_recorded_as_the_executed_command() -> None:
    assert (
        pf_command(
            {
                "args": ["file with spaces.md", "-o", "build"],
                "stdout": "guide.txt",
                "stderr": None,
                "append": False,
                "stderr_to_stdout": True,
            }
        )
        == "pf 'file with spaces.md' -o build > guide.txt 2>&1"
    )


def test_pf_output_paths_are_confined_before_native_execution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    bridge = Bridge(["codex"], "gpt-6.1-sol", "medium", 1000)
    replies = []
    monkeypatch.setattr(bridge, "tool_result", lambda *args: replies.append(args))
    monkeypatch.setattr(
        bridge,
        "request",
        lambda *args: pytest.fail("an escaping path reached native execution"),
    )
    bridge.handle_tool(
        {
            "id": 4,
            "params": {
                "tool": "pf",
                "arguments": {"args": [], "stdout": "../outside.txt"},
            },
        }
    )
    assert replies and replies[0][2] is False
    assert not (tmp_path.parent / "outside.txt").exists()


def test_codex_receives_an_isolated_home_and_requires_explicit_reasoning(
    tmp_path: Path,
) -> None:
    harness = Codex()
    held = {
        "PATH": "/usr/bin",
        "CODEX_HOME": "caller",
        "OPENAI_API_KEY": "caller",
        "CODEX_OTHER": "caller",
    }
    assert harness.environment(tmp_path, held) == {
        "PATH": "/usr/bin",
        "CODEX_HOME": str(tmp_path / "codex"),
    }
    with pytest.raises(CorpusError, match="reasoning-effort"):
        harness.argv(["codex"], "gpt-6.1-sol", 1000)
    argv = harness.argv(["codex"], "gpt-6.1-sol", 1000, reasoning_effort="medium")
    assert argv[argv.index("--model") + 1] == "gpt-6.1-sol"
    assert argv[argv.index("--reasoning-effort") + 1] == "medium"


def test_codex_bootstrap_material_uses_its_native_skill_root(tmp_path: Path) -> None:
    workflow = next(
        workflow for workflow in workflows() if workflow.name == "bootstrap-audit"
    )
    prepare(
        tmp_path,
        workflow,
        workflow.scenarios[0],
        BOOTSTRAP_SET,
        {},
        Path(Codex().skill_home),
    )
    assert (tmp_path / ".agents/skills/bootstrap-audit/SKILL.md").is_file()
    assert not (tmp_path / ".claude").exists()
    assert not (tmp_path / "bin/pf").exists()
    assert len(matrix(workflows(), ["gpt-6.1-sol"], list(FORMS), 1, Codex())) == 76


def test_native_thread_readback_refuses_another_model_or_outside_instructions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    bridge = Bridge(["codex"], "gpt-6.1-sol", "medium", 1000)
    with pytest.raises(ProtocolError, match="model"):
        bridge.subscribed({"model": "another-model", "instructionSources": []})
    with pytest.raises(ProtocolError, match="instructions"):
        bridge.subscribed(
            {
                "model": "gpt-6.1-sol",
                "instructionSources": [str(tmp_path.parent / "AGENTS.md")],
            }
        )
    bridge.subscribed({"model": "gpt-6.1-sol", "instructionSources": []})


def isolated_config() -> dict[str, Any]:
    return {
        "config": {
            "features": {
                **dict.fromkeys(DISABLED, False),
                "skip_host_skill_discovery": True,
            },
            "project_doc_max_bytes": 0,
        },
        "layers": [],
    }


def test_loaded_ancestor_configuration_is_refused_before_a_thread(
    tmp_path: Path,
) -> None:
    result = isolated_config()
    result["layers"] = [
        {
            "name": {
                "type": "project",
                "dotCodexFolder": str(tmp_path.parent / ".codex"),
            },
            "config": {},
            "disabledReason": None,
        }
    ]
    with pytest.raises(ProtocolError, match="ancestor"):
        configuration(result, tmp_path, tmp_path / "home")


@pytest.mark.parametrize("capability", DISABLED)
def test_an_enabled_external_capability_or_shell_is_refused(
    tmp_path: Path, capability: str
) -> None:
    result = isolated_config()
    result["config"]["features"][capability] = True
    with pytest.raises(ProtocolError, match="capability"):
        configuration(result, tmp_path, tmp_path / "home")


def test_an_inherited_mcp_server_is_refused_before_a_thread(tmp_path: Path) -> None:
    result = isolated_config()
    result["config"]["mcp_servers"] = {"fixture": {"enabled": True}}
    with pytest.raises(ProtocolError, match="MCP"):
        configuration(result, tmp_path, tmp_path / "home")


def test_child_subscription_is_native_and_happens_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    bridge = Bridge(["codex"], "gpt-6.1-sol", "medium", 1000)
    bridge.thread = "root"
    requested: list[tuple[Any, ...]] = []
    monkeypatch.setattr(bridge, "request", lambda *args: requested.append(args))
    started = call("a", "child", "Follow plan__work.bundle.md")
    assert bridge.notice(started) is False
    assert bridge.notice(started) is False
    assert requested == [
        ("subscribe", "thread/resume", {"threadId": "child", "excludeTurns": True})
    ]


def test_codex_preflight_requires_auth_and_refuses_caller_context(
    tmp_path: Path,
) -> None:
    harness = Codex()
    assert "holds no login" in (harness.preflight(tmp_path, tmp_path, ()) or "")
    home = tmp_path / "codex"
    home.mkdir()
    (home / "auth.json").write_text("{}")
    assert harness.preflight(tmp_path, tmp_path, ()) is None
    (home / "config.toml").write_text("model = 'fixture'\n")
    assert "auth-only" in (harness.preflight(tmp_path, tmp_path, ()) or "")


STUB_SERVER = Path(__file__).with_name("stub_codex.py")


def test_the_bridge_drives_native_stdio_and_sandboxed_pf_without_a_model(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "config"))
    argv = Codex().argv(
        [sys.executable, str(STUB_SERVER)],
        "gpt-6.1-sol",
        1000,
        reasoning_effort="medium",
    )
    ran = subprocess.run(
        argv,
        input="Follow workflow.md.",
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert ran.returncode == 0, ran.stderr
    assert "configuration-content-sentinel" not in ran.stdout + ran.stderr
    transcript = tmp_path / "transcript.jsonl"
    transcript.write_text(ran.stdout)
    result = Codex().result(transcript)
    assert result is not None and result["is_error"] is False, result
    assert Codex().tokens(result) == 120
    assert Codex().commands(transcript) == ("pf > guide.txt 2>&1",)
    executed = next(
        json.loads(line)
        for line in ran.stdout.splitlines()
        if json.loads(line).get("type") == "pf"
    )
    assert (executed["threadId"], executed["callId"]) == ("root", "pf-1")
    assert (tmp_path / "guide.txt").read_text().startswith("pf compiles")
    thread = json.loads((tmp_path / "thread-request.json").read_text())
    turn = json.loads((tmp_path / "turn-request.json").read_text())
    command = json.loads((tmp_path / "command-request.json").read_text())
    assert thread["ephemeral"] is True and thread["allowProviderModelFallback"] is False
    assert thread["experimentalRawEvents"] is True
    assert {tool["name"] for tool in thread["dynamicTools"]} == {
        "read_file",
        "write_file",
        "list_files",
        "pf",
    }
    assert turn["effort"] == "medium"
    assert turn["input"][0]["text"] == "Follow workflow.md."
    assert turn["sandboxPolicy"] == command["sandboxPolicy"] == policy(tmp_path)
    assert Path(command["command"][0]).name == "pf"


def test_a_bootstrap_compile_runs_pf_from_the_skill_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    workflow = next(item for item in workflows() if item.name == "bootstrap-audit")
    prepare(
        tmp_path,
        workflow,
        workflow.scenarios[0],
        BOOTSTRAP_SET,
        {},
        Path(Codex().skill_home),
    )
    skill = tmp_path / ".agents/skills/bootstrap-audit"
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("STUB_CODEX_PF_CWD", str(skill.relative_to(tmp_path)))
    monkeypatch.setenv(
        "STUB_CODEX_PF_ARGS",
        json.dumps(["sources/workflow.md", "-o", str(tmp_path / "build")]),
    )
    argv = Codex().argv(
        [sys.executable, str(STUB_SERVER)],
        "gpt-6.1-sol",
        1000,
        reasoning_effort="medium",
    )
    ran = subprocess.run(
        argv,
        input="Follow the skill.",
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=10,
    )
    [bundle] = (tmp_path / "build").rglob("sources_workflow.bundle.md")
    assert "flowchart" in bundle.read_text(), ran.stdout + ran.stderr
    for due in workflow.scenarios[0].trace:
        target = bundle.parent / entry_bundle(f"{SOURCE_DIR}/{due.section}").name
        assert target.is_file()
        assert names(f"Follow {target.name}", due.section, SOURCE_DIR)
        assert not names(f"Follow {target.name}", due.section)
    executed = next(
        json.loads(line)
        for line in ran.stdout.splitlines()
        if json.loads(line).get("type") == "pf"
    )
    assert executed["cwd"] == ".agents/skills/bootstrap-audit"
    command = json.loads((tmp_path / "command-request.json").read_text())
    assert command["cwd"] == str(skill)
    assert command["sandboxPolicy"] == policy(tmp_path)
