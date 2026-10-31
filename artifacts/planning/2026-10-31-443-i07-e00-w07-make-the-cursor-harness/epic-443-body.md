## Overview

The review of fifteen merged epics recorded forty-two blockers and majors. This epic delivers forty of them, across the build's order of checks, the repository checks, the build's source, the diagram-following eval and the example skill. One is deferred to the work that moves the example tree; findings 1 and 8 are one defect and are delivered by a single criterion.

Each task repairs one scope area and carries the case that failed, so a defect cannot return unnoticed. The ordering is deliberate: the check order lands first, because until `make steps` and `make authoring` run ahead of `corpus` and `test`, a broken corpus reports moved bundle bytes rather than the rule that was broken — which is the reason several of these findings read as something else when they were first raised.

## Problem

- **A guard states more than it inspects.**
  Seven findings are a rule stated in a check's documentation that the check cannot see: an unlabelled fence, a step anchor read as a contract section, a step at its own level, a duplicate heading compared by text, prose beside a compiled step, a coincidence warning that skips a merged group, and a fixture the render check omits.
- **A construct resolves by accident rather than refusing.**
  A dispatch link in an absorbed title is an internal error, a `links` array renders anchors the run never follows, and a group name of `-` emits an empty heading. Each exits successfully or fails as an internal fault.
- **The eval scores what it cannot observe.**
  One harness crashes before a session starts, another reports every dispatched question as answered, and a run stopped by its budget tabulates as completed. A baseline is then written from cells the run never measured.
- **The instrument that should catch these runs last or not at all.**
  Two check targets sit after the corpus, and two more after the tests, so the first failure a broken tree produces is not the rule it broke.
- **A count and a revision are remembered rather than read.**
  A page states a figure that has drifted, and the revision a demonstration is repeatable on is named nowhere the demonstration is taught.

## Proposal

- **The check moves to the rule, and the corpus moves with it.**
  Where a check accepts what its documentation forbids, the check is corrected and the example is corrected where it breaks the rule, in the same pull request. Fixtures that begin failing are the outcome the task is for.
- **A construct with no representation is refused.**
  A named code and a stating remedy, in the manner the contract already uses for an unreadable input, replaces both silent resolution and the internal error.
- **The eval measures only what it saw.**
  A harness reads the state's output, a stopped run is refused carrying its reason, and a form whose entry gives away the answer is corrected so it measures the behaviour it names.
- **A count is read from its artefact, and a revision is named where it is used.**
  The example's stated figures are derived when the check runs, and the tag a demonstration repeats on is named beside the command that repeats it.
- **Each repair is proved by the case that failed.**
  Every task adds the fixture, test or check that would have caught its finding, and the task is not delivered until that case fails without the fix.

## Work Breakdown

