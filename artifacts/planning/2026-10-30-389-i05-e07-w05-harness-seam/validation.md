# I05:E07:W05 Validation

Each check the work item's Test row names, with the revision it ran on and what it observed.

- **Branch.** `i05/e07/w05-harness-seam`, cut from `i05/e07/main` at `7649693`.
- **Tested revision.** `9338030a`.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`.
- **No paid session ran.** The harness is exercised against stub transcripts, and the Cursor stream's shape was taken from a real session captured before the adapter was written.

## T1 Harness reading

Each harness reads a transcript in its own CLI's shape. The Cursor fixtures are the shapes the CLI printed in the captured session: `tool_call` events labelled `started` and `completed`, a `taskToolCall` holding `args` and `result` as siblings, `model_call_id` shared by two starts dispatched in one message, and a `result` message carrying usage in camelCase.

| Test | Observes |
| --- | --- |
| `test_claude_reads_starts_from_tool_use_blocks` | A `Task` `tool_use` is one start, two in one assistant message are together, and a `tool_result` states `done` or `question`. |
| `test_cursor_reads_starts_from_task_calls` | A `taskToolCall` on starting is one start, and its completed call's step text states what it returned. |
| `test_cursor_reads_two_starts_in_one_message_as_together` | Two starts sharing a `model_call_id` read as together, and a start in a message of its own does not. |
| `test_cursor_reads_a_returned_question` | `question: …` in the completed call's text reads `question`, and a `done` text reads `done`. |
| `test_cursor_ignores_a_call_that_is_not_a_task` | A `readToolCall` beside a `taskToolCall` names no start. |
| `test_each_harness_reads_the_usage_it_reports` | Claude's usage sums to its token count; Cursor reports none from a Claude-shaped result. |
| `test_cursor_reads_its_own_usage_and_reports_no_cost` | The captured camelCase usage sums to 47 467, and no cost is reported. |
| `test_an_absent_transcript_names_no_start` | Neither harness invents a start or a result from a transcript that is not there. |
| `test_a_harness_hands_its_own_isolation_to_the_session` | Claude refuses a config with no login and accepts one with it; Cursor refuses a config path that does not exist. |

## T2 The suite over the seam

`pytest evals/diagram-following` at `9338030a`: **189 passed**. Up from 179 on the base by the ten harness tests.

The suite drives the stub through the seam: the matrix, workspaces, isolation, budget, timeout, trace scoring, dispatch checks, the departure matrix, and the report's tables and baseline comparison all pass with the harness supplying the command line and reading the stream.

## T3 The whole tree

`make check` at `9338030a` exited 0:

- lock check, lint, format check and strict type check over `src/prosiform`, `src/tests`, `checks` and `evals`;
- the unit tests in `src`;
- the 189 harness tests;
- the corpus of 342 fixtures, the installed-wheel smoke run, and the layout, tables, links, vocabulary, invocation, conformance, independence, steps and authoring checks, each clean.

## What this unit does not claim

- **No Cursor pass rate.** The harness can start a Cursor session and read its stream, but no run has been made, so there is no pass rate for any form on that CLI. The committed baseline is Claude's and stays so until a run replaces it.
- **Cursor's isolation is narrower than Claude's.** It declares no configuration directory, no MCP switch, no slash-command switch and no per-session spend cap, so a Cursor session shares the caller's configuration and the run's token guard is the only budget. A Cursor pass rate is comparable with Claude's only where that difference is stated beside it.
- **The stub prints Claude's shape.** It gains a token count but not a second emitter, so the Cursor path is held by `test_harness.py` against captured shapes rather than by a stubbed run end to end. A stubbed Cursor run is the next step for confidence in the seam.
