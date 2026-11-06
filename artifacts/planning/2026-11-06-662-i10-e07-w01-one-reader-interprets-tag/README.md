# Shared Preset-List Reader — November 2026

> I10 E07 W01 delivery · Created 2026-11-06

## Executive Summary

One reader normalizes the comma-separated preset names supplied by a parsed Markdown link title or the CLI list value. Complete names match independently of whitespace, case, repetition and ordering.

The reader establishes the common interpretation consumed by the source and command layers. The command option is `--presets`; the runtime contract pin is adopted with the joined CLI and guide delivery.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w01.md](w01.md) | Component scope and observing checks |
| [todos.md](todos.md) | Delivery checklist |
| [changes.md](changes.md) | Applied coverage corrections and run boundary |
| [validation.md](validation.md) | Tested revision, observing checks and review findings |
| [make-check.txt](make-check.txt) | Full deterministic check output |
| [authorization.json](authorization.json) | Authorized unit and lane |
| [delivery-survey.txt](delivery-survey.txt) | Fresh task eligibility and blocked work |
| [dispatch-export.json](dispatch-export.json) | Machine-readable eligible unit |
| [dispatch-batch.json](dispatch-batch.json) | Selected delivery batch |
| [start-evidence.json](start-evidence.json) | Published-record and reservation checks |
| [reservation-readback.json](reservation-readback.json) | Saved task reservation |
| [board-reservation-readback.json](board-reservation-readback.json) | Saved In Progress board state |
| [target-protection.json](target-protection.json) | Target branch protection response |
| [target-rules.json](target-rules.json) | Target branch active rules |
| [board-completion-readback.json](board-completion-readback.json) | Saved Ready state for the next task |
| [completed-epic.json](completed-epic.json) | Saved W01 and AC2 completion |
| [design-integration.json](design-integration.json) | Draft design integration after conflict resolution |
| [development-links.json](development-links.json) | Complete pull-request Development relations |
| [epic-sync.txt](epic-sync.txt) | Completion findings and branch-configuration limitation |
| [execution.json](execution.json) | Completed worker, delivery revision and next unit |
| [head-checks.json](head-checks.json) | Successful hosted check at the task head |
| [head-status.json](head-status.json) | Commit status evidence at the task head |
| [main-integration.json](main-integration.json) | Draft main integration and its verified body |
| [merge-result.json](merge-result.json) | Confirmed task merge result |
| [merged-pr.json](merged-pr.json) | Merged task pull request and tested head |
| [merged-reader-check.txt](merged-reader-check.txt) | Reader instrument at the exact merge commit |
| [next-unit-dispatch.json](next-unit-dispatch.json) | Machine-readable next eligible task |
| [next-unit-survey.txt](next-unit-survey.txt) | W02 eligibility and I11 dependency gate |
| [reviews.json](reviews.json) | Task review snapshot before merge |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I10 E07](https://github.com/m2ux/prosiform/issues/662) |
| Board | [Project 18](https://github.com/users/m2ux/projects/18/views/4) |
| Contract | [Preset selection](https://github.com/m2ux/prosiform/blob/c67cf78f020923c4e5bd25d95497ced206be7161/artifacts/planning/2026-10-17-prosiform-v1/design.md#presets) |
| Task delivery | [Merged PR #665](https://github.com/m2ux/prosiform/pull/665) |
| Main integration | [Draft PR #666](https://github.com/m2ux/prosiform/pull/666) |
| Design integration | [Draft PR #664](https://github.com/m2ux/prosiform/pull/664) |
