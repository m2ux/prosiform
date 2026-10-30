# W04 Validation

**Branch:** `i05/e01/w04-report-baseline-comparison-and` at `f06ef18d`, cut from `i05/e01/main` at `befb47ed`. **Pull request:** [#338](https://github.com/m2ux/prosiform/pull/338).

Every check ran in the task worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`. The report tests are `evals/diagram-following/test_report.py`, run by `make harness`; 8 pass, alongside the runner's 11, the scorer's 23 and the corpus's 26. They read a hand-made run: a `run.json` and ten `session.json` records over two models and four cells — passes; `unfinished`, `loop_miscount`, `skipped_state` and `missing_action` failures; one session ended at its timeout with no usage or cost — and two sessions not started, against a baseline holding two of those cells and one the run lacks. No live session ran.

## T1 Each row gives its pass rate and failure classes per model, form and scenario

**Covers:** AC8. **Result:** ✓

- `test_each_cell_gives_its_pass_rate_failures_timeouts_tokens_and_cost`: four cells, keyed and ordered by model, form, workflow and scenario. The `claude-haiku-5-5` `bundle` `linear` `straight-through` cell holds 4 sessions, 3 passed, pass rate 0.75, `unfinished` 1 and every other class 0, 1 timeout, mean tokens over the three sessions recording usage and mean cost 0.2 over the three recording a cost. The `tree` cell holds `skipped_state` 1 and `missing_action` 1 at pass rate 0.
- `test_the_roll_ups_gather_each_model_and_form_and_each_model`: four model-and-form rows; `claude-haiku-5-5` across forms holds 8 sessions, 4 passed, pass rate 0.5, its four classes, 1 timeout and mean cost over its seven costed sessions.
- `test_the_report_gives_the_run_cost_and_the_sessions_not_started`: run id, models, repetitions, 10 of 12 started, cost USD 2.75 and the two sessions not started, from `run.json`.

## T2 Each row carries its difference from the baseline

**Covers:** AC8. **Result:** ✓

- `test_without_a_baseline_no_row_is_compared`: with no baseline file, `baseline` is null, every row's `in_baseline` and `difference` are null, and `baseline_only` is empty at every level.
- `test_each_row_carries_its_difference_from_the_baseline`: the `bundle` cell's difference is pass rate +0.25 and `unfinished` −1; the `prose` cell's −0.5 and `loop_miscount` +1. The model roll-ups compare with rows summed from the baseline's cells: `claude-haiku-5-5` 0.5 less 4/6, `claude-sonnet-5-5` +0.5 with `wrong_branch` −1.
- `test_rows_absent_from_either_side_are_marked`: the cells and model-and-form rows the baseline lacks carry `in_baseline` false and no difference; `baseline_only` lists the baseline's `claude-sonnet-5-5` `tree` cell and its model-and-form row, and no model.
- `test_the_command_writes_the_report_beside_the_run`: `report.py <run> --baseline <file>` writes `report.json`, equal to the report, and `report.md`, whose rows carry `+25 pts`, `unfinished 1 (-1)`, `new` for a row the baseline lacks, and list the baseline-only cell and the sessions not started.
- `test_writing_the_baseline_follows_the_comparison_with_the_one_it_replaces`: `--write-baseline` writes the report compared with the old baseline, then the baseline holding the run's id, date, models, repetitions, cost and cells (key, sessions, passed, pass rate, failures); a report against it shows zero difference everywhere.

## T3 A run ends by writing its report

**Covers:** none. **Result:** ✓

`test_a_run_ends_by_writing_its_report` (in `test_run.py`): a stub-agent run of two `linear` `bundle` sessions at USD 0.125 each leaves `report.json` beside `run.json`, with one cell of 2 sessions, 2 passed, mean cost 0.125, run cost 0.25 and none not started.

## T4 The command, matrix and cost are documented, and no check starts a session

**Covers:** AC10. **Result:** ✓

Inspection at `f06ef18d`:

- **Makefile.** `check` depends on `lock-check lint format-check typecheck test harness corpus smoke layout tables links vocabulary invocation conformance independence`. None of those depends on `eval-diagrams`, and no recipe among them names `run.py`; `harness` runs pytest over `checks/tests` and `evals/diagram-following`, whose runner tests start `stub_agent.py` through `--agent-command`, and whose report tests read hand-made records. `eval-diagrams` alone runs `evals/diagram-following/run.py`, with `--budget-usd $(EVAL_BUDGET_USD)` (75) then `$(ARGS)`.
- **`evals/diagram-following/README.md`.** States what the eval measures and why three forms, the scoring and its seven classes, the one-time login, `make eval-diagrams` in a command table with every runner option and its default, the default matrix (two models, five scenarios over three workflows, three forms, five repetitions: 150 sessions), and its cost: at most USD 75, 150 sessions at the USD 0.50 session cap, with the measured figure the `cost_usd` the committed baseline records. It says how to read the report and refresh the baseline.
- **`checks.md`.** States the eval is outside `make check` and the checks hold its runner, scorer and report against a stub agent and recorded results.

## T5 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits `0` at `f06ef18d`: lock, lint, format and typecheck (over `evals`, the report included), `test` (1176 passed), `harness` (729 passed), `corpus`, smoke, layout, `tables` (naming `make eval-diagrams` from the eval's README), links, vocabulary, invocation, conformance and independence. No target starts `claude`.
