# Coincident Heading Warning — October 2026

> Delivery Record · Created 2026-10-26

## Executive Summary

Two file headings that coincided passed silently, and two merged-group members whose names coincided refused the bundle with `E_AMBIGUOUS_FILE_GROUP`. pf now publishes the bundle in both cases, exits 0 and reports `W_COINCIDENT_HEADING` once per coinciding set, naming the shared text and every source location, so the user can scrutinise the bundle. `E_AMBIGUOUS_FILE_GROUP` is removed.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w21.md) | Scope, the warning, rules kept and changed, fixture outcomes |
| [Validation](validation.md) | Check results, the corpus re-run and the work-planner bundles |

## Delivery Context

- Epic: I02 E00, issue #258; task W21.
- Task branch: `i02/e00/w21-coincident-heading-warning`, cut from epic base `i02/e00/main` at `b46b1bf4`.
- Worktree: `.worktrees/i02-e00-w21`.
- Components: `src/prosiform` (`cli.py`, `bundle.py`), `src/tests`, `fixtures`, `invocation.md`, `README.md` (design pin); `design.md` on this branch.
- Rulings: the user's — coinciding generated headings (file headings; member headings in a merged group) publish and warn with `W_COINCIDENT_HEADING` (text and `-d json`), `location` plus `related`, one diagnostic per set, exit 0; authored repeats do not warn; an unused error code is removed everywhere. No flag or compatibility path.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Pull request | [#286](https://github.com/m2ux/prosiform/pull/286) |
