# I00:E11:W04 A Fixture Declaring an Allowed Source Root the Run Cannot Find - October 2026

> Task Plan - Created 2026-10-20 - Revised 2026-10-20

## Executive Summary

This record holds the local plan for the row that states, as a corpus fixture, what a run does when its allowed source root names no directory. A manifest's declared diagnostics decide which rule its root is held to: one expecting `E_ROOT_NOT_FOUND` names a path the fixture does not hold, which is the shape of fixture the validator refused before this row.

It matters because the outcome is reachable from any caller's command line and is held by one build's own tests alone. A fixture that states it holds every build to the same answer, and tells a build that reports it from one that does not.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w04.md](w04.md) | The task's plan: how the fixture declares a root the run cannot find, and what its run expects |
| [plan-changes.md](plan-changes.md) | The plan changes this session applied and held, and the debt classification behind them |
| [validation.md](validation.md) | The rule under test, the fixture's run against a build that reports the outcome and one that does not, the checks the delivery was held to, and the review |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#39 \[I00:E11\] Deferred Debt](https://github.com/m2ux/prosiform/issues/39) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Origin | [E02:W07 validation record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w07-an-error-code-for) |
| Pull request | [#124 \[I00:E11\] A Fixture for an Allowed Source Root the Run Cannot Find](https://github.com/m2ux/prosiform/pull/124) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
