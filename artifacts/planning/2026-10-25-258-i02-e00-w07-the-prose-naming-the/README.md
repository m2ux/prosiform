# The Prose Naming the Example It Describes — October 2026

> Delivery Record · Created 2026-10-25

## Executive Summary

The example grew from four documents to forty-nine and the pages that document it did not follow. `example/README.md` names `work-tracker` seven times and quotes a Prerequisites section neither tree carries; `invocation.md` runs four example commands from the replaced directory. This row rewrites both against `example/work-planner` and holds every quoted block to what the tree actually holds.

The row is last in the epic and the one a reader meets first: it is the page the demonstration's command is published beside, so a stale excerpt here makes the demonstration unreproducible.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w07.md) | Scope, component and validation obligations |
| [Validation](validation.md) | The checks and the excerpts re-read |

## Delivery Context

- Epic: I02 E00, issue #258; task W07; coverage AC10.
- Task branch: `i02/e00/w07-the-prose-naming`, cut from epic base `i02/e00/main` at `714c95c1`.
- Worktree: `.worktrees/i02-e00-w07`.
- Component: `example/README.md`.
- Prerequisite: W06, delivered by [#270](https://github.com/m2ux/prosiform/pull/270).
- Repository auto-close setting: confirmed disabled for `m2ux/prosiform`.

## State on the base

| File | `work-tracker` | `work-planner` |
| --- | --- | --- |
| `example/README.md` | 7 | 0 |
| `invocation.md` | 1 | 0 |
| `fixtures/README.md` | 0 | 1 |

The quoted Prerequisites block at `example/README.md` is stale: neither `example/work-tracker/modes/plan-mode.md` nor `example/work-planner/modes/plan-mode.md` carries a `## Prerequisites` section.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Preceding row | [W06 pull request #270](https://github.com/m2ux/prosiform/pull/270) |
| Board | [Board 18](https://github.com/users/m2ux/projects/18) |
