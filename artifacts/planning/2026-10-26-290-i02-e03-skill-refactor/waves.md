# Waves

The epic's sixty tasks in three waves. Each task extends one component, the file its work item declares, and is one pull request unless its Joins cell names another. Depends on carries the order; the waves group the work by kind.

- **No file is written by two tasks that can run together.** Two tasks extending one file are ordered by Depends on, so tasks that can run at once touch different files. The usage fixtures every task re-records are generated output, so a rebase re-records them rather than merging them.
- **Wave 1 and wave 2 change artifacts only.** Their call sites in modes and protocols move in wave 3, so no two early tasks edit one mode. The example is not run live, so an operation with no caller yet on the epic base costs nothing; the last task removes any that stay uncalled.
- **A wave-2 task touching no wave-1 file depends on none.** Seven new operations sit in files wave 1 leaves alone, so they can start with wave 1.
- **Wave 3 protocols depend on the operations they apply,** and each mode task depends on the protocols it follows and the operations it applies.
- **Joined pairs share a pull request.** The two operations that resolve their own missing evidence, the two freshness retries, the Task Merge rewrite with the narrowing of the operation it absorbs, and the README with the fixture verification.

## Wave 1: small fixes and extensions of existing operations

| Task | Component | Description | Depends on | Joins |
| --- | --- | --- | --- | --- |
| W01 | `example/work-planner/artifacts/issue.md` | Saved issues ensuring their own labels |  |  |
| W02 | `example/work-planner/artifacts/issue-body.md` | Format repair taking each kind's validator |  |  |
| W03 | `example/work-planner/artifacts/epic-issue-body.md` | Hold and release rules in the epic body |  |  |
| W04 | `example/work-planner/artifacts/task-body.md` | Task delivery returning its comment file |  |  |
| W05 | `example/work-planner/artifacts/delivery-evidence.md` | Delivery evidence read without writes |  |  |
| W06 | `example/work-planner/artifacts/delivery-plan.md` | Available work resolving its own issues |  | W07 |
| W07 | `example/work-planner/artifacts/standup-report.md` | Standup report resolving its own initiatives |  | W06 |
| W08 | `example/work-planner/artifacts/pull-request.md` | Merge and publication rules in pull request fields |  |  |
| W09 | `example/work-planner/artifacts/delivery-branches.md` | Review worktree retrying a changed head |  | W10 |
| W10 | `example/work-planner/artifacts/repository-graph.md` | Change measurement retrying a stale index |  | W09 |
| W11 | `example/work-planner/artifacts/planning-record.md` | Planning record populated and published together |  |  |
| W12 | `example/work-planner/artifacts/placement.md` | Placement options ordered by their field |  |  |
| W13 | `example/work-planner/artifacts/dependency-graph.md` | Dependency check reading its own work items |  |  |
| W14 | `example/work-planner/artifacts/board.md` | Board placement taking the issue number |  |  |
| W15 | `example/work-planner/artifacts/initiative-issue-body.md` | Source departures stated in Sources field |  |  |
| W16 | `example/work-planner/artifacts/architecture-overview.md` | Overview ownership stated in its fields |  |  |
| W17 | `example/work-planner/artifacts/goal-trace.md` | Goal review returning its trace table |  |  |
| W18 | `example/work-planner/modes/revise-mode.md` | Revision checklist linking the guidelines |  |  |

## Wave 2: new operations and the technical-debt artifact

| Task | Component | Description | Depends on | Joins |
| --- | --- | --- | --- | --- |
| W19 | `example/work-planner/artifacts/epic.md` | Pull requests matched to tasks |  |  |
| W20 | `example/work-planner/artifacts/board-queue.md` | Board queue applied until it converges |  |  |
| W21 | `example/work-planner/artifacts/pull-request-body.md` | Test coverage checked against criteria |  |  |
| W22 | `example/work-planner/artifacts/work-item.md` | Work item read for its component |  |  |
| W23 | `example/work-planner/artifacts/delivery-brief.md` | Delivery brief read and reservation confirmed |  |  |
| W24 | `example/work-planner/artifacts/plan-change.md` | Plan changes settled by one operation |  |  |
| W25 | `example/work-planner/artifacts/technical-debt.md` | Technical debt classified by its artifact |  |  |
| W26 | `example/work-planner/artifacts/issue.md` | Issue completion checked by kind | W01 |  |
| W27 | `example/work-planner/artifacts/issue-body.md` | Open questions resolved by one operation | W02 |  |
| W28 | `example/work-planner/artifacts/initiative-issue-body.md` | Placeholder epic links resolved | W15 |  |
| W29 | `example/work-planner/artifacts/epic-issue-body.md` | Unplaced task row placed by one operation | W03 |  |
| W30 | `example/work-planner/artifacts/acceptance-criteria.md` | Verified criteria recorded, criteria quality checked | W15 |  |
| W31 | `example/work-planner/artifacts/board.md` | Project board ensured for a theme | W14 |  |
| W32 | `example/work-planner/artifacts/delivery-evidence.md` | Board-scoped delivery evidence read once | W05 |  |
| W33 | `example/work-planner/artifacts/pull-request.md` | Pull request bases aligned to the epic | W08 |  |
| W34 | `example/work-planner/artifacts/planning-record.md` | Planning record located by reference | W11 |  |

