"""Hold each harness to what its own stream states.

A session's stream is the one thing an agent CLI differs in, so each test
here lays out a transcript in one CLI's shape and asks that CLI's harness
for the starts, the result and the tokens it holds. The shapes are the ones
the CLIs print: Claude's `tool_use` and `tool_result` blocks, and Cursor's
`tool_call` events carrying `taskToolCall`. A start read from either is the
same `Start`, which is what lets the scorer above be unaware of the CLI.
"""

import inspect
import json
import re
from dataclasses import fields
from pathlib import Path

import pytest
from harness import HARNESSES, Claude, Codex, Cursor, Opencode, Start, harness_named
from run import BOOTSTRAP_SET, prepare
from workflow import AUTHORED_FORM, COMPILED_FORM, workflows


def transcript(tmp_path: Path, lines: list[dict[str, object]]) -> Path:
    """A transcript holding the supplied messages, one to a line."""
    path = tmp_path / "transcript.jsonl"
    path.write_text("\n".join(json.dumps(line) for line in lines) + "\n")
    return path


def claude_call(identifier: str, target: str) -> dict[str, object]:
    """One Claude `Agent` call, its prompt naming the section handed over."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "id": identifier,
                    "name": "Agent",
                    "input": {"description": "Follow the workflow", "prompt": target},
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
        "args": {"description": "Follow the workflow", "prompt": target},
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
    assert set(HARNESSES) == {"claude", "cursor", "opencode", "codex"}
    assert harness_named("cursor") is HARNESSES["cursor"]
    assert harness_named("opencode") is HARNESSES["opencode"]
    assert harness_named("codex") is HARNESSES["codex"]
    assert Codex().name == "codex"
    assert (
        Claude().name == "claude"
        and Cursor().name == "cursor"
        and Opencode().name == "opencode"
    )


def test_the_harness_module_names_every_declared_harness() -> None:
    """AC3: the module docstring lists each harness `HARNESSES` declares."""
    import harness

    stated = harness.__doc__ or ""
    for name in HARNESSES:
        assert f"- `{name}`" in stated, name


def test_no_harness_declares_a_field_nothing_reads() -> None:
    """AC3: each field of a declared harness has a reader.

    A field is read where its own class reads it as `self.<field>`, or where
    an eval module reads it from any harness as `harness.<field>`.
    """
    here = Path(__file__).parent
    modules = " ".join(
        path.read_text()
        for path in sorted(here.glob("*.py"))
        if not path.name.startswith("test_")
    )
    for declared in HARNESSES.values():
        own = inspect.getsource(type(declared))
        unread = [
            field.name
            for field in fields(declared)
            if not re.search(rf"\bself\.{field.name}\b", own)
            and not re.search(rf"\bharness\.{field.name}\b", modules)
        ]
        assert not unread, f"{declared.name} declares {unread}, which nothing reads"


def test_every_claude_session_carries_a_shell_limited_to_pf() -> None:
    """Every form can follow the run-pf line, with arguments and redirects."""
    argv = Claude().argv(["claude"], "a-model", 60_000)
    assert argv[argv.index("--tools") + 1] == "Read,Write,Edit,Glob,Grep,Agent,Bash"
    assert argv[argv.index("--allowedTools") + 1] == "Bash(pf *)"


def test_claude_reads_the_shell_commands_a_session_ran(tmp_path: Path) -> None:
    """AC12: a session's `pf` command is read from its `Bash` calls."""
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
                            "name": "Bash",
                            "input": {"command": "pf --help"},
                        }
                    ]
                },
            },
        ],
    )
    assert Claude().commands(held) == ("pf --help",)
    assert Claude().commands(tmp_path / "absent.jsonl") == ()


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
                            "name": "Agent",
                            "input": {
                                "description": "Review",
                                "prompt": "review#source",
                            },
                        },
                        {
                            "type": "tool_use",
                            "id": "c",
                            "name": "Agent",
                            "input": {
                                "description": "Review",
                                "prompt": "review#tests",
                            },
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
                            "content": "Question: which?",
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


def test_claude_reads_blocks_of_one_message_as_together(tmp_path: Path) -> None:
    """The CLI prints each block of a message as its own event, carrying its id."""

    def event(message: str, identifier: str, target: str) -> dict[str, object]:
        held = claude_call(identifier, target)
        held["message"]["id"] = message  # type: ignore[index]
        return held

    held = transcript(
        tmp_path,
        [
            event("m1", "a", "plan#work"),
            event("m2", "b", "review#source"),
            event("m2", "c", "review#tests"),
            event("m3", "d", "review#docs"),
        ],
    )
    assert [start.together for start in Claude().starts(held)] == [
        False,
        False,
        True,
        False,
    ]


def test_claude_reads_the_report_inside_its_hand_back_frame(tmp_path: Path) -> None:
    """The CLI frames each sub-agent's report; the return is read from the report."""

    def framed(identifier: str, report: str) -> dict[str, object]:
        text = (
            "[Subagent hand-back] The text below is the final report of a "
            "subagent. The report follows:\n"
            + "".join(f"  {line}\n" for line in report.splitlines())
            + "agentId: a1\n<usage>subagent_tokens: 9</usage>"
        )
        return {
            "type": "user",
            "message": {
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": identifier,
                        "content": [{"type": "text", "text": text}],
                    }
                ]
            },
        }

    held = transcript(
        tmp_path,
        [
            claude_call("a", "draft#choose"),
            framed("a", "Question: which provider?\nOptions: north, south."),
            claude_call("b", "draft#choose"),
            framed("b", "Wrote actions/draft.txt."),
        ],
    )
    assert [start.returned for start in Claude().starts(held)] == ["question", "done"]


