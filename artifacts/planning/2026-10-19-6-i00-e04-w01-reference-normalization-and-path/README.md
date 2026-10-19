# I00:E04:W01 Reference Normalization and Path Identity - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the first row of [I00:E04] Dependency Closure. A reference is classified as a Markdown document by its suffix, `.md` and `.markdown` recognized case-insensitively while filesystem spelling and case semantics are preserved. URI components split before percent-decoding so an encoded delimiter stays a filename character, escapes validate strictly and decode exactly once as UTF-8, and relative segments normalize against the proper base. A query on a local Markdown reference fails, as do unsupported schemes, NULs, control characters, decoded path separators, backslash separators, root-relative URL paths, absolute reference paths, protocol-relative URLs and drive paths.

It matters because a link string is not a path, and a check performed on the string alone can confine a reference that escapes the root. Every later row of the epic resolves against the identity this row establishes, and the row that follows it enforces the root by access rather than by inspection. The row covers AC6, AC8 and AC14, and extends a module of its own that no other row in this delivery wave touches.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w01.md](w01.md) | The task's plan: the component split, the validation order and the error code for each rejected form |
| [validation.md](validation.md) | The validation record: the command behind each Test Plan row and the output it returned |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#6 \[I00:E04\] Dependency Closure](https://github.com/m2ux/prosiform/issues/6) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
