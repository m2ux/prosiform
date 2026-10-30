# W05 Validation

**Branch:** `i05/e01/w05-first-baseline-from-the` at `b3a6d106`, cut from `i05/e01/main` at `22ae0f2e`. **Pull request:** [#379](https://github.com/m2ux/prosiform/pull/379), merged as `961df526`.

Every check ran in the task worktree. `make check` ran with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 The baseline and its report come from the default matrix

**Covers:** AC9. **Result:** ✓

- **Pre-run check.** `~/projects/eval/prosiform/config/.credentials.json` was present (presence only read). No `CLAUDE.md` was in `~/projects/eval/`, `~/projects/` or `~`.
- **Command.** `uv run --project src --frozen python evals/diagram-following/run.py --models claude-haiku-5-5,claude-sonnet-5-5 --repetitions 5 --session-budget-usd 0.25 --budget-usd 40`, from the worktree root.
- **Run record.** `run.json` of run `20261028T165414Z` holds options `models claude-haiku-5-5,claude-sonnet-5-5`, `repetitions 5`, `workflows null` (every one), `forms bundle,tree,prose`, `session_budget_usd 0.25`, `budget_usd 40`; `sessions 150`, `started 150`, `cost_usd 4.006788`, `not_started []`.
- **Baseline.** `evals/diagram-following/baseline.json` names run `20261028T165414Z`, both models, 5 repetitions and cost 4.006788, and holds 30 cells: two models by three forms by five scenarios over `branching`, `linear` and `looping`, each 5 sessions.
- **Report.** `evals/diagram-following/report.md` is the run's report as the runner wrote it, before a baseline existed; byte-identical to the report `--write-baseline` wrote.
- **Sessions.** Every session exited 0, none reached its timeout, none wrote `stderr.log`. One record read in full (`claude-haiku-5-5/looping/two-rounds/bundle/1`): its trace is `Draft Review Revise Check Review Revise Check Review Publish`, equal to the expected path, with each state's action file present.

## T2 The report over the baseline run against the committed baseline shows no difference

**Covers:** none. **Result:** ✓

`report.py results/20261028T165414Z` against the committed `baseline.json`: all 38 rows (30 cells, 6 model-and-form, 2 model) carry `in_baseline` true, pass-rate difference 0 and every failure-class difference 0; `baseline_only` is empty at every level. `report.md` reads `+0 pts` on all 38 rows.

## T3 The command, matrix and measured cost are documented, and no check starts a paid session

**Covers:** AC10. **Result:** ✓

Inspection at `b3a6d106`:

- **README.** `evals/diagram-following/README.md` names `make eval-diagrams` in its command table with the measured cost (about USD 4, about 10 minutes) and its USD 75 budget, lists every runner option with its default, states the default matrix (two models, five scenarios of three workflows, three forms, five repetitions: 150 sessions) and, under "Default matrix and cost", the measured cost USD 4.01 with a per-model table: `claude-haiku-5-5` 0.0038 a session, 0.29 a run, 15 s; `claude-sonnet-5-5` 0.0496 a session, 3.72 a run, 18 s.
- **Makefile.** `check` depends on `lock-check lint format-check typecheck test harness corpus smoke layout tables links vocabulary invocation conformance independence steps`. None depends on `eval-diagrams`, the one recipe naming `run.py`. `harness` runs the runner tests, which start `stub_agent.py` through `--agent-command`.

## T4 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits 0 at `b3a6d106`: lint and typecheck clean, `test` 1302 passed, `harness` 812 passed, and the corpus, smoke, layout, tables, links, vocabulary, invocation, conformance, independence and steps checks.
