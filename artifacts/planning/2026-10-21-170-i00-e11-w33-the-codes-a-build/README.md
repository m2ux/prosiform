# The Codes a Build Reports for Itself — October 2026

> Delivery · Created 2026-10-21

## Executive Summary

The contract states that the error codes a build emits are exactly those the design declares. Three readings establish parts of it: the harness holds the schema's catalogues to the design's codes, and the corpus runner compares each emitted diagnostic's code with the one its fixture declared. A code a build carries on a path no fixture reaches is held by nothing, and a check naming a build's internals would bind that implementation rather than the contract.

It matters because the gap is invisible: a build carrying a code the design does not name passes every check the repository runs. The documented invocation is already held to the build's own help output, so the command's surface is where a build can state what it produces without any check reading inside it.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W33](w33.md) | The work item: scope, component, breakdown and test requirements |
| [Decision](decision.md) | Where a build states the codes it can emit, and what that reading costs |
| [Validation](validation.md) | The checks run, their revisions, and the evidence each result links |
| [Change list](change-list.md) | Each plan change this delivery applied and each it held |

## Links

| Resource | Link |
| --- | --- |
| Task issue | [#170 \[I00:E11:W33\] Emitted Codes: A Build Reports the Codes It Can Emit](https://github.com/m2ux/prosiform/issues/170) |
| Epic | [#39 \[I00:E11\] Deferred Debt](https://github.com/m2ux/prosiform/issues/39) |
| Origin record | [Clause-to-fixture mapping](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-9-i00-e10-w02-clause-to-fixture-mapping) |
