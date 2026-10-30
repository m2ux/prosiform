# The Prose Naming the Example It Describes — October 2026

> Delivery Record · Created 2026-10-25

## Executive Summary

The example grew from four documents to forty-nine and the pages that document it did not follow. `example/README.md` named `work-tracker` seven times and called its blocks exact excerpts while quoting a Prerequisites section neither tree carries; `invocation.md` ran four example commands from the replaced directory. This row rewrites both against `example/work-planner`, and holds every quoted block to the bytes the file it names now holds.

The row is last in the epic and the one a reader meets first: it is the page the demonstration's command is published beside, so a stale excerpt here makes the demonstration unreproducible.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w07.md) | Scope, component and validation obligations |
| [Validation](validation.md) | The checks, the command runs and each excerpt against its source |

## Delivery Context

- Epic: I02 E00, issue #258; task W07; coverage AC10.
- Task branch: `i02/e00/w07-the-prose-naming`, cut from epic base `i02/e00/main` at `714c95c1`.
- Worktree: `.worktrees/i02-e00-w07`.
- Component: `example/README.md`.
- Pull request: [#271](https://github.com/m2ux/prosiform/pull/271), merged into `i02/e00/main` at `119e37a6`.
- Prerequisite: W06, delivered by [#270](https://github.com/m2ux/prosiform/pull/270).
- Repository auto-close setting: confirmed disabled for `m2ux/prosiform`.
- The epic base is ready to integrate. Its own merge into `main` and the epic's closure are the next decision, not this row's.

## Plan changes

| Kind | Subject | Applied |
| --- | --- | --- |
| Folded work | [W07 work item](w07.md) — the Implementation Findings the build's measurements added | The stale-excerpt list widened from one block to eight; `make links` recorded in place of `make links --online` |
| Folded work | Epic #258 body — W07's row and AC10 | The row links [#271](https://github.com/m2ux/prosiform/pull/271) and is ticked; AC10 is ticked on the `make links` result |
| Task creation | [#263](https://github.com/m2ux/prosiform/issues/263) W06 and W07, with AC6 and AC7 | Raised |

No initiative was created and no issue renumbered. No held change was taken.

## State on the base

| File | `work-tracker` | `work-planner` |
| --- | --- | --- |
| `example/README.md` | 7 | 0 |
| `invocation.md` | 1 | 0 |
| `fixtures/README.md` | 0 | 1 |

The quoted Prerequisites block at `example/README.md` was stale: neither `example/work-tracker/modes/plan-mode.md` nor `example/work-planner/modes/plan-mode.md` carries a `## Prerequisites` section. Both carry `# Plan Mode`, `## Procedure` and `## Outcomes`. The publish step inside `## Procedure` replaced the excerpt, because it demonstrates the same point: two in-root links and one deferred link.

Eight blocks were stale, not one. Every one is re-read and replaced; [Validation](validation.md#the-excerpts-replaced) lists each against its source.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Preceding row | [W06 pull request #270](https://github.com/m2ux/prosiform/pull/270) |
| Board | [Board 18](https://github.com/users/m2ux/projects/18) |
