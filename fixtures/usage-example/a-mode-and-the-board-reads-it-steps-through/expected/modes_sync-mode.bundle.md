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
  - Bodies, long comments and commit messages always go through a file (`-F body=@file`), never inline, which avoids quoting. The file holds the exact intended text.
  - Keep these files in a working directory outside the repository.
- **Helper invocation.**
  A helper is a script in `<workspace>`, the checkout holding this skill. It runs from `<workspace>`, or the directory within it that its command names, under the sandbox invoked by its absolute path, `<workspace>/scripts/sbx`. A file kept outside `<workspace>`, such as a body file, is passed by its absolute path.
- **Write confirmation.**
  Only a fresh re-read confirms a write: read the written object again and compare it with the intended state. The write's own output confirms nothing. A re-read that fails, or shows another state, leaves the write uncertain; that uncertainty returns to the caller, and the write is never retried as a different write.
- **Boards.**
  A project board sits under `users/{owner}`, or `orgs/{owner}` when `gh api repos/{owner}/{repo} --jq .owner.type` is `Organization`.
- **Example values.**  Substitute the real ones:
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

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

When the request depends on the discussion, fetch every comment from the repository checkout using the supplied repository and issue number.

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/<issue-number>/comments'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/874/comments'
```

##### 3. Return the Issue Read

Read each requested response and its exit code; return the issue record and any requested comments, or the failed read as missing evidence. When no discussion was requested, return the issue record alone.

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

For a new issue, run this creation command from the repository checkout using the supplied title, existing labels and complete body file as [Bodies](#conventions) states.

Repeat `-f 'labels[]=<label>'` for each supplied label.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues' -f title='<title>' -F 'body=@<body-file>' -f 'labels[]=<label>' --jq .number
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues' -f title='<title>' -F body=@body.md -f 'labels[]=<label>' --jq .number
```

##### 4. Update the Existing Issue

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

For an existing issue, run each command whose field is being changed, preserving all other fields. After each selected command, read its exit code and output; stop and return any failure before another mutation. If no field changes, continue with the supplied issue identity.

