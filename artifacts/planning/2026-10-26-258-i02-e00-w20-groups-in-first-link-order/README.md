# Groups in First-Link Order — October 2026

> Delivery Record · Created 2026-10-26

## Executive Summary

pf ordered groups, and members inside a merged group, by working-directory path, so a work-planner mode bundle put Artifacts, Conventions, other modes, Protocols and References ahead of the binding Rules. pf now arranges sources in placement order: each document is placed at the first reference naming it, reading the entry references in command-line order and then each placed document's selected content in turn. Groups and members follow it, so authors set the order by the order they write links.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w20.md) | Scope, the ordering rule, rules kept and changed, fixture outcomes |
| [Validation](validation.md) | Check results, the re-record diff check and the example outlines |

## Delivery Context

- Epic: I02 E00, issue #258; task W20.
- Task branch: `i02/e00/w20-groups-in-first-link-order`, cut from epic base `i02/e00/main` at `7c47e0a0`; `f171675d` (W19, #284) merged in before re-recording.
- Worktree: `.worktrees/i02-e00-w20`.
- Components: `src/prosiform` (`cli.py`, `grouping.py`, `bundle.py`), `src/tests`, `fixtures`, `invocation.md`, `docs/glossary.md`, `docs/images/compilation.*`, `README.md` (diagram alt text, design pin), `example/README.md`; `design.md` on this branch.
- Rulings: the user's — groups and members ordered by first link, reading the entry first; authors set order by listing links in the preamble; deterministic; parent-first arrangement of merged sections kept. No compatibility path.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Pull request | [#285](https://github.com/m2ux/prosiform/pull/285) |
