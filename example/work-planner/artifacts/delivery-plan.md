---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Delivery Plan

The available units, held rows, blocked work and merge candidates for one board.

## Operations

### Plan Available Work

One delivery plan from supplied board and delivery evidence.

**Inputs:** [Board items](board.md#board-items), [Pull request records](pull-request.md#pull-request-records), [Project checkout](delivery-branches.md#project-checkout), [Epic bases](delivery-branches.md#epic-bases), [Off-board issues](#off-board-issues), [Output directory](#off-board-issues), [Record date](#branch-context)

**Outputs:** [Available work](#report-lines)

#### 1. Compute the Available Work

From `<workspace>`, compute available work using the supplied board items, pull request records, project checkout, epic-base names, resolved off-board issue files and optional record date.

- `--items` and `--prs` receive the supplied snapshots. A row's own links, which say whether its work is under way, are read from the epic body.
- `--project` is the checkout; `--bases` is its comma-separated epic-base list.
- `--others` supplies each resolved off-board issue; `--date` selects another record date.

`<epic-base-names>` is a comma-separated list of full epic-base branch names.

Omit `--others` when there are no resolved off-board issues; otherwise pass every resolved file after it. Omit `--date` to use today.

Runs as [Helper invocation](../conventions.md) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --items '<board-items-file>' --prs '<pull-request-records-file>' --project '<checkout>' --bases '<epic-base-names>' --others '<off-board-issue-file>' --date '<record-date>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --items items.json --prs prs.json --project '<checkout>' --bases i07/e00/main,i07/e00/workflows
```

#### 2. Resolve Each Unresolved Reference

Read the planner’s exit code and output. Continue with unresolved issue references; preserve unresolvable-dependency blockers in the returned plan and return any other execution error.

For each unresolved issue reference the plan returns:
- Apply [Read Tracker Issue](issue.md#read-tracker-issue) with its repository and number into a file in the output directory.
- Add the returned file to the resolved off-board issue files.

From `<workspace>`, recompute available work with every resolved off-board issue file, retaining the board items, pull requests, checkout, bases and record date.

- `--items` and `--prs` receive the supplied snapshots. A row's own links, which say whether its work is under way, are read from the epic body.
- `--project` is the checkout; `--bases` is its comma-separated epic-base list.
- `--others` supplies each resolved off-board issue; `--date` selects another record date.

`<epic-base-names>` is a comma-separated list of full epic-base branch names.

Omit `--others` when there are no resolved off-board issues; otherwise pass every resolved file after it. Omit `--date` to use today.

Runs as [Helper invocation](../conventions.md) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --items '<board-items-file>' --prs '<pull-request-records-file>' --project '<checkout>' --bases '<epic-base-names>' --others '<off-board-issue-file>' --date '<record-date>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --items items.json --prs prs.json --project '<checkout>' --bases i07/e00/main,i07/e00/workflows
```

After each recomputation, inspect its exit code and unresolved references. Repeat this step while a reference remains that no read has failed; return any other computation error. An unavailable issue stays an unresolved reference.

#### 3. Return the Available Work Plan

Return the units, holds, blockers, merge candidates and unresolved references meeting [Fields](#fields). The caller decides holds and dispatch.

## Fields

### Off-Board Issues

Resolved dependency issues outside the board, each an [issue record](issue.md#issue-record) at a local path, and the output directory holding those files.

### Work Units

A unit is one task row or tasks that name each other in Joins, as [Work Breakdown](epic-issue-body.md#work-breakdown) defines. One unit is one pull request's work. Its task ids and Descriptions determine the planning-folder identity, branch, epic base and worktree.

### Report Lines

- A `unit` line names one session's tasks, Coverage, record, branch, base and worktree. Its record is the folder's name, which is the record identity, and names the [planning-folder path](planning-record.md#record-folder) that folder takes. One base is `base i07/e00/main`; several are `bases i07/e00/main i07/e00/workflows`.
- A `hold` line names a row a session holds and the record it links.
- A `blocked` line names a free row whose dependencies are undelivered or whose joined task is unavailable.
- An `unresolvable` line names a free row carrying a `Depends on` entry nothing can resolve, and the entry as written. The row waits on no delivery, so it is told apart from a blocked one, and a run meeting one exits nonzero.
- A `merge` line names an open pull request whose test plan has passed and the epic base it targets.
- An unresolved issue reference identifies dependency evidence no read could supply.

### Branch Context

The project checkout supplies the long-lived branch names defined in [Branches](delivery-branches.md#branches). A base whose last segment is not one of those names is ignored. A supplied record date determines the planning folder's day; the default is today.
