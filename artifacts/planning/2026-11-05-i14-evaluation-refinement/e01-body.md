## Overview

The committed evaluation baseline measures every cell the default matrix runs, the bootstrap-audit scenarios among them, and each harness the eval defines has a committed run of that matrix whose sessions all ended without a crash. The work extends the eval's committed records to the matrix's full scope, so the baseline's cells and each harness's crash evidence are readable from what the repository holds.

## Problem

- **The baseline omits the bootstrap-audit cells.**
  The default matrix builds more cells than the committed baseline carries, so those scenarios have no measured pass rate.
- **One harness carries the crash evidence.**
  The committed baseline's sessions ran on one harness, and a harness with no committed record has no crash-free evidence of its own.

## Proposal

- **The baseline covers the matrix.**
  A default-matrix run records a cell for every model, form and scenario the matrix builds, and the committed baseline carries each of them.
- **Each harness carries its own record.**
  The default matrix runs on every harness the eval defines, and each run's record is committed beside the baseline so its sessions' exit statuses are readable.
- **The page follows the records.**
  The evaluation README names the committed default-matrix baseline and each harness record, and states the crash-free result each one shows.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-05-i14-evaluation-refinement/e01/w01.md) | Reconcile the default-matrix baseline cells | AC1 | | | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-05-i14-evaluation-refinement/e01/w02.md) | Record cross-harness crash-free runs | AC2 | | | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-05-i14-evaluation-refinement/e01/w03.md) | Publish the harness coverage evidence | AC3 | W01, W02 | | | |

## Acceptance Criteria

- [ ] **AC1.** The committed default-matrix baseline carries a cell for every model, form and scenario the default matrix runs, the bootstrap-audit scenarios among them, as a comparison of the baseline file against the matrix shows.
- [ ] **AC2.** Every harness the eval defines has a committed default-matrix run whose every session ended without a crash, as that run's record shows.
- [ ] **AC3.** The evaluation README's default-matrix and harness statements match the committed baseline and run records, as a comparison of the page against those records shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-05-i14-evaluation-refinement) — the deferral decision, work items and delivery decisions.
- **R2.** [Evaluation and Checks](https://github.com/m2ux/prosiform/issues/464) — the originating initiative, whose default-matrix baseline and cross-harness coverage are deferred here.
