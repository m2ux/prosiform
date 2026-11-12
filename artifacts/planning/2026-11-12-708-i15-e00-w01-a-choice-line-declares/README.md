# A Choice Line Declares an Alternative — November 2026

> I15 E00 W01 delivery · Created 2026-11-12 · Revised 2026-11-12

## Executive Summary

Deliver the second row of Declared Alternatives: a preset holding a non-empty one-line `choice` decodes as an alternative, and a malformed `choice`, a `choice` in `default` and a preset named `?` fail with `E_INVALID_CONVERSION_METADATA`. AC2 and AC3 are the unit's coverage.

The task targets `i15/e00/main`. The rules it implements are stated in the v1 design as W00 delivered it on `i15/e00/engineering`.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w01.md](w01.md) | Component plan, scope and observing checks |
| [test-results.md](test-results.md) | The test plan's results, with the revision tested |
| [changes.md](changes.md) | The plan changes the delivery session applied and held |

## Links

| Resource | Link |
| --- | --- |
| Epic | [Declared Alternatives](https://github.com/m2ux/prosiform/issues/708) |
| Design row | [W00 delivery](https://github.com/m2ux/prosiform/pull/710) |
| Pull request | [A choice line declares an alternative](https://github.com/m2ux/prosiform/pull/712) |
| Epic review | [Declared Alternatives](https://github.com/m2ux/prosiform/pull/713) |
