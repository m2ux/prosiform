## Overview

The composition edge workflows have a measured shakedown, committed live records on each shell harness and a published account matching those records. The work follows the delivered compiled form, composition and dispatch grammar.

## Problem

- **The edge workflows have no committed live measurement.**
  Corpus and harness checks cannot establish how a live agent follows them.
- **The runbook needs observed sessions.**
  Its budget and triage treatment must be checked before the full run.
- **The evaluation page needs recorded results.**
  Its rates must identify the corpus and records they describe.

## Proposal

- **A shakedown establishes the run.**
  Read the integrated guide, workflows and scorer; reconcile baseline and edge workflow selections; exercise each shell harness before setting the measured budget.
- **The live records follow the runbook.**
  Each selected shell harness runs the edge matrix and commits its own composition-edge report. Every failing session receives the rubric's disposition.
- **The page follows the evidence.**
  Its compiled form, edge workflow inventory and pass rates agree with the corpus and committed records.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-05-i14-evaluation-refinement/e00/w01.md) | Shake down the edge-run runbook | AC1, AC2 | [I10:E04:W17](https://github.com/m2ux/prosiform/issues/579), [I10:E04:W18](https://github.com/m2ux/prosiform/issues/579), [I10:E04:W19](https://github.com/m2ux/prosiform/issues/579), [I10:E06:W01](https://github.com/m2ux/prosiform/issues/639) | | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-05-i14-evaluation-refinement/e00/w02.md) | Record the live edge workflow run | AC3, AC4 | W01 | | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-05-i14-evaluation-refinement/e00/w03.md) | Publish the measured edge workflow results | AC5, AC6 | W02 | | | |

## Acceptance Criteria

- [ ] **AC1.** The edge-run runbook records a shakedown on each shell harness whose measured cost determines the run budget, as the runbook and shakedown records show.
- [ ] **AC2.** Every rubric entry for a pf-run failure class decides a shakedown session or is recorded as produced by none, as the shakedown record shows.
- [ ] **AC3.** Each shell harness has a committed edge-case record carrying a cell for every default-matrix model and every form and scenario of the edge workflows, as a comparison of the records against that matrix and the workflow corpus shows.
- [ ] **AC4.** Each edge-case record gives every failing session the triage rubric's disposition, as the committed records show.
- [ ] **AC5.** The evaluation README describes the compiled form and every edge workflow and scenario, as a comparison against the corpus shows.
- [ ] **AC6.** The evaluation README's pass rates match each committed edge-case record, as a comparison against the records shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-05-i14-evaluation-refinement) — the deferral decision and work items.
- **R2.** [Composition Following](https://github.com/m2ux/prosiform/issues/579) — the scenario and harness implementation providing the run inputs.
