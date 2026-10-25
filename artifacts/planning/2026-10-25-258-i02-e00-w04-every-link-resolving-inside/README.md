# Every Link Resolving Inside the Example — October 2026

> Delivery Record · Created 2026-10-25

## Executive Summary

The merged base compiles every mode at the default budget except `deliver-mode`, but the bundles it produces are smaller than the documents they name. A mode's Procedure links `../artifacts/board.md#select-project-board` and the artifact's text never arrives: each file's declared root points at its own folder, so the example directory is never one root and the link resolves outside it. This row gives the tree one effective root and writes every in-root link from that directory.

The measurement is unambiguous. `advance-mode`'s bundle contains 9 of the example's 49 documents; under one root it contains 27. Across the ten modes, 285 authored links name an in-root document whose content the bundle does not carry. The corrected configuration leaves none, compiles all ten modes at `-E 8`, and keeps every bundle inside the 262,144-byte budget.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w04.md) | Scope, component and validation obligations |
| [Validation](validation.md) | The ten bundles measured, and the checks run |

## Delivery Context

- Epic: I02 E00, issue #258; task W04; coverage AC6.
- Task branch: `i02/e00/w04-every-link-resolving-inside`, cut from epic base `i02/e00/main` at `1e2dc068`.
- Worktree: `.worktrees/i02-e00-w04`.
- Component: `example/work-planner/`.
- Prerequisite: W03, delivered by [#266](https://github.com/m2ux/prosiform/pull/266).
- Repository auto-close setting: confirmed disabled for `m2ux/prosiform`.

## Governing rule

Anything outside a file's declared root is never bundled. It stays a link at every level. So AC6's obligation covers links whose target sits inside the example; links naming `example/guidelines.md` or the shared `skills/guidelines.md` remain links and are W05's AC8 to defer.

## Known constraint carried in

The root declaration is resolved from the declaring file's folder, so one directory needs two spellings: `.` at the top level and `..` one level down. That limitation is #263 W03's subject and this row works within it rather than fixing it.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Preceding row | [W03 pull request #266](https://github.com/m2ux/prosiform/pull/266) |
| Board | [Board 18](https://github.com/users/m2ux/projects/18) |
