# I10:E00 W04 Shake Down the Baseline Runbook — November 2026

> Task delivery · Created 2026-11-03

## Executive Summary

The baseline runbook shaken down on the hardened corpus on the user's model, its faults fixed and its budget and cost cap set from the measured cost.

This record holds its delivery of `AC10`: the work item, the validation evidence for every check the work item names, and the plan changes the session applied and held.

## Validation

### T1: Baseline shakedown

`make eval-diagrams HARNESS=opencode` over the default matrix's 74 cells, one repetition, on `openrouter/deepseek/deepseek-v4.1-flash-1017`, as run `baseline-shakedown-3` on 2026-11-04. All 74 sessions started and the run recorded `completed`: 20 815 533 tokens for USD 0.551214, the largest session 1 414 151 tokens and the mean 281 291.

71 passed. Every charted form passed in full: `bundle` 24/24, `tree` 24/24, `linked` 9/9, `prose` 9/9, `compiled` 3/3, `bootstrap` 2/2.

Three runs preceded it and each stopped on a `defect`, which the runbook's stop rules forbid committing:

- `baseline-shakedown` at 09:10 scored a corpus that predated the `Entry`/`Exit` heading, so its 68 passes measured another workflow shape.
- `baseline-shakedown-2` passed 7 of 74. 67 failed `wrong_branch` at divergence 0, each omitting `Entry` and `Exit`, because `instruction.md` still told a session never to trace "the diagram's start or stop marker" while the corpus required the opposite. Corrected in `fa3c85b2`, probed on one `linear/bundle` session at USD 0.0048 as run `entry-probe`, then repeated.

### T2: Triage

`dispositions.json` beside the run's `run.json` decides all three failures. Each is `miss`: the `authored` form's step links `review.md`, `plan.md` or `draft.md`, and the session named `workflow.md#<heading>` in its sub-agent prompts. Each sub-agent ran, returned `done`, and wrote its action, and the `together` flags match the step, so only the section's document was misnamed.

The report lists no `untriaged` session and no `defect` or `unclear` one, which the runbook requires before a run is committed.

### T3: Caps

The session cap is the largest session doubled and rounded up to the next ten thousand: 1 414 151 to 2 830 000, which `DEFAULT_SESSION_BUDGET` states. `EVAL_BUDGET_TOKENS` is the default matrix's 760 sessions at that cap, 2 150 800 000. A harness reporting dollars takes its cost cap from twice its sessions times mean session cost, USD 2 at USD 0.007449 a session.

`test_runbook.py` reads the cap from the shakedown row stating it and the budget from the Makefile, so a cap that does not follow the measurement, or a budget below the matrix's need, fails.

### T4: `make check`

Passes over the whole repository: 1 363 tests, the 516 fixtures, the 3 185 vocabulary terms, the conformance report and the independence check.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w04.md](w04.md) | The W04 work item: the baseline shakedown's design, budget rule and tests, its Validation and change list. |
| [ac10-tests.patch](ac10-tests.patch) | Regression tests for the baseline model, completed measurement, derived caps and default-matrix budget; applied once the shakedown completes. |
| [codex-adapter.md](codex-adapter.md) | The native Codex adapter's protocol, isolation, dispatch evidence, usage and test design. |
| [Evaluation request](evaluation-request.md) | The shakedown's material, destination, command, limits and execution approval |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I10:E00 Corpus Separability](https://github.com/m2ux/prosiform/issues/403) |
| Initiative | [I10 Evaluation and Checks](https://github.com/m2ux/prosiform/issues/464) |
| Epic record | [Evaluation and Checks](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) |
