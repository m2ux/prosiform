---
prosiform:
  root: ".."
  group: "protocols"
  group-depth: 1
---
# Task Merge

What the task, epic, board and initiative records become after one task pull request merges.

## Procedure

1. **Merge.**
   Apply [Merge Task Pull Requests](../artifacts/pull-request.md#merge-task-pull-requests) with the task pull request identity, its epic base, the repository prerequisite and the passing test-plan evidence.
   - Return a handoff for human approval to the caller.
   - On a refusal:
     - Apply [Update Task Branch](../artifacts/delivery-branches.md#update-task-branch) with the task worktree, task branch and epic base.
     - Return a failed update to the caller.
     - Apply Merge Task Pull Requests again with the same inputs, returning a second refusal to the caller.
2. **Read and record.**
   Apply [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue) for the epic and each task issue the merged pull request delivers.
   - Apply [Read Delivery Evidence](../artifacts/delivery-evidence.md#read-delivery-evidence) with the repository and initiative prefix, the epic's current JSON, authenticated access and destination snapshot files.
   - Follow [Issue Delivery](issue-delivery.md) with the merged pull request, the task issue records of the tasks it delivers, the epic JSON, the returned pull request records and complete issue-link snapshot, those task-to-pull-request matches, project checkout, named instruments and output body and comment files.
   - Follow [Issue Closure](issue-closure.md) for each task issue whose delivery result it returns as eligible, with the confirmed repository setting.
3. **Review.**
   Follow [Review Pull Request](review-pull-request.md) for the affected epic base, with the epic's Delivery Findings, the epic's issue and the repository setting confirmed for the session.
4. **Close when complete.**
   When the epic's [Delivery Findings](../artifacts/epic.md#delivery-findings) name an epic base unmerged:
   - Apply [Record Epic Review](../artifacts/board-delivery.md#record-epic-review) with the epic identity, the supplied board identity and output paths.
   - Report an absent board item, and continue.
   - Follow [Epic Closure](epic-closure.md) with the epic identity and body, its Delivery Findings, review identity, repository and initiative prefix, project checkout, current delivery records, complete issue-link snapshot, confirmed repository setting, criterion verification evidence and named instruments.
   - Return its pending findings and result to the caller.
