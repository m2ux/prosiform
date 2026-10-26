---
prosiform:
  root: ".."
---
# Deliver Mode

Starts the work a theme board makes available. It advances the board, merges each open pull request whose test plan has passed, stands a completed epic in review on the board, holds each available unit with a planning record, and dispatches one session per unit to plan, implement, open its pull request, merge it when its test plan has passed, hoist arising issues, and defer the technical debt its validation finds.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md) and ensure all [Outcomes](#outcomes) are met.

## Procedure

1. **Select.**
   Apply [Select Project Board](../artifacts/board.md#select-project-board) with the requested theme or board identity.
   - Use its returned owner and board number for the following steps.
2. **Advance.**
   Follow [⇉ Advance Mode](advance-mode.md) for the selected board, with the [allowance](../artifacts/plan-change.md#allowance) this run applies.
   - Continue to the fetch step only after it returns a complete applied queue.
   - Report an unavailable dependency, and a queue decision it recorded rather than asked, before dispatch. An incomplete queue means no initiative is under way, so the run has no work to offer.
   - Carry the [change list](../artifacts/plan-change.md#change-list) it returns into the report step.
3. **Fetch.**
   Apply [Read Board Delivery Evidence](../artifacts/delivery-evidence.md#read-board-delivery-evidence) with the selected owner and board number, output paths and destination snapshot files.
   - Use its board snapshot, pull request records and issue-link snapshot in the following steps.
   - Report incomplete evidence it returns, and stop.
4. **Survey.**
   Follow [Delivery Base Preparation](../protocols/delivery-base-preparation.md) with the candidate epics, their current initiative and epic bodies, all prerequisite issue and base-merge records, the project checkout, changed long-lived branches, the repository, initiative prefix and the pull request records the fetch step returned.
   - Carry each prerequisite finding and conflict it returns into the report step; an epic with a prerequisite finding has no base and offers no unit.
   - Carry each pull request awaiting a decision into the confirm step's interview.
   - Apply [Plan Available Work](../artifacts/delivery-plan.md#plan-available-work) with the board items, pull request records, project checkout, the epic bases Delivery Base Preparation returned, an output directory and the selected record date.
   - For delivery discrepancies:
     - Apply [Read Delivery Evidence](../artifacts/delivery-evidence.md#read-delivery-evidence) for the affected initiative and epics.
     - Resume the survey with its returned records.
   - Handle the returned availability findings:
     - **Held work.**
       - Carry each `hold` line to the confirm step, with the record it links and whether a session is still running.
     - **Blocked work.**
       - Report a `blocked` or `unresolvable` line, and an unresolved issue reference, without asking. Its dependencies decide when it becomes available.
   - Use the returned [Work Units](../artifacts/delivery-plan.md#work-units) as the units of confirmation and dispatch.
5. **Merge.**
   Apply [Confirm Repository Auto-Close](../artifacts/issue.md#confirm-repository-auto-close) for each repository a `merge` line names.
   - For each `merge` line, follow [⇉ Task Merge](../protocols/task-merge.md) with the pull request and epic base it names, that confirmed setting as the repository prerequisite, the passing test-plan evidence its pull request record carries, its head branch and the worktree [Task Branches](../artifacts/delivery-branches.md#task-branches) places for that branch, the repository, initiative prefix and project checkout, the epic issue its tasks belong to with its criterion ids and named instruments, the selected board identity, and output body and comment files.
   - Carry each merge, handoff, refusal, conflict, epic review and pending finding it returns into the report step.
6. **Confirm.**
   Show each `unit` line, with its tasks, coverage, record, branch, base and worktree, and each `hold` line with the record it links and whether a session is still running.
   - Name, with its units, each corpus-changing epic whose body lacks its [Corpus Audit](../artifacts/epic-issue-body.md#corpus-audit) criterion.
   - Confirm the units to dispatch, the rows to release and each pull request awaiting a decision as one [interview](../rules.md). Dispatch only the units the user confirms. No session starts until the user confirms the set of units.
   - This mode reads no clock and reclaims nothing on its own, so a row the user leaves stays held.
   - For each released row:
     - Apply [Release Task Rows](../artifacts/epic-issue-body.md#release-task-rows) with the epic JSON, the row's task ids, the user's release decision and an output body file.
     - Apply [Read Board Delivery Evidence](../artifacts/delivery-evidence.md#read-board-delivery-evidence) again.
     - Apply Plan Available Work again with its refreshed board items and pull request records, retaining the other inputs and output directory.
     - Confirm the units it returns before any of them is dispatched.
   - Settle each plan change after this step through [Settle Plan Change](../artifacts/plan-change.md#settle-plan-change) with this run's allowance and change list, so none is put to the user.
7. **Hold.**
   For each confirmed unit, before its session starts, follow [Unit Hold](../protocols/unit-hold.md) with the unit line's task ids, record identity and folder path, the epic JSON and number, the repository, the planning-records base URL, the record date, the selected board identity, and each task's and the epic's item ids with the Status field and option ids from the board snapshot.
   - Report a unit whose hold returns a missing work item, a discrepancy or a refused row, and dispatch no session for it, as [Task Delivery](../artifacts/epic-issue-body.md#task-delivery) holds require.
   - Carry each held unit's record folder, and the component and Test row of each task, to the dispatch step.
   - Retain the queue decisions returned by the completed advance step.
8. **Dispatch.**
   For each held unit:
   - Apply [Create Task Worktree](../artifacts/delivery-branches.md#create-task-worktree) with the project checkout, the worktree, branch and base the unit line names, and the prerequisite evidence Delivery Base Preparation confirmed.
   - Apply [Populate Delivery Brief](../artifacts/delivery-brief.md#populate-delivery-brief) with the confirmed unit, the components and Test rows Unit Hold returned, the record folder, worktrees, test obligations, selected board identity and this run's allowance.
   - Resolve any returned gap before dispatch.
   - Start each unit's session through the sub-agent dispatch this session provides, following [Run Delivery Session](#run-delivery-session) with the unit's brief, in the unit's worktree, with the engineering worktree in reach for the planning record. No unit's session starts any other way.
   - When this session provides no sub-agent dispatch, report that and stop before any unit begins.
   - Continue to the report step without waiting for unit completion; the dispatched session owns the implementation, debt and arising-issue work its brief carries.
9. **Report.**
   Each pull request merged, and each left open by a conflict; each epic moved to In Review; each review pull request updated; each unit dispatched, with its record, branch, worktree and the session started for it; each row left held; each blocked row and what blocks it.
   - Report the run's [change list](../artifacts/plan-change.md#change-list) as a list of its own, so each plan change this run applied, and each it held for the user, is read in one place.

### Run Delivery Session

The confirmed unit carried from its supplied brief through implementation and delivery.

1. **Read the brief.**
   Apply [Read Delivery Brief](../artifacts/delivery-brief.md#read-delivery-brief) with the supplied brief path and an output file for the epic body.
   - Use its confirmed unit, criteria, tests, branch and bases, worktree, planning-folder identity, board identity and change allowance.
   - Return each missing part, missing folder or released row it reports before changing the worktree.
2. **Plan.**
   Apply [Populate Work Item](../artifacts/work-item.md#populate-work-item) for each task with its reserved file path, scope, design, component, criteria and test requirements from the brief, so the component the plan was checked against is the one this file declares.
3. **Link the work items.**
   Apply [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record) with the planning-folder identity and path, each returned work-item file and any further file the work needs, and a commit message file, asking it to publish. The row retains its folder link while reserved.
4. **Match the tests to the criteria.**
   Apply [Check Test Coverage](../artifacts/pull-request-body.md#check-test-coverage) with each work item's test row and each criterion the unit's Coverage carries.
   - For each criterion it returns with no test, apply Populate Work Item again with that test added to the task's test requirements, then Check Test Coverage again, before implementation.
5. **Implement.**
   Deliver the work in the worktree, with every test the work item names, as [Tables](../artifacts/issue-body.md#tables) state.
   - Group the unit's rows by the component each declares, and give each group to the sub-agent dispatch this session provides when the unit has more than one group.
   - Give each sub-agent the unit's worktree, its group's work items, and the criteria those rows' Coverage names.
   - A sub-agent writes the files its work items name, runs the tests they name, and commits nothing.
   - A plan change a sub-agent meets returns to this session, which holds the allowance the brief names.
   - Write a file two groups reach — a shared test, an index, a manifest — in this session.
   - Stage and commit each returning group's own files, then run the unit's tests once every group has returned.
   - A unit of one group, and a session with no sub-agent dispatch, is delivered by this session.
6. **Open the pull request.**
   Apply [Confirm Repository Auto-Close](../artifacts/issue.md#confirm-repository-auto-close) for the repository, where the session holds no confirmed setting.
   - Apply [Populate Pull Request Body](../artifacts/pull-request-body.md#populate-pull-request-body) with the change summary, the unit's delivery scope and its validation evidence.
   - Apply [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request) with the repository, task kind, the returned body file, a title meeting [Titles](../artifacts/pull-request-body.md#titles), the unit's branch and the base [Branches](../artifacts/delivery-branches.md#branches) gives it, the unit's task issue where one exists, that confirmed setting and a link-snapshot destination.
   - Apply [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery) for the unit's tasks with the epic JSON, the pull request records and issue-link snapshot, task issue records, the matches of those tasks to the opened pull request, the unit's worktree as project checkout and an output body file.
   - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the repository, epic number and the returned body file.
7. **Merge.**
   Apply Populate Pull Request Body with the check results and the current body, following [Test Plan](../artifacts/pull-request-body.md#test-plan).
   - Apply Publish Pull Request with the pull request number and the returned body file.
   - Follow [⇉ Task Merge](../protocols/task-merge.md) with the task pull request and its epic base, the confirmed setting as the repository prerequisite, the passing test-plan evidence, the unit's worktree and branch, the repository and initiative prefix, the unit's worktree as project checkout, the epic issue with its criterion ids and named instruments, the board identity the brief names, and output body and comment files.
   - Carry a returned handoff, refusal, conflict or pending finding into the session result, and continue to the debt step.
8. **Classify and defer the debt.**
   For each item this unit's validation finds, apply [Classify Technical Debt](../artifacts/technical-debt.md#classify-technical-debt) with the item, the evidence that shows it and the criteria the unit's Coverage carries.
   - **Blocking or trivial.**
     - Fix it in this unit.
   - **Non-trivial.**
     - Follow [Hoist Arising Issue](#hoist-arising-issue) with the item and its placement as a new task in this initiative's [deferred-debt epic](../artifacts/initiative-issue-body.md#deferred-debt). Where the initiative has no such epic, the placement raises it as a new epic, carrying the criterion its initiative row covers.
   - Resume the arising-issues step with each saved placement or reported blocker.
9. **Arising issues.**
   Follow [Hoist Arising Issue](#hoist-arising-issue) for each issue that arose during delivery, after the pull request is open and epic delivery is recorded.
10. **Report the changes.**
    Apply [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record) with the planning-folder identity and path, the session's [change list](../artifacts/plan-change.md#change-list) and a commit message file, asking it to publish.
    - Return the list with the delivery session result, so the user reads each plan change this session applied and each it held.

### Hoist Arising Issue

One issue a delivery session meets, saved as a standalone issue and placed in the plan.

1. **Save the issue.**
   Apply [Populate Standalone Body](../artifacts/standalone-body.md#populate-standalone-body) with the issue's problem, design, criteria, open questions and an output path.
   - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the repository, the returned body file and its title.
2. **Place it.**
   Follow [⇉ Hoist Mode](hoist-mode.md) with the saved issue identity, the allowance the brief names, and the placement the caller names, where it names one.
3. **Record the placement.**
   Apply [Record Plan Change](../artifacts/plan-change.md#record-plan-change) with each placement Hoist Mode's returned change list marks applied or held, and the session's current list.
   - Return the saved placement or the reported blocker to the calling step.

## Outcomes

- **Available work started.**
  The user has each confirmed unit of the theme board in a session, with a planning record held for that session.
- **Parallel where the plan allows it.**
  The units offered are those of the epics planned to start together, and an epic planned for later is not offered while they run.
  Within a unit, work that can proceed together does.
- **Passed work merged.**
  Each open pull request whose test plan has passed is merged, and one a conflict blocks stays open with the conflict named.
- **Review visible on the board.**
  The user sees each completed epic in review on its theme board before being asked to mark its review ready.
- **Holds left to the user.**
  A row a session holds is released only when the user says so, and a blocked row is named with what blocks it.
- **One session for each unit.**
  Each confirmed unit has its own session, and a row another session holds is not given a second one.
- **Delivery that runs unattended.**
  Once the user has confirmed the units, each session delivers its work, places what arises and defers what it cannot carry, without a further question.
- **Plan changes applied and reported.**
  The user reads what delivery changed in the plan, and work needing an initiative is left open for them to decide.

## Guidance

- **Allowance.**
  This mode's runs, and every session they dispatch, apply each kind in [Change Kinds](../artifacts/plan-change.md#change-kinds). A change outside them is held and reported.
