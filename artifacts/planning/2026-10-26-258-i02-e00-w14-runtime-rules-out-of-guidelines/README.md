# Runtime Rules Out of Guidelines — October 2026

> Delivery Record · Created 2026-10-26

## Executive Summary

The example skill's guidelines are for revising the skill, yet every mode that puts a question to the user deferred to the Interview rule in `guidelines.md#modes`. This row moves that rule into the Decisions rule of `rules.md`, which every mode bundles, repoints each runtime link at `rules.md`, and restates the guidelines that told authors to put rules binding every mode into guidelines.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w14.md) | Scope, component and validation obligations |
| [Validation](validation.md) | Check results, the migrated rule, repointed links, mode-bundle sizes and fixture re-recording |

## Delivery Context

- Epic: I02 E00, issue #258; task W14; coverage AC12, AC13.
- Task branch: `i02/e00/w14-runtime-rules-out-of-guidelines`, cut from epic base `i02/e00/main` at `ad8f1a2a`.
- Worktree: `.worktrees/i02-e00-w14`.
- Components: `example/work-planner/{rules.md,guidelines.md,modes/,protocols/epic-integration.md}`, `example/README.md`, `fixtures/usage-example/`.
- Prerequisite: W13, delivered by [#277](https://github.com/m2ux/prosiform/pull/277).

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Pull request | [#279](https://github.com/m2ux/prosiform/pull/279) |
