# Rules and Conventions in Files of Their Own — October 2026

> Delivery Record · Created 2026-10-26

## Executive Summary

The example skill's Rules and Conventions sit in `SKILL.md`, which no mode bundle reaches, so a mode followed from its bundle never carries them. This row moves each into its own file beside `SKILL.md`, has every mode's preamble link both and its own Outcomes, and removes the guidance that described the previous structure.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w13.md) | Scope, component and validation obligations |
| [Validation](validation.md) | Check results, the guideline changes, mode-bundle sizes and fixture re-recording |

## Delivery Context

- Epic: I02 E00, issue #258; task W13; coverage AC2, AC12, AC13.
- Task branch: `i02/e00/w13-rules-and-conventions-files`, cut from epic base `i02/e00/main` at `a334c55d`.
- Worktree: `.worktrees/i02-e00-w13`.
- Components: `example/work-planner/{SKILL.md,rules.md,conventions.md,guidelines.md,modes/}`, `example/guidelines.md`, `fixtures/usage-example/`.
- Prerequisite: W11, delivered by [#276](https://github.com/m2ux/prosiform/pull/276).

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Pull request | pending |
