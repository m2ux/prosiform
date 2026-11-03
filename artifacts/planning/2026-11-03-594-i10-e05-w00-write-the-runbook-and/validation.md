# I10:E05 W00 Validation — November 2026

> Validation evidence · Created 2026-11-03

## Executive Summary

Each check the [W00 work item](../2026-11-01-464-i10-evaluation-and-checks/e05/w00.md) names, run against branch `i10/e05/w00-write-the-runbook-and` at `41841001`.

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

- **T5 — Proof shakedown.** Not run.
  The shakedown's harness `claude` and model `claude-haiku-5-5`, named by the user on 2026-11-03, are recorded in `RUNBOOK.md` with the USD 5 cap and a USD 0.80 estimate. The run stopped before its first session, spending nothing:

  ```text
  workflow.CorpusError: /home/mike1/projects/eval/prosiform/config/plugins/installed_plugins.json installs a plugin, whose hooks reach every session before its first turn; remove /home/mike1/projects/eval/prosiform/config/plugins/installed_plugins.json before this run
  ```

  `installed_plugins.json` installs a managed plugin at `managed` scope, and the signed `remote-settings.json` enables it with telemetry environment. Both are org-managed and were left untouched, so no cost was measured and the proof's budget is unset.

## Make check

- **T6 — `make check` with `PROSIFORM_BUILD` naming the worktree's build.**
  Exit 0: 1663 check tests and 1262 harness tests pass, and `make links`, `make tables` and every other target pass.
