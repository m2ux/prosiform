# A Run-Time Fault No Source Tree States — October 2026

> Delivery · Created 2026-10-21

## Executive Summary

Two runs the error catalogue names are facts about the run rather than about the documents it reads. A source that changes between discovery and the recheck before publication raises `E_SOURCE_CHANGED`, and a build that fails in itself returns the internal-error status; neither arises from a source tree and an invocation alone, so the two fixtures declaring them carry `awaiting` and no run reaches them. This work gives a fixture a way to declare the fault its run meets, so the runner performs it beside the invocation it qualifies and both fixtures run unmarked.

It matters because the corpus is what the contract is proven against. While those two fixtures await an instrument, the error catalogue's coverage of `E_SOURCE_CHANGED` and `E_UNEXPECTED_INTERNAL_ERROR` rests on declarations no run has exercised, and the design's Consistency adversarial family is named by nothing the corpus runs. Epic [#9](https://github.com/m2ux/prosiform/issues/9) reads that family listing for its AC1, so this row is one of the two that decide whether Corpus Conformance can be integrated.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W24](w24.md) | The work item: scope, component, breakdown and test requirements |
| [Validation](validation.md) | The checks, the revision they ran at, the instruments weighed, and what the runs observed |
| [Changes](changes.md) | The plan changes this delivery made, and the delivery record behind them |

## Links

| Resource | Link |
| --- | --- |
| Task issue | [#150 \[I00:E11:W24\] Corpus Instrument for a Run-Time Fault No Source Tree States](https://github.com/m2ux/prosiform/issues/150) |
| Epic | [#39 \[I00:E11\] Deferred Debt](https://github.com/m2ux/prosiform/issues/39) |
| Initiative | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Origin record | [Error code coverage](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-129-i00-e11-w17-an-error-code-no) |
