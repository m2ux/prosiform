# I00:E11:W13 A Parser Resource Limit That Suppresses a Reference Lookup - October 2026

> Task Plan - Created 2026-10-20

## Executive Summary

This record holds the local plan for the row that makes the build raise the code the contract declares when an internal parser resource limit prevents a reference lookup. The run fails with that code, naming the first affected source span where the parser reports one, and a budget consumed on its last valid reference with no later lookup suppressed stays a successful run.

It matters because a reference the parser silently declined to resolve is a dependency the bundle omits without saying so, and nothing in the repository would notice. A declared code that no module defines and no fixture expects is a claim rather than a contract.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w13.md](w13.md) | The task's plan: where suppression is observed, what the diagnostic carries and the two fixtures that separate exhaustion from omission |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#39 \[I00:E11\] Deferred Debt](https://github.com/m2ux/prosiform/issues/39) |
| Task issue | [#108 A Parser Resource Limit Suppressing a Reference Lookup Is Detected by Nothing](https://github.com/m2ux/prosiform/issues/108) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
