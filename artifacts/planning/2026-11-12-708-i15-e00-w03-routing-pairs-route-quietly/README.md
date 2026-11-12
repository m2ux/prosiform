# Routing Pairs Route Quietly — November 2026

> I15 E00 W03 delivery · Created 2026-11-12

## Executive Summary

Deliver the routing rule of Declared Alternatives: an alternative's `subst` pairs route its document's links without the warnings a stand-in raises, so a used pair raises no `W_SUBST_USED` and `W_SUBST_UNUSED` fires only for a key no link of the document names. AC7 and AC8 are the unit's coverage.

The task targets `i15/e00/main`, beside W02, which also extends `cli.py`; whichever merges second rebases on the first.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w03.md](w03.md) | Component plan, scope and observing checks |
| [test-results.md](test-results.md) | The test plan's results, with the revision tested |

## Links

| Resource | Link |
| --- | --- |
| Epic | [Declared Alternatives](https://github.com/m2ux/prosiform/issues/708) |
| Prerequisite | [W01 delivery](https://github.com/m2ux/prosiform/pull/712) |
