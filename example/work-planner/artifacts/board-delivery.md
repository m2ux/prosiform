---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Board Delivery

The membership, status and assignee changes that record delivery on one board.

## Operations

### Plan Board Changes

The board changes implied by supplied delivery state.

**Inputs:** [Initiative](issue.md#issue-record), [Epics](issue.md#issue-record), [Tasks](issue.md#issue-record), [Pull request records](pull-request.md#pull-request-records), [Issue-link snapshot](pull-request.md#issue-link-snapshot), [Board](board.md#board-identity), [Board fields](board.md#board-fields), [Board items](board.md#board-items), [Output directory](#change-calls), [Assignee login](board.md#assignees), [Off-board issues](issue.md#issue-record)

**Outputs:** [Change calls](#change-calls), [Missing evidence](#missing-evidence)

#### 1. Require the Board Change Link Snapshot

Require the complete pull-request issue-link snapshot; refuse the computation without it.

#### 2. Compute the Board Changes

Run [Compute Board Changes](#compute-board-changes), mapping the supplied records and board context to its parameters.

#### 3. Return the Planned Board Calls

Return the generated calls and unresolved references, meeting [Fields](#fields). The caller gathers missing evidence, applies changes and confirms them as [Write confirmation](../conventions.md) states.

### Record Epic Review

One epic's board item at In Review, recording that its delivery is complete and its review draft awaits the user's mark.

**Inputs:** [Epic](issue.md#issue-record), [Board](board.md#board-identity), [Output paths](board.md#board-files)

**Outputs:** [Epic board item](board.md#board-items)

#### 1. Read the Review Board State

Apply [Read Board State](board.md#read-board-state) for the supplied board to obtain its items and Status field.

#### 2. Read the Review Status Options

Apply [Read Board Configuration](board.md#read-board-configuration) with the board identity and output paths for the Status option ids.

#### 3. Match the Epic to Its Board Item

Match the epic's issue to its board item.
- Return an absent item as a finding and stop. The status write below needs it.

#### 4. Set the Epic Status to In Review

Apply [Update Item Status](board.md#update-item-status) with the board and item identities, the Status field and In Review option ids, and that status in its request body file, meeting [Status Changes](#status-changes).
- Confirm the write as [Write confirmation](../conventions.md) states. The item list can lag a write, so an item still showing the preceding status has the same write repeated and the item read again.

#### 5. Return the Epic Review Status

Return the confirmed status or the discrepancy left for the caller.

### Record Board Delivery

The board's status and assignees after its issues record delivery.

**Inputs:** [Initiative](issue.md#issue-record), [Epics](issue.md#issue-record), [Tasks](issue.md#issue-record), [Board](board.md#board-identity), [Output directory](#change-calls)

**Outputs:** [Board items](board.md#board-items), [Assignees](board.md#assignees)

#### 1. Read the Delivery Evidence

Read the issues and the board's delivery evidence.
- Apply [Read Tracker Issue](issue.md#read-tracker-issue) for the saved initiative, epic and task identities.
- Apply [Read Board Delivery Evidence](delivery-evidence.md#read-board-delivery-evidence) with the board identity and output directory.
- Pass the returned issue records, board snapshot, pull request records and complete issue-link snapshot to Plan Board Changes.

#### 2. Plan the Delivery Board Changes

Apply [Plan Board Changes](#plan-board-changes) with the initiative JSON, linked epic records, task issue records, pull request records, complete issue-link snapshot, board identity, board fields, board items, output directory, and assignee login.
- Fetch each unresolved issue.
- Pass the fetched files to Plan Board Changes as resolved off-board issue files.

#### 3. Run the Delivery Board Calls

Run each emitted call, including the assignee calls, which act on the issue rather than the board item.
- Apply [Read Board Configuration](board.md#read-board-configuration) with the board identity, output paths and changed item identity to confirm its current status, as [Write confirmation](../conventions.md) states.
- If that item still shows the preceding status:
  - Repeat its write.
  - Repeat the same item read. The item list can lag a write.

#### 4. Re-Read the Delivery Evidence

Read the issues and the board's delivery evidence again, as [1. Read the Delivery Evidence](#1-read-the-delivery-evidence) does.
- Apply [Plan Board Changes](#plan-board-changes) with the refreshed initiative JSON, linked epic records, task issue records, pull request records, complete issue-link snapshot, board identity, board fields, board items, output directory, assignee login, and every resolved off-board issue file.
- Stop when it emits no further call and every changed item has been confirmed. An issue added in one pass gets its status in the next.

## Fields

### Status Changes

An open initiative or epic whose criteria are all ticked is In Review. An epic with an open pull request and a criterion unticked is In Progress.

An initiative or epic with no open pull request and unticked criteria keeps Ready or Backlog, and keeps In Progress when delivery has started. In Review then becomes In Progress. One not yet on the board is added at Backlog, or at In Progress when delivery has started. Delivery does not move an initiative or epic between Ready and Backlog.

Task readiness meets [Task Eligibility](board-queue.md#task-eligibility). The caller supplies saved issue bodies and closure state.

A task gated on an [unresolvable dependency](board-queue.md#unresolvable-dependencies) keeps the Status it holds: the row waits on no delivery, so no status follows from its gate. The run names the row and the entry and exits nonzero, as every reader of that cell does.

### Change Calls

The result contains calls for issues to add, items to remove, Status to set and assignees to add or remove. Each call names its affected issue and board item, and the call files occupy one output directory. Assignees follow [Assignees](board.md#assignees).

### Missing Evidence

Unresolved issue references identify dependency records the caller must supply before a complete result. A newly added issue receives its status on a subsequent pass using refreshed items.

## Commands

### Compute Board Changes

Computes membership, Status and assignee calls from supplied delivery evidence.

**Inputs:** Initiative JSON, epic and task JSON records, pull request and complete issue-link snapshots, board identity, board fields and items, output directory, assignee login and resolved off-board issue records.

- `--epics`, `--tasks`, `--prs` and `--links` receive the related records and complete link snapshot.
- `--board`, `--fields` and `--items` identify the current board state.
- `--out` receives the call files; `--assignee` is the supplied login.
- `--others` supplies each resolved dependency issue.

Pass each epic or task JSON file as a separate argument after its corresponding flag.

Runs as [Helper invocation](../conventions.md) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/board.py '<initiative-json-file>' --epics '<epic-json-file>' --tasks '<task-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --board '<board-identity>' --fields '<board-fields-file>' --items '<board-items-file>' --out '<output-directory>' --assignee '<assignee-login>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/board.py issue-936.json --epics issue-943.json issue-937.json --tasks issue-637.json --prs prs.json --links links.json --board 'users/<owner>/projectsV2/9' --fields fields.json --items items.json --out board/ --assignee m2ux
```
