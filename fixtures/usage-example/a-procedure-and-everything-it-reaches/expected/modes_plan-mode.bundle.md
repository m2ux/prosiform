# Prosiform

## Dispatch

Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Plan Mode

Scopes the solution: the design, the criteria, and the breakdown of an initiative and its epics, and keeps them current as work lands.

Follow the [Procedure](#procedure), adhering to [Rules](#rules) and [Conventions](#conventions) and ensure all [Outcomes](#outcomes) are met.

## Procedure

### 1. Take the Proposal

- When the user names a proposal, its associated issue body defines the problem scope.
- When the user names an initiative that already exists, fetch its body with [Read Tracker Issue](#read-tracker-issue). That body defines the problem scope, and no proposal is raised for work it already carries.
- When neither a proposal nor an existing initiative is named:
  - Follow [Propose Mode](#propose-mode) with the user's goal.
  - Resume this selection step with its published proposal; an unresolved proposal blocks initiative drafting.

### 2. Prepare the Planning Record

- For an initiative, epic or complex plan, apply [Populate Planning Record](#populate-planning-record) with the record identity, folder and supplied evidence files.
- For initiative or epic planning:
  - Populate a discussion body through [Populate Pull Request Body](#populate-pull-request-body).
  - Apply [Publish Pull Request](#publish-pull-request) as a draft with the planning branch, target, title and body file. Only the user decides to merge that discussion pull request.

### 3. Draft Each Initiative Body

- For a new initiative, obtain its proposed prefix through [Select Tracker Number](#select-tracker-number) with the initiative prefix letter.
- Apply [Draft Initiative Issue Body](#draft-initiative-issue-body) for each initiative with the scoped proposal, confirmed goal clauses, requirement sources, epic summaries and output path.

### 4. Populate the Epics

Apply [Populate Epic Issue Body](#populate-epic-issue-body) for each epic and each new task row.

- Apply [Populate Work Item](#populate-work-item) for each task with its scope, design, the component its implementation extends, criteria and test requirements.
- Apply Populate Planning Record with the record identity, folder path and each returned work-item file.
- Apply [Check Dependencies and Numbering](#check-dependencies-and-numbering) with the initiative and epic drafts, the planning record, current pull request records, confirmed numbering maps when any, no allowance and the run's change list.
- Apply Populate Planning Record with the record identity, folder path and the returned longest chains, contending pairs and proposed [Epic Priority](#epic-priority) map as its [Dependency Check](#dependency-check).
- Return each checked epic draft and its format results to [5. Review the Drafts](#5-review-the-drafts).

### 5. Review the Drafts

Apply [Review Initiative Goal](#review-initiative-goal) with the initiative and epic drafts, confirmed goal clauses, marked sources and the epic format results.

- Apply Populate Planning Record with the record identity, folder path and the returned trace table as its [Goal Trace](#goal-trace). With no planning record, give the trace table to the user.
- Apply [Report Review Finding](#report-review-finding) for each returned finding, with its scope, evidence and proposed resolution.
- Apply each confirmed resolution to the drafts:
  - For a local epic finding, apply Populate Epic Issue Body with the confirmed Proposal, row and criterion changes, including every new or renumbered criterion in Coverage.
  - For a confirmed distinct concern:
    - Apply Populate Epic Issue Body for its own epic.
    - Apply Draft Initiative Issue Body with the epic summaries that include it.
    - Repeat Check Dependencies and Numbering for the new epic and initiative row, and record its result as [4. Populate the Epics](#4-populate-the-epics) does.
- Apply Populate Planning Record with the record identity, folder path and each finding, resolution and decision.
- Repeat Review Initiative Goal with the revised initiative and epic bodies and retained goal clauses and sources. No issue is created while a content or structural finding remains. Unresolved links to unpublished issues are recorded with their intended row identities and resolved during publication; no other finding is deferred.

### 6. Publish

Put the proposed [Epic Priority](#epic-priority) map for the reviewed epics to the user as an [interview](#rules), the proposal the recommended answer.

- Take the positive integer the user confirms for each epic.
- Follow [Initiative Publication](#initiative-publication) with the repository, initiative prefix letter, the reviewed initiative and epic body files with their existing issue numbers, titles and labels, each epic's confirmed [priority label](#priority-sets) among them, each label's colour and description, the current pull request records, corpus branch and requirement sources, the kind templates, the record identity, folder path, evidence and decisions, and a commit message file.
- Put each blocker it returns to the user.

### 7. Keep the Goal Current

When the goal, a criterion, a Problem, a Proposal or an epic changes:

- Repeat Review Initiative Goal with the revised bodies and current sources, and record its trace table as [5. Review the Drafts](#5-review-the-drafts) does.
- Apply Report Review Finding for each finding.
- Apply confirmed resolutions as [5. Review the Drafts](#5-review-the-drafts) does.
- Repeat that review until clear.
- After each round, apply [Check Round of Edits](#check-round-of-edits) to affected bodies.
- Whenever tasks, edges or a work item's component change, repeat Check Dependencies and Numbering, and record its result as [4. Populate the Epics](#4-populate-the-epics) does.
  - Put the proposed Epic Priority map to the user again where the edges or the contention moved an epic's number.
  - Apply [Save Tracker Issue](#save-tracker-issue) with each confirmed change as that epic's [priority label](#priority-sets), with its colour and description.
- Apply Save Tracker Issue with each affected body, its title matching current numbers.
- Keep local body files as the source for the next pass.
- Apply Populate Work Item for each added or renamed task.
- Apply Populate Pull Request Body with the discussion pull request's current body.
- Apply Publish Pull Request with the discussion pull request's number and the returned body file.
- Apply Populate Planning Record with the record identity, folder path, each added or renamed task's work-item file, each removed task's work-item file as removed, and a commit message file, asking it to publish.

### 8. Prepare Epic Delivery

Before any task starts:

- Apply [Resolve Open Questions](#resolve-open-questions) for each affected issue with its identity, current JSON, its kind's template and field conditions, related context and an output body path.
  - Apply Populate Planning Record with each decision it returns.
  - Stop on a question it leaves open.
- Apply [Apply Body Corrections](#apply-body-corrections) to each body with a criterion joining several conditions, with the split criteria at the end of the list and their Coverage as [Shared Acceptance Criteria](#shared-acceptance-criteria) states.
  - Apply Save Tracker Issue with each returned body.
- Follow [Delivery Base Preparation](#delivery-base-preparation) with the initiative's epics, the current initiative and epic bodies, prerequisite issue and base-merge records, project checkout, changed long-lived branches, repository and initiative prefix.
  - Stop on a prerequisite finding it returns.
  - Put each conflict and pull request awaiting a decision it returns to the user.
- Repeat goal and ordering review on changed bodies, as [7. Keep the Goal Current](#7-keep-the-goal-current) does, before returning readiness.

### 9. Record Delivered Work

When work has landed:

- Follow [Sync Mode](#dispatch-sync-mode) for the affected initiative.
- For each unplaced task row it returns pending:
  - Apply [Place Unplaced Task Row](#place-unplaced-task-row) with the epic JSON, that task issue, no allowance, the returned change list and delivery evidence, and an output body file.
  - Repeat Sync Mode with the refreshed epic.
- Return the saved delivery state or blockers.

#### Dispatch Sync Mode

Dispatch `modes_sync-mode.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states.

## Outcomes

- **A scoped initiative.**
  The user has an initiative scoped to the proposal they named, or to a proposal raised for that problem.
- **Several initiatives.**
  One proposal may become several initiatives. A partition by solution maturity, such as an MVP demo, a functional prototype, and a production-intent version, is an example of that result. Those initiatives may run in series or in parallel. The example does not limit the partition.
- **A goal made true.**
  Each clause of the goal the user confirmed is made true by the initiative's criteria, and the epics the initiative lists are the work that delivers those criteria.
- **Epics that start together.**
  The user has settled which of the initiative's epics start alongside each other, from a proposal the dependency graph makes.
- **Review before creation.**
  Findings on that initiative are folded in before any of its issues are created.

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

#### Select Tracker Number

The next unused number for one prefixed issue kind in the repository.

**Inputs:** [Repository](#tracker-repository), [Prefix letter](#tracker-prefix)

**Outputs:** [Tracker number](#tracker-prefix)

##### 1. List the Prefixed Titles

From the repository checkout, list titles in all issue states using the supplied repository and kind’s prefix letter.

```bash
gh api --paginate 'repos/<owner>/<repository>/issues?state=all&per_page=100' --jq '.[] | select(.title | test("^\\[<prefix-letter>[0-9]{2}\\]")) | .title'
```

**Example:** Initiatives in one repository.

```bash
gh api --paginate 'repos/m2ux/workflow-server/issues?state=all&per_page=100' --jq '.[] | select(.title | test("^\\[I[0-9]{2}\\]")) | .title'
```

##### 2. Read the Highest Prefix

Read the result of each command in the preceding step as [Command result](#command-result) states.

Read the highest prefix carrying that letter.

##### 3. Confirm the Next Number Is Unused

Confirm the following number, or `00` when there is no prefix, remains unused before creation.

##### 4. Return the Tracker Number

Return the confirmed number.

### Fields

#### Observed Development Links

Every linked pull request URL in an issue's Development field, across repositories and states, and whether the entire field was readable.

#### Tracker Repository

The repository whose tracker holds the issues: its owner and name, written `<owner>/<repo>`.

#### Issue Identity

One issue's [repository](#tracker-repository), number and URL. An issue yet to be created has its repository alone. An unresolved identity names the repository and the title prefix that matched no issue.

#### Issue Content

An issue's title, body and labels. The title meets [Titles](#titles-3), the body is a [body file](#body-file-3), and each label is a [repository label](#label-identity). The saved title, body and labels equal the supplied values.

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

## Planning Record

### Operations

#### Populate Planning Record

One planning directory and its artifact inventory.

**Inputs:** [Record identity](#record-folder), [Folder path](#record-folder), [Artifact files](#artifacts-1), [External links](#links), [Removed artifacts](#artifacts-1), [Commit message](#commit-message)

**Outputs:** [Folder path](#record-folder), [Publication](#publication)

##### 1. Prepare the Selected Planning Record

For a new record, run this command from the engineering worktree with the caller-composed [Record Folder](#record-folder) path.

```bash
mkdir -p '<planning-folder-path>'
```

**Example:**

```bash
mkdir -p artifacts/planning/2026-10-15-950-queue-plan
```

##### 2. Populate the Record Entry Point

For a new record, inspect the folder-creation result. Return any error without writing or publishing further files. On success, populate README.md from the [Template](#template).

For an existing record, read its README, retaining its creation date, other artifacts and links.

- Update only the supplied content.

For either kind of record, the folder must meet [Layout](#layout), and every populated README field must meet [Fields](#fields-1).

##### 3. Register the Supplied Artifact Files

Register the artifact files supplied by the caller, using their chosen names.

- Each file must have a row meeting [Layout](#layout) and [Artifacts](#artifacts-1).
- File content remains supplied by the caller; this operation does not author that artifact's content.
- Delete each artifact the caller names as removed, with its row.

##### 4. Publish the Populated Planning Record

When the caller asks to publish, apply [Publish Planning Record](#publish-planning-record) with the folder path, the files this call wrote and the commit message file.

##### 5. Return the Planning Record Folder

Return the folder path, and the publication result when it published.

#### Publish Planning Record

The record's folder committed and pushed, so every link into it resolves for a reader.

**Inputs:** [Folder path](#record-folder), [Record files](#layout), [Commit message](#commit-message)

**Outputs:** [Publication](#publication)

##### 1. Find the Publishing Worktree

From any project checkout, list the worktree for the configured [engineering branch](#engineering-branch).

- The engineering branch has one long-lived worktree and takes no further one.

```bash
git worktree list | grep '\[<engineering-branch>\]'
```

##### 2. Commit the Planning Record Folder

Inspect the worktree lookup. Return a lookup error or missing-worktree finding before any write. Use the returned path as `<engineering-worktree>`.

Stage and commit the supplied folder with the supplied message file. Resolve the message file against the engineering worktree, or pass its absolute path.

- Staging and committing are one call, and the commit names its folder, so a concurrent session's staged work cannot ride along. See [Shared Worktree](#shared-worktree).
- Pass the message as [Bodies](#bodies) states. The worktree is a linked one, so git writes here run unsandboxed.

```bash
cd '<engineering-worktree>' && git add '<planning-folder-path>' && git commit -F '<message-file>' -- '<planning-folder-path>'
```

**Example:**

```bash
cd .engineering && git add artifacts/planning/2026-10-15-950-queue-plan && git commit -F msg.txt -- artifacts/planning/2026-10-15-950-queue-plan
```

##### 3. Push the Engineering Branch

Inspect the commit result; return a failure without pushing. Confirm the commit holds the files this record wrote, meeting [Shared Worktree](#shared-worktree), then push from the engineering worktree.

- Planning records go straight to the branch; they take no pull request.

```bash
cd '<engineering-worktree>' && git push
```

##### 4. Return the Publication Result

Inspect the push result. Report a non-fast-forward refusal or other push failure without rewriting the branch. Return the published commit and record path only after a successful push.

### Fields

#### Template

```markdown
# [Descriptive name] — [Month Year]

> [Classifier] · Created [YYYY-MM-DD]

## Executive Summary

[Two paragraphs on the purpose of this work and why it matters.]

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Name](file.md) | What this artifact holds |

## Links

| Resource | Link |
| --- | --- |
| [External reference] | [link] |
```

#### Shared Worktree

The engineering branch has one worktree and every session writes its records there, so they share one index. A commit therefore names the folder it is for, and a session confirms its own files landed in its own commit rather than assuming the index held only its staging.

#### Layout

README.md is the one file the folder must hold. Any file beyond README.md is added as the work needs it.

```text
./
├── README.md
└── …
```

Each file beyond README.md is a row in the README's Artifacts.

An overview record explains one pull request's change. Its folder's reference is the pull request number and its slug comes from the pull request's title. A pull request has one overview record, and a later overview of it reuses that folder.

#### Header

One blockquote: the classifier, the day the record was created, and a revised date when the README is updated after the work is done.

#### Executive Summary

Two paragraphs: the purpose of this work, and why it matters.

#### Artifacts

- One row for every artifact in the record other than README.md, added when the file is produced and removed with it.
- The link sits on the artifact's name. The row says what the artifact holds, and the artifact is the home of that content.
- In an overview record, the architecture overview is the one row, and its pull request is under Links.

#### Dependency Check

`dependencies.md`, an Artifacts row: the longest chains, contending pairs and proposed epic priority map the initiative's latest dependency check printed. A later check replaces it.

#### Goal Trace

`goal-trace.md`, an Artifacts row: the trace table of the initiative's latest goal review. A later review replaces it.

#### Links

External references only: a tracker issue, a parent epic, a pull request. An artifact of this plan is an Artifacts row.

#### Record Folder

- `<planning-folder-path>` is `<records-folder><yyyy-mm-dd>[-<ref>]-<slug>/`, under the [records folder](#engineering-branch). The date is the day the record is opened.
- `<ref>` is the bare number of the issue or the pull request the record is for. A record for ad hoc work, which has neither, has no ref segment.
- The slug is lowercase words separated by hyphens, a short name of the work.
- The folder's files are the [planning layout](#layout).
- Edits are made on that worktree. The engineering branch takes no further worktree and no branch.

One planning record's folder, at `<records-folder><yyyy-mm-dd>[-<ref>]-<slug>/` under the [records folder](#engineering-branch). The date is the day the record opened. The reference is the bare number of the issue or pull request the record is for, absent for ad hoc work. The slug is lowercase hyphenated words naming the work. The folder's name is the record identity.

#### Commit Message

A file holding the message of the commit that publishes the record, as [Bodies](#bodies) states.

#### Publication

The engineering-branch commit holding the record's folder, pushed to its remote.

## Pull Request Body

### Operations

#### Populate Pull Request Body

One pull request body from supplied change and validation evidence.

**Inputs:** [Change summary](#change-summary), [Delivery scope](#scope), [Validation evidence](#test-plan), [Current body](#body-file), [Output body file](#body-file)

**Outputs:** [Pull request body](#body-file), [Unresolved evidence links](#test-plan)

##### 1. Populate the Pull Request Template

Populate the body from the [Template](#template-1) using the change and its evidence, using [Populate Review Body](#populate-review-body) for an epic review.

- Start from the current body when one is supplied.
- All populated fields must meet [Fields](#fields-2).

##### 2. Verify the Test Result Links

Verify each result link against [Test Plan](#test-plan) before publishing the body.

##### 3. Return the Pull Request Body

Return the complete body file and any unresolved evidence links to the caller for publication.

#### Populate Review Body

The current change carried by one epic base.

**Inputs:** [Base change](#change-summary), [Task merges](#pull-request-records), [Existing review body](#review-body)

**Outputs:** [Review body](#review-body)

##### 1. Populate the Review Template

Populate the review body from the [Template](#template-1) using the actual task merges into the base.

- All populated fields must meet [Fields](#fields-2), including the review-specific requirements in [Review Body](#review-body).

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

A local Markdown file at a given path holding one pull request body that meets [Template](#template-1).

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

**Inputs:** [Repository](#repository-1), [Initiative prefix](#titles-1), [Records path](#pull-request-records)

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

#### Align Pull Request Base

Each open delivery pull request pointed at the base its head requires.

**Inputs:** [Repository](#repository-1), [Pull request records](#pull-request-records), [Long-lived branches](#branches), [Epic bases](#epic-bases), [Project checkout](#project-checkout)

**Outputs:** [Alignment result](#alignment-result)

##### 1. Take Each Pull Request Target

Take the target of each open pull request in the current records from [Scope](#scope) and [Other Pull Requests](#other-pull-requests), with each long-lived branch as [Epic Bases](#epic-bases) names it.

- Report an open pull request for which neither field gives a target for the user's decision, and leave it unchanged.

##### 2. Retarget Mismatched Pull Requests

For each open pull request whose base differs from its target, apply [Publish Pull Request](#publish-pull-request) with its number and that target as the base change.

##### 3. Update Unmergeable Task Branches

For each task pull request whose saved state is not mergeable, apply [Update Task Branch](#update-task-branch) with the worktree [Task Branches](#task-branches) places under the project checkout, its task branch and its epic base.

- A conflict leaves the pull request open and is reported.

##### 4. Return the Alignment Results

Return the retargeted pull requests, updated task branches, conflicts and the pull requests awaiting a decision.

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

The fields a publication writes: a body file at its path, meeting [Template](#template-1), its title, head and base. A change to an existing pull request names only the fields it changes.

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

#### Alignment Result

The pull requests retargeted, the task branches updated, the conflicts met, and the pull requests whose target awaits the user's decision.

## Initiative Issue Body

### Operations

#### Draft Initiative Issue Body

One initiative body, scoped to one proposal.

**Inputs:** [Scoped proposal](#template-5), [Goal clauses](#goal-clauses), [Requirement sources](#sources), [Epic summaries](#work-breakdown), [Output body file](#body-file-1)

**Outputs:** [Initiative body](#body-file-1)

##### 1. Copy the Initiative Template

Populate the body from the [Template](#template-2) into a local file at the supplied output path.

- That file must be the source for every later edit.
- All populated fields must meet [Fields](#fields-4).

##### 2. Derive Problem and Non-Goals

Derive the Problem and Non-Goals from the proposal this initiative is scoped to.

- The Problem must meet [Problem and Proposal](#problem-and-proposal).
- Each Non-Goal must meet [Non-Goals](#non-goals).

##### 3. Write Initiative Acceptance Criteria First

Write the acceptance criteria before the Work Breakdown, so each row's Coverage can cite them.

- Each criterion must come from a confirmed clause and meet [Initiative Acceptance Criteria](#initiative-acceptance-criteria).
- The criteria must come from the requirements sources the proposal references. Where the proposal references none, they must come from the proposal's body alone.

##### 4. Write the Shared Initiative Table

Populate the shared table through [Write Issue Table](#write-issue-table).

##### 5. Fill the Initiative-Specific Cells

Fill the initiative-specific cells.

- Each row must meet [Work Breakdown](#work-breakdown).
- An item a test cannot observe must stay named as [Coverage Reports](#coverage-reports) define.

#### Resolve Placeholder Links

Saved issue identities in the links an initiative and its epics carry before their issues exist.

**Inputs:** [Initiative body](#body-file-1), [Epic bodies](#body-file-2), [Saved issues](#issue-record)

**Outputs:** [Initiative body](#body-file-1), [Epic bodies](#body-file-2), [Unresolved links](#temporary-links)

##### 1. Replace Temporary Issue Links

Replace every temporary link in the initiative and epic body files with the saved issue identity it stands for.

- Each epic row of the initiative must meet [Work Breakdown](#work-breakdown).
- Each row reference in an epic must meet the epic's [Work Breakdown](#work-breakdown-1).

##### 2. Confirm No Temporary Link Remains

Confirm no temporary link remains in any of those files.

##### 3. Return the Rewritten Body Files

Return the rewritten body files and each temporary link left unresolved, with the file that holds it.

#### Validate Initiative Body

The body's local format and field findings.

**Inputs:** [Initiative issue](#issue-record), [Epic issues](#issue-record), [Source evidence](#source-evidence), [Output body file](#body-file-1)

**Outputs:** [Initiative body](#body-file-1), [Validation findings](#format-findings)

##### 1. Validate the Initiative Issue Body

Apply [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#fields-4), supplied related evidence and output file, supplying each linked epic as `--epic`.

##### 2. Title the Initiative Row

Use its current title for the initiative row.

##### 3. Report Excluded Names and Departures

Include excluded names in Problem and Proposal and criterion/source departures in the findings.

##### 4. Return the Validated Initiative Body

Return the corrected body, mechanical diff and unresolved findings for the caller.

#### Read Requirement Sources

The requirements evidence used to validate an initiative's criteria.

**Inputs:** [Initiative references](#references), [Source files](#source-evidence)

**Outputs:** [Source evidence](#source-evidence)

##### 1. Read Local Requirement Sources

Read each local source at its checkout path.

##### 2. Fetch Pinned GitHub Sources

For a pinned GitHub blob, fetch its content from the repository checkout using the repository owner and name, source path, pinned revision and destination file. URL-encode the path and revision for the request.

```bash
gh api 'repos/<owner>/<repository>/contents/<source-path>?ref=<revision>' --jq .content | base64 -d > '<source-file>'
```

**Example:**

```bash
gh api 'repos/m2ux/workflow-server/contents/docs/spec.md?ref=4a217fe6' --jq .content | base64 -d > source-R1.md
```

##### 3. Fetch Other Source URLs

Read each pinned-source command’s result as [Command result](#command-result) states. Carry a failed or empty response into the unreadable-source findings below.

Fetch other URLs through the harness's web access.

##### 4. Record Unreadable Sources

Record an unreadable or empty source as a [Sources](#sources) finding; its criteria remain unevaluated.

##### 5. Return the Requirement Source Contents

Return each source's contents and identity with those findings.

### Fields

#### Body File

A local Markdown file at a given path holding one initiative body that meets [Template](#template-2).

#### Temporary Links

Each placeholder for an unsaved initiative or epic issue, with the body file containing it and the intended issue identity.

#### Source Evidence

Each marked [source](#sources), its identity and contents, the local file path holding those contents, and any unreadable or empty-source finding.

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

#### Problem

- A Problem meets [Problem and Proposal](#problem-and-proposal).

#### Proposal

- A Proposal states the design, as [Problem and Proposal](#problem-and-proposal) defines.
- A Proposal names no epic, task, or acceptance criterion of its own initiative.

#### Work Breakdown

The columns are `Epic | Description | Coverage | Depends on | Done`. The table has no Joins column.

- The body meets [Breakdown Prose](#breakdown-prose-1).
- An epic row's id is the epic, linked to its issue: `[E01](…/issues/937)`.
- An epic row's Description is the epic's title name, and its Coverage names the initiative criteria the epic serves.
- An epic row is complete when its issue is closed as completed.
- Depends on names epics only. A cell that names a task fails. Name a prerequisite epic only when every task or joined unit in the dependent epic requires every task in that prerequisite epic, directly or through its dependencies. The consumed output and the work producing it establish that requirement. Dependencies on selected tasks remain in the task tables. An edge another named whole-epic prerequisite already implies is omitted.
- An initiative dependency that only some tasks need, or that requires only part of its prerequisite epic, is overbroad. The output and its producing tasks establish the edge.
- An epic depending on a later epic is a backward reference.
- Epic numbering meets [Numbering](#numbering).

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

#### Non-Goals

- One succinct sentence each on what the initiative does not do, naming no initiative, epic, task or issue, and no owner.

#### References

- A proposal-derived initiative identifies its originating proposal in References with the proposal's exact title and issue URL, labelled as the originating proposal.
- A reference the criteria answer to carries **Source.** after its label: `- **R1.** **Source.** [Title](url) — what it binds`. An unmarked reference is background, and binds no criterion. What a marked one requires of the criteria is [Sources](#sources).
- A cross-initiative overlap is recorded in References. An approved edit to another initiative's issue stays minimal.

#### Sources

A marked source in References is a document the initiative's criteria answer to. The criteria are aligned with it in both directions.

- A criterion that misstates or contradicts a marked source fails the [Correct](#individual) characteristic.
- A requirement a marked source states that no criterion makes true, and no Non-Goal excludes, is a gap.
- A departure from a marked source is corrected in the criterion, unless a Non-Goal records it.
- An epic is aligned against its initiative's marked sources, through the initiative criteria its row covers.
- A marked source that cannot be read leaves its criteria unaligned until it is read.

#### Deferred Debt

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
  It takes its bases from the long-lived branches its rows change, carries the [corpus audit](#corpus-audit) criterion where those rows change workflow definitions, and remains open until every delivery base has merged and its completion conditions hold.
- **The initiative stays open while it stands.**
  Its row is undelivered and its criterion unticked until the epic closes.

#### Breakdown Prose

Work Breakdown contains its table. Explanatory prose belongs in Proposal. The body does not narrate execution order or how the tables work; Depends on carries the order.

## Epic Issue Body

### Operations

#### Populate Epic Issue Body

One epic body and its local validation findings.

**Inputs:** [Initiative issue](#issue-record), [Epic scope](#epic-scope), [Pull request records](#pull-request-records), [Corpus branch](#branches), [Output body file](#body-file-2)

**Outputs:** [Epic body](#body-file-2), [Draft rows](#work-breakdown-1), [Validation findings](#format-findings), [Unresolved links](#temporary-links)

##### 1. Draft the Epic Body

Populate the body from the [Template](#template-3) at the supplied output path.

- Every section must meet [Fields](#fields-5).
- Shared content must meet the common [body conditions](#fields-11).

##### 2. Write the Shared Epic Table

Populate the shared table through [Write Issue Table](#write-issue-table).

##### 3. Fill the Epic-Specific Cells

Fill the epic-specific cells.

- Each row must meet [Work Breakdown](#work-breakdown-1).

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

**Inputs:** [Epic issue](#issue-record), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Task issues](#issue-record), [Task matches](#task-matches), [Project checkout](#project-checkout), [Output body file](#body-file-2)

**Outputs:** [Epic body](#body-file-2), [Delivery findings](#delivery-findings)

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
- Row changes must meet [Task Delivery](#task-delivery) and [Work Breakdown](#work-breakdown-1).

##### 2. Return the Epic Delivery Findings

Read the helper’s result as [Helper result](#helper-result) states, retaining its reported findings or refused criteria.

Return the updated body and [Delivery Findings](#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.

#### Validate Epic Body

The body's local format and field findings.

**Inputs:** [Epic issue](#issue-record), [Initiative issue](#issue-record), [Pull request records](#pull-request-records), [Corpus branch](#branches), [Output body file](#body-file-2)

**Outputs:** [Epic body](#body-file-2), [Validation findings](#format-findings)

##### 1. Validate the Epic Issue Body

Apply [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#fields-5), supplied related evidence and output file, supplying initiative JSON as `--initiative`, current pull request records as `--prs` and corpus branch as `--corpus`.

##### 2. Read Epic Pull Request Reach

Read reach from each epic pull request's base, through an epic base or initiative branch. Without both pull requests and the corpus branch, reach is unevaluable.

##### 3. Report Corpus Audit and Coverage Gaps

Include a missing [Corpus Audit](#corpus-audit) criterion on a corpus-changing epic and any epic criterion no task row delivers in the findings.

##### 4. Return the Validated Epic Body

Return the corrected body, mechanical diff and unresolved findings for the caller.

#### Revise Epic Rows

One epic body with confirmed task-grain and coverage corrections.

**Inputs:** [Epic body](#body-file-2), [Row changes](#work-breakdown-1), [Field findings](#field-findings), [Dependency references](#work-breakdown-1), [Output body file](#body-file-2)

**Outputs:** [Epic body](#body-file-2), [Numbering changes](#numbering-map), [Dependency changes](#work-breakdown-1)

##### 1. Apply the Confirmed Row Changes

Apply the confirmed row changes through [Populate Epic Issue Body](#populate-epic-issue-body), preserving unrelated content.

- Description, Coverage, Depends on, Joins and task grain must meet [Work Breakdown](#work-breakdown-1).
- Split a task exceeding the allowed criterion grain into the confirmed tasks.

##### 2. Return the Revised Epic Body

Return the revised body and any cross-body numbering or dependency changes for the caller.

#### Place Unplaced Task Row

One epic body given the row its table lacks for a task issue of the epic.

**Inputs:** [Epic issue](#issue-record), [Unplaced task issue](#issue-record), [Allowance](#allowance), [Change list](#change-list), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Task issues](#issue-record), [Task matches](#task-matches), [Project checkout](#project-checkout), [Output body file](#body-file-2)

**Outputs:** [Saved epic issue](#issue-record), [Epic body](#body-file-2), [Delivery findings](#delivery-findings), [Change list](#change-list)

##### 1. Draft the Unplaced Task Row

Draft the task issue's row, meeting [Work Breakdown](#work-breakdown-1).

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

- The body meets [Breakdown Prose](#breakdown-prose-1).

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

A local Markdown file at a given path holding one epic body that meets [Template](#template-3).

#### Epic Scope

The work one epic takes: its slice of the initiative's design, its title and labels meeting [Titles](#titles-2), its [acceptance criteria](#acceptance-criteria), and its proposed task rows meeting [Work Breakdown](#work-breakdown-1).

#### Release Decision

The user's explicit decision to release the hold on named task rows, naming each task id it releases.

#### Gap Disposition

Each criterion a delivered row left unmet, with its missing evidence and one disposition:

- **Holds.** The user confirms it already holds; the delivered task retains it, awaiting verification and ticking.
- **Further task.** A further task row adopts it, meeting [Task grain](#work-breakdown-1).
- **Pending.** The decision or the further task's draft is unanswered.

## Work Item

### Operations

#### Populate Work Item

One task's local implementation plan.

**Inputs:** [Task id](#identity), [Task scope](#work-breakdown-1), [Epic context](#template-3), [Design](#sections), [Component](#component), [Criteria](#acceptance-criteria), [Test requirements](#test-coverage), [Work-item path](#identity)

**Outputs:** [Work item](#template-4)

- Write the supplied task's file from [Template](#template-4), returning its path for registration in the planning record.
  - Its name and content must meet [Identity](#identity) and [Sections](#sections).
  - The supplied component must meet [Component](#component).
  - The test row must meet [Test Coverage](#test-coverage), using the supplied criteria without copying them into the file.

### Fields

#### Template

````markdown
**Component:** {{The one component this task's implementation extends}}

## Overview

{{What this task delivers and why.}}

## Problem

{{The present friction.}}

## Proposal

{{The scene, then the design. Lists of distinct items use bullets.}}

## Work Breakdown

| Part | Description |
| --- | --- |
| Analysis | {{The evidence to gather}} |
| Plan | {{The decisions and design}} |
| Implementation | {{The work to perform}} |
| Review | {{The review of that work}} |
| Test | {{The checks required by the work, including the project's system test when applicable}} |
````

#### Identity

One file per task, named for its id in lowercase, such as `w01.md`. The record's README links each file. The file names no other task and carries no acceptance criteria, Coverage, dependency or Joins; those belong to the epic table.

#### Component

One declaration line ahead of the first heading, naming the single component the Implementation part extends as the path to it in the repository that holds it.

- A task that creates the component names the path it creates.
- A task whose implementation extends more than one component is split into a task for each.

#### Sections

- Component names the component the Implementation part extends, meeting [Component](#component).
- Overview states what the task delivers and why.
- Problem and Proposal meet [Problem and Proposal](#problem-and-proposal); the Proposal starts with the scene.
- Work Breakdown decomposes the work into parts, such as analysis, plan, implementation, review and test. Its columns are Part and Description. The test row names the checks required by the work.

## Dependency Graph

### Operations

#### Check Dependencies and Numbering

The task graph and the row numbers it permits, checked and renumbered across the supplied bodies.

**Inputs:** [Initiative body](#template-2), [Epic bodies](#template-3), [Planning records](#artifacts-1), [Pull request records](#pull-request-records), [Numbering maps](#numbering-map), [Allowance](#allowance), [Change list](#change-list), [Outside files](#outside-files)

**Outputs:** [Dependency report](#dependency-report), [Change list](#change-list)

##### 1. Gather Bodies and Check Dependencies

Use the supplied local drafts when reviewing unpublished work.

- For published issues, fetch the initiative and each epic body with [Read Tracker Issue](#read-tracker-issue).
- Read each task row's work-item file from the planning record that registered it, as its [Artifacts](#artifacts-1) list it. The record holds one per task whatever that row currently links, so contention is measured rather than reported as unchecked.

From `<workspace>`, check dependencies using the initiative body, every epic id and body, every task id and work-item file read, and each planning-record file accounting for independent pairs.

- Keep `I=` for the initiative. Repeat the `<epic-id>=<epic-body-file>` argument once per epic, the `<epic-id>:<task-id>=<work-item-file>` argument once per work item, and `R=<record-file>` once per record.

- Initiative edges follow the [whole-epic prerequisite rule](#work-breakdown); narrower dependencies stay in the task graph.
- It also reports dependencies listed twice or already implied, and Joins pairs.
- It prints each pair of tasks in an epic where neither depends on the other, the two do not name each other in Joins, and no `R=` record accounts for the pair. Each line names both resolutions, as [Joins](#joins) states. A record accounts for a pair by naming both ids on one of its lines, and an `R=` file it cannot read is a problem.
- An entry it cannot resolve is a problem naming the entry as written, as [Edges](#edges) states. Its second clause says what this run could not find, which is the epics it was given.
- It prints each pair of rows in different epics whose work items declare one component, meeting [Component Contention](#component-contention), and names the rows it was given no work item for, so a partial report says what it passed over.
- A task row naming an epic rather than the rows it consumes is a problem, as [Edges](#edges) states. That row still reaches the epic's rows, so a body carrying the retired form is reported once rather than taking its initiative's gates down with it.
- It reads a declared component without its link, a wrapping code span, a trailing full stop or a leading `./`, and reports a work item it cannot read.
- It prints the proposed [Epic Priority](#epic-priority) of each epic, largest first.
- It reads bodies from [Read Tracker Issue](#read-tracker-issue), or local drafts.

Runs as [Helper invocation](#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deps.py 'I=<initiative-body-file>' '<epic-id>=<epic-body-file>' '<epic-id>:<task-id>=<work-item-file>' 'R=<record-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deps.py I=/drafts/live-936.md E00=/drafts/live-943.md E01=/drafts/live-937.md E00:W01=/drafts/e00/w01.md E01:W01=/drafts/e01/w01.md R=/records/joins.md
```

##### 2. Settle Dependency Findings

Read the dependency checker’s result as [Command result](#command-result) states. Treat reported dependency or numbering problems as findings to settle; return an unreadable input as a blocker.

Settle each finding through [Settle Plan Change](#settle-plan-change), with the correction below as its recommended option, the affected issue identities, the supplied allowance and the current change list.

- The correction each finding takes:
  - Name the producing row for each consumed output, meeting [Edges](#edges), replacing an epic a task row names with the rows the task consumes.
  - Read tasks for implied consumption edges.
  - Account for every independent pair as [Joins](#joins) states.
  - Account for every contending pair as [Component Contention](#component-contention) states: the proposed map separates the two epics by a number, or the contending rows move into one epic.
  - Resolve backward references by moving work to the epic owning its inputs, or removing duplicate work already owned there. Work claimed twice has one owner and a boundary in both bodies.
- Make the correction Settle Plan Change returns as applied, or the one the user's answer chooses, carrying its updated change list into the next finding.
- Keep each held finding unresolved.

##### 3. Renumber the Confirmed Maps

Require explicit authorization for each supplied outside-initiative file before editing it. Renumber the confirmed maps, preserving the numbers [Numbering Map](#numbering-map) protects.

For a confirmed epic map, run the renumberer from `<workspace>` with the initiative number, current pull request records, confirmed map, every affected body and any explicitly authorized outside-initiative files.

- The map is a comma-separated list of `<old-number>:<new-number>` pairs. Pass each body file as a separate argument; append `--outside` followed by each outside-initiative file when supplied.
- Files are rewritten in place. Outside files change only references carrying this initiative's prefix; links retain their targets. A collision or a number already named by a pull request is refused.

Runs as [Helper invocation](#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/renumber.py --initiative '<initiative-number>' --prs '<pull-request-records-file>' --map '<epic-number-map>' '<body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/renumber.py --initiative 07 --prs prs.json --map 6:0,0:1 live-936.md live-943.md
```

For a confirmed task map, run the renumberer from `<workspace>` with the initiative and epic numbers, owning epic body, confirmed old-to-new task map and every affected body file.

- `<task-number-map>` is a comma-separated list of `<old-number>:<new-number>` pairs. Pass each affected body file as a separate argument.

- It renumbers `<epic-id> Wxx` and `<epic-id>:Wxx` everywhere, and bare `Wxx` inside that epic's own body. **Example:** for `E01`, the qualified forms are `E01 Wxx` and `E01:Wxx`.
- The map assigns each old task number a distinct new number. A source absent from the files or a duplicate destination is refused.
- Append `--outside` followed by each explicitly authorized outside-initiative body file when supplied; only this initiative's prefixed references change there.
- Only rows no pull request names may be renumbered. Inspect the rewritten files before publishing them.

Runs as [Helper invocation](#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/renumber.py --initiative '<initiative-number>' --epic '<epic-number>' --own '<epic-body-file>' --tasks '<task-number-map>' '<affected-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/renumber.py --initiative 07 --epic 1 --own live-937.md --tasks 7:3,3:5 live-*.md
```

- Re-sort rewritten tables.
- Inspect every reported range.
- Search prose for references the script cannot see.
- Repeat [1. Gather Bodies and Check Dependencies](#1-gather-bodies-and-check-dependencies) after each edge or numbering change, using the current bodies, until it reports no problem but the held findings.
- Return the checked bodies, the printed longest chains, each printed contending pair, the proposed [Epic Priority](#epic-priority) map, the updated change list and the unresolved findings to the caller; do not publish a failed renumbering.

### Fields

#### Outside Files

Local body files outside the initiative, each identified by its path and the initiative references it contains.

#### Dependency Report

The checked initiative and epic bodies, longest dependency chains, contending task pairs, proposed [epic priority](#epic-priority) map and unresolved findings.

- **Scope.** One initiative, its epics and their task rows.
- **Source.** The initiative body and every epic body it links, published or as local drafts.

#### Edges

A task edge names the producing row for each output the depending row consumes. An edge a task's prose implies is carried explicitly.

- **An edge names rows, never an epic.**
  A row naming an epic gates its task on every row of that epic, including the rows it consumes nothing from, which is how a [whole-epic edge](#whole-epic-edges) the rows do not justify reaches the initiative.
- **A task consuming from every row of an epic names the producing row for each output.**
  An edge another in the cell already implies is dropped, so a prerequisite chain is named by its last row, and the whole-epic reach is what the rows establish either way.
- **An entry that cannot resolve is a permanent condition, not a prerequisite to come.**
  An entry naming no row and linking no issue, naming an issue the run was not given, or naming a row the epic it points to does not carry, cannot resolve. Every tool reading the cell names the entry as written, leaves the row where it stands rather than placing it as work still to come, and exits nonzero.

#### Whole-Epic Edges

An initiative Depends on cell takes the epics it derives, as [Work Breakdown](#work-breakdown) states. It derives one only where every row of the dependent epic requires every row of the prerequisite, through the task edges alone: a task row names rows, so no cell can assert a whole epic that the rows do not already establish.

- **The edge is the coarsest gate the plan has.**
  It holds the dependent epic until the prerequisite closes, not until the row it consumes merges, and it drops the dependent a [priority](#epic-priority) number, so the board keeps it out of Ready while the prerequisite runs.
- **Its cost is why it is derived and never written.**
  A narrower dependency stays in the task graph, where it gates the row that consumes the output rather than the epic around it.

#### Epic Priority

The map proposes one positive integer for each epic supplied, derived from the whole-epic edges and the components its rows declare. Epics sharing a number start together, so the number asserts they can run in parallel, and it holds a set only where both of these do.

- **Prerequisite depth establishes when an epic may start.**
  An epic with no prerequisite epic, one whose tasks are not yet written among them, carries the largest number, and each other epic takes one less than the smallest its prerequisites carry.
- **Component contention establishes whether it can.**
  An epic holding a row that contends with a row of an epic of the same depth takes the number below that depth, and the epics depending on it follow it down, as [Component Contention](#component-contention) states.

#### Component Contention

Two task rows in different epics whose work items declare one [component](#component) contend. Concurrent epics are two bases and two pull requests, so one component written from both is a merge conflict.

- Rows of one epic are out of scope: they land on one base, in the order Depends on and [Joins](#joins) set, so one component written twice is a rebase on that base rather than a conflict between two of them.
- A contending pair is answered by the number that separates its epics, or by moving the rows into one epic.

#### Joins

Every pair of tasks in an epic where neither depends on the other is named in the epic's Joins, or accounted for in the planning record.

- **Both resolutions are stated where the pair is reported.**
  Naming the pair in Joins asserts one pull request; the record entry says why there are two. A report naming only the first makes the assertion the cheaper answer.
- **The record is read, so the second resolution closes the line.**
  A record file gives each pair a line of its own naming its two ids, which is the form a joins artifact takes, and the pair leaves the report. A line naming more rows than that is prose about them and accounts for none, so no enumeration empties the report. What remains is the set named in neither.

#### Numbering Map

A comma-separated list of `<old-number>:<new-number>` pairs assigning each old number one distinct new number. A number a pull request already names is preserved, and a row a pull request names is not renumbered. A source absent from the supplied files, or a duplicate destination, is refused.

## Goal Trace

### Operations

#### Review Initiative Goal

The draft checked against the initiative outcomes.

**Inputs:** [Initiative body](#template-2), [Epic bodies](#template-3), [Goal clauses](#goal-clauses), [Requirement sources](#sources), [Epic format results](#format-findings)

**Outputs:** [Trace table](#trace-table), [Ranked gaps](#gaps)

##### 1. State the Goal as Clauses

Take the goal the user stated and confirmed, as clauses, each an outcome someone could observe.

##### 2. Build the Trace Table

Build the [Trace Table](#trace-table) from those clauses, the initiative criteria, the epics whose Coverage cells cite them and the epic criteria that deliver them.

- Every goal clause has an initiative criterion that makes it true.
- Every initiative criterion is delivered by an epic, and that epic's criteria make the criterion wholly true.
- Every initiative criterion traces to a goal clause.
- Remove one that traces to none, or put that scope to the user.
- Record any criterion no task row delivers as a gap from the supplied epic format results.

##### 3. Read the Initiative References

Apply [Read Requirement Sources](#read-requirement-sources) with the initiative References, checkout, authenticated access and output files.

- Extend the trace table with the source requirement each criterion answers to. Each unmatched requirement, each criterion that departs from the one it cites, and each source that could not be read is a gap [Sources](#sources) names.

##### 4. Check Criteria Against the Standards

Check each criterion against the [shared acceptance criteria](#shared-acceptance-criteria) and [Initiative Acceptance Criteria](#initiative-acceptance-criteria).

##### 5. Snapshot the Local Drafts

Apply [Build Body Snapshot](#build-body-snapshot) for each supplied local draft with its title, labels and existing identity when present.

- Use the returned initiative and epic JSON for [Validate Initiative Body](#validate-initiative-body) with the initiative JSON, every linked epic's current JSON, source evidence and output file.
- Incorporate its local findings into this review.

##### 6. Apply the Outside Threat Check

Apply [Check Outside Threats](#check-outside-threats).

##### 7. Rank the Trace Gaps

Rank the gaps, meeting [Gaps](#gaps).

- Flag the few that most threaten the goal.
- Return the trace table and the ranked findings to the caller.

#### Check Outside Threats

An item the draft leaves open is a gap.

**Inputs:** [Initiative body](#template-2), [Epic bodies](#template-3), [Changed artifacts](#changed-artifacts)

**Outputs:** [Threats](#gaps)

##### 1. Check Outside Consumers

Check for anything outside the plan that reads, builds or ships what the plan changes or removes.

##### 2. Check Hidden Violation Paths

Check for a skip, a fallback, or a fail-closed path that hides a violation.

##### 3. Check the Done Threshold

Check that done has a threshold, a baseline, and an instrument that is independent of the thing measured. The baseline is fixed before the plan changes what it measures.

##### 4. Check Artifact and Reader Skew

Check for skew between an artifact the plan produces and an implementation that reads it.

##### 5. Check Shifting Ground

Check for a change elsewhere that alters the ground the plan stands on.

- Return the evidenced threats and gaps to [Review Initiative Goal](#review-initiative-goal).

### Fields

#### Goal Clauses

The confirmed goal divided into independently observable outcomes, each with an identifier used in the [trace table](#trace-table).

#### Changed Artifacts

The artifacts a plan changes and the consumers affected by those changes, with the interfaces and requirements each relies on.

#### Trace Table

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| The outcome the user confirmed | The criteria that make the clause true | The epics whose Coverage cells cite those criteria | The epic criteria that deliver them | The requirement the criterion answers to |

Every clause, criterion and epic the initiative holds occupies a row. A cell with no entry is a gap, not an omission.

#### Gaps

A gap is a clause no criterion makes true, a criterion no epic delivers, a criterion tracing to no clause, a criterion no task row delivers, an unmatched source requirement, a criterion departing from the source it cites, a source that could not be read, or a threat the draft leaves open. Gaps are ranked, and the few that most threaten the goal are flagged.

## Review Finding

### Operations

#### Populate Review Finding

One finding verified against its supplied source.

**Inputs:** [Finding](#finding-content), [Decision](#decision-state)

**Outputs:** [Populated finding](#finding-content), [Pending decision](#decision-state)

##### 1. Verify the Reported Problem

Verify the problem against the supplied source.

##### 2. Return Unproven Findings

If evidence is missing or contradictory, return that finding for the caller to resolve.

##### 3. Quote the Finding Source

Populate the finding with its source quotation.

- It must meet [Finding Content](#finding-content) and [Decision State](#decision-state).

##### 4. Return the Populated Finding

Return the finding and any pending decision.

#### Report Review Finding

The verified findings presented for resolution.

**Inputs:** [Findings](#finding-content)

**Outputs:** [Reported findings](#finding-content), [Confirmed resolutions](#decision-state)

##### 1. Populate the Review Finding

Apply [Populate Review Finding](#populate-review-finding) with the area, severity, problem, solution and source evidence.

- Resolve any evidence gap before reporting it.
- Group the returned findings by area.

##### 2. Ask Pending Finding Decisions

Put each pending decision to the user, one question at a time.

- Wait for the answer.
- Record the confirmed answer on the finding, meeting [Decision State](#decision-state).
- Return each confirmed resolution to the caller for application to its selected issue kind. A pending decision returns without applying a change.

### Fields

#### Finding Content

Each finding has an area, severity, one problem/solution pair and a source quotation with file and line. The source establishes the stated problem. Findings are grouped by area when presented together.

#### Decision State

A finding identifies whether it needs a user decision and records any supplied answer. An unanswered decision remains pending.

## Board Queue

### Fields

#### Priority Sets

A parallel work map assigns a positive integer to each ranked initiative. Every initiative with the same number runs together as one set. One left unordered stays in Backlog.

The epics of one initiative carry their own sets. Every epic with the same number starts together, and a number is compared only with its siblings'.

A priority label carries a set's number, with the name, colour and description [Priority Labels](#priority-labels) sets. A larger number is higher, with no maximum. Two such labels on one issue count as the larger number.

## Issue Body

### Operations

#### Write Issue Table

The shared table, before a kind fills its cells.

**Inputs:** [Current body](#body-file-3), [Kind conditions](#kind-conditions), [Row data](#tables)

**Outputs:** [Issue body](#body-file-3)

##### 1. Populate the Shared Table Cells

Populate the shared Done, Coverage and Depends on cells from the supplied row data.

- The columns must match the kind's table.
- The shared cells must meet [Tables](#tables).

##### 2. Read the Finished Issue Table

Read the finished table against [Tables](#tables), [Numbering](#numbering), and [Reference form](#reference-form). A Depends on cell that holds prose fails [Tables](#tables). Numbering that does not follow start order is advisory, as [Numbering](#numbering) states.

#### Check Round of Edits

The shared check after a round of edits.

**Inputs:** [Changed bodies](#body-file-3), [Kind conditions](#kind-conditions), [Related context](#related-context)

**Outputs:** [Format findings](#format-findings), [Field findings](#field-findings)

##### 1. Check Each Section Against Fields

Check each section of the issue against the field conditions for its kind and against [Fields](#fields-11) in this file.

##### 2. Check the Changed Body Formats

From `<workspace>`, check every changed issue using its issue JSON, local correction output path and additional format inputs supplied by its kind. Read each result as [Command result](#command-result) states before the next issue; retain format findings and stop on an unreadable input.

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

##### 3. Return the Body Check Findings

Read each format check’s result as [Command result](#command-result) states. Return its format findings with the field findings; report an unreadable input as a blocker.

#### Validate Issue Body

One body checked against its supplied kind and template.

**Inputs:** [Issue record](#issue-record), [Kind conditions](#kind-conditions), [Related context](#related-context), [Output body path](#body-file-3)

**Outputs:** [Corrected body](#body-file-3), [Format findings](#format-findings), [Field findings](#field-findings)

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

**Inputs:** [Current body](#body-file-3), [Kind conditions](#kind-conditions), [Related context](#related-context), [Confirmed resolutions](#body-resolutions), [Output body path](#body-file-3)

**Outputs:** [Corrected body](#body-file-3), [Format findings](#format-findings), [Field findings](#field-findings), [Required changes](#required-changes)

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

#### Repair Issue Format

The saved format corrections for a set of issues of one kind and any unresolved content findings.

**Inputs:** [Issues](#issue-record), [Kind conditions](#kind-conditions), [Related context](#related-context), [Output body paths](#body-file-3)

**Outputs:** [Repaired issues](#issue-record), [Format findings](#format-findings), [Field findings](#field-findings)

##### 1. Apply the Format Validator

Apply the kind's validator to each issue body with its current JSON, output path and the further inputs its kind conditions name: the kind's Validate operation where its body file has one, otherwise [Validate Issue Body](#validate-issue-body) with the kind conditions.

- Return an unreadable source as a blocker before editing.

##### 2. Review Each Format Diff

Review each returned diff.

- Publish wording-preserving format, title and label corrections through [Save Tracker Issue](#save-tracker-issue), without asking.
- Retain content decisions and cross-body findings separately; do not publish them as mechanical fixes.

##### 3. Resolve Single-Body Findings

Resolve a non-mechanical finding confined to one body.

- Obtain the user's decision.
- Apply [Apply Body Corrections](#apply-body-corrections) with the current body, kind template and conditions, related context, confirmed resolution and output path.
- Publish through Save Tracker Issue. An unanswered decision or a finding requiring changes to other issues returns to the caller as a blocker.

##### 4. Re-Read Each Repaired Issue

Apply [Read Tracker Issue](#read-tracker-issue) for each saved issue, as [Write confirmation](#write-confirmation) states.

- Repeat the kind's validator with the saved JSON and the same further inputs, context and output path.
- Return each saved body, whether a correction was made, and the validation result to the caller. A remaining failure is a blocker.

#### Resolve Open Questions

The answers to an issue's Open Questions saved in its body, and the questions that stay open.

**Inputs:** [Issue record](#issue-record), [Kind conditions](#kind-conditions), [Related context](#related-context), [Output body path](#body-file-3)

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

Each place a body departs from its kind conditions or [Fields](#fields-11): a missing or extra section, a wrong-kind layout, historical narration, or a criterion failing its named instrument, with the section it concerns.

#### Body Resolutions

The decision taken on each non-mechanical finding or open question: content to add, an extra section kept, folded or removed, a criterion change, or an answer, each tied to the finding or question it settles.

#### Required Changes

Changes a body correction needs outside that body: a tracker-kind change, a title or label change, or an edit to another issue's body, each naming the issue it applies to.

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

## Task Body

### Fields

#### Task Delivery Result

One task's delivery as recorded: the body with its delivering pull request and verified criteria ticked, a comment file reading `Delivered by #<pull-request-number>.`, and the eligibility findings stating whether the task is closable.

## Epic

### Operations

#### Check Epic Prerequisites

The evidence required before starting an epic's work.

**Inputs:** [Initiative issue](#issue-record), [Epic issue](#issue-record), [Prerequisite epic issues](#issue-record), [Base merges](#state)

**Outputs:** [Prerequisite evidence](#prerequisite-evidence)

##### 1. Identify Epic Prerequisites

Identify each prerequisite the supplied initiative row names.

##### 2. Apply the Whole-Epic Dependency Rule

Apply the initiative's [whole-epic dependency rule](#work-breakdown); a task row's reference to a row of another epic gates that row rather than this epic.

##### 3. Confirm Prerequisite Epics Completed

Confirm from current issue and base-merge records that each prerequisite epic is closed as completed and every one of its bases has merged. Missing records leave the prerequisite unconfirmed.

##### 4. Return the Prerequisite Evidence

Return the [Prerequisite Evidence](#prerequisite-evidence), identifying each confirmed prerequisite and missing condition. Only a confirmed result permits an unstarted epic to be marked Ready, its bases to be created or its task to be dispatched.

### Fields

#### Task Matches

Task-to-pull-request pairs identifying the epic task id and delivering pull request, with each match marked confirmed or pending.

#### Prerequisite Evidence

Each prerequisite has its issue identity and completion state, expected delivery bases and their merge evidence. The result identifies confirmed and missing conditions for the candidate epic.

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

## Initiative

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

## Proposal Body

### Operations

#### Populate Proposal Body

One proposal body from a confirmed problem and goal.

**Inputs:** [Proposal scope](#proposal-scope), [Output body path](#body-file-3)

**Outputs:** [Proposal body](#template-5)

- Populate the body from the [Template](#template-5) at the supplied output path, from the confirmed problem and goal.
  - The title must meet the shared [Titles](#titles-3) conditions.
  - The Problem must meet the shared [Problem and Proposal](#problem-and-proposal) conditions.
  - All populated fields must meet [Fields](#fields-17), including the required [Sections](#sections-1).

#### Validate Proposal Body

The body's local format and field findings.

**Inputs:** [Proposal issue](#issue-record), [Related context](#related-context), [Output body path](#body-file-3)

**Outputs:** [Corrected body](#body-file-3), [Format findings](#format-findings), [Field findings](#field-findings)

##### 1. Validate the Proposal Fields

Apply [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#fields-17), supplied related evidence and output file, using the proposal field conditions and required title and label metadata.

##### 2. Return the Validated Proposal Body

Return the corrected body, mechanical diff and unresolved findings for the caller.

### Fields

#### Template

````markdown
## Overview

{{One paragraph: the problem this proposal scopes. Name the goal the clauses state.}}

## Problem

{{One sentence on the friction, then one bullet per facet. Each bullet opens with a bold statement, and its body is on the next line.}}

- **{{Facet}}.**
  {{The evidence.}}

## Goal

- {{A clause: an outcome someone could observe. Not a description of the change.}}

## Non-Goals

- {{One succinct sentence on what this proposal does not do. It names no initiative, epic, task or issue, and no owner.}}

## References

- **R1.** [{{Title}}]({{URL}}) — {{What the reader finds there. Delete the section when there is none.}}
````

#### Titles

- The title is `[P00] Name: Subtitle`.
- The label is the proposal [kind label](#kind-labels).
- `P` is the proposal number. Proposals count from `00`.

#### Problem

- A Problem meets [Problem and Proposal](#problem-and-proposal).

#### Goal

- Each clause is an outcome someone could observe.
- A clause does not describe the change.

#### Non-Goals

- One succinct sentence each on what the proposal does not do.
- A non-goal names no initiative, epic, task or issue, and no owner.

#### Sections

- Overview, Problem, Goal and Non-Goals are present in that order. References follows when it has content.

#### Proposal Scope

The problem one proposal scopes, with the evidence for each facet, its goal clauses and its boundary, as the [Template](#template-5)'s Problem, Goal and Non-Goals hold them.

## Board

### Operations

#### Select Project Board

The theme or proposals board the request names.

**Inputs:** [Board owner](#board-identity), [Board selection](#board-selection)

**Outputs:** [Selected board](#board-identity)

##### 1. Find the Named Board

Select the command matching the requested board kind. The selection meets [Themes](#themes) or [Proposals](#proposals).

For a theme selection, run this query from the repository checkout using the board owner and requested theme name.

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title | sub("^\\[P[0-9]+\\] "; "") | startswith("<theme-name>: ")) | .number'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title | sub("^\\[P[0-9]+\\] "; "") | startswith("Canon: ")) | .number'
```

For a proposals selection, run this query from the repository checkout using the board owner and configured [proposals title](#proposals-board).

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "<proposals-board-title>") | .number'
```

##### 2. Report a Missing Board Selection

Read the result of each command in the preceding step as [Command result](#command-result) states.

Return a missing-selection result when neither a theme nor proposals is specified; the caller obtains that choice.

##### 3. Return the Selected Board Number

Return the selected board number, or an absent-board result for [Copy Project Board](#copy-project-board). Work one board at a time.

#### Copy Project Board

A missing theme board, or a missing proposals board.

**Inputs:** [Board owner](#board-identity), [Repository](#repository-1), [Board selection](#board-selection), [Theme title](#one-board-per-theme), [Originating proposal](#issue-record)

**Outputs:** [Copied board](#board-identity)

##### 1. Create an Absent Proposals Board

When no open board carries the [proposals board](#proposals-board) title, apply [Create Proposals Board](#create-proposals-board). The copy source and the title meet [Proposals](#proposals).

##### 2. Create an Absent Theme Board

When the selected theme board is absent:

- Apply [Create Theme Board](#create-theme-board) with the owner, repository, theme title and originating proposal record when applicable.
- Require the new theme's label and board before an initiative takes that theme.

#### Ensure Project Board

The theme or proposals board the request names, created when it is absent.

**Inputs:** [Board owner](#board-identity), [Repository](#repository-1), [Board selection](#board-selection), [Theme title](#one-board-per-theme), [Originating proposal](#issue-record)

**Outputs:** [Board](#board-identity)

##### 1. Select the Requested Board

Apply [Select Project Board](#select-project-board) with the owner and the theme name or proposals selection.

- On a missing-selection result, return it to the caller and stop.
- On a selected board, return its owner and number and stop.

##### 2. Copy an Absent Requested Board

When the board is absent:

- For a theme a proposal derives, apply [Read Tracker Issue](#read-tracker-issue) for the originating proposal's identity. Return unresolved provenance and stop when it cannot be read.
- Apply [Copy Project Board](#copy-project-board) with the owner, repository, selected board kind, theme title and that proposal record when applicable.

##### 3. Return the Copied Board Number

Return the owner and the board number the copy created.

#### Create Proposals Board

A new proposals board linked to the supplied repository.

**Inputs:** [Board owner](#board-identity), [Repository](#repository-1)

**Outputs:** [Proposals board](#board-identity)

##### 1. Copy the Proposals Template

Apply [Copy Board Template](#copy-board-template) with the owner, repository, the proposals board's [template title](#board-templates) and the configured [proposals title](#proposals-board) as the copy's title. The copied board meets [Proposals](#proposals).

##### 2. Return the Proposals Board Number

Return the copied board's owner and number.

#### Create Theme Board

A new theme board linked to the supplied repository.

**Inputs:** [Board owner](#board-identity), [Repository](#repository-1), [Theme title](#one-board-per-theme), [Originating proposal](#issue-record)

**Outputs:** [Theme board](#board-identity)

##### 1. Require the Originating Proposal

Require the originating proposal record for a proposal-derived board; return a missing-input finding when its designator is unavailable.

##### 2. Copy the Initiative Template

Apply [Copy Board Template](#copy-board-template) with the owner, repository, the theme board's [template title](#board-templates) and the title required by [One Board Per Theme](#one-board-per-theme) as the copy's title. The copy carries the template's theme board [Status options](#status-field).

##### 3. Return the Theme Board Number

Return the copied board's owner and number.

#### Copy Board Template

One board copied from an open template board and linked to its repository.

**Inputs:** [Board owner](#board-identity), [Repository](#repository-1), [Board title](#one-board-per-theme)

**Outputs:** [Copied board](#board-identity)

##### 1. Find the Template Board

From the repository checkout, find the open template board using the owner and the supplied [template title](#board-templates).

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "<template-title>") | .number'
```

##### 2. Copy the Template Board

Read the result of each command in the preceding step as [Command result](#command-result) states.

From the repository checkout, copy the returned template number for the owner, using the supplied board title.

- The copy's JSON is one project; `.number` identifies the new board.

```bash
gh project copy '<template-number>' --source-owner '<owner>' --target-owner '<owner>' --title '<board-title>' --format json --jq .number
```

##### 3. Link the Board to the Repository

Read the result of each command in the preceding step as [Command result](#command-result) states.

From the repository checkout, link the new board using its owner, returned number and supplied repository.

```bash
gh project link '<board-number>' --owner '<owner>' --repo '<repo>'
```

##### 4. Return the Copied Board Number

Read the result of each command in the preceding step as [Command result](#command-result) states.

Return the new board number after linking succeeds.

#### Place Issue on Board

One issue's membership and initial status.

**Inputs:** [Board](#board-identity), [Repository](#repository-1), [Issue](#issue-record), [Output file](#board-files), [Initial status](#status-field)

**Outputs:** [Board item](#board-items)

##### 1. Read the Issue to Place

Apply [Read Tracker Issue](#read-tracker-issue) with the repository, issue number and output file for the complete JSON, and take the issue id from it.

##### 2. Fetch the Placement Status Options

From the repository checkout, fetch the supplied board’s fields into the destination file, using its owner and number.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/fields?per_page=100" > '<board-fields-file>'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/fields?per_page=100" > fields.json
```

##### 3. Add the Issue to the Board

Read the result of each command in the preceding step as [Command result](#command-result) states.

From the repository checkout, add the issue using the board owner and number and the returned issue id, not its issue number.

```bash
gh api --method POST 'users/<owner>/projectsV2/<board-number>/items' -f type=Issue -F 'id=<issue-id>' --jq .id
```

**Example:**

```bash
gh api --method POST 'users/<owner>/projectsV2/13/items' -f type=Issue -F id=3040123456 --jq .id
```

##### 4. Set the Placed Item Status

Read the result of each command in the preceding step as [Command result](#command-result) states.

From the repository checkout, set the caller’s selected Status using the board owner and number, returned item id and supplied status-request file.

The input file meets [Status Request](#status-request), with the supplied Status field id as a JSON integer and the selected option id as a JSON string.

**Example payload:** `{"fields":[{"id":419167630,"value":"OPTION"}]}`.

```bash
gh api --method PATCH 'users/<owner>/projectsV2/<board-number>/items/<item-id>' --input '<status-input-file>' --jq .id
```

**Example:**

```bash
gh api --method PATCH 'users/<owner>/projectsV2/13/items/1001' --input status-backlog.json --jq .id
```

##### 5. Confirm the Placed Board Item

Read the result of each command in the preceding step as [Command result](#command-result) states.

From the repository checkout, read the saved item using the board owner and number, item id and Status field id.

```bash
gh api "users/<owner>/projectsV2/<board-number>/items/<item-id>?fields=<status-field-id>"
```

**Example:**

```bash
gh api "users/<owner>/projectsV2/9/items/1001?fields=419167630"
```

##### 6. Return the Placed Board Item

Read the final fetch’s result as [Command result](#command-result) states. Return the confirmed item only when its issue and Status match the intended placement; otherwise return the failure or discrepancy.

### Fields

#### Themes

Every initiative belongs to one theme, and each theme has one project board. Each project names its own themes, with their labels, in [Theme Labels](#theme-labels).

#### One Board Per Theme

- A proposal-derived board title is the originating proposal's exact `[Pxx]` designator, a space, the theme name, a colon, and its description: `[P03] Canon: Definitions Checked Against the Design Canon`. Preserve the proposal's digits exactly. A board with no originating proposal uses `Name: Description`.
- It is linked to the repository.
- It holds the theme's initiatives, their epics and their task issues.

#### Proposals

- The board carries the [proposals board](#proposals-board) title. It holds proposal issues, the incoming funnel for work that may become an initiative.
- Its copy source is the open board with the proposals board's [template title](#board-templates). That template carries the [Proposals Priority Field](#proposals-priority-field), and its view is a board grouped by Status.
- Its [Status options](#status-field) mean:
  - **Suggested.**
    Raised, and nobody has taken it up. A new proposal lands here, with no assignee.
  - **Considering.**
    Someone is weighing the goal, the evidence and the criteria. That person is the assignee.
  - **Approved.**
    Qualified to become an initiative. The assignee is the user.
  - **Held.**
    Not now. It stays on the board, with no assignee.
  - **Declined.**
    It will not become an initiative. It has no assignee.

#### Board Identity

A board's owner and number, written `users/<owner>/projectsV2/<number>` for a user's board or `orgs/<owner>/projectsV2/<number>` for an organisation's. The owner is the user's login or organisation name; a board yet to be created has its owner alone.

#### Board Selection

One theme's name, as [Theme Labels](#theme-labels) names it, or the proposals board.

#### Board Items

A board's items as JSON, each with its item id, its Status and its issue whole. A single board item is one such entry.

#### Board Files

The local paths a board read writes its JSON into: an issue file, a board fields file and a board item file.

#### Status Request

A JSON file naming the Status field id as an integer and the selected option id as a string: `{"fields":[{"id":<status-field-id>,"value":"<status-option-id>"}]}`.

## Delivery Branches

### Operations

#### Prepare Delivery Bases

The branches a task pull request targets.

**Inputs:** [Project checkout](#project-checkout), [Epic prefix](#epic-bases), [Changed long-lived branches](#branches), [Prerequisite evidence](#prerequisite-evidence)

**Outputs:** [Epic bases](#epic-bases)

##### 1. Read the Delivery Branch Collections

Apply [Read Delivery Branches](#read-delivery-branches) with the project checkout and epic branch prefix.

##### 2. Report Missing Branch Configuration

A missing or empty `config/branches` reports the names as unevaluable; obtain the project's branch names before creating delivery branches.

##### 3. Require Base Prerequisite Evidence

Require the caller's confirmed prerequisite evidence before creating a base. The board status alone supplies no such evidence.

##### 4. Create Each Missing Epic Base

Apply [Create Epic Base](#create-epic-base) for each missing base, passing the project checkout, corresponding long-lived branch, epic base name and confirmed prerequisite evidence.

#### Create Epic Base

The missing epic branch rooted in its remote long-lived branch.

**Inputs:** [Project checkout](#project-checkout), [Long-lived branch](#branches), [Epic base](#epic-bases), [Prerequisite evidence](#prerequisite-evidence)

**Outputs:** [Epic base](#epic-bases)

##### 1. Require a Missing Destination Base

Require the confirmed prerequisites and a missing destination. Refuse a destination that already exists.

##### 2. Fetch the Long-Lived Source Branch

From the supplied repository checkout, fetch the corresponding long-lived source branch, such as `main`.

```bash
git fetch origin '<source-branch>'
```

##### 3. Publish the New Epic Base

Read the result of each command in the preceding step as [Command result](#command-result) states.

After a successful fetch:

From the repository checkout, publish the fetched source as the confirmed missing epic base, such as `i07/e00/main`, meeting [Epic Bases](#epic-bases).

```bash
git push origin 'origin/<source-branch>:refs/heads/<epic-base>'
```

##### 4. Confirm the Published Epic Base

Read the push’s result as [Command result](#command-result) states. Return the created base only on success; return a refused or non-fast-forward push without rewriting the remote branch.

#### Update Task Branch

The current epic base merged into a unit's task branch.

**Inputs:** [Task worktree](#task-branches), [Task branch](#task-branches), [Epic base](#epic-bases)

**Outputs:** [Task branch](#task-branches)

##### 1. Fetch the Epic Base into the Task Worktree

From the unit’s worktree, fetch its epic base, such as `i07/e00/main`.

```bash
git fetch origin '<source-branch>'
```

##### 2. Stop on a Task Branch Fetch Failure

Read the result of each command in the preceding step as [Command result](#command-result) states.

Stop on failure.

##### 3. Merge the Epic Base into the Task Branch

From the unit’s worktree, merge its fetched epic base using the branch name without the `origin/` prefix, such as `i07/e00/main`. A conflict stops the update, leaves the pull request open and is reported.

```bash
git merge --no-edit 'origin/<source-branch>'
```

##### 4. Push the Updated Task Branch

Read the result of each command in the preceding step as [Command result](#command-result) states.

After a successful merge:
After a successful merge, push from the task worktree with the supplied task branch as destination.

```bash
git push origin 'HEAD:refs/heads/<task-branch>'
```

**Example:**

```bash
git push origin HEAD:refs/heads/i07/e00/w01-queue-plan
```

##### 5. Confirm the Task Branch Push

Read the push’s result as [Command result](#command-result) states. Return the updated task branch only on success; report a failed or non-fast-forward push without rewriting the remote branch.

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

#### Task Branches

A unit's task branch is cut from the epic base for the long-lived branch the unit changes, named for its initiative, epic and first task in lowercase separated by slashes, and hyphenated with a slug of at most four words from its Description when one exists: `i01/e02/w04-write-defaults`. Every pull request delivering the unit's work is opened from this branch.

Its worktree is named by that branch under the worktree directory of the repository's main working tree.

#### Project Checkout

A checkout of the repository whose branches are delivered. Its main working tree holds the [Branches](#branches) statement, and its worktree directory holds every epic-base, task and review worktree.

# Propose Mode

Scopes one problem: the friction, the evidence, and the boundary, and states the goal as clauses the user confirms. It raises one proposal on the [proposals board](#proposals-board).

Follow the [Procedure](#procedure-1), adhering to [Rules](#rules) and [Conventions](#conventions) and ensure all [Outcomes](#outcomes-1) are met.

## Procedure

### 1. Understand the Problem

Ask the user until the friction and the boundary are clear.

- State the goal back as clauses meeting [Goal](#goal).
- Have the user confirm those clauses.

### 2. Gather Evidence

- Measure the current state: counts, paths, and file:line.
- Delegate broad sweeps to parallel sub-agents.
- Spot-check what they return before recording it.

### 3. Draft the Body

Apply [Populate Proposal Body](#populate-proposal-body) with the confirmed problem, evidence, goal clauses, boundary and output body path. The local file is the source for the issue.

- Obtain the proposal's number through [Select Tracker Number](#select-tracker-number) with the proposal prefix letter, and carry it in the title.
- The goal clauses are the clauses the user confirmed. The Non-Goals are the boundary.
- The design, the acceptance criteria, and the breakdown belong to a later goal.

### 4. Validate

Apply [Build Body Snapshot](#build-body-snapshot) with the body file, title, labels and a JSON path.

- Apply [Validate Proposal Body](#validate-proposal-body) with the returned JSON and the output file.
- Resolve each finding it leaves unresolved in the problem, evidence, goal clauses or boundary, and repeat Populate Proposal Body with them and the same output path.
- Repeat Build Body Snapshot and Validate Proposal Body with the revised body and the same paths. Proceed to publication only when validation passes.

### 5. Publish

Apply [Save Tracker Issue](#save-tracker-issue) with the repository, the validated body file, its title, the proposal's labels and each label's colour and description, leaving it unassigned.

### 6. Confirm Placement

Ask whether to add the issue to the proposals board.

- On acceptance, continue to [7. Place](#7-place).
- On a decline, skip placement and continue to [8. Report](#8-report) with the issue URL.
- Wait for an unanswered decision.

### 7. Place

Apply [Ensure Project Board](#ensure-project-board) with the board owner, the repository and the proposals-board selection.

- Apply [Place Issue on Board](#place-issue-on-board) with the returned owner and board number, the repository, the saved issue number, an output file and initial status Suggested.
- Leave the issue unassigned.

### 8. Report

Give the issue's URL, and the board's when the issue was placed.

## Outcomes

- **A scoped problem.**
  The user has one problem scoped, and has confirmed its goal.
- **One proposal.**
  The user has that problem raised as one proposal.
- **On the proposals board.**
  When the user wants the proposal on the proposals board, it is there, raised, and unassigned.

# Protocols

## Initiative Publication

A reviewed initiative and its epics saved to the tracker, linked to one another, format-checked and recorded in the planning record.

Follow the [Procedure](#procedure-2), adhering to [Rules](#rules) and [Conventions](#conventions).

### Procedure

#### 1. Number the Initiative

For a new initiative, apply [Select Tracker Number](#select-tracker-number) with the repository, the initiative prefix letter and its existing titles.

- Use the confirmed number in the initiative's title.

#### 2. Save the Initiative

Apply [Save Tracker Issue](#save-tracker-issue) with the repository, the reviewed initiative body file, its title and labels, and each label's colour and description.

- For an existing initiative, pass its issue number and the selected body and metadata changes.

#### 3. Save the Epics

For each reviewed epic, a prerequisite epic before the epics that depend on it:

- Apply [Save Tracker Issue](#save-tracker-issue) with the repository, the epic body file, its title, its labels with the confirmed priority label among them, and each label's colour and description.
- For an existing epic, pass its issue number and the selected body and metadata changes.

#### 4. Resolve the Links

Apply [Resolve Placeholder Links](#resolve-placeholder-links) with the initiative body file, each epic body file and the saved issue identity of the initiative and of each epic.

- Return each temporary link left unresolved, with the file that holds it, to the caller as a blocker.
- Apply [Save Tracker Issue](#save-tracker-issue) with the body change for each rewritten body file.

#### 5. Repair the Format

- Apply [Repair Issue Format](#repair-issue-format) with [Validate Epic Body](#validate-epic-body) as the validator, the saved initiative JSON, current pull request records and corpus branch as its further inputs, the epic template, and every saved epic with its identity, current JSON and output body path.
- Apply [Repair Issue Format](#repair-issue-format) with [Validate Initiative Body](#validate-initiative-body) as the validator, every saved epic JSON and the requirement sources as its further inputs, the initiative template, and the saved initiative with its identity, current JSON and output body path.
- Return each blocker either repair returns to the caller.

#### 6. Record the Publication

Apply [Populate Planning Record](#populate-planning-record) with the record identity, folder path, the saved initiative and epic issue links, the evidence and decisions the caller supplies, and the caller's commit message file, asking it to publish.

- Return the saved initiative and epic identities, the publication result and any blocker to the caller.

## Delivery Base Preparation

The epic bases a set of epics needs, created once their prerequisites hold, and the open delivery pull requests pointed at them.

Follow the [Procedure](#procedure-3), adhering to [Rules](#rules) and [Conventions](#conventions).

### Procedure

#### 1. Confirm Prerequisites

For each supplied epic:

- Apply [Check Epic Prerequisites](#check-epic-prerequisites) with the current initiative and epic bodies and the prerequisite issue and base-merge records.
- Carry a missing or unconfirmed prerequisite into the result as that epic's finding, and leave its bases uncreated.

#### 2. Prepare the Bases

For each epic whose prerequisites are confirmed, apply [Prepare Delivery Bases](#prepare-delivery-bases) with the project checkout, epic identity, changed long-lived branches and the confirmed [Prerequisite Evidence](#prerequisite-evidence).

- Carry unevaluable branch names or a failed creation into the result.

#### 3. Read Branches and Pull Requests

- Apply [Read Delivery Branches](#read-delivery-branches) with the project checkout and each supplied epic's identity.
- Use the current pull request records the caller supplies. When it supplies none, apply [Read Initiative Pull Requests](#read-initiative-pull-requests) with the repository, initiative prefix and destination collection file.
- Return to the caller with the findings when the branch names are unevaluable or the pull request evidence is incomplete.

#### 4. Align the Pull Requests

Apply [Align Pull Request Base](#align-pull-request-base) with the repository, those pull request records, the long-lived branches and epic bases Read Delivery Branches returned, and the project checkout.

#### 5. Return the Result

Return to the caller:

- The bases created and each epic's prerequisite findings.
- The long-lived branches and epic bases Read Delivery Branches returned.
- The retargeted pull requests, updated task branches, conflicts and pull requests awaiting a decision that Align Pull Request Base returned.

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

#### Priority Labels

The label carrying a priority set: `priority:` and a positive integer `<n>`.

- **Colour.**  `BFD4F2`.
- **Description.**  `Priority set <n>; a larger number starts sooner`, with `<n>` its integer.

### Boards

#### Proposals Board

The board holding proposal issues, titled `Proposals`.

#### Board Templates

The open boards a new board is copied from, by exact title.

| Board | Template title |
| --- | --- |
| Proposals board | `Proposals Template` |
| Theme board | `Initiative Template` |

#### Status Field

The single-select field a board item's status is read from and written to, named `Status`.

- **Theme board options.**  Backlog, Ready, In Progress, In Review and Done.
- **Proposals board options.**  Suggested, Considering, Approved, Held and Declined.

#### Proposals Priority Field

The single-select field `Priority` on the proposals board, with the options High, Medium and Low.

### Planning Records

#### Engineering Branch

The long-lived branch holding every planning record, named `engineering`, checked out in one worktree.

- **Records folder.**  `artifacts/planning/`, relative to that worktree.

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
