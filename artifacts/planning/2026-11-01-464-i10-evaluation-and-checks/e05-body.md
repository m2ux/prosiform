## Overview

The MVP is the argument surface and the grouping and composition work merged together, each feature with a diagram-following workflow per permutation ([I09:E05](https://github.com/m2ux/prosiform/issues/523)). This epic proves it: one live run of those workflows on the harness and model the run names, committed beside the baseline, and the eval page stating what it proves and what it cost.

## Problem

- **No session follows a bundle built with the new features.**
  The feature workflows state each path a correct agent walks; no live session has walked one.
- **The baseline belongs to the corpus work.**
  A proof written into it would move the reference that work measures against.
- **A proof file is unexplained without the page.**
  A reader finds a run record beside the baseline and no statement of what it shows or what a rerun spends.

## Proposal

- **Harness and model are chosen at the start.**
  The run's session asks which harness and which model it uses, and passes both explicitly.
- **A shakedown, then the full run.**
  A shakedown over the feature workflows clears failures that are not the agent's own, then every form the chosen harness runs in the default matrix runs on the chosen model.
- **A file of its own.**
  The run is committed as `mvp-proof.json` beside `baseline.json`, which stays untouched, and records its measured cost.
- **The page states the proof.**
  The eval page names each feature workflow and its permutations, and states what `mvp-proof.json` proves and what it cost.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-03-594-i10-e05-w01-run-the-live-default/) | Run the live default-matrix proof | AC1, AC2, AC3 | [I09:E05](https://github.com/m2ux/prosiform/issues/523) | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e05/w02.md) | State the proof on the eval page | AC4, AC5 | W01 | | |

## Acceptance Criteria

- [ ] **AC1.** `evals/diagram-following/mvp-proof.json` records one live run over the feature workflows, naming the harness and model it ran on, across every form that harness runs in the default matrix, as the file's run record shows.
- [ ] **AC2.** Every feature scenario passes every run in at least one form cell, and no cell of the proof run passes no run, as `mvp-proof.json` shows.
- [ ] **AC3.** The proof run leaves `evals/diagram-following/baseline.json` unchanged, as its pull request's changed files show.
- [ ] **AC4.** The eval page names each feature workflow and the permutations its scenarios cover, as a read of the page against `workflows/` shows.
- [ ] **AC5.** The eval page states what `mvp-proof.json` proves and the run's measured cost, matching the cost the file records, as the page and the file show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the work items and the decision that moved the proof here.
- **R2.** [Grouping and composition record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-463-i09-grouping-and-composition) — the feature workflows, the pass bar and the proof's earlier decisions.
