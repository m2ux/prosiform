# Validation — I05:E01 W09

> Task delivery · Created 2026-10-29

## Delivery Checkpoint

- Epic: [I05:E01] Diagram Following — https://github.com/m2ux/prosiform/issues/333
- Task issue: [#396](https://github.com/m2ux/prosiform/issues/396)
- Branch: `i05/e01/w09-refused-run-a-matrix`, cut from `origin/i05/e01/main` at `63a5f6e6`
- Worktree: `/home/mike1/projects/dev/md-composer/.worktrees/i05/e01/w09-refused-run-a-matrix`
- Tested revision: `7ff0a13e`
- Environment: `UV_CACHE_DIR=/tmp/w09-uv`, `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen pf"`

## Test Plan

Every row was executed at the head of this branch. Instrument: the eval's own tests under `evals/diagram-following/`, and `make check`. No paid session ran.

| Test | Description | Coverage | Result |
| --- | --- | --- | --- |
| T1 | A run whose every session errored is refused, with one session's message as the reason | AC21, AC1 | ✓ Pass |
| T2 | A refused run's report names the state and reason and gives no row or comparison | AC21, AC1 | ✓ Pass |
| T3 | `--write-baseline` refuses a refused run | AC21, AC1 | ✓ Pass |
| T4 | A genuine mix of an errored session beside a passing one is a completed result | AC21 | ✓ Pass |
| T5 | A run the budget stopped part way is not refused | AC21 | ✓ Pass |
| T6 | The eval README's report section and `checks.md`'s `make harness` row state the refused run | AC1 | ✓ Pass |
| T7 | `make check` over the whole repository | — | ✓ Pass |

## Checks

### T1 A run whose every session errored is refused, quoting the agent's message

**Where:** `evals/diagram-following/test_run.py::test_a_run_whose_every_session_errored_is_refused_and_reported_as_such`

`STUB_AGENT_ERROR` makes the stub's `result` message report `is_error` true for every session, and `STUB_AGENT_REASON` supplies the text a refused agent prints (`You've hit your weekly limit`). The run starts both sessions of one workflow in the `bundle` form and asserts:

- `run.json` and the returned record both carry `"state": "refused"`, and both carry that exact reason;
- `started == sessions == 2`, so the whole matrix ran;
- every `session.json` carries the `errored` failure class.

**Result:** ✓ Pass.

### T2 A refused run's report names the state and reason and gives no rows

**Where:** `evals/diagram-following/test_run.py::test_a_run_whose_every_session_errored_is_refused_and_reported_as_such`, second half; `evals/diagram-following/test_report.py::test_a_refused_run_gives_its_state_and_reason_and_no_row`

After the run, `report.json` carries `"state": "refused"` and the same reason; `cells`, `by_form` and `by_model` are all empty and `baseline_only` is empty at every level; `baseline` is null although a baseline file exists beside the reporters. `report.md` carries `**State:** \`refused\``, the quoted `You've hit your weekly limit`, and "not compared", and carries no `Pass rate` column and no `## By Model` table.

The report test drives the same behaviour from a hand-made run directory holding a refused `run.json` and a real baseline, so the report is shown to read the state rather than infer it: the same records under a `completed` state would produce rows and differences.

**Result:** ✓ Pass.

### T3 A refused run writes no baseline

**Where:** `evals/diagram-following/test_run.py::test_a_refused_run_writes_no_baseline`

`report.main` with `--write-baseline` over the refused run raises `CorpusError` matching `refused, so it has no cells`, and the baseline file is never created. A baseline written from a refused run would record pass rates of zero for every cell and compare every later run against a refusal.

**Result:** ✓ Pass.

### T4 A genuine mix of an errored session beside a passing one is a result

**Where:** `evals/diagram-following/test_run.py::test_a_run_with_a_genuine_mix_of_errors_and_states_is_a_result`

`STUB_AGENT_ERROR_ONCE` makes the first session report an error and the rest walk the path, so the run holds one `errored` session beside one passing session. The run records `"state": "completed"` and `reason: null`, and its report carries a cell with one pass. This is the far side of the boundary: an error on a real fault is a failure class in a result, not a refusal.

**Result:** ✓ Pass.

### T5 A run the budget stopped part way is not refused

**Where:** `evals/diagram-following/test_run.py::test_a_run_the_budget_stopped_part_way_is_not_refused`

Every session of the run errors, but the budget starts only three of the five, so two are listed as not started. The run records `"state": "completed"`, since an unfinished matrix is not a wholly errored one: the two it never started might have entered a state.

**Result:** ✓ Pass.

### T6 The documentation states the refused run

**Where:** `evals/diagram-following/README.md`, sections **Scoring** and **Reading the report**; `checks.md`, the `make harness` row.

Inspected. The eval README's Scoring section now states that a run every session of which took `errored` is refused, that `run.json` records the state and a reason quoted from one session's own `result` text, and where the boundary is decided: a whole matrix started and wholly errored, decided once the sessions settle and before `run.json` is written. Its Reading the report section states that a refused report gives the state and reason with no row and no comparison, and that `--write-baseline` refuses one. `checks.md`'s `make harness` row now names the refused state among what the runner's stub-agent tests assert, and the state and reason among what the report gives in place of a pass rate.

**Result:** ✓ Pass.

### T7 `make check` over the whole repository

**Where:** the worktree, `make check`.

Every target passed, exit 0: `lock-check`, `lint`, `format-check`, `typecheck`, `make test` (1302 passed), `make harness` (836 passed), `corpus`, `smoke`, `layout`, `tables`, `links`, `vocabulary`, `invocation`, `conformance`, `independence`, `steps`.

**Result:** ✓ Pass.

## Mutation Checks

Each new behaviour was removed in turn and the eval's suite rerun, so each test is shown to observe what it claims.

| Mutation | Observed |
| --- | --- |
| `outcome` never refuses, however the sessions scored | `test_a_run_whose_every_session_errored_is_refused_and_reported_as_such` and `test_a_refused_run_writes_no_baseline` both fail |
| `outcome` refuses without requiring the whole matrix to have started | `test_a_run_the_budget_stopped_part_way_is_not_refused` fails: `assert ('refused' == 'completed')` |
| `report()` ignores the run's state and always reports rows | `test_a_refused_run_gives_its_state_and_reason_and_no_row`, and both runner tests above, fail |

## Test Runs

| Run | Command | Result |
| --- | --- | --- |
| Eval tests | `uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . evals/diagram-following/` | ✓ 93 passed |
| Full suite | `make check` | ✓ exit 0 — lint, format-check, typecheck, `make test` 1302 passed, `make harness` 836 passed, and every document check |

No paid session ran. Every test drives the stub agent beside the suite.

## Limitations

- The state is decided from the verdict records the runner writes, so a session whose `session.json` is missing is read as not errored and leaves the run completed. No path in `run` writes a record for a session it started without one.
- The reason is the first session's `result` text in matrix order. When sessions were refused for different reasons — one login limit and one crash — only the first is quoted, and the rest are visible only in their own records.
- AC21 is observed against the stub agent alone. No paid run was made, so nothing here shows a real spent login producing `errored` sessions in every place this test's stub does; W07 and W08 established that path separately.
