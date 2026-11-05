# Decisions and goal trace

## Confirmed scope

The user defers I10 E04 W14–W16 to later evaluation refinement because the measurements are not critical to starting I11. The destination is I14: I13 remains Production Build (#532). I14 has one epic at priority 1, no delivery lanes, and three sequential tasks. It remains in Backlog without an initiative priority; it is not dispatched in this alignment.

## Transfer map

| Source | Destination | Criterion mapping |
| --- | --- | --- |
| I10 E04 W16 | I14 E00 W01 | AC25 becomes AC1 (measured shakedown budget) and AC2 (rubric exercise) |
| I10 E04 W14 | I14 E00 W02 | AC20 becomes AC3 (edge matrix records); AC24 becomes AC4 (failure dispositions) |
| I10 E04 W15 | I14 E00 W03 | AC21 becomes AC5 (form and workflow inventory) and AC6 (published pass rates) |

The removed source row and criterion IDs remain unused. Existing delivered row IDs, PR links and completion ticks stand. Source work-item files identify the destination; destination work items retain their design and use no lanes. The guide means the guide integrated with the measured build, rather than an older integration branch's printed text.

## Goal trace

The goal is published edge measurements supported by committed, reproducible evidence. Initiative AC1 spans E00 AC1–AC6: shakedown budget, rubric exercise, declared-matrix coverage, failure disposition, source inventory and published rates. Every epic criterion has one task row. The initiative marks no new requirement source; its scope is the work the user transfers from the existing plan.

## Release boundary

I10 AC13 describes corpus and harness capability, with its completion still subject to E04 integration. I10 AC15 remains the runbook condition for live records committed under its retained scope; E04's Coverage omits it because the live edge run is held here. The removed measurement criteria are transferred, not ticked as complete.

I11's argument-surface and grouping-and-composition prerequisites (#462 and #463) are closed as completed. Deferred edge measurement does not gate release preparation. E04 review PR #622 remains open and conflicted at head `1076ef5293c0da74163d1289adf56ab0ef8cfbb0`; the alignment neither merges it nor claims its integration complete. The user owns the release merge.

## Deferred execution findings

Before the shakedown, reconcile the runner's baseline and edge workflow selections and token budget with the runbook. Check the integrated guide against emitted dispatch-set headings. Existing corpus and printed-guide tests do not establish those conditions or constitute a live edge measurement. The runbook's model and run budget are selected for the eventual run; this plan authorizes no paid session.
