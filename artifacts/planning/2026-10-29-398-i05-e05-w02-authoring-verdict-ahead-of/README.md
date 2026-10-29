# I05:E05 W02 Authoring Verdict — October 2026

> Task delivery · Created 2026-10-29 · Revised 2026-10-29

## Executive Summary

The authoring check ran last in `make check`, so a rule break in a file any usage-example fixture reaches failed the corpus first, as a byte difference in a bundle. This record holds the placement of #398, the task that moves the verdict ahead of the corpus so a rule break is named by the rule it breaks.

The work is deferred debt of I05 delivered past the epic that produced it: W10 wired the check into `make check` and closed its own coverage, and the ordering it exposed is a separate change to the same target.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W02 work item](w02.md) | The new position for the authoring check in `make check`, the test that holds it, and the before-and-after evidence |
| [joins.md](joins.md) | The rows that could share a pull request and keep their own, and why |

## Decisions

- **The order alone.**  The change is the position of `authoring` among `check`'s prerequisites. No check's rules, no fixture and no example file change, so a passing run asserts exactly what it asserted before.
- **The order sits directly ahead of `corpus`.**  `authoring` needs no build, so `lock-check` is the only prerequisite that plausibly precedes it, and the position that keeps every other check running where it ran is the one `corpus` had.
- **The order is held by a test rather than by prose.**  `checks/tests/test_check_order.py` reads `check`'s prerequisite list from the `Makefile` and fails unless `authoring` is named ahead of `corpus`.

## Links

| Resource | Link |
| --- | --- |
| Epic | [Deferred Debt](https://github.com/m2ux/prosiform/issues/374) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Issue | [#398](https://github.com/m2ux/prosiform/issues/398) — the defect this task fixes |
| Pull request | [#399](https://github.com/m2ux/prosiform/pull/399) — the delivery of this task |
| Raised by | [W10 delivery](https://github.com/m2ux/prosiform/pull/397) |
| Review pull request | [#386](https://github.com/m2ux/prosiform/pull/386) — the epic review that reported it as outrun |

## Plan Changes

None applied and none held. The unit changed no task, epic, migration, priority or folded scope, so its change list is empty.
