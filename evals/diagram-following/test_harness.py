"""Hold each harness to what its own stream states.

A session's stream is the one thing an agent CLI differs in, so each test
here lays out a transcript in one CLI's shape and asks that CLI's harness
for the starts, the result and the tokens it holds. The shapes are the ones
the CLIs print: Claude's `tool_use` and `tool_result` blocks, and Cursor's
`tool_call` events carrying `taskToolCall`. A start read from either is the
same `Start`, which is what lets the scorer above be unaware of the CLI.
"""

import json
from pathlib import Path

from harness import HARNESSES, Claude, Cursor, Start, harness_named


def transcript(tmp_path: Path, lines: list[dict[str, object]]) -> Path:
    """A transcript holding the supplied messages, one to a line."""
    path = tmp_path / "transcript.jsonl"
    path.write_text("\n".join(json.dumps(line) for line in lines) + "\n")
    return path


def claude_call(identifier: str, target: str) -> dict[str, object]:
    """One Claude `Task` call, its description naming the section handed over."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "id": identifier,
                    "name": "Task",
                    "input": {"description": target},
                }
            ]
        },
    }


def cursor_call(
    message: str, target: str, *, started: bool = True, text: str = ""
) -> dict[str, object]:
    """One Cursor `taskToolCall`, as the CLI prints it on starting or completing.

    `result` sits beside `args` in the captured stream, not within it.
    """
    task: dict[str, object] = {
        "args": {"description": target, "prompt": f"Follow {target}."},
        "toolCallId": f"{message}-call",
    }
    if not started:
        task["result"] = {
            "success": {
                "conversationSteps": [{"assistantMessage": {"text": text}}],
            }
        }
    return {
        "type": "tool_call",
        "subtype": "started" if started else "completed",
        "call_id": f"{message}-call",
        "model_call_id": message,
        "tool_call": {"taskToolCall": task},
    }


def test_the_declared_harnesses_are_named() -> None:
    assert set(HARNESSES) == {"claude", "cursor"}
    assert harness_named("cursor") is HARNESSES["cursor"]
    assert Claude().name == "claude" and Cursor().name == "cursor"


def test_claude_reads_starts_from_tool_use_blocks(tmp_path: Path) -> None:
    held = transcript(
        tmp_path,
        [
            claude_call("a", "plan#work"),
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "b",
                            "name": "Task",
                            "input": {"description": "review#source"},
                        },
                        {
                            "type": "tool_use",
                            "id": "c",
                            "name": "Task",
                            "input": {"description": "review#tests"},
                        },
                    ]
                },
            },
            {
                "type": "user",
                "message": {
                    "content": [
                        {"type": "tool_result", "tool_use_id": "a", "content": "done"}
                    ]
                },
            },
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "b",
                            "content": "question: which?",
                        }
                    ]
                },
            },
        ],
    )
    assert Claude().starts(held) == (
        Start("plan#work", "done", False),
        Start("review#source", "question", False),
        Start("review#tests", "done", True),
    )


def test_cursor_reads_starts_from_task_calls(tmp_path: Path) -> None:
    """A Cursor start is a `taskToolCall`, and its return is its steps' text."""
    held = transcript(
        tmp_path,
        [
            cursor_call("m1", "plan#work"),
            cursor_call("m1", "review#source", started=False, text="done: read"),
        ],
    )
    assert Cursor().starts(held) == (Start("plan#work", "done", False),)


def test_cursor_reads_two_starts_in_one_message_as_together(tmp_path: Path) -> None:
    """Two starts sharing a `model_call_id` were dispatched in one message."""
    held = transcript(
        tmp_path,
        [
            cursor_call("m1", "plan#work"),
            cursor_call("m2", "review#source"),
            cursor_call("m2", "review#tests"),
        ],
    )
    assert Cursor().starts(held) == (
        Start("plan#work", "done", False),
        Start("review#source", "done", False),
        Start("review#tests", "done", True),
    )


def test_cursor_reads_a_returned_question(tmp_path: Path) -> None:
    held = transcript(
        tmp_path,
        [
            cursor_call("m1", "draft#choose"),
            cursor_call(
                "m1", "draft#choose", started=False, text="question: which provider?"
            ),
        ],
    )
    assert Cursor().starts(held) == (Start("draft#choose", "question", False),)


def test_cursor_ignores_a_call_that_is_not_a_task(tmp_path: Path) -> None:
    held = transcript(
        tmp_path,
        [
            {
                "type": "tool_call",
                "subtype": "started",
                "call_id": "x",
                "model_call_id": "m1",
                "tool_call": {
                    "readToolCall": {"args": {"path": "/tmp/task.md"}},
                },
            },
            cursor_call("mota", "plan#work"),
        ],
    )
    assert Cursor().starts(held) == (Start("plan#work", "done", False),)


def test_each_harness_reads_the_usage_it_reports(tmp_path: Path) -> None:
    held = transcript(
        tmp_path,
        [
            {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "usage": {
                    "input_tokens": 10,
                    "output_tokens": 5,
                    "cache_creation_input_tokens": 3,
                    "cache_read_input_tokens": 2,
                },
            }
        ],
    )
    result = Claude().result(held)
    assert Claude().tokens(result) == 20
    assert Cursor().tokens(result) is None


def test_cursor_reads_its_own_usage_and_reports_no_cost(tmp_path: Path) -> None:
    held = transcript(
        tmp_path,
        [
            {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "usage": {
                    "inputTokens": 24757,
                    "outputTokens": 438,
                    "cacheReadTokens": 22272,
                    "cacheWriteTokens": 0,
                },
            }
        ],
    )
    result = Cursor().result(held)
    assert Cursor().tokens(result) == 47467
    assert Cursor().cost(result) is None


def test_an_absent_transcript_names_no_start(tmp_path: Path) -> None:
    assert Claude().starts(tmp_path / "absent.jsonl") == ()
    assert Cursor().starts(tmp_path / "absent.jsonl") == ()
    assert Claude().result(tmp_path / "absent.jsonl") is None


def test_the_claude_cli_is_capped_in_dollars_not_tokens(tmp_path: Path) -> None:
    """A token budget is not a dollar cap, so the CLI is given a price."""
    argv = Claude().argv(["claude"], "a-model", 60_000)
    assert argv[argv.index("--max-budget-usd") + 1] == "0.5"
    assert "60000" not in argv


def test_a_harness_hands_its_own_isolation_to_the_session(tmp_path: Path) -> None:
    """Each harness names what confines a session, and refuses what it cannot."""
    config = tmp_path / "config"
    config.mkdir()
    refused = Claude().preflight(config)
    assert refused is not None and refused.startswith(f"{config} holds no login")
    (config / ".credentials.json").touch()
    assert Claude().preflight(config) is None
    assert Cursor().preflight(config) is None
    refused = Cursor().preflight(tmp_path / "absent")
    assert refused is not None and "is no directory" in refused
