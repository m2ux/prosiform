## Overview

The diagram-following eval cannot tell its forms apart. Every cell of its committed baseline is 5 of 5, so a report detects only a whole-cell collapse and says nothing about what bundling adds, what the diagram adds, or whether a branch is resolved by following a link. This epic makes the corpus hard enough for an agent to fail in ways the scorer names, then commits a baseline of every form the default matrix runs, the dispatch scenarios among them.

The two are one epic because neither is worth having alone: a baseline over the present corpus adds a column of 100% cells, and a harder corpus without a baseline has nothing to measure against.

## Problem

- **Every cell is saturated.**
  The [committed baseline](https://github.com/m2ux/prosiform/blob/23882b7d9c4faa78407468072a9eee1f8baeba4c/evals/diagram-following/baseline.json) holds 30 cells, every one 5 passed of 5, with no recorded failure of any class.
- **Five scenarios cannot reach eight classes.**
  A linear workflow offers nothing to mis-branch at, and a two-round loop is short enough to miscount by accident rather than error. Nothing asserts that each class the scorer defines has a scenario able to produce it, so a class can go dead unnoticed.
- **Three forms are in the baseline.**
  The baseline carries `bundle`, `tree` and `prose`, so every `linked` cell of a report reads `new`.
- **The dispatch forms have no baseline.**
  The compiled and authored dispatch forms are newer than the baseline, so a dispatch scenario's pass rate has nothing to be compared with.

## Proposal

- **Difficulty comes from the scenarios.**
  Each failure class the scorer defines gets a scenario a plausible misreading fails: a second decision, a counted loop, a state reachable only through a link, and a distractor no edge leads to. The corpus test asserts every class is reachable.
- **Success is two forms that differ.**
  The epic is done when the committed default-matrix baseline gives two forms of one scenario different pass rates. A harder corpus whose forms still score alike is reported as not separating them.
- **One run carries every form and every dispatch scenario.**
  The default matrix is run once, after the corpus is hardened and the eval's scoring and harness corrections land, and its cells are committed with the measured cost stated in the README. `baseline.json` is one file, so a second run would replace the first.
- **A scenario's documents declare `prosiform`.**
  A link compiles only when its target declares, so each new scenario's documents declare, and the baseline runs once the eval tree states its settings in presets.
- **The run is the evidence for I07's harness criteria.**
  The one default-matrix run is what I07's crash and answered-dispatch criteria cite, so a single paid run settles both.
- **The forms stay one statement of the edges.**
  A new scenario's path is the walk of its workflow's diagram, so the forms remain consistent with each other and with the corpus test.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/pull/655) | The default matrix runs the user's model | AC8 | W04 | | ✓ |
| [W01](https://github.com/m2ux/prosiform/pull/609) | Scenarios reaching every failure class | AC1, AC2, AC5 | [I07:E00:W10](https://github.com/m2ux/prosiform/issues/443), [I10:E05:W00](https://github.com/m2ux/prosiform/issues/594) | | ✓ |
| [W02](https://github.com/m2ux/prosiform/pull/657) | Every-form baseline over the hardened corpus | AC3, AC4, AC9 | W00, W01, W04, [I07:E00:W08](https://github.com/m2ux/prosiform/issues/443), [I07:E00:W09](https://github.com/m2ux/prosiform/issues/443), [I07:E00:W16](https://github.com/m2ux/prosiform/issues/443), [I08:E08:W02](https://github.com/m2ux/prosiform/issues/465) | | ✓ |
| [W03](https://github.com/m2ux/prosiform/pull/659) | Harness criteria read from the baseline | AC6, AC7 | W02 | | ✓ |
| [W04](https://github.com/m2ux/prosiform/pull/654) | Shake down the baseline runbook | AC10 | W01, [I10:E05:W00](https://github.com/m2ux/prosiform/issues/594), [I10:E06:W01](https://github.com/m2ux/prosiform/issues/639), [I10:E06:W07](https://github.com/m2ux/prosiform/issues/639) | | ✓ |

## Acceptance Criteria

- [x] **AC1.** Each failure class the scorer defines, and `errored`, is produced by at least one scenario in the corpus, as the corpus test `make check` runs shows.
- [x] **AC2.** Every scenario's expected path walks its workflow's diagram from the start state to a terminal state over the edges each of its forms states, as the corpus test `make check` runs shows.
- [x] **AC3.** The committed baseline carries a cell for every model, form and scenario the default matrix runs, the dispatch scenarios' compiled and authored forms among them, as a comparison of the baseline file against the matrix shows.
- [x] **AC4.** Two forms of at least one scenario carry different pass rates for one model in the committed baseline, as the baseline file shows.
- [x] **AC5.** Every document a scenario's linked form links declares `prosiform`, so each of its links compiles, as the corpus test `make check` runs shows.
- [x] **AC6.** A diagram-following harness crashes on no form the matrix runs, as the committed baseline's run against each harness shows.
- [x] **AC7.** A dispatched question counts as answered only where the session produced an answer, as the committed baseline's run against each harness shows.
- [x] **AC8.** `run.py` runs one model by default, the model `RUNBOOK.md` records as the user's choice, as `run.py --help` and `make harness` show.
- [x] **AC9.** The committed baseline gives every failing session the triage rubric's disposition, as the baseline file shows.
- [x] **AC10.** `RUNBOOK.md` records the model the user chose for the default matrix, and its baseline runbook carries a shakedown over the hardened corpus on that model, whose measured cost sets its budget and every failure of which the triage rubric decides, as the file shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the design, the work items, the joins and the planning decisions.
- **R2.** [Corpus separability record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-29-i05-e08-corpus-separability) — the decisions that made the corpus and the baseline one epic and folded the dispatch baseline into it.
