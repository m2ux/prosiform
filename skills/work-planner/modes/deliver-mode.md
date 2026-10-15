# Deliver Mode

Starts the work a theme board makes available. It advances the board, merges each open pull request whose test plan has passed, holds each available unit with a planning record, and dispatches one session per unit to plan, implement, open its pull request, merge it when its test plan has passed, hoist arising issues, and defer the technical debt its validation finds.

## Prerequisites

Read these files first.

- [Board](../artifacts/board.md)
- [Advance Mode](advance-mode.md)
- [Pull Request](../artifacts/pull-request.md)
- [Epic](../artifacts/epic.md)
- [Delivery Branches](../artifacts/delivery-branches.md)
- [Delivery Plan](../artifacts/delivery-plan.md)
- [Issue](../artifacts/issue.md)
- [Sync Mode](sync-mode.md)
- [Guidelines](../guidelines.md)
- [Epic Issue Body](../artifacts/epic-issue-body.md)
- [Planning Record](../artifacts/planning-record.md)
- [Delivery Brief](../artifacts/delivery-brief.md)
- [Hoist Mode](hoist-mode.md)
- [Initiative Issue Body](../artifacts/initiative-issue-body.md)
- [Work Item](../artifacts/work-item.md)
- [Pull Request Body](../artifacts/pull-request-body.md)
- [Issue Body](../artifacts/issue-body.md)
- [Understand Mode](understand-mode.md)

## Procedure

