# Ambiguous Deferred Targets — November 2026

> Hot-fix · Created 2026-11-18

## Executive Summary

A deferred composition directive inside composed content that names a fragment matching two headings of its target ends the run with `E_UNEXPECTED_INTERNAL_ERROR`, where an ordinary reference to such a fragment fails with `E_AMBIGUOUS_SOURCE_HEADING`.

The fix reports the ambiguous fragment as the input failure it is, naming the directive, its source location and the headings it matches, so an author can correct the source instead of meeting an internal error.

## Artifacts

| Artifact | What it holds |
| --- | --- |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F20] Ambiguous Deferred Targets](https://github.com/m2ux/prosiform/issues/795) |
| Found by | [[F19] Tagged Compositions](https://github.com/m2ux/prosiform/pull/794) |
| Convention | [Docstrings and comments](https://github.com/m2ux/prosiform/blob/main/AGENTS.md#docstrings-and-comments) |
