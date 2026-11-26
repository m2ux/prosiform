# F41: Branch Declaration

> Hot-fix record. Created 2026-11-26.

## Executive Summary

`main` declares the long-lived branches in `config/branches`, so the work-planner can read them at an epic base cut from `main`, and the corpus runner's entry docstring names what it reports.

The epic syncs of I19 E01 reported every branch-based check as not run for want of that declaration.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [agent-review.json](agent-review.json) | The agent review of #866 at b74bc52e2: one nonblocking finding, fixed. |

## Links

| Resource | URL |
| --- | --- |
| Hot-fix issue | https://github.com/m2ux/prosiform/issues/865 |
| Delivering pull request | https://github.com/m2ux/prosiform/pull/866 |
