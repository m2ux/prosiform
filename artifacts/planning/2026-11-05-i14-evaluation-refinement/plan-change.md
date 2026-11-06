# Plan change: default-matrix and cross-harness coverage deferred from I10

> Recorded 2026-11-06

## Decision

> 'defer the eval to i14'

The user defers the two measurements I10 left unmeasured to this initiative. I10 closed with both criteria dispositioned as deferred rather than measured, and the obligations are carried here by a new epic with three tasks.

## Entries

| Kind | Issue or row | Option applied |
| --- | --- | --- |
| Migration | #464 AC1, AC11 | Each criterion keeps its id, gains a sentence naming the deferral, and is ticked with the deferral as its disposition. No measurement of either was taken under #464. |
| Epic creation | [I14:E01](https://github.com/m2ux/prosiform/issues/677) | A new epic under [I14](https://github.com/m2ux/prosiform/issues/660), carrying the deferred obligations as its criteria, with three task rows and work items in this record. |
| Epic creation | [I14](https://github.com/m2ux/prosiform/issues/660) row E01 | The initiative's Work Breakdown gains the epic row, and its criteria gain the invariant the epic makes true. |

## I10 criterion disposition

| Criterion | Final state | What was not measured |
| --- | --- | --- |
| AC1 | Ticked with the deferral sentence | A pass rate for the matrix's bootstrap-audit scenarios. The committed baseline carries no bootstrap-audit cell. |
| AC11 | Ticked with the deferral sentence | Any harness's crash-free record beyond the harness whose run the committed baseline is. |

The remaining criteria #464 carries were already ticked and stand unchanged. This change neither ticks a criterion whose evidence is absent nor records a measurement that was not taken.

## Queue effect

The new epic is deferred work. It sits at the same status as its sibling epic and supplies no MVP release condition: #524 and #525 depend on nothing this change adds.

## References

- **R1.** [I10 initiative](https://github.com/m2ux/prosiform/issues/464) — the criteria this change dispositions.
- **R2.** [I14 initiative](https://github.com/m2ux/prosiform/issues/660) — the epic table this change extends.
- **R3.** [Matrix Coverage epic](https://github.com/m2ux/prosiform/issues/677) — the epic this change creates.
