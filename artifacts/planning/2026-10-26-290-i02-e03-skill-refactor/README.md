# I02 E03 Skill Refactor — October 2026

> Epic planning · Created 2026-10-26

## Executive Summary

This record plans the refactor of the example skill, `example/work-planner`, along the object-oriented structure its own rules prescribe. Each mode becomes orchestration alone; each object the modes act on is an artifact owning its operations under Operations, one `###` per operation with an opening line and an **Inputs:** line, beside its Fields, Guidance and Commands; each protocol is an artifact-agnostic procedure built only of applied operations and followed protocols; and every call goes down the stack.

It matters because the example is the demonstration the initiative is built on, and today its modes do much of the work its artifacts and protocols should own: verification, plan-change settlement and board evidence are written out several times across modes, protocols restate artifact rules, and some operations change two objects. The plan delivers in three waves, artifacts, then protocols, then modes and a final verification, as nineteen tasks of one pull request each, so no two tasks that can run together write the same source file, and every mode bundle stays clean and every check green throughout.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Refactor analysis](refactor-analysis.md) | The evidence: what leaves each mode, sorted by object, with the operations and protocols it becomes (line numbers at `da6d0515`) |
| [Epic draft](e03.md) | The epic body as published |
| [Waves](waves.md) | The tasks by wave, with each task's files, and why they are grouped as they are |
| [Joins](joins.md) | Every independent pair of tasks, accounted for as two pull requests |
| [W01](w01.md) | The work item for W01: Issue and issue-body operations |
| [W02](w02.md) | The work item for W02: Criteria and initiative-body operations |
| [W03](w03.md) | The work item for W03: Epic, epic-body and task-body operations |
| [W04](w04.md) | The work item for W04: Board and board-queue operations |
| [W05](w05.md) | The work item for W05: Delivery evidence, plan and report operations |
| [W06](w06.md) | The work item for W06: Pull request and branch operations |
| [W07](w07.md) | The work item for W07: Planning record, work item and brief operations |
| [W08](w08.md) | The work item for W08: Plan change, dependency and placement operations |
| [W09](w09.md) | The work item for W09: Technical debt classified by its artifact |
| [W10](w10.md) | The work item for W10: Overview and goal-trace fields and returns |
| [W11](w11.md) | The work item for W11: Delivery recording and closure protocols |
| [W12](w12.md) | The work item for W12: Base preparation, review and integration protocols |
| [W13](w13.md) | The work item for W13: Initiative publication and issue placement protocols |
| [W14](w14.md) | The work item for W14: Unit hold and change overview protocols |
| [W15](w15.md) | The work item for W15: Sync, Advance and Standup orchestrating only |
| [W16](w16.md) | The work item for W16: Align and Plan orchestrating only |
| [W17](w17.md) | The work item for W17: Deliver Mode orchestrating only |
| [W18](w18.md) | The work item for W18: Hoist, Propose and Revise orchestrating only |
| [W19](w19.md) | The work item for W19: Uncalled operations removed, tree and fixtures verified |

## Links

| Resource | Link |
| --- | --- |
| Epic | [#290](https://github.com/m2ux/prosiform/issues/290) |
| Initiative | [#261](https://github.com/m2ux/prosiform/issues/261) |
| Prerequisite epic | [#258](https://github.com/m2ux/prosiform/issues/258) |
| Decision D13 | [I02 decisions](../2026-10-25-261-i02-mvp-demonstration/decisions.md) |
| Epic base | [i02/e03/main](https://github.com/m2ux/prosiform/tree/i02/e03/main) |
| Board | [Board 18](https://github.com/users/m2ux/projects/18) |
