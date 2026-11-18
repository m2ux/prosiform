# Input Failures: Deferred Fragments and the Pick Remedy — November 2026

> Hot-fix · Created 2026-11-18

## Executive Summary

A deferred composition directive whose fragment matches two headings of its target, or names a heading a container carries, ends the run with `E_UNEXPECTED_INTERNAL_ERROR`, where an ordinary reference to such a fragment fails with `E_AMBIGUOUS_SOURCE_HEADING` or `E_NESTED_SECTION_TARGET`. Separately, the `E_ALTERNATIVE_UNRESOLVED` remedy tells the author to rerun with `--pick`, which the run refuses beside an entry whose title carries no `?`.

The fix reports the deferred fragment as the input failure it is, naming the reference, the document it resolved to and the chain, and gives the unresolved-alternative failure a remedy the run accepts: `--pick` where the entry carries `?`, and otherwise the alternative named in the links reaching the document.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [f20.md](f20.md) | The work item: the deferred-target refusal and the pick remedy |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F20] Input Failures: Deferred Fragments and the Pick Remedy](https://github.com/m2ux/prosiform/issues/795) |
| Found by | [[F19] Tagged Compositions](https://github.com/m2ux/prosiform/pull/794) |
| Convention | [Docstrings and comments](https://github.com/m2ux/prosiform/blob/main/AGENTS.md#docstrings-and-comments) |
