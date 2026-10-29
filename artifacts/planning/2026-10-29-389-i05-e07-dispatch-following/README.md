# I05:E07 Dispatch Following — October 2026

> Epic planning · Created 2026-10-29

## Executive Summary

This epic measures whether an agent given a bundle set follows it. `pf` compiles each dispatched target into a bundle of its own and opens each bundle with the dispatch protocol it uses, so a dispatch chain, a parallel set and a relayed question are all things a bundle set states rather than things an agent has to invent. Nothing observes any of them: the diagram-following eval walks one bundled diagram from its entry to a terminal state and records no sub-agent start.

The epic is I05:E07: dispatch and parallel-dispatch scenarios in the diagram-following eval, a sub-agent record beside the trace, the scorer checks that pass or classify a dispatch trace, and the first baseline. Every row extends the eval I05:E01 built, so the epic takes priority 7, one below E01, and its rows carry the task edges on E01's rows.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W01 work item](w01.md) | Dispatch scenarios in their compiled and authored-protocol forms |
| [W02 work item](w02.md) | The sub-agent record and the scorer's dispatch checks |
| [W03 work item](w03.md) | The first baseline of the dispatch scenarios |

## Design

### Scenarios

- **Four scenarios.** A dispatch chain, a parallel set, a set beside a dispatch, and a dispatched target returning a question. Each names its inputs and the dispatch trace a correct agent produces: the sub-agents it starts, in what order, and what each returned.
- **A form is a bundle set.** The compiled form is the source tree whose links carry `⇉` and `⫽`, bundled by `pf` from the guide a bare `pf` prints. The authored-protocol form is the same state documents with the protocol written in as prose, so the report separates what compilation adds.
- **The scenario names the trace.** A scenario's expected trace is a walk of the bundle set its source produces, so the corpus holds one statement of the dispatch each source states.

### Scoring

- **The transcript is the record.** A sub-agent start reaches the session transcript, which the runner reads beside the trace and the session's cost and writes out. The scorer needs no second read.
- **Four checks.** Every bundle reached a sub-agent; a set's bundles started together; every question a sub-agent returned was put to the user rather than answered; the run completed.
- **One class per check.** A failing trace takes the first check it fails, so the report's failure kinds distinguish a bundle left undispatched from a set run in sequence and from a question answered in the sub-agent's place.

### Baseline

- **Cost first.** The run's estimate is put to the user before it starts, as the diagram-following baseline's was, and the run starts only on their approval.
- **Committed with its cost.** The baseline file and the run's report are committed, and the eval's README states the dispatch scenarios' measured cost.

## Delivery

| Row | Task | Pull request |
| --- | --- | --- |
| W01 | Dispatch scenarios in both forms | 1 |
| W02 | Sub-agent record and dispatch scorer checks | 2 |
| W03 | First baseline of the dispatch scenarios | 3 |

## Decisions

- **The eval leaves E03.** The three criteria W16 carried are the eval's, not the compiler's, and W16 could not start until the diagram-following eval reached `main`, so the work moves to its own epic: E07, beside the epic it extends, with the row split into the scenarios, the scorer's checks and the baseline. (User, 2026-10-29.)
- **Three rows.** The scenarios, the scorer's checks and the baseline are three pull requests: the first two are stub-agent-tested work, the third spends money and needs the user's approval before it starts. (User, 2026-10-29.)
- **E03 renumbers its criteria.** The retired AC23–AC25 leave AC26–AC38 closing the gap to AC23–AC35. The merged review-fix pull request #366 and its record cite the retired numbers. (User, 2026-10-29.)
- **Priority 7.** Every row extends `evals/diagram-following/`, which exists only on `i05/e01/main` and has not reached `main`, so E07 follows E01 by one number. E01 is at priority 8 and unmerged; E07 is released when E01's base merges. (User, 2026-10-29.)
- **No whole-epic edge in the initiative.** E07's rows take their edges on E01's rows, and E07 consumes nothing from E03, so the initiative row names no epic. (Planning, 2026-10-29.)

## Component Map

| Row | Component | Further paths written |
| --- | --- | --- |
| W01 | `evals/diagram-following/workflows` | `evals/diagram-following/workflow.py`, `test_workflow.py`, `README.md` |
| W02 | `evals/diagram-following/score.py` | `evals/diagram-following/run.py`, `stub_agent.py`, `instruction.md`, `test_score.py`, `test_run.py` |
| W03 | `evals/diagram-following/baseline.json` | `evals/diagram-following/report.py`, `report.md`, `README.md` |

## Collision Surface

Checked against the in-flight I05 epics and the open pull requests on 2026-10-29.

- **I05:E01 Diagram Following (#333).**
  `i05/e01/main` is unmerged, its review pull request #353 open, and it holds `evals/diagram-following/`. Every row of this epic writes the same folder: `deps.py` reports E01 W01 and E07 W01 contending on `evals/diagram-following/workflows`, E01 W02 and E07 W02 on `score.py`, and E01 W05 and E07 W03 on `baseline.json`. That is why E07 takes priority 7 and waits for E01.
- **I05:E03 Dispatch Bundles (#351).**
  Holds the `pf` behaviour these scenarios exercise; the eval row has left it, and no row here writes `src/` or `fixtures/`. No collision.
- **I05:E06 Example Authoring (#376).**
  Writes `example/work-planner/`; no row here does. No collision.

## Epic Priority

`deps.py` over I05's body with E03 rewritten and E07 added proposes E07 one below E01 and E03, from the task edges on E01's rows and the three contending components above. Confirmed: E07 `priority: 7`.

Longest chain: E01 W01 → W02 → W03 → W04 → E07 W01 → W02 → W03, seven steps.

## Review

Review Initiative Goal and Check Dependencies and Numbering over the drafts, 2026-10-29.

- **Goal trace.**
  I05's goal clauses (tests, rules, passing checks) map to its AC1–AC3. E07 delivers AC1 through AC1 and AC3 — each scenario runs end to end in both forms, and the scorer's verdict is held by stub-agent tests — AC2 adds nothing the eval's command does not already report, and AC3 through every row's `make check` and the baseline run. I05 marks no source, so no source alignment applies.
- **`format.py`.**
  E07 reports no finding. The revised E03 reports the three findings the live body already carried: AC16 and AC22 each state a condition over a list, and the epic reaches the corpus with no corpus-audit criterion. None is caused by this move.
- **`deps.py`.**
  No problem, no unaccounted pair and no numbering advisory across I05's eight epics.
- **Settled by the user.**
  The move itself, the three-row split, E03's renumbering and the priority.
- **Sync, 2026-10-29.**
  The three rows link their work items in the epic's record, and the epic reads Backlog with every row undelivered: its prerequisite E01 W05 has landed on `i05/e01/main` but that base is unmerged.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E07 Dispatch Following](https://github.com/m2ux/prosiform/issues/389) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Prerequisite epic | [I05:E01 Diagram Following](https://github.com/m2ux/prosiform/issues/333) |
| Source epic | [I05:E03 Dispatch Bundles](https://github.com/m2ux/prosiform/issues/351) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
