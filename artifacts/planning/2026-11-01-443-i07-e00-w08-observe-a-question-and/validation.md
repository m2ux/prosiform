# W08 Validation

Evidence for each check the [W08 work item](w08.md) names. Tested revisions: `fa02c1b9` on `i07/e00/w08-observe-a-question-and`, cut from `i07/e00/main` at `5bffb717`, and `f590e0a2`, that head merged with `i07/e00/main` at `5b16c3b4`; `make check` and CI `Checks` passed on both. Merged into `i07/e00/main` as `9b40ffdc` by [#478](https://github.com/m2ux/prosiform/pull/478).

## Source of the opencode shapes

The installed CLI (`~/.opencode/bin/opencode`, version 1.19.5) builds a completed `task` call's output as:

```text
<task id="ses_…" state="completed">
<task_result>
{the sub-agent's final text}
</task_result>
</task>
```

A failed sub-agent takes `<task_error>` in place of `<task_result>`. The CLI's own reader extracts the same element (`/<task_result>\s*([\s\S]*?)\s*<\/task_result>/`). Each model step prints its own `step_finish` part carrying that step's `tokens` and `cost`.

## AC17 A question reads as a question

`test_score.py::test_an_opencode_question_left_unanswered_scores_as_a_question` records the starts of an opencode transcript for `dispatch-question`, whose first sub-agent returned `question: which option?`, and scores the workspace.

- **Before.** `Opencode.starts` returned `done` for every start: `assert ['done', 'done'] == ['question', 'done']`. Scored, the cell takes `unrelayed_question` though the session relayed the question.
- **After.** The record reads `['question', 'done']` and the verdict passes.

## AC17 The harness reads the returned text

`test_harness.py::test_opencode_reads_what_each_sub_agent_returned` reads a `question` inside `<task_result>`, a `done`, a `question` inside `<task_error>`, and a call printing no output.

- **Before.** `Start(target='a#b', returned='done', …) != Start(target='a#b', returned='question', …)`.
- **After.** `question`, `done`, `question`, `done`, in order.

## AC18 The ledger settles every step

`test_run.py::test_the_ledger_settles_an_opencode_session_for_every_step` writes a three-step transcript (120, 60 and 20 tokens; 0.25, 0.125 and 0.0625 USD), settles a `Ledger` with `Opencode().tokens(Opencode().result(…))`, and reads the session's cost.

- **Before.** `assert 20 == 200`: the ledger was settled for the last step alone.
- **After.** `ledger.spent == 200` and the cost is `0.4375`.

## AC18 The harness sums every step

`test_harness.py::test_opencode_sums_every_step_of_a_session` reads tokens and cost from a three-step transcript.

- **Before.** `assert 9 == 149`: the last step's tokens.
- **After.** 149 tokens, 0.375 USD. The single-step test (`test_opencode_sums_the_token_kinds_of_one_step`) still reads 117 tokens and 0.125 USD.

## Test runs

- `make harness` (via `make check`): `evals/diagram-following` 215 passed.
- `make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`: exit 0, every target passing, the mock scenario check ending `5 scenario(s), 5 pass, 0 fail`.