The main path meets [Outcomes](#outcomes).

1. **Select.**
   Run [Select Project Board](../artifacts/board.md#select-project-board) with the requested theme or board identity. Use its returned owner and board number for the following steps.
2. **Advance.**
   Run [Advance Mode](advance-mode.md) for the selected board. Continue to the fetch step only after it returns a complete applied queue; report a pending decision or unavailable dependency before dispatch.
3. **Fetch.**
   Run [Read Board State](../artifacts/board.md#read-board-state) with the selected board identity to obtain its current items and Status field.
   Run [Fetch All Initiative Pull Requests](../artifacts/pull-request.md#fetch-all-initiative-pull-requests) for each selected board repository, then [Fetch Pull Request Issue Links](../artifacts/pull-request.md#fetch-pull-request-issue-links) with those records. Use both snapshots in Plan Available Work.
   - Run [Read Board Configuration](../artifacts/board.md#read-board-configuration).
   - Run [Read Board Assignee](../artifacts/board.md#read-board-assignee) for the assignee.
4. **Survey.**
   Run [Check Epic Prerequisites](../artifacts/epic.md#check-epic-prerequisites) for each candidate epic with its current initiative and epic bodies and all prerequisite issue and base-merge records, then pass its confirmed result to [Prepare Delivery Bases](../artifacts/delivery-branches.md#prepare-delivery-bases).
   Read the project branches and each epic's bases through [Read Delivery Branches](../artifacts/delivery-branches.md#read-delivery-branches). Call [Plan Available Work](../artifacts/delivery-plan.md#plan-available-work) with the board items, pull requests, complete issue-link snapshot, project checkout, epic bases and selected record date. Resolve any missing issue through [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue), then repeat Plan Available Work with every resolved off-board issue while retaining the other inputs. For delivery discrepancies, run [Read Delivery Evidence](sync-mode.md#read-delivery-evidence) for the affected initiative and epics, then resume the survey with its returned records.
   - **Held work.**
     Put each `hold` line to the user as an [Interview](../guidelines.md#modes) before any unit is dispatched, with the record it links and whether a session is still running. The user releases it or leaves it. A released row goes through [Release Task Rows](../artifacts/epic-issue-body.md#release-task-rows) and [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue), and [Plan Available Work](../artifacts/delivery-plan.md#plan-available-work) runs again with refreshed board items, pull request records, complete issue-link snapshot, project checkout, epic-base names, every resolved off-board issue file, and the record date when supplied. A held row is released only on the user's word. This mode reads no clock and reclaims nothing on its own.
   - **Blocked work.**
     A `blocked` line is reported, not asked. Its dependencies decide when it becomes available.
   - **One unit.**
     Use the returned [Work Units](../artifacts/delivery-plan.md#work-units) as the units of confirmation and dispatch.
5. **Merge.**
   Follow [Merge Task Pull Requests](#merge-task-pull-requests) for each `merge` line, then [Record Task Merge](sync-mode.md#record-task-merge) for each confirmed merge result.
6. **Confirm.**
   Show each `unit` line, with its tasks, coverage, record folder, branch, base and worktree, and confirm the set as an [Interview](../guidelines.md#modes). Dispatch only the units the user confirms. No session starts until the user confirms the set of units.
7. **Hold.**
   For each confirmed unit, before its session starts:
   - Add its record with [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record), named as the `unit` line gives it, and commit and push the engineering worktree.
   - Run [Reserve Task Rows](../artifacts/epic-issue-body.md#reserve-task-rows) for the unit's tasks and [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the body it writes.
   - Set each task issue of the unit, where one exists, to In Progress with [Update Item Status](../artifacts/board.md#update-item-status), and its epic with it. Retain the queue decisions returned by the completed advance step.
   - A unit's record exists, its row carries that record's link, and the body is patched, before its session starts. A session is never dispatched for a row another one holds.
   - A held row stays held while its session plans and implements. The pull request's link replaces the record's link, which frees the row.
8. **Dispatch.**
   Confirm each corpus-changing epic has its [Corpus Audit](../artifacts/epic-issue-body.md#corpus-audit) criterion and dispatch that final row as its own unit.
   For each held unit:
   - Run [Create Task Worktree](../artifacts/delivery-branches.md#create-task-worktree). Call [Populate Delivery Brief](../artifacts/delivery-brief.md#populate-delivery-brief) with the confirmed unit, reserved folder, worktrees, test obligations and [Run Delivery Session](#run-delivery-session) as the supplied execution procedure. Resolve any returned gap before dispatch.
   - The agent running this mode starts each unit through the sub-agent dispatch of the session it was called from, and that dispatch is the only way a unit's session starts.
   - When that session provides no sub-agent dispatch, this mode reports that and stops before any unit begins.
   - The sub-agent works in the unit's worktree, reads the brief, and has the engineering worktree in reach for the planning record.
   - Leave the dispatched session running its Run Delivery Session procedure. The calling mode continues to the report step without waiting for unit completion; the dispatched session owns the implementation, debt and arising-issue work below.
   - A unit works on the branch [Plan Available Work](../artifacts/delivery-plan.md#plan-available-work) names, cut from the epic base, as the [Work Breakdown Guide](../artifacts/delivery-branches.md#branches) defines.
   - Raise issues arising from one work item as standalone issues. Once its pull request is open and its epic delivery is recorded, run [Hoist Mode](hoist-mode.md) for those issue identities, then resume the delivery session with their placement results.
   - Technical debt a unit finds while validating its work — running its tests, auditing the definitions it changed, reviewing its pull request — is classified, and the classification decides where it is fixed.
     - **Blocking.**
       The unit's own criteria cannot be verified without it, so the unit fixes it, whatever its size.
     - **Trivial.**
       It blocks nothing and needs no work item of its own, so the unit fixes it.
     - **Non-trivial.**
       It blocks nothing and would warrant a work item of its own. The unit defers it to this initiative's [deferred-debt epic](../artifacts/initiative-issue-body.md#deferred-debt), and the epic in hand keeps the scope it was planned with.
     - The session classifies each item and puts it to the user as an [Interview](../guidelines.md#modes), its classification the recommended answer, before the fix or the deferral.
9. **Report.**
   Each pull request merged, and each left open by a conflict; each review pull request updated; each unit dispatched, with its record, branch, worktree and the session started for it; each row left held; each blocked row and what blocks it.

### Run Delivery Session

The confirmed unit carried from its supplied brief through implementation and delivery.

**Inputs:** Published delivery brief, confirmed unit, reserved planning folder, task and epic identities, worktrees and selected branches.

1. **Read the brief.**
   Read the supplied [Delivery Brief](../artifacts/delivery-brief.md). Use its confirmed unit, criteria, tests, selected branch and bases, worktree and planning-folder identity. Return missing context before starting.
2. **Confirm the reservation.**
   Confirm the supplied reserved folder exists and its rows remain held for this session before changing its worktree.
3. **Plan.**
   Call [Populate Work Item](../artifacts/work-item.md#populate-work-item) for each task with its reserved file path, scope, design, criteria and test requirements from the confirmed delivery brief. Add any further file the work needs, as [Layout](../artifacts/planning-record.md#layout) describes.
4. **Link the work items.**
   Register each returned work-item file through [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record). The row retains its folder link while reserved. Commit and push the engineering worktree.
5. **Match the tests to the criteria.**
   Check the returned work item's test row against each criterion the unit's Coverage carries and [Test Coverage](../artifacts/pull-request-body.md#test-coverage). Resolve a missing test before implementation.
6. **Implement.**
   Deliver the work in the worktree, with every test the work item names, as [Tables](../artifacts/issue-body.md#tables) state.
7. **Open the pull request.**
   Open it with [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request), so the title, the base, the Test Plan, and the issue links meet [Titles](../artifacts/pull-request-body.md#titles), [Branches](../artifacts/delivery-branches.md#branches), [Test Coverage](../artifacts/pull-request-body.md#test-coverage), and [Issue Links](../artifacts/pull-request.md#issue-links). Then run [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery) for the unit's tasks and [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue).
8. **Merge.**
   Record check results with [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request), following [Test Plan](../artifacts/pull-request-body.md#test-plan), then follow [Merge Task Pull Requests](#merge-task-pull-requests) for the task pull request. On a confirmed merge, run [Record Task Merge](sync-mode.md#record-task-merge) with that merge result and the unit's current task and epic evidence. Resume the defer step when recording returns; a merge or recording blocker remains explicit.
9. **Defer.**
   Confirm each item with the user. Create a confirmed deferred item as a standalone issue through [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue), then run [Hoist Mode](hoist-mode.md) with that issue identity and its confirmed placement as a new task in this initiative's [deferred-debt epic](../artifacts/initiative-issue-body.md#deferred-debt). Resume the arising-issues step with its saved placement or reported blocker.
10. **Arising issues.**
    Create each issue that arose during delivery as a standalone issue with [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue), with no agent-engineering prefix. Run [Hoist Mode](hoist-mode.md) with those new issue identities after the pull request is open and epic delivery is recorded. Return each placement or pending user decision with the delivery session result.

### Merge Task Pull Requests

Merges each open task pull request whose test plan has passed, on a delivery run that finds it and in the session that opened it.

**Inputs:** Task pull request identities, current test results, epic-base and task worktrees, target branches, repository prerequisite and evidence output paths.

1. **Check.**
   Confirm the repository prerequisite in [Close Tracker Issue](../artifacts/issue.md#close-tracker-issue) and the task pull request's epic base. The base carries no review requirement of its own; where one applies, [Merge Delivery Pull Request](../artifacts/pull-request.md#merge-delivery-pull-request) governs.
2. **Update and merge.**
   Run [Update Epic Base](../artifacts/delivery-branches.md#update-epic-base), fetch readiness with [Fetch Merge Readiness](#fetch-merge-readiness) for the task pull request and its epic base, then [Merge Delivery Pull Request](../artifacts/pull-request.md#merge-delivery-pull-request) with delivery kind task, the verified head, target requirements, repository prerequisite and passing evidence, without further confirmation. Stop on a handoff for human approval. If the merge is refused, run [Update Task Branch](../artifacts/delivery-branches.md#update-task-branch), repeat Fetch Merge Readiness for the updated task head, then retry Merge Delivery Pull Request once with that verified evidence. A conflict or repeated refusal leaves the pull request open with the blocker reported.
3. **Confirm.**
   Run [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state) to confirm the merged state, head, base and merge commit. Return that result to the caller.

### Integrate Epic Delivery

Coordinates current branch, epic and pull-request evidence for one epic-base integration.

**Inputs:** Epic identity and current body, review pull request identity, epic-base worktree and target, current delivery records, complete issue-link snapshot and criterion verification evidence.

1. **Prepare the evidence.**
   Confirm the repository prerequisite in [Close Tracker Issue](../artifacts/issue.md#close-tracker-issue). Run [Maintain Review Pull Request](sync-mode.md#maintain-review-pull-request) with the actual task merges, then run [Understand Mode](understand-mode.md) with the review pull request identity. Resume with its published overview so the complete review body cites the task merges and carries that overview. Read the pull request through [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state); require the user to have marked the draft ready, and leave a draft waiting for that decision. Confirm its head is the epic base and its target is the corresponding long-lived branch.
2. **Refresh and validate.**
   Run [Update Epic Base](../artifacts/delivery-branches.md#update-epic-base), obtain current criterion verification for the updated result and refresh the delivery records. Call [Check Epic Readiness](../artifacts/epic.md#check-epic-readiness) with the current epic, delivery records, complete issue-link snapshot and that verification evidence. When the branch content changes, repeat Maintain Review Pull Request with the current task merges and Understand Mode with the same pull request identity and updated head before checking merge readiness. Follow [Fetch Merge Readiness](#fetch-merge-readiness) for the exact current head and target. A conflict, failed or pending check, unmet epic condition or incomplete evidence leaves integration blocked.
3. **Merge or hand off.**
   Pass the confirmed epic readiness, verified head, target requirements, repository prerequisite and passing evidence to [Merge Delivery Pull Request](../artifacts/pull-request.md#merge-delivery-pull-request) with delivery kind epic, without asking for further confirmation. Return its handoff when a human reviewer must merge. A changed head requires fresh verification; a merge refusal returns to the readiness checks, and a repeated refusal is reported without retrying.
4. **Confirm the result.**
   Run [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state) to confirm the merged state, verified head, target and merge commit. Return the result or blocker; draft and blocked pull requests remain open.

### Fetch Merge Readiness

The current pull request's readiness against its target requirements and head checks.

**Inputs:** Repository, pull request number, target branch and evidence output paths.

1. **Read the head.**
   Run [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state) with the pull request identity and destination `epic-pr.json`. Retain the literal head SHA and target branch for the evidence calls.
2. **Read target requirements.**
   Call [Read Target Requirements](../artifacts/delivery-branches.md#read-target-requirements) with the repository, target and protection/rules output paths. Carry any unresolved requirement into the readiness result.
3. **Read head evidence.**
   Call [Read Head Evidence](../artifacts/pull-request.md#read-head-evidence) with the exact head SHA and check/status output paths. Request reviews through [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state) with the pull request identity and reviews output path. A missing or pending check, blocked merge state or unmet required review leaves readiness unresolved.
4. **Confirm the head.**
   Run [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state) again with the same identity and destination. Compare its head with the retained SHA; a changed head requires fresh evidence. Return the verified head, target requirements and readiness result, including unresolved conditions.

## Outcomes

- **Available work started.**
  The user has each confirmed unit of the theme board in a session, with a planning record held for that session.
- **Passed work merged.**
  Each open pull request whose test plan has passed is merged, and one a conflict blocks stays open with the conflict named.
- **Holds left to the user.**
  A row a session holds is released only when the user says so, and a blocked row is named with what blocks it.
- **One session for each unit.**
  Each confirmed unit has its own session, and a row another session holds is not given a second one.
- **Debt and arising issues decided.**
  Technical debt the unit's validation finds is fixed or deferred on the user's word, and issues that arise during delivery are placed where the user directs.
