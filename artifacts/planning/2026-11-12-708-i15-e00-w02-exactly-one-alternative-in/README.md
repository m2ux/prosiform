# Exactly One Alternative in Force — November 2026

> I15 E00 W02 delivery · Created 2026-11-12 · Revised 2026-11-12

## Executive Summary

Deliver the exactly-one rule of Declared Alternatives: a document declaring alternatives compiles only with exactly one in force in each bundle, none or several fail with `E_ALTERNATIVE_UNRESOLVED` naming each alternative with its choice line, and an unpicked alternative raises no `W_PRESET_UNUSED`. AC4, AC5 and AC6 are the unit's coverage.

The task targets `i15/e00/main`, beside W03, which also extends `cli.py`; whichever merges second rebases on the first.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w02.md](w02.md) | Component plan, scope and observing checks |
| [test-results.md](test-results.md) | The test plan's results, with the revision tested |
| [changes.md](changes.md) | The plan changes this delivery applied and held |

## Links

| Resource | Link |
| --- | --- |
| Epic | [Declared Alternatives](https://github.com/m2ux/prosiform/issues/708) |
| Prerequisite | [W01 delivery](https://github.com/m2ux/prosiform/pull/712) |
| Pull request | [Exactly one alternative in force](https://github.com/m2ux/prosiform/pull/715) |
