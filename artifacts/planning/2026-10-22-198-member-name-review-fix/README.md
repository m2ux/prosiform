# Distinct Displayed Member Names — October 2026

> Review correction · Created 2026-10-22

## Executive Summary

The correction to PR #198 qualifies member names after the transformations that produce their displayed text. A pair of paths whose stems differ before word removal therefore retains enough path context to identify each member.

The validation exercises group-word removal, title casing and separator normalization, plus members in one directory whose group word must remain. A corpus fixture checks distinct destinations and the same names in overview subsections and pooled variants.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Validation](validation.md) | Reproduction and verification evidence |

## Links

| Resource | Link |
| --- | --- |
| Epic review | https://github.com/m2ux/prosiform/pull/198 |
