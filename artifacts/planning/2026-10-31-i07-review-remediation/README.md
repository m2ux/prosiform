# I07 Review Remediation — October 2026

> Planning record · Created 2026-10-31

## Executive Summary

Fifteen epics already merged into `main` were reviewed for delivered defects. Eighty-two findings were recorded, of which forty-one are blockers or majors. This initiative delivers forty-one of them across forty criteria: every blocker and major except the one deferred to the work that moves the example tree, plus one minor the same instrument already reaches. Two findings describe one defect and share a criterion.

The findings and their evidence are held in [the review record](../2026-10-31-merged-epic-review/README.md). This record holds what that review did not: the decisions taken when each finding was reconciled.
    10|
## Decisions

Each decision was taken with the user before the initiative was raised. A decision covers every finding it names.

| Id | Decision | Findings |
| --- | --- | --- |
| D1 | **Tighten the instrument.** Where a check accepts what its documentation forbids, the check moves to the rule and the corpus is corrected where it breaks it in the same pull request. Fixtures that begin failing are the intended outcome. | 10, 12, 13, 20, 33, 34 |
| D2 | **Refuse what cannot be represented.** A construct the build cannot carry is refused with a named code and a remedy, rather than resolved silently or by an internal error. | 4, 19, 21, 37, 39 |
| D3 | **Observe the question.** The opencode harness reads a state's output text, as the other two harnesses do, so a dispatched question is measurable rather than assumed answered. | 6 |
| D4 | **Refuse a stopped run.** A run its budget stopped, where every started session errored, is refused carrying the agent's reason, on the same rule that already refuses a run which started nothing. | 23 |
| D5 | **Keep separators.** One title-casing convention governs every heading a bundle emits, preserving the separators a name carries, which is what the glossary and hierarchy pages already say. Affected fixtures are regenerated. | 38 |
| D6 | **Drop the label from the linked entry.** The linked form measures link-following, so its entry document carries no branch label, and the corpus check holds every entry document to that. | 22 |
| D7 | **Name the refresh condition.** An overview is rewritten when the head it explains has moved, which is the condition that makes its retention and its rewriting one rule. | 26 |
| D8 | **Read the absent record.** The board path reads a task issue's Development links, as the delivery path already does, so a pull request titled without its initiative prefix cannot make evidence look complete. | 27 |
| D9 | **Derive the counts.** A count in the example is read from the artefact it describes at check time, so it cannot drift again. | 30 |
| D10 | **Name the revision.** The tag a demonstration is repeatable on is named where the demonstration is taught. | 31 |
| D11 | **Bound the work, not only the bytes.** The declared resource bound also bounds the work its run performs, so a legal input cannot cost time or memory beyond it. | 35 |
| D12 | **Declare the inputs.** A step that calls an operation declares each input that operation requires. | 81 |
| D13 | **Deferred to the tree that moves.** The example's script paths are corrected by the work that gives the example its program, so this initiative does not repatch a tree that is about to move. | 32 |
| D14 | **Cut by scope area, held to the grain.** A task is one pull request's worth of work and carries at most three criteria, so a scope area holding more than three distinct invariants is split. | all |
| D15 | **Add the unplanned finding.** One finding is delivered although it is not a major, because the criterion it belongs to already exists: the baseline ships short of the cell set its matrix runs. | 61 |
| D16 | **The guard task repairs the corpus it breaks.** A task that tightens a rule also corrects the example where that rule is already broken, so a rule and the document violating it never ship apart. | 12, 16 |
| D17 | **No task shares a pull request.** Each task repairs one scope area and carries its own failing case, so no pair is comparable and none needs a shared branch. | all |

## Finding Disposition

Findings 1 and 8 describe one defect from two directions — the Cursor harness receiving a session form where a corpus form is expected — and are delivered by one criterion.

Each finding below is delivered by exactly one task. Coverage cells carry one criterion per finding, so a finding's criterion and the task that delivers it are read from the same row.

| Task | Scope | Findings |
| --- | --- | --- |
| W01 | build | 3, 11 |
| W02 | checks | 12, 13 |
| W03 | checks | 14, 15, 16 |
| W04 | source | 4, 18 |
| W05 | source | 19, 20, 25 |
| W06 | source | 33, 37, 39 |
| W07 | source | 28, 38, 40 |
| W08 | source | 35, 36 |
| W09 | eval | 1, 2, 8 |
| W10 | eval | 6, 7 |
| W11 | eval | 9, 23, 24 |
| W12 | eval | 10, 21, 22 |
| W13 | example | 5, 26, 27 |
| W14 | example | 30, 31, 34 |
| W15 | example | 17, 29, 81 |

## Deferred

| Finding | What it is | Taken by |
| --- | --- | --- |
| 32 | Thirty-nine command blocks name a script path no tree carries | [I06 Skill Distribution](https://github.com/m2ux/prosiform/issues/405) — its Problem names the same lines |

## Joins

No task shares a pull request with another, and no pair is joined. The tasks are incomparable: each repairs one scope area across files the others do not touch, and each carries the case that proves its own finding, so no pair needs a shared branch to land.

That incomparability is what the empty Joins cell records, rather than an unexamined default.

## Corrections

The epic was reviewed for gaps, consistency, dependencies and joins after it was raised, and the review is what these corrections answer.

| Correction | Why |
| --- | --- |
| Findings 33 and 37 merged into AC13, and 21 into AC39 | The epic published a criterion per finding for all but these; the Problem named them while no criterion restated them |
| W04's edge dropped from W08 | W08 consumes neither output W04 produces, so the edge was overbroad |
| AC3 and AC7 widened to require the example carry no instance of the rule they report | The tightened rules fail on the example as it stands, so the guard task repairs that in the same pull request |
| The Work Breakdown table lost its Joins column | An epic row carries five cells; Joins is a task-level column the rows never used |
| The epic's title widened | It named enforcement alone while the epic also refuses, derives and corrects |
| This record's closing section renamed | It discussed the review point and the demonstration tag, and named neither in its heading |

## Points Reviewed

The review ran at `23882b7d`. The tag `demo/i02` is unaffected; the question D10 settles is where that tag is named, not whether it exists.
