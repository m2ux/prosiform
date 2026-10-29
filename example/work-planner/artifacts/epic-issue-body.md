---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Epic Issue Body

Populates one epic body. The body states one slice of the design and lists the tasks that deliver it.

## Operations

### Populate Epic Issue Body

One epic body and its local validation findings.

**Inputs:** [Initiative issue](issue.md#issue-record), [Epic scope](#epic-scope), [Pull request records](pull-request.md#pull-request-records), [Corpus branch](delivery-branches.md#branches), [Output body file](#body-file)

**Outputs:** [Epic body](#body-file), [Draft rows](#work-breakdown), [Validation findings](issue-body.md#format-findings), [Unresolved links](initiative-issue-body.md#temporary-links)

#### 1. Draft the Epic Body

Populate the body from the [Template](#template) at the supplied output path.
- Every section must meet [Fields](#fields).
- Shared content must meet the common [body conditions](issue-body.md#fields).

#### 2. Write the Shared Epic Table

Populate the shared table through [Write Issue Table](issue-body.md#write-issue-table).

#### 3. Fill the Epic-Specific Cells

Fill the epic-specific cells.
- Each row must meet [Work Breakdown](#work-breakdown).

#### 4. Build the Epic Body Snapshot

Apply [Build Body Snapshot](issue-body.md#build-body-snapshot) with the draft body, title, labels and existing issue JSON when present.

#### 5. Validate the Epic Draft

Pass that snapshot, initiative context, available pull request records, corpus branch and output file to [Validate Epic Body](#validate-epic-body).

#### 6. Identify Unresolved Epic Links

Identify unresolved publication links separately; they remain pending until tracker identities exist.

#### 7. Return the Epic Draft Rows

Return the draft rows, their dependency references and the validation findings for the caller's cross-body ordering check.

### Record Epic Delivery

One epic body with supplied delivery matches and completed rows recorded.

**Inputs:** [Epic issue](issue.md#issue-record), [Pull request records](pull-request.md#pull-request-records), [Issue-link snapshot](pull-request.md#issue-link-snapshot), [Task issues](issue.md#issue-record), [Task matches](epic.md#task-matches), [Project checkout](delivery-branches.md#project-checkout), [Output body file](#body-file)

**Outputs:** [Epic body](#body-file), [Delivery findings](epic.md#delivery-findings)

#### 1. Run Sync Epic

From `<workspace>`, update the supplied epic JSON, mapping pull requests to `--prs`, links to `--links`, task issues to `--tasks`, each confirmed match to `--link`, the checkout to `--project` and the output body file to `--fix`.

- A row whose id links its task issue links the pull request instead.
- A pull request whose head is an epic base is the pull request that merges that base, and is not matched to a task.
- An unmerged epic base keeps the epic open, even when every row is delivered and every criterion is ticked.
- `--project` is a checkout of the project. Without the long-lived branch names, an epic that would otherwise be closable is not.
- `--link` names each task id and the pull request number it links. `--tasks` is the task issues. `--links` is the pull requests' Development-linked issues. `--fix` is the body written with the Done ticks.

`<task-pull-request-map>` is a comma-separated list of `<task-id>=<pull-request-number>` pairs. Pass each task JSON file as a separate argument after `--tasks`.

Runs as [Helper invocation](../conventions.md#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --tasks '<task-json-file>' --link '<task-pull-request-map>' --project '<checkout>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json --tasks issue-637.json --link W01=950,W02=950 --project '<checkout>' --fix fixed-943.md
```

- Omit `--tasks` when no row has its own task issue; otherwise supply each task issue's record.
- Row changes must meet [Task Delivery](#task-delivery) and [Work Breakdown](#work-breakdown).

#### 2. Return the Epic Delivery Findings

Read the helper’s result as [Helper result](../conventions.md#helper-result) states, retaining its reported findings or refused criteria.

Return the updated body and [Delivery Findings](epic.md#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.

### Record Epic Criteria

Verified criteria and completed rows in one epic body.

**Inputs:** [Epic issue](issue.md#issue-record), [Pull request records](pull-request.md#pull-request-records), [Issue-link snapshot](pull-request.md#issue-link-snapshot), [Verified criteria](#acceptance-criteria), [Output body file](#body-file)

**Outputs:** [Epic body](#body-file), [Refused criteria](acceptance-criteria.md#unverified-criteria)

#### 1. Run Tick Epic Criteria

From `<workspace>`, update the epic JSON with records as `--prs`, snapshot as `--links`, verified criterion ids as `--tick` and output body file as `--fix`. Refuse criteria not ready to verify.

`<criterion-ids>` is a comma-separated list of verified criterion ids.

Runs as [Helper invocation](../conventions.md#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --tick '<criterion-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json --tick AC1,AC3 --fix fixed-943.md
```

#### 2. Return the Epic Body and Refused Criteria

Read the helper’s result as [Helper result](../conventions.md#helper-result) states, retaining its reported findings or refused criteria.

Return the body and refused criteria. Complete rows receive Done ticks.

### Reserve Task Rows

Task rows held for one confirmed delivery session.

**Inputs:** [Epic issue](issue.md#issue-record), [Task ids](#task-delivery), [Planning folder](planning-record.md#layout), [Records base URL](../configuration.md#engineering-branch), [Record date](planning-record.md#header), [Output body file](#body-file)

**Outputs:** [Epic body](#body-file)

#### 1. Check the Rows to Reserve

Require the caller's confirmed unit and existing planning folder. Refuse a row already held or linked to a pull request or commit.

#### 2. Run Reserve Row

From `<workspace>`, reserve the confirmed task ids using the epic as `--epic`, ids as `--reserve`, supplied records base URL as `--records`, record date as `--date` and output body file as `--fix`.

- `--records` is the URL of the planning records folder, needed when no row id in the epic links a record.
- The caller supplies the planned folder identity; `--date` is the day it is opened.

`<task-ids>` is a comma-separated list of task ids; `<records-base-url>` is the URL of the [records folder](../configuration.md#engineering-branch) on the engineering branch.

Runs as [Helper invocation](../conventions.md#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic '<epic-json-file>' --reserve '<task-ids>' --records '<records-base-url>' --date '<record-date>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic issue-943.json --reserve W01,W02 --records 'https://github.com/<owner>/<repo>/tree/engineering/artifacts/planning' --fix fixed-943.md
```

#### 3. Return the Reserved Epic Body

Read the helper’s result as [Helper result](../conventions.md#helper-result) states, retaining its reported findings or refused criteria.

Return the body with the folder as each row's single link, meeting [Task Delivery](#task-delivery).

### Release Task Rows

Held task rows returned to their work-item links.

**Inputs:** [Epic issue](issue.md#issue-record), [Task ids](#task-delivery), [Release decision](#release-decision), [Output body file](#body-file)

**Outputs:** [Saved epic issue](issue.md#issue-record)

#### 1. Check the Rows to Release

Require the user's explicit decision releasing the hold, and refuse any row that is not held.

#### 2. Run Release Row

From `<workspace>`, release the authorized held task ids using the epic as `--epic`, ids as `--release` and output body file as `--fix`.

- The file is the task id in lowercase within that folder, as [Task ids](#task-delivery) defines.

`<task-ids>` is a comma-separated list of task ids.

Runs as [Helper invocation](../conventions.md#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic '<epic-json-file>' --release '<task-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic issue-943.json --release W01 --fix fixed-943.md
```

#### 3. Publish the Released Epic Body

Read the helper’s result as [Helper result](../conventions.md#helper-result) states, retaining its reported findings or refused criteria.

Publish the returned body through [Save Tracker Issue](issue.md#save-tracker-issue).

#### 4. Return the Saved Released Body

Return the saved body with each task id linked to its lowercase work-item file inside the reserved folder, meeting [Task Delivery](#task-delivery).

### Validate Epic Body

The body's local format and field findings.

**Inputs:** [Epic issue](issue.md#issue-record), [Initiative issue](issue.md#issue-record), [Pull request records](pull-request.md#pull-request-records), [Corpus branch](delivery-branches.md#branches), [Output body file](#body-file)

**Outputs:** [Epic body](#body-file), [Validation findings](issue-body.md#format-findings)

#### 1. Validate the Epic Issue Body

Apply [Validate Issue Body](issue-body.md#validate-issue-body) with the current body, local [Fields](#fields), supplied related evidence and output file, supplying initiative JSON as `--initiative`, current pull request records as `--prs` and corpus branch as `--corpus`.

#### 2. Read Epic Pull Request Reach

Read reach from each epic pull request's base, through an epic base or initiative branch. Without both pull requests and the corpus branch, reach is unevaluable.

#### 3. Report Corpus Audit and Coverage Gaps

Include a missing [Corpus Audit](#corpus-audit) criterion on a corpus-changing epic and any epic criterion no task row delivers in the findings.

#### 4. Return the Validated Epic Body

Return the corrected body, mechanical diff and unresolved findings for the caller.

### Revise Epic Rows

One epic body with confirmed task-grain and coverage corrections.

**Inputs:** [Epic body](#body-file), [Row changes](#work-breakdown), [Field findings](issue-body.md#field-findings), [Dependency references](#work-breakdown), [Output body file](#body-file)

**Outputs:** [Epic body](#body-file), [Numbering changes](dependency-graph.md#numbering-map), [Dependency changes](#work-breakdown)

#### 1. Apply the Confirmed Row Changes

Apply the confirmed row changes through [Populate Epic Issue Body](#populate-epic-issue-body), preserving unrelated content.
- Description, Coverage, Depends on, Joins and task grain must meet [Work Breakdown](#work-breakdown).
- Split a task exceeding the allowed criterion grain into the confirmed tasks.

#### 2. Return the Revised Epic Body

Return the revised body and any cross-body numbering or dependency changes for the caller.

### Plan Gap Task

The agreed disposition of criteria a delivered row left unmet.

**Inputs:** [Epic issue](issue.md#issue-record), [Delivered task row](#work-breakdown), [Unmet criteria](#acceptance-criteria), [Pull request records](pull-request.md#pull-request-records), [Issue-link snapshot](pull-request.md#issue-link-snapshot), [Output body file](#body-file)

**Outputs:** [Saved epic issue](issue.md#issue-record), [Gap disposition](#gap-disposition)

#### 1. Present Unmet Epic Criteria

Present each unmet criterion and its missing evidence, read from the current epic issue, to the user.
- Return the criteria the user confirms already hold to the caller for verification and ticking. The delivered task retains them.
- Record an unanswered decision as pending.
- If no criteria need further work, return the pending findings to the caller.
- Continue to [2. Draft the Gap Task](#2-draft-the-gap-task) with only the criteria the user confirms need further work.

#### 2. Draft the Gap Task

Draft a further task for the criteria selected for further work, meeting [Work Breakdown](#work-breakdown).
- Confirm the draft with the user.
- On acceptance, apply [Revise Epic Rows](#revise-epic-rows) with the further row and the criteria it adopts from the delivered task's Coverage.
- Return an unanswered draft as pending without continuing to [3. Record the Revised Epic Delivery](#3-record-the-revised-epic-delivery).

#### 3. Record the Revised Epic Delivery

Apply [Record Epic Delivery](#record-epic-delivery) with the revised epic and the supplied delivery evidence.
- Publish the returned body through [Save Tracker Issue](issue.md#save-tracker-issue).
- Return the saved row and criterion disposition to the caller. Done follows [Tables](issue-body.md#tables).

### Place Unplaced Task Row

One epic body given the row its table lacks for a task issue of the epic.

**Inputs:** [Epic issue](issue.md#issue-record), [Unplaced task issue](issue.md#issue-record), [Allowance](plan-change.md#allowance), [Change list](plan-change.md#change-list), [Pull request records](pull-request.md#pull-request-records), [Issue-link snapshot](pull-request.md#issue-link-snapshot), [Task issues](issue.md#issue-record), [Task matches](epic.md#task-matches), [Project checkout](delivery-branches.md#project-checkout), [Output body file](#body-file)

**Outputs:** [Saved epic issue](issue.md#issue-record), [Epic body](#body-file), [Delivery findings](epic.md#delivery-findings), [Change list](plan-change.md#change-list)

#### 1. Draft the Unplaced Task Row

Draft the task issue's row, meeting [Work Breakdown](#work-breakdown).

#### 2. Settle the Row Placement

Apply [Settle Plan Change](plan-change.md#settle-plan-change) with the drafted row as a task creation, the task issue as its subject, the drafted row as the recommended option, the epic and task issue identities, the supplied allowance and the change list.
- Return a row left held, unanswered or declined to the caller as pending, with the updated change list, without continuing to [3. Revise Epic Rows with the Placed Row](#3-revise-epic-rows-with-the-placed-row).

#### 3. Revise Epic Rows with the Placed Row

Apply [Revise Epic Rows](#revise-epic-rows) with the row as applied.

#### 4. Save the Revised Epic Issue

Publish the returned body through [Save Tracker Issue](issue.md#save-tracker-issue).

#### 5. Re-Record the Epic Delivery

Apply [Record Epic Delivery](#record-epic-delivery) again with the saved epic JSON and refreshed task issue records, retaining the pull request records, complete issue-link snapshot, confirmed matches, project checkout and output body file.

#### 6. Return the Recorded Epic Body

Return the recorded body, its [Delivery Findings](epic.md#delivery-findings) and the change list to the caller.

## Fields

### Template

````markdown
## Overview

{{One paragraph: what this epic delivers and why it exists within the initiative.}}

## Problem

{{The friction as it is now. Bullets for distinct facets, sub-bullets for several items.}}

## Proposal

{{The design, in bullets or paragraphs, each opening with a bold statement, and its body on the next line.}}

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W01 | {{What the task delivers, at most eight words}} | AC{{n}}, AC{{m}} | {{Earlier task in this epic, [Exx:Wyy](…) or [Exx](…) in an earlier epic, or #issue}} | {{Tasks that can land in the same pull request}} | |

## Acceptance Criteria

- [ ] **AC1.** {{An end state of one invariant. It ends by naming its instrument.}}

## Open Questions

- {{An undecided point the epic cannot start without, with a recommendation in the planning record. Resolve every one before the first task starts, then delete the section.}}

## References

- **R1.** [Planning record]({{PLANNING_RECORD_URL}}) — {{What the reader finds there.}}
````

### Titles

- The title is `[I07:E00] Name: Subtitle`. Its prefix matches its row in the initiative table.
- Labels are the epic [kind label](../configuration.md#kind-labels) and its initiative's [theme label](../configuration.md#theme-labels).
- `E` is the epic within its initiative. Epics count from `00`.
- The prefix separates levels with colons, then a short name, a colon, and a subtitle: `[I07:E06] Reliability Evaluation: Briefs, Measures and the Thresholds That Define Reliable`.

### Proposal

- A boundary with a sibling epic is plain language.

### Work Breakdown

New tasks exist as epic rows with their details, discussion and evidence in the epic and planning record. Planning creates no separate task issues. Existing issues hoisted into an epic retain their records and row links when new tasks are planned.

The columns are `Task | Description | Coverage | Depends on | Joins | Done`.

- The body meets [Breakdown Prose](issue-body.md#breakdown-prose).

- **Done.**
  A task row is complete when it is delivered, and every criterion its Coverage names is ticked.
- **Row id.**
  The row id is the task, `W01`. `W00` holds preparatory work that must land before the first real task.
- **Description.**
  Each detail beyond the phrase is a criterion stating one invariant.
- **Coverage.**
  Coverage names the epic's criteria the task must meet. Each row claims only criteria its work makes true; it cannot claim a criterion another row delivers alone or one its work cannot meet. A complete task's cell is empty.
- **Depends on.**
  A task row names the rows it depends on. An earlier task in the epic (`W03`, `W04–W09`), a row of an earlier epic (`[E01:W02](…)`), or something outside the initiative (`#750`, `[I05:E00:W02](…)`).
  - A task row names rows, never an epic. It names the row producing each output it consumes (`[E01:W01](…), [E01:W02](…)`), and where the task consumes from every row of an epic that is what establishes the whole-epic reach.
  - Cross-epic dependencies name rows before any issue of the epic is created. Both tables exist, and each edge names the row that produces what the dependent row consumes.
  - A dependency listed twice or already implied by another in the cell is unsound. A task that measures, extends or consumes another task's output depends on it, even when the prose does not say so.
- **Task grain.**
  - A task is one pull request's worth of work.
  - A criterion a merged pull request left unticked belongs to a further task. The further task depends on the delivered task, and its Coverage is that criterion. Criteria one pull request can deliver share one further task. The delivered task's Coverage omits each criterion a further task adopts.
  - A task delivering more than three criteria is split into tasks one pull request each can deliver.
  - A task covers at least one acceptance criterion. A criterion more than one row cites is imprecise: it is split into the invariant each task makes true, and each is cited from the row that delivers it.
  - Every test the work calls for accompanies that task. The content steers which kinds those are, including the project's system test when the work is something that test can exercise. A failure in any test the task carries keeps the task open. None of those tests is a later row.
  - Reusable routines, techniques, and resources are specced, created, and tested before an activity binds them. The grain of an existing resource is in that work.
  - When the behaviour a wired activity produces differs from the behaviour the work expected, that task changes the routine, technique, or resource, and the tests that cover the change, until fit, form, and function hold.
- **Joins.**
  The tasks that share one pull request. Each names the other, and neither depends on the other, directly or through a task outside the pair: the pull request holds their order.
  - Joins are complete before any issue of the epic is created. Every pair of tasks in the epic where neither depends on the other, directly or through another task, is accounted for.
  - A pair that shares a pull request names each other.
  - A pair that does not is named in the planning record, with why.
  - An empty cell is a task that shares no pull request, and only once that record names every such pair.
- **Numbering.**
  Task numbering meets [Numbering](issue-body.md#numbering); a row whose id links a pull request is fixed.
- **Reference form.**
  A table reference uses colons (`E01:W03`, `I05:E00:W02`), and every epic reference links to that epic's issue: `[E01:W03](…/issues/937)`. Prose uses a space (`E01 W03`).

### Acceptance Criteria

An epic criterion meets the [shared acceptance criteria](issue-body.md#shared-acceptance-criteria). Contradictions between criteria in one epic are findings.

### Open Questions

Each question holds only what is undecided and has a recommendation in the planning record. A settled point belongs in that record. No question remains when the epic starts.

### Corpus Audit

An epic whose tasks change workflow definitions carries this criterion, and a final task row delivers it:

```markdown
- [ ] **ACn.** The definitions this epic changes carry no outstanding confirmed finding, as the canon audit's coverage report shows.
```

- **The row is the epic's last.**
  It is named `Canon audit of the changed definitions`, depends on the rows whose definitions it audits, and covers this criterion alone.
- **The audit row is a unit of its own.**
  It is joined to no other row, so its Joins cell is empty.
- **A finding closes by a fix on this epic's branch or by an issue that takes it.**
  Outstanding means neither.
- **Definitions change when a task row's work reaches the branch the corpus lives on.**
  A row that only changes the engine, continuous integration or the workspace does not bring the criterion.

### Task Delivery

- **Holds.**
  - A unit's record exists and its rows link it before its session starts.
  - A row another session holds is not dispatched.
  - A held row stays held while its session plans and implements. The pull request's link replaces the record's link, which frees the row.
- **Task ids.**
  - An unreserved task awaiting its pull request links its file in the planning record: `[W01](…/w01.md)`. The file name is the task id in lower case.
  - Every link on a task row names that row's id, and the row carries one delivery per long-lived branch its unit changes. A reserved task links only its planning folder: `[W01](…/2026-10-06-943-i07-e00-w01-queue-plan/)`. The folder's README links the work-item file. Releasing the reservation points the row to that file.
  - Once a pull request is open, its link replaces the planning link: `[W01](…/pull/950)`. A unit changing two long-lived branches links the pull request on each: `[W01](…/pull/950), [W01](…/pull/951)`. Further delivery work on one of those branches gets another task row under Task grain. Joined rows each link their shared pull request.
  - The task is delivered when a linked pull request has merged, or its id links a commit.
  - A link to an open pull request does not deliver the task.
  - A linked pull request whose title names another epic delivers the task once it has merged. The mismatch is reported, and the row stays open while a criterion its Coverage names is unticked.
- **Tasks with their own issue.**
  - A task issue belongs to one epic. Its title carries that epic's prefix.
  - When that epic's table has no row for its id, the issue is unplaced. Once the row exists, that epic's planning manages the issue.
  - The row links the pull request, not the issue.
  - The pull request's Development field links the issue as [Issue Links](pull-request.md#issue-links) state.
  - A completed task issue has all criteria verified and every Development-linked pull request merged.
- **Issues backing several tasks.**
  An issue backing several tasks, such as an investigation, is a reference: the epic cites it under References, no row id links it, and its title carries no agent-engineering prefix.
- **Work another issue takes.**
  It leaves the table. Its criteria go with it, or to another row that delivers them.

### Body File

A local Markdown file at a given path holding one epic body that meets [Template](#template).

### Epic Scope

The work one epic takes: its slice of the initiative's design, its title and labels meeting [Titles](#titles), its [acceptance criteria](#acceptance-criteria), and its proposed task rows meeting [Work Breakdown](#work-breakdown).

### Release Decision

The user's explicit decision to release the hold on named task rows, naming each task id it releases.

### Gap Disposition

Each criterion a delivered row left unmet, with its missing evidence and one disposition:
- **Holds.** The user confirms it already holds; the delivered task retains it, awaiting verification and ticking.
- **Further task.** A further task row adopts it, meeting [Task grain](#work-breakdown).
- **Pending.** The decision or the further task's draft is unanswered.