def test_claude_reads_a_question_only_from_its_marker_line(tmp_path: Path) -> None:
    """The guide has a returned question's first line read `Question:`."""
    held = transcript(
        tmp_path,
        [
            claude_call("a", "draft#choose"),
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "a",
                            "content": "Questions remain.\nQuestion: which?",
                        }
                    ]
                },
            },
            claude_call("b", "draft#choose"),
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "b",
                            "content": "\nQuestion: which provider?\nOptions: north.",
                        }
                    ]
                },
            },
        ],
    )
    assert [start.returned for start in Claude().starts(held)] == ["done", "question"]


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


def test_claude_counts_every_model_and_sub_agent_a_session_ran(
    tmp_path: Path,
) -> None:
    """The last result's `modelUsage` counts the whole session, sub-agents included.

    Its `usage` counts the parent's own turns, so a session that dispatched
    reports more under `modelUsage` than under `usage`.
    """
    held = transcript(
        tmp_path,
        [
            {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "usage": {"input_tokens": 10, "output_tokens": 5},
                "modelUsage": {
                    "claude-haiku-5-5": {"inputTokens": 10, "outputTokens": 5},
                },
            },
            {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "usage": {
                    "input_tokens": 1,
                    "output_tokens": 2,
                    "cache_creation_input_tokens": 3,
                    "cache_read_input_tokens": 4,
                },
                "modelUsage": {
                    "claude-haiku-5-5": {
                        "inputTokens": 20,
                        "outputTokens": 10,
                        "cacheCreationInputTokens": 30,
                        "cacheReadInputTokens": 40,
                        "costUSD": 0.5,
                    },
                    "claude-sonnet-5-5": {"inputTokens": 7, "outputTokens": 3},
                },
            },
        ],
    )
    result = Claude().result(held)
    assert Claude().tokens(result) == 110
    assert Cursor().tokens(result) is None


def test_claude_reports_no_tokens_where_the_result_counts_no_model(
    tmp_path: Path,
) -> None:
    held = transcript(
        tmp_path,
        [{"type": "result", "is_error": False, "usage": {"input_tokens": 10}}],
    )
    assert Claude().tokens(Claude().result(held)) is None


def test_a_claude_task_call_is_no_start(tmp_path: Path) -> None:
    """The CLI dispatches through `Agent`; a block naming another tool is none."""
    call = claude_call("a", "plan#work")
    call["message"]["content"][0]["name"] = "Task"  # type: ignore[index]
    assert Claude().starts(transcript(tmp_path, [call])) == ()


