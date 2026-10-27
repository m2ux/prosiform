# W03 Validation

**Branch:** `i05/e01/w03-headless-agent-runner-with` at `91f317dc`, cut from `i05/e01/main` at `9466313a`. **Pull request:** [#337](https://github.com/m2ux/prosiform/pull/337).

Every check ran in the task worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`. The runner tests are `evals/diagram-following/test_run.py`, beside the corpus reader and scorer and run by `make harness`; 10 pass, alongside the corpus's 26 and the scorer's 23. Each starts `stub_agent.py` in place of `claude` through `--agent-command`, under an eval root in the test's temporary directory whose `config/` holds an empty `.credentials.json`, with `CLAUDECODE`, `CLAUDE_CODE_ENTRYPOINT`, `CLAUDE_CONFIG_DIR`, `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_BASE_URL` set in the caller's environment, so none starts a paid session.

## T1 Each session starts in a fresh, isolated workspace of its form and inputs

**Covers:** AC5. **Result:** ✓

- `test_the_matrix_holds_one_session_per_model_form_scenario_and_repetition`: two models, three forms and five repetitions over the five scenarios give 150 distinct sessions.
- `test_each_session_starts_in_a_fresh_workspace_of_its_form_and_inputs`: a run of two repetitions with three in parallel starts 30 sessions, each in its own workspace. The stub logs the files each workspace held on starting; across the run they are exactly, per session, `workflow.md` for a bundled form or the diagram source tree for `tree`, plus `inputs/<name>` for each of its scenario's inputs, and nothing a previous session wrote. Each session's arguments carry `--tools Read,Write,Edit,Glob,Grep`, `--strict-mcp-config` and `--disable-slash-commands`, and no `--mcp-config`, `--bare`, `--allowedTools` or Bash; its prompt names `workflow.md`. Its workspace lies under `<eval-root>/workspaces/test/` and is gone once the run ends, as is that directory. Its environment's `CLAUDE_CONFIG_DIR` is `<eval-root>/config`, and it holds none of the caller's variables above and no `CLAUDE_CODE_*` or `ANTHROPIC_*` variable.
- `test_a_bundled_form_is_one_file_and_the_tree_its_sources`: on `looping`, the `bundle` and `prose` forms are one file each and `tree` is the source tree.
- `test_a_run_without_a_login_starts_no_session`: with no `.credentials.json` in `<eval-root>/config` the run raises, naming `CLAUDE_CONFIG_DIR=<eval-root>/config claude` then `/login`, before starting any session or writing a results directory.

## T2 Each session records its transcript, usage, cost and verdict

**Covers:** AC6. **Result:** ✓

- `test_each_session_records_its_transcript_usage_cost_and_verdict`: each of 15 sessions' `session.json` holds exit status `0`, `cost_usd` `0.125`, the stub's `usage`, and its `result` equal to the last line of `transcript.jsonl` in the same directory. Its verdict passes, its `actual` equals the kept `trace.log`, and the kept `actions/` holds the action file of every state on the trace.
- `test_a_failing_session_is_recorded_with_its_failure`: a stub stopped after one state is recorded as `unfinished` with `actual` `["Plan"]`.

## T3 A run stops before its cost would pass its cap

**Covers:** AC7. **Result:** ✓

- `test_a_run_stops_before_its_cost_would_pass_its_cap`: budget USD 1.00, session cap USD 0.25, each session costing USD 0.125, one at a time. Seven sessions start (recorded USD 0.875; an eighth cap would reach USD 1.125); `run.json` and the returned record list the other eight, in matrix order, as not started.
- `test_parallel_sessions_reserve_their_cap_within_the_budget`: the same costs over 30 sessions, four in parallel. The run starts seven, records at most USD 1.00 with no room for another cap, and lists 23 as not started.
- `test_a_session_reporting_no_cost_is_charged_its_cap`: sessions printing no `result` message are charged their USD 0.25 cap, so a USD 0.50 budget starts two.

## T4 A session past its timeout is ended, scored and charged

**Covers:** none. **Result:** ✓

`test_a_session_past_its_timeout_is_ended_scored_and_charged`: two `linear` `bundle` sessions, one at a time, with a 1-second timeout; the first stub writes `Plan`, `Build` and their actions, then hangs. The run ends in under a minute. The first session's `exit_status` is `timeout`, its `cost_usd` null, its kept trace scored `unfinished` with `actual` `["Plan", "Build"]`, and it is charged its USD 0.25 cap; the second then starts and exits `0` at USD 0.125, so the run records USD 0.375 and lists none as not started. The planner directed the timeout on PR #337.

## T5 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits `0` at `91f317dc`: lock, lint, format and typecheck (over `evals`, the runner and stub included), `test` (1176 passed), `harness` (720 passed), `corpus`, smoke, layout, tables, links, vocabulary, invocation, conformance and independence. No target starts `claude`.

## T6 Live session

**Covers:** none. **Result:** Not run — awaiting the eval login

The planned session — `claude-haiku-5-5`, `linear`, `bundle`, `straight-through`, one repetition, session cap USD 0.50 — waits until `~/projects/eval/prosiform/config` holds the eval's claude.ai team login (`CLAUDE_CONFIG_DIR=~/projects/eval/prosiform/config claude`, then `/login`). The planner then runs:

```
uv run --project src --frozen python evals/diagram-following/run.py --models claude-haiku-5-5 --workflows linear --forms bundle --repetitions 1 --parallel 1 --session-budget-usd 0.50 --budget-usd 0.50
```

and records here its cost, tokens, duration, verdict and the `result` message's field names. The runner reads `total_cost_usd` and `usage` and keeps the whole `result` message in `session.json`.
