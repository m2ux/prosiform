---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Delivery Evidence

The pull request records and issue links that establish what an initiative's epics or a board's issues have delivered, with the findings that evidence yields.

## Operations

### Read Delivery Evidence

The pull requests and issue links that establish current delivery.

**Inputs:** [Repositories](repository-labels.md#repository), [Initiative prefix](initiative-issue-body.md#titles), [Epic issues](issue.md#issue-record), [Records path](pull-request.md#pull-request-records), [Link snapshot path](pull-request.md#issue-link-snapshot)

**Outputs:** [Pull request records](pull-request.md#pull-request-records), [Issue-link snapshot](pull-request.md#issue-link-snapshot), [Delivery findings](epic.md#delivery-findings), [Unnamed deliveries](#unnamed-deliveries)

#### 1. Fetch Pull Requests and Links

Fetch the pull requests and their links.
- Apply [Read Initiative Pull Requests](pull-request.md#read-initiative-pull-requests).
- Apply [Fetch Pull Request Issue Links](pull-request.md#fetch-pull-request-issue-links).
- Use [Access Development Links](pull-request.md#access-development-links) for the actual complete link sets.

#### 2. Inspect the Epic Delivery

Apply [Inspect Epic Delivery](epic.md#inspect-epic-delivery) with the epic JSON, pull request records and complete issue-link snapshot.
- Route the returned [Delivery Findings](epic.md#delivery-findings) to matching, verification or user decisions.
- Fetch any linked pull request absent from the input with [Read Pull Request State](pull-request.md#read-pull-request-state).
- Repeat Inspect Epic Delivery with the same epic JSON, refreshed pull request records and complete issue-link snapshot.

#### 3. Name the Unnamed Deliveries

Name each pull request whose issue links reach an epic or one of its task issues and whose title omits that epic's reference as an [unnamed delivery](#unnamed-deliveries).

#### 4. Return the Delivery Evidence

Return the current pull request records, complete issue-link snapshot, per-epic findings and unnamed deliveries to the caller, reporting incomplete evidence as a blocker.

### Read Board Delivery Evidence

The board snapshot and pull request records that establish current delivery across one board.

**Inputs:** [Board](board.md#board-identity), [Board files](board.md#board-files), [Records path](pull-request.md#pull-request-records), [Link snapshot path](pull-request.md#issue-link-snapshot)

**Outputs:** [Board snapshot](#board-snapshot), [Pull request records](pull-request.md#pull-request-records), [Issue-link snapshot](pull-request.md#issue-link-snapshot)

#### 1. Apply the Board Reads

Apply the [board reads](#run-board-reads).

#### 2. Return the Board Delivery Evidence

Return the [board snapshot](#board-snapshot), pull request records and complete issue-link snapshot to the caller, reporting incomplete evidence as a blocker.

#### Run Board Reads

##### 1. Read Board State

Apply [Read Board State](board.md#read-board-state) with the board owner and number for its items, Status field and [repositories](board.md#repositories).

##### 2. Fetch Initiative Pull Requests

Apply [Fetch All Initiative Pull Requests](pull-request.md#fetch-all-initiative-pull-requests) for each repository Read Board State returned, for the pull request records.

##### 3. Fetch Pull Request Issue Links

Apply [Fetch Pull Request Issue Links](pull-request.md#fetch-pull-request-issue-links) with the pull request records Fetch Initiative Pull Requests returned, for the complete issue-link snapshot.

##### 4. Read Board Configuration

Apply [Read Board Configuration](board.md#read-board-configuration) with the board owner and number and output paths for the board fields.

##### 5. Read Board Assignee

Apply [Read Board Assignee](board.md#read-board-assignee) for the assignee login.

## Fields

- **Pull request records.**
  The initiative's [pull request records](pull-request.md#pull-request-records): every pull request carrying its prefix, across the selected repositories, in all states.
- **Issue-link snapshot.**
  The complete set of Development links between those pull requests and the issues they deliver, read through the access that exposes them whole, as an [issue-link snapshot](pull-request.md#issue-link-snapshot).
- **Findings.** The per-epic [Delivery Findings](epic.md#delivery-findings) the evidence yields.

### Board Snapshot

The board items with their Status, the Status field, the board fields, the board's [repositories](board.md#repositories) and the assignee login, read together with the board's pull request records and issue-link snapshot. Each is a local file at its path.

### Unnamed Deliveries

A pull request whose issue links reach an epic or its task issues while its title omits that epic's reference. Each is named with the epic it reaches, for the user to confirm.

### Completeness

Evidence is complete when every linked pull request the snapshot names has a record, including one absent from the initiative list. Incomplete evidence is a blocker, not a partial result.

### Named Delivery

A pull request that delivers an epic carries that epic's reference in its title, as `[I07:E00] Purpose`. A delivery the user confirms whose title omits its epic is repaired to carry that reference.
