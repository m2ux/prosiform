## Overview

The composition, deferral and dispatch evaluation has published measurements backed by a measured runbook and committed session evidence. Its goal is an auditable account of how agents follow the edge workflows, with every failed session classified under the triage rubric.

## Problem

The edge workflows have corpus and harness tests but no committed live measurement.

- **A test does not establish agent behavior.**
  Controlled checks establish compiled paths and scoring; only a live session shows which path an agent follows.
- **A live run needs a measured budget.**
  The shakedown establishes the session limits and token or cost cap before the full run starts.
- **A result needs traceable evidence.**
  A reader needs the source revision, run configuration and failure dispositions behind the published rates.

## Proposal

- **The runbook is exercised first.**
  A shakedown of the edge workflows establishes the budget and tests the rubric against real sessions.
- **The records preserve the measured scope.**
  Each shell harness has a committed edge record, with the matrix's model, form and scenario cells and a rubric disposition for every failed session.
- **The published account follows the records.**
  The evaluation page identifies the compiled form, workflow inventory and measured pass rates against those records.
- **The work is deferred beyond the release.**
  Measurement starts after its scenario and harness implementation is integrated. The MVP release has no dependency on these measurements.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/661) | Composition Measurements | AC1 | | |

## Acceptance Criteria

- [ ] **AC1.** The published edge evaluation is supported by committed measurements taken under its measured runbook, as a review of the evaluation page against the workflow corpus, runbook and session records shows.

## Non-Goals

- It does not gate the MVP release.
- It does not replace the baseline or feature-proof records.
- It does not select a paid-run model or authorize a live run.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-05-i14-evaluation-refinement) — the deferred scope, source mapping, work items and delivery decisions.
- **R2.** [Composition Following](https://github.com/m2ux/prosiform/issues/579) — the corpus and harness implementation supplying the measurement inputs.
- **R3.** [Evaluation and Checks](https://github.com/m2ux/prosiform/issues/464) — the originating initiative, whose edge measurement is deferred here.
