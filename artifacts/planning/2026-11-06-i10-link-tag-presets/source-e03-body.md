## Overview

Grouping pools one heading text from several documents into a single emitted heading, and where the text occurs more than once each contributor hangs beneath a variant heading named after its document. A reference to a pooled heading reaches the variant naming its own document, and a whole-document reference reaches the one heading naming that member, so no two members of one group reach one destination. That holds by construction alone: candidate validation passes a bundle in which one destination answers two members. This epic makes validation hold it.

## Problem

- **The invariant holds by construction alone.**
  The design states that no two members of one group reach one destination, and the [target-integrity check](https://github.com/m2ux/prosiform/blob/e520dfa4f460298c9abd2981a2960f0a8e7852f6/src/prosiform/candidate.py#L980-L1007) asks only whether a destination's heading answers the target assigned to it.
- **A heading answering two members passes.**
  A merged heading recorded as answering both contributors' fragments satisfies that check for both, which is how the regression [02ec51b1](https://github.com/m2ux/prosiform/commit/02ec51b1) repaired stayed green in the corpus.
- **The validation page lists no such invariant.**
  [The invariants](https://github.com/m2ux/prosiform/blob/e520dfa4f460298c9abd2981a2960f0a8e7852f6/docs/validation.md#the-invariants) name target integrity and uniqueness, and neither says a destination answers one member.

## Proposal

- **The design lists the invariant among those validation holds.**
  One destination answers the targets of one member of a group, and candidate validation checks it against the provenance each emitted heading records.
- **A destination answering two members is refused.**
  A candidate whose emitted heading answers targets of two documents in one merged group fails validation, and nothing is published.
- **The validation page states it.**
  The invariant table names it beside target integrity, so a reader of the page meets the rule the build holds.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/pull/630) | Design clause | AC1 | | | ✓ |
| [W01](https://github.com/m2ux/prosiform/pull/631) | A destination answers one member | AC2 | W00 | | ✓ |
| [W02](https://github.com/m2ux/prosiform/pull/633) | The validation page states the invariant | AC3 | W01 | | ✓ |

## Acceptance Criteria

- [x] **AC1.** The canonical design lists one member per destination among the invariants candidate validation holds before the build checks it, as the requirement trace and revision history show.
- [x] **AC2.** A candidate in which one emitted heading answers the targets of two members of one group fails with a named code and publishes nothing, as the candidate-validation tests show.
- [x] **AC3.** The validation page lists one member per destination among the invariants a bundle is held to, as an inspection of `docs/validation.md` and `make vocabulary` show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-463-i09-grouping-and-composition) — the work items, the dependency check and what earlier work already delivered, planned when this epic was I09:E01.
- **R2.** [Candidate validation](https://github.com/m2ux/prosiform/blob/e520dfa4f460298c9abd2981a2960f0a8e7852f6/src/prosiform/candidate.py) — the invariants a candidate is held to against its provenance.
- **R3.** [Grouping fixture](https://github.com/m2ux/prosiform/tree/e520dfa4f460298c9abd2981a2960f0a8e7852f6/fixtures/grouping/a-reference-to-a-grouping-depth-heading) — a reference to a pooled heading reaching the variant naming its document.
- **R4.** [Evaluation and checks record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the initiative this epic belongs to and the decision that moved it there.
