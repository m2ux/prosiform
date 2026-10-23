---
metadata:
  prosiform-group: "artifacts"
  prosiform-group-depth: "2"
---
# Epic Issue Body

Populates one epic body. The body states one slice of the design and lists the tasks that deliver it.

The delivery lines this body records are defined in [Epic](epic.md).

## Operations

### *Populate* Epic Issue Body

One epic body and its local validation findings.

**Inputs:** Initiative context, epic scope, draft title and labels, criteria, proposed task rows, available pull request records and output path.

1. Populate the body from the [Template](#template) at the supplied output path.
2. Fill the epic-specific cells.
   - Each row must meet [Work Breakdown](#work-breakdown).
3. Pass the draft, initiative context and output file to [Validate Epic Body](#validate-epic-body).
4. Return the draft rows, their dependency references and the validation findings for the caller's cross-body ordering check.

### *Record* Epic Delivery

One epic body with supplied delivery matches and completed rows recorded.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches and output body file.

1. Run [Sync Epic](#sync-epic), mapping pull requests to `--prs`, links to `--links`, task issues to `--tasks`, each confirmed match to `--link` and the output file to `--fix`.
   - Row changes must meet [Task Delivery](#task-delivery) and [Work Breakdown](#work-breakdown).
2. Return the updated body and [Delivery Findings](epic.md#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.

### *Validate* Epic Body

The body's local format and field findings.

**Inputs:** Epic JSON, initiative context, current pull request records and output file.

1. Check the current body against the local [Fields](#fields), supplying initiative JSON as `--initiative` and pull requests as `--prs`.
2. Include any epic criterion no task row delivers in the findings.
3. Return the corrected body, mechanical diff and unresolved findings for the caller.

## Fields

### Template

````markdown
## Overview

{{One paragraph: what this epic delivers and why it exists within the initiative.}}

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
````

### Work Breakdown

The columns are `Task | Description | Coverage | Depends on | Joins | Done`.

- **Done.**
  A task row is complete when it is delivered, and every criterion its Coverage names is ticked.
- **Row id.**
  The row id is the task, `W01`. `W00` holds preparatory work that must land before the first real task.
- **Coverage.**
  Coverage names the epic's criteria the task must meet. Each row claims only criteria its work makes true; it cannot claim a criterion another row delivers alone or one its work cannot meet. A complete task's cell is empty.
- **Depends on.**
  A task row names the rows it depends on, never an epic. It names the row producing each output it consumes, and where the task consumes from every row of an epic that is what establishes the whole-epic reach.

### Task Delivery

- **Task ids.**
  - Every link on a task row names that row's id, and the row carries one delivery per long-lived branch its unit changes.
  - Once a pull request is open, its link replaces the planning link. A unit changing two long-lived branches links the pull request on each.
  - The task is delivered when a linked pull request has merged, or its id links a commit. A link to an open pull request does not deliver the task.
- **Tasks with their own issue.**
  - A task issue belongs to one epic. Its title carries that epic's prefix.
  - When that epic's table has no row for its id, the issue is unplaced. Once the row exists, that epic's planning manages the issue.
  - The row links the pull request, not the issue.
- **Work another issue takes.**
  It leaves the table. Its criteria go with it, or to another row that delivers them.

## Commands

### Sync Epic

Links each named task's id to a pull request naming the epic, open or merged, and ticks Done on a row once it is complete.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, task records, confirmed matches and output body file.

- A row whose id links its task issue links the pull request instead.
- A pull request whose head is an epic base is the pull request that merges that base, and is not matched to a task.
- An unmerged epic base keeps the epic open, even when every row is delivered and every criterion is ticked.

```bash
work-tracker sync '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --tasks '<task-json-file>' --link '<task-pull-request-map>' --fix '<output-body-file>'
```

**Example:**

```bash
work-tracker sync issue-943.json --prs prs.json --links links.json --tasks issue-637.json --link W01=950,W02=950 --fix fixed-943.md
```
