# Declared Metadata Contract — October 2026

> Delivery Record · Created 2026-10-23

## Executive Summary

I01 E06 W01 defines per-file conversion metadata in Prosiform's normative design. It covers AC1: the design defines the metadata and its failure behavior, observed through a contract review.

The user requested delivery of the next unit after prioritizing this epic. W01 is the only available task; the remaining rows depend on its delivery. This unit changes the engineering contract and its supporting evidence, not the compiler.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w01.md) | Scope, component and validation obligations |
| [Contract Review](validation.md) | Requirement trace, matrix coverage, diagnostics and exact candidate checks |
| [Contract Check](contract-check.py) | Reproducible local candidate checks using pinned baseline helpers |
| [Change List](changes.md) | Bounded refinements and remaining delivery prerequisite |

## Delivery Context

- Epic: I01 E06, issue #218; task W01; coverage AC1.
- Task branch: `i01/e06/w01-declared-metadata-contract`.
- Epic base: `i01/e06/engineering`, targeting `engineering`.
- Worktree: `.worktrees/i01-e06-w01`.
- Component: `artifacts/planning/2026-10-17-prosiform-v1/design.md`.
- Prerequisites: the initiative row has no prerequisite epic; W01 has no task dependency; no open questions or reservation were present at selection.
- Queue: E06 is the sole next epic. Findings Ledger and Section Composition move to Backlog under the confirmed priority-6 choice.
- Branch evidence: the contract's owning branch and work item explicitly identify engineering. The workspace's `config/branches` lists only main and workspace, so the delivery calculator resolves the unit but omits its engineering base. The supplied base follows the actual component owner; no unrelated branch registry edit is part of this task.
- Repository auto-close setting: the user confirms automatic closure of linked issues on pull-request merge is disabled.

## Progress

- [x] Confirm queue, task scope and prerequisites.
- [x] Reserve and dispatch the task.
- [x] Implement and review the contract.
- [x] Validate and publish the delivery PR.
- [x] Merge W01 and record its verified AC1 delivery.
- [x] Link draft epic review #220 to epic #218 through GitHub's Development relation.

## Links

| Resource | Link |
| --- | --- |
| Epic | [#218](https://github.com/m2ux/prosiform/issues/218) |
| Task Pull Request | [#219](https://github.com/m2ux/prosiform/pull/219) |
| Draft Epic Review | [#220](https://github.com/m2ux/prosiform/pull/220) |
| Board | [Bundling](https://github.com/users/m2ux/projects/18) |
