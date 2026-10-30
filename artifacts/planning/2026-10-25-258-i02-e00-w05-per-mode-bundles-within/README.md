# Per-Mode Bundles Within the Budget — October 2026

> Delivery Record · Created 2026-10-25

## Executive Summary

W04's one-root fix brought the example's own `guidelines.md` into scope, so seven of the ten mode bundles now carry guidance text. Six carry its H1 and the `### Modes` section, 4,323 bytes each; `revise-mode` carries its text whole, 23,797 bytes. The largest bundle sits at 94% of the 262,144-byte budget. This row defers each in-root guidelines link, so a mode's bundle carries its procedure and the artifacts it runs without the guidance document riding along.

Both criteria land together here. AC7's budget condition is already met on the base — all ten modes compile inside 262,144 — and this row keeps it met while AC8's deferral removes the guidance text from all seven affected bundles. The ten bundles fall from 1,284,909 bytes to 1,215,638.

One finding is recorded rather than fixed: `revise-mode` falls to 3,482 bytes once its guideline links are deferred, because all four in-root links it writes point at guidance and its only other links are same-file anchors. That is the marker working as designed and a design signal about the mode's own references.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w05.md) | Scope, component and validation obligations |
| [Validation](validation.md) | The ten bundles measured, and the checks run |

## Delivery Context

- Epic: I02 E00, issue #258; task W05; coverage AC7, AC8.
- Task branch: `i02/e00/w05-per-mode-bundles-within`, cut from epic base `i02/e00/main` at `820b5cb6`.
- Worktree: `.worktrees/i02-e00-w05`.
- Component: `example/work-planner/`.
- Prerequisite: W04, delivered by [#267](https://github.com/m2ux/prosiform/pull/267).
- Repository auto-close setting: confirmed disabled for `m2ux/prosiform`.

## Governing rule

Anything outside a file's declared root is never bundled. It stays a link at every level. The example's `guidelines.md` is inside the root, so its links are followed today; the deferral marker is what keeps its content out while keeping its destination valid.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Preceding row | [W04 pull request #267](https://github.com/m2ux/prosiform/pull/267) |
| Board | [Board 18](https://github.com/users/m2ux/projects/18) |
