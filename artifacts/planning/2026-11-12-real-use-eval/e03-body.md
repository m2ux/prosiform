## Overview

The eval measures one skill of real size. Work Planner runs as two skill variants, the revision used through prosiform and the plain-Markdown revision before it, and each session answers a captured request. A session is scored on the context its request requires, and one committed run compares the variants on that score, tokens and reads.

## Problem

- **Every workflow is small enough to read whole.**
  [`branching`'s diagram form](https://github.com/m2ux/prosiform/tree/8c611259ab407e09e4d50262b79cf2f8eef14a5d/evals/diagram-following/workflows/branching/diagram) is nine files and 1441 bytes in all.
- **The forms tie.**
  In the [committed baseline](https://github.com/m2ux/prosiform/blob/8c611259ab407e09e4d50262b79cf2f8eef14a5d/evals/diagram-following/report.md#L16-L25), `bundle`, `tree`, `prose` and `linked` each pass every session, so no cell shows what compiling adds to reading.
- **The scorer reads a path of states.**
  A session [passes on its trace and its actions](https://github.com/m2ux/prosiform/blob/8c611259ab407e09e4d50262b79cf2f8eef14a5d/evals/diagram-following/score.py#L11-L12), and nothing states the content a request requires or checks that a session read it.
- **Tokens are reported per cell and compared nowhere.**
  The same baseline gives `bundle` a mean of 223946 tokens and `tree` 291774, and no table sets one against the other.
- **No skill of real size compiles.**
  Work Planner declares no `prosiform` until [its cutover](https://github.com/m2ux/prosiform-skills/issues/9) lands, and its [reading contracts](https://github.com/m2ux/workflow-server/pull/1695) have been run on raw sources alone.

## Proposal

- **Work Planner is a workflow of the eval.**
  Its `compiled` variant is the skill at the revision where every mode compiles, and its `tree` variant the skill at the plain revision before it.
- **Each variant names its commit.**
  Each variant is a submodule of the skill's repository pinned to one commit, and the corpus test holds the placed files to it.
- **The skill text is the skill's own.**
  Each variant's `SKILL.md` is the file its revision holds, with no paragraph of the eval's, so the scorer reads the session's record of reads and commands.
- **A scenario is a captured request.**
  Standup, Revise and Understand requests open a session in plain words, each with the inputs its request reads, so no session reaches a tracker.
- **The score is the request's context contract.**
  A session passes when its reads cover every file and section the contract its variant's revision states requires, from a source or from a bundle carrying it.
- **The report sets the variants side by side.**
  For each scenario it gives each variant's pass rate, mean tokens and mean reads, and the difference between the variants.
- **One run commits the comparison.**
  A runbook section states the run and its shakedown rule; the record is `field-scale.json` and `field-scale.md`, with every failing session triaged.
- **Finished output is not graded.**
  No check scores the standup, revision or overview a session produces.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e03/w01.md) | Work Planner placed as two variants | AC1, AC2 | [E00:W03](https://github.com/m2ux/prosiform/issues/735), [I16:E07](https://github.com/m2ux/prosiform-skills/issues/9) | | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e03/w02.md) | Sessions scored on their context contract | AC3 | W01 | | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e03/w03.md) | Report compares the variants per scenario | AC4 | W02 | | | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e03/w04.md) | Field-scale runbook section | AC5 | W03, [E02:W02](https://github.com/m2ux/prosiform/issues/737) | | | |
| [W05](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e03/w05.md) | Field-scale shakedown | AC6 | W04 | | | |
| [W06](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e03/w06.md) | The field-scale run and record | AC7 | W05 | | | |

## Acceptance Criteria

- [ ] **AC1.** The Work Planner workflow holds a `compiled` and a `tree` skill variant, each the skill's files at the repository commit its submodule pins, as the corpus test shows.
- [ ] **AC2.** Every Work Planner scenario states a captured request as its task and holds each input that request reads, as the corpus test shows.
- [ ] **AC3.** A Work Planner session passes only when its recorded reads cover every file and section its request's context contract requires, as the scorer tests show.
- [ ] **AC4.** The report gives, for each Work Planner scenario, each variant's pass rate, mean tokens and mean reads and the difference between the variants, as the report tests show.
- [ ] **AC5.** The runbook states a field-scale section whose caps are set by a shakedown rule, as the runbook test shows.
- [ ] **AC6.** The runbook's field-scale section takes its session cap, token budget and cost cap from a recorded shakedown of the Work Planner workflow, as the runbook test shows.
- [ ] **AC7.** `field-scale.json` and `field-scale.md` record a run of every Work Planner scenario in both variants whose every failing session is triaged and none is a defect or unclear, as the report's Failing Sessions shows.

## Open Questions

- Which repository commits the `compiled` and `tree` variants name. They follow the settled and baseline revisions Work Planner's cutover fixes.
## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-real-use-eval) — the field-scale decisions, the options set aside and the recommendation for each open question.
- **R2.** [Use Through Prosiform](https://github.com/m2ux/prosiform-skills/issues/9) — the cutover that makes every Work Planner mode compile and fixes the baseline revision.
- **R3.** [Reading-route harness](https://github.com/m2ux/workflow-server/pull/1695) — the captured requests, the per-request context contracts and the conformance check.
- **R4.** [Runbook](https://github.com/m2ux/prosiform/blob/8c611259ab407e09e4d50262b79cf2f8eef14a5d/evals/diagram-following/RUNBOOK.md) — the triage rubric and stop rules the run follows.
