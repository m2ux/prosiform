# I00:E00:W03 Test Runner and Static Checks - October 2026

> Task Plan - Created 2026-10-18

## Executive Summary

This record holds the local plan for the third task of [I00:E00] Project Foundation. The task makes tests, lint, format and type checks each run from one documented command with a declared configuration, and brings the layout, link and vocabulary checks W01 wrote into that same scheme. It adds a lock check, so a dependency list edited without relocking fails rather than passing against a lockfile that no longer describes it, and it moves the vocabulary check's term inventory onto the design and the acceptance criteria so the shipped glossary is measured against the contract's own usage.

It matters because every later epic carries tests, and nothing yet states how they are discovered, how they are run, or what reports a failure. W04 runs these same commands in continuous integration, so a check that exists only as a local habit cannot be enforced there. The task covers AC3 of the epic.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w03.md](w03.md) | The task's plan: the named commands and their runner, the tool configuration and where it lives, the inventory the vocabulary check reads, and the lock check |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#26 \[I00:E00\] Project Foundation](https://github.com/m2ux/prosiform/issues/26) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W01 record | [Repository layout, README and glossary](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-18-26-i00-e00-w01-repository-layout-readme-and) |
| W02 record | [Python environment and pinned dependencies](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-18-26-i00-e00-w02-python-environment-and-pinned) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
