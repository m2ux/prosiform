# An Agent-Pick Eval Workflow — November 2026

> I15 E01 W05 delivery · Created 2026-11-12

## Executive Summary

Deliver an agent-pick workflow for the diagram-following eval's `compiled` form: a headless session reaches a kind router through a `?` link, compiles it with `pf`, reads the alternatives and continues with the one its input calls for. The scenarios pass only a session that enters the picked kind's states alone, after running `pf` with `?` replaced by that alternative and reading no source. AC7 is the unit's coverage.

The task targets `i15/e01/main`, after the guide entry and router fixtures (W03). The live run that measures it is W06.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w05.md](w05.md) | Component plan, scope and observing checks |
| [validation.md](validation.md) | Each Test Plan check's procedure, tested revision and observation |

## Links

| Resource | Link |
| --- | --- |
| Epic | [Agent Pick](https://github.com/m2ux/prosiform/issues/709) |
| Prerequisites | [W03 delivery](https://github.com/m2ux/prosiform/pull/723) |
