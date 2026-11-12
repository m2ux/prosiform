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
| [instruction-fix.md](instruction-fix.md) | The `compiled` instruction's defect the W06 shakedown found, its fix and test evidence |

## Links

| Resource | Link |
| --- | --- |
| Epic | [Agent Pick](https://github.com/m2ux/prosiform/issues/709) |
| Prerequisites | [W03 delivery](https://github.com/m2ux/prosiform/pull/723) |
| Pull request | [[I15:E01] An agent-pick eval workflow](https://github.com/m2ux/prosiform/pull/725) |
| Instruction fix | [[I15:E01] The compiled instruction names no sources](https://github.com/m2ux/prosiform/pull/727) |
| Epic review | [[I15:E01] Agent Pick](https://github.com/m2ux/prosiform/pull/722) |

## Plan Changes

| Change | State |
| --- | --- |
| W05's work item declares the scorer, harness, Codex bridge, stub agent, runbook and their tests beside the workflow and README, since AC7's "reading no source" needs a check the scorer lacked | Applied |
