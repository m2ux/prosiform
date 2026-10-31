# I07 Review Remediation — October 2026

> Planning record · Created 2026-10-31

## Executive Summary

Fifteen epics already merged into `main` were reviewed for delivered defects, and eighty-two findings were recorded: five blockers, thirty-six majors and forty-one minors.

This initiative delivers forty-one of them across thirty-four criteria in fifteen tasks. Every blocker is delivered here. Eight majors and thirty-three minors are taken elsewhere: the findings whose fix no run of the tool shows belong to [I01:E03](https://github.com/m2ux/prosiform/issues/187) by its own stated boundary, and the example's missing script paths belong to [I06:E00](https://github.com/m2ux/prosiform/issues/406), whose Problem names the same lines.
    10|
The findings and their evidence are held in [the review record](../2026-10-31-merged-epic-review/README.md), whose disposition table names the task delivering each finding.

## Decisions

Each decision was taken with the user before the initiative was raised, or on review of the epic after it was.

| Id | Decision | Findings |
| --- | --- | --- |
| D1 | **Tighten the instrument.** Where a check accepts what its documentation forbids, the check moves to the rule and the corpus is corrected where it breaks it. | 10, 12, 13, 20, 33, 34 |
| D2 | **Refuse what cannot be represented.** A construct the build cannot carry is refused with a named code and a remedy. | 4, 19, 21, 37, 39 |
| D3 | **Observe the question.** The opencode harness reads a state's output text, so a dispatched question is measurable rather than assumed answered. | 6 |
| D4 | **Refuse a stopped run.** A run its budget stopped, where every started session errored, is refused carrying the agent's reason. | 23 |
| D5 | **Keep separators.** One title-casing convention governs every heading a bundle emits, preserving the separators a name carries. | 38 |
| D6 | **Drop the label from the linked entry.** The linked form measures link-following, so its entry document carries no branch label. | 22 |
| D7 | **Name the refresh condition.** An overview is rewritten where the head it explains has moved. | 26 |
| D8 | **Read the absent record.** The board path reads a task issue's Development links, so a pull request titled without its initiative prefix cannot make evidence look complete. | 27 |
| D9 | **Derive the counts.** A count in the example is read from the artefact it describes at check time. | 30 |
| D10 | **Name the revision.** The tag a demonstration is repeatable on is named where the demonstration is taught. | 31 |
| D11 | **Bound the work, not only the bytes.** The declared resource bound also bounds the work its run performs. | 35 |
| D12 | **Declare the inputs.** A step that calls an operation declares each input that operation requires. | 81 |
| D13 | **Deferred to the tree that moves.** The example's script paths are corrected by the work that gives the example its program. | 32 |
| D14 | **Cut by scope area, held to the grain.** A task is one pull request's worth of work and carries at most three criteria. | all |
| D15 | **Add the unplanned finding.** The baseline ships short of the cell set its matrix runs, and the corpus row already holds its criterion. | 61 |
| D16 | **The guard task repairs the corpus it breaks.** A task that tightens a rule also corrects the example where that rule is already broken. | 12, 16 |
| D17 | **No task shares a pull request.** Each task repairs one scope area and carries its own failing case. | all |
| D18 | **Raise priority.** The epic holds every blocker and a silent data-loss path, so it outranks work that leaves what a user sees unchanged. | all |
| D19 | **Move the check-and-design findings.** A finding whose fix no run of the tool shows belongs to the epic that holds that material by its own boundary. | 10, 12, 13, 14, 15, 16, 33, 34, 52, 55, 56, 65, 71, 76, 77 |
| D20 | **Defer the minors.** A minor is recorded and addressed later, so no epic is raised for one before the blockers and majors it would sit beside are delivered. | 41–51, 53, 54, 57–60, 62–64, 66–70, 72–75, 78, 79 |
| D21 | **Amend the initiative to its epic.** A criterion no epic serves is dropped, and one served in part is narrowed to what the epic delivers. | initiative AC2, AC7 |

## Task Disposition

Each finding below is delivered by exactly one task, and each row's Coverage carries one criterion per finding, so a criterion and the task delivering it read from the same row.

| Task | Scope | Findings |
| --- | --- | --- |
| W01 | build | 3, 11 |
| W02 | source | 4, 18 |
| W03 | source | 19, 20, 25 |
| W04 | source | 37, 39 |
| W05 | source | 28, 38, 40 |
| W06 | source | 35, 36 |
| W07 | eval | 1, 8 |
| W08 | eval | 6, 7 |
| W09 | eval | 9, 23, 24 |
| W10 | eval | 21, 22 |
| W11 | eval | 61 |
| W12 | example | 5, 26 |
| W13 | example | 26, 27 |
| W14 | example | 30, 31 |
| W15 | example | 17, 29, 81 |

Findings 1 and 8 describe one defect from two directions and share one criterion.

## Taken Elsewhere

| Taken by | Findings | Why |
| --- | --- | --- |
| [I01:E03](https://github.com/m2ux/prosiform/issues/187) | 10, 12, 13, 14, 15, 16, 33, 34, 52, 55, 56, 65, 71, 76, 77 | A rule the design or a check states imprecisely, whose fix no run of the tool shows, which is that epic's stated boundary |
| [I06:E00](https://github.com/m2ux/prosiform/issues/406) | 32 | The example's command lines, named in that epic's own Problem |
| Recorded only | 41–51, 53, 54, 57–60, 62–64, 66–70, 72–75, 78, 79 | Minors deferred by decision: they are addressed later, not by this initiative |

## Joins

No task shares a pull request with another, and no pair is joined. The tasks are incomparable: each repairs one scope area across files the others do not touch, and each carries the case that proves its own finding.

That incomparability is what the empty Joins cell records, rather than an unexamined default.

## Corrections

The epic was reviewed twice after it was raised, and these corrections are what the reviews answered.

| Correction | Why |
| --- | --- |
| Fifteen findings moved to I01:E03 | That epic states the boundary they belong to; two epics claiming one scope is how the stale-README finding came to be reported twice |
| Priority raised from 3 to 1 | It holds every blocker and a silent data-loss path, ahead of work that changes nothing a user sees |
| W13's edge dropped from W14 and W15 | Neither consumed an output it produces, the same overbreadth removed from W08 |
| Criteria renumbered in sequence | Two were appended out of order, and dependencies now read as earlier rows throughout |
| The title widened | It named enforcement alone while the epic also refuses, derives and corrects |
| Criteria grouped to their task | Each row's Coverage carries the criteria its findings need, one per finding |
