# I05:E05 W02 Authoring Verdict — October 2026

> Task delivery · Created 2026-10-29

## Executive Summary

The authoring check runs last in `make check`, so a rule break in a file any usage-example fixture reaches fails the corpus first, as a byte difference in a bundle. This record holds the placement of #398, the task that moves the verdict ahead of the corpus so a rule break is named by the rule it breaks.

The work is deferred debt of I05 delivered past the epic that produced it: W10 wired the check into `make check` and closed its own coverage, and the ordering it exposed is a separate change to the same target.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W02 work item](w02.md) | The new position for the authoring check in `make check`, and the test that holds it |
| [joins.md](joins.md) | The rows that could share a pull request and keep their own, and why |

## Decisions

- **The order alone.**  The change is the position of `authoring` among `check`'s prerequisites. No check's rules, no fixture and no example file change, so a passing run asserts exactly what it asserted before.

## Links

| Resource | Link |
| --- | --- |
| Epic | [Deferred Debt](https://github.com/m2ux/prosiform/issues/374) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Issue | [#398](https://github.com/m2ux/prosiform/issues/398) — the defect this task fixes |
| Raised by | [W10 delivery](https://github.com/m2ux/prosiform/pull/397) |
| Review pull request | [#386](https://github.com/m2ux/prosiform/pull/386) — the epic review that reported it as outrun |
