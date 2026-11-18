# Tagged Compositions — November 2026

> Hot-fix · Created 2026-11-18

## Executive Summary

A section composed twice, once with title tags that select a preset routing its links and once without, publishes both contributions under the tagged preset's routes. The `subst` pairs in force for a document are the union of the presets every reference reaching it selects, so a composed copy resolves under that union, whatever its own directive selects.

The fix has each contribution, and each dispatch brief, resolve under the presets its own directive or dispatch selects, layered over the document's `default`, while a document's own group keeps the union. A brief compiled as a composition reaches the defect easily, which is why the dispatch-brief review found it.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [f19.md](f19.md) | The work item: each composed copy resolving under its own presets |
| [test-results.md](test-results.md) | The checks run on the delivering branch and their results |
| [agent-review.json](agent-review.json) | The agent review records of the delivering pull request's reviewed heads and bases |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F19] Tagged Compositions](https://github.com/m2ux/prosiform/issues/793) |
| Delivering pull request | [[F19] Tagged Compositions](https://github.com/m2ux/prosiform/pull/794) |
| Precedent | [[F16] Dispatch Brief](https://github.com/m2ux/prosiform/issues/784) |
| Convention | [Docstrings and comments](https://github.com/m2ux/prosiform/blob/main/AGENTS.md#docstrings-and-comments) |