| Task | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/pull/466) | Put rule guards ahead of the corpus | AC1, AC2 | | ✓ |
| [W02](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-443-i07-e00-w02-refuse-distribution-faults-and/) | Refuse distribution faults and entry overwrite | AC3, AC4 | | |
| W03 | Carry every click and every link element | AC5, AC6, AC7 | W02 | |
| W04 | Refuse group and member names that empty | AC8, AC9 | W02 | |
| W05 | One title case, one destination per parent | AC10, AC11, AC12 | W02 | |
| [W06](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-443-i07-e00-w06-bound-the-work-behind/) | Bound the work behind the byte budget | AC13, AC14 | | |
| [W07](https://github.com/m2ux/prosiform/pull/468) | Make the Cursor harness run and keep traces | AC15, AC16 | | ✓ |
| W08 | Observe a question and count a session | AC17, AC18 | W07 | |
| W09 | Refuse a run that could not complete | AC19, AC20, AC21 | W07 | |
| W10 | Hold the corpus to what each form measures | AC22, AC23, AC24 | W07 | |
| W11 | Complete the committed baseline | AC25 | W09 | |
| W13 | State the overview rule and its condition | AC26, AC27 | | |

## Acceptance Criteria

- [x] **AC1.** `make check` runs every guard that reads the example ahead of every target that bundles it, as the order test reads the `Makefile`.
- [x] **AC2.** A file breaking a rule guard fails the run naming that file and the rule, as an injected break in each guarded document class shows.
- [ ] **AC3.** A dispatch link in an absorbed document title is refused with a named code and a remedy rather than raising an internal error, as a run over that document is shown.
- [ ] **AC4.** A path standing at `<entry>.bundles` that is neither a directory nor a symbolic link is refused and left untouched, as a run over that path shows.
- [ ] **AC5.** A `links` value that is an array of destinations is refused with a named code, as a run over that value shows.
- [ ] **AC6.** An anchor in a fence line is refused only where the renderer draws an anchor there, as a run over a tooltip, a pie label and a sequence note shows.
- [ ] **AC7.** A line carrying more than one `click` follows every one of them, as a run over that line shows.
- [ ] **AC8.** A declared group name whose title case is empty is refused, as a run over each such name shows.
- [ ] **AC9.** A member whose name title-cases to nothing takes its path text, or is refused, as a run over that member shows.
- [ ] **AC10.** Every heading a bundle emits is title-cased by one convention, as a bundle holding a group, a member and a file heading shows.
- [ ] **AC11.** A titled parent's whole-document reference resolves to its own title heading at every grouping depth, as a run at each depth shows.
- [ ] **AC12.** An overview wrapper is emitted only where a member's above-depth content would otherwise sit beneath the group heading, as a run over members holding only a first heading shows.
- [ ] **AC13.** The declared byte budget also bounds the work its run performs, as a run at the bound is shown to complete within it.
- [ ] **AC14.** A root-not-found diagnostic names the reference that declared the root and the root it named, with a remedy, as a run over that reference shows.
- [x] **AC15.** `--harness cursor` completes a matrix over the default form list, as a matrix run against the Cursor harness shows.
- [x] **AC16.** A dispatched sub-agent's trace is kept beside the dispatching session's, under the name the instruction states, as a scored run over a dispatching scenario shows.
- [ ] **AC17.** A dispatched question the session left unanswered reads as a question, as a score against a recorded transcript shows.
- [ ] **AC18.** A session's reported spend is the sum of its steps, as the ledger against a multi-step transcript shows.
- [ ] **AC19.** A run its budget stopped, whose started sessions all errored, is refused carrying the agent's reason, as a budget-stopped run shows.
- [ ] **AC20.** A baseline is written only from cells the run measured, as a write attempted from an empty matrix shows.
- [ ] **AC21.** A set dispatched together passes only where the opener starts first and every later member starts alongside it, as a score over a split set shows.
- [ ] **AC22.** The linked form's entry document carries no branch label, as a bundle of that form shows.
- [ ] **AC23.** Every form is held to what its entry document may carry, as the corpus check over a form whose entry violates it shows.
- [ ] **AC24.** Every fixture the render check lists produces a bundle Mermaid parses, as a render of each listed fixture shows.
- [ ] **AC25.** The committed baseline carries a cell for each form and scenario the matrix runs, as a comparison of the baseline against the matrix shows.
- [ ] **AC26.** An overview is rewritten only where the head it explains has moved, as the protocol run over a moved head and an unmoved head show.
- [ ] **AC27.** The written rule states the condition under which an overview is rewritten, as that page reads against the protocol it describes.

## Initiative

[I07 Review Remediation](https://github.com/m2ux/prosiform/issues/442) — E00.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-31-i07-review-remediation/README.md) — the decisions reconciling each finding, the task that delivers it, and why no two tasks share a pull request.
- **R2.** [Merged-Epic Review, October 2026](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-31-merged-epic-review/README.md) — the review these findings come from.
- **R3.** **Source.** [Findings table](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-31-merged-epic-review/findings.md) — each defect by epic, scope and severity, with its site and failing case.