def test_claude_sessions_dispatch_in_the_foreground(tmp_path: Path) -> None:
    """A sub-agent runs within the call that starts it, so its answer is the result."""
    env = Claude().environment(tmp_path, {"CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "0"})
    assert env["CLAUDE_CODE_DISABLE_BACKGROUND_TASKS"] == "1"


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


@pytest.mark.parametrize("name", ["claude", "cursor", "opencode"])
def test_a_start_reads_its_prompt_when_its_description_names_another_section(
    name: str, tmp_path: Path
) -> None:
    """A call's compiled file determines its target, whatever its description."""
    prompt = "Follow review__check.bundle.md and write actions/check.txt."
    if name == "claude":
        event = claude_call("a", prompt)
        event["message"]["content"][0]["input"]["description"] = "plan#work"  # type: ignore[index]
    elif name == "cursor":
        event = cursor_call("m1", prompt)
        event["tool_call"]["taskToolCall"]["args"]["description"] = "plan#work"  # type: ignore[index]
    else:
        event = opencode_part(tool="task", description=prompt)
        event["part"]["state"]["input"]["description"] = "plan#work"  # type: ignore[index]
    assert HARNESSES[name].starts(transcript(tmp_path, [event])) == (
        Start(prompt, "done", False),
    )


def test_the_claude_cli_is_capped_in_dollars_not_tokens(tmp_path: Path) -> None:
    """A token budget is not a dollar cap, so the CLI is given a price."""
    argv = Claude().argv(["claude"], "a-model", 60_000)
    assert argv[argv.index("--max-budget-usd") + 1] == "0.5"
    assert "60000" not in argv


def test_claude_reads_each_shell_call_under_the_start_whose_sub_agent_made_it(
    tmp_path: Path,
) -> None:
    """AC12: a `Bash` call is the session's or the start its parent names.

    The session runs `pf` on its line, the review's sub-agent compiles its
    line and starts the ruling, and the ruling's sub-agent compiles its own
    line. A compiled session records the session's command list; one in a
    form carrying no shell records none.
    """
    from score import read_commands, read_starts, record_calls

    held = transcript(
        tmp_path,
        [
            under(None, shell_call("s", "pf reference/loading.md#crew")),
            under(None, claude_call("a", "hop/review#scan")),
            under("a", shell_call("t", "pf steps/weighing.md#weigh")),
            under("a", claude_call("b", "steps/ruling#rule")),
            under("b", shell_call("u", "pf -o out steps/recording.md#file")),
        ],
    )
    assert Claude().commands(held) == ("pf reference/loading.md#crew",)
    assert Claude().starts(held) == (
        Start("hop/review#scan", "done", False, None, ("pf steps/weighing.md#weigh",)),
        Start(
            "steps/ruling#rule",
            "done",
            False,
            0,
            ("pf -o out steps/recording.md#file",),
        ),
    )
    compiled = tmp_path / "compiled"
    compiled.mkdir()
    record_calls(held, compiled, Claude(), COMPILED_FORM)
    assert read_commands(compiled) == ("pf reference/loading.md#crew",)
    assert read_starts(compiled) == Claude().starts(held)
    authored = tmp_path / "authored"
    authored.mkdir()
    record_calls(held, authored, Claude(), AUTHORED_FORM)
    assert read_commands(authored) is None


def shell_call(identifier: str, command: str) -> dict[str, object]:
    """One Claude `Bash` call, as the CLI prints it."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "id": identifier,
                    "name": "Bash",
                    "input": {"command": command},
                }
            ]
        },
    }


def test_a_harness_hands_its_own_isolation_to_the_session(tmp_path: Path) -> None:
    """Each harness names what confines a session, and refuses what it cannot."""
    config = tmp_path / "config"
    config.mkdir()
    refused = Claude().preflight(config, tmp_path, ())
    assert refused is not None and refused.startswith(f"{config} holds no login")
    (config / ".credentials.json").touch()
    assert Claude().preflight(config, tmp_path, ()) is None
    assert Cursor().preflight(config, tmp_path, ()) is None
    refused = Cursor().preflight(tmp_path / "absent", tmp_path, ())
    assert refused is not None and "is no directory" in refused


def test_an_opencode_session_reads_no_directory_of_the_callers(tmp_path: Path) -> None:
    """Every directory the CLI shares with the caller is named under the eval root."""
    config = tmp_path / "config"
    held = Opencode().environment(config, {"PATH": "/bin", "OPENCODE_X": "caller"})
    assert "OPENCODE_X" not in held
    assert held["XDG_CONFIG_HOME"] == str(config / "config")
    assert held["XDG_DATA_HOME"] == str(config / "data")
    assert held["XDG_STATE_HOME"] == str(config / "state")
    assert held["XDG_CACHE_HOME"] == str(config / "cache")
    assert held["OPENCODE_CONFIG"] == str(config / "harness.json")


def test_an_opencode_session_runs_no_plugin_a_caller_installed(tmp_path: Path) -> None:
    """The flags that keep the caller's plugins and external skills out are set."""
    held = Opencode().environment(tmp_path, {})
    for name in (
        "OPENCODE_PURE",
        "OPENCODE_DISABLE_DEFAULT_PLUGINS",
        "OPENCODE_DISABLE_EXTERNAL_SKILLS",
        "OPENCODE_DISABLE_CLAUDE_CODE_SKILLS",
        "OPENCODE_DISABLE_PROJECT_CONFIG",
    ):
        assert held.get(name) == "1", name


def test_an_opencode_session_may_run_only_pf_and_read_its_workspace(
    tmp_path: Path,
) -> None:
    """The run writes the permissions a session reads, and admits no other path."""
    config = tmp_path / "config"
    Opencode().prepare(config)
    settings = json.loads((config / "harness.json").read_text())
    assert settings["permission"] == Opencode().permission
    assert settings["permission"]["bash"] == {"*": "deny", "pf *": "allow"}
    assert settings["permission"]["external_directory"] == "deny"
    assert settings["permission"]["webfetch"] == "deny"


def test_an_opencode_session_may_dispatch_at_every_hop_a_bundle_states(
    tmp_path: Path,
) -> None:
    """A nested start is refused at the CLI's depth of one, so the run raises it."""
    config = tmp_path / "config"
    Opencode().prepare(config)
    settings = json.loads((config / "harness.json").read_text())
    assert settings["subagent_depth"] == Opencode().subagent_depth
    assert settings["subagent_depth"] >= 3


def test_opencode_reports_no_nested_dispatch_the_parent_stream_lacks() -> None:
    """A `task` call's parts are its own, so a sub-agent's start is unobservable."""
    assert Opencode().nested_starts is False


def test_an_opencode_run_without_the_evals_login_is_refused(tmp_path: Path) -> None:
    """A run names its credential store under the eval root, and refuses without it."""
    config = tmp_path / "config"
    config.mkdir()
    refused = Opencode().preflight(config, tmp_path, ())
    assert refused is not None and "holds no login" in refused
    (config / "data" / "opencode").mkdir(parents=True)
    (config / "data" / "opencode" / "auth.json").write_text("{}")
    assert Opencode().preflight(config, tmp_path, ()) is None


def test_a_bootstrap_skill_sits_where_the_runs_harness_discovers_it(
    tmp_path: Path,
) -> None:
    """A bootstrap workspace holds the skill under the harness's own root."""
    workflow = next(item for item in workflows() if item.name == "bootstrap-audit")
    scenario = workflow.scenarios[0]
    for harness in HARNESSES.values():
        workspace = tmp_path / harness.name
        workspace.mkdir()
        skill_home = Path(harness.skill_home)
        prepare(workspace, workflow, scenario, BOOTSTRAP_SET, {}, skill_home)
        assert (workspace / skill_home / workflow.name / "SKILL.md").is_file()
    assert HARNESSES["claude"].skill_home == HARNESSES["cursor"].skill_home
    assert HARNESSES["opencode"].skill_home == ".opencode/skills"


def opencode_part(
    *, tool: str, description: str, message: str = "m1", output: str | None = None
) -> dict[str, object]:
    """One opencode `tool_use` part, as the CLI prints it."""
    state: dict[str, object] = {
        "status": "completed",
        "input": {"description": "Follow the workflow", "prompt": description},
    }
    if output is not None:
        state["output"] = output
    return {
        "type": "tool_use",
        "part": {
            "type": "tool",
            "callID": f"call_{description}",
            "messageID": message,
            "tool": tool,
            "state": state,
        },
    }


def opencode_task_output(text: str, *, state: str = "completed") -> str:
    """A `task` call's output, the sub-agent's text wrapped as opencode wraps it."""
    element = "task_error" if state == "error" else "task_result"
    return "\n".join(
        [
            f'<task id="ses_1" state="{state}">',
            f"<{element}>",
            text,
            f"</{element}>",
            "</task>",
        ]
    )


def opencode_step(tokens: int, cost: float) -> dict[str, object]:
    """One opencode `step_finish` part, its token kinds summing to `tokens`."""
    return {
        "type": "step_finish",
        "part": {
            "type": "step_finish",
            "tokens": {
                "input": tokens - 4,
                "output": 1,
                "reasoning": 1,
                "cache": {"write": 1, "read": 1},
            },
            "cost": cost,
        },
    }


def test_opencode_reads_a_task_part_as_a_start(tmp_path: Path) -> None:
    """A `tool_use` naming `task` is a sub-agent start, named by its prompt."""
    held = transcript(tmp_path, [opencode_part(tool="task", description="plan#work")])
    assert Opencode().starts(held) == (Start("plan#work", "done", False),)


def test_opencode_reads_starts_sharing_a_message_as_together(tmp_path: Path) -> None:
    held = transcript(
        tmp_path,
        [
            opencode_part(tool="task", description="a#b", message="m1"),
            opencode_part(tool="task", description="c#d", message="m1"),
            opencode_part(tool="task", description="e#f", message="m2"),
        ],
    )
    assert [start.together for start in Opencode().starts(held)] == [False, True, False]


def test_opencode_reads_a_command_not_a_task_as_no_start(tmp_path: Path) -> None:
    held = transcript(tmp_path, [opencode_part(tool="read", description="x")])
    assert Opencode().starts(held) == ()


def test_opencode_reports_the_commands_a_session_ran(tmp_path: Path) -> None:
    held = transcript(
        tmp_path,
        [
            {
                "type": "tool_use",
                "part": {
                    "type": "tool",
                    "callID": "c1",
                    "tool": "bash",
                    "state": {"input": {"command": "pf -o build sources/workflow.md"}},
                },
            }
        ],
    )
    assert Opencode().commands(held) == ("pf -o build sources/workflow.md",)


def test_opencode_reads_what_each_sub_agent_returned(tmp_path: Path) -> None:
    """A start returns what its sub-agent's text states, read inside the wrapper."""
    held = transcript(
        tmp_path,
        [
            opencode_part(
                tool="task",
                description="a#b",
                output=opencode_task_output("Question: which source?"),
            ),
            opencode_part(
                tool="task",
                description="c#d",
                message="m2",
                output=opencode_task_output("done: read it"),
            ),
            opencode_part(
                tool="task",
                description="e#f",
                message="m3",
                output=opencode_task_output("question: stopped", state="error"),
            ),
            opencode_part(tool="task", description="g#h", message="m4"),
        ],
    )
    assert Opencode().starts(held) == (
        Start("a#b", "question", False),
        Start("c#d", "done", False),
        Start("e#f", "question", False),
        Start("g#h", "done", False),
    )


def test_opencode_sums_every_step_of_a_session(tmp_path: Path) -> None:
    """A session's tokens and cost are the sum of its steps, not its last one."""
    held = transcript(
        tmp_path,
        [opencode_step(100, 0.25), opencode_step(40, 0.125), opencode_step(9, 0.0)],
    )
    result = Opencode().result(held)
    assert Opencode().tokens(result) == 149
    assert Opencode().cost(result) == 0.375


def test_opencode_sums_the_token_kinds_of_one_step(
    tmp_path: Path,
) -> None:
    held = transcript(
        tmp_path,
        [
            {
                "type": "step_finish",
                "part": {
                    "type": "step_finish",
                    "tokens": {
                        "input": 100,
                        "output": 5,
                        "reasoning": 2,
                        "cache": {"write": 3, "read": 7},
                    },
                    "cost": 0.125,
                },
            }
        ],
    )
    result = Opencode().result(held)
    assert Opencode().tokens(result) == 117
    assert Opencode().cost(result) == 0.125


def under(parent: str | None, call: dict[str, object]) -> dict[str, object]:
    """A Claude message as a sub-agent's stream prints it, naming its `Task` call."""
    return {**call, "parent_tool_use_id": parent}


def test_claude_files_each_start_under_the_sub_agent_that_made_it(
    tmp_path: Path,
) -> None:
    """AC5: starts three dispatches deep sit under the section each followed.

    A sub-agent's messages reach the session's stream, each naming the `Task`
    call it runs under, so a start made at the second or third depth names
    the start whose sub-agent made it. A set two deep shares its message.
    """
    nested_set: dict[str, object] = {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "id": identifier,
                    "name": "Task",
                    "input": {"description": target},
                }
                for identifier, target in (
                    ("c", "review#source"),
                    ("d", "review#tests"),
                )
            ]
        },
    }
    held = transcript(
        tmp_path,
        [
            under(None, claude_call("a", "plan#work")),
            under("a", claude_call("b", "review#check")),
            under("b", nested_set),
            under("d", claude_call("e", "deep#leaf")),
            claude_call("f", "close#out"),
        ],
    )
    starts = Claude().starts(held)
    assert [(start.target, start.parent, start.together) for start in starts] == [
        ("plan#work", None, False),
        ("review#check", 0, False),
        ("review#source", 1, False),
        ("review#tests", 1, True),
        ("deep#leaf", 3, False),
        ("close#out", None, False),
    ]
    assert all(start.commands == () for start in starts)


