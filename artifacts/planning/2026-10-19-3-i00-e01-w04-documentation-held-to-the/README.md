# I00:E01:W04 Documentation Held to the Project It Describes - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for a task of [I00:E01] Corpus Harness. The task adds a check comparing the build README's dependency and command tables with what the project actually declares, failing in either direction: a declared item the README omits, and a README row the project does not declare. It also widens the link check from the root README alone to every README the repository owns, discovering them rather than naming them, so a tree added later is covered without the check being edited.

It matters because a reader installs from a README and invokes what it names, so a stale table or a dead link is a wrong instruction rather than an untidy one. Both tables went stale on the first change that touched them, and a reading by hand is what caught it; three of the four READMEs gained links that nothing checks. The task covers AC6 and AC8 of the epic.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w04.md](w04.md) | The task's plan: how a table is located and a row mapped to a declared item, which declaration sets the table check compares, why no Makefile target is excluded from documentation, and how both checks discover the READMEs they read |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#3 \[I00:E01\] Corpus Harness](https://github.com/m2ux/prosiform/issues/3) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W01 record | [Fixture layout and manifest schema](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-3-i00-e01-w01-fixture-layout-and-manifest) |
| W02 record | [Corpus runner and result comparison](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-3-i00-e01-w02-corpus-runner-and-result) |
| Epic review | [#41](https://github.com/m2ux/prosiform/pull/41) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