## Wave 3: protocols, and the residue in modes, protocols and artifacts

| Task | Component | Description | Depends on | Joins |
| --- | --- | --- | --- | --- |
| W35 | `example/work-planner/protocols/unit-hold.md` | Unit Hold protocol | W03, W11, W22 |  |
| W36 | `example/work-planner/protocols/issue-placement.md` | Issue Placement protocol | W13 |  |
| W37 | `example/work-planner/protocols/review-pull-request.md` | Review Pull Request applying operations only | W08 |  |
| W38 | `example/work-planner/artifacts/dependency-graph.md` | Dependency findings settled through plan change | W13, W24 |  |
| W39 | `example/work-planner/protocols/delivery-base-preparation.md` | Delivery Base Preparation protocol | W33 |  |
| W40 | `example/work-planner/protocols/delivery-recording.md` | Delivery Recording protocol | W19, W27, W29, W30 |  |
| W41 | `example/work-planner/protocols/epic-closure.md` | Epic Closure protocol | W30 |  |
| W42 | `example/work-planner/protocols/initiative-publication.md` | Initiative Publication protocol | W01, W02, W11, W28 |  |
| W43 | `example/work-planner/protocols/change-overview.md` | Change Overview applying operations only | W09, W10, W34 |  |
| W44 | `example/work-planner/protocols/epic-integration.md` | Epic Integration applying operations only | W08, W30 |  |
| W45 | `example/work-planner/protocols/issue-closure.md` | Issue Closure applying operations only | W26 |  |
| W46 | `example/work-planner/protocols/issue-delivery.md` | Issue Delivery applying operations only | W04, W29, W30 |  |
| W47 | `example/work-planner/artifacts/pull-request.md` | Task pull requests merged without branch updates | W33 | W53 |
| W48 | `example/work-planner/artifacts/board-delivery.md` | Board delivery reading board evidence | W32 |  |
| W49 | `example/work-planner/modes/advance-mode.md` | Advance Mode orchestrating only | W01, W20, W24, W32 |  |
| W50 | `example/work-planner/modes/hoist-mode.md` | Hoist Mode orchestrating only | W02, W12, W36, W38 |  |
| W51 | `example/work-planner/modes/propose-mode.md` | Propose Mode orchestrating only | W01, W31 |  |
| W52 | `example/work-planner/modes/standup-mode.md` | Standup Mode orchestrating only | W02, W07, W32 |  |
| W53 | `example/work-planner/protocols/task-merge.md` | Task Merge from merge to records | W41 | W47 |
| W54 | `example/work-planner/modes/align-mode.md` | Align Mode orchestrating only | W38, W39, W40 |  |
| W55 | `example/work-planner/modes/plan-mode.md` | Plan Mode orchestrating only | W17, W27, W38, W39, W42 |  |
| W56 | `example/work-planner/modes/sync-mode.md` | Sync Mode orchestrating only | W16, W31, W40, W41 |  |
| W57 | `example/work-planner/modes/deliver-mode.md` | Deliver Mode orchestrating only | W06, W21, W23, W24, W25, W32, W35, W39, W53 |  |
| W58 | `example/work-planner` | No operation or protocol left uncalled | W18, W37, W43, W44, W45, W46, W47, W48, W49, W50, W51, W52, W54, W55, W56, W57 |  |
| W59 | `example/README.md` | Worked examples quoting the current tree | W58 | W60 |
| W60 | `fixtures/usage-example` | Mode bundles and usage fixtures verified | W58 | W59 |
