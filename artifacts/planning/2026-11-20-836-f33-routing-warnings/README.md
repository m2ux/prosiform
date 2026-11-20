# Routing Warnings — November 2026

> Hot-fix · Created 2026-11-20

## Executive Summary

Every `subst` pair but an alternative's warned `W_SUBST_USED` as material under test, so a stage routing on two axes warned on every live run. A stub's pair alone now stands in and warns; every other pair routes where its author declared and raises nothing where a link used it.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [f33.md](f33.md) | The work item: which pairs route and which stand in |
| [test-results.md](test-results.md) | The checks run on the delivering branch and their results |
| [agent-review.json](agent-review.json) | The agent review records of the delivering pull request |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F33] Routing Warnings](https://github.com/m2ux/prosiform/issues/836) |
| Delivering pull request | [[F33] Routing Warnings](https://github.com/m2ux/prosiform/pull/837) |
