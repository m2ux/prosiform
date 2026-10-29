# I05:E05 W02 Authoring Verdict — October 2026

> Task delivery · Created 2026-10-29

## Executive Summary

The authoring check runs last in `make check`, so a rule break in a file any usage-example fixture reaches fails the corpus first, as a byte difference in a bundle. This record holds the placement of #398, the task that moves the verdict ahead of the corpus so a rule break is named by the rule it breaks.

The work is deferred debt of I05 delivered past the epic that produced it: W10 wired the check into `make check` and closed its own coverage, and the ordering it exposed is a separate change to the same target.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [joins.md](joins.md) | The rows that could share a pull request and keep their own, and why |

## Links

| Resource | Link |
| --- | --- |
| Epic | [Deferred Debt](https://github.com/m2ux/prosiform/issues/374) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Issue | [#398](https://github.com/m2ux/prosiform/issues/398) — the defect this task fixes |
| Raised by | [W10 delivery](https://github.com/m2ux/prosiform/pull/397) |
