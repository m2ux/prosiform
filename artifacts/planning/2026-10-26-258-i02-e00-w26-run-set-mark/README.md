# Run-Set Mark — October 2026

> Delivery Record · Created 2026-10-26

## Executive Summary

A link whose text opens with `⫽` (U+2AFD) followed by a space is a run-set link: the calls its target holds run concurrently. The target is compiled into the bundle like any link and the mark is published. pf warns with `W_RUN_SET_SHAPE` (exit 0, bundle published) where the target is no run-set. A run-set is one bulleted list below the heading whose every item links a Markdown document or section under the root. Any two of `¬`, `⇉`, `⫽` on one link are refused, and so is a `⫽` naming anything but a Markdown document or section under the root.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w26.md) | Scope, rulings, the shape rule, the warning, fixture outcomes |
| [Validation](validation.md) | Check results and the work-planner bundles |

## Delivery Context

- Epic: I02 E00, issue #258; task W26.
- Task branch: `i02/e00/w26-run-set-mark`, cut from epic base `i02/e00/main` at `2ff72d16`.
- Worktree: `.worktrees/i02-e00-w26`.
- Components: `src/prosiform/closure.py`, `src/prosiform/run_set.py` (new), `src/prosiform/cli.py`, `src/tests`, `fixtures`, `invocation.md`, `docs/glossary.md`, `README.md` (design pin); `design.md` on this branch.
- Rulings (the user's, relayed):
  - `⫽ ` opens the run-set operator and withholds nothing; its mark is published.
  - Shape is a warning, never a failure.
  - The W25 spacing rule applies.
  - One operator per link, across all three marks.
  - A `⫽` naming no Markdown document or section under the root is refused.
  - A `⇉` inside a run-set's target is a hop of the bundle compiling it.
  - No flag or compatibility path.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Pull request | [#310](https://github.com/m2ux/prosiform/pull/310) |
