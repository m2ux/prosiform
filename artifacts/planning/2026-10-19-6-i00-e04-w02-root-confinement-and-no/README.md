# I00:E04:W02 Root Confinement and No-Symlink Source Access - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the second row of [I00:E04] Dependency Closure. Every source read is confined by rooted, no-follow access rather than by inspecting the path string, and a reference whose normalized path leaves the allowed root, or that reaches a source through a symbolic link below it, fails with its declared error code.

It matters because a check performed on a string can confine a reference that escapes the root: a symbolic link below the root resolves outside it while every segment of the written path stays inside. The row covers AC5 and extends the closure module [W01](https://github.com/m2ux/prosiform/pull/62) introduced, which no concurrent unit touches. The codes it needs, `E_SOURCE_OUTSIDE_ROOT` and `E_SOURCE_SYMLINK`, are already in the catalogue.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w02.md](w02.md) | The task's plan: the access mechanism, the canonicalization and the two error codes |
| [validation.md](validation.md) | The validation record: the behaviour measured before the design was built to it, the command behind each Test Plan row, and the output it returned |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#6 \[I00:E04\] Dependency Closure](https://github.com/m2ux/prosiform/issues/6) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W01 record | [Reference normalization and path identity](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-6-i00-e04-w01-reference-normalization-and-path) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
