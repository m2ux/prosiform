# I10:E05 W00 Validation — November 2026

> Validation evidence · Created 2026-11-03

## Executive Summary

Each check the [W00 work item](../2026-11-01-464-i10-evaluation-and-checks/e05/w00.md) names, run against branch `i10/e05/w00-write-the-runbook-and` at `e23d83b9`.

## AC6

- **T1 — Rubric test.**
  `test_runbook.py::test_the_rubric_decides_every_class_the_scorer_gives` passes under `make harness`: the By Class table's rows are exactly the `Failure` members of `score.py`, `errored` among them. `test_the_rubric_gives_the_dispositions_the_report_reads` holds the disposition table to `report.DISPOSITION_NAMES`.
- **T2 — Read of the rubric against the scorer.**
  Each of the twelve classes has a `miss`, `defect` and `unclear` condition read from the session's records, and the disposition table gives each disposition's action: a miss is recorded and the run continues; a defect or an unclear session stops the run, commits nothing and is escalated. The rubric states that a run never edits a scenario, a form, the instruction, the harness, the runner or the scorer. `test_report.py` holds the report to listing each failing session with its disposition and refusing one outside the three.

## AC7

- **T3 — Runbook options test.**
  `test_runbook.py::test_each_runbook_passes_only_options_the_runner_accepts` passes for the MVP proof, the baseline and the edge run: every option in each runbook's `ARGS` is one `run.py --help` names. `HARNESS=` is the Makefile's variable for `--harness`.
- **T4 — Read of the runbooks against `run.py --help`.**
  Each runbook states its command and arguments, model, harnesses, forms, session cap, token budget, cost cap, stop rules and committed files. The proof's matrix is 150 sessions on any harness, read from `run.matrix` over the six feature workflows. The baseline's and edge run's budgets are formulas that E00 W04 and E04 W16 set from their shakedowns; the edge run's `staged` form and workflows arrive with E04's earlier rows.

## AC8

- **T5 — Proof shakedown.** Pass.
  Run `mvp-proof-shakedown`, the command `e23d83b9` records run on the code at `d8cfd26f`, on the harness `claude` and model `claude-haiku-5-5` the user named on 2026-11-03, within the USD 5 cap after a USD 0.80 estimate:
  - **Result.** `completed`: 30 of 30 sessions started and passed, so no failing session took a disposition and none was a defect or unclear.
  - **Measured.** USD 0.123701 in all, USD 0.004123 a session; 3 593 668 tokens, 119 789 a session, the largest 206 458.
  - **Budget set.** The proof's session cap is 420 000 tokens, its token budget 63 000 000 and its cost cap USD 2, as `RUNBOOK.md` records with the formula each follows.
  - **Managed plugin.** `run.json` names a managed plugin and six telemetry environment keys. Every one of the 30 transcripts holds its `SessionStart:startup` `hook_response` carrying the organisation's `additionalContext`, and the run completed, so the hook response is accepted rather than failing the run.
- **Earlier attempts.**
  - At `41841001` the preflight refused the eval login's managed plugin. By the user's decision of 2026-11-03 the preflight admits it at `60a2c02d` ([#597](https://github.com/m2ux/prosiform/issues/597) closed as not planned).
  - Two attempts at `60a2c02d` and `d8cfd26f` were `refused`: every session `errored` on an expired OAuth session, USD 0, until the user renewed the eval login.
  - The next attempt completed but started 16 of 30 sessions, USD 0.073912: a session records over 100 000 tokens, its cache reads included, so the runner's 60 000 default session cap exhausted the 1 800 000 budget. The shakedown's command now passes `--session-budget-tokens 400000` and `--budget-tokens 12000000`, the fault fixed on this branch.
  - The shakedown's spend over every attempt is USD 0.197613.

## Make check

- **T6 — `make check` with `PROSIFORM_BUILD` naming the worktree's build.**
  Exit 0 at `e23d83b9`: 1663 check tests and 1264 harness tests pass, and `make links`, `make tables` and every other target pass.
