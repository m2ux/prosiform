---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Initiative Issue Body

Populates one initiative body. The body states the goal as criteria and lists the epics that deliver them.

## Operations

### Populate Initiative Issue Body

One initiative body and its local validation findings.

**Inputs:** [Scoped proposal](proposal-body.md#template), [Goal clauses](goal-trace.md#goal-clauses), [Requirement sources](#sources), [Epic summaries](#work-breakdown), [Output body file](#body-file)

**Outputs:** [Initiative body](#body-file), [Format findings](issue-body.md#format-findings)

#### 1. Draft the Initiative Body

Populate the body through [Draft Initiative Issue Body](#draft-initiative-issue-body).

#### 2. Check the Initiative Round of Edits

Apply [Check Round of Edits](issue-body.md#check-round-of-edits).

#### 3. Return the Populated Initiative Body

Return the populated body and its local format findings to the caller.

### Draft Initiative Issue Body

One initiative body, scoped to one proposal.

**Inputs:** [Scoped proposal](proposal-body.md#template), [Goal clauses](goal-trace.md#goal-clauses), [Requirement sources](#sources), [Epic summaries](#work-breakdown), [Output body file](#body-file)

**Outputs:** [Initiative body](#body-file)

#### 1. Copy the Initiative Template

Populate the body from the [Template](#template) into a local file at the supplied output path.
- That file must be the source for every later edit.
- All populated fields must meet [Fields](#fields).

#### 2. Derive Problem and Non-Goals

Derive the Problem and Non-Goals from the proposal this initiative is scoped to.
- The Problem must meet [Problem and Proposal](issue-body.md#problem-and-proposal).
- Each Non-Goal must meet [Non-Goals](#non-goals).

#### 3. Write Initiative Acceptance Criteria First

Write the acceptance criteria before the Work Breakdown, so each row's Coverage can cite them.
- Each criterion must come from a confirmed clause and meet [Initiative Acceptance Criteria](#initiative-acceptance-criteria).
- The criteria must come from the requirements sources the proposal references. Where the proposal references none, they must come from the proposal's body alone.

#### 4. Write the Shared Initiative Table

Populate the shared table through [Write Issue Table](issue-body.md#write-issue-table).

#### 5. Fill the Initiative-Specific Cells

Fill the initiative-specific cells.
- Each row must meet [Work Breakdown](#work-breakdown).
- An item a test cannot observe must stay named as [Coverage Reports](issue-body.md#coverage-reports) define.

### Resolve Placeholder Links

Saved issue identities in the links an initiative and its epics carry before their issues exist.

**Inputs:** [Initiative body](#body-file), [Epic bodies](epic-issue-body.md#body-file), [Saved issues](issue.md#issue-record)

**Outputs:** [Initiative body](#body-file), [Epic bodies](epic-issue-body.md#body-file), [Unresolved links](#temporary-links)

#### 1. Replace Temporary Issue Links

Replace every temporary link in the initiative and epic body files with the saved issue identity it stands for.
- Each epic row of the initiative must meet [Work Breakdown](#work-breakdown).
- Each row reference in an epic must meet the epic's [Work Breakdown](epic-issue-body.md#work-breakdown).

#### 2. Confirm No Temporary Link Remains

Confirm no temporary link remains in any of those files.

#### 3. Return the Rewritten Body Files

Return the rewritten body files and each temporary link left unresolved, with the file that holds it.

### Record Initiative Delivery

One initiative body with its epic delivery recorded.

**Inputs:** [Initiative issue](issue.md#issue-record), [Epic issues](issue.md#issue-record), [Output body file](#body-file)

**Outputs:** [Initiative body](#body-file), [Delivery findings](initiative.md#delivery-findings)

#### 1. Run Sync Initiative

From `<workspace>`, update the supplied initiative JSON with every linked epic’s current record as `--epics`, adding `--fix` when an output body is requested.

- It takes every linked epic's current JSON. Delivery findings follow [Delivery State](initiative.md#delivery-state).

Pass every epic JSON file as a separate argument after `--epics`. Omit `--fix` when no output body is requested.

Runs as [Helper invocation](../conventions.md#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<initiative-json-file>' --epics '<epic-json-file>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-936.json --epics issue-943.json issue-937.json
```

#### 2. Return the Initiative Delivery Findings

Read the helper’s result as [Helper result](../conventions.md#helper-result) states, retaining its reported findings or refused criteria.

Return the body and [Delivery Findings](initiative.md#delivery-findings) from the supplied initiative and epic records. Delivery eligibility follows [Delivery State](initiative.md#delivery-state).

### Record Initiative Criteria

Verified criteria and completed rows in one initiative body.

**Inputs:** [Initiative issue](issue.md#issue-record), [Epic issues](issue.md#issue-record), [Verified criteria](#initiative-acceptance-criteria), [Output body file](#body-file)

**Outputs:** [Initiative body](#body-file), [Refused criteria](acceptance-criteria.md#unverified-criteria)

#### 1. Run Tick Initiative Criteria

From `<workspace>`, update the initiative JSON with linked epic records as `--epics`, verified criterion ids as `--tick` and output body file as `--fix`. Refuse criteria not ready to verify.

Pass every epic JSON file as a separate argument after `--epics`. `<criterion-ids>` is a comma-separated list of verified criterion ids.

Runs as [Helper invocation](../conventions.md#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<initiative-json-file>' --epics '<epic-json-file>' --tick '<criterion-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-936.json --epics issue-943.json issue-937.json --tick AC2 --fix fixed-936.md
```

#### 2. Return the Initiative Body and Refused Criteria

Read the helper’s result as [Helper result](../conventions.md#helper-result) states, retaining its reported findings or refused criteria.

Return the body and refused criteria. Complete rows receive Done ticks.

### Validate Initiative Body

The body's local format and field findings.

**Inputs:** [Initiative issue](issue.md#issue-record), [Epic issues](issue.md#issue-record), [Source evidence](#source-evidence), [Output body file](#body-file)

**Outputs:** [Initiative body](#body-file), [Validation findings](issue-body.md#format-findings)

#### 1. Validate the Initiative Issue Body

Apply [Validate Issue Body](issue-body.md#validate-issue-body) with the current body, local [Fields](#fields), supplied related evidence and output file, supplying each linked epic as `--epic`.

#### 2. Title the Initiative Row

Use its current title for the initiative row.

#### 3. Report Excluded Names and Departures

Include excluded names in Problem and Proposal and criterion/source departures in the findings.

#### 4. Return the Validated Initiative Body

Return the corrected body, mechanical diff and unresolved findings for the caller.

### Read Requirement Sources

The requirements evidence used to validate an initiative's criteria.

**Inputs:** [Initiative references](#references), [Source files](#source-evidence)

**Outputs:** [Source evidence](#source-evidence)

#### 1. Read Local Requirement Sources

Read each local source at its checkout path.

#### 2. Fetch Pinned GitHub Sources

For a pinned GitHub blob, fetch its content from the repository checkout using the repository owner and name, source path, pinned revision and destination file. URL-encode the path and revision for the request.

```bash
gh api 'repos/<owner>/<repository>/contents/<source-path>?ref=<revision>' --jq .content | base64 -d > '<source-file>'
```

**Example:**

```bash
gh api 'repos/m2ux/workflow-server/contents/docs/spec.md?ref=4a217fe6' --jq .content | base64 -d > source-R1.md
```

#### 3. Fetch Other Source URLs

Read each pinned-source command’s result as [Command result](../conventions.md#command-result) states. Carry a failed or empty response into the unreadable-source findings below.

Fetch other URLs through the harness's web access.

#### 4. Record Unreadable Sources

Record an unreadable or empty source as a [Sources](#sources) finding; its criteria remain unevaluated.

#### 5. Return the Requirement Source Contents

Return each source's contents and identity with those findings.

## Fields

### Body File

A local Markdown file at a given path holding one initiative body that meets [Template](#template).

### Temporary Links

Each placeholder for an unsaved initiative or epic issue, with the body file containing it and the intended issue identity.

### Source Evidence

Each marked [source](#sources), its identity and contents, the local file path holding those contents, and any unreadable or empty-source finding.

### Template

````markdown
## Overview

{{One paragraph: what the initiative achieves, stated as the end state. Name the goal the reviews will test against.}}

## Problem

{{One sentence on the friction, then one bullet per facet. Each bullet opens with a bold statement, and its body is on the next line.}}

- **{{Facet}}.**
  {{The evidence.}}

## Proposal

- **{{Move}}.**
  {{What is done, within two lines.}}

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/{{OWNER}}/{{REPO}}/issues/{{EPIC_ISSUE}}) | {{The epic's title name, the part before the colon}} | AC{{n}}, AC{{m}} | {{Earlier epic}} | |

## Acceptance Criteria

- [ ] **AC1.** {{One invariant. It is specific, measurable, achievable, relevant, and time-bound. It carries no stale count. It names no initiative, epic, task, or issue. It states what the initiative achieves as a whole, and it ends by naming its instrument.}}

## Non-Goals

- {{One succinct sentence on what this initiative does not do. It names no initiative, epic, task or issue, and no owner.}}

## References

- **R1.** [{{Title}}]({{URL}}) — {{What the reader finds there.}}
- **R2.** **Source.** [{{Title}}]({{URL}}) — {{The requirements this initiative's criteria answer to.}}
````

### Titles

- The title is `[I07] Name: Subtitle`.
- Labels are the initiative [kind label](../configuration.md#kind-labels) and one [theme label](../configuration.md#theme-labels).
- `I` is the initiative number. Initiatives count from `00`.

### Problem

- A Problem meets [Problem and Proposal](issue-body.md#problem-and-proposal).

### Proposal

- A Proposal states the design, as [Problem and Proposal](issue-body.md#problem-and-proposal) defines.
- A Proposal names no epic, task, or acceptance criterion of its own initiative.

### Work Breakdown

The columns are `Epic | Description | Coverage | Depends on | Done`. The table has no Joins column.

- The body meets [Breakdown Prose](issue-body.md#breakdown-prose).
- An epic row's id is the epic, linked to its issue: `[E01](…/issues/937)`.
- An epic row's Description is the epic's title name, and its Coverage names the initiative criteria the epic serves.
- An epic row is complete when its issue is closed as completed.
- Depends on names epics only. A cell that names a task fails. Name a prerequisite epic only when every task or joined unit in the dependent epic requires every task in that prerequisite epic, directly or through its dependencies. The consumed output and the work producing it establish that requirement. Dependencies on selected tasks remain in the task tables. An edge another named whole-epic prerequisite already implies is omitted.
- An initiative dependency that only some tasks need, or that requires only part of its prerequisite epic, is overbroad. The output and its producing tasks establish the edge.
- An epic depending on a later epic is a backward reference.
- Epic numbering meets [Numbering](issue-body.md#numbering).

### Initiative Acceptance Criteria

An initiative criterion meets the [shared acceptance criteria](issue-body.md#shared-acceptance-criteria) and [Requirement Characteristics](../references/requirement-characteristics.md), and:

- **No counts.**
  An initiative criterion carries no counts or figures, which go stale: it measures against a named baseline or check ("against the baseline", "as the budget test measures it"). A figure stays only where it is the criterion's own target, such as a bound it holds to.
- **SMART.**
  Each initiative criterion is specific about what holds, measurable by a named check or baseline, achievable by the epics that cite it, and relevant, tracing to a clause and to the Problem. It is time-bound by a release tag or another named milestone outside the initiative's own work, where one exists, and otherwise by the epics that cite it.
- **Local.**
  An initiative criterion names no initiative, epic, task or issue, and is solution-agnostic. Coverage cells link epics to criteria. One that holds only through another initiative's work is restated as what this initiative achieves, or it is dropped.
- **Whole.**
  An initiative criterion states what the initiative achieves as a whole. One that restates a single epic's criterion is a duplicate: it is raised to what the epics achieve together, or left to the epic.
- **Verified.**
  - An initiative criterion ends by naming its instrument. Which instruments keep a criterion is [Verifiable](issue-body.md#verifiable).
  - An automated test is an end-to-end walk through the real server, a smoke run of an agent against a live server, a live check on a deployed host, or a guard, fixture suite or check that continuous integration runs. The walk, smoke run or live check is preferred where the criterion is about what a run does.
  - A named test that does not exist yet is work the plan holds: a task in the epic whose subject it tests, or a discrete test-infrastructure epic when the tests serve several criteria. That epic's row cites the criteria its tests verify.

### Non-Goals

- One succinct sentence each on what the initiative does not do, naming no initiative, epic, task or issue, and no owner.

### References

- A proposal-derived initiative identifies its originating proposal in References with the proposal's exact title and issue URL, labelled as the originating proposal.
- A reference the criteria answer to carries **Source.** after its label: `- **R1.** **Source.** [Title](url) — what it binds`. An unmarked reference is background, and binds no criterion. What a marked one requires of the criteria is [Sources](#sources).
- A cross-initiative overlap is recorded in References. An approved edit to another initiative's issue stays minimal.

### Sources

A marked source in References is a document the initiative's criteria answer to. The criteria are aligned with it in both directions.

- A criterion that misstates or contradicts a marked source fails the [Correct](../references/requirement-characteristics.md#individual) characteristic.
- A requirement a marked source states that no criterion makes true, and no Non-Goal excludes, is a gap.
- A departure from a marked source is corrected in the criterion, unless a Non-Goal records it.
- An epic is aligned against its initiative's marked sources, through the initiative criteria its row covers.
- A marked source that cannot be read leaves its criteria unaligned until it is read.

### Deferred Debt

A final epic of the initiative holds the debt that initiative's delivery defers. Its title name is `Deferred Debt` and its subtitle names the clear-up it takes; it carries its initiative's theme label and `tech-debt`, and it is raised when the initiative defers its first item. The initiative carries this criterion, which the epic's row covers:

```markdown
- [ ] **ACn.** The technical debt this initiative's delivery defers is fixed, as the Done column of its final epic's Work Breakdown shows.
```

- **It is the initiative's last epic.**
  Its number follows every other epic of the initiative, so the epics in flight are planned and delivered ahead of it and the clear-up competes with none of them.
- **A deferred item is a task row.**
  Each row covers the criterion stating what fixing that item makes true, and those statements are the epic's criteria.
- **It takes the debt its own delivery defers.**
  Debt a unit of this epic finds in resolving its row becomes a further row of the epic, so the clear-up absorbs what fixing it uncovers.
- **It delivers like any other epic.**
  It takes its bases from the long-lived branches its rows change, carries the [corpus audit](epic-issue-body.md#corpus-audit) criterion where those rows change workflow definitions, and remains open until every delivery base has merged and its completion conditions hold.
- **The initiative stays open while it stands.**
  Its row is undelivered and its criterion unticked until the epic closes.

### Breakdown Prose

Work Breakdown contains its table. Explanatory prose belongs in Proposal. The body does not narrate execution order or how the tables work; Depends on carries the order.
