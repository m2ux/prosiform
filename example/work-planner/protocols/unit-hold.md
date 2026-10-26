---
prosiform:
  root: ".."
  group: "protocols"
  group-depth: 1
---
# Unit Hold

One confirmed work unit's planning record, reserved epic rows and board status, in place before its session starts.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md).

## Procedure

1. **Read the components.**
   For each of the unit's tasks, apply [Read Work Item](../artifacts/work-item.md#read-work-item) with the task id and the planning folder its epic row links, before the reservation replaces that link.
   - Retain each returned component and Test row for the caller.
   - Return a reported missing file, declaration or Test row to the caller before any hold.
2. **Add the record.**
   Apply [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record) with the record identity and folder path the [unit line](../artifacts/delivery-plan.md#report-lines) names, and a commit message file naming that folder, asking it to publish.
   - Return a publication discrepancy to the caller before any row is reserved.
3. **Reserve the rows.**
   Apply [Reserve Task Rows](../artifacts/epic-issue-body.md#reserve-task-rows) with the epic JSON, the unit's task ids, the folder identity from step 2, the planning-records base URL, the record date and an output body file.
   - Return a refused row to the caller.
   - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the repository, the epic number and the returned body file.
4. **Set the board status.**
   For each task issue of the unit, where one exists, and then its epic, apply [Update Item Status](../artifacts/board.md#update-item-status) with the selected board identity, the item identity, the current Status field and option ids, the In Progress selection and a request body file.
   - Return a discrepancy to the caller.
   - Return the record folder, the saved epic body, and the component and Test row of each task to the caller.
