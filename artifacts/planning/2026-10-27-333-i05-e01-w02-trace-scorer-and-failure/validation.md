# W02 Validation

**Branch:** `i05/e01/w02-trace-scorer-and-failure` at `c4f213f2`, cut from `i05/e01/main` at `d35ef693`. **Pull request:** [#336](https://github.com/m2ux/prosiform/pull/336).

Every check ran in the task worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`. The scorer tests are `evals/diagram-following/test_score.py`, beside the corpus reader and run by `make harness`; 17 pass, alongside the corpus's 26.

## T1 A run walking its scenario path with every action done passes

**Covers:** AC4. **Result:** ✓

`test_a_run_walking_its_scenario_path_with_every_action_passes` lays out, for each of the five scenarios, a workspace whose `trace.log` is the scenario's path and whose `actions/` holds each state's file with its stated value and a trailing newline. Each verdict is `passed`, with no failure, no divergence and no actions named.

## T2 Each failing trace is classified at its first divergence

**Covers:** AC4. **Result:** ✓

One hand-made trace per class, each with every entered state's action done, gives that class and its divergence index and no other:

| Class | Workflow, scenario | Trace | Divergence |
| --- | --- | --- | --- |
| wrong branch | branching, high-severity | Intake, Triage, Queue, Resolve | 2 |
| skipped state | linear, straight-through | Plan, Test, Ship | 1 |
| invented state | linear, straight-through | Plan, Build, Deploy, Ship | 2 |
| loop miscount | looping, two-rounds | Draft, Review, Revise, Check, Review, Publish | 5 |
| missing action | linear, straight-through | the path, `build.txt` absent and `ship.txt` holding other content | 1 |
| unfinished | linear, straight-through | Plan, Build | 2 |

Loop miscount is also reached by taking the loop once more than `no-rework` requires (divergence 2), and stands apart from wrong branch because the decision it diverges at counts `trace.log` lines. Unfinished is also reached by an absent `trace.log` and an empty one (divergence 0). A state entered after the terminal one (`Ship` then `Plan`) and a step back no walk reaches (`Build` then `Plan`) are invented states.

## T3 Trace reading and the verdict record

**Covers:** AC4. **Result:** ✓

`test_a_trace_is_read_stripped_of_blank_lines_and_surrounding_whitespace` reads a log with blank lines, leading and trailing spaces and a tab as the four state names, and passes it. `test_a_name_in_another_case_is_a_state_the_diagram_does_not_hold` scores `build` as an invented state. `test_the_record_is_plain_json_values` round-trips `Verdict.record()` through `json` to `passed`, `failure`, `divergence`, `expected`, `actual` and `actions` as plain values.

## T4 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits `0` at `c4f213f2`: lock, lint, format and typecheck (over `evals`, the scorer included), `test` (1176 passed), `harness` (704 passed), `corpus`, smoke, layout (`evals/` — 44 tracked files), tables, links, vocabulary, invocation, conformance and independence.
