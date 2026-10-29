---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Placement

A proposed destination and disposition for one orphan's work.

## Operations

### Draft Issue Placement

The placement options for one orphan, from the orphan and its candidate destinations.

**Inputs:** [Orphan](#orphan), [Candidate destinations](#candidate-destinations)

**Outputs:** [Placement options](#placement-record), [Draft bodies](#draft-bodies)

#### 1. Identify the Placement Options

Identify each destination in [Placement Record](#placement-record) that could take the orphan's work, among the candidate destinations, Leave included.

#### 2. Record Each Placement Destination

For each option, record the destination and the work it takes, meeting [Destination](#destination).

#### 3. Record Each Orphan Disposition

For each option, record the orphan's disposition, meeting [Disposition](#disposition).

#### 4. Return the Placement Options

Return the options for the caller to offer and apply, each a [placement](#placement-record) with its [draft bodies](#draft-bodies), in the order that contract states.

### Find Placement Candidates

The issue candidates and available destinations, from the repository's issues.

**Inputs:** [Repository issues](issue.md#issue-record)

**Outputs:** [Candidate issues](#candidate-issues), [Candidate destinations](#candidate-destinations)

#### 1. List the Orphan Issues

From `<workspace>`, run the orphans helper with the repository issues' JSON file as `<issues-json-file>`. Runs as [Helper invocation](../conventions.md) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/orphans.py '<issues-json-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/orphans.py issues.json
```

#### 2. Return the Placement Candidates

By the helper's exit code:
- **Nonzero.**
  - Return its error output to the caller as a blocker.
- **Zero.**
  - Return the orphans and cited standalone issues it prints as [Candidate Issues](#candidate-issues), and the open initiatives and epics it prints as [Candidate Destinations](#candidate-destinations), for the caller to investigate.

### Apply Issue Placement

The destination bodies one confirmed placement populates, as local files.

**Inputs:** [Confirmed placement](#placement-record), [Orphan](#orphan), [Destination](#destination), [Initiative body](initiative-issue-body.md#template), [Epic body](epic-issue-body.md#template), [Body paths](#draft-bodies)

**Outputs:** [Populated bodies](#draft-bodies), [Destination](#destination), [Disposition](#disposition)

#### 1. Populate the Confirmed Destination Body

Populate only the branch matching the confirmed destination, each body at its supplied path:
- **Existing task.**
  - Add the orphan's outcomes to the task criteria.
  - Add its design to Proposal.
  - When they exceed the epic's criteria, add epic criteria cited by the task row.
- **New task.**
  - Apply [Populate Epic Issue Body](epic-issue-body.md#populate-epic-issue-body) with the confirmed task scope, current epic context and body path.
  - Add the epic criteria the row's Coverage needs where the orphan's outcomes exceed the epic's, as [Destination](#destination) states.
  - Link the kept orphan's issue in the row's Task cell, as [Task Delivery](epic-issue-body.md#task-delivery) states for a task with its own issue. A subsumed orphan leaves the cell holding the row id alone until the work is planned and the row gains its work-item file.
  - Number the row where it can start.
- **New epic.**
  - Apply [Populate Epic Issue Body](epic-issue-body.md#populate-epic-issue-body).
  - Populate the covering row through [Draft Initiative Issue Body](initiative-issue-body.md#draft-initiative-issue-body), with a temporary link standing for the epic's issue until it is saved.
- **New initiative.**
  - Apply [Populate Initiative Issue Body](initiative-issue-body.md#populate-initiative-issue-body) from the orphan's scoped problem and confirmed goal.
- **Leave.**
  - Use the orphan as the destination with disposition left, changing no destination body.

#### 2. Carry Subsumed Orphan Work

For a subsumed orphan, carry its work in the destination body.
- Make each outcome a criterion of one invariant.
- Put the design in Proposal.
- Cite the orphan and any planning record in References.

#### 3. Return the Populated Placement Bodies

Return each populated [draft body](#draft-bodies), the destination, including the epic and row for a new task, and the confirmed disposition.

### Rewrite Orphan Issue

The selected layout, with the original wording preserved for readers.

**Inputs:** [Orphan](#orphan), [Destination](#destination)

**Outputs:** [Rewritten orphan](#orphan)

#### 1. Fetch the Orphan Issue Live

Fetch the body and discussion live with [Read Tracker Issue](issue.md#read-tracker-issue).
- Post the complete body word for word through [Comment on Issue](issue.md#comment-on-issue), preceded by the line in [Original Body](#original-body) and a blank line, before the body is rewritten.
- Skip the comment where the discussion already carries one, since a second hoist of the same issue would otherwise repeat it.

#### 2. Populate the Selected Orphan Body

Use the selected [Populate Task Body](task-body.md#populate-task-body), [Populate Epic Issue Body](epic-issue-body.md#populate-epic-issue-body), [Populate Initiative Issue Body](initiative-issue-body.md#populate-initiative-issue-body) or [Populate Standalone Body](standalone-body.md#populate-standalone-body) body.
- Carry evidence into Problem and design into Proposal.

#### 3. Check the Rewritten Orphan Body

Apply [Check Round of Edits](issue-body.md#check-round-of-edits) with the populated body and selected kind conditions before publishing.
- Resolve findings.
- Apply [Save Tracker Issue](issue.md#save-tracker-issue) with the validated body, title and labels.
- Return the saved identity to the caller.

### Subsume Orphan Work

The orphan closed, its work tracked by the taking issue.

**Inputs:** [Orphan](#orphan), [Destination](#destination)

**Outputs:** [Closed orphan](#orphan)

#### 1. Prepare the Subsumption Comment

Prepare the comment file naming the taking issue and task, as [Bodies](../conventions.md) states, for example `Tracked in [I07:E01](…/issues/937) W04.` The closure operation records it once.

#### 2. Close the Subsumed Orphan

Apply [Close Transferred Work](issue.md#close-transferred-work) with the orphan identity, the saved destination as its evidence and the comment file, retaining the orphan's body.
- Return the confirmed closure or blocker to the caller.

## Fields

### Orphan

The orphan: a [tracker issue](issue.md#issue-record) with its repository, number, current body and discussion, the evidence, design and work its body proposes, and any planning-record reference it carries.

### Candidate Issues

Candidates are open issues without an agent-engineering prefix. Orphans have no incoming link from an open initiative, epic or task. Cited standalone issues have such a link in prose or References; their records include labels, citing issues and any linked planning folder. An investigation cited by an epic is a candidate, its disposition meeting [Disposition](#disposition).

### Candidate Destinations

The open initiatives and epics an orphan's work could join, each with its [theme labels](../configuration.md#theme-labels) and its current [initiative body](initiative-issue-body.md#template) or [epic body](epic-issue-body.md#template).

### Placement Record

One option for an orphan: its destination, the work it takes, and the disposition the destination allows.

| Destination | Work | Issue Disposition |
| --- | --- | --- |
| Existing task | Criteria and design in a task that has its own issue | Subsumed |
| New task | A row in an existing epic, with its criteria | Kept or subsumed |
| New epic | An epic in an existing initiative | Kept or subsumed |
| New initiative | An initiative | Kept or subsumed |
| Leave | Work outside the initiative structure | Left open |

Placement options are ordered best first, the destination that most nearly holds the orphan's work leading, with Leave last.

### Destination

The selected issue or proposed work, of a kind in [Placement Record](#placement-record), with the criteria and design it takes.
- An existing-epic option identifies the row to add, with Description, criteria, Depends on and Joins, or the existing task already delivering the work.
- Leave applies when no initiative goal covers the work or it is not planned work.

### Disposition

Kept, subsumed or left, with a reason; [Placement Record](#placement-record) gives the dispositions each destination allows.
- An orphan with a planning-record reference is subsumed, with that folder cited beside the orphan in the destination.
- Otherwise the orphan is kept when its work needs its own discussion or evidence, and subsumed when its detail fits in rows, criteria and a reference.
- Work an existing criterion already states is subsumed into the issue holding that criterion, without a new row; for cited standalone work this is usually the citing issue.

### Draft Bodies

One local body file for each issue a placement changes or creates, each with its path and the issue identity it saves to, or its title and labels for a new issue, and each temporary link it holds.
- Each body meets its own kind's shape and states the result. It carries no account of how the work arrived. A source reference says what detail it holds.
- An initiative row identifies its epic issue. A task issue has its delivery link through Development.

### Original Body

The comment starts with `The body before this issue took the [I07:E01:W04] layout:` for a kept issue, or `The body before this issue took the standalone layout:` for one left in place. A blank line separates that lead from the complete original body.