def test_the_record_lists_each_sub_agents_starts_and_commands(tmp_path: Path) -> None:
    """AC5: the session record holds its commands and each start's parent and commands.

    The record is what the scorer reads, so a start written under its parent
    with its sub-agent's commands reads back as the same start.
    """
    from score import SUBAGENTS, read_commands, read_starts, record_calls

    held = transcript(
        tmp_path,
        [
            under(None, claude_call("a", "plan#work")),
            under("a", claude_call("b", "review#check")),
        ],
    )
    records = tmp_path / "claude"
    records.mkdir()
    record_calls(held, records, Claude(), COMPILED_FORM)
    written = json.loads((records / SUBAGENTS).read_text())
    assert written == {
        "commands": [],
        "starts": [
            {
                "target": "plan#work",
                "returned": "done",
                "together": False,
                "parent": None,
                "commands": [],
            },
            {
                "target": "review#check",
                "returned": "done",
                "together": False,
                "parent": 0,
                "commands": [],
            },
        ],
    }
    assert read_starts(records) == Claude().starts(held)
    assert read_commands(records) == ()
    (records / SUBAGENTS).write_text(
        json.dumps(
            {
                "commands": ["pf"],
                "starts": [
                    {
                        "target": "plan#work",
                        "returned": "done",
                        "together": False,
                        "parent": None,
                        "commands": ["pf", "pf -o out net.md#retry"],
                    }
                ],
            }
        )
    )
    assert read_commands(records) == ("pf",)
    assert read_starts(records) == (
        Start("plan#work", "done", False, None, ("pf", "pf -o out net.md#retry")),
    )
    opencode = tmp_path / "opencode"
    opencode.mkdir()
    shell = opencode_part(tool="bash", description="compile")
    shell["part"]["state"]["input"] = {"command": "pf"}  # type: ignore[index]
    stream = transcript(
        opencode, [shell, opencode_part(tool="task", description="plan#work")]
    )
    record_calls(stream, opencode, Opencode(), COMPILED_FORM)
    assert read_commands(opencode) == ("pf",)
    assert read_starts(opencode) == (Start("plan#work", "done", False),)


def test_each_harness_declares_whether_a_sub_agents_calls_reach_its_stream() -> None:
    """AC5: depth is what each CLI prints, read rather than assumed.

    Claude prints a sub-agent's messages under its `Task` call. Cursor reports
    a sub-agent's text and no tool call it made. opencode's run command prints
    a part only where it belongs to the session it started, and a sub-agent
    runs in a child session, so neither reports a nested start or a
    sub-agent's command.
    """
    assert Claude().sub_agent_calls is True
    assert Cursor().sub_agent_calls is False
    assert Opencode().sub_agent_calls is False
