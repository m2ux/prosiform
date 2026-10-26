---
prosiform:
  root: ".."
  group: "protocols"
  group-depth: 1
---
# Issue Delivery

The task and epic bodies brought to what one pull request's delivery establishes.

## Procedure

1. **Task issues.**
   For each task issue the pull request delivers:
   - Apply [Verify Selected Criteria](../artifacts/acceptance-criteria.md#verify-selected-criteria) for each criterion the task covers, with its current body, delivery findings, delivery revisions, named instruments and the project checkout.
   - Apply [Record Task Delivery](../artifacts/task-body.md#record-task-delivery) with the task JSON, pull request records, complete issue-link snapshot, delivering pull request number, returned verified criterion ids, output body file and output comment file.
   - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the repository, task issue number and returned body file.
   - Apply [Comment on Issue](../artifacts/issue.md#comment-on-issue) with the repository, task issue number and returned comment file.
2. **Epic rows.**
   Apply [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery) with the epic JSON, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches, project checkout and output body file.
   - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the returned body when it differs from the current one.
   - For each task issue its [Delivery Findings](../artifacts/epic.md#delivery-findings) name as unplaced:
     - Apply [Place Unplaced Task Row](../artifacts/epic-issue-body.md#place-unplaced-task-row) with the saved epic JSON, that task issue, the caller's allowance and change list when supplied, the pull request records, complete issue-link snapshot, task issue records, confirmed matches, project checkout and output body file.
     - Use the body and Delivery Findings it returns in the following steps; a row it leaves pending is returned to the caller with the updated change list.
3. **Epic criteria.**
   Apply [Record Verified Criteria](../artifacts/acceptance-criteria.md#record-verified-criteria) with the repository, the criteria the returned Delivery Findings name as ready to verify, the saved epic JSON and body, those findings, delivery revisions, named instruments, project checkout, output body file, pull request records and complete issue-link snapshot.
4. **Return the result.**
   Return to the caller the saved task and epic identities, each task's eligibility findings, the verified criteria with their evidence, the epic's Delivery Findings with each coverage disagreement as [Delivery Findings](../artifacts/epic.md#delivery-findings) defines it, and the updated change list.
