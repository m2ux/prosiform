# I10:E02 W01 Every Project-Scope Settings File Refused — November 2026

> Task delivery · Created 2026-11-03

## Executive Summary

Refuses a run whose session workspace or an ancestor holds a .claude settings file declaring a hook, naming the file and the remedy.

This record holds its delivery of `AC1,AC2,AC3`: the work item, the validation evidence for every check the work item names, and the plan changes the session applied and held.

## Artifacts

| Artifact | What it holds |
| --- | --- |

## Test Evidence

Each check is a stub-agent test in `evals/diagram-following/test_run.py`, run by `make check` in the row worktree at commit `b0bc6bca`. No live session or paid run is made.

| Check | Procedure | Coverage |
| --- | --- | --- |
| Form tree settings | A copied form tree plants a `SessionStart` hook in its `.claude/settings.json`, then in `.claude/settings.local.json`. Each run is refused before the first session, naming the file and no results folder is written. | AC1 |
| Ancestor settings declaring a hook | A `.claude` directory above the eval workspaces plants a `SessionStart` hook in each of its two settings files. Each run is refused, naming the file and `--eval-root`. | AC3 |
| Ancestor settings declaring no hook | A `.claude` directory above the eval workspaces holds `settings.json` with preferences only. The session starts. | AC2 |

`make check` exits 0 with the `PROSIFORM_BUILD` setting from the brief.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I10:E02 Session Isolation](https://github.com/m2ux/prosiform/issues/456) |
| Initiative | [I10 Evaluation and Checks](https://github.com/m2ux/prosiform/issues/464) |
| Epic record | [Evaluation and Checks](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) |
