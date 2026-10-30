# Entry References Left Unwarned — October 2026

> Delivery Record · Created 2026-10-26

## Executive Summary

A successful run emitted one `W_ENTRY_DESTINATION` warning per entry reference, naming the destination the bundle's entry line already links it to. An entry reference resolving to that destination is allowed, so `pf` says nothing about it. This row removes the warning outright: its emission, its code, the tests and fixture expectations of it, the design clause declaring it and every document describing it.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w12.md) | Scope, components and fixture outcomes |
| [Validation](validation.md) | Check results and the stale-wording search |

## Delivery Context

- Epic: I02 E00, issue #258; task W12.
- Task branch: `i02/e00/w12-entry-reference-unwarned`, cut from epic base `i02/e00/main` at `a334c55d`.
- Worktree: `.worktrees/i02-e00-w12`.
- Components: `src/prosiform`, `src/tests`, `checks`, `fixtures`, `README.md` design pin; `design.md` on this branch.
- Ruling: the user's — an entry reference resolving to the destination the entry line links it to is allowed, and `pf` says nothing about it.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Pull request | [#278](https://github.com/m2ux/prosiform/pull/278) |
