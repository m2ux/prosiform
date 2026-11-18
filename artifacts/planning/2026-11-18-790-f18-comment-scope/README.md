# Comment Scope — November 2026

> Hot-fix · Created 2026-11-18

## Executive Summary

The docstring and comment convention in the repository's `AGENTS.md` states the code it covers: all code in the repository, the build under `src/prosiform/` and the code under `checks/`, `evals/` and `scripts/` alike.

The convention's wording, "a rule the build implements", came from `src/README.md`, where it meant the build alone. At the repository root it leaves the rest of the code's coverage open, so two authors can hold the same file to different rules.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [test-results.md](test-results.md) | The checks run at the delivering head and their results |
| [agent-review.json](agent-review.json) | The agent review record of the delivering pull request's reviewed head and base |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F18] Scope the comment convention to all code](https://github.com/m2ux/prosiform/issues/790) |
| Delivering pull request | [[F18] Scope the comment convention to all code](https://github.com/m2ux/prosiform/pull/789) |
| Precedent | [F17 Comment Convention](../2026-11-17-788-f17-comment-convention/README.md) |
