# F41: Corpus Entry Docstring

> Hot-fix record. Created 2026-11-26.

## Executive Summary

The corpus runner's entry docstring names the fixtures a work item unblocks.

The hot-fix first also declared the long-lived branches on `main` in `config/branches`. The user decided `config/` is a workspace file that does not belong in the project, so the branch was rewritten to the docstring alone. The work-planner's reading of `config/branches` at an epic base is a gap in the skill, not in this repository.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [agent-review.json](agent-review.json) | The agent reviews of #866: at b74bc52e2, one nonblocking finding fixed; at 42e742f2e, after the rewrite, none. |

## Links

| Resource | URL |
| --- | --- |
| Hot-fix issue | https://github.com/m2ux/prosiform/issues/865 |
| Delivering pull request | https://github.com/m2ux/prosiform/pull/866 |
