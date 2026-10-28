# Prosiform

## Dispatch

Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Sync Mode

Records delivery on an initiative, its epics, and their task issues. Each task that has a pull request is linked to that pull request, open or merged. Criteria that now hold are recorded, complete rows are marked done, complete issues are closed, and the initiative's theme board is brought up to date.

Follow the [Procedure](#procedure), adhering to [Rules](#rules) and [Conventions](#conventions) and ensure all [Outcomes](#outcomes) are met.

## Procedure

### 1. Select

Select an initiative with its open epics, or the epics the user names.

- Apply [Read Tracker Issue](#read-tracker-issue) for the initiative, each selected epic and each task issue under it, titled as [Titles](#titles) states.
- Apply [Repair Issue Format](#repair-issue-format) once per kind, with that kind's validator — [Validate Initiative Body](#validate-initiative-body), [Validate Epic Body](#validate-epic-body), or [Validate Issue Body](#validate-issue-body) with the task [Fields](#fields-1) — its further inputs, each fetched body with its identity, current JSON and output body path, the kind template and required related evidence.
  - Use the saved bodies it returns in the following steps.
  - Return a remaining format failure as a blocker.
- Apply [Confirm Repository Auto-Close](#confirm-repository-auto-close) for the repository holding the issues, and pass the confirmed setting to every protocol this run follows.

### 2. Record Delivery

Follow [Delivery Recording](#dispatch-delivery-recording) with the selected repositories and initiative prefix, the fetched epic JSON and task issue records, the project checkout, named instruments, the confirmed setting, the allowance the caller supplied, the run's [change list](#change-list), and output body and comment files.

- Route what it returns:
  - **Unnamed deliveries.**
    - Put each [unnamed delivery](#unnamed-deliveries) to the user as an [interview](#rules).
    - For each the user confirms, apply [Publish Pull Request](#publish-pull-request) with its repository and number and the title [Named Delivery](#named-delivery) states.
    - Follow Delivery Recording again with the same inputs.
  - **Incomplete evidence.**
    - Return it as a blocker.
  - **Pending matches, rows and open questions.**
    - Report each as pending; the epic it concerns stays open.
  - **Conflicts and disagreements.**
    - Report each as unresolved with its pull request and row.

#### Dispatch Delivery Recording

Dispatch `protocols_delivery-recording.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states.

### 3. Close Each Epic

For each selected epic, follow [Epic Closure](#dispatch-epic-closure) with the repository, initiative prefix and project checkout, the epic JSON, issue and body with its criterion ids and named instruments, its latest Delivery Findings, task issue records, confirmed matches and the task-merge records among the pull request records, the confirmed setting, and the verification evidence Delivery Recording and each earlier Epic Closure of this run returned.

- Report a draft awaiting the user's ready mark, a blocker and each initiative Delivery Finding it returns as pending.

#### Dispatch Epic Closure

Dispatch `protocols_epic-closure.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states.

### 4. Close the Initiative

Follow [Issue Closure](#issue-closure) for the initiative with the confirmed setting, the verification evidence the last Epic Closure returned and the project checkout.

- Report an incomplete result with its unmet criteria and open epics.

### 5. Sync the Board

Apply [Ensure Project Board](#ensure-project-board) with the owner, repository, the initiative's theme name and title, and the originating proposal's identity its [References](#references-1) name when a proposal derives the theme.

- Return a missing selection or unresolved provenance as a blocker.
- Apply [Record Board Delivery](#record-board-delivery) with the saved initiative, epic and task identities, the returned board identity and an output directory.

### 6. Explain Each Change Entering Review

For each task or epic Record Board Delivery newly moves to In Review, follow [Understand Mode](#dispatch-understand-mode) with the task's open pull request or each epic review pull request, one run per base, where [Ownership](#ownership) gives the overview to this run.

- Complete each overview before continuing.

#### Dispatch Understand Mode

Dispatch `modes_understand-mode.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states.

### 7. Report

Return saved delivery results and unresolved findings to the caller, or present them to the user for a direct request.

- Report queue decisions unevaluated by this run.
Report per issue: tasks linked, criteria ticked, rows marked done, criteria left unticked and why, conflicts, test plan disagreements, what was closed, each board and assignee change, and each overview written. What the report names about criteria is [Coverage Reports](#coverage-reports).

## Outcomes

- **Delivery recorded.**
  The user has each landed task tied to the pull request that delivered it, and has what now holds recorded on the initiative and its epics.
- **Complete work closed.**
  Work that is complete is closed.
- **The board is current.**
  The theme board shows where the initiative and its epics stand, including what a reviewer can take up.
- **A change entering review is explained.**
  Each task and epic that enters review has an overview on the pull request a reviewer reads.
- **The queue stays undecided.**
  A sync on its own leaves the choice of what to start next undecided.

# Rules

- **Decisions.**
  A question the user must decide is put as an interview, one question at a time. A decision the run's [allowance](#allowance) covers is taken with its recommended option rather than asked. Record each decision in the affected issues and, when there is one, the planning record.
  - A plain-language paragraph before the question gives the context the user needs to answer it.
  - The question offers more than one choice. The recommended choice is marked on its option.
  - Wait for the user's answer. An unanswered question stays pending. A recommendation or elapsed time supplies no answer.
  - The user can select Other and specify a response beyond the options.
  - Use the native tool for presenting the question when one is available.
- **Layers.**
  Modes, protocols, artifacts. A mode aggregates protocol calls, as an application calls services; a protocol applies artifact operations and follows other protocols; an artifact does neither. A call goes down the stack, never up. A mode reaches an artifact operation directly only where no protocol owns that change.
- **Execution.**
  A call passes its named inputs. A protocol is one change that lands in several artifacts together, and is followed whole. Follow another mode, a protocol or a named procedure subsection, and apply an artifact operation, only where the procedure calls for it; finish that call and return its result before continuing. Calls run in order. A step's `⇉` call runs in a sub-agent, and its `⫽` calls run in sub-agents together, as the bundle's Prosiform section states; those together never write to the same object.

# Conventions

- **Session.**
  Once per session, before the first `gh` call, unset `GH_TOKEN` and `GITHUB_TOKEN` so `gh` uses its keyring login. Where shell state does not persist between commands, confirm instead that neither is set in the shell profile.
- **Repository.**
  `gh` resolves `{owner}/{repo}` from the git remote of the directory it runs in, so run `gh` commands inside a checkout of the repository that holds the issues. `{other}` is a further repository the board's issues live in.
- **Bodies.**
  - Bodies and long comments always go through a file (`-F body=@file`), never inline, which avoids quoting.
  - **Example.**  workflow-server's dynamic-shell restrictions deny a body inlined in the command.
  - Keep these files in a working directory outside the repository.
- **Scripts.**
  Scripts run under `sbx`, invoked by its absolute path from `<workspace>`, the checkout holding this skill.
- **Boards.**
  A project board sits under `users/{owner}`, or `orgs/{owner}` when `gh api repos/{owner}/{repo} --jq .owner.type` is `Organization`.
- **Example values.**  Substitute the real ones:
  - `936` an initiative issue, `943` and `937` its epics, `637` a task issue, `874` an orphan, `946` an initiative off the board, `960` a proposal;
  - `950` a pull request, `I07` and `I08` initiative numbers;
  - board `9`, workflow-server's Canon theme, and `419167630` its Status field id;
  - `1` the Initiative Template board, `13` a board copied from it;
  - `14` the Proposals Template, `15` the Proposals board;
  - `m2ux` the user.
  - `<checkout>` any checkout of the project, a linked worktree included.

# Artifacts

## Issue

### Operations

#### *Read* Tracker Issue

The current issue, its saved body and discussion.

**Inputs:** Repository, issue number and output files; whether discussion is needed.

##### 1. Fetch the Tracker Issue

Run [Fetch Tracker Issue](#fetch-tracker-issue) for the complete JSON, or [Fetch Issue Body](#fetch-issue-body) for its body, with the issue number and destination file.

##### 2. Fetch the Issue Comments

Run [Fetch Issue Comments](#fetch-issue-comments) when the request depends on the discussion.

#### *Save* Tracker Issue

One populated body and its metadata, written to the tracker.

**Inputs:** Repository, optional existing issue number, populated body file, title and labels for creation; selected body or metadata changes for an existing issue; each assigned label's colour and description. Optional comment file.

##### 1. Take the Issue Body and Metadata

Take the supplied body and metadata, preserving each field the caller does not change for an existing issue.

##### 2. Ensure the Issue Labels

Apply [Ensure Repository Labels](#ensure-repository-labels) with every label the save assigns and its colour and description.

- Return an unknown label definition to the caller before any write.

##### 3. Create New Issue

For a new issue, run [Create Tracker Issue](#create-tracker-issue) with the body's file, title and labels.

##### 4. Update the Existing Issue

For an existing issue, run [Patch Issue Body](#patch-issue-body), [Retitle Tracker Issue](#retitle-tracker-issue), [Add Issue Labels](#add-issue-labels) or [Remove Issue Label](#remove-issue-label) for the fields being changed.

##### 5. Comment on the Saved Issue

Apply [Comment on Issue](#comment-on-issue) for an answer or a preserved body the caller requires, with the issue number and comment file.

##### 6. Re-Read the Saved Issue

Re-read with [Fetch Tracker Issue](#fetch-tracker-issue).

##### 7. Compare the Saved Issue Fields

Compare the saved fields with the intended body and metadata.

#### *Check* Issue Completion

The normal delivery result of one task, epic or initiative before tracker closure.

**Inputs:** Issue kind, current issue JSON, complete Development snapshot, fresh linked pull request records and criterion verification evidence; for a task, the delivery result its delivering pull request established; for an epic, its project checkout.

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

#### *Close* Tracker Issue

Verified completion of an issue and its linked delivery.

**Inputs:** Issue identity, successful normal delivery result, current issue JSON, complete Development snapshot, confirmed repository setting and fresh linked pull request records.

##### 1. Capture the Issue Development

Apply [Capture Issue Development](#capture-issue-development) for the issue's complete links and confirmed repository setting.

##### 2. Take Fresh Pull Request Records

Take the caller's fresh records for every linked pull request, across repositories and states; return missing evidence to the caller.

- Return a repository setting that is unconfirmed or fails [Auto-Close Setting](#auto-close-setting) to the caller as a blocker.
- Take the records only from a fresh destination file, so an earlier snapshot cannot supply membership.
- Use the issue's entire Development field to establish membership. Titles, branch names, body mentions and a list filtered to one initiative do not establish completeness. An explicitly empty field adds no pull request requirement.

##### 3. Run the Closure Check

Run [Check Issue Closure](#check-issue-closure) with `--issue`, `--development`, and `--prs` for those fresh records.

##### 4. Require the Closure Gate

Require normal delivery checks to pass, every criterion to be verified and ticked, and every currently linked pull request to be merged.

- Keep the issue open for an open, draft, closed without merge, or unreadable linked pull request.
- Obtain the user's decision before removing an abandoned or incorrect Development link. A replacement pull request does not remove the requirement on a link still present.

##### 5. Close the Issue as Completed

Apply [Close as Completed](#close-as-completed), which repeats the gate immediately before the write. A changed link set requires another capture and check.

#### *Comment* on Issue

The supplied discussion text saved on one issue.

**Inputs:** Repository, issue number and exact comment text or file; reviewer identity and addressed feedback when replying to a review.

##### 1. Compose the Feedback Reply

When replying to feedback already folded into the body, compose a precise, factual reply addressing each point and mentioning the reviewer, with no thanks or filler. Name what the body now says, by criterion id where one carries it, or the issue that takes the point.

##### 2. Publish the Issue Comment

Publish the supplied comment:

- For a one-line comment, run [Post Inline Comment](#post-inline-comment) with the exact text.
- For a longer comment, run [Post Comment File](#post-comment-file) with the complete file.

##### 3. Return the Comment URL

Return the saved comment URL.

#### *Close* as Completed

An issue closed after its final evidence check.

**Inputs:** Repository, issue number, authenticated access, confirmed repository auto-closing setting, passing normal delivery checks and absolute paths to the current issue, Development and linked pull request evidence.

##### 1. Capture Development Before Closure

Apply [Capture Issue Development](#capture-issue-development) immediately before closure with the issue identity, authenticated access, confirmed repository setting and evidence paths.

##### 2. Compare the Development Links

Compare its links with the supplied fresh pull request records; return a changed link set or missing evidence to the caller for refresh.

##### 3. Run the Completion Gate

Run [Check Issue Closure](#check-issue-closure) with the current issue, Development and linked pull request files, using absolute evidence paths when changing directory.

##### 4. Require the Completion Gate to Pass

Require exit 0 and passing normal delivery checks; a sync report of closable does not permit skipping this gate.

##### 5. Set the Completed State

Immediately after the gate passes, run [Set Completed State](#set-completed-state) with the issue's repository and number and the passing evidence.

##### 6. Return the Completed State

Return the saved state or failure.

#### *Capture* Issue Development

The issue's current content and complete Development snapshot.

**Inputs:** Issue identity, authenticated access, observed repository auto-closing setting and issue and Development output paths.

##### 1. Read the Development Field

Apply [Read Issue Development](#read-issue-development) for the entire field across repositories and states. An inaccessible field returns incomplete evidence; an empty array means the field was checked and empty.

##### 2. Write the Development Snapshot

Run [Write Development Snapshot](#write-development-snapshot) with the issue identity, observed link set, completeness result and repository setting, saving `development-943.json` or the supplied path.

- Set `complete` true only after the full read, and `auto_close_issues` false only after the repository setting is confirmed disabled.

##### 3. Fetch the Issue Snapshot

Run [Fetch Tracker Issue](#fetch-tracker-issue) into `issue-943.json` or the supplied path.

##### 4. Return the Development Files

Return both files and any incomplete evidence. The caller supplies fresh linked pull request records in `development-prs-943.json`.

#### *Read* Issue Development

The Development links observed for one issue through authenticated GitHub.

**Inputs:** Issue identity and authenticated access.

##### 1. Read Every Development Link

Read every page and state, across repositories, recording each linked pull request's identity.

##### 2. Return the Observed Development Links

Return the observed links and whether the entire field was readable.

#### *Confirm* Repository Auto-Close

Whether the repository auto-closes issues whose linked pull requests merge, established for this session.

**Inputs:** Repository and authenticated access.

##### 1. Read the Auto-Close Setting

Read the setting where the authenticated API exposes it, and take a read value as the answer.

##### 2. Ask the User for Auto-Close

Where no API field carries it, put the setting to the user and take their explicit answer, meeting [Auto-Close Setting](#auto-close-setting).

##### 3. Return the Confirmed Auto-Close Setting

Return the confirmed value. An unconfirmed setting is a blocker, and an enabled one leaves the caller to obtain authorization before the repository is reconfigured.

### Fields

#### Auto-Close Setting

GitHub's **Auto-close issues with merged linked pull requests** repository setting, which must be disabled before a delivery pull request is linked or merged, so that closure follows the criteria rather than the merge.

- The setting is confirmed per repository and holds for the session; it is not inferred from an issue that stayed open.
- No REST field and no GraphQL field of `gh` 2.46 carries it, so on such a host the user's explicit answer is the only source.
- An enabled setting closes issues on merge whatever their criteria. Where it cannot be disabled, each affected issue's state is read after every merge and reopened where its criteria are unmet.

### Commands

#### Create Tracker Issue

Creates an issue from a body file, with its title and labels, and prints its number.

**Inputs:** Repository, populated body file, title and existing label names.

Repeat `-f 'labels[]=<label>'` for each supplied label.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues' -f title='<title>' -F 'body=@<body-file>' -f 'labels[]=<label>' --jq .number
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues' -f title='<title>' -F body=@body.md -f 'labels[]=<label>' --jq .number
```

#### Patch Issue Body

Replaces an issue's body from a file.

**Inputs:** Repository, issue number and complete populated body file.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -F 'body=@<body-file>' --jq .number
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -F body=@body.md --jq .number
```

#### Fetch Issue Body

Saves an issue's body alone.

**Inputs:** Repository, issue number and destination file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' --jq .body > '<output-body-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' --jq .body > live-943.md
```

#### Retitle Tracker Issue

Replaces an issue's title.

**Inputs:** Repository, issue number and complete title.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f title='<title>' --jq .title
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -f title='<title>' --jq .title
```

#### Add Issue Labels

Adds labels to an issue.

**Inputs:** Repository, issue number and existing label names.

Repeat `-f 'labels[]=<label>'` for each supplied label.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/labels' -f 'labels[]=<label>' --jq '.[].name'
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/943/labels' -f 'labels[]=<label>' --jq '.[].name'
```

#### Remove Issue Label

Removes one label from an issue.

**Inputs:** Repository, issue number and label name.

```bash
gh api --method DELETE 'repos/<owner>/<repo>/issues/<issue-number>/labels/<label>' --jq '.[].name'
```

**Example:**

```bash
gh api --method DELETE 'repos/<owner>/<repo>/issues/943/labels/<label>' --jq '.[].name'
```

#### Fetch Issue Comments

Prints an issue's comments.

**Inputs:** Repository and issue number.

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/<issue-number>/comments'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/874/comments'
```

#### Fetch Tracker Issue

Saves an issue whole, as JSON, for the scripts that read issues.

**Inputs:** Repository, issue number and destination JSON file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' > '<issue-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' > issue-943.json
```

#### Check Issue Closure

Checks the issue criteria, the complete link snapshot and every linked pull request.

**Inputs:** Current issue JSON, complete Development snapshot and fresh linked pull request records.

- `--issue`, `--development`, and `--prs` are the fresh issue JSON, Development snapshot, and linked pull request records.
- Exit 0 means the closure gate passes; normal delivery checks must also pass. Exit 1 reports blockers. The command performs no network calls or writes.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue '<issue-json-file>' --development '<development-snapshot-file>' --prs '<linked-pull-request-records-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue issue-943.json --development development-943.json --prs development-prs-943.json
```

#### Post Inline Comment

Posts one line of exact comment text and returns its URL.

**Inputs:** Repository, issue number and one-line comment text.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -f body='<comment-text>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/637/comments' -f body='Delivered by #950.' --jq .html_url
```

#### Post Comment File

Posts a complete comment file and returns its URL.

**Inputs:** Repository, issue number and exact comment file.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -F 'body=@<comment-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/874/comments' -F body=@comment-874.md --jq .html_url
```

#### Set Completed State

Sets an issue to closed with the completed reason and returns its state.

**Inputs:** Repository, issue number, passing normal delivery checks and an immediately preceding successful closure gate on current evidence.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f state=closed -f state_reason=completed --jq .state
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -f state=closed -f state_reason=completed --jq .state
```

#### Write Development Snapshot

Saves an observed Development field and repository setting as JSON.

**Inputs:** Repository and issue number, observed links, completeness result, confirmed or unknown auto-closing setting and destination file.

Write the supplied values in this shape. Substitute the issue number as a JSON integer, completeness as a boolean, and the auto-closing setting as a boolean or `null` when unknown. Supply every observed pull request URL, or an empty array when there are none. Preserve incomplete evidence as incomplete.

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

## Task Body

### Fields

#### Template

````markdown
## Overview

{{One paragraph: what this task delivers and why it exists within the epic.}}

## Problem

{{The friction as it is now. Bullets for distinct facets, sub-bullets for several items.}}

## Proposal

{{The design, in bullets or paragraphs, each opening with a bold statement, and its body on the next line.}}

## Acceptance Criteria

- [ ] **AC1.** {{An end state of one invariant. It ends by naming its instrument.}}

## Open Questions

- {{An undecided point the task cannot start without. Resolve every one before the task starts, then delete the section.}}

## References

- **R1.** [{{Title}}]({{URL}}) — {{What the reader finds there. Delete the section when there is none.}}
````

#### Titles

- The title is `[I07:E00:W01] Name: Subtitle`.
- The label is the task [kind label](#kind-labels).
- `W` is the task within the epic. Tasks count from `W01`.

#### Open Questions

- Each holds only what is undecided, and is resolved before the task starts.

#### Acceptance Criteria

- A task criterion meets the [shared acceptance criteria](#shared-acceptance-criteria).

#### Sections

- A task has the [epic issue body](#epic-issue-body)'s sections without the Work Breakdown table.
- New task planning follows [Work Breakdown](#work-breakdown-1). This body describes an existing issue kept as a task.

## Issue Body

### Operations

#### *Write* Issue Table

The shared table, before a kind fills its cells.

**Inputs:** Current body, the kind's table columns and supplied row data.

##### 1. Populate the Shared Table Cells

Populate the shared Done, Coverage and Depends on cells from the supplied row data.

- The columns must match the kind's table.
- The shared cells must meet [Tables](#tables).

##### 2. Read the Finished Issue Table

Read the finished table against [Tables](#tables), [Numbering](#numbering), and [Reference form](#reference-form). A Depends on cell that holds prose fails [Tables](#tables). Numbering that does not follow start order is advisory, as [Numbering](#numbering) states.

#### *Validate* Issue Body

One body checked against its supplied kind and template.

**Inputs:** Issue JSON, kind field conditions, required related evidence and output body file.

##### 1. Run the Body Format Check

Run [Check Body Format](#check-body-format) with the supplied issue JSON, kind inputs and output file as `--fix`.

##### 2. Review the Body Field Conditions

Review the body against the supplied field conditions.

##### 3. Return the Body Validation Findings

Return the [Format Findings](#format-findings), mechanical diff and field findings, including missing sections, extra sections, wrong-kind layout, historical narration and criteria that fail their named instrument. A mechanical correction preserves wording; new content and scope decisions require caller-supplied resolutions.

#### *Apply* Body Corrections

One body rewritten from confirmed local findings.

**Inputs:** Current body, selected kind template and field conditions, related context, confirmed resolutions and output path.

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

#### *Build* Body Snapshot

A local issue-shaped record for body validation.

**Inputs:** Current body file, title, labels, optional existing issue JSON and destination JSON path.

##### 1. Write the Body Snapshot JSON

Write the body's exact text, title and labels to the destination as JSON.

##### 2. Preserve the Issue Identity

Preserve the existing issue's identity and state when supplied.

##### 3. Mark an Unpublished Draft

For an unpublished draft, use `number: null` and `state: "open"`; labels are strings or objects with a name.

##### 4. Return the Snapshot Path

Return the JSON path for validation. No tracker issue is created by this operation.

#### *Repair* Issue Format

The saved format corrections for a set of issues of one kind and any unresolved content findings.

**Inputs:** The kind's validator, either its body file's Validate operation or [Validate Issue Body](#validate-issue-body) with the kind's field conditions; that validator's further inputs; a set of issue bodies, each with its identity, current JSON and output body path; kind template and required related evidence.

##### 1. Apply the Format Validator

Apply the supplied validator to each issue body with its current JSON, output path and the validator's further inputs.

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

Apply [Read Tracker Issue](#read-tracker-issue) for each saved issue.

- Repeat the supplied validator with the saved JSON and the same further inputs, context and output path.
- Return each saved body, whether a correction was made, and the validation result to the caller. A remaining failure is a blocker.

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

### Commands

#### Check Body Format

Checks one issue against its template, and with `--fix` writes the body with the mechanical fixes made.

**Inputs:** Issue JSON, local output body file and the additional format inputs supplied by the kind.

- The format reader takes the template fence from the body artifact and its table columns where present. A body with a Work Breakdown table requires coverage for every criterion.
- The input is one issue JSON. `--fix` names the output body file for mechanical fixes. Further inputs are specified by the calling body procedure.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/format.py '<issue-json-file>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/format.py issue.json --fix fixed.md
```

## Initiative Issue Body

### Operations

#### *Validate* Initiative Body

The body's local format and field findings.

**Inputs:** Initiative JSON, every linked epic JSON, source evidence and output file.

##### 1. Validate the Initiative Issue Body

Apply [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#fields-3), supplied related evidence and output file, supplying each linked epic as `--epic`.

##### 2. Title the Initiative Row

Use its current title for the initiative row.

##### 3. Report Excluded Names and Departures

Include excluded names in Problem and Proposal and criterion/source departures in the findings.

##### 4. Return the Validated Initiative Body

Return the corrected body, mechanical diff and unresolved findings for the caller.

### Fields

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

Populates one epic body. The body states one slice of the design and lists the tasks that deliver it.

### Operations

#### *Populate* Epic Issue Body

One epic body and its local validation findings.

**Inputs:** Initiative context, epic scope, draft title and labels, criteria, proposed task rows, available pull request records, corpus branch and output path.

##### 1. Draft the Epic Body

Populate the body from the [Template](#template-2) at the supplied output path.

- Every section must meet [Fields](#fields-4).
- Shared content must meet the common [body conditions](#fields-2).

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

#### *Record* Epic Delivery

One epic body with supplied delivery matches and completed rows recorded.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches, project checkout and output body file.

##### 1. Run Sync Epic

Run [Sync Epic](#sync-epic), mapping pull requests to `--prs`, links to `--links`, task issues to `--tasks`, each confirmed match to `--link`, the checkout to `--project` and the output file to `--fix`.

- Row changes must meet [Task Delivery](#task-delivery) and [Work Breakdown](#work-breakdown-1).

##### 2. Return the Epic Delivery Findings

Return the updated body and [Delivery Findings](#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.

#### *Record* Epic Criteria

Verified criteria and completed rows in one epic body.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, verified criterion ids and output body file.

##### 1. Run Tick Epic Criteria

Run [Tick Epic Criteria](#tick-epic-criteria) with the epic JSON, records as `--prs`, snapshot as `--links`, verified ids as `--tick` and output as `--fix`. Refuse criteria not ready to verify.

##### 2. Return the Epic Body and Refused Criteria

Return the body and refused criteria. Complete rows receive Done ticks.

#### *Reserve* Task Rows

Task rows held for one confirmed delivery session.

**Inputs:** Epic JSON, confirmed task ids, supplied planning-folder identity, planning-records base URL, record date and output body file.

##### 1. Check the Rows to Reserve

Require the caller's confirmed unit and existing planning folder. Refuse a row already held or linked to a pull request or commit.

##### 2. Run Reserve Row

Run [Reserve Row](#reserve-row) with the epic as `--epic`, ids as `--reserve`, supplied base URL as `--records`, record date as `--date` and output as `--fix`.

##### 3. Return the Reserved Epic Body

Return the body with the folder as each row's single link, meeting [Task Delivery](#task-delivery).

#### *Release* Task Rows

Held task rows returned to their work-item links.

**Inputs:** Epic JSON, task ids, explicit user decision releasing the hold and output body file.

##### 1. Check the Rows to Release

Require the supplied release decision and refuse any row that is not held.

##### 2. Run Release Row

Run [Release Row](#release-row) with the epic as `--epic`, ids as `--release` and output as `--fix`.

##### 3. Publish the Released Epic Body

Publish the returned body through [Save Tracker Issue](#save-tracker-issue).

##### 4. Return the Saved Released Body

Return the saved body with each task id linked to its lowercase work-item file inside the reserved folder, meeting [Task Delivery](#task-delivery).

#### *Validate* Epic Body

The body's local format and field findings.

**Inputs:** Epic JSON, initiative context, current pull request records, corpus branch and output file.

##### 1. Validate the Epic Issue Body

Apply [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#fields-4), supplied related evidence and output file, supplying initiative JSON as `--initiative`, pull requests as `--prs` and corpus branch as `--corpus`.

##### 2. Read Epic Pull Request Reach

Read reach from each epic pull request's base, through an epic base or initiative branch. Without both pull requests and the corpus branch, reach is unevaluable.

##### 3. Report Corpus Audit and Coverage Gaps

Include a missing [Corpus Audit](#corpus-audit) criterion on a corpus-changing epic and any epic criterion no task row delivers in the findings.

##### 4. Return the Validated Epic Body

Return the corrected body, mechanical diff and unresolved findings for the caller.

#### *Revise* Epic Rows

One epic body with confirmed task-grain and coverage corrections.

**Inputs:** Epic body, confirmed row changes, field findings, supplied dependency references and output path.

##### 1. Apply the Confirmed Row Changes

Apply the confirmed row changes through [Populate Epic Issue Body](#populate-epic-issue-body), preserving unrelated content.

- Description, Coverage, Depends on, Joins and task grain must meet [Work Breakdown](#work-breakdown-1).
- Split a task exceeding the allowed criterion grain into the confirmed tasks.

##### 2. Return the Revised Epic Body

Return the revised body and any cross-body numbering or dependency changes for the caller.

#### *Plan* Gap Task

The agreed disposition of criteria a delivered row left unmet.

**Inputs:** Current epic JSON and body, delivered task row, unmet criterion ids, delivery records, complete issue-link snapshot and output body path.

##### 1. Present Unmet Epic Criteria

Present each unmet criterion and its missing evidence to the user.

- Return the criteria the user confirms already hold to the caller for verification and ticking. The delivered task retains them.
- Record an unanswered decision as pending.
- If no criteria need further work, return the pending findings to the caller.
- Continue to [2. Draft the Gap Task](#2-draft-the-gap-task) with only the criteria the user confirms need further work.

##### 2. Draft the Gap Task

Draft a further task for the criteria selected for further work, meeting [Work Breakdown](#work-breakdown-1).

- Confirm the draft with the user.
- On acceptance, apply [Revise Epic Rows](#revise-epic-rows) with the further row and the criteria it adopts from the delivered task's Coverage.
- Return an unanswered draft as pending without continuing to [3. Record the Revised Epic Delivery](#3-record-the-revised-epic-delivery).

##### 3. Record the Revised Epic Delivery

Apply [Record Epic Delivery](#record-epic-delivery) with the revised epic and the supplied delivery evidence.

- Publish the returned body through [Save Tracker Issue](#save-tracker-issue).
- Return the saved row and criterion disposition to the caller. Done follows [Tables](#tables).

#### *Place* Unplaced Task Row

One epic body given the row its table lacks for a task issue of the epic.

**Inputs:** Epic JSON, the unplaced task issue, the run's allowance and change list when supplied, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches, project checkout and output body file.

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

#### Breakdown Prose

Work Breakdown contains its table. Explanatory prose belongs in Proposal. The body does not narrate execution order or how the tables work; Depends on carries the order.

### Commands

#### Sync Epic

Links each named task's id to a pull request naming the epic, open or merged, and ticks Done on a row once it is complete.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, task records, confirmed matches, project checkout and output body file.

- A row whose id links its task issue links the pull request instead.
- A pull request whose head is an epic base is the pull request that merges that base, and is not matched to a task.
- An unmerged epic base keeps the epic open, even when every row is delivered and every criterion is ticked.
- `--project` is a checkout of the project. Without the long-lived branch names, an epic that would otherwise be closable is not.
- `--link` names each task id and the pull request number it links. `--tasks` is the task issues. `--links` is the pull requests' Development-linked issues. `--fix` is the body written with the Done ticks.

`<task-pull-request-map>` is a comma-separated list of `<task-id>=<pull-request-number>` pairs. Pass each task JSON file as a separate argument after `--tasks`.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --tasks '<task-json-file>' --link '<task-pull-request-map>' --project '<checkout>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json --tasks issue-637.json --link W01=950,W02=950 --project '<checkout>' --fix fixed-943.md
```

#### Tick Epic Criteria

Ticks confirmed epic criteria, refusing any not ready to verify, and ticks completed rows.

**Inputs:** Current epic JSON, pull request and link snapshots, verified criterion ids and destination body file.

`<criterion-ids>` is a comma-separated list of verified criterion ids.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --tick '<criterion-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json --tick AC1,AC3 --fix fixed-943.md
```

#### Reserve Row

Holds each named task row for one session, by setting its record folder as the row's single link.

**Inputs:** Epic JSON, confirmed reservable task ids, planning-folder identity, record date, records base URL and output body file.

- `--records` is the URL of the planning records folder, needed when no row id in the epic links a record.
- The caller supplies the planned folder identity; `--date` is the day it is opened.

`<task-ids>` is a comma-separated list of task ids; `<records-base-url>` is the URL of the [records folder](#engineering-branch) on the engineering branch.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic '<epic-json-file>' --reserve '<task-ids>' --records '<records-base-url>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic issue-943.json --reserve W01,W02 --records 'https://github.com/<owner>/<repo>/tree/engineering/artifacts/planning' --fix fixed-943.md
```

#### Release Row

Frees each named task row, by replacing the planning-folder link with its work-item file link.

**Inputs:** Epic JSON, confirmed held task ids, authorized release and output body file.

- The file is the task id in lowercase within that folder, as [Task ids](#task-delivery) defines.

`<task-ids>` is a comma-separated list of task ids.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic '<epic-json-file>' --release '<task-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic issue-943.json --release W01 --fix fixed-943.md
```

## Plan Change

### Operations

#### *Check* Plan Change Autonomy

One pending change assessed against the run's allowance.

**Inputs:** The pending change, its subject, the option recommended for it, and the allowance the caller was supplied.

##### 1. Match the Plan Change Kind

Match the change to one kind in [Change Kinds](#change-kinds).

##### 2. Return an Automatic Plan Change

Return it as automatic where the supplied allowance names that kind, with the supplied recommendation as the option the caller applies.

##### 3. Return a Held Plan Change

Return it as [held](#held-change) otherwise.

- A change matching no kind is held, as is one matching [Initiative Creation](#initiative-creation).
- An absent allowance holds every change, so a run the user drives decides nothing on their behalf.

#### *Record* Plan Change

One entry in the run's list, for a change it applied or held.

**Inputs:** The change, its kind, the option applied or recommended, the affected issue identities and the run's current list.

##### 1. Add the Plan Change Entry

Add one entry meeting [Entry](#entry) to the supplied [Change List](#change-list), marked applied or held.

##### 2. Return the Updated Change List

Return the updated list for the caller to publish and report.

#### *Settle* Plan Change

One pending change carried to its outcome: applied, held, or answered by the user.

**Inputs:** The pending change, its subject, the option recommended for it, the affected issue identities, the allowance the caller was supplied, and the run's current [Change List](#change-list).

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

One line: the kind, the issue or row it concerns, and the option applied or recommended. The entry states the change, not the alternatives weighed against it.

#### Held Change

A held change is left unapplied and its subject stays as it stands, so the next run sees the same decision. Its entry carries the recommended option, which is what the user is answering.

## Delivery Evidence

### Operations

#### *Read* Board Delivery Evidence

The board snapshot and pull request records that establish current delivery across one board.

**Inputs:** Board owner and number, authenticated access, output paths and destination snapshot files.

##### 1. Apply the Board Reads

Apply the [board reads](#run-board-reads).

##### 2. Return the Board Delivery Evidence

Return the [board snapshot](#board-snapshot), pull request records and complete issue-link snapshot to the caller, reporting incomplete evidence as a blocker.

##### Run Board Reads

###### 1. Read Board State

Apply [Read Board State](#read-board-state) with the board owner and number for its items, Status field and [repositories](#repositories).

###### 2. Fetch Initiative Pull Requests

Apply [Fetch All Initiative Pull Requests](#fetch-all-initiative-pull-requests) for each repository Read Board State returned, for the pull request records.

###### 3. Fetch Pull Request Issue Links

Apply [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links) with the pull request records Fetch Initiative Pull Requests returned, for the complete issue-link snapshot.

###### 4. Read Board Configuration

Apply [Read Board Configuration](#read-board-configuration) with the board owner and number and output paths for the board fields.

###### 5. Read Board Assignee

Apply [Read Board Assignee](#read-board-assignee) for the assignee login.

### Fields

#### Board Snapshot

The board items with their Status, the Status field, the board fields, the board's [repositories](#repositories) and the assignee login, read together with the board's pull request records and issue-link snapshot.

#### Unnamed Deliveries

A pull request whose issue links reach an epic or its task issues while its title omits that epic's reference. Each is named with the epic it reaches, for the user to confirm.

#### Named Delivery

A pull request that delivers an epic carries that epic's reference in its title, as `[I07:E00] Purpose`. A delivery the user confirms whose title omits its epic is repaired to carry that reference.

## Pull Request

### Operations

#### *Access* Development Links

The observed or updated Development relation for a pull request.

**Inputs:** Pull request identity, authenticated access and requested relation read or write; for an edit, the issue identity, confirmed repository prerequisite and any user decision authorizing removal of an abandoned or incorrect link, meeting the applicable preconditions in [Close Tracker Issue](#close-tracker-issue).

##### 1. Read the Pull Request Development Links

Run [Read Development Links](#read-development-links) for the actual field, including every page and state. A missing tool or inaccessible field is a blocker, not an empty link set.

##### 2. Return the Read-Only Relation

Return the complete relation for a read-only request.

##### 3. Edit the Development Links

For a link edit:

- Take the supplied repository prerequisite from [Confirm Repository Auto-Close](#confirm-repository-auto-close); an unconfirmed setting blocks the edit.
- For an addition, run [Set Development Link](#set-development-link) with the pull request and issue identities.
- For removal of an abandoned or incorrect link:
  - Require the supplied user decision.
  - Run [Remove Development Link](#remove-development-link) with those identities.

##### 4. Re-Read the Pull Request Development Links

Run [Read Development Links](#read-development-links) again for the same pull request.

##### 5. Compare the Field with the Edit

Compare the field with the intended edit.

##### 6. Return the Verified Link Relation

Return the verified relation or discrepancy.

#### *Fetch* Pull Request Issue Links

The complete issue-link snapshot for a supplied set of pull requests.

**Inputs:** Current pull request records, authenticated access and destination link-snapshot file.

##### 1. Read Links for Each Pull Request

For every pull request in `prs.json`, apply [Access Development Links](#access-development-links) with a read-only request and its identity. An observed empty field supplies an empty array; an unreadable field leaves the fetch incomplete.

##### 2. Re-Read Links After a Change

Repeat that read after a link changes.

##### 3. Return an Incomplete Link Fetch

If any relation is unreadable, return the incomplete result.

##### 4. Write the Links Snapshot

Run [Write Pull Request Links](#write-pull-request-links) with the observed complete relations and destination `links.json`, including one entry per pull request and every linked issue's repository and number.

##### 5. Return the Links Snapshot

Return the snapshot for the scripts' `--links` input.

#### *Link* Pull Request to Issue

The verified delivery-issue relation for a pull request.

**Inputs:** Pull request identity, delivery issue identity, current pull request records, link-snapshot destination, authenticated access and the caller's confirmed repository prerequisite documented in [Close Tracker Issue](#close-tracker-issue).

##### 1. Add the Development Link

Apply [Access Development Links](#access-development-links) with the supplied identities, requested link addition and confirmed repository prerequisite.

##### 2. Stop on an Unverified Link Edit

Stop on a blocker or an unverified edit.

##### 3. Refresh the Links Snapshot

Apply [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links) with the current records and destination after the edit.

##### 4. Return the Verified Link and Snapshot

Return the verified relation and refreshed snapshot.

#### *Fetch* All Initiative Pull Requests

The pull request collection covering every supplied board repository.

**Inputs:** Ordered repository list and destination JSON-lines file.

##### 1. Fetch the First Repository Pull Requests

Run [Fetch Repository Initiative Pull Requests](#fetch-repository-initiative-pull-requests) for the first repository and destination `prs.json`. This replaces the destination with a fresh collection.

##### 2. Stop on a First Fetch Failure

Stop on failure.

##### 3. Append Further Repository Pull Requests

Run [Append Repository Initiative Pull Requests](#append-repository-initiative-pull-requests) for each further repository, passing the same destination.

##### 4. Return Incomplete Pull Request Evidence

If any fetch failed, return incomplete evidence.

##### 5. Return the Complete Pull Request Collection

Return the complete collection only after every fetch succeeds.

#### *Read* Pull Request State

One current pull request and its requested supporting records.

**Inputs:** Repository, pull request number, output paths and requested records: metadata, changed paths or reviews.

##### 1. Fetch the Pull Request Snapshot

Run [Fetch Pull Request](#fetch-pull-request) or [Save Pull Request Snapshot](#save-pull-request-snapshot) for current identity, state, head and base.

##### 2. Fetch Requested Files or Reviews

Run [Fetch Pull Request Files](#fetch-pull-request-files) or [Fetch Pull Request Reviews](#fetch-pull-request-reviews) when the caller requests those records.

##### 3. Return the Pull Request Snapshots

Return the snapshots or missing evidence.

#### *Publish* Pull Request

One pull request created or updated from supplied content and metadata.

**Inputs:** Repository, optional pull request number, task, epic or planning-discussion kind, body file and selected title, head or base changes, and, for a created delivery pull request, its delivery issue identity, the repository setting confirmed for the session and a link-snapshot destination.

##### 1. Open a New Pull Request

For creation, run [Open Task Pull Request](#open-task-pull-request), [Open Epic Pull Request](#open-epic-pull-request) or [Open Discussion Pull Request](#open-discussion-pull-request) for the supplied kind, body, title, head and base, preserving epic and discussion draft state.

- For a task or epic pull request, apply [Link Pull Request to Issue](#link-pull-request-to-issue) with it, the supplied delivery issue, that confirmed setting and the snapshot destination, meeting [Issue Links](#issue-links).

##### 2. Update the Existing Pull Request

For an existing pull request, run [Patch Pull Request Body](#patch-pull-request-body), [Retitle Pull Request](#retitle-pull-request) or [Retarget Pull Request](#retarget-pull-request) for the supplied changes, preserving other fields.

##### 3. Re-Read the Published Pull Request

Re-read through [Read Pull Request State](#read-pull-request-state).

##### 4. Return the Published State

Return the saved state or discrepancy.

### Fields

#### Issue Links

- GitHub shows the link in the pull request's Development field and in the issue's Linked pull requests field, which the project board reads.
- A task pull request links the task's issue, and a review pull request links its epic's issue.
- The link is addressed by issue, so a pull request whose work carries no issue links nothing. A task pull request delivering rows that have no issue of their own is the whole of what stays unlinked.
- The link is stored on the pull request. It holds on any base branch and on a pull request that has merged, and a later body edit leaves it standing.
- A linked issue remains open until its criteria and delivery requirements hold and every Development-linked pull request is merged.
- The field is the whole of the relation: neither body links the other. The pull request's References carry its sources, and the issue it delivers is not among them.
- A pull request with a delivery issue but no Development link is uncited.

### Commands

#### Open Discussion Pull Request

Opens a draft for the supplied planning branch and body.

**Inputs:** Repository owner and name, title, planning branch, target branch and body file.

```bash
gh api --method POST 'repos/<owner>/<repository>/pulls' -f title='<title>' -f head='<planning-branch>' -f base='<target-branch>' -F body=@'<body-file>' -F draft=true
```

**Example:**

```bash
gh api --method POST repos/m2ux/workflow-server/pulls -f title='Queue Planning: Scope and Delivery' -f head=planning/queue -f base=engineering -F body=@discussion.md -F draft=true
```

#### Retarget Pull Request

Points a pull request at another base branch, such as its epic's base branch.

**Inputs:** Repository, pull request number and target branch.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/<pull-request-number>' -f base='<target-branch>' --jq .base.ref
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/950' -f base='i07/e00/main' --jq .base.ref
```

#### Fetch Pull Request

Appends one pull request, as one JSON line, to the supplied file.

**Inputs:** Repository, pull request number and destination JSON-lines file.

```bash
gh api 'repos/<owner>/<repo>/pulls/<pull-request-number>' --jq . >> '<pull-request-records-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/pulls/439' --jq . >> prs.json
```

#### Retitle Pull Request

Replaces a pull request's title.

**Inputs:** Repository, pull request number and complete title.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/<pull-request-number>' -f title='<title>' --jq .title
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/950' -f title='[I07:E00] Purpose' --jq .title
```

#### Open Task Pull Request

Creates a pull request from a unit's branch to its epic base.

**Inputs:** Repository, title, task head, epic base and populated body file.

- Supply the epic prefix and purpose as title, the task branch as head, the epic base as base, and the complete body file.

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='<title>' -f head='<task-branch>' -f base='<epic-base>' -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='[I07:E00] Purpose' -f head='i07/e00/w01-purpose' -f base='i07/e00/main' -F body=@body.md --jq .html_url
```

#### Open Epic Pull Request

Creates the draft pull request from an epic base to its long-lived target.

**Inputs:** Repository, title, epic head, long-lived base and populated review body file.

- Supply the epic prefix and name as title, the epic base as head, its long-lived branch as base, and the populated review body file.
- `draft` is true, including when the work is already complete.

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='<title>' -f head='<epic-base>' -f base='<long-lived-base>' -F draft=true -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='[I07:E00] Name' -f head='i07/e00/main' -f base='main' -F draft=true -F body=@body.md --jq .html_url
```

#### Patch Pull Request Body

Replaces a pull request's body.

**Inputs:** Repository, pull request number and complete populated body file.

- The file is the whole body. The issue a pull request delivers is linked on the pull request itself, so this call leaves that link standing.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/<pull-request-number>' -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/950' -F body=@pr-950.md --jq .html_url
```

#### Read Development Links

Returns the complete Development relation through authenticated GitHub or an available supported tool.

**Inputs:** Pull request identity and authenticated access.

Read the actual field across every page and state, recording repository and number for each linked issue. Return the links and whether the field was fully readable.

#### Set Development Link

Adds one pull request to an issue's Development relation.

**Inputs:** Pull request identity, issue identity, authenticated access and confirmed repository prerequisite.

Use [GitHub's sidebar linking procedure](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue): in the issue's Development selector, select the pull request's repository and pull request, including a different repository when required. Return the edit result.

#### Remove Development Link

Removes one selected Development relation.

**Inputs:** Pull request and issue identities, authenticated access and the user's decision authorizing removal of the abandoned or incorrect link.

Deselect the supplied relation in the authenticated Development selector and save the edit. Return the edit result.

#### Write Pull Request Links

Saves complete observed Development-linked issues as a JSON array.

**Inputs:** One complete relation per pull request, with all repository and number pairs, and destination link-snapshot file.

Write the supplied relations in this shape. Substitute numbers as JSON integers. Include each pull request and all its linked issues; use an empty array for a complete relation with no linked issues. Each repository is the one belonging to that pull request or issue.

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

#### Save Pull Request Snapshot

Saves one complete pull request response, replacing the destination file.

**Inputs:** Repository, pull request number and destination JSON file.

```bash
gh api 'repos/<owner>/<repo>/pulls/<pull-request-number>' > '<pull-request-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/pulls/980' > epic-pr.json
```

#### Fetch Pull Request Reviews

Saves every review on one pull request.

**Inputs:** Repository, pull request number and destination file.

```bash
gh api --paginate 'repos/<owner>/<repo>/pulls/<pull-request-number>/reviews?per_page=100' > '<reviews-file>'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/pulls/980/reviews?per_page=100' > reviews.json
```

#### Fetch Repository Initiative Pull Requests

Starts a collection with all initiative-prefixed pull requests from one repository.

**Inputs:** Repository and destination JSON-lines file.

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' > '<pull-request-records-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' > prs.json
```

#### Append Repository Initiative Pull Requests

Appends all initiative-prefixed pull requests from one further repository.

**Inputs:** Repository and existing destination JSON-lines file.

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' >> '<pull-request-records-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' >> prs.json
```

#### Fetch Pull Request Files

Saves the paths a pull request changes.

**Inputs:** Repository, pull request number and destination path-list file.

```bash
gh api --paginate 'repos/<owner>/<repo>/pulls/<pull-request-number>/files' --jq '.[].filename' > '<changed-paths-file>'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/pulls/950/files' --jq '.[].filename' > changed-files.txt
```

## Board

### Operations

#### *Select* Project Board

The theme or proposals board the request names.

**Inputs:** Board owner and either a theme name or the proposals-board selection.

##### 1. Find the Named Board

Run [Find Theme Board](#find-theme-board) for the named theme, or [Find Proposals Board](#find-proposals-board) with the [proposals board](#proposals-board) title when the request names proposals. The selection meets [Themes](#themes) or [Proposals](#proposals).

##### 2. Report a Missing Board Selection

Return a missing-selection result when neither a theme nor proposals is specified; the caller obtains that choice.

##### 3. Return the Selected Board Number

Return the selected board number, or an absent-board result for [Copy Project Board](#copy-project-board). Work one board at a time.

#### *Copy* Project Board

A missing theme board, or a missing proposals board.

**Inputs:** Board owner, repository, selected board kind, theme title and originating proposal record when applicable.

##### 1. Create an Absent Proposals Board

When no open board carries the [proposals board](#proposals-board) title, apply [Create Proposals Board](#create-proposals-board). The copy source and the title meet [Proposals](#proposals).

##### 2. Create an Absent Theme Board

When the selected theme board is absent:

- Apply [Create Theme Board](#create-theme-board) with the owner, repository, theme title and originating proposal record when applicable.
- Require the new theme's label and board before an initiative takes that theme.

#### *Ensure* Project Board

The theme or proposals board the request names, created when it is absent.

**Inputs:** Board owner, repository, either a theme name and title or the proposals-board selection, and the originating proposal's identity when a proposal derives the theme.

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

#### *Create* Proposals Board

A new proposals board linked to the supplied repository.

**Inputs:** Board owner and repository.

##### 1. Find the Proposals Template

Run [Find Board Template](#find-board-template) with the owner and the proposals board's [template title](#board-templates).

##### 2. Use the Proposals Template as Source

Use the returned number as the copy source.

##### 3. Copy the Proposals Template

Run [Copy Board Template](#copy-board-template) with that template number, the owner and the [proposals board](#proposals-board) title.

##### 4. Retain the Proposals Board Number

Retain the new board number. The copy meets [Proposals](#proposals).

##### 5. Link the Proposals Board to the Repository

Run [Link Board to Repository](#link-board-to-repository) with the owner, new board number and repository.

##### 6. Return the Proposals Board Number

Return the new board number after linking succeeds.

#### *Create* Theme Board

A new theme board linked to the supplied repository.

**Inputs:** Board owner, repository, theme title and originating proposal record when applicable.

##### 1. Require the Originating Proposal

Require the originating proposal record for a proposal-derived board; return a missing-input finding when its designator is unavailable.

##### 2. Find the Initiative Template

Run [Find Board Template](#find-board-template) with the owner and the theme board's [template title](#board-templates).

##### 3. Use the Initiative Template as Source

Use the returned number as the copy source.

##### 4. Copy the Initiative Template

Run [Copy Board Template](#copy-board-template) with that template number, the owner and the title required by [One Board Per Theme](#one-board-per-theme).

##### 5. Retain the Theme Board Number

Retain the new board number. The copy carries the template's theme board [Status options](#status-field).

##### 6. Link the Theme Board to the Repository

Run [Link Board to Repository](#link-board-to-repository) with the owner, new board number and repository.

##### 7. Return the Theme Board Number

Return the new board number after linking succeeds.

#### *Read* Board State

The selected board's items and status fields.

**Inputs:** Existing board owner and number, as [Select Project Board](#select-project-board) or [Copy Project Board](#copy-project-board) returns them, whether the caller ran that operation or carries its result.

##### 1. Find the Board Status Field

Run [Find Status Field](#find-status-field) for the board number and the [Status field](#status-field) name.

##### 2. Fetch Board Items with Status

Run [Fetch Board Items with Status](#fetch-board-items-with-status), passing that field id and board number.

##### 3. Return the Board State

Return the items, Status field, item ids and the board's [Repositories](#repositories) to the caller.

#### *Read* Board Assignee

The authenticated login available for board assignments.

**Inputs:** Authenticated repository access.

##### 1. Find the Board User

Run [Find User](#find-user).

##### 2. Return the Assignee Login

Return its login for the caller's assignment decisions.

#### *Read* Board Configuration

One board's field definitions and requested item state.

**Inputs:** Board owner and number, output paths and optional item identity.

##### 1. Fetch the Configured Board Fields

Run [Fetch Board Fields](#fetch-board-fields) for the supplied board.

##### 2. Fetch the Requested Board Item

When a single item is requested for write confirmation, run [Fetch Board Item](#fetch-board-item). A list snapshot may lag a write.

##### 3. Return the Board Configuration

Return the field definitions and requested current item.

### Fields

#### Themes

Every initiative belongs to one theme, and each theme has one project board. Each project names its own themes, with their labels, in [Theme Labels](#theme-labels).

#### One Board Per Theme

- A proposal-derived board title is the originating proposal's exact `[Pxx]` designator, a space, the theme name, a colon, and its description: `[P03] Canon: Definitions Checked Against the Design Canon`. Preserve the proposal's digits exactly. A board with no originating proposal uses `Name: Description`.
- It is linked to the repository.
- It holds the theme's initiatives, their epics and their task issues.

#### Repositories

A board's repositories are those its items' issues live in, read from each item's issue, deduplicated and ordered with the board's own repository first. An item whose issue is unreadable leaves the list incomplete, which is reported rather than filled by assumption.

#### Assignees

An issue at Ready, In Progress, In Review or Done is assigned to the user; one in Backlog has no assignee. An assignee is set on the issue, not on the board item, so the call that changes one acts on the issue.

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

### Commands

#### Find Board Template

Prints the number of the open board with the supplied exact template title.

**Inputs:** Board owner and template title.

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "<template-title>") | .number'
```

#### Copy Board Template

Copies the supplied template into a new open board with the supplied title and prints its number.

**Inputs:** Board owner, template board number and new board title.

- The copy's JSON is one project; `.number` identifies the new board.

```bash
gh project copy '<template-number>' --source-owner '<owner>' --target-owner '<owner>' --title '<board-title>' --format json --jq .number
```

#### Link Board to Repository

Links one board to the supplied repository.

**Inputs:** Board owner, board number and repository.

```bash
gh project link '<board-number>' --owner '<owner>' --repo '<repo>'
```

#### Find Proposals Board

Prints the number of the open board with the supplied title.

**Inputs:** Board owner and the [proposals board](#proposals-board) title.

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "<proposals-board-title>") | .number'
```

#### Fetch Board Fields

Saves a board's fields.

**Inputs:** Board owner, board number and destination file.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/fields?per_page=100" > '<board-fields-file>'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/fields?per_page=100" > fields.json
```

#### Find Theme Board

Prints the number of the open board for one theme, by its theme name after any proposal designator.

**Inputs:** Board owner and theme name.

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title | sub("^\\[P[0-9]+\\] "; "") | startswith("<theme-name>: ")) | .number'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title | sub("^\\[P[0-9]+\\] "; "") | startswith("Canon: ")) | .number'
```

#### Find Status Field

Prints the id of a board's Status field.

**Inputs:** Board owner and number, and the [Status field](#status-field) name.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/fields?per_page=100" --jq '.[] | select(.name == "<status-field-name>") | .id'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/fields?per_page=100" --jq '.[] | select(.name == "Status") | .id'
```

#### Fetch Board Items with Status

Saves a board's items with their Status, each carrying its issue whole.

**Inputs:** Board owner and number, Status field id and destination file.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/items?per_page=100&fields=<status-field-id>" > '<board-items-file>'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/items?per_page=100&fields=419167630" > items.json
```

#### Fetch Board Item

Reads one board item, including its current Status.

**Inputs:** Board owner and number, item id and Status field id.

```bash
gh api "users/<owner>/projectsV2/<board-number>/items/<item-id>?fields=<status-field-id>"
```

**Example:**

```bash
gh api "users/<owner>/projectsV2/9/items/1001?fields=419167630"
```

#### Find User

Prints the login `gh` runs as, the user assigned to work from Ready on.

**Inputs:** Authenticated repository access.

```bash
gh api user --jq .login
```

## Board Delivery

### Operations

#### *Plan* Board Changes

The board changes implied by supplied delivery state.

**Inputs:** Initiative JSON, epic and task records, pull request records, complete issue-link snapshot, board identity, fields and items, output directory, assignee login and resolved off-board issue files.

##### 1. Require the Board Change Link Snapshot

Require the complete pull-request issue-link snapshot; refuse the computation without it.

##### 2. Compute the Board Changes

Run [Compute Board Changes](#compute-board-changes), mapping the supplied records and board context to its parameters.

##### 3. Return the Planned Board Calls

Return the generated calls and unresolved references, meeting [Fields](#fields-9). The caller gathers missing evidence, applies changes and confirms their live state.

#### *Record* Board Delivery

The board's status and assignees after its issues record delivery.

**Inputs:** Saved initiative, epic and task identities, board identity and output directory.

##### 1. Read the Delivery Evidence

Read the issues and the board's delivery evidence.

- Apply [Read Tracker Issue](#read-tracker-issue) for the saved initiative, epic and task identities.
- Apply [Read Board Delivery Evidence](#read-board-delivery-evidence) with the board identity and output directory.
- Pass the returned issue records, board snapshot, pull request records and complete issue-link snapshot to Plan Board Changes.

##### 2. Plan the Delivery Board Changes

Apply [Plan Board Changes](#plan-board-changes) with the initiative JSON, linked epic records, task issue records, pull request records, complete issue-link snapshot, board identity, board fields, board items, output directory, and assignee login.

- Fetch each unresolved issue.
- Pass the fetched files to Plan Board Changes as resolved off-board issue files.

##### 3. Run the Delivery Board Calls

Run each emitted call, including the assignee calls, which act on the issue rather than the board item.

- Apply [Read Board Configuration](#read-board-configuration) with the board identity, output paths and changed item identity to confirm its current status.
- If that item still shows the preceding status:
  - Repeat its write.
  - Repeat the same item read. The item list can lag a write.

##### 4. Re-Read the Delivery Evidence

Read the issues and the board's delivery evidence again, as [1. Read the Delivery Evidence](#1-read-the-delivery-evidence) does.

- Apply [Plan Board Changes](#plan-board-changes) with the refreshed initiative JSON, linked epic records, task issue records, pull request records, complete issue-link snapshot, board identity, board fields, board items, output directory, assignee login, and every resolved off-board issue file.
- Stop when it emits no further call and every changed item has been confirmed. An issue added in one pass gets its status in the next.

### Fields

#### Status Changes

An open initiative or epic whose criteria are all ticked is In Review. An epic with an open pull request and a criterion unticked is In Progress.

An initiative or epic with no open pull request and unticked criteria keeps Ready or Backlog, and keeps In Progress when delivery has started. In Review then becomes In Progress. One not yet on the board is added at Backlog, or at In Progress when delivery has started. Delivery does not move an initiative or epic between Ready and Backlog.

Task readiness meets [Task Eligibility](#task-eligibility). The caller supplies saved issue bodies and closure state.

A task gated on an [unresolvable dependency](#unresolvable-dependencies) keeps the Status it holds: the row waits on no delivery, so no status follows from its gate. The run names the row and the entry and exits nonzero, as every reader of that cell does.

#### Change Calls

The result contains calls for issues to add, items to remove, Status to set and assignees to add or remove. Each call names its affected issue and board item. Assignees follow [Assignees](#assignees).

#### Missing Evidence

Unresolved issue references identify dependency records the caller must supply before a complete result. A newly added issue receives its status on a subsequent pass using refreshed items.

### Commands

#### Compute Board Changes

Computes membership, Status and assignee calls from supplied delivery evidence.

**Inputs:** Initiative JSON, epic and task JSON records, pull request and complete issue-link snapshots, board identity, board fields and items, output directory, assignee login and resolved off-board issue records.

- `--epics`, `--tasks`, `--prs` and `--links` receive the related records and complete link snapshot.
- `--board`, `--fields` and `--items` identify the current board state.
- `--out` receives the call files; `--assignee` is the supplied login.
- `--others` supplies each resolved dependency issue.

Pass each epic or task JSON file as a separate argument after its corresponding flag.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/board.py '<initiative-json-file>' --epics '<epic-json-file>' --tasks '<task-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --board '<board-identity>' --fields '<board-fields-file>' --items '<board-items-file>' --out '<output-directory>' --assignee '<assignee-login>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/board.py issue-936.json --epics issue-943.json issue-937.json --tasks issue-637.json --prs prs.json --links links.json --board 'users/<owner>/projectsV2/9' --fields fields.json --items items.json --out board/ --assignee m2ux
```

## Architecture Overview

### Fields

#### Ownership

One overview explains one pull request, and a reviewer meets it on that pull request. The run that integrates an epic base owns that epic's overview. Any other run writes an overview only for a task or epic entering review that no integration explained. An overview already written is kept: the pull request it explains is the one already reviewed. An initiative has no overview of its own.

## Repository Labels

### Operations

#### *Ensure* Repository Labels

The required label definitions available for issue publication.

**Inputs:** Repository and required label names, colours and descriptions.

##### 1. List the Repository Labels

Run [List Labels](#list-labels) for the repository.

##### 2. Compare Required Label Names

Compare the returned labels with the supplied required names.

##### 3. Create Absent Required Labels

Run [Create Label](#create-label) for each absent required definition.

##### 4. Return the Available Labels

Return the available labels; an unknown definition is a finding for the caller to resolve before publication.

### Commands

#### List Labels

Lists the labels that exist in the repository.

**Inputs:** Repository.

```bash
gh api "repos/<owner>/<repo>/labels?per_page=100" --jq '.[].name'
```

#### Create Label

Creates the label specified by its name, colour and description.

**Inputs:** Repository, label name, colour and description.

```bash
gh api --method POST 'repos/<owner>/<repo>/labels' -f name='<label>' -f color='<hex-colour>' -f description='<description>' --jq .name
```

## Delivery Branches

### Operations

#### *Read* Delivery Branches

The configured long-lived branches and existing epic bases.

**Inputs:** Project checkout and epic identity.

##### 1. Read the Long-Lived Branch Configuration

Run [List Long-Lived Branches](#list-long-lived-branches) with the supplied checkout. Missing or empty configuration leaves branch names unevaluable.

##### 2. Read the Epic Base Names

Run [List Epic Bases](#list-epic-bases) for the supplied epic.

##### 3. Return the Delivery Branch Collections

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

### Commands

#### List Epic Bases

Prints one epic's base branch names, one per line.

**Inputs:** Repository checkout and epic branch prefix.

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

#### List Long-Lived Branches

Prints the long-lived branch names, one per line.

**Inputs:** Project checkout.

- The names meet [Branches](#branches).
- `--project` is any checkout of the project. The names are the ones `config/branches` states in its main working tree, which a linked worktree resolves for itself.
- A missing or empty statement prints `unevaluable:`, names what is missing, and exits 1.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py --names --project '<checkout>'
```

## Epic

### Operations

#### *Inspect* Epic Delivery

The delivery findings for one epic from supplied evidence.

**Inputs:** Epic JSON, current pull request records and complete issue-link snapshot.

##### 1. Match Epic Pull Requests

Run [Match Pull Requests](#match-pull-requests) with the epic JSON, pull request records as `--prs` and link snapshot as `--links`.

##### 2. Return the Inspected Delivery Findings

Return the [Delivery Findings](#delivery-findings); missing linked pull requests are missing evidence for the caller to supply.

#### *Check* Epic Readiness

The epic's eligibility for integration from current delivery and criterion evidence.

**Inputs:** Current epic JSON, pull request records, complete issue-link snapshot and criterion verification evidence for the current delivery revisions.

##### 1. Inspect the Epic Delivery

Apply [Inspect Epic Delivery](#inspect-epic-delivery) with the supplied epic JSON, pull request records and complete issue-link snapshot.

##### 2. Confirm Epic Integration Conditions

Confirm every task is delivered, every epic criterion is verified and ticked, and no open question or unresolved delivery discrepancy remains. An unmerged epic base awaiting integration is expected at this stage. Missing or stale verification leaves readiness unconfirmed.

##### 3. Return the Epic Integration Readiness

Return the integration readiness in [Delivery State](#delivery-state), with the evidence revisions and each blocker. Readiness establishes the epic's content conditions; the caller supplies pull-request review, target and head-check evidence for the merge.

#### *Check* Epic Completion

The epic's normal delivery result before tracker closure.

**Inputs:** Current epic JSON, pull request records, complete issue-link snapshot, current criterion verification evidence, complete expected base list and each base's merge evidence.

##### 1. Check the Epic Readiness

Apply [Check Epic Readiness](#check-epic-readiness) with the current epic, pull request records, issue-link snapshot and criterion verification evidence.

##### 2. Reconcile Epic Bases with Task Targets

Reconcile the expected bases with the task delivery targets.

##### 3. Confirm Every Epic Base Merged

Confirm every base has merged into its corresponding long-lived branch. An unknown or incomplete base list, or missing merge evidence, leaves completion unconfirmed even when every task is delivered and every criterion is ticked.

##### 4. Return the Epic Completion Result

Return the completion result in [Delivery State](#delivery-state), identifying remaining blockers. Passing normal delivery checks supplies the caller's closure evidence; the tracker issue's current Development-link gate still governs the write.

### Fields

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

### Commands

#### Match Pull Requests

Reports an epic's delivery state against the pull requests that name it.

**Inputs:** Epic JSON, pull request records and complete issue-link snapshot.

- Results follow [Delivery Findings](#delivery-findings).

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json
```

## Initiative

### Operations

#### *Check* Initiative Completion

The initiative's normal delivery result before tracker closure.

**Inputs:** Current initiative JSON, every linked epic's current JSON, criterion verification evidence and the current complete Development-link and linked pull-request records.

##### 1. Evaluate Initiative Delivery Evidence

Evaluate the supplied evidence against [Delivery State](#delivery-state-1).

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

## Board Queue

### Fields

#### Task Eligibility

A task is Ready only when its epic is Ready or In Progress and every row its Depends on cell names is delivered. A row naming another epic's row waits for that epic to close, since its output reaches this epic's base when that epic's bases merge, and the rows beside it wait for nothing it waits on. The queue contains no task issue changes; task status comes from the supplied delivery state.

#### Unresolvable Dependencies

A `Depends on` entry that names no row and links no issue, names an issue the run was not given, or names a row the epic it points to does not carry, cannot resolve. No delivery makes it readable, so it is told apart from a prerequisite that has not landed.

- The report names the row and the entry as written, and a run that met one while deciding a placement exits nonzero.
- The epic that row gates keeps the Status it holds. The run proposes no move for it, so a Ready epic is not returned to Backlog on an entry nobody can read.
- Every entry of a cell is read, so a cell carrying two names both.
- A note raised while reading delivery rather than deciding a placement is reported and leaves the exit status alone.

# Protocols

## Issue Closure

Fresh closure evidence assembled across an issue and its linked pull requests, and the closure it permits.

Follow the [Procedure](#procedure-1), adhering to [Rules](#rules) and [Conventions](#conventions).

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
