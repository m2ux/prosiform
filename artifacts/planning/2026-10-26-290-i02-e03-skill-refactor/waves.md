# Waves

The epic's nineteen tasks in three waves. Each task is one pull request over one group of files, and the file its work item declares as its component is the group's first. Depends on carries the order; the waves group the work by layer.

- **Wave 1 changes artifacts.** Each task completes one artifact group: the fixes and extensions to its existing operations and the operations it gains, so no task waits on another for the same file. The ten tasks share no source file and can run together.
- **Wave 2 changes protocols.** Each task writes or clears one cluster of protocols that share inputs, and depends on the artifact groups whose operations it applies. The four clusters share no file.
- **Wave 3 changes modes, then verifies.** Each mode task depends on the protocols it follows and the artifact groups it applies directly; the four mode groups share no file. The last task removes operations left uncalled, brings the worked examples in line, and verifies the bundles and fixtures.
- **Concurrent tasks share only generated files.** Every task re-records the usage fixtures its change moves, so a rebase re-records them rather than merging them.
- **Call sites move a layer at a time.** Wave 1 leaves the modes' and protocols' calls as they are, and wave 2 the modes' calls. The example is not run live, so an operation with no caller yet on the epic base costs nothing; the last task removes any that stay uncalled.

## Wave 1: artifacts

| Task | Files | Description | Coverage | Depends on |
| --- | --- | --- | --- | --- |
| W01 | `example/work-planner/artifacts/issue.md`, `example/work-planner/artifacts/issue-body.md` | Issue and issue-body operations | AC1, AC2 |  |
| W02 | `example/work-planner/artifacts/initiative-issue-body.md`, `example/work-planner/artifacts/acceptance-criteria.md` | Criteria and initiative-body operations | AC3, AC4 |  |
| W03 | `example/work-planner/artifacts/epic-issue-body.md`, `example/work-planner/artifacts/task-body.md`, `example/work-planner/artifacts/epic.md` | Epic, epic-body and task-body operations | AC5, AC6, AC7 |  |
| W04 | `example/work-planner/artifacts/board.md`, `example/work-planner/artifacts/board-queue.md` | Board and board-queue operations | AC8, AC9, AC10 |  |
| W05 | `example/work-planner/artifacts/delivery-evidence.md`, `example/work-planner/artifacts/delivery-plan.md`, `example/work-planner/artifacts/standup-report.md`, `example/work-planner/artifacts/board-delivery.md` | Delivery evidence, plan and report operations | AC11, AC12, AC13 |  |
| W06 | `example/work-planner/artifacts/pull-request.md`, `example/work-planner/artifacts/delivery-branches.md`, `example/work-planner/artifacts/repository-graph.md`, `example/work-planner/artifacts/pull-request-body.md` | Pull request and branch operations | AC14, AC15, AC16 |  |
| W07 | `example/work-planner/artifacts/planning-record.md`, `example/work-planner/artifacts/work-item.md`, `example/work-planner/artifacts/delivery-brief.md` | Planning record, work item and brief operations | AC17, AC18 |  |
| W08 | `example/work-planner/artifacts/placement.md`, `example/work-planner/artifacts/dependency-graph.md`, `example/work-planner/artifacts/plan-change.md` | Plan change, dependency and placement operations | AC19, AC20, AC21 |  |
| W09 | `example/work-planner/artifacts/technical-debt.md` | Technical debt classified by its artifact | AC22 |  |
| W10 | `example/work-planner/artifacts/architecture-overview.md`, `example/work-planner/artifacts/goal-trace.md` | Overview and goal-trace fields and returns | AC23, AC24 |  |

## Wave 2: protocols

| Task | Files | Description | Coverage | Depends on |
| --- | --- | --- | --- | --- |
| W11 | `example/work-planner/protocols/delivery-recording.md`, `example/work-planner/protocols/epic-closure.md`, `example/work-planner/protocols/issue-closure.md`, `example/work-planner/protocols/issue-delivery.md`, `example/work-planner/protocols/task-merge.md` | Delivery recording and closure protocols | AC25 | W01, W02, W03, W06 |
| W12 | `example/work-planner/protocols/review-pull-request.md`, `example/work-planner/protocols/delivery-base-preparation.md`, `example/work-planner/protocols/epic-integration.md` | Base preparation, review and integration protocols | AC26 | W02, W06 |
| W13 | `example/work-planner/protocols/issue-placement.md`, `example/work-planner/protocols/initiative-publication.md` | Initiative publication and issue placement protocols | AC27 | W01, W02, W07, W08 |
| W14 | `example/work-planner/protocols/unit-hold.md`, `example/work-planner/protocols/change-overview.md` | Unit hold and change overview protocols | AC28 | W03, W06, W07 |

## Wave 3: modes and verification

| Task | Files | Description | Coverage | Depends on |
| --- | --- | --- | --- | --- |
| W15 | `example/work-planner/modes/advance-mode.md`, `example/work-planner/modes/standup-mode.md`, `example/work-planner/modes/sync-mode.md` | Sync, Advance and Standup orchestrating only | AC29 | W04, W05, W08, W10, W11 |
| W16 | `example/work-planner/modes/align-mode.md`, `example/work-planner/modes/plan-mode.md` | Align and Plan orchestrating only | AC30 | W10, W11, W12, W13 |
| W17 | `example/work-planner/modes/deliver-mode.md` | Deliver Mode orchestrating only | AC31 | W05, W08, W09, W11, W12, W14 |
| W18 | `example/work-planner/modes/revise-mode.md`, `example/work-planner/modes/hoist-mode.md`, `example/work-planner/modes/propose-mode.md` | Hoist, Propose and Revise orchestrating only | AC32, AC33 | W04, W13 |
| W19 | `example/work-planner`, `example/README.md`, `fixtures/usage-example` | Uncalled operations removed, tree and fixtures verified | AC34, AC35, AC36 | W15, W16, W17, W18 |
