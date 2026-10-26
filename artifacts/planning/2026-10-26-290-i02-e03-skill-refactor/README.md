# I02 E03 Skill Refactor — October 2026

> Epic planning · Created 2026-10-26

## Executive Summary

This record plans the refactor of the example skill, `example/work-planner`, along the object-oriented structure its own rules prescribe. Each mode becomes orchestration alone; each object the modes act on is an artifact owning its operations under Operations, one `###` per operation with an opening line and an **Inputs:** line, beside its Fields, Guidance and Commands; each protocol is an artifact-agnostic procedure built only of applied operations and followed protocols; and every call goes down the stack.

It matters because the example is the demonstration the initiative is built on, and today its modes do much of the work its artifacts and protocols should own: verification, plan-change settlement and board evidence are written out several times across modes, protocols restate artifact rules, and some operations change two objects. The plan delivers in three waves of one-file tasks so no two tasks that can run together write the same file, and holds every mode bundle clean and every check green throughout.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Refactor analysis](refactor-analysis.md) | The evidence: what leaves each mode, sorted by object, with the operations and protocols it becomes (line numbers at `da6d0515`) |
| [Epic draft](e03.md) | The epic body as published |
| [Waves](waves.md) | The tasks by wave, with each task's component, and why they are grouped as they are |
| [Joins](joins.md) | Every independent pair of tasks, accounted for as two pull requests |
| [W01](w01.md) | The work item for W01: Saved issues ensuring their own labels |
| [W02](w02.md) | The work item for W02: Format repair taking each kind's validator |
| [W03](w03.md) | The work item for W03: Hold and release rules in the epic body |
| [W04](w04.md) | The work item for W04: Task delivery returning its comment file |
| [W05](w05.md) | The work item for W05: Delivery evidence read without writes |
| [W06](w06.md) | The work item for W06: Available work resolving its own issues |
| [W07](w07.md) | The work item for W07: Standup report resolving its own initiatives |
| [W08](w08.md) | The work item for W08: Merge and publication rules in pull request fields |
| [W09](w09.md) | The work item for W09: Review worktree retrying a changed head |
| [W10](w10.md) | The work item for W10: Change measurement retrying a stale index |
| [W11](w11.md) | The work item for W11: Planning record populated and published together |
| [W12](w12.md) | The work item for W12: Placement options ordered by their field |
| [W13](w13.md) | The work item for W13: Dependency check reading its own work items |
| [W14](w14.md) | The work item for W14: Board placement taking the issue number |
| [W15](w15.md) | The work item for W15: Source departures stated in Sources field |
| [W16](w16.md) | The work item for W16: Overview ownership stated in its fields |
| [W17](w17.md) | The work item for W17: Goal review returning its trace table |
| [W18](w18.md) | The work item for W18: Revision checklist linking the guidelines |
| [W19](w19.md) | The work item for W19: Pull requests matched to tasks |
| [W20](w20.md) | The work item for W20: Board queue applied until it converges |
| [W21](w21.md) | The work item for W21: Test coverage checked against criteria |
| [W22](w22.md) | The work item for W22: Work item read for its component |
| [W23](w23.md) | The work item for W23: Delivery brief read and reservation confirmed |
| [W24](w24.md) | The work item for W24: Plan changes settled by one operation |
| [W25](w25.md) | The work item for W25: Technical debt classified by its artifact |
| [W26](w26.md) | The work item for W26: Issue completion checked by kind |
| [W27](w27.md) | The work item for W27: Open questions resolved by one operation |
| [W28](w28.md) | The work item for W28: Placeholder epic links resolved |
| [W29](w29.md) | The work item for W29: Unplaced task row placed by one operation |
| [W30](w30.md) | The work item for W30: Verified criteria recorded, criteria quality checked |
| [W31](w31.md) | The work item for W31: Project board ensured for a theme |
| [W32](w32.md) | The work item for W32: Board-scoped delivery evidence read once |
| [W33](w33.md) | The work item for W33: Pull request bases aligned to the epic |
| [W34](w34.md) | The work item for W34: Planning record located by reference |
| [W35](w35.md) | The work item for W35: Unit Hold protocol |
| [W36](w36.md) | The work item for W36: Issue Placement protocol |
| [W37](w37.md) | The work item for W37: Review Pull Request applying operations only |
| [W38](w38.md) | The work item for W38: Dependency findings settled through plan change |
| [W39](w39.md) | The work item for W39: Delivery Base Preparation protocol |
| [W40](w40.md) | The work item for W40: Delivery Recording protocol |
| [W41](w41.md) | The work item for W41: Epic Closure protocol |
| [W42](w42.md) | The work item for W42: Initiative Publication protocol |
| [W43](w43.md) | The work item for W43: Change Overview applying operations only |
| [W44](w44.md) | The work item for W44: Epic Integration applying operations only |
| [W45](w45.md) | The work item for W45: Issue Closure applying operations only |
| [W46](w46.md) | The work item for W46: Issue Delivery applying operations only |
| [W47](w47.md) | The work item for W47: Task pull requests merged without branch updates |
| [W48](w48.md) | The work item for W48: Board delivery reading board evidence |
| [W49](w49.md) | The work item for W49: Advance Mode orchestrating only |
| [W50](w50.md) | The work item for W50: Hoist Mode orchestrating only |
| [W51](w51.md) | The work item for W51: Propose Mode orchestrating only |
| [W52](w52.md) | The work item for W52: Standup Mode orchestrating only |
| [W53](w53.md) | The work item for W53: Task Merge from merge to records |
| [W54](w54.md) | The work item for W54: Align Mode orchestrating only |
| [W55](w55.md) | The work item for W55: Plan Mode orchestrating only |
| [W56](w56.md) | The work item for W56: Sync Mode orchestrating only |
| [W57](w57.md) | The work item for W57: Deliver Mode orchestrating only |
| [W58](w58.md) | The work item for W58: No operation or protocol left uncalled |
| [W59](w59.md) | The work item for W59: Worked examples quoting the current tree |
| [W60](w60.md) | The work item for W60: Mode bundles and usage fixtures verified |

## Links

| Resource | Link |
| --- | --- |
| Epic | [#290](https://github.com/m2ux/prosiform/issues/290) |
| Initiative | [#261](https://github.com/m2ux/prosiform/issues/261) |
| Prerequisite epic | [#258](https://github.com/m2ux/prosiform/issues/258) |
| Decision D13 | [I02 decisions](../2026-10-25-261-i02-mvp-demonstration/decisions.md) |
| Epic base | [i02/e03/main](https://github.com/m2ux/prosiform/tree/i02/e03/main) |
| Board | [Board 18](https://github.com/users/m2ux/projects/18) |