When changing the issue body, run this update from the repository checkout using its repository, number and complete body file as [Bodies](#conventions) states.

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

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Apply [Comment on Issue](#comment-on-issue) for an answer or a preserved body the caller requires, with the issue number and comment file.

##### 6. Re-Read the Saved Issue

As [Write confirmation](#conventions) states, read the saved issue.

From the repository checkout, save the current issue using its repository, number and supplied destination JSON file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' > '<issue-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' > issue-943.json
```

##### 7. Compare the Saved Issue Fields

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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

From `<workspace>`, run the closure gate with the fresh issue JSON, complete Development snapshot and linked pull request records as `--issue`, `--development` and `--prs`.

- `--issue`, `--development`, and `--prs` are the fresh issue JSON, Development snapshot, and linked pull request records.
- Exit 0 means the closure gate passes; normal delivery checks must also pass. Exit 1 reports blockers. The command performs no network calls or writes.

Runs as [Helper invocation](#conventions) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue '<issue-json-file>' --development '<development-snapshot-file>' --prs '<linked-pull-request-records-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue issue-943.json --development development-943.json --prs development-prs-943.json
```

##### 4. Require the Closure Gate

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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

For a longer comment, post the complete supplied file from the repository checkout using the repository and issue number, as [Bodies](#conventions) states.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -F 'body=@<comment-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/874/comments' -F body=@comment-874.md --jq .html_url
```

##### 3. Return the Comment URL

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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

From `<workspace>`, run the closure gate with the current issue JSON, complete Development snapshot and linked pull request records. Use absolute evidence paths when changing directory.

- `--issue`, `--development`, and `--prs` are the fresh issue JSON, Development snapshot, and linked pull request records.
- Exit 0 means the closure gate passes; normal delivery checks must also pass. Exit 1 reports blockers. The command performs no network calls or writes.

Runs as [Helper invocation](#conventions) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue '<issue-json-file>' --development '<development-snapshot-file>' --prs '<linked-pull-request-records-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue issue-943.json --development development-943.json --prs development-prs-943.json
```

##### 4. Require the Completion Gate to Pass

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the saved state or failure.

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

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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

An issue's title, body and labels. The title meets [Titles](#titles-1), the body is a [body file](#body-file), and each label is a [repository label](#label-identity). The saved title, body and labels equal the supplied values.

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

#### Review Feedback

The reviewer's login and each point they raised in an issue's discussion.

#### Auto-Close Setting

GitHub's **Auto-close issues with merged linked pull requests** repository setting, which must be disabled before a delivery pull request is linked or merged, so that closure follows the criteria rather than the merge.

- The setting is confirmed per repository and holds for the session; it is not inferred from an issue that stayed open.
- No REST field and no GraphQL field of `gh` 2.46 carries it, so on such a host the user's explicit answer is the only source.
- An enabled setting closes issues on merge whatever their criteria. Where it cannot be disabled, each affected issue's state is read after every merge and reopened where its criteria are unmet.

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

#### Task Scope

The work one task delivers within its epic: its problem, design and acceptance criteria, as the [Template](#template) sections hold them.

#### Task Delivery Result

One task's delivery as recorded: the body with its delivering pull request and verified criteria ticked, a comment file reading `Delivered by #<pull-request-number>.`, and the eligibility findings stating whether the task is closable.

## Issue Body

### Operations

#### Write Issue Table

The shared table, before a kind fills its cells.

**Inputs:** [Current body](#body-file), [Kind conditions](#kind-conditions), [Row data](#tables)

**Outputs:** [Issue body](#body-file)

##### 1. Populate the Shared Table Cells

Populate the shared Done, Coverage and Depends on cells from the supplied row data.

- The columns must match the kind's table.
- The shared cells must meet [Tables](#tables).

##### 2. Read the Finished Issue Table

Read the finished table against [Tables](#tables), [Numbering](#numbering), and [Reference form](#reference-form). A Depends on cell that holds prose fails [Tables](#tables). Numbering that does not follow start order is advisory, as [Numbering](#numbering) states.

#### Validate Issue Body

One body checked against its supplied kind and template.

**Inputs:** [Issue record](#issue-record), [Kind conditions](#kind-conditions), [Related context](#related-context), [Output body path](#body-file)

**Outputs:** [Corrected body](#body-file), [Format findings](#format-findings), [Field findings](#field-findings)

##### 1. Run the Body Format Check

From `<workspace>`, check the supplied issue JSON with its kind’s additional format inputs and the output body file as `--fix`.

- The format reader takes the template fence from the body artifact and its table columns where present. A body with a Work Breakdown table requires coverage for every criterion.
- The input is one issue JSON. `--fix` names the output body file for mechanical fixes. Further inputs are specified by the calling body procedure.

Runs as [Helper invocation](#conventions) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/format.py '<issue-json-file>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/format.py issue.json --fix fixed.md
```

##### 2. Review the Body Field Conditions

Read the format checker’s exit code, findings and corrected body. Return an unreadable input or invocation failure as a blocker; retain format findings for the review.

Review the body against the supplied field conditions.

##### 3. Return the Body Validation Findings

Return the [Format Findings](#format-findings), mechanical diff and field findings, including missing sections, extra sections, wrong-kind layout, historical narration and criteria that fail their named instrument. A mechanical correction preserves wording; new content and scope decisions require caller-supplied resolutions.

#### Apply Body Corrections

One body rewritten from confirmed local findings.

**Inputs:** [Current body](#body-file), [Kind conditions](#kind-conditions), [Related context](#related-context), [Confirmed resolutions](#body-resolutions), [Output body path](#body-file)

**Outputs:** [Corrected body](#body-file), [Format findings](#format-findings), [Field findings](#field-findings), [Required changes](#required-changes)

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

**Inputs:** [Issues](#issue-record), [Kind conditions](#kind-conditions), [Related context](#related-context), [Output body paths](#body-file)

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

Apply [Read Tracker Issue](#read-tracker-issue) for each saved issue, as [Write confirmation](#conventions) states.

- Repeat the kind's validator with the saved JSON and the same further inputs, context and output path.
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

#### Body File

One issue body as a local markdown file at a given path, in its kind's template section order and table columns.

#### Kind Conditions

One body kind's template, with its table columns, its field conditions, and any further inputs its format check takes, as that kind's body file defines them.

#### Related Context

The current records a body refers to or depends on: its parent and sibling issues, linked delivery and cited sources.

#### Body Snapshot

A local [issue record](#issue-record) built from a body file, title and labels, saved as JSON at a given path. It carries the existing issue's identity and state, or `number: null` and `state: "open"` for an unpublished draft. Labels are strings or objects with a name.

#### Field Findings

Each place a body departs from its kind conditions or [Fields](#fields-2): a missing or extra section, a wrong-kind layout, historical narration, or a criterion failing its named instrument, with the section it concerns.

#### Body Resolutions

The decision taken on each non-mechanical finding or open question: content to add, an extra section kept, folded or removed, a criterion change, or an answer, each tied to the finding or question it settles.

#### Required Changes

Changes a body correction needs outside that body: a tracker-kind change, a title or label change, or an edit to another issue's body, each naming the issue it applies to.

## Initiative Issue Body

### Operations

#### Validate Initiative Body

The body's local format and field findings.

**Inputs:** [Initiative issue](#issue-record), [Epic issues](#issue-record), [Source evidence](#source-evidence), [Output body file](#body-file-1)

**Outputs:** [Initiative body](#body-file-1), [Validation findings](#format-findings)

##### 1. Validate the Initiative Issue Body

Apply [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#fields-3), supplied related evidence and output file, supplying each linked epic as `--epic`.

##### 2. Title the Initiative Row

Use its current title for the initiative row.

##### 3. Report Excluded Names and Departures

Include excluded names in Problem and Proposal and criterion/source departures in the findings.

##### 4. Return the Validated Initiative Body

Return the corrected body, mechanical diff and unresolved findings for the caller.

### Fields

#### Body File

A local Markdown file at a given path holding one initiative body that meets [Template](#template-1).

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

#### Populate Epic Issue Body

One epic body and its local validation findings.

**Inputs:** [Initiative issue](#issue-record), [Epic scope](#epic-scope), [Pull request records](#pull-request-records), [Corpus branch](#branches), [Output body file](#body-file-2)

**Outputs:** [Epic body](#body-file-2), [Draft rows](#work-breakdown-1), [Validation findings](#format-findings), [Unresolved links](#temporary-links)

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

Runs as [Helper invocation](#conventions) states.

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

Read the helper’s exit code, output and any written body; return an invocation failure as a blocker and retain reported findings or refused criteria. Publish only a successfully written body.

Return the updated body and [Delivery Findings](#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.

#### Record Epic Criteria

Verified criteria and completed rows in one epic body.

**Inputs:** [Epic issue](#issue-record), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Verified criteria](#acceptance-criteria-1), [Output body file](#body-file-2)

**Outputs:** [Epic body](#body-file-2), [Refused criteria](#unverified-criteria)

##### 1. Run Tick Epic Criteria

From `<workspace>`, update the epic JSON with records as `--prs`, snapshot as `--links`, verified criterion ids as `--tick` and output body file as `--fix`. Refuse criteria not ready to verify.

`<criterion-ids>` is a comma-separated list of verified criterion ids.

Runs as [Helper invocation](#conventions) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --tick '<criterion-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json --tick AC1,AC3 --fix fixed-943.md
```

##### 2. Return the Epic Body and Refused Criteria

Read the helper’s exit code, output and any written body; return an invocation failure as a blocker and retain reported findings or refused criteria. Publish only a successfully written body.

Return the body and refused criteria. Complete rows receive Done ticks.

#### Reserve Task Rows

Task rows held for one confirmed delivery session.

**Inputs:** [Epic issue](#issue-record), [Task ids](#task-delivery), [Planning folder](#layout), [Records base URL](#engineering-branch), [Record date](#header), [Output body file](#body-file-2)

**Outputs:** [Epic body](#body-file-2)

##### 1. Check the Rows to Reserve

Require the caller's confirmed unit and existing planning folder. Refuse a row already held or linked to a pull request or commit.

##### 2. Run Reserve Row

From `<workspace>`, reserve the confirmed task ids using the epic as `--epic`, ids as `--reserve`, supplied records base URL as `--records`, record date as `--date` and output body file as `--fix`.

- `--records` is the URL of the planning records folder, needed when no row id in the epic links a record.
- The caller supplies the planned folder identity; `--date` is the day it is opened.

`<task-ids>` is a comma-separated list of task ids; `<records-base-url>` is the URL of the [records folder](#engineering-branch) on the engineering branch.

Runs as [Helper invocation](#conventions) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic '<epic-json-file>' --reserve '<task-ids>' --records '<records-base-url>' --date '<record-date>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic issue-943.json --reserve W01,W02 --records 'https://github.com/<owner>/<repo>/tree/engineering/artifacts/planning' --fix fixed-943.md
```

##### 3. Return the Reserved Epic Body

Read the helper’s exit code, output and any written body; return an invocation failure as a blocker and retain reported findings or refused criteria. Publish only a successfully written body.

Return the body with the folder as each row's single link, meeting [Task Delivery](#task-delivery).

#### Release Task Rows

Held task rows returned to their work-item links.

**Inputs:** [Epic issue](#issue-record), [Task ids](#task-delivery), [Release decision](#release-decision), [Output body file](#body-file-2)

**Outputs:** [Saved epic issue](#issue-record)

##### 1. Check the Rows to Release

Require the user's explicit decision releasing the hold, and refuse any row that is not held.

##### 2. Run Release Row

From `<workspace>`, release the authorized held task ids using the epic as `--epic`, ids as `--release` and output body file as `--fix`.

- The file is the task id in lowercase within that folder, as [Task ids](#task-delivery) defines.

`<task-ids>` is a comma-separated list of task ids.

Runs as [Helper invocation](#conventions) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic '<epic-json-file>' --release '<task-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic issue-943.json --release W01 --fix fixed-943.md
```

##### 3. Publish the Released Epic Body

Read the helper’s exit code, output and any written body; return an invocation failure as a blocker and retain reported findings or refused criteria. Publish only a successfully written body.

Publish the returned body through [Save Tracker Issue](#save-tracker-issue).

##### 4. Return the Saved Released Body

Return the saved body with each task id linked to its lowercase work-item file inside the reserved folder, meeting [Task Delivery](#task-delivery).

#### Validate Epic Body

The body's local format and field findings.

**Inputs:** [Epic issue](#issue-record), [Initiative issue](#issue-record), [Pull request records](#pull-request-records), [Corpus branch](#branches), [Output body file](#body-file-2)

**Outputs:** [Epic body](#body-file-2), [Validation findings](#format-findings)

##### 1. Validate the Epic Issue Body

Apply [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#fields-4), supplied related evidence and output file, supplying initiative JSON as `--initiative`, current pull request records as `--prs` and corpus branch as `--corpus`.

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

#### Plan Gap Task

The agreed disposition of criteria a delivered row left unmet.

**Inputs:** [Epic issue](#issue-record), [Delivered task row](#work-breakdown-1), [Unmet criteria](#acceptance-criteria-1), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Output body file](#body-file-2)

**Outputs:** [Saved epic issue](#issue-record), [Gap disposition](#gap-disposition)

##### 1. Present Unmet Epic Criteria

Present each unmet criterion and its missing evidence, read from the current epic issue, to the user.

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

#### Body File

A local Markdown file at a given path holding one epic body that meets [Template](#template-2).

#### Epic Scope

The work one epic takes: its slice of the initiative's design, its title and labels meeting [Titles](#titles-3), its [acceptance criteria](#acceptance-criteria-1), and its proposed task rows meeting [Work Breakdown](#work-breakdown-1).

#### Release Decision

The user's explicit decision to release the hold on named task rows, naming each task id it releases.

#### Gap Disposition

Each criterion a delivered row left unmet, with its missing evidence and one disposition:

- **Holds.** The user confirms it already holds; the delivered task retains it, awaiting verification and ticking.
- **Further task.** A further task row adopts it, meeting [Task grain](#work-breakdown-1).
- **Pending.** The decision or the further task's draft is unanswered.

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

## Delivery Evidence

### Operations

#### Read Board Delivery Evidence

The board snapshot and pull request records that establish current delivery across one board.

**Inputs:** [Board](#board-identity), [Board files](#board-files), [Records path](#pull-request-records), [Link snapshot path](#issue-link-snapshot)

**Outputs:** [Board snapshot](#board-snapshot), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot)

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

The board items with their Status, the Status field, the board fields, the board's [repositories](#repositories) and the assignee login, read together with the board's pull request records and issue-link snapshot. Each is a local file at its path.

#### Unnamed Deliveries

A pull request whose issue links reach an epic or its task issues while its title omits that epic's reference. Each is named with the epic it reaches, for the user to confirm.

#### Named Delivery

A pull request that delivers an epic carries that epic's reference in its title, as `[I07:E00] Purpose`. A delivery the user confirms whose title omits its epic is repaired to carry that reference.

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

Read the same pull request's actual Development field through authenticated GitHub or an available supported tool, as [Write confirmation](#conventions) states.

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

Repeat that read after a link changes, as [Write confirmation](#conventions) states.

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

#### Fetch All Initiative Pull Requests

The pull request collection covering every supplied board repository.

**Inputs:** [Repositories](#repositories), [Records path](#pull-request-records)

**Outputs:** [Pull request records](#pull-request-records)

##### 1. Fetch the First Repository Pull Requests

From the first repository’s checkout, fetch all initiative-prefixed pull requests to the supplied JSON-lines file, such as `prs.json`. This replaces the destination with a fresh collection.

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' > '<pull-request-records-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' > prs.json
```

##### 2. Stop on a First Fetch Failure

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Stop on failure.

##### 3. Append Further Repository Pull Requests

From each further repository’s checkout, append its initiative-prefixed pull requests to the same destination file. Read each fetch result before continuing; return incomplete evidence on any failure.

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' >> '<pull-request-records-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' >> prs.json
```

##### 4. Return Incomplete Pull Request Evidence

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

If any fetch failed, return incomplete evidence.

##### 5. Return the Complete Pull Request Collection

Return the complete collection only after every fetch succeeds.

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

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Run each requested supporting-record command. After each read, inspect its exit code and output; return a failure before the next read, keeping missing evidence explicit.

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

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the snapshots or missing evidence.

#### Publish Pull Request

One pull request created or updated from supplied content and metadata.

**Inputs:** [Pull request](#pull-request-identity), [Kind](#pull-request-kind), [Pull request content](#pull-request-content), [Delivery issue](#issue-record), [Auto-close setting](#auto-close-setting), [Link snapshot path](#issue-link-snapshot)

**Outputs:** [Pull request snapshot](#pull-request-snapshot), [Issue-link snapshot](#issue-link-snapshot)

##### 1. Open a New Pull Request

For creation, select exactly one command for the supplied kind, body, title, head and base, preserving epic and discussion draft state. For an existing pull request, continue at [3. Update the Existing Pull Request](#3-update-the-existing-pull-request).

For task creation, run this command from the repository checkout using the supplied title, task branch, epic base and complete body file as [Bodies](#conventions) states.

- Supply the epic prefix and purpose as title, the task branch as head, the epic base as base, and the complete body file.

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='<title>' -f head='<task-branch>' -f base='<epic-base>' -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='[I07:E00] Purpose' -f head='i07/e00/w01-purpose' -f base='i07/e00/main' -F body=@body.md --jq .html_url
```

For epic creation, run this command from the repository checkout using the supplied title, epic base, long-lived target and review body file as [Bodies](#conventions) states.

- Supply the epic prefix and name as title, the epic base as head, its long-lived branch as base, and the populated review body file.
- `draft` is true, including when the work is already complete.

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='<title>' -f head='<epic-base>' -f base='<long-lived-base>' -F draft=true -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='[I07:E00] Name' -f head='i07/e00/main' -f base='main' -F draft=true -F body=@body.md --jq .html_url
```

For discussion creation, run this command from the repository checkout using the supplied title, planning branch, target branch and body file as [Bodies](#conventions) states.

```bash
gh api --method POST 'repos/<owner>/<repository>/pulls' -f title='<title>' -f head='<planning-branch>' -f base='<target-branch>' -F body=@'<body-file>' -F draft=true
```

**Example:**

```bash
gh api --method POST repos/m2ux/workflow-server/pulls -f title='Queue Planning: Scope and Delivery' -f head=planning/queue -f base=engineering -F body=@discussion.md -F draft=true
```

##### 2. Confirm Creation and Link the Delivery Issue

For a creation request, read the command’s exit code and returned identity; return a failure before attempting a link.

- For a task or epic pull request with a delivery issue, require the confirmed auto-close setting and snapshot destination, then apply [Link Pull Request to Issue](#link-pull-request-to-issue) with them, meeting [Issue Links](#issue-links). A row task without its own issue supplies no delivery issue, auto-close setting or link snapshot for publication.
- After a successful creation and any required link, continue at [4. Re-Read the Published Pull Request](#4-re-read-the-published-pull-request).

##### 3. Update the Existing Pull Request

For an existing pull request, run each command for a supplied change, preserving other fields. After each selected command, read its exit code and output; stop and return any failure before another mutation. If no field changes, continue with the supplied pull request identity.

When changing the body, run this update from the repository checkout using the pull request’s repository, number and complete body file as [Bodies](#conventions) states.

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

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Re-read through [Read Pull Request State](#read-pull-request-state), as [Write confirmation](#conventions) states.

##### 5. Return the Published State

Return the saved state or discrepancy, and the issue-link snapshot when the creation path linked a delivery issue. Other publication paths return no issue-link snapshot.

### Fields

#### State

A pull request is open, draft, ready for review, merged or closed without merge. A merged result identifies the verified head, target and merge commit.

- An epic's review pull request is published as a draft when the first task merges into its epic base, and an unmerged epic base with work merged into it has one.
- The review stays draft, and its epic open, until the epic is complete and the user marks it ready.

#### Scope

A task pull request delivers one task, or a set of tasks that name each other in Joins. It targets the epic base for the long-lived branch its work changes.

#### Issue Links

- GitHub shows the link in the pull request's Development field and in the issue's Linked pull requests field, which the project board reads.
- A task pull request links the task's issue, and a review pull request links its epic's issue.
- The link is addressed by issue, so a pull request whose work carries no issue links nothing. A task pull request delivering rows that have no issue of their own is the whole of what stays unlinked.
- The link is stored on the pull request. It holds on any base branch and on a pull request that has merged, and a later body edit leaves it standing.
- A linked issue remains open until its criteria and delivery requirements hold and every Development-linked pull request is merged.
- The field is the whole of the relation: neither body links the other. The pull request's References carry its sources, and the issue it delivers is not among them.
- A pull request with a delivery issue but no Development link is uncited.

#### Pull Request Identity

A pull request's [repository](#repository) and number. A pull request yet to be created has its repository alone.

#### Pull Request Kind

Task, epic or planning discussion. A delivery pull request is a task or an epic one: a task pull request meets [Scope](#scope), and an epic's review pull request has an epic base as its head.

#### Pull Request Content

The fields a publication writes: a body file at its path, meeting [Template](#template-3), its title, head and base. A change to an existing pull request names only the fields it changes.

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

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return a missing-selection result when neither a theme nor proposals is specified; the caller obtains that choice.

##### 3. Return the Selected Board Number

Return the selected board number, or an absent-board result for [Copy Project Board](#copy-project-board). Work one board at a time.

#### Copy Project Board

A missing theme board, or a missing proposals board.

**Inputs:** [Board owner](#board-identity), [Repository](#repository), [Board selection](#board-selection), [Theme title](#one-board-per-theme), [Originating proposal](#issue-record)

**Outputs:** [Copied board](#board-identity)

##### 1. Create an Absent Proposals Board

When no open board carries the [proposals board](#proposals-board) title, apply [Create Proposals Board](#create-proposals-board). The copy source and the title meet [Proposals](#proposals).

##### 2. Create an Absent Theme Board

When the selected theme board is absent:

- Apply [Create Theme Board](#create-theme-board) with the owner, repository, theme title and originating proposal record when applicable.
- Require the new theme's label and board before an initiative takes that theme.

#### Ensure Project Board

The theme or proposals board the request names, created when it is absent.

**Inputs:** [Board owner](#board-identity), [Repository](#repository), [Board selection](#board-selection), [Theme title](#one-board-per-theme), [Originating proposal](#issue-record)

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

**Inputs:** [Board owner](#board-identity), [Repository](#repository)

**Outputs:** [Proposals board](#board-identity)

##### 1. Find the Proposals Template

From the repository checkout, find the template using the owner and proposals board’s [template title](#board-templates).

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "<template-title>") | .number'
```

##### 2. Use the Proposals Template as Source

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Use the returned number as the copy source.

##### 3. Copy the Proposals Template

From the repository checkout, copy the returned template number for the owner, using the configured [proposals title](#proposals-board).

- The copy's JSON is one project; `.number` identifies the new board.

```bash
gh project copy '<template-number>' --source-owner '<owner>' --target-owner '<owner>' --title '<board-title>' --format json --jq .number
```

##### 4. Retain the Proposals Board Number

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Retain the new board number. The copy meets [Proposals](#proposals).

##### 5. Link the Proposals Board to the Repository

From the repository checkout, link the new board using its owner, returned number and supplied repository.

```bash
gh project link '<board-number>' --owner '<owner>' --repo '<repo>'
```

##### 6. Return the Proposals Board Number

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the new board number after linking succeeds.

#### Create Theme Board

A new theme board linked to the supplied repository.

**Inputs:** [Board owner](#board-identity), [Repository](#repository), [Theme title](#one-board-per-theme), [Originating proposal](#issue-record)

**Outputs:** [Theme board](#board-identity)

##### 1. Require the Originating Proposal

Require the originating proposal record for a proposal-derived board; return a missing-input finding when its designator is unavailable.

##### 2. Find the Initiative Template

From the repository checkout, find the template using the owner and theme board’s [template title](#board-templates).

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "<template-title>") | .number'
```

##### 3. Use the Initiative Template as Source

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Use the returned number as the copy source.

##### 4. Copy the Initiative Template

From the repository checkout, copy the returned template number for the owner, using the title required by [One Board Per Theme](#one-board-per-theme).

- The copy's JSON is one project; `.number` identifies the new board.

```bash
gh project copy '<template-number>' --source-owner '<owner>' --target-owner '<owner>' --title '<board-title>' --format json --jq .number
```

##### 5. Retain the Theme Board Number

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Retain the new board number. The copy carries the template's theme board [Status options](#status-field).

##### 6. Link the Theme Board to the Repository

From the repository checkout, link the new board using its owner, returned number and supplied repository.

```bash
gh project link '<board-number>' --owner '<owner>' --repo '<repo>'
```

##### 7. Return the Theme Board Number

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the new board number after linking succeeds.

#### Read Board State

The selected board's items and status fields.

**Inputs:** [Board](#board-identity)

**Outputs:** [Board items](#board-items), [Status field id](#status-field-id), [Repositories](#repositories)

##### 1. Find the Board Status Field

Use the existing board returned by [Select Project Board](#select-project-board) or [Copy Project Board](#copy-project-board), whether the caller ran that operation or carries its result. From the repository checkout, query its owner and number for the configured [Status field](#status-field) name.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/fields?per_page=100" --jq '.[] | select(.name == "<status-field-name>") | .id'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/fields?per_page=100" --jq '.[] | select(.name == "Status") | .id'
```

##### 2. Fetch Board Items with Status

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

From the repository checkout, save the board items using the board owner and number, returned Status field id and destination file.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/items?per_page=100&fields=<status-field-id>" > '<board-items-file>'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/items?per_page=100&fields=419167630" > items.json
```

##### 3. Return the Board State

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the items, Status field, item ids and the board's [Repositories](#repositories) to the caller.

#### Read Board Assignee

The authenticated login available for board assignments.

**Inputs:** None

**Outputs:** [Assignee login](#assignees)

##### 1. Find the Board User

From the repository checkout, read the authenticated login.

```bash
gh api user --jq .login
```

##### 2. Return the Assignee Login

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return its login for the caller's assignment decisions.

#### Read Board Configuration

One board's field definitions and requested item state.

**Inputs:** [Board](#board-identity), [Output paths](#board-files), [Board item](#board-items)

**Outputs:** [Board fields](#board-fields), [Board item](#board-items)

##### 1. Fetch the Configured Board Fields

From the repository checkout, save the supplied board’s fields using its owner, number and destination file.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/fields?per_page=100" > '<board-fields-file>'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/fields?per_page=100" > fields.json
```

##### 2. Fetch the Requested Board Item

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

When a single item is requested for [write confirmation](#conventions), read it from the repository checkout using the board owner and number, item id and Status field id. A list snapshot may lag a write.

```bash
gh api "users/<owner>/projectsV2/<board-number>/items/<item-id>?fields=<status-field-id>"
```

**Example:**

```bash
gh api "users/<owner>/projectsV2/9/items/1001?fields=419167630"
```

##### 3. Return the Board Configuration

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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

The user is the login `gh` runs as. An issue at Ready, In Progress, In Review or Done is assigned to the user; one in Backlog has no assignee. An assignee is set on the issue, not on the board item, so the call that changes one acts on the issue.

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

#### Board Fields

A board's field definitions as JSON: each field's id and name, and the [Status field](#status-field)'s id with its option ids.

#### Status Field Id

The numeric identifier of the board's [Status field](#status-field).

#### Board Items

A board's items as JSON, each with its item id, its Status and its issue whole. A single board item is one such entry.

#### Board Files

The local paths a board read writes its JSON into: an issue file, a board fields file and a board item file.

## Board Delivery

### Operations

#### Plan Board Changes

The board changes implied by supplied delivery state.

**Inputs:** [Initiative](#issue-record), [Epics](#issue-record), [Tasks](#issue-record), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot), [Board](#board-identity), [Board fields](#board-fields), [Board items](#board-items), [Output directory](#change-calls), [Assignee login](#assignees), [Off-board issues](#issue-record)

**Outputs:** [Change calls](#change-calls), [Missing evidence](#missing-evidence)

##### 1. Require the Board Change Link Snapshot

Require the complete pull-request issue-link snapshot; refuse the computation without it.

##### 2. Compute the Board Changes

From `<workspace>`, compute board changes using the supplied initiative, epic and task records, pull request and complete link snapshots, board identity, fields and items, output directory, assignee and resolved off-board issues.

- `--epics`, `--tasks`, `--prs` and `--links` receive the related records and complete link snapshot.
- `--board`, `--fields` and `--items` identify the current board state.
- `--out` receives the call files; `--assignee` is the supplied login.
- `--others` supplies each resolved dependency issue.

Pass each epic or task JSON file as a separate argument after its corresponding flag.

Omit `--others` when there are no resolved off-board issues; otherwise pass every resolved file after it.

Runs as [Helper invocation](#conventions) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/board.py '<initiative-json-file>' --epics '<epic-json-file>' --tasks '<task-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --board '<board-identity>' --fields '<board-fields-file>' --items '<board-items-file>' --out '<output-directory>' --assignee '<assignee-login>' --others '<off-board-issue-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/board.py issue-936.json --epics issue-943.json issue-937.json --tasks issue-637.json --prs prs.json --links links.json --board 'users/<owner>/projectsV2/9' --fields fields.json --items items.json --out board/ --assignee m2ux
```

##### 3. Return the Planned Board Calls

Read the helper’s exit code and output. Preserve unresolved references as missing evidence; return any other execution error without applying calls.

Return the generated calls and unresolved references, meeting [Fields](#fields-9). The caller gathers missing evidence, applies changes and confirms them as [Write confirmation](#conventions) states.

#### Record Board Delivery

The board's status and assignees after its issues record delivery.

**Inputs:** [Initiative](#issue-record), [Epics](#issue-record), [Tasks](#issue-record), [Board](#board-identity), [Output directory](#change-calls)

**Outputs:** [Board items](#board-items), [Assignees](#assignees)

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

- Apply [Read Board Configuration](#read-board-configuration) with the board identity, output paths and changed item identity to confirm its current status, as [Write confirmation](#conventions) states.
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

The result contains calls for issues to add, items to remove, Status to set and assignees to add or remove. Each call names its affected issue and board item, and the call files occupy one output directory. Assignees follow [Assignees](#assignees).

#### Missing Evidence

Unresolved issue references identify dependency records the caller must supply before a complete result. A newly added issue receives its status on a subsequent pass using refreshed items.

## Architecture Overview

### Fields

#### Ownership

One overview explains one pull request, and a reviewer meets it on that pull request. The run that integrates an epic base owns that epic's overview. Any other run writes an overview only for a task or epic entering review that no integration explained. An overview already written is kept: the pull request it explains is the one already reviewed. An initiative has no overview of its own.

## Repository Labels

### Operations

#### Ensure Repository Labels

The required label definitions available for issue publication.

**Inputs:** [Repository](#repository), [Required labels](#label-identity)

**Outputs:** [Available labels](#label-identity)

##### 1. List the Repository Labels

From the repository checkout, list its labels using the supplied owner and repository.

```bash
gh api "repos/<owner>/<repo>/labels?per_page=100" --jq '.[].name'
```

##### 2. Compare Required Label Names

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Compare the returned labels with the supplied required names.

##### 3. Create Absent Required Labels

From the repository checkout, create each absent required label using its supplied name, colour and description. Read each creation’s exit code and output before the next label; return a failure immediately.

```bash
gh api --method POST 'repos/<owner>/<repo>/labels' -f name='<label>' -f color='<hex-colour>' -f description='<description>' --jq .name
```

##### 4. Return the Available Labels

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the observed existing labels and successful creations. When every required label already exists, return that observed set. An unknown definition is a finding for the caller to resolve before publication.

### Fields

#### Repository

One repository, written `<owner>/<repo>`.

#### Label Identity

Each label has a name, colour and description. Issue assignments use labels that exist in the repository.

## Acceptance Criteria

### Fields

#### Verification Evidence

One criterion's instrument result, passing or failing, with the issue that states the criterion and the revision it was taken on. Within one run, evidence stands for its criterion on its revision: the criterion's instrument runs at most once on each revision, and a later verification on that revision keeps the earlier evidence.

#### Unverified Criteria

Each criterion left unticked, refused as not ready to verify or unverified, with what it is missing.

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

Runs as [Helper invocation](#conventions) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py --names --project '<checkout>'
```

##### 2. Read the Epic Base Names

Read the helper’s exit code and output. Preserve a missing or empty configuration as unevaluable evidence; return any other execution error.

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

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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

## Epic

### Operations

#### Inspect Epic Delivery

The delivery findings for one epic from supplied evidence.

**Inputs:** [Epic issue](#issue-record), [Pull request records](#pull-request-records), [Issue-link snapshot](#issue-link-snapshot)

**Outputs:** [Delivery findings](#delivery-findings)

##### 1. Match Epic Pull Requests

From `<workspace>`, inspect the epic JSON using the supplied pull request records as `--prs` and complete link snapshot as `--links`.

- Results follow [Delivery Findings](#delivery-findings).

Runs as [Helper invocation](#conventions) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json
```

##### 2. Return the Inspected Delivery Findings

Read the helper’s exit code and output; return execution failures as blockers and retain delivery findings as evidence.

Return the [Delivery Findings](#delivery-findings); missing linked pull requests are missing evidence for the caller to supply.

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

## Planning Record

### Fields

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

## Dependency Graph

### Fields

#### Numbering Map

A comma-separated list of `<old-number>:<new-number>` pairs assigning each old number one distinct new number. A number a pull request already names is preserved, and a row a pull request names is not renumbered. A source absent from the supplied files, or a duplicate destination, is refused.

## Pull Request Body

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
