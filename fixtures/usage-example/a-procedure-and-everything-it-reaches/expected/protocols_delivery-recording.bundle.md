# Protocols

## Delivery Recording

The task and epic records brought to the delivery an initiative's pull requests establish, with the findings that delivery leaves routed.

Follow the [Procedure](#procedure), adhering to [Rules](#rules) and [Conventions](#conventions).

### Procedure

#### 1. Read the Evidence

Apply [Read Delivery Evidence](#read-delivery-evidence) with the selected repositories and initiative prefix, each selected epic's fetched JSON, authenticated access and destination snapshot files.

- Use its pull request records, complete issue-link snapshot and per-epic [Delivery Findings](#delivery-findings) in the following steps.
- Return its [unnamed deliveries](#unnamed-deliveries) and any incomplete evidence to the caller with the result.

#### 2. Match Deliveries to Tasks

For each selected epic, apply [Match Delivery to Tasks](#match-delivery-to-tasks) with the epic JSON and the pull requests its Unmatched and In flight findings name, and those linked to the task issue a Note row links, with their changes and descriptions.

- Use the confirmed task-to-pull-request pairs in the following steps.
- Return the pending matches to the caller.

#### 3. Record the Merged Deliveries

For each selected epic with a confirmed match whose pull request has merged:

- Follow [Issue Delivery](#issue-delivery) once with every such merged pull request, its matched tasks' issue records, the epic JSON, the pull request records, complete issue-link snapshot, confirmed matches, project checkout, named instruments, the caller's allowance and change list, and output body and comment files.
- Follow [Issue Closure](#issue-closure) for each task issue whose delivery result it returns as eligible, with the confirmed repository setting.

#### 4. Record Each Epic

For each selected epic, apply [Record Epic Delivery](#record-epic-delivery) with its current JSON, the pull request records, complete issue-link snapshot, task issue records, every confirmed match, open or merged, project checkout and output body file.

- Apply [Save Tracker Issue](#save-tracker-issue) with the returned body when it differs from the current one.
- Route the returned [Delivery Findings](#delivery-findings):
  - **Conflict.**
    - Return each to the caller as an unresolved finding.
  - **Unmatched, in flight or note.**
    - Apply Match Delivery to Tasks with the pull requests it names, or for a note those linked to the row's task issue.
    - Add the confirmed pairs to the matches.
  - **Draft or references.**
    - Follow [Review Pull Request](#review-pull-request) with the repository, the epic base it names, the delivery findings, the actual task merges into that base, the epic's issue, the confirmed repository setting and the current epic and task-merge records.
  - **Unmerged.**
    - Return the epic base to the caller with its review identity.
  - **Uncited.**
    - Apply [Link Pull Request to Issue](#link-pull-request-to-issue) with the pull request and issue it names, the pull request records, link-snapshot destination, authenticated access and confirmed repository setting.
    - Use its refreshed snapshot in the following steps.
  - **Unplaced.**
    - Apply [Place Unplaced Task Row](#place-unplaced-task-row) with the epic JSON, the unplaced task issue, the caller's allowance and change list, the pull request records, complete issue-link snapshot, task issue records, confirmed matches, project checkout and output body file.
    - Return a row it leaves pending to the caller with the updated change list.
  - **Open questions.**
    - Apply [Resolve Open Questions](#resolve-open-questions) with the epic identity, current JSON, the epic [Template](#template) and [Fields](#fields-2), the initiative as related context and an output body path.
    - Return the questions it leaves open to the caller.
  - **Ready to verify.**
    - Apply [Record Verified Criteria](#record-verified-criteria) with the repository, those criterion ids, the epic's current JSON and body, delivery findings, delivery revisions, named instruments, project checkout, the verification evidence Issue Delivery and each earlier pass of this routing returned, output body file, pull request records and complete issue-link snapshot.
    - Retain its verified ids and verification evidence, with those Issue Delivery returned, for the next pass and the caller.
    - For each criterion this run leaves unverified on an unmet row, as Delivery Findings defines one, apply [Plan Gap Task](#plan-gap-task) with the current epic JSON and body, the delivered task row, those criterion ids, the delivery records, complete issue-link snapshot and output body path, once per criterion.
    - Apply Record Verified Criteria again for each criterion Plan Gap Task returns as already holding, with the verification evidence retained so far.
  - **Ticked early.**
    - Apply Match Delivery to Tasks for the delivery the criterion's rows lack.
    - Where no match is confirmed, apply [Untick Criteria](#untick-criteria) with the current body, those criterion ids and the output body file.
    - Apply Save Tracker Issue with the returned body.
  - **Disagreement.**
    - Return each to the caller with its pull request and row.
- Repeat Record Epic Delivery, its save and this routing with the saved epic JSON, refreshed records and every confirmed match, until it returns no unmatched, in flight, uncited, note or unplaced finding beyond those returned to the caller as pending.
- Return to the caller the saved epic and task identities, each epic's latest Delivery Findings, the verified criteria, every verification evidence this run took with the revision it was taken on, the pull request records and complete issue-link snapshot, the updated change list and every pending or unresolved finding.

## Issue Delivery

The task and epic bodies brought to what an epic's merged pull requests establish, one pull request or several.

Follow the [Procedure](#procedure-1), adhering to [Rules](#rules) and [Conventions](#conventions).

### Procedure

#### 1. Task Issues

For each task issue the pull requests deliver:

- Apply [Verify Selected Criteria](#verify-selected-criteria) for each criterion the task covers, with its current body, delivery findings, delivery revisions, named instruments, the project checkout and the run's verification evidence.
- Add the verification evidence it returns to the run's, which starts as the verification evidence the caller supplied.
- Apply [Record Task Delivery](#record-task-delivery) with the task JSON, pull request records, complete issue-link snapshot, its delivering pull request number, returned verified criterion ids, output body file and output comment file.
- Apply [Save Tracker Issue](#save-tracker-issue) with the repository, task issue number and returned body file.
- Apply [Comment on Issue](#comment-on-issue) with the repository, task issue number and returned comment file.

#### 2. Epic Rows

Apply [Record Epic Delivery](#record-epic-delivery) with the epic JSON, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches, project checkout and output body file.

- Apply [Save Tracker Issue](#save-tracker-issue) with the returned body when it differs from the current one.
- For each task issue its [Delivery Findings](#delivery-findings) name as unplaced:
  - Apply [Place Unplaced Task Row](#place-unplaced-task-row) with the saved epic JSON, that task issue, the caller's allowance and change list when supplied, the pull request records, complete issue-link snapshot, task issue records, confirmed matches, project checkout and output body file.
  - Use the body and Delivery Findings it returns in the following steps; a row it leaves pending is returned to the caller with the updated change list.

#### 3. Epic Criteria

Apply [Record Verified Criteria](#record-verified-criteria) with the repository, the criteria the returned Delivery Findings name as ready to verify, the saved epic JSON and body, those findings, delivery revisions, named instruments, project checkout, the run's verification evidence, output body file, pull request records and complete issue-link snapshot.

- Add the verification evidence it returns to the run's.
- Return to the caller the saved task and epic identities, each task's eligibility findings, the verified criteria, the run's verification evidence with the revision each was taken on, each criterion left unverified, the epic's Delivery Findings with each coverage disagreement as [Delivery Findings](#delivery-findings) defines it, and the updated change list.

## Issue Closure

Fresh closure evidence assembled across an issue and its linked pull requests, and the closure it permits.

Follow the [Procedure](#procedure-2), adhering to [Rules](#rules) and [Conventions](#conventions).

### Procedure

#### 1. Issue

- Apply [Read Tracker Issue](#read-tracker-issue) for the issue selected by the delivery checks.
- Apply [Capture Issue Development](#capture-issue-development) for that issue.

#### 2. Pull Requests

Apply [Read Pull Request State](#read-pull-request-state) for every captured link, across repositories and all states.

#### 3. Check Delivery Completion

Apply [Check Issue Completion](#check-issue-completion) with the issue's kind, current JSON, complete Development snapshot, those pull request records and criterion verification evidence, adding the task's delivery result for a task and the project checkout for an epic.

- Return an incomplete or failed result to the caller before closure.

#### 4. Close

Apply [Close Tracker Issue](#close-tracker-issue) with the issue identity, the successful completion result, issue JSON, complete Development snapshot, confirmed repository setting and those pull request records.

- On a changed link set or missing evidence, repeat from [1. Issue](#1-issue) for the same issue.
- Report any unmerged link or unmet criterion.

## Review Pull Request

The draft pull request and body that present one epic base's delivered changes for review.

Follow the [Procedure](#procedure-3), adhering to [Rules](#rules) and [Conventions](#conventions).

### Procedure

#### 1. Find

Use the review number in the supplied delivery findings.

- When it is absent:
  - Apply [Locate Review Pull Request](#locate-review-pull-request) with the repository and epic base as head.
  - Use its returned number or absence result.
- Fetch an existing review through [Read Pull Request State](#read-pull-request-state).

#### 2. Populate

Pass the existing body when present and the actual task merges into the base to [Populate Review Body](#populate-review-body).

#### 3. Publish

For an existing review, or a base whose [State](#state) calls for one, pass the returned file to [Publish Pull Request](#publish-pull-request).

- For an existing review, supply its number.
- For a new review, supply the epic kind, the epic base as head with the target [Other Pull Requests](#other-pull-requests) gives it, the epic's issue, the repository setting the caller confirmed and a link-snapshot destination.
- Return a discrepancy Publish Pull Request reports to the caller.
- When the base has no review and its State calls for none, return the absence result to the caller.

#### 4. Record

Apply [Record Epic Delivery](#record-epic-delivery) with the current epic and the task-merge records, including the review state Publish Pull Request returned.

- Return its updated body and [Delivery Findings](#delivery-findings) with the review identity to the caller.

# Rules

What binds every mode, protocol and artifact operation, stated once here and linked by the step that applies it.

## Decisions

A question the user must decide is put as an interview, one question at a time. A decision the run's [allowance](#allowance) covers is taken with its recommended option rather than asked. Record each decision in the affected issues and, when there is one, the planning record.

- A plain-language paragraph before the question gives the context the user needs to answer it.
- The question offers more than one choice. The recommended choice is marked on its option.
- Wait for the user's answer. An unanswered question stays pending. A recommendation or elapsed time supplies no answer.
- The user can select Other and specify a response beyond the options.
- Use the native tool for presenting the question when one is available.

## Layers

Modes, protocols, artifacts. A mode aggregates protocol calls, as an application calls services; a protocol applies artifact operations and follows other protocols; an artifact does neither. A call goes down the stack, never up. A mode reaches an artifact operation directly only where no protocol owns that change.

## Execution

A call passes its named inputs. A protocol is one change that lands in several artifacts together, and is followed whole. Follow another mode, a protocol or a named procedure subsection, and apply an artifact operation, only where the procedure calls for it; finish that call and return its result before continuing. Calls run in order. A step's `⇉` call runs in a sub-agent, from any session, dispatched or not; its `⫽` calls run in sub-agents together, as the bundle's Prosiform section states, and those together never write to the same object.

# Conventions

The prerequisites every mode's run shares: the session it starts in, where a command runs, how a result is read, and the values its examples use. Each is stated once here, and every step applying one links it.

## Session

Once per session, before the first `gh` call, unset `GH_TOKEN` and `GITHUB_TOKEN` so `gh` uses its keyring login. Where shell state does not persist between commands, confirm instead that neither is set in the shell profile.

## Repository

`gh` resolves `{owner}/{repo}` from the git remote of the directory it runs in, so run `gh` commands inside a checkout of the repository that holds the issues. `{other}` is a further repository the board's issues live in.

## Bodies

- Bodies, long comments and commit messages always go through a file (`-F body=@file`), never inline, which avoids quoting. The file holds the exact intended text.
- Keep these files in a working directory outside the repository.

## Helper Invocation

A helper is a script in `<workspace>`, the checkout holding this skill. It runs from `<workspace>`, or the directory within it that its command names, under the sandbox invoked by its absolute path, `<workspace>/scripts/sbx`. A file kept outside `<workspace>`, such as a body file, is passed by its absolute path.

## Command Result

Read each command's exit code and output before the next step. A failing exit code, or a refusal the command reports, returns to the caller as an execution error or refusal before the work continues.

## Helper Result

A helper's written body exists only on a zero exit code. An invocation failure returns as a blocker, and only a successfully written body is published.

## Write Confirmation

Only a fresh re-read confirms a write: read the written object again and compare it with the intended state. The write's own output confirms nothing. A re-read that fails, or shows another state, leaves the write uncertain; that uncertainty returns to the caller, and the write is never retried as a different write.

- A list read can lag a write, so a written item confirms by its own read alone. An item still showing the preceding state has the same write repeated and that item read again.

## Boards

A project board sits under `users/{owner}`, or `orgs/{owner}` when `gh api repos/{owner}/{repo} --jq .owner.type` is `Organization`.

## Example Values

Substitute the real ones:

- `936` an initiative issue, `943` and `937` its epics, `637` a task issue, `874` an orphan, `946` an initiative off the board, `960` a proposal;
- `950` a pull request, `I07` and `I08` initiative numbers;
- board `9` a theme board, and `419167630` its Status field id;
- `1` the Initiative Template board, `13` a board copied from it;
- `14` the Proposals Template, `15` the Proposals board;
- `m2ux` the user.
- `<checkout>` any checkout of the project, a linked worktree included.

# Artifacts

## Delivery Evidence

### Operations

#### Read Delivery Evidence

The pull requests and issue links that establish current delivery.

**Inputs:** [Repositories](#repository-1), [Initiative prefix](#titles-2), [Epic issues](#issue-record), [Records path](#pull-request-records), [Link snapshot path](#issue-link-snapshot)

**Outputs:** [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Delivery findings](#delivery-findings), [Unnamed deliveries](#unnamed-deliveries)

##### 1. Fetch Pull Requests and Links

Fetch the pull requests and their links.

- Apply [Read Initiative Pull Requests](#read-initiative-pull-requests).
- Apply [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links).
- Use [Access Development Links](#access-development-links) for the actual complete link sets.

##### 2. Inspect the Epic Delivery

Apply [Inspect Epic Delivery](#inspect-epic-delivery) with the epic JSON, pull request records and complete issue-link snapshot.

- Route the returned [Delivery Findings](#delivery-findings) to matching, verification or user decisions.
- Fetch any linked pull request absent from the input with [Read Pull Request State](#read-pull-request-state).
- Repeat Inspect Epic Delivery with the same epic JSON, refreshed pull request records and complete issue-link snapshot.

##### 3. Name the Unnamed Deliveries

Name each pull request whose issue links reach an epic or one of its task issues and whose title omits that epic's reference as an [unnamed delivery](#unnamed-deliveries).

##### 4. Return the Delivery Evidence

Return the current pull request records, complete issue-link snapshot, per-epic findings and unnamed deliveries to the caller, reporting incomplete evidence as a blocker.

### Fields

#### Unnamed Deliveries

A pull request whose issue links reach an epic or its task issues while its title omits that epic's reference. Each is named with the epic it reaches, for the user to confirm.

## Epic

### Operations

#### Inspect Epic Delivery

The delivery findings for one epic from supplied evidence.

**Inputs:** [Epic issue](#issue-record), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot)

**Outputs:** [Delivery findings](#delivery-findings)

##### 1. Match Epic Pull Requests

From `<workspace>`, inspect the epic JSON using the supplied pull request records as `--prs` and complete link snapshot as `--links`.

- Results follow [Delivery Findings](#delivery-findings).

Runs as [Helper invocation](#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json
```

##### 2. Return the Inspected Delivery Findings

Read the helper’s result as [Command result](#command-result) states, retaining delivery findings as evidence.

Return the [Delivery Findings](#delivery-findings); missing linked pull requests are missing evidence for the caller to supply.

#### Match Delivery to Tasks

The tasks each delivering pull request works on.

**Inputs:** [Epic issue](#issue-record), [Pull request records](#pull-request-records)

**Outputs:** [Task matches](#task-matches)

##### 1. Read Pull Requests Against Task Rows

Read each pull request's changes and description against the Descriptions of the epic's task rows.

##### 2. Name the Matched Tasks

Name the tasks it works on: one task, or tasks that name each other in [Joins](#work-breakdown).

##### 3. Interview on Unclear Matches

Put each match that is not clear to the user as an [interview](#rules). An unanswered match stays pending.

##### 4. Return the Task Matches

Return the confirmed matches as task-to-pull-request pairs, and the pending ones, to the caller.

#### Check Epic Readiness

The epic's eligibility for integration from current delivery and criterion evidence.

**Inputs:** [Epic issue](#issue-record), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Criterion verification](#verification-evidence)

**Outputs:** [Integration readiness](#delivery-state)

##### 1. Inspect the Epic Delivery

Apply [Inspect Epic Delivery](#inspect-epic-delivery) with the supplied epic JSON, pull request records and complete issue-link snapshot.

##### 2. Confirm Epic Integration Conditions

Confirm every task is delivered, every epic criterion is verified and ticked, and no open question or unresolved delivery discrepancy remains. An unmerged epic base awaiting integration is expected at this stage. Missing or stale verification leaves readiness unconfirmed.

##### 3. Return the Epic Integration Readiness

Return the integration readiness in [Delivery State](#delivery-state), with the evidence revisions and each blocker. Readiness establishes the epic's content conditions; the caller supplies pull-request review, target and head-check evidence for the merge.

#### Check Epic Completion

The epic's normal delivery result before tracker closure.

**Inputs:** [Epic issue](#issue-record), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Criterion verification](#verification-evidence), [Expected bases](#epic-bases), [Base merges](#state)

**Outputs:** [Completion result](#delivery-state)

##### 1. Check the Epic Readiness

Apply [Check Epic Readiness](#check-epic-readiness) with the current epic, pull request records, issue-link snapshot and criterion verification evidence.

##### 2. Reconcile Epic Bases with Task Targets

Reconcile the expected bases with the task delivery targets.

##### 3. Confirm Every Epic Base Merged

Confirm every base has merged into its corresponding long-lived branch. An unknown or incomplete base list, or missing merge evidence, leaves completion unconfirmed even when every task is delivered and every criterion is ticked.

##### 4. Return the Epic Completion Result

Return the completion result in [Delivery State](#delivery-state), identifying remaining blockers. Passing normal delivery checks supplies the caller's closure evidence; the tracker issue's current Development-link gate still governs the write.

### Fields

#### Task Matches

Task-to-pull-request pairs identifying the epic task id and delivering pull request, with each match marked confirmed or pending.

#### Delivery State

The epic is identified by its repository and issue number. Its state contains task delivery findings, criterion verification and ticks, open questions, expected delivery bases and their merges, and the revisions supporting the evidence. Integration readiness and completion are separate results, each with its unresolved conditions. An epic may be ready to integrate while one or more bases await merging.

#### Delivery Findings

| Line | What it names |
| --- | --- |
| Conflict | Tasks that share a pull request and do not name each other in Joins. A row linked to a pull request whose title names another epic. |
| Unmatched | A merged pull request that names the epic and that no row links. |
| In flight | An open pull request that names the epic and that no row links. A pull request whose head is an epic base is not a task match. |
| Draft | An epic base a merged task targets that has no pull request merging it, while a task is undelivered or a criterion is unticked. |
| Unmerged | An epic base its pull requests target that has not merged into its long-lived branch, once every task is delivered and every criterion is ticked. A draft pull request is named draft. |
| References | A review pull request whose cited pull requests differ from the task pull requests merged into its base. |
| Uncited | A linked pull request whose task has its own issue and does not link it, or a review pull request that does not link the epic's issue. |
| Note | A row that links its task issue. |
| Unplaced | A task issue of this epic whose id is not a row. |
| Open questions | The epic's Open Questions section remains. |
| Ready to verify | An unticked criterion whose delivering rows are all delivered. |
| Ticked early | A criterion ticked while a delivering row is not delivered. |
| Disagreement | A linked pull request's test plan against the Coverage of the rows it delivers. |

An unmet row links a merged pull request while a covered criterion remains unticked. A linked pull request naming another epic is a conflict and delivers its linked task once merged. A missing linked pull request leaves the supplied evidence incomplete.

A coverage disagreement identifies the pull request and row, a criterion absent from either the test plan or row Coverage, an empty Test cell, or prose assigning the criterion to another task. Recording links, verified criteria and Done continues despite that finding.

## Epic Issue Body

### Operations

#### Populate Epic Issue Body

One epic body and its local validation findings.

**Inputs:** [Initiative issue](#issue-record), [Epic scope](#epic-scope), [Pull request records](#pull-request-records), [Corpus branch](#branches), [Output body file](#body-file)

**Outputs:** [Epic body](#body-file), [Draft rows](#work-breakdown), [Validation findings](#format-findings), [Unresolved links](#temporary-links)

##### 1. Draft the Epic Body

Populate the body from the [Template](#template) at the supplied output path.

- Every section must meet [Fields](#fields-2).
- Shared content must meet the common [body conditions](#fields-5).

##### 2. Write the Shared Epic Table

Populate the shared table through [Write Issue Table](#write-issue-table).

##### 3. Fill the Epic-Specific Cells

Fill the epic-specific cells.

- Each row must meet [Work Breakdown](#work-breakdown).

##### 4. Build the Epic Body Snapshot

Apply [Build Body Snapshot](#build-body-snapshot) with the draft body, title, labels and existing issue JSON when present.

##### 5. Validate the Epic Draft

Pass that snapshot, initiative context, available pull request records, corpus branch and output file to [Validate Epic Body](#validate-epic-body).

##### 6. Identify Unresolved Epic Links

Identify unresolved publication links separately; they remain pending until tracker identities exist.

##### 7. Return the Epic Draft Rows

Return the draft rows, their dependency references and the validation findings for the caller's cross-body ordering check.

#### Record Epic Delivery

One epic body with supplied delivery matches and completed rows recorded.

**Inputs:** [Epic issue](#issue-record), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Task issues](#issue-record), [Task matches](#task-matches), [Project checkout](#project-checkout), [Output body file](#body-file)

**Outputs:** [Epic body](#body-file), [Delivery findings](#delivery-findings)

##### 1. Run Sync Epic

From `<workspace>`, update the supplied epic JSON, mapping pull requests to `--prs`, links to `--links`, task issues to `--tasks`, each confirmed match to `--link`, the checkout to `--project` and the output body file to `--fix`.

- A row whose id links its task issue links the pull request instead.
- A pull request whose head is an epic base is the pull request that merges that base, and is not matched to a task.
- An unmerged epic base keeps the epic open, even when every row is delivered and every criterion is ticked.
- `--project` is a checkout of the project. Without the long-lived branch names, an epic that would otherwise be closable is not.
- `--link` names each task id and the pull request number it links. `--tasks` is the task issues. `--links` is the pull requests' Development-linked issues. `--fix` is the body written with the Done ticks.

`<task-pull-request-map>` is a comma-separated list of `<task-id>=<pull-request-number>` pairs. Pass each task JSON file as a separate argument after `--tasks`.

Runs as [Helper invocation](#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --tasks '<task-json-file>' --link '<task-pull-request-map>' --project '<checkout>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json --tasks issue-637.json --link W01=950,W02=950 --project '<checkout>' --fix fixed-943.md
```

- Omit `--tasks` when no row has its own task issue; otherwise supply each task issue's record.
- Row changes must meet [Task Delivery](#task-delivery) and [Work Breakdown](#work-breakdown).

##### 2. Return the Epic Delivery Findings

Read the helper’s result as [Helper result](#helper-result) states, retaining its reported findings or refused criteria.

Return the updated body and [Delivery Findings](#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.

#### Record Epic Criteria

Verified criteria and completed rows in one epic body.

**Inputs:** [Epic issue](#issue-record), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Verified criteria](#acceptance-criteria), [Output body file](#body-file)

**Outputs:** [Epic body](#body-file), [Refused criteria](#unverified-criteria)

##### 1. Run Tick Epic Criteria

From `<workspace>`, update the epic JSON with records as `--prs`, snapshot as `--links`, verified criterion ids as `--tick` and output body file as `--fix`. Refuse criteria not ready to verify.

`<criterion-ids>` is a comma-separated list of verified criterion ids.

Runs as [Helper invocation](#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --tick '<criterion-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json --tick AC1,AC3 --fix fixed-943.md
```

##### 2. Return the Epic Body and Refused Criteria

Read the helper’s result as [Helper result](#helper-result) states, retaining its reported findings or refused criteria.

Return the body and refused criteria. Complete rows receive Done ticks.

#### Validate Epic Body

The body's local format and field findings.

**Inputs:** [Epic issue](#issue-record), [Initiative issue](#issue-record), [Pull request records](#pull-request-records), [Corpus branch](#branches), [Output body file](#body-file)

**Outputs:** [Epic body](#body-file), [Validation findings](#format-findings)

##### 1. Validate the Epic Issue Body

Apply [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#fields-2), supplied related evidence and output file, supplying initiative JSON as `--initiative`, current pull request records as `--prs` and corpus branch as `--corpus`.

##### 2. Read Epic Pull Request Reach

Read reach from each epic pull request's base, through an epic base or initiative branch. Without both pull requests and the corpus branch, reach is unevaluable.

##### 3. Report Corpus Audit and Coverage Gaps

Include a missing [Corpus Audit](#corpus-audit) criterion on a corpus-changing epic and any epic criterion no task row delivers in the findings.

##### 4. Return the Validated Epic Body

Return the corrected body, mechanical diff and unresolved findings for the caller.

#### Revise Epic Rows

One epic body with confirmed task-grain and coverage corrections.

**Inputs:** [Epic body](#body-file), [Row changes](#work-breakdown), [Field findings](#field-findings), [Dependency references](#work-breakdown), [Output body file](#body-file)

**Outputs:** [Epic body](#body-file), [Numbering changes](#numbering-map), [Dependency changes](#work-breakdown)

##### 1. Apply the Confirmed Row Changes

Apply the confirmed row changes through [Populate Epic Issue Body](#populate-epic-issue-body), preserving unrelated content.

- Description, Coverage, Depends on, Joins and task grain must meet [Work Breakdown](#work-breakdown).
- Split a task exceeding the allowed criterion grain into the confirmed tasks.

##### 2. Return the Revised Epic Body

Return the revised body and any cross-body numbering or dependency changes for the caller.

#### Plan Gap Task

The agreed disposition of criteria a delivered row left unmet.

**Inputs:** [Epic issue](#issue-record), [Delivered task row](#work-breakdown), [Unmet criteria](#acceptance-criteria), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Output body file](#body-file)

**Outputs:** [Saved epic issue](#issue-record), [Gap disposition](#gap-disposition)

##### 1. Present Unmet Epic Criteria

Present each unmet criterion and its missing evidence, read from the current epic issue, to the user.

- Return the criteria the user confirms already hold to the caller for verification and ticking. The delivered task retains them.
- Record an unanswered decision as pending.
- If no criteria need further work, return the pending findings to the caller.
- Continue to [2. Draft the Gap Task](#2-draft-the-gap-task) with only the criteria the user confirms need further work.

##### 2. Draft the Gap Task

Draft a further task for the criteria selected for further work, meeting [Work Breakdown](#work-breakdown).

- Confirm the draft with the user.
- On acceptance, apply [Revise Epic Rows](#revise-epic-rows) with the further row and the criteria it adopts from the delivered task's Coverage.
- Return an unanswered draft as pending without continuing to [3. Record the Revised Epic Delivery](#3-record-the-revised-epic-delivery).

##### 3. Record the Revised Epic Delivery

Apply [Record Epic Delivery](#record-epic-delivery) with the revised epic and the supplied delivery evidence.

- Publish the returned body through [Save Tracker Issue](#save-tracker-issue).
- Return the saved row and criterion disposition to the caller. Done follows [Tables](#tables).

#### Place Unplaced Task Row

One epic body given the row its table lacks for a task issue of the epic.

**Inputs:** [Epic issue](#issue-record), [Unplaced task issue](#issue-record), [Allowance](#allowance), [Change list](#change-list), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Task issues](#issue-record), [Task matches](#task-matches), [Project checkout](#project-checkout), [Output body file](#body-file)

**Outputs:** [Saved epic issue](#issue-record), [Epic body](#body-file), [Delivery findings](#delivery-findings), [Change list](#change-list)

##### 1. Draft the Unplaced Task Row

Draft the task issue's row, meeting [Work Breakdown](#work-breakdown).

##### 2. Settle the Row Placement

Apply [Settle Plan Change](#settle-plan-change) with the drafted row as a task creation, the task issue as its subject, the drafted row as the recommended option, the epic and task issue identities, the supplied allowance and the change list.

- Return a row left held, unanswered or declined to the caller as pending, with the updated change list, without continuing to [3. Revise Epic Rows with the Placed Row](#3-revise-epic-rows-with-the-placed-row).

##### 3. Revise Epic Rows with the Placed Row

Apply [Revise Epic Rows](#revise-epic-rows) with the row as applied.

##### 4. Save the Revised Epic Issue

Publish the returned body through [Save Tracker Issue](#save-tracker-issue).

##### 5. Re-Record the Epic Delivery

Apply [Record Epic Delivery](#record-epic-delivery) again with the saved epic JSON and refreshed task issue records, retaining the pull request records, complete issue-link snapshot, confirmed matches, project checkout and output body file.

##### 6. Return the Recorded Epic Body

Return the recorded body, its [Delivery Findings](#delivery-findings) and the change list to the caller.

### Fields

#### Template

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

#### Titles

- The title is `[I07:E00] Name: Subtitle`. Its prefix matches its row in the initiative table.
- Labels are the epic [kind label](#kind-labels) and its initiative's [theme label](#theme-labels).
- `E` is the epic within its initiative. Epics count from `00`.
- The prefix separates levels with colons, then a short name, a colon, and a subtitle: `[I07:E06] Reliability Evaluation: Briefs, Measures and the Thresholds That Define Reliable`.

#### Proposal

- A boundary with a sibling epic is plain language.

#### Work Breakdown

New tasks exist as epic rows with their details, discussion and evidence in the epic and planning record. Planning creates no separate task issues. Existing issues hoisted into an epic retain their records and row links when new tasks are planned.

The columns are `Task | Description | Coverage | Depends on | Joins | Done`.

- The body meets [Breakdown Prose](#breakdown-prose).

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
  Task numbering meets [Numbering](#numbering); a row whose id links a pull request is fixed.
- **Reference form.**
  A table reference uses colons (`E01:W03`, `I05:E00:W02`), and every epic reference links to that epic's issue: `[E01:W03](…/issues/937)`. Prose uses a space (`E01 W03`).

#### Acceptance Criteria

An epic criterion meets the [shared acceptance criteria](#shared-acceptance-criteria). Contradictions between criteria in one epic are findings.

#### Open Questions

Each question holds only what is undecided and has a recommendation in the planning record. A settled point belongs in that record. No question remains when the epic starts.

#### Corpus Audit

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

#### Task Delivery

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
  - The pull request's Development field links the issue as [Issue Links](#issue-links) state.
  - A completed task issue has all criteria verified and every Development-linked pull request merged.
- **Issues backing several tasks.**
  An issue backing several tasks, such as an investigation, is a reference: the epic cites it under References, no row id links it, and its title carries no agent-engineering prefix.
- **Work another issue takes.**
  It leaves the table. Its criteria go with it, or to another row that delivers them.

#### Body File

A local Markdown file at a given path holding one epic body that meets [Template](#template).

#### Epic Scope

The work one epic takes: its slice of the initiative's design, its title and labels meeting [Titles](#titles), its [acceptance criteria](#acceptance-criteria), and its proposed task rows meeting [Work Breakdown](#work-breakdown).

#### Release Decision

The user's explicit decision to release the hold on named task rows, naming each task id it releases.

#### Gap Disposition

Each criterion a delivered row left unmet, with its missing evidence and one disposition:

- **Holds.** The user confirms it already holds; the delivered task retains it, awaiting verification and ticking.
- **Further task.** A further task row adopts it, meeting [Task grain](#work-breakdown).
- **Pending.** The decision or the further task's draft is unanswered.

## Issue

### Operations

#### Read Tracker Issue

The current issue, its saved body and discussion.

**Inputs:** [Issue identity](#issue-identity), [Record path](#issue-record)

**Outputs:** [Issue record](#issue-record), [Issue comments](#issue-comment)

##### 1. Fetch the Tracker Issue

Select the command for the requested response shape, using the issue number and destination file.

For a complete JSON response, run this query from the repository checkout using the supplied repository, issue number and destination JSON file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' > '<issue-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' > issue-943.json
```

For the body alone, run this query from the repository checkout using the supplied repository, issue number and destination body file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' --jq .body > '<output-body-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' --jq .body > live-943.md
```

##### 2. Fetch the Issue Comments

Read the result of each command in the preceding step as [Command result](#command-result) states.

When the request depends on the discussion, fetch every comment from the repository checkout using the supplied repository and issue number.

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/<issue-number>/comments'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/874/comments'
```

##### 3. Return the Issue Read

Read each requested response as [Command result](#command-result) states; return the issue record and any requested comments, or the failed read as missing evidence. When no discussion was requested, return the issue record alone.

#### Save Tracker Issue

One populated body and its metadata, written to the tracker.

**Inputs:** [Issue identity](#issue-identity), [Issue content](#issue-content), [Label definitions](#label-identity), [Comment](#issue-comment)

**Outputs:** [Saved issue](#issue-record)

##### 1. Take the Issue Body and Metadata

Take the supplied body and metadata, preserving each field the caller does not change for an existing issue.

##### 2. Ensure the Issue Labels

Apply [Ensure Repository Labels](#ensure-repository-labels) with every label the save assigns and its colour and description.

- Return an unknown label definition to the caller before any write.

##### 3. Create New Issue

For a new issue, run this creation command from the repository checkout using the supplied title, existing labels and complete body file as [Bodies](#bodies) states.

Repeat `-f 'labels[]=<label>'` for each supplied label.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues' -f title='<title>' -F 'body=@<body-file>' -f 'labels[]=<label>' --jq .number
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues' -f title='<title>' -F body=@body.md -f 'labels[]=<label>' --jq .number
```

##### 4. Update the Existing Issue

Read the result of each command in the preceding step as [Command result](#command-result) states.

For an existing issue, run each command whose field is being changed, preserving all other fields. After each selected command, read its result as [Command result](#command-result) states; stop before another mutation on a failure. If no field changes, continue with the supplied issue identity.

When changing the issue body, run this update from the repository checkout using its repository, number and complete body file as [Bodies](#bodies) states.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -F 'body=@<body-file>' --jq .number
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -F body=@body.md --jq .number
```

When changing the issue title, run this update from the repository checkout using its repository, number and complete new title.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f title='<title>' --jq .title
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -f title='<title>' --jq .title
```

For each requested label addition, run this command from the repository checkout using the issue’s repository, number and existing label names.

Repeat `-f 'labels[]=<label>'` for each supplied label.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/labels' -f 'labels[]=<label>' --jq '.[].name'
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/943/labels' -f 'labels[]=<label>' --jq '.[].name'
```

For each requested label removal, run this command from the repository checkout using the issue’s repository, number and label name.

```bash
gh api --method DELETE 'repos/<owner>/<repo>/issues/<issue-number>/labels/<label>' --jq '.[].name'
```

**Example:**

```bash
gh api --method DELETE 'repos/<owner>/<repo>/issues/943/labels/<label>' --jq '.[].name'
```

##### 5. Comment on the Saved Issue

Read the result of each command in the preceding step as [Command result](#command-result) states.

Apply [Comment on Issue](#comment-on-issue) for an answer or a preserved body the caller requires, with the issue number and comment file.

##### 6. Re-Read the Saved Issue

As [Write confirmation](#write-confirmation) states, read the saved issue.

From the repository checkout, save the current issue using its repository, number and supplied destination JSON file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' > '<issue-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' > issue-943.json
```

##### 7. Compare the Saved Issue Fields

Read the result of each command in the preceding step as [Command result](#command-result) states.

Compare the saved fields with the intended body and metadata.

#### Check Issue Completion

The normal delivery result of one task, epic or initiative before tracker closure.

**Inputs:** [Issue record](#issue-record), [Development snapshot](#development-snapshot), [Linked pull request records](#linked-pull-request-records), [Verification evidence](#verification-evidence), [Task delivery result](#task-delivery-result), [Project checkout](#project-checkout)

**Outputs:** [Completion result](#completion-result)

##### 1. Select the Completion Check

Select the check by the issue's kind:

- **Task.**
  - Retain the task delivery result its delivering pull request established.
- **Epic.**
  - Apply [Read Delivery Branches](#read-delivery-branches) with the project checkout and epic identity for the complete expected bases.
  - Apply [Read Pull Request State](#read-pull-request-state) for each base's merge evidence.
  - Apply [Check Epic Completion](#check-epic-completion) with the current epic JSON, linked pull request records, complete issue-link snapshot, criterion verification evidence and those base records.
- **Initiative.**
  - Apply [Read Tracker Issue](#read-tracker-issue) for every linked epic.
  - Apply [Check Initiative Completion](#check-initiative-completion) with the current initiative JSON, all linked epic records, criterion verification evidence and the Development snapshot and linked pull request records.

##### 2. Return the Completion Result

Return the completion result; an incomplete or failed result is a blocker to closure.

#### Close Tracker Issue

Verified completion of an issue and its linked delivery.

**Inputs:** [Issue identity](#issue-identity), [Completion result](#completion-result), [Issue record](#issue-record), [Development snapshot](#development-snapshot), [Auto-close setting](#auto-close-setting), [Linked pull request records](#linked-pull-request-records)

**Outputs:** [Closed issue](#issue-state)

##### 1. Capture the Issue Development

Apply [Capture Issue Development](#capture-issue-development) for the issue's complete links and confirmed repository setting.

##### 2. Take Fresh Pull Request Records

Take the caller's fresh records for every linked pull request, across repositories and states; return missing evidence to the caller.

- Return a repository setting that is unconfirmed or fails [Auto-Close Setting](#auto-close-setting) to the caller as a blocker.
- Take the records only from a fresh destination file, so an earlier snapshot cannot supply membership.
- Use the issue's entire Development field to establish membership. Titles, branch names, body mentions and a list filtered to one initiative do not establish completeness. An explicitly empty field adds no pull request requirement.

##### 3. Run the Closure Check

Apply [Run Closure Gate](#run-closure-gate) with the fresh issue JSON, complete Development snapshot and linked pull request records, using absolute evidence paths.

##### 4. Require the Closure Gate

Read the result of each command in the preceding step as [Command result](#command-result) states.

Require the supplied completion result to be complete, normal delivery checks to pass, every criterion to be verified and ticked, and every currently linked pull request to be merged.

- Keep the issue open for an open, draft, closed without merge, or unreadable linked pull request.
- Obtain the user's decision before removing an abandoned or incorrect Development link. A replacement pull request does not remove the requirement on a link still present.

##### 5. Close the Issue as Completed

Apply [Close as Completed](#close-as-completed), which repeats the gate immediately before the write. A changed link set requires another capture and check.

#### Comment on Issue

The supplied discussion text saved on one issue.

**Inputs:** [Issue identity](#issue-identity), [Comment](#issue-comment), [Review feedback](#review-feedback)

**Outputs:** [Saved comment](#issue-comment)

##### 1. Compose the Feedback Reply

When replying to feedback already folded into the body, compose a precise, factual reply addressing each point and mentioning the reviewer, with no thanks or filler. Name what the body now says, by criterion id where one carries it, or the issue that takes the point.

##### 2. Publish the Issue Comment

Publish the supplied comment:
For a one-line comment, post its exact text from the repository checkout using the supplied repository and issue number.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -f body='<comment-text>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/637/comments' -f body='Delivered by #950.' --jq .html_url
```

For a longer comment, post the complete supplied file from the repository checkout using the repository and issue number, as [Bodies](#bodies) states.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -F 'body=@<comment-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/874/comments' -F body=@comment-874.md --jq .html_url
```

##### 3. Return the Comment URL

Read the result of each command in the preceding step as [Command result](#command-result) states.

Return the saved comment URL.

#### Close as Completed

An issue closed after its final evidence check.

**Inputs:** [Issue identity](#issue-identity), [Auto-close setting](#auto-close-setting), [Completion result](#completion-result), [Issue record](#issue-record), [Development snapshot](#development-snapshot), [Linked pull request records](#linked-pull-request-records)

**Outputs:** [Completed issue](#issue-state)

##### 1. Capture Development Before Closure

Require absolute paths for the issue, Development and linked pull request evidence files.
Apply [Capture Issue Development](#capture-issue-development) immediately before closure with the issue identity, authenticated access, confirmed repository setting and evidence paths.

##### 2. Compare the Development Links

Compare its links with the supplied fresh pull request records; return a changed link set or missing evidence to the caller for refresh.

##### 3. Run the Completion Gate

Apply [Run Closure Gate](#run-closure-gate) with the current issue JSON, complete Development snapshot and linked pull request records, using absolute evidence paths.

##### 4. Require the Completion Gate to Pass

Read the result of each command in the preceding step as [Command result](#command-result) states.

Require exit 0 and passing normal delivery checks; a sync report of closable does not permit skipping this gate.

##### 5. Set the Completed State

Immediately after the gate passes and normal delivery checks pass, run this closure from the repository checkout using the issue’s repository and number.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f state=closed -f state_reason=completed --jq .state
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -f state=closed -f state_reason=completed --jq .state
```

##### 6. Return the Completed State

Read the result of each command in the preceding step as [Command result](#command-result) states.

Return the saved state or failure.

#### Run Closure Gate

The closure check's verdict for one issue, its Development snapshot and its linked pull request records.

**Inputs:** [Issue record](#issue-record), [Development snapshot](#development-snapshot), [Linked pull request records](#linked-pull-request-records)

**Outputs:** [Closure verdict](#closure-verdict)

##### 1. Run the Closure Command

From `<workspace>`, run the closure gate with the fresh issue JSON, complete Development snapshot and linked pull request records.

- `--issue`, `--development`, and `--prs` are the fresh issue JSON, Development snapshot, and linked pull request records.
- Exit 0 means the closure gate passes; normal delivery checks must also pass. Exit 1 reports blockers. The command performs no network calls or writes.

Runs as [Helper invocation](#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue '<issue-json-file>' --development '<development-snapshot-file>' --prs '<linked-pull-request-records-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue issue-943.json --development development-943.json --prs development-prs-943.json
```

##### 2. Return the Closure Verdict

Read the result of each command as [Command result](#command-result) states. Return the verdict with each blocker it reports, or the execution failure.

#### Capture Issue Development

The issue's current content and complete Development snapshot.

**Inputs:** [Issue identity](#issue-identity), [Auto-close setting](#auto-close-setting), [Record path](#issue-record), [Snapshot path](#development-snapshot)

**Outputs:** [Development snapshot](#development-snapshot), [Issue record](#issue-record)

##### 1. Read the Development Field

Apply [Read Issue Development](#read-issue-development) for the entire field across repositories and states. An inaccessible field returns incomplete evidence; an empty array means the field was checked and empty.

##### 2. Write the Development Snapshot

Write the issue identity, observed links, completeness result and repository setting to the supplied path, such as `development-943.json`, in the [Development Snapshot](#development-snapshot) shape. Preserve incomplete evidence as incomplete and the unknown auto-close setting as `null`.

##### 3. Fetch the Issue Snapshot

From the repository checkout, save the issue’s current JSON using its repository and number and the supplied path, such as `issue-943.json`.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' > '<issue-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' > issue-943.json
```

##### 4. Return the Development Files

Read the result of each command in the preceding step as [Command result](#command-result) states.

Return both files and any incomplete evidence. The caller supplies fresh linked pull request records in `development-prs-943.json`.

#### Read Issue Development

The Development links observed for one issue through authenticated GitHub.

**Inputs:** [Issue identity](#issue-identity)

**Outputs:** [Observed links](#observed-development-links)

##### 1. Read Every Development Link

Read every page and state, across repositories, recording each linked pull request's identity.

##### 2. Return the Observed Development Links

Return the observed links and whether the entire field was readable.

#### Confirm Repository Auto-Close

Whether the repository auto-closes issues whose linked pull requests merge, established for this session.

**Inputs:** [Repository](#tracker-repository)

**Outputs:** [Auto-close setting](#auto-close-setting)

##### 1. Read the Auto-Close Setting

Read the setting where the authenticated API exposes it, and take a read value as the answer.

##### 2. Ask the User for Auto-Close

Where no API field carries it, put the setting to the user and take their explicit answer, meeting [Auto-Close Setting](#auto-close-setting).

##### 3. Return the Confirmed Auto-Close Setting

Return the confirmed value. An unconfirmed setting is a blocker, and an enabled one leaves the caller to obtain authorization before the repository is reconfigured.

### Fields

#### Observed Development Links

Every linked pull request URL in an issue's Development field, across repositories and states, and whether the entire field was readable.

#### Tracker Repository

The repository whose tracker holds the issues: its owner and name, written `<owner>/<repo>`.

#### Issue Identity

One issue's [repository](#tracker-repository), number and URL. An issue yet to be created has its repository alone. An unresolved identity names the repository and the title prefix that matched no issue.

#### Issue Content

An issue's title, body and labels. The title meets [Titles](#titles-1), the body is a [body file](#body-file-1), and each label is a [repository label](#label-identity). The saved title, body and labels equal the supplied values.

#### Issue Record

One issue as the tracker returns it, saved as JSON at a local path: its [identity](#issue-identity), [content](#issue-content), [state](#issue-state) and kind, which its [tracker prefix](#tracker-prefix) and [kind label](#kind-labels) give. A body-only record is the issue's body alone, saved as markdown.

#### Issue Comment

One comment on an issue: its exact text, as one line or a complete local file, and once saved its URL. An issue's discussion is its comments in order. A saved comment preserves the supplied text.

#### Issue State

The issue is open, or closed with its reason: completed or not planned. Completed work satisfies its criteria and delivery checks; transferred work, closed as not planned, identifies the issue tracking it.

#### Tracker Prefix

The bracketed prefix a planned issue's title opens with: for each level, its kind's prefix letter and a two-digit number, levels separated by colons, as `[I07]`, `[I07:E00]` and `[I07:E00:W01]`. A tracker number is the two-digit number of one level.

#### Development Snapshot

One issue's Development field as observed, saved as JSON at a local path: the issue's repository and number, whether the whole field was read, the repository's [auto-close setting](#auto-close-setting) as confirmed or `null` when unknown, and every linked pull request URL across repositories and states. An empty list in a complete snapshot means the field holds no link; an incomplete snapshot is incomplete evidence.

The JSON object has this shape. The issue number is a JSON integer, completeness is a boolean, and the auto-closing setting is a boolean or `null` when unknown. The array holds every observed pull request URL, or is empty when there are none. Incomplete evidence has completeness `false`.

```text
{
  "repo": "<owner>/<repo>",
  "number": <issue-number>,
  "complete": <complete>,
  "auto_close_issues": <auto-close-issues>,
  "pull_requests": ["<pull-request-url>"]
}
```

**Example payload:**

```json
{
  "repo": "owner/repo",
  "number": 943,
  "complete": true,
  "auto_close_issues": false,
  "pull_requests": ["https://github.com/owner/repo/pull/980"]
}
```

- Set `complete` true only after the full read, and `auto_close_issues` false only after the repository setting is confirmed disabled.

#### Linked Pull Request Records

A fresh record of every pull request a [Development snapshot](#development-snapshot) names, across repositories and states, saved as JSON lines at a local path, each with its [state](#state) and merge result.

#### Completion Result

The normal delivery result of one task, epic or initiative: complete, or incomplete with each unmet condition. A task's comes from its [task delivery result](#task-delivery-result), an epic's from its [delivery state](#delivery-state), and an initiative's from its [delivery state](#delivery-state-1).

#### Closure Verdict

The closure gate's report for one issue: passing, or the blockers that keep it open.

#### Review Feedback

The reviewer's login and each point they raised in an issue's discussion.

#### Auto-Close Setting

GitHub's **Auto-close issues with merged linked pull requests** repository setting, which must be disabled before a delivery pull request is linked or merged, so that closure follows the criteria rather than the merge.

- The setting is confirmed per repository and holds for the session; it is not inferred from an issue that stayed open.
- No REST field and no GraphQL field of `gh` 2.46 carries it, so on such a host the user's explicit answer is the only source.
- An enabled setting closes issues on merge whatever their criteria. Where it cannot be disabled, each affected issue's state is read after every merge and reopened where its criteria are unmet.

## Pull Request

### Operations

#### Access Development Links

The observed or updated Development relation for a pull request.

**Inputs:** [Pull request](#pull-request-identity), [Link request](#link-request), [Delivery issue](#issue-record), [Auto-close setting](#auto-close-setting)

**Outputs:** [Development links](#issue-links)

##### 1. Read the Pull Request Development Links

Use authenticated GitHub or an available supported tool to read the supplied pull request's actual Development field across every page and state, recording the repository and number for each linked issue and whether the field was fully readable. A missing tool or inaccessible field is a blocker, not an empty link set.

##### 2. Return the Read-Only Relation

Return the complete relation for a read-only request.

##### 3. Edit the Development Links

For a link edit, take the supplied repository prerequisite from [Confirm Repository Auto-Close](#confirm-repository-auto-close); an unconfirmed setting blocks the edit.

- Meet the applicable preconditions in [Close Tracker Issue](#close-tracker-issue).
- For an addition, use [GitHub's sidebar linking procedure](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue): in the issue's authenticated Development selector, select the pull request's repository and pull request, including a different repository when required. Retain the edit result.
- For removal of an abandoned or incorrect link, require the supplied user decision before deselecting the supplied relation in the authenticated Development selector and saving the edit. Retain the edit result.

##### 4. Re-Read the Pull Request Development Links

Read the same pull request's actual Development field through authenticated GitHub or an available supported tool, as [Write confirmation](#write-confirmation) states.

- Include every page and state, recording each linked issue's repository and number and whether the field was fully readable.
- Return a failed edit or unreadable field as a blocker.

##### 5. Compare the Field with the Edit

Compare the field with the intended edit.

##### 6. Return the Verified Link Relation

Return the verified relation or discrepancy.

#### Fetch Pull Request Issue Links

The complete issue-link snapshot for a supplied set of pull requests.

**Inputs:** [Pull request records](#pull-request-records), [Link snapshot path](#issue-link-snapshot)

**Outputs:** [Issue-link snapshot](#issue-link-snapshot)

##### 1. Read Links for Each Pull Request

For every pull request in the current records, `prs.json`, apply [Access Development Links](#access-development-links) with a read-only request and its identity. An observed empty field supplies an empty array; an unreadable field leaves the fetch incomplete.

##### 2. Re-Read Links After a Change

Repeat that read after a link changes, as [Write confirmation](#write-confirmation) states.

##### 3. Return an Incomplete Link Fetch

If any relation is unreadable, return the incomplete result.

##### 4. Write the Links Snapshot

Write the observed complete relations to the supplied destination, such as `links.json`, in the [Issue-Link Snapshot](#issue-link-snapshot) shape. Include one entry per pull request and every linked issue's repository and number.

##### 5. Return the Links Snapshot

Return the snapshot for the scripts' `--links` input.

#### Link Pull Request to Issue

The verified delivery-issue relation for a pull request.

**Inputs:** [Pull request](#pull-request-identity), [Delivery issue](#issue-record), [Pull request records](#pull-request-records), [Link snapshot path](#issue-link-snapshot), [Auto-close setting](#auto-close-setting)

**Outputs:** [Development links](#issue-links), [Issue-link snapshot](#issue-link-snapshot)

##### 1. Add the Development Link

Apply [Access Development Links](#access-development-links) with the supplied identities, requested link addition and the repository prerequisite confirmed as [Close Tracker Issue](#close-tracker-issue) documents.

##### 2. Stop on an Unverified Link Edit

Stop on a blocker or an unverified edit.

##### 3. Refresh the Links Snapshot

Apply [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links) with the current records and destination after the edit.

##### 4. Return the Verified Link and Snapshot

Return the verified relation and refreshed snapshot.

#### Read Initiative Pull Requests

The current delivery pull requests for one initiative.

**Inputs:** [Repository](#repository-1), [Initiative prefix](#titles-2), [Records path](#pull-request-records)

**Outputs:** [Pull request records](#pull-request-records)

##### 1. Fetch the Initiative Pull Requests

From the repository checkout, save the initiative’s pull requests using its repository, prefix and destination JSON-lines file.

`<initiative-prefix>` includes the opening bracket and initiative id, matching its task and epic titles.

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("<initiative-prefix>"))' > '<pull-request-records-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I07"))' > prs.json
```

##### 2. Return the Initiative Collection

Read the result of each command in the preceding step as [Command result](#command-result) states.

Return the collection or an incomplete-fetch finding.

#### Read Pull Request State

One current pull request and its requested supporting records.

**Inputs:** [Pull request](#pull-request-identity), [Requested records](#pull-request-snapshot), [Snapshot paths](#pull-request-snapshot)

**Outputs:** [Pull request snapshot](#pull-request-snapshot)

##### 1. Fetch the Pull Request Snapshot

Select the command for the supplied destination shape to capture current identity, state, head and base.

For a JSON-lines collection, append the pull request from the repository checkout using its repository, number and destination file.

```bash
gh api 'repos/<owner>/<repo>/pulls/<pull-request-number>' --jq . >> '<pull-request-records-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/pulls/439' --jq . >> prs.json
```

For a complete standalone JSON snapshot, save the pull request from the repository checkout using its repository, number and destination file. This replaces the destination.

```bash
gh api 'repos/<owner>/<repo>/pulls/<pull-request-number>' > '<pull-request-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/pulls/980' > epic-pr.json
```

##### 2. Fetch Requested Files or Reviews

Read the result of each command in the preceding step as [Command result](#command-result) states.

Run each requested supporting-record command. After each read, read its result as [Command result](#command-result) states; return a failure before the next read, keeping missing evidence explicit.

When changed files are requested, save their paths from the repository checkout using the supplied repository, pull request number and destination file.

```bash
gh api --paginate 'repos/<owner>/<repo>/pulls/<pull-request-number>/files' --jq '.[].filename' > '<changed-paths-file>'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/pulls/950/files' --jq '.[].filename' > changed-files.txt
```

When reviews are requested, save every review from the repository checkout using the supplied repository, pull request number and destination file.

```bash
gh api --paginate 'repos/<owner>/<repo>/pulls/<pull-request-number>/reviews?per_page=100' > '<reviews-file>'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/pulls/980/reviews?per_page=100' > reviews.json
```

##### 3. Return the Pull Request Snapshots

Read the result of each command in the preceding step as [Command result](#command-result) states.

Return the snapshots or missing evidence.

#### Publish Pull Request

One pull request created or updated from supplied content and metadata.

**Inputs:** [Pull request](#pull-request-identity), [Kind](#pull-request-kind), [Pull request content](#pull-request-content), [Delivery issue](#issue-record), [Auto-close setting](#auto-close-setting), [Link snapshot path](#issue-link-snapshot)

**Outputs:** [Pull request snapshot](#pull-request-snapshot), [Issue-link snapshot](#issue-link-snapshot)

##### 1. Open a New Pull Request

For creation, select exactly one command for the supplied kind, body, title, head and base, preserving epic and discussion draft state. For an existing pull request, continue at [3. Update the Existing Pull Request](#3-update-the-existing-pull-request).

For task creation, run this command from the repository checkout using the supplied title, task branch, epic base and complete body file as [Bodies](#bodies) states.

- Supply the epic prefix and purpose as title, the task branch as head, the epic base as base, and the complete body file.

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='<title>' -f head='<task-branch>' -f base='<epic-base>' -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='[I07:E00] Purpose' -f head='i07/e00/w01-purpose' -f base='i07/e00/main' -F body=@body.md --jq .html_url
```

For epic creation, run this command from the repository checkout using the supplied title, epic base, long-lived target and review body file as [Bodies](#bodies) states.

- Supply the epic prefix and name as title, the epic base as head, its long-lived branch as base, and the populated review body file.
- `draft` is true, including when the work is already complete.

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='<title>' -f head='<epic-base>' -f base='<long-lived-base>' -F draft=true -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='[I07:E00] Name' -f head='i07/e00/main' -f base='main' -F draft=true -F body=@body.md --jq .html_url
```

For discussion creation, run this command from the repository checkout using the supplied title, planning branch, target branch and body file as [Bodies](#bodies) states.

```bash
gh api --method POST 'repos/<owner>/<repository>/pulls' -f title='<title>' -f head='<planning-branch>' -f base='<target-branch>' -F body=@'<body-file>' -F draft=true
```

**Example:**

```bash
gh api --method POST repos/m2ux/workflow-server/pulls -f title='Queue Planning: Scope and Delivery' -f head=planning/queue -f base=engineering -F body=@discussion.md -F draft=true
```

##### 2. Confirm Creation and Link the Delivery Issue

For a creation request, read the command’s result as [Command result](#command-result) states, with its returned identity; return a failure before attempting a link.

- For a task or epic pull request with a delivery issue, require the confirmed auto-close setting and snapshot destination, then apply [Link Pull Request to Issue](#link-pull-request-to-issue) with them, meeting [Issue Links](#issue-links). A row task without its own issue supplies no delivery issue, auto-close setting or link snapshot for publication.
- After a successful creation and any required link, continue at [4. Re-Read the Published Pull Request](#4-re-read-the-published-pull-request).

##### 3. Update the Existing Pull Request

For an existing pull request, run each command for a supplied change, preserving other fields. After each selected command, read its result as [Command result](#command-result) states; stop before another mutation on a failure. If no field changes, continue with the supplied pull request identity.

When changing the body, run this update from the repository checkout using the pull request’s repository, number and complete body file as [Bodies](#bodies) states.

- The file is the whole body. The issue a pull request delivers is linked on the pull request itself, so this call leaves that link standing.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/<pull-request-number>' -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/950' -F body=@pr-950.md --jq .html_url
```

When changing the title, run this update from the repository checkout using the pull request’s repository, number and complete title.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/<pull-request-number>' -f title='<title>' --jq .title
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/950' -f title='[I07:E00] Purpose' --jq .title
```

When changing the base, run this update from the repository checkout using the pull request’s repository, number and target branch.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/<pull-request-number>' -f base='<target-branch>' --jq .base.ref
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/950' -f base='i07/e00/main' --jq .base.ref
```

##### 4. Re-Read the Published Pull Request

Read the result of each command in the preceding step as [Command result](#command-result) states.

Re-read through [Read Pull Request State](#read-pull-request-state), as [Write confirmation](#write-confirmation) states.

##### 5. Return the Published State

Return the saved state or discrepancy, and the issue-link snapshot when the creation path linked a delivery issue. Other publication paths return no issue-link snapshot.

#### Locate Review Pull Request

The review pull request for a supplied epic base.

**Inputs:** [Repository](#repository-1), [Epic base](#epic-bases)

**Outputs:** [Review pull request](#pull-request-identity)

##### 1. Find the Review Pull Request

From the repository checkout, find the open review pull request using the repository owner and name and supplied epic base as head.

```bash
gh api "repos/<owner>/<repo>/pulls?state=open&head=<owner>:<epic-base>" --jq '.[0].number'
```

**Example:**

```bash
gh api "repos/<owner>/<repo>/pulls?state=open&head=<owner>:i07/e00/main" --jq '.[0].number'
```

##### 2. Return the Review Pull Request Number

Read the result of each command in the preceding step as [Command result](#command-result) states.

Return its number or an absent-review finding.

### Fields

#### State

A pull request is open, draft, ready for review, merged or closed without merge. A merged result identifies the verified head, target and merge commit.

- An epic's review pull request is published as a draft when the first task merges into its epic base, and an unmerged epic base with work merged into it has one.
- The review stays draft, and its epic open, until the epic is complete and the user marks it ready.

#### Scope

A task pull request delivers one task, or a set of tasks that name each other in Joins. It targets the epic base for the long-lived branch its work changes.

#### Other Pull Requests

- A pull request whose head is an epic base targets that base's long-lived branch.
- A pull request outside epic delivery targets a long-lived branch. An open stacked pull request targets its long-lived branch once its base merges.
- A merged pull request keeps the base it merged into.

#### Issue Links

- GitHub shows the link in the pull request's Development field and in the issue's Linked pull requests field, which the project board reads.
- A task pull request links the task's issue, and a review pull request links its epic's issue.
- The link is addressed by issue, so a pull request whose work carries no issue links nothing. A task pull request delivering rows that have no issue of their own is the whole of what stays unlinked.
- The link is stored on the pull request. It holds on any base branch and on a pull request that has merged, and a later body edit leaves it standing.
- A linked issue remains open until its criteria and delivery requirements hold and every Development-linked pull request is merged.
- The field is the whole of the relation: neither body links the other. The pull request's References carry its sources, and the issue it delivers is not among them.
- A pull request with a delivery issue but no Development link is uncited.

#### Pull Request Identity

A pull request's [repository](#repository-1) and number. A pull request yet to be created has its repository alone.

#### Pull Request Kind

Task, epic or planning discussion. A delivery pull request is a task or an epic one: a task pull request meets [Scope](#scope), and an epic's review pull request has an epic base as its head.

#### Pull Request Content

The fields a publication writes: a body file at its path, meeting [Template](#template-2), its title, head and base. A change to an existing pull request names only the fields it changes.

#### Pull Request Snapshot

One pull request's REST record as a local JSON file at its path, with its identity, state, head SHA, base and mergeable state. Its requested supporting records are its changed paths and its reviews, each in a file of its own.

#### Pull Request Records

A local JSON-lines file at its path, one pull request's REST record per line. An initiative's records hold every pull request whose title carries its prefix, in all states, across its repositories; a failed fetch leaves them incomplete.

#### Issue-Link Snapshot

A local JSON file (`links.json`) at its path holding an array of pull request entries. Each entry has `repo` as its owner/repository string, `number` as its integer pull request number, and `closingIssuesReferences` as an array of objects with `repo` and integer `number` for each Development-linked issue. An observed empty field is an empty array. The snapshot is complete only when every relation was read.

The JSON array has this shape. Numbers are JSON integers. Every pull request includes all linked issues; an empty array denotes a complete relation with no linked issues. Each repository belongs to its pull request or issue.

```text
[
  {
    "repo": "<pull-request-owner>/<pull-request-repo>",
    "number": <pull-request-number>,
    "closingIssuesReferences": [{"repo": "<issue-owner>/<issue-repo>", "number": <issue-number>}]
  }
]
```

**Example payload:**

```json
[
  {
    "repo": "owner/repo",
    "number": 950,
    "closingIssuesReferences": [{"repo": "owner/repo", "number": 637}]
  }
]
```

#### Link Request

A read, an addition or a removal of one pull request's Development link. An edit names the issue; a removal carries the user's decision naming the abandoned or incorrect link.

## Issue Body

### Operations

#### Write Issue Table

The shared table, before a kind fills its cells.

**Inputs:** [Current body](#body-file-1), [Kind conditions](#kind-conditions), [Row data](#tables)

**Outputs:** [Issue body](#body-file-1)

##### 1. Populate the Shared Table Cells

Populate the shared Done, Coverage and Depends on cells from the supplied row data.

- The columns must match the kind's table.
- The shared cells must meet [Tables](#tables).

##### 2. Read the Finished Issue Table

Read the finished table against [Tables](#tables), [Numbering](#numbering), and [Reference form](#reference-form). A Depends on cell that holds prose fails [Tables](#tables). Numbering that does not follow start order is advisory, as [Numbering](#numbering) states.

#### Validate Issue Body

One body checked against its supplied kind and template.

**Inputs:** [Issue record](#issue-record), [Kind conditions](#kind-conditions), [Related context](#related-context), [Output body path](#body-file-1)

**Outputs:** [Corrected body](#body-file-1), [Format findings](#format-findings), [Field findings](#field-findings)

##### 1. Run the Body Format Check

From `<workspace>`, check the supplied issue JSON with its kind’s additional format inputs and the output body file as `--fix`.

- The format reader takes the template fence from the body artifact and its table columns where present. A body with a Work Breakdown table requires coverage for every criterion.
- The input is one issue JSON. `--fix` names the output body file for mechanical fixes. Further inputs are specified by the calling body procedure.

Runs as [Helper invocation](#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/format.py '<issue-json-file>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/format.py issue.json --fix fixed.md
```

##### 2. Review the Body Field Conditions

Read the format checker’s result as [Command result](#command-result) states, with its findings and corrected body. Return an unreadable input as a blocker; retain format findings for the review.

Review the body against the supplied field conditions.

##### 3. Return the Body Validation Findings

Return the [Format Findings](#format-findings), mechanical diff and field findings, including missing sections, extra sections, wrong-kind layout, historical narration and criteria that fail their named instrument. A mechanical correction preserves wording; new content and scope decisions require caller-supplied resolutions.

#### Apply Body Corrections

One body rewritten from confirmed local findings.

**Inputs:** [Current body](#body-file-1), [Kind conditions](#kind-conditions), [Related context](#related-context), [Confirmed resolutions](#body-resolutions), [Output body path](#body-file-1)

**Outputs:** [Corrected body](#body-file-1), [Format findings](#format-findings), [Field findings](#field-findings), [Required changes](#required-changes)

##### 1. Populate Missing Body Sections

Populate missing sections from the supplied issue and related context.

##### 2. Apply Extra-Section Decisions

Apply each confirmed decision to keep, fold or remove an extra section, and rewrite a wrong-kind body in the selected template.

##### 3. Record the Tracker-Kind Change

Record a required tracker-kind change for the caller.

##### 4. Restate Historical Narration

Restate historical narration as the current design.

##### 5. Apply Confirmed Criterion Changes

Apply confirmed criterion changes.

- The body must meet [Body](#body), [Shared Acceptance Criteria](#shared-acceptance-criteria) and the supplied kind conditions.

##### 6. Validate the Corrected Body

Validate the body through [Validate Issue Body](#validate-issue-body).

##### 7. Return the Corrected Body

Return the corrected file, validation findings and any required cross-body or metadata changes for the caller.

#### Build Body Snapshot

A local issue-shaped record for body validation.

**Inputs:** [Issue content](#issue-content), [Existing issue](#issue-record), [Snapshot path](#body-snapshot)

**Outputs:** [Body snapshot](#body-snapshot)

##### 1. Write the Body Snapshot JSON

Write the body's exact text, title and labels to the destination as JSON.

##### 2. Preserve the Issue Identity

Preserve the existing issue's identity and state when supplied.

##### 3. Mark an Unpublished Draft

For an unpublished draft, use `number: null` and `state: "open"`; labels are strings or objects with a name.

##### 4. Return the Snapshot Path

Return the JSON path for validation. No tracker issue is created by this operation.

#### Resolve Open Questions

The answers to an issue's Open Questions saved in its body, and the questions that stay open.

**Inputs:** [Issue record](#issue-record), [Kind conditions](#kind-conditions), [Related context](#related-context), [Output body path](#body-file-1)

**Outputs:** [Saved issue](#issue-record), [Question decisions](#body-resolutions)

##### 1. Interview on Open Questions

Put each question in the body's Open Questions section to the user as an [interview](#rules).

##### 2. Apply the Question Answers

Apply [Apply Body Corrections](#apply-body-corrections) with the current body, kind template and conditions, related context, each confirmed answer and output path, removing each settled question from Open Questions.

##### 3. Publish the Answered Body

Publish the corrected body through [Save Tracker Issue](#save-tracker-issue).

##### 4. Re-Read the Answered Issue

Apply [Read Tracker Issue](#read-tracker-issue) for the saved issue, as [Write confirmation](#write-confirmation) states.

##### 5. Return the Question Decisions

Return the saved body, each decision taken and the questions still open in its Open Questions section. A question still open is a blocker to work that depends on it.

### Fields

#### Titles

- **Titles.**
  - A title is a short name, a colon, and a subtitle stating the outcome.
  - The name is two or three words and the subtitle a succinct summary of at most ten, in title case.
  - A prefixed title separates its levels with colons, then the name.
- **Bodies.**
  - Every body keeps the section order of its kind template and the columns of that kind's table.
  - Fill each `{{…}}` and delete a section the template marks as optional when it has nothing to say.
- **Code references.**
  A body references code as a link on the words it supports, a permalink pinned to a commit with its line anchors, never a bare `path:line`: `the [extrinsic type](…/blob/<sha>/runtime/src/lib.rs#L1231-L1232)`.
- **Succinct items.**
  Each Problem and Proposal item, and each of its sub-bullets, is at most two lines. A bold opener does not count toward the two. Several distinct points go in a bulleted list, never packed into those two lines.
- **Bold leads.**
  - A Problem or Proposal item that opens with a bold statement puts its body on the next line, indented under the bullet:

    ```markdown
    - **Length is the only check on entry.**
      The data source decodes the key and never checks its value.
    ```

  - A bulleted item with sub-bullets keeps the line introducing them on its bold statement's line:

    ```markdown
    - **Framing is undocumented.** Nothing describes:
      - the runtime's extrinsic type;
    ```
- **Labels.**
  - Add `enhancement`, `bug` and `tech-debt` as they apply.
  - **Example.**  workflow-server adds `workflows`.
  - Only labels that exist are applied.

#### Problem and Proposal

- **Friction.**
  A Problem states the friction as it is now. Its evidence is a count or a code link for that friction. A Problem does not describe the plan.
- **Plan ids.**
  A Problem or Proposal names no epic, task or acceptance criterion of its own initiative. The Work Breakdown table holds those references; a sibling boundary is plain language.
- **Evidence that may be cited.**
  Code, a merged pull request, and an issue outside this initiative may be cited.

#### Shared Acceptance Criteria

An acceptance criterion meets these. A kind adds its own under its Acceptance Criteria.

- States an end state, not an activity.
- Names or implies the instrument that observes it: a test, a guard, a command or a measure.
- Is unambiguous, so two readers agree on whether it holds.
- Meets [Requirement Characteristics](#requirement-characteristics).
- **One invariant.**
  Each criterion states a single condition that holds or does not. One joining several is split, and the Coverage cells cite the new ones. A condition over a list of subjects is one condition.

##### Verifiable

- Subjective wording is an observable pass or fail, or the criterion is absent.
- A fact that inspection, analysis, demonstration, or test can check is kept, such as every option having a description.
- A judgment about meaning, such as a claim that a description states what choosing means, is subjective wording.
- An item none of those methods can observe is named as [Coverage Reports](#coverage-reports) define, and it stays named there.

#### Tables

- **Done.**
  The last column. Its cell is empty while the row is open, and a tick, ✓, when the row is complete.
- **Description.**
  A short phrase naming what the row delivers, at most eight words, with no list, semicolon or detail.
- **Coverage.**
  The acceptance criteria the row delivers, `AC2, AC5`, and nothing else. Every criterion is delivered by at least one row.
- **Depends on.**
  References only, with no prose, and only what no other entry in the cell already implies.

#### Breakdown Prose

Work Breakdown contains its table. Explanatory prose belongs in Proposal. The body does not narrate execution order or how the tables work; Depends on carries the order.

#### Numbering

Rows are numbered in the order they can start, so every dependency points to an earlier row. Numbering that does not follow start order is advisory.

Work a pull request names keeps its number. Renumbering touches only a row no pull request names.

#### Reference Form

Tables write references with colons, the form the scripts read. Prose uses a space.

#### Body

- **Stale references.**
  A row number, issue link or decision wording agrees with the current plan.
- **Body.**
  A body states the plan as it is. It carries no change narrative. How the plan evolved belongs in the planning record and in commit and pull request bodies.

#### Stale References

Task and epic numbers, issue links and wording must agree with the current decisions and bodies. References to superseded decisions are findings.

#### References

An issue's References section does not link issues or pull requests on the same board.

#### Coverage Reports

- **Unobservable items.**
  An item a test cannot observe is named in the plan or the coverage report. It stays in the report.
- **The check matches the criterion.**
  - A file or string check counts as coverage only when the criterion is a fact about that file.
  - A criterion about a run is covered by a run that shows it.
- **The specified set.**
  A coverage report lists every acceptance criterion the work under review is specified to cover.

#### Format Findings

- **Fixed.**
  Structural changes preserve the wording and are present in the returned body file, with a body diff.
- **Apply.** Title or label changes for the caller to publish on the issue.
- **Decide.** Missing content or a judgement for the caller to resolve.

#### Body File

One issue body as a local markdown file at a given path, in its kind's template section order and table columns.

#### Kind Conditions

One body kind's template, with its table columns, its field conditions, and any further inputs its format check takes, as that kind's body file defines them.

#### Related Context

The current records a body refers to or depends on: its parent and sibling issues, linked delivery and cited sources.

#### Body Snapshot

A local [issue record](#issue-record) built from a body file, title and labels, saved as JSON at a given path. It carries the existing issue's identity and state, or `number: null` and `state: "open"` for an unpublished draft. Labels are strings or objects with a name.

#### Field Findings

Each place a body departs from its kind conditions or [Fields](#fields-5): a missing or extra section, a wrong-kind layout, historical narration, or a criterion failing its named instrument, with the section it concerns.

#### Body Resolutions

The decision taken on each non-mechanical finding or open question: content to add, an extra section kept, folded or removed, a criterion change, or an answer, each tied to the finding or question it settles.

#### Required Changes

Changes a body correction needs outside that body: a tracker-kind change, a title or label change, or an edit to another issue's body, each naming the issue it applies to.

## Acceptance Criteria

### Operations

#### Verify Selected Criteria

The verification evidence for a supplied set of criteria whose delivery is ready.

**Inputs:** [Criterion ids](#criterion), [Current body](#body-file-1), [Epic delivery findings](#delivery-findings), [Initiative delivery findings](#delivery-findings-1), [Delivery revisions](#revision), [Instruments](#instrument), [Project checkout](#instrument-checkout), [Verification evidence](#verification-evidence)

**Outputs:** [Verification evidence](#verification-evidence), [Verified criterion ids](#criterion), [Unverified criteria](#unverified-criteria)

##### 1. Confirm Criterion Readiness

Confirm the supplied delivery findings establish [Readiness](#readiness) for each selected criterion.

- Return an undelivered or unreadable dependency as a blocker for that criterion.

##### 2. Check Out the Delivered Branches

Check out each branch the delivering pull requests merged into, in the supplied project checkout, meeting [Instrument Checkout](#instrument-checkout).

- Keep the supplied evidence of each criterion taken on the revision now checked out, meeting [Verification Evidence](#verification-evidence).
- Run the named instrument of each other criterion there.
- Record the result against the tested revisions, meeting [Instrument Result](#instrument-result).

##### 3. Return the Criteria Verification Evidence

Return the verification evidence of each selected criterion, kept or taken, the verified criterion ids, and each unresolved criterion with what is missing.

- Leave body publication and further planning to the caller.

#### Tick Verified Criteria

The confirmed criteria and completed rows recorded in an epic or initiative body.

**Inputs:** [Issue record](#issue-record), [Verified criterion ids](#criterion), [Output body path](#body-file-1), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Linked epic records](#issue-record)

**Outputs:** [Ticked body](#body-file-1), [Refused criteria](#unverified-criteria)

##### 1. Record the Criterion Ticks

Record the criteria, meeting [Tick State](#tick-state).

- For an epic, apply [Record Epic Criteria](#record-epic-criteria) with the issue JSON, pull request records, complete issue-link snapshot, verified criterion ids and output body file.
- For an initiative, apply [Record Initiative Criteria](#record-initiative-criteria) with the issue JSON, every linked epic record, verified criterion ids and output body file.

##### 2. Return the Ticked Body

Return the resulting body and any criteria refused as not ready to verify. The artifact operations return the updated bodies for publication.

#### Untick Criteria

The criteria a body ticked without the delivery their evidence depends on, returned to unticked.

**Inputs:** [Current body](#body-file-1), [Criterion ids](#criterion), [Output body path](#body-file-1)

**Outputs:** [Unticked body](#body-file-1)

##### 1. Clear the Criterion Ticks

Clear the tick on each supplied criterion, and Done on each row or table that cites it, meeting [Tick State](#tick-state).

##### 2. Return the Unticked Body

Write the body to the output file and return it for publication, leaving every other criterion and row as it stands.

#### Record Verified Criteria

The verified criteria of one epic or initiative, ticked and saved to its issue.

**Inputs:** [Issue record](#issue-record), [Criterion ids](#criterion), [Epic delivery findings](#delivery-findings), [Initiative delivery findings](#delivery-findings-1), [Delivery revisions](#revision), [Instruments](#instrument), [Project checkout](#instrument-checkout), [Verification evidence](#verification-evidence), [Output body path](#body-file-1), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Linked epic records](#issue-record)

**Outputs:** [Saved issue](#issue-record), [Verified criterion ids](#criterion), [Verification evidence](#verification-evidence), [Unverified criteria](#unverified-criteria)

##### 1. Verify the Selected Criteria

Apply [Verify Selected Criteria](#verify-selected-criteria) with the criterion ids, current issue body, delivery findings, delivery revisions, named instruments, project checkout and the run's verification evidence.

- When it returns no verified id, continue at [4. Return the Recorded Verification](#4-return-the-recorded-verification).

##### 2. Tick the Verified Criteria

Pass only its returned verified ids to [Tick Verified Criteria](#tick-verified-criteria) with the issue JSON and output body file, and the pull request records with the complete issue-link snapshot for an epic or every linked epic record for an initiative.

##### 3. Save the Ticked Issue Body

When the returned body differs from the current issue body, apply [Save Tracker Issue](#save-tracker-issue) with the repository, issue number and output body file.

##### 4. Return the Recorded Verification

Return the verified ids, the verification evidence Verify Selected Criteria returned, the ids refused as not ready to verify, and each unverified criterion with what it is missing. A refused or unverified criterion stays unticked.

### Fields

#### Criterion

The id of one acceptance criterion in the issue body that states it, as `AC2`. A set of criteria is a list of those ids.

#### Instrument

The command, test or check the criterion names as the thing that observes it.

#### Revision

The branch and commit the instrument ran against, which is the branch the delivering pull requests merged into.

#### Readiness

A criterion is ready to verify when the supplied delivery findings show the work its evidence depends on delivered and readable. An undelivered or unreadable dependency leaves it unready.

#### Instrument Checkout

An instrument runs in a checkout of the project at the merged revision it is verifying, which the caller supplies. A checkout the caller is editing is not that revision, so a criterion verified against uncommitted work is unverified.

#### Instrument Result

A criterion is verified only on a passing run of its named instrument, recorded against the tested revisions as [Coverage Reports](#coverage-reports) define. A failed, unavailable or inconclusive instrument leaves it unverified, and an unverified criterion is not ticked.

#### Verification Evidence

One criterion's instrument result, passing or failing, with the issue that states the criterion and the revision it was taken on. Within one run, evidence stands for its criterion on its revision: the criterion's instrument runs at most once on each revision, and a later verification on that revision keeps the earlier evidence.

#### Tick State

A ticked criterion carries verification evidence. Done on the row or table that cites it follows [Tables](#tables) and [Work Breakdown](#work-breakdown). A criterion refused as not ready to verify is returned unticked with what it is missing.

#### Unverified Criteria

Each criterion left unticked, refused as not ready to verify or unverified, with what it is missing.

## Plan Change

### Operations

#### Check Plan Change Autonomy

One pending change assessed against the run's allowance.

**Inputs:** [Pending change](#pending-change), [Allowance](#allowance)

**Outputs:** [Autonomy result](#autonomy-result)

##### 1. Match the Plan Change Kind

Match the change to one kind in [Change Kinds](#change-kinds).

##### 2. Return an Automatic Plan Change

Return it as automatic where the supplied allowance names that kind, with the supplied recommendation as the option the caller applies.

##### 3. Return a Held Plan Change

Return it as [held](#held-change) otherwise.

- A change matching no kind is held, as is one matching [Initiative Creation](#initiative-creation).
- An absent allowance holds every change, so a run the user drives decides nothing on their behalf.

#### Record Plan Change

One entry in the run's list, for a change it applied or held.

**Inputs:** [Pending change](#pending-change), [Change kind](#change-kinds), [Option](#entry), [Outcome](#entry), [Affected issues](#issue-record), [Change list](#change-list)

**Outputs:** [Change list](#change-list)

##### 1. Add the Plan Change Entry

Add one entry meeting [Entry](#entry) to the supplied [Change List](#change-list), marked applied or held.

##### 2. Return the Updated Change List

Return the updated list for the caller to publish and report.

#### Settle Plan Change

One pending change carried to its outcome: applied, held, or answered by the user.

**Inputs:** [Pending change](#pending-change), [Affected issues](#issue-record), [Allowance](#allowance), [Change list](#change-list)

**Outputs:** [Settlement](#settlement), [Change list](#change-list)

##### 1. Check the Plan Change Autonomy

Apply [Check Plan Change Autonomy](#check-plan-change-autonomy) with the change, its subject, the recommended option and the supplied allowance.

##### 2. Settle by the Autonomy Result

Settle the change by what it returns:

- **Automatic.**
  - Take the recommended option as the applied option.
  - Apply [Record Plan Change](#record-plan-change) with the change, its kind, that option, the affected issue identities and the current list, marked applied.
- **Held, with an allowance supplied.**
  - Leave the change unapplied, meeting [Held Change](#held-change).
  - Apply Record Plan Change with the change, its kind, the recommended option, the affected issue identities and the current list, marked held.
  - Ask nothing, since the work the run was dispatched for does not wait on an answer.
- **Held, with no allowance supplied.**
  - Put the change to the user as an [interview](#rules), with the recommended option marked, and wait for the answer.
  - Where the answer applies a change, apply Record Plan Change with the change, its kind, the option the user chose, the affected issue identities and the current list, marked applied.
  - An answer leaving the work where it is takes no entry, as [Change Kinds](#change-kinds) states.

##### 3. Return the Settled Plan Change

Return the applied option, held, or the user's answer, with the updated change list.

### Fields

#### Pending Change

A change to the plan not yet applied: what it changes, its subject (the issue or row it concerns) and the option recommended for it.

#### Allowance

The caller names the change kinds its run applies without asking. A run the user drives directly is supplied none.

#### Change Kinds

| Kind | What It Covers |
| --- | --- |
| Task creation | A new task row, and the task issue that delivers it |
| Epic creation | A new epic, and the initiative row that carries it |
| Migration | Work moved from one issue to another, with the renumbering that move forces |
| Re-prioritisation | A priority label, a queue order or a board status |
| Folded work | Criteria, scope or design added to an existing issue because the work in hand needs it |

An option deciding to leave work where it is changes no plan, so it needs no allowance and takes no entry, unlike a change [held](#held-change) for the user to decide.

#### Initiative Creation

A new initiative is outside every allowance. The work stays where it is, open and unplaced, until the user decides where it belongs.

#### Change List

One list for the run, holding every change it applied and every change it held. It is what the run reports and what its record keeps.

#### Entry

One line: the kind, the issue or row it concerns, the option applied or recommended, and its outcome, applied or held. The entry states the change, not the alternatives weighed against it.

#### Autonomy Result

Automatic or held. An automatic result carries the change's [kind](#change-kinds) and the recommended option as the option to apply; a held result meets [Held Change](#held-change).

#### Settlement

The option applied, a [held change](#held-change), or the user's answer.

#### Held Change

A held change is left unapplied and its subject stays as it stands, so the next run sees the same decision. Its entry carries the recommended option, which is what the user is answering.

## Repository Labels

### Operations

#### Ensure Repository Labels

The required label definitions available for issue publication.

**Inputs:** [Repository](#repository-1), [Required labels](#label-identity)

**Outputs:** [Available labels](#label-identity)

##### 1. List the Repository Labels

From the repository checkout, list its labels using the supplied owner and repository.

```bash
gh api "repos/<owner>/<repo>/labels?per_page=100" --jq '.[].name'
```

##### 2. Compare Required Label Names

Read the result of each command in the preceding step as [Command result](#command-result) states.

Compare the returned labels with the supplied required names.

##### 3. Create Absent Required Labels

From the repository checkout, create each absent required label using its supplied name, colour and description. Read each creation’s result as [Command result](#command-result) states before the next label; return a failure immediately.

```bash
gh api --method POST 'repos/<owner>/<repo>/labels' -f name='<label>' -f color='<hex-colour>' -f description='<description>' --jq .name
```

##### 4. Return the Available Labels

Read the result of each command in the preceding step as [Command result](#command-result) states.

Return the observed existing labels and successful creations. When every required label already exists, return that observed set. An unknown definition is a finding for the caller to resolve before publication.

### Fields

#### Repository

One repository, written `<owner>/<repo>`.

#### Label Identity

Each label has a name, colour and description. Issue assignments use labels that exist in the repository.

## Initiative Issue Body

### Operations

#### Record Initiative Criteria

Verified criteria and completed rows in one initiative body.

**Inputs:** [Initiative issue](#issue-record), [Epic issues](#issue-record), [Verified criteria](#initiative-acceptance-criteria), [Output body file](#body-file-2)

**Outputs:** [Initiative body](#body-file-2), [Refused criteria](#unverified-criteria)

##### 1. Run Tick Initiative Criteria

From `<workspace>`, update the initiative JSON with linked epic records as `--epics`, verified criterion ids as `--tick` and output body file as `--fix`. Refuse criteria not ready to verify.

Pass every epic JSON file as a separate argument after `--epics`. `<criterion-ids>` is a comma-separated list of verified criterion ids.

Runs as [Helper invocation](#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<initiative-json-file>' --epics '<epic-json-file>' --tick '<criterion-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-936.json --epics issue-943.json issue-937.json --tick AC2 --fix fixed-936.md
```

##### 2. Return the Initiative Body and Refused Criteria

Read the helper’s result as [Helper result](#helper-result) states, retaining its reported findings or refused criteria.

Return the body and refused criteria. Complete rows receive Done ticks.

### Fields

#### Body File

A local Markdown file at a given path holding one initiative body that meets [Template](#template-1).

#### Temporary Links

Each placeholder for an unsaved initiative or epic issue, with the body file containing it and the intended issue identity.

#### Template

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

#### Titles

- The title is `[I07] Name: Subtitle`.
- Labels are the initiative [kind label](#kind-labels) and one [theme label](#theme-labels).
- `I` is the initiative number. Initiatives count from `00`.

#### Initiative Acceptance Criteria

An initiative criterion meets the [shared acceptance criteria](#shared-acceptance-criteria) and [Requirement Characteristics](#requirement-characteristics), and:

- **No counts.**
  An initiative criterion carries no counts or figures, which go stale: it measures against a named baseline or check ("against the baseline", "as the budget test measures it"). A figure stays only where it is the criterion's own target, such as a bound it holds to.
- **SMART.**
  Each initiative criterion is specific about what holds, measurable by a named check or baseline, achievable by the epics that cite it, and relevant, tracing to a clause and to the Problem. It is time-bound by a release tag or another named milestone outside the initiative's own work, where one exists, and otherwise by the epics that cite it.
- **Local.**
  An initiative criterion names no initiative, epic, task or issue, and is solution-agnostic. Coverage cells link epics to criteria. One that holds only through another initiative's work is restated as what this initiative achieves, or it is dropped.
- **Whole.**
  An initiative criterion states what the initiative achieves as a whole. One that restates a single epic's criterion is a duplicate: it is raised to what the epics achieve together, or left to the epic.
- **Verified.**
  - An initiative criterion ends by naming its instrument. Which instruments keep a criterion is [Verifiable](#verifiable).
  - An automated test is an end-to-end walk through the real server, a smoke run of an agent against a live server, a live check on a deployed host, or a guard, fixture suite or check that continuous integration runs. The walk, smoke run or live check is preferred where the criterion is about what a run does.
  - A named test that does not exist yet is work the plan holds: a task in the epic whose subject it tests, or a discrete test-infrastructure epic when the tests serve several criteria. That epic's row cites the criteria its tests verify.

## Delivery Branches

### Operations

#### Read Delivery Branches

The configured long-lived branches and existing epic bases.

**Inputs:** [Project checkout](#project-checkout), [Epic prefix](#epic-bases)

**Outputs:** [Long-lived branches](#branches), [Epic bases](#epic-bases)

##### 1. Read the Long-Lived Branch Configuration

From `<workspace>`, read the branch configuration using the supplied project checkout. Missing or empty configuration leaves branch names unevaluable.

- The names meet [Branches](#branches).
- `--project` is any checkout of the project. The names are the ones `config/branches` states in its main working tree, which a linked worktree resolves for itself.
- A missing or empty statement prints `unevaluable:`, names what is missing, and exits 1.

Runs as [Helper invocation](#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py --names --project '<checkout>'
```

##### 2. Read the Epic Base Names

Read the helper’s result as [Command result](#command-result) states. Preserve a missing or empty configuration as unevaluable evidence.

From the repository checkout, list remote bases using the supplied epic branch prefix.

- A base is `<epic-branch-prefix>/<name>` whose `<name>` is a [long-lived branch](#branches), named as [Epic Bases](#epic-bases) states.
- The prefix has the form `i<initiative-number>/e<epic-number>`. **Example:** `i07/e00`; a corresponding base is `i07/e00/main`.
- The output contains one full base branch name per line.

```bash
git ls-remote --heads origin 'refs/heads/<epic-branch-prefix>/*' | cut -f2 | sed 's|refs/heads/||'
```

**Example:**

```bash
git ls-remote --heads origin 'refs/heads/i07/e00/*' | cut -f2 | sed 's|refs/heads/||'
```

##### 3. Return the Delivery Branch Collections

Read the result of each command in the preceding step as [Command result](#command-result) states.

Return both collections and any missing configuration.

### Fields

#### Branches

A project states its long-lived branches in `config/branches` at its root, one name per line. A run from a linked worktree reads the statement its main working tree holds.

- **Example.**
  workflow-server's `config/branches` names `docker`, `main`, `workflows` and `workspace`.

#### Epic Bases

- Each long-lived branch an epic changes has a base branch, named for the initiative, the epic and that branch, and rooted in that long-lived branch. Its prerequisite epics are closed as completed with every delivery base merged.
- **Example.**
  An epic base cut from `main` is `i07/e00/main`.
- The base's last segment is its long-lived branch, which gives the target it merges and is merged into.
- Each base is worked in one worktree, named by the base under the worktree directory of the repository's main working tree.
- **Example.**
  `i07/e00/main` merges `main`, and is checked out at `.worktrees/i07/e00/main`.
- A completed epic is delivered by merging each base into its long-lived branch. The epic stays open until every base has merged.

#### Project Checkout

A checkout of the repository whose branches are delivered. Its main working tree holds the [Branches](#branches) statement, and its worktree directory holds every epic-base, task and review worktree.

## Task Body

### Operations

#### Record Task Delivery

One task body with its confirmed delivery and verified criteria recorded.

**Inputs:** [Task issue](#issue-record), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Delivering pull request](#pull-request-identity), [Verified criterion ids](#criterion), [Output body path](#body-file-1), [Comment path](#issue-comment)

**Outputs:** [Task delivery result](#task-delivery-result)

##### 1. Sync the Task Issue

From `<workspace>`, update the task JSON with records as `--prs`, snapshot as `--links`, delivering pull request number as `--pr`, verified criterion ids as `--tick` and output body file as `--fix`. Tick only criteria the caller has verified.

`<criterion-ids>` is a comma-separated list of verified criterion ids.

Runs as [Helper invocation](#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<task-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --pr '<pull-request-number>' --tick '<criterion-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-637.json --prs prs.json --links links.json --pr 950 --tick AC1 --fix fixed-637.md
```

##### 2. Write the Delivery Comment

Read the helper’s result as [Command result](#command-result) states, with its written body. Return an invocation failure before writing the comment, retaining any eligibility findings.

Write `Delivered by #<pull-request-number>.` to the output comment file, with the delivering pull request number.

##### 3. Return the Task Delivery Result

Return the body, the comment file and the eligibility findings. The caller saves the body, posts the comment file through [Comment on Issue](#comment-on-issue) and closes the tracker issue.

### Fields

#### Task Delivery Result

One task's delivery as recorded: the body with its delivering pull request and verified criteria ticked, a comment file reading `Delivered by #<pull-request-number>.`, and the eligibility findings stating whether the task is closable.

## Dependency Graph

### Fields

#### Numbering Map

A comma-separated list of `<old-number>:<new-number>` pairs assigning each old number one distinct new number. A number a pull request already names is preserved, and a row a pull request names is not renumbered. A source absent from the supplied files, or a duplicate destination, is refused.

## Initiative

### Operations

#### Check Initiative Completion

The initiative's normal delivery result before tracker closure.

**Inputs:** [Initiative issue](#issue-record), [Epic issues](#issue-record), [Criterion verification](#verification-evidence), [Issue-link snapshot](#issue-link-snapshot), [Pull request records](#pull-request-records)

**Outputs:** [Completion result](#delivery-state-1)

##### 1. Evaluate Initiative Delivery Evidence

Evaluate the current initiative, every linked epic's current record, the criterion verification, and the current Development links and linked pull request records against [Delivery State](#delivery-state-1).

##### 2. Identify Initiative Completion Blockers

Identify each missing, open or cancelled epic, each unverified or unticked criterion, and each unmerged or unreadable Development-linked pull request. Incomplete link evidence leaves completion unconfirmed.

##### 3. Return the Initiative Completion Result

Return the completion result and its supporting issue identities, evidence revisions and blockers. Passing normal delivery checks supplies the caller's closure evidence; the tracker issue's current Development-link gate still governs the write.

### Fields

#### Delivery State

The state records every linked epic's completion, each initiative criterion's verification and tick, and the complete Development-linked pull request set and merge states. Each finding retains its source identity and evidence revision.

An epic is delivered when its issue is closed as completed. A missing, open or cancelled epic remains undelivered, including when all initiative criteria are ticked. Criterion readiness and premature ticks are [Delivery Findings](#delivery-findings-1); delivery alone does not verify a criterion.

Initiative completion requires every linked epic to be closed as completed, every criterion verified and ticked, and every Development-linked pull request merged. Incomplete evidence leaves completion unconfirmed. The result names each missing condition.

#### Delivery Findings

| Finding | Condition in the Supplied Initiative and Epic Records |
| --- | --- |
| Ready to verify | The initiative criterion is unticked and every epic whose Coverage cites it is delivered. |
| Ticked early | The initiative criterion is ticked and an epic whose Coverage cites it is undelivered. |

Epic delivery follows [Delivery State](#delivery-state-1). Each finding names the criterion and the supporting or missing epic evidence.

## Pull Request Body

### Operations

#### Populate Review Body

The current change carried by one epic base.

**Inputs:** [Base change](#change-summary), [Task merges](#pull-request-records), [Existing review body](#review-body)

**Outputs:** [Review body](#review-body)

##### 1. Populate the Review Template

Populate the review body from the [Template](#template-2) using the actual task merges into the base.

- All populated fields must meet [Fields](#fields-14), including the review-specific requirements in [Review Body](#review-body).

##### 2. Update for a Later Task Merge

For a later task merge:

- Add its functional change under the corresponding area.
- Cite the merged task pull request as the next reference.

##### 3. Return the Updated Review Body

Return the complete updated body file to the caller.

### Fields

#### Template

````markdown
## Overview

{{One paragraph: what this pull request delivers and why.}}

## Changes

{{One sentence on what changed and why it was needed. Then one heading per area the changes sit in. A heading is two to five words, in title case, such as Queue Placement or Task Readiness. Under each heading, one bullet per functional change in that area. The bullet opens with a bold lead, as the scheme's Bold leads rule lays one out. The change is at most two lines, the lead included: the lead names what it does, and the behavior is the single line under it.}}

### {{Queue Placement}}

- **{{What it does.}}**
  {{The behavior as it is.}}

## Test Plan

| Test | Description | Coverage | Pass |
| --- | --- | --- | --- |
| T1 | {{Check name, per [Test Plan](#test-plan).}} | {{Observed criteria, if any.}} | [{{Result}}]({{Planning document URL#test-section}}) |

## Open Questions

- {{An undecided point. Resolve it, then delete the section.}}

## References

- **R1.** [{{Title}}]({{URL}}) — {{What the reader finds there. The issue this pull request delivers is not a reference: the Development field carries that link, as [Issue Links](pull-request.md#issue-links) state. Delete the section when there is none.}}
````

#### Titles

- A pull request's title starts with the epic it works on: `[I07:E00] Purpose`.
- A pull request working on no epic takes `Name: Subtitle`, with no prefix, as a revision of the skill itself does.
- The prefix is how an epic's pull requests are found, and each one, open or merged, is matched to the tasks it works on from its changes and the tasks' Descriptions.
- The pull request that merges an epic base carries the same prefix. Its head is the epic base, which tells it from a task pull request.

#### Review Body

- Overview is one paragraph on what the base carries.
- Changes holds one heading per area, with a bullet per functional change.
- References cites each task pull request merged into that base.
- It carries no Test Plan, since it delivers no task of its own, and no statement about what the epic has yet to deliver. The epic's Work Breakdown is where delivery state is read.

#### Test Plan

A task pull request carries a Test Plan.

- **Table.**
  The pull request's Test Plan section contains only one table, with columns Test, Description, Coverage and Pass, in that order.
- **Columns.**
  - Test names the id.
  - Description briefly names the check.
  - Coverage names the criteria the check observes, `AC1, AC3`, and is empty when the check observes none.
  - A row whose Test cell is empty names a criterion no check observes, and its Pass cell is empty.
  - Pass is empty while a check awaits a result. A recorded result uses ✓ when the check ran and held, or an accurate label such as Partial, Fail or Not run.
- **Evidence.**
  - Test procedures, tested revisions, observations, limitations and supporting evidence belong in the work's published planning document.
  - Each recorded result in Pass links to its relevant section in that document, using the result as link text: `[✓](URL#check)` or `[Partial](URL#check)`.
  - Each evidence link is accessible to the pull request's readers and resolves to the intended section.
- **Completion.**
  The test plan has passed when every row with a Test id carries ✓ as its result. Partial, failed and unexecuted checks remain incomplete.

#### Test Coverage

- Every criterion a unit's Coverage names has an observing test in its work item and pull request. A criterion no test can observe remains in the [coverage report](#coverage-reports) and in a test-plan row with an empty Test cell.
- The criterion selects the test kind: a unit test for one component, an integration test for a seam between components, and an end-to-end or system test for running-system behaviour. That evidence meets [Coverage Reports](#coverage-reports).
- An instrument that does not exist yet is work the task carries, as the verified rule defines. Use the project's own system test where it can observe the criterion.
- One row per check, in execution order, followed by any unobserved criteria. Every criterion in the unit's Coverage appears in at least one row.

#### Change Summary

The functional changes a pull request, or the epic base a review covers, carries, each placed under the area it sits in.

#### Body File

A local Markdown file at a given path holding one pull request body that meets [Template](#template-2).

# Configuration

### Labels

#### Kind Labels

The label naming an agent-engineering issue's kind.

| Kind | Label |
| --- | --- |
| Proposal | `type:proposal` |
| Initiative | `type:initiative` |
| Epic | `type:epic` |
| Task | `type:task` |

#### Theme Labels

The label naming the theme an initiative and its epics belong to: `theme:` and the theme's name in lowercase. This deployment's themes:

| Theme | Label | Description |
| --- | --- | --- |
| Canon | `theme:canon` | Definitions Checked Against the Design Canon |
| Language | `theme:language` | The Definition Language and Its Rules |
| Mechanical | `theme:mechanical` | The Engine That Runs Definitions |
| Delivery | `theme:delivery` | What Reaches Agents and Hosts |

# References

## Requirement Characteristics

The characteristics an acceptance criterion meets, and the characteristics a set of them meets. Condensed from ISO/IEC/IEEE 29148:2018, clauses 5.2.4 to 5.2.7.

### Individual

Each criterion has these characteristics.

- **Necessary.**
  It states a capability, constraint, or quality the work must have. Leaving it out leaves that need unmet, and no other criterion meets it. It applies now.
- **Appropriate.**
  The detail matches the level of the work. It states what holds, and does not lock in a design the need does not require.
- **Unambiguous.**
  It can be read in only one way.
- **Complete.**
  It states the condition fully. Knowing whether it holds does not depend on some other text.
- **Singular.**
  It states one capability, constraint, or quality. Several conditions under which that one thing holds are still one criterion.
- **Feasible.**
  It can be met within the cost, schedule, and technical bounds of the work, at an acceptable risk.
- **Verifiable.**
  Its wording lets the realisation be proved, at the level the criterion is written, by inspection, analysis, demonstration, or test. A measure makes that proof easier.
- **Correct.**
  It states the need it came from, accurately.
- **Conforming.**
  It follows the acceptance-criterion form: an end state, one invariant, and a named instrument.

### A Set

The criteria of one issue, taken together, have these characteristics.

- **Complete.**
  Together they state what the work must achieve. Nothing the set needs is left to be defined later.
- **Consistent.**
  No two conflict or overlap. The same word means the same thing throughout.
- **Feasible.**
  The set can be met within the same cost, schedule, and technical bounds, at an acceptable risk.
- **Comprehensible.**
  A reader can see what the work is expected to achieve, and how that sits with the rest of the plan.
- **Able to be validated.**
  Meeting the set achieves the need the plan states, within its constraints.

### Wording

- **What, not how.**
  A criterion states the condition that holds. A design choice belongs in the Proposal.
- **Bounded words.**
  These make a criterion hard to prove, or open to more than one reading, unless a measure defines them:
  - superlatives, such as best or most;
  - subjective praise, such as easy or robust;
  - vague pronouns, such as it or this;
  - open comparatives, such as better or significant;
  - loopholes, such as if possible or as appropriate;
  - words of totality, such as all, always, or never, unless the set they cover is named;
  - an open-ended promise, such as provide support.
- **Assumptions.**
  An assumption is recorded beside the criterion, in the Problem or the Proposal. It is not written as the criterion.
- **Definitions.**
  A definition is a statement of what a term means. It is not a criterion.
