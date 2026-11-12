# A Choice Line Declares an Alternative — November 2026

> I15 E00 W01 delivery · Created 2026-11-12

## Executive Summary

Deliver the second row of Declared Alternatives: a preset holding a non-empty one-line `choice` decodes as an alternative, and a malformed `choice`, a `choice` in `default` and a preset named `?` fail with `E_INVALID_CONVERSION_METADATA`. AC2 and AC3 are the unit's coverage.

The task targets `i15/e00/main`. The rules it implements are stated in the v1 design as W00 delivered it on `i15/e00/engineering`.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w01.md](../2026-11-12-preset-alternatives/e00/w01.md) | Component plan, scope and observing checks |

## Links

| Resource | Link |
| --- | --- |
| Epic | [Declared Alternatives](https://github.com/m2ux/prosiform/issues/708) |
| Design row | [W00 delivery](https://github.com/m2ux/prosiform/pull/710) |
