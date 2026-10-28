---
prosiform:
  root: ".."
  group: "protocols"
  group-depth: 1
---
# Issue Closure

Fresh closure evidence assembled across an issue and its linked pull requests, and the closure it permits.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md).

## Procedure

### 1. Issue

- Apply [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue) for the issue selected by the delivery checks.
- Apply [Capture Issue Development](../artifacts/issue.md#capture-issue-development) for that issue.

### 2. Pull Requests

Apply [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state) for every captured link, across repositories and all states.

### 3. Check Delivery Completion

Apply [Check Issue Completion](../artifacts/issue.md#check-issue-completion) with the issue's kind, current JSON, complete Development snapshot, those pull request records and criterion verification evidence, adding the task's delivery result for a task and the project checkout for an epic.
- Return an incomplete or failed result to the caller before closure.

### 4. Close

Apply [Close Tracker Issue](../artifacts/issue.md#close-tracker-issue) with the issue identity, the successful completion result, issue JSON, complete Development snapshot, confirmed repository setting and those pull request records.
- On a changed link set or missing evidence, repeat from [1. Issue](#1-issue) for the same issue.
- Report any unmerged link or unmet criterion.
