# A Root Bounds Inclusion Only — October 2026

> Delivery Record · Created 2026-10-26

## Executive Summary

`prosiform.root` (or the working directory) also named things: an ungrouped document was headed by its title-cased root-relative path, sources and members were ordered and named from it, and the default output name was the entry's path from its effective root. A root now bounds which files links may include and which files pf may open, and nothing else. A file group is headed by its document's title, or by its working-directory path where it has none, and output names derive from the working-directory path.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w16.md) | Scope, components and fixture outcomes |
| [Validation](validation.md) | Check results, the re-record diff check and the stale-wording search |

## Delivery Context

- Epic: I02 E00, issue #258; task W16.
- Task branch: `i02/e00/w16-root-bounds-only`, cut from epic base `i02/e00/main` at `f5038166`; `0d3e0cff` (W17) and `8040ab68` (#282) merged in before re-recording.
- Worktree: `.worktrees/i02-e00-w16`.
- Components: `src/prosiform`, `src/tests`, `checks/smoke.py`, `fixtures`, `invocation.md`, `docs/glossary.md`, `README.md` (my-skill command, design pin), `fixtures/README.md`; `design.md` on this branch.
- Rulings: the user's — (1) an ungrouped document is headed by its own H1 title, or by its title-cased working-directory path without one, coinciding headings disambiguated as repeated headings are; (2) the default output name is the entry's working-directory path. No compatibility path.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Pull request | [#283](https://github.com/m2ux/prosiform/pull/283) |
