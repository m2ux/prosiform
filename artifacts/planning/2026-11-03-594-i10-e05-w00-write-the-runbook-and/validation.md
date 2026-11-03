# I10:E05 W00 Validation — November 2026

> Validation evidence · Created 2026-11-03

## Executive Summary

Each check the [W00 work item](../2026-11-01-464-i10-evaluation-and-checks/e05/w00.md) names, run against branch `i10/e05/w00-write-the-runbook-and` at `d8cfd26f`.

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

- **T5 — Proof shakedown.** Not run to a measurement.
  The shakedown's harness `claude` and model `claude-haiku-5-5`, named by the user on 2026-11-03, are recorded in `RUNBOOK.md` with the USD 5 cap and a USD 0.80 estimate.
  - **First attempt, at `41841001`.** The preflight refused the eval login before any session: `installed_plugins.json` installs a managed plugin at `managed` scope and the signed `remote-settings.json` enables it.
  - **User decision, 2026-11-03.** The org-managed plugin is allowed. At `60a2c02d` the preflight admits a plugin installed at managed scope or enabled by signed remote settings, and `run.json` and the report name it, its version and the environment it adds ([#597](https://github.com/m2ux/prosiform/issues/597) closed as not planned).
  - **Second attempt, at `60a2c02d`, run `mvp-proof-shakedown`.** The preflight passed and all 30 sessions started, with `run.json` recording a managed plugin and six telemetry environment keys. Every session took `errored` with `Failed to authenticate: OAuth session expired and could not be refreshed`, so the run is `refused`, its tokens 0 and its summed cost USD 0. No session reached a hook response, so the managed hook's transcript record is unobserved.
  - **Third attempt, at `d8cfd26f`, 07:44 CET.** Refused the same way: all 30 sessions `errored` on `OAuth session expired and could not be refreshed`, USD 0. The eval config's `.credentials.json` was last written at 07:35:03, when the second attempt's failed refresh left its access and refresh tokens empty, and its `history.jsonl` holds one interactive entry, `quit`, so no `/login` completed in that directory.
  - **What it waits on.** A renewed eval login, `CLAUDE_CONFIG_DIR=~/projects/eval/prosiform/config claude` then `/login`, which writes under `config/` and is the user's to run.

## Make check

- **T6 — `make check` with `PROSIFORM_BUILD` naming the worktree's build.**
  Exit 0 at `d8cfd26f`: 1663 check tests and 1264 harness tests pass, and `make links`, `make tables` and every other target pass.
