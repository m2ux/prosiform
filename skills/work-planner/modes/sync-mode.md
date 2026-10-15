# Sync Mode

Records delivery on an initiative, its epics, and their task issues. Each task that has a pull request is linked to that pull request, open or merged. Criteria that now hold are recorded, complete rows are marked done, complete issues are closed, and the initiative's theme board is brought up to date.

## Prerequisites

Read these files first.

- [Issue](../artifacts/issue.md)
- [Issue Body](../artifacts/issue-body.md)
- [Align Mode](align-mode.md)
- [Task Body](../artifacts/task-body.md)
- [Pull Request](../artifacts/pull-request.md)
- [Epic](../artifacts/epic.md)
- [Epic Issue Body](../artifacts/epic-issue-body.md)
- [Deliver Mode](deliver-mode.md)
- [Initiative Issue Body](../artifacts/initiative-issue-body.md)
- [Board](../artifacts/board.md)
- [Understand Mode](understand-mode.md)
- [Pull Request Body](../artifacts/pull-request-body.md)
- [Board Delivery](../artifacts/board-delivery.md)
- [Delivery Branches](../artifacts/delivery-branches.md)
- [Initiative](../artifacts/initiative.md)

## Procedure

The main path meets [Outcomes](#outcomes).

1. **Select.**
   - Select an initiative with its open epics, or the epics the user names.
   - Run [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue) for each selected issue before inspecting its Open Questions or format.
   - Use the returned current JSON and body in the following checks.
   - For an epic with Open Questions:
     - Obtain the user's decision on each question.
     - Apply confirmed resolutions through [Apply Body Corrections](../artifacts/issue-body.md#apply-body-corrections) with the epic template and field conditions.
     - Publish through [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue).
     - Fetch the saved epic.
     - Continue only when its Open Questions section is resolved; otherwise return the unresolved questions as blockers.
   - For an issue rejected by [Validate Issue Body](../artifacts/issue-body.md#validate-issue-body):
     - Run [Repair Issue Format](align-mode.md#repair-issue-format) with that issue identity, current JSON, kind template and field conditions, required related evidence and output body path.
     - When it returns, fetch the saved body again.
     - Validate that saved body before continuing to the fetch step.
     - Return a remaining format failure as a blocker.
2. **Fetch.**
   - Run [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue) for each issue, including each task issue under an epic being synced, titled as [Titles](../artifacts/task-body.md#titles) states.
   - Run [Read Delivery Evidence](#read-delivery-evidence) with the selected repositories and initiative prefix, fetched epic JSON, authenticated access and destination snapshot files.
   - Use its returned pull request records, complete issue-link snapshot and findings in the following steps.
   - Confirm the repository prerequisite for issue closure: GitHub's setting that auto-closes issues with merged linked pull requests is disabled.
   - Capture each issue's Development links.
   - Fetch linked pull requests absent from the initiative list before evaluating closure.
3. **Unnamed deliveries.**
   - When the user says work has landed but no pull request names its epic:
     - Find the pull request.
     - Confirm it with the user.
     - Give it the epic's reference, `[I07:E00] Purpose`, with [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request).
     - Run [Read Initiative Pull Requests](../artifacts/pull-request.md#read-initiative-pull-requests) again.
     - Run [Fetch Pull Request Issue Links](../artifacts/pull-request.md#fetch-pull-request-issue-links) again.
4. **Match pull requests to tasks.**
   - Run [Inspect Epic Delivery](../artifacts/epic.md#inspect-epic-delivery) for each epic.
   - Use the unmatched and in-flight results defined in [Delivery Findings](../artifacts/epic.md#delivery-findings).
   - Read its changes and description against the tasks' Descriptions.
   - Name the tasks it works on: one task, or tasks that name each other in Joins.
   - Put any match that is not clear to the user.
5. **Sync each task issue.**
   - For a task delivered by a merged pull request, run [Verify Selected Criteria](#verify-selected-criteria) with its current body, selected criteria, delivery evidence, revisions and named instruments.
   - Run [Record Task Delivery](../artifacts/task-body.md#record-task-delivery) with the task JSON, pull request records, complete issue-link snapshot, delivering pull request number, returned verified criterion ids and output body path.
   - Publish the returned body through [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) before closure.
   - Record the pull request on it with [Comment on Issue](../artifacts/issue.md#comment-on-issue): `Delivered by #950.`
   - [Close Delivered Issue](#close-delivered-issue) when it reports closable.
6. **Sync each epic.**
   Run [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery), linking every match from the match step, open or merged, with the task issues. Linking a pull request replaces the planning-record link on that task.
   - **Conflict.** Put it to the user.
   - **Unmatched.** Match them as in the match step.
   - **In flight.** Match them as in the match step.
   - **Draft.**
     - Open it as a draft review pull request.
     - Leave the epic open until the user marks the draft ready.
   - **Unmerged.** The close step opens or merges that pull request.
   - **References.**
     Bring the body up to the merges with [Maintain Review Pull Request](#maintain-review-pull-request).
   - **Uncited.**
     - Set the link with [Link Pull Request to Issue](../artifacts/pull-request.md#link-pull-request-to-issue).
     - Run [Fetch Pull Request Issue Links](../artifacts/pull-request.md#fetch-pull-request-issue-links) again.
   - **Note.** Link the pull request as in the match step.
   - **Unplaced.**
     - Draft the missing task row against [Work Breakdown](../artifacts/epic-issue-body.md#work-breakdown).
     - Confirm it with the user; an unanswered placement stays pending.
     - Apply the confirmed row through [Revise Epic Rows](../artifacts/epic-issue-body.md#revise-epic-rows).
     - Publish through [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue).
     - Repeat Record Epic Delivery with the saved epic and refreshed task records. An unanswered placement stays pending.
   - **Open questions.**
     - Return to the select step for this epic.
     - Resolve the questions there.
     - Fetch the saved body before repeating Record Epic Delivery.
   - **Ticked early.** Untick them, or link the missing delivery.
   - **Disagreement.**
     Continue recording links, verified criteria and Done despite the reported coverage disagreement.
   After applying the returned findings, repeat Record Epic Delivery with the revised epic body and refreshed delivery records, retaining the complete issue-link snapshot and output body path. Recording the epic's delivery is finished when unmatched, in flight, uncited, note, and unplaced are clear, apart from a pull request the user leaves unmatched.
7. **Verify.**
   - Run [Verify Selected Criteria](#verify-selected-criteria) for the criteria reported ready to verify, supplying the current issue body, delivery findings, relevant delivery revisions and named instruments.
   - Retain the returned verified criterion ids and evidence for the tick step.
   - For an unresolved epic criterion requiring further work:
     - Follow [Plan Gap Task](align-mode.md#plan-gap-task) with the current epic JSON and body, delivered task row, criterion ids, findings, delivery records, complete issue-link snapshot, delivery revisions, named instruments and output body path.
     - Resume with its recorded disposition; a criterion that cannot be confirmed stays unticked.
8. **Tick.**
   Tick the confirmed criteria with [Tick Verified Criteria](#tick-verified-criteria). It ticks Done as [Tables](../artifacts/issue-body.md#tables) and [Work Breakdown](../artifacts/epic-issue-body.md#work-breakdown) state.
9. **Patch.**
   Patch each changed body from its output body file with [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue).
10. **Close.**
    - When [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery) reports an epic base unmerged and names no open pull request, open it as a draft review pull request and leave the epic open. The user marks the draft ready when the epic is complete.
    - For each open epic pull request:
      - Follow [Integrate Epic Delivery](deliver-mode.md#integrate-epic-delivery) with the epic identity and body, review identity, base worktree and target, current delivery records, complete issue-link snapshot and criterion verification evidence.
      - Report a draft waiting for the user.
    - Fetch the pull requests again after merging.
    - Re-run [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery).
    - [Close Delivered Issue](#close-delivered-issue) each epic the re-run reports closable.
11. **Sync the initiative.**
    - Run [Record Initiative Delivery](../artifacts/initiative-issue-body.md#record-initiative-delivery), with the epic JSON fetched after closing. An epic row is delivered when its issue is closed as completed, and Done is ticked on it as [Work Breakdown](../artifacts/initiative-issue-body.md#work-breakdown) states.
    - For returned criteria ready to verify:
      - Run [Verify Selected Criteria](#verify-selected-criteria) with their ids, current initiative body, delivery findings, delivery revisions and named instruments.
      - Pass returned verified ids to [Tick Verified Criteria](#tick-verified-criteria) with the initiative JSON, every linked epic record and output body file.
      - Report the remaining findings as pending.
    - [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) the initiative from its output body file when a tick changed it, so the board sync reads every criterion ticked.
    - [Close Delivered Issue](#close-delivered-issue) the initiative when it reports closable.
12. **Sync the board.**
    - Select the initiative's theme board.
    - Run [Copy Project Board](../artifacts/board.md#copy-project-board) if it is absent.
    - Follow [Record Board Delivery](#record-board-delivery) after the issue bodies and closures are saved.
13. **Explain each change entering review.**
    - For each task or epic newly confirmed In Review by the board step:
      - Run [Understand Mode](understand-mode.md) with the task's open pull request or each epic review pull request, one run per base.
      - Complete each overview before continuing; an initiative has no overview of its own. An issue already In Review when the sync began keeps the overview it has: the pull request it explains is the one already reviewed. A reviewer meets the overview on the pull request it explains.
14. **Report.**
    - Return saved delivery results and unresolved findings to the caller, or present them to the user for a direct request.
    - Report queue decisions unevaluated by this run.
    Report per issue: tasks linked, criteria ticked, rows marked done, criteria left unticked and why, conflicts, test plan disagreements, what was closed, each board and assignee change, and each overview written. What the report names about criteria is [Coverage Reports](../artifacts/issue-body.md#coverage-reports).

### Read Delivery Evidence

The pull requests and issue links that establish current delivery.

**Inputs:** Selected repositories and initiative prefix, current epic JSON, authenticated access and destination files for pull request records and the complete issue-link snapshot.

1. **Fetch.**
   - Run [Read Initiative Pull Requests](../artifacts/pull-request.md#read-initiative-pull-requests).
   - Run [Fetch Pull Request Issue Links](../artifacts/pull-request.md#fetch-pull-request-issue-links).
   - Use [Access Development Links](../artifacts/pull-request.md#access-development-links) for the actual complete link sets.
2. **Match.**
   Run [Inspect Epic Delivery](../artifacts/epic.md#inspect-epic-delivery) with the epic JSON, pull request records and complete issue-link snapshot.
   - Route the returned [Delivery Findings](../artifacts/epic.md#delivery-findings) to matching, verification or user decisions.
   - Fetch any linked pull request absent from the input with [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state).
   - Repeat Inspect Epic Delivery with the same epic JSON, refreshed pull request records and complete issue-link snapshot.
3. **Repair a name.**
   - When the user confirms a delivery whose title omits its epic:
     - Run [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request) with the confirmed epic prefix and purpose.
     - Repeat the fetch and match steps with the saved title before returning.
   - Return the current pull request records, complete issue-link snapshot and per-epic findings to the caller, reporting incomplete evidence as a blocker.

### Record Issue Delivery

The issue bodies associated with a pull request's delivery.

**Inputs:** Delivered unit, current task and epic JSON, pull request records, complete issue-link snapshot, confirmed matches, verification evidence, project checkout and output body paths.

1. **Task issues.**
   - Verify each criterion with its named instrument before passing its id to [Record Task Delivery](../artifacts/task-body.md#record-task-delivery).
   - Supply the issue JSON, pull request records, complete issue-link snapshot, delivering pull request number, verified criterion ids, and output body file.
2. **Epic rows.**
   - Run [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery) with the epic JSON, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches, project checkout, and output body file.
   - Interpret the returned [Delivery Findings](../artifacts/epic.md#delivery-findings).

   - Run [Populate Epic Issue Body](../artifacts/epic-issue-body.md#populate-epic-issue-body) for a confirmed unplaced task.
   - Repeat Record Epic Delivery with the refreshed epic JSON and the same pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches, project checkout, and output body file.
3. **Coverage agreement.**
   - Report the coverage disagreements returned in [Delivery Findings](../artifacts/epic.md#delivery-findings), including each pull request and row.
   - Continue recording links, verified criteria and Done.
4. **Criteria and bodies.**
   - For the epic, run [Tick Verified Criteria](#tick-verified-criteria) with its current JSON, pull request records, complete issue-link snapshot, verified criterion ids and output body path.
   - Publish that returned epic body and each task body returned by Record Task Delivery through [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue).
   - Return the saved identities and findings to the caller.

### Maintain Review Pull Request

The draft pull request and body for one epic base's delivered changes.

**Inputs:** Epic identity and JSON, epic base and long-lived target, current task-merge records, complete issue-link snapshot, optional review identity and output body path.

1. **Find.**
   - Use the review number in the supplied delivery findings.
   - When it is absent:
     - Run [Locate Review Pull Request](../artifacts/pull-request.md#locate-review-pull-request) with the repository and epic base as head.
     - Use its returned number or absence result.
   - Fetch an existing review through [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state).
2. **Populate.**
   Pass the existing body when present and the actual task merges into the base to [Populate Review Body](../artifacts/pull-request-body.md#populate-review-body).
3. **Publish.**
   - When the first task merges, a draft is reported or an unmerged base has no review:
     - Pass the returned file to [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request), supplying its number for an existing review. The epic stays open; the user marks the draft ready when the epic is complete.
4. **Confirm.**
   - Run [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state) for the published review.
   - Compare its complete body with the published file.
   - Run [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery) with the current epic and refreshed review and task-merge records.
   - Return its cited-versus-actual merge findings with the review identity. The session recording each task merge owns this update.

### Record Task Merge

The task and epic records after one confirmed task merge.

**Inputs:** Confirmed task merge result, delivered unit, current task and epic records, issue-link snapshot, criterion evidence, base worktree and target, initiative context and output paths.

1. **Read and record.**
   - Follow [Read Delivery Evidence](#read-delivery-evidence).
   - Run [Record Issue Delivery](#record-issue-delivery) for the delivered unit.
   - Close an eligible task issue through [Close Delivered Issue](#close-delivered-issue).
2. **Review.**
   Follow [Maintain Review Pull Request](#maintain-review-pull-request) for the affected epic base.
3. **Complete when ready.**
   - When every task and criterion is complete:
     - Follow [Integrate Epic Delivery](deliver-mode.md#integrate-epic-delivery) with the epic identity and body, review identity, base worktree and target, current delivery records, complete issue-link snapshot and criterion verification evidence. A draft or unmet merge condition stays pending.
4. **Close the epic.**
   - After every epic base has merged:
     - Refresh the evidence.
     - Run [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery) with the epic JSON, pull request records, complete issue-link snapshot, task issue records, project checkout, and output body file.
     - Follow [Close Delivered Issue](#close-delivered-issue) when eligible.
     - Run [Record Initiative Delivery](../artifacts/initiative-issue-body.md#record-initiative-delivery) with the current initiative and every linked epic record. Initiative completion does not gate an epic merge. A task merge alone does not sync the initiative or board.

### Record Board Delivery

The board's status and assignees after its issues record delivery.

**Inputs:** Saved initiative, epic and task identities, theme board identity, board and delivery snapshot paths, output directory and resolved dependency records.

1. **Read.**
   - Run [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue) for the saved initiative, epic and task identities.
   - Run [Read Board State](../artifacts/board.md#read-board-state) for the selected board.
   - Run [Fetch All Initiative Pull Requests](../artifacts/pull-request.md#fetch-all-initiative-pull-requests) for its repositories.
   - Run [Fetch Pull Request Issue Links](../artifacts/pull-request.md#fetch-pull-request-issue-links) for those records.
   - Run [Read Board Configuration](../artifacts/board.md#read-board-configuration) with the board and output paths.
   - Run [Read Board Assignee](../artifacts/board.md#read-board-assignee) for the assignment login.
   - Pass these returned snapshots to Plan Board Changes.
2. **Plan.**
   - Run [Plan Board Changes](../artifacts/board-delivery.md#plan-board-changes) with the initiative JSON, linked epic records, task issue records, pull request records, complete issue-link snapshot, board identity, board fields, board items, output directory, and assignee login.
   - Fetch each unresolved issue.
   - Pass the fetched files to Plan Board Changes as resolved off-board issue files.
3. **Write.**
   - Run each emitted call.
   - Run [Read Board Configuration](../artifacts/board.md#read-board-configuration) with the board identity, output paths and changed item identity to confirm its current status.
   - If that item still shows the preceding status:
     - Repeat its write.
     - Repeat the same item read. The item list can lag a write.
4. **Repeat.**
   - Fetch the issues and items again.
   - Run [Plan Board Changes](../artifacts/board-delivery.md#plan-board-changes) with the refreshed initiative JSON, linked epic records, task issue records, pull request records, complete issue-link snapshot, board identity, board fields, board items, output directory, assignee login, and every resolved off-board issue file.
   - Stop when it emits no further call and every changed item has been confirmed. An issue added in one pass gets its status in the next.

### Close Delivered Issue

Fresh closure evidence assembled across the issue and its linked pull requests.

**Inputs:** Issue identity and kind, successful delivery findings, current body and criterion evidence, related delivery records, repository prerequisite and snapshot output paths.

1. **Issue.**
   - Run [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue) for the issue selected by the delivery checks.
   - Run [Capture Issue Development](../artifacts/issue.md#capture-issue-development) for that issue.
2. **Pull requests.**
   - Run [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state) for every captured link, across repositories and all states.
   - Use a fresh destination file so an earlier snapshot cannot supply membership.
3. **Check delivery completion.**
   - For an epic:
     - Run [Read Delivery Branches](../artifacts/delivery-branches.md#read-delivery-branches) for the complete expected bases.
     - Run [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state) for their merge evidence.
     - Run [Check Epic Completion](../artifacts/epic.md#check-epic-completion) with the current epic JSON, delivery records, complete issue-link snapshot, criterion verification evidence and those base records.
   - For an initiative:
     - Refresh every linked epic through [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue).
     - Run [Check Initiative Completion](../artifacts/initiative.md#check-initiative-completion) with the current initiative JSON, all linked epic records, criterion verification evidence and captured Development-link and pull-request records. A task retains its task delivery result.
   - Return any incomplete or failed result before closure.
4. **Close.**
   - Pass the successful normal delivery result, issue JSON, complete Development snapshot, confirmed repository setting and fresh pull request records to [Close Tracker Issue](../artifacts/issue.md#close-tracker-issue).
   - If the operation reports a changed link set or missing evidence:
     - Refresh those inputs.
     - Repeat the completion check before trying again.
   - Report any unmerged link or unmet criterion.

### Verify Selected Criteria

The verification evidence for a supplied set of criteria whose delivery is ready.

**Inputs:** Current issue body, selected criterion ids, current delivery findings, delivery revisions and the instruments named by those criteria.

1. **Check the evidence.**
   - Confirm the supplied delivery findings establish readiness for each selected criterion.
   - Return an undelivered or unreadable dependency as a blocker for that criterion.
2. **Verify each criterion.**
   - Run its named instrument on the branch or branches the delivering pull requests merged into.
   - Record the result against the tested revisions, meeting [Coverage Reports](../artifacts/issue-body.md#coverage-reports). A failed, unavailable or inconclusive instrument leaves the criterion unverified.
3. **Return the findings.**
   - Return verified criterion ids with their evidence and each unresolved criterion with what is missing.
   - Leave body publication and further planning to the caller.

### Tick Verified Criteria

The confirmed criteria and completed rows recorded in an epic or initiative body.

**Inputs:** Current issue JSON, verified criterion ids, destination body file, and either pull request and link snapshots for an epic or every linked epic's current JSON for an initiative.

1. **Record the criteria.**
   - For an epic, run [Record Epic Criteria](../artifacts/epic-issue-body.md#record-epic-criteria) with the issue JSON, pull request records, complete issue-link snapshot, verified criterion ids and output body file.
   - For an initiative, run [Record Initiative Criteria](../artifacts/initiative-issue-body.md#record-initiative-criteria) with the issue JSON, every linked epic record, verified criterion ids and output body file.
2. **Return the body.**
   Return the resulting body and any criteria refused as not ready to verify. The artifact operations return the updated bodies for publication.

## Outcomes

- **Delivery recorded.**
  The user has each landed task tied to the pull request that delivered it, and has what now holds recorded on the initiative and its epics.
- **Complete work closed.**
  Work that is complete is closed.
- **The board is current.**
  The theme board shows where the initiative and its epics stand, including what a reviewer can take up.
- **A change entering review is explained.**
  Each task and epic that enters review has an overview on the pull request a reviewer reads.
- **The queue stays undecided.**
  A sync on its own leaves the choice of what to start next undecided.
