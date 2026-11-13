## Overview

The eval's committed records measure real use: the bare-prompt records leave, and one baseline run on the skill-entry eval, shaken down under the runbook, replaces them. The harness and model are the user's choice when the run starts.

## Problem

- **Every committed record is a bare-prompt run.**
  [`baseline.json`](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/README.md#L367), the feature proof and the agent-pick run each started their sessions from an instruction naming an entry file.
- **The runbook runs the bare-prompt eval.**
  Its [MVP proof, baseline, edge and agent-pick sections](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/RUNBOOK.md#L94-L244) set caps from bare-prompt shakedowns.

## Proposal

- **The bare-prompt records leave.**
  `baseline.json`, `report.md`, `mvp-proof.json`, `mvp-proof.md`, `agent-pick.json` and `agent-pick.md` are deleted with the README and runbook sections that describe them.
- **The baseline covers every workflow.**
  Every harness gives a shell, so the split between baseline and edge workflows leaves and the default matrix holds every workflow.
- **A runbook section states the real-use baseline.**
  Its shakedown, one repetition of every cell on the harness and model the user names, sets the session cap, token budget and cost cap.
- **The baseline is the run the section states.**
  Its failing sessions are triaged under the rubric, and `baseline.json` and `report.md` are written from it.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e02/w01.md) | Bare-prompt records and sections deleted | AC1 | [E01:W06](https://github.com/m2ux/prosiform/issues/736) | | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e02/w02.md) | Real-use baseline runbook section | AC4 | W01 | | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e02/w03.md) | Real-use baseline shakedown | AC2 | W02 | | | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e02/w04.md) | The real-use baseline run and record | AC3 | W03, [I15:E02:W00](https://github.com/m2ux/prosiform/issues/733) | | | |

## Acceptance Criteria

- [ ] **AC1.** No record of a bare-prompt run, and no README or runbook section describing one, remains in the eval, as the README and runbook tests show.
- [ ] **AC2.** The runbook's real-use baseline section takes its session cap, token budget and cost cap from a recorded shakedown on the skill-entry eval, as the runbook test shows.
- [ ] **AC3.** `baseline.json` and `report.md` record a run of every workflow of the skill-entry eval whose every failing session is triaged and none is a defect or unclear, as the report's Failing Sessions shows.
- [ ] **AC4.** The runbook states a real-use baseline section whose caps are set by a shakedown rule, as the runbook test shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-real-use-eval) — the records decision and why the run rows stay apart.
- **R2.** [Runbook](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/RUNBOOK.md) — the triage rubric and stop rules the run follows.

