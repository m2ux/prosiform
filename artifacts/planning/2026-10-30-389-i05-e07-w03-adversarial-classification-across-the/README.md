# I05:E07 W03 Adversarial Classification — October 2026

> Task delivery · Created 2026-10-30

## Executive Summary

The scorer's four dispatch checks are tested one departure each, on one scenario. A class that fired for the wrong reason would pass every test the corpus holds, because no test puts a scenario beside a departure other than the one it was written for.

This record holds the delivery of W03: each departure the stub agent states, run over every dispatch scenario in both of its forms, so every cell is classified by the class its script predicts and a correct run stays passing. It is fixture coverage and not a baseline: the stub walks the workflow's own diagram, so its pass rates are correct by construction and no baseline file is written.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W03 work item](w03.md) | The matrix: each departing script over every dispatch scenario in both forms, with the class each cell must read |
| [Validation](validation.md) | Each check the work item's Test row names, with the revision it ran on and what it observed |
| [Change list](change-list.md) | The plan changes this session met and those it held |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E07 Dispatch Following](https://github.com/m2ux/prosiform/issues/389) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic record | [Dispatch Following design](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-29-389-i05-e07-dispatch-following) — the design, the W03 work item |
| Preceding rows | [W01](https://github.com/m2ux/prosiform/pull/411) and [W02](https://github.com/m2ux/prosiform/pull/413) — the scenarios and the checks this row exercises |
| Moved row | The measured baseline, now I05:E08 W02 — one run covering every form |
