## Overview

Picking dispatches use their link text as the generated section name, so three different operations have three recognizable destinations. Their alternatives retain the same descriptions, models and bundle targets.

## Changes

### Dispatch Naming

- **Match navigation to the dispatch.**
  Pick headings and their local graph anchors carry the dispatch name without its handoff mark.
- **Validate named selections together.**
  Picks and briefed dispatches share collision validation; different selections cannot silently share a heading.
- **Keep the output contract current.**
  Documentation, seven bundle snapshots and two diagnostic expectations describe the named sections and shared collision message.

## Test Plan

| Test | Description | Coverage | Pass |
| --- | --- | --- | --- |
| T1 | Compiler regressions and packaging integrations | AC1, AC3 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-24-846-f37-pick-dispatch-headings/test-results.md#compiler-tests) |
| T2 | Complete fixture corpus | AC2, AC4 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-24-846-f37-pick-dispatch-headings/test-results.md#fixture-corpus) |
| T3 | Lint, types and documentation checks | AC4 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-24-846-f37-pick-dispatch-headings/test-results.md#source-and-documentation) |

## References

- **R1.** [Test results](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-24-846-f37-pick-dispatch-headings/test-results.md) — Exact local candidate and observed validation, retained with this hot-fix record.
