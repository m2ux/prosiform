---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Issue

A tracker issue: its identity, saved body, metadata, discussion and closure state. The caller supplies the populated body and the delivery decision.

## Operations

### Read Tracker Issue

The current issue, its saved body and discussion.

**Inputs:** [Issue identity](#issue-identity), [Record path](#issue-record)

**Outputs:** [Issue record](#issue-record), [Issue comments](#issue-comment)

#### 1. Fetch the Tracker Issue

Run [Fetch Tracker Issue](#fetch-tracker-issue) for the complete JSON, or [Fetch Issue Body](#fetch-issue-body) for its body, with the issue number and destination file.

#### 2. Fetch the Issue Comments

Run [Fetch Issue Comments](#fetch-issue-comments) when the request depends on the discussion.

### Save Tracker Issue

One populated body and its metadata, written to the tracker.

**Inputs:** [Issue identity](#issue-identity), [Issue content](#issue-content), [Label definitions](repository-labels.md#label-identity), [Comment](#issue-comment)

**Outputs:** [Saved issue](#issue-record)

#### 1. Take the Issue Body and Metadata

Take the supplied body and metadata, preserving each field the caller does not change for an existing issue.

#### 2. Ensure the Issue Labels

Apply [Ensure Repository Labels](repository-labels.md#ensure-repository-labels) with every label the save assigns and its colour and description.
- Return an unknown label definition to the caller before any write.

#### 3. Create New Issue

For a new issue, run [Create Tracker Issue](#create-tracker-issue) with the body's file, title and labels.

#### 4. Update the Existing Issue

For an existing issue, run [Patch Issue Body](#patch-issue-body), [Retitle Tracker Issue](#retitle-tracker-issue), [Add Issue Labels](#add-issue-labels) or [Remove Issue Label](#remove-issue-label) for the fields being changed.

#### 5. Comment on the Saved Issue

Apply [Comment on Issue](#comment-on-issue) for an answer or a preserved body the caller requires, with the issue number and comment file.

#### 6. Re-Read the Saved Issue

Re-read with [Fetch Tracker Issue](#fetch-tracker-issue), as [Write confirmation](../conventions.md) states.

#### 7. Compare the Saved Issue Fields

Compare the saved fields with the intended body and metadata.

### Check Issue Completion

The normal delivery result of one task, epic or initiative before tracker closure.

**Inputs:** [Issue record](#issue-record), [Development snapshot](#development-snapshot), [Linked pull request records](#linked-pull-request-records), [Verification evidence](acceptance-criteria.md#verification-evidence), [Task delivery result](task-body.md#task-delivery-result), [Project checkout](delivery-branches.md#project-checkout)

**Outputs:** [Completion result](#completion-result)

#### 1. Select the Completion Check

Select the check by the issue's kind:
- **Task.**
  - Retain the task delivery result its delivering pull request established.
- **Epic.**
  - Apply [Read Delivery Branches](delivery-branches.md#read-delivery-branches) with the project checkout and epic identity for the complete expected bases.
  - Apply [Read Pull Request State](pull-request.md#read-pull-request-state) for each base's merge evidence.
  - Apply [Check Epic Completion](epic.md#check-epic-completion) with the current epic JSON, linked pull request records, complete issue-link snapshot, criterion verification evidence and those base records.
- **Initiative.**
  - Apply [Read Tracker Issue](#read-tracker-issue) for every linked epic.
  - Apply [Check Initiative Completion](initiative.md#check-initiative-completion) with the current initiative JSON, all linked epic records, criterion verification evidence and the Development snapshot and linked pull request records.

#### 2. Return the Completion Result

Return the completion result; an incomplete or failed result is a blocker to closure.

### Close Tracker Issue

Verified completion of an issue and its linked delivery.

**Inputs:** [Issue identity](#issue-identity), [Completion result](#completion-result), [Issue record](#issue-record), [Development snapshot](#development-snapshot), [Auto-close setting](#auto-close-setting), [Linked pull request records](#linked-pull-request-records)

**Outputs:** [Closed issue](#issue-state)

#### 1. Capture the Issue Development

Apply [Capture Issue Development](#capture-issue-development) for the issue's complete links and confirmed repository setting.

#### 2. Take Fresh Pull Request Records

Take the caller's fresh records for every linked pull request, across repositories and states; return missing evidence to the caller.
- Return a repository setting that is unconfirmed or fails [Auto-Close Setting](#auto-close-setting) to the caller as a blocker.
- Take the records only from a fresh destination file, so an earlier snapshot cannot supply membership.
- Use the issue's entire Development field to establish membership. Titles, branch names, body mentions and a list filtered to one initiative do not establish completeness. An explicitly empty field adds no pull request requirement.

#### 3. Run the Closure Check

Run [Check Issue Closure](#check-issue-closure) with `--issue`, `--development`, and `--prs` for those fresh records.

#### 4. Require the Closure Gate

Require the supplied completion result to be complete, normal delivery checks to pass, every criterion to be verified and ticked, and every currently linked pull request to be merged.
- Keep the issue open for an open, draft, closed without merge, or unreadable linked pull request.
- Obtain the user's decision before removing an abandoned or incorrect Development link. A replacement pull request does not remove the requirement on a link still present.

#### 5. Close the Issue as Completed

Apply [Close as Completed](#close-as-completed), which repeats the gate immediately before the write. A changed link set requires another capture and check.

### Close Transferred Work

An issue whose work is tracked by another issue.

**Inputs:** [Issue identity](#issue-identity), [Transfer destination](#transfer-destination), [Comment](#issue-comment)

**Outputs:** [Closed issue](#issue-state)

#### 1. Confirm the Transfer Destination

Confirm the supplied destination contains the work and cites its source issue.

#### 2. Comment with the Destination

Apply [Comment on Issue](#comment-on-issue) with the destination reference and supplied comment file.

#### 3. Close the Issue as Not Planned

Run [Close as Not Planned](#close-as-not-planned), retaining the issue's body.

#### 4. Re-Read the Transferred Issue

Re-read it with [Fetch Tracker Issue](#fetch-tracker-issue) for its state and reason, as [Write confirmation](../conventions.md) states.

### Comment on Issue

The supplied discussion text saved on one issue.

**Inputs:** [Issue identity](#issue-identity), [Comment](#issue-comment), [Review feedback](#review-feedback)

**Outputs:** [Saved comment](#issue-comment)

#### 1. Compose the Feedback Reply

When replying to feedback already folded into the body, compose a precise, factual reply addressing each point and mentioning the reviewer, with no thanks or filler. Name what the body now says, by criterion id where one carries it, or the issue that takes the point.

#### 2. Publish the Issue Comment

Publish the supplied comment:
- For a one-line comment, run [Post Inline Comment](#post-inline-comment) with the exact text.
- For a longer comment, run [Post Comment File](#post-comment-file) with the complete file.

#### 3. Return the Comment URL

Return the saved comment URL.

### Close as Completed

An issue closed after its final evidence check.

**Inputs:** [Issue identity](#issue-identity), [Auto-close setting](#auto-close-setting), [Completion result](#completion-result), [Issue record](#issue-record), [Development snapshot](#development-snapshot), [Linked pull request records](#linked-pull-request-records)

**Outputs:** [Completed issue](#issue-state)

#### 1. Capture Development Before Closure

Require absolute paths for the issue, Development and linked pull request evidence files.
Apply [Capture Issue Development](#capture-issue-development) immediately before closure with the issue identity, authenticated access, confirmed repository setting and evidence paths.

#### 2. Compare the Development Links

Compare its links with the supplied fresh pull request records; return a changed link set or missing evidence to the caller for refresh.

#### 3. Run the Completion Gate

Run [Check Issue Closure](#check-issue-closure) with the current issue, Development and linked pull request files, using absolute evidence paths when changing directory.

#### 4. Require the Completion Gate to Pass

Require exit 0 and passing normal delivery checks; a sync report of closable does not permit skipping this gate.

#### 5. Set the Completed State

Immediately after the gate passes, run [Set Completed State](#set-completed-state) with the issue's repository and number and the passing evidence.

#### 6. Return the Completed State

Return the saved state or failure.

### Capture Issue Development

The issue's current content and complete Development snapshot.

**Inputs:** [Issue identity](#issue-identity), [Auto-close setting](#auto-close-setting), [Record path](#issue-record), [Snapshot path](#development-snapshot)

**Outputs:** [Development snapshot](#development-snapshot), [Issue record](#issue-record)

#### 1. Read the Development Field

Apply [Read Issue Development](#read-issue-development) for the entire field across repositories and states. An inaccessible field returns incomplete evidence; an empty array means the field was checked and empty.

#### 2. Write the Development Snapshot

Run [Write Development Snapshot](#write-development-snapshot) with the issue identity, observed link set, completeness result and repository setting, saving `development-943.json` or the supplied path.
- Set `complete` true only after the full read, and `auto_close_issues` false only after the repository setting is confirmed disabled.

#### 3. Fetch the Issue Snapshot

Run [Fetch Tracker Issue](#fetch-tracker-issue) into `issue-943.json` or the supplied path.

#### 4. Return the Development Files

Return both files and any incomplete evidence. The caller supplies fresh linked pull request records in `development-prs-943.json`.

### Read Issue Development

The Development links observed for one issue through authenticated GitHub.

**Inputs:** [Issue identity](#issue-identity)

**Outputs:** [Observed links](#observed-development-links)

#### 1. Read Every Development Link

Read every page and state, across repositories, recording each linked pull request's identity.

#### 2. Return the Observed Development Links

Return the observed links and whether the entire field was readable.

### Confirm Repository Auto-Close

Whether the repository auto-closes issues whose linked pull requests merge, established for this session.

**Inputs:** [Repository](#tracker-repository)

**Outputs:** [Auto-close setting](#auto-close-setting)

#### 1. Read the Auto-Close Setting

Read the setting where the authenticated API exposes it, and take a read value as the answer.

#### 2. Ask the User for Auto-Close

Where no API field carries it, put the setting to the user and take their explicit answer, meeting [Auto-Close Setting](#auto-close-setting).

#### 3. Return the Confirmed Auto-Close Setting

Return the confirmed value. An unconfirmed setting is a blocker, and an enabled one leaves the caller to obtain authorization before the repository is reconfigured.

### Read Repository Issues

The issue collection used for repository-wide selection.

**Inputs:** [Repository](#tracker-repository), [Issues path](#repository-issues)

**Outputs:** [Repository issues](#repository-issues)

#### 1. Fetch All Repository Issues

Run [Fetch All Issues](#fetch-all-issues), saving the complete collection.

#### 2. Return the Repository Issues

Return it with pull requests distinguishable from issues.

### Locate Initiative Issue

The tracker identity matching one initiative prefix.

**Inputs:** [Repository](#tracker-repository), [Initiative prefix](#tracker-prefix)

**Outputs:** [Initiative issue](#issue-identity)

#### 1. Find the Initiative Issue

Run [Find Initiative Issue](#find-initiative-issue) with the supplied repository and prefix.

#### 2. Return the Initiative Issue Number

Return its issue number or an unresolved identity.

### Select Tracker Number

The next unused number for one prefixed issue kind in the repository.

**Inputs:** [Repository](#tracker-repository), [Prefix letter](#tracker-prefix)

**Outputs:** [Tracker number](#tracker-prefix)

#### 1. List the Prefixed Titles

Run [List Prefixed Titles](#list-prefixed-titles) for the supplied repository and prefix letter, covering all issue states.

#### 2. Read the Highest Prefix

Read the highest prefix carrying that letter.

#### 3. Confirm the Next Number Is Unused

Confirm the following number, or `00` when there is no prefix, remains unused before creation.

#### 4. Return the Tracker Number

Return the confirmed number.

## Fields

### Observed Development Links

Every linked pull request URL in an issue's Development field, across repositories and states, and whether the entire field was readable.


### Tracker Repository

The repository whose tracker holds the issues: its owner and name, written `<owner>/<repo>`.

### Issue Identity

One issue's [repository](#tracker-repository), number and URL. An issue yet to be created has its repository alone. An unresolved identity names the repository and the title prefix that matched no issue.

### Issue Content

An issue's title, body and labels. The title meets [Titles](issue-body.md#titles), the body is a [body file](issue-body.md#body-file), and each label is a [repository label](repository-labels.md#label-identity). The saved title, body and labels equal the supplied values.

### Issue Record

One issue as the tracker returns it, saved as JSON at a local path: its [identity](#issue-identity), [content](#issue-content), [state](#issue-state) and kind, which its [tracker prefix](#tracker-prefix) and [kind label](../configuration.md#kind-labels) give. A body-only record is the issue's body alone, saved as markdown.

### Issue Comment

One comment on an issue: its exact text, as one line or a complete local file, and once saved its URL. An issue's discussion is its comments in order. A saved comment preserves the supplied text.

### Issue State

The issue is open, or closed with its reason: completed or not planned. Completed work satisfies its criteria and delivery checks; transferred work, closed as not planned, identifies the issue tracking it.

### Tracker Prefix

The bracketed prefix a planned issue's title opens with: for each level, its kind's prefix letter and a two-digit number, levels separated by colons, as `[I07]`, `[I07:E00]` and `[I07:E00:W01]`. A tracker number is the two-digit number of one level.

### Repository Issues

Every issue in one [repository](#tracker-repository), in all states, saved as one JSON file of [issue records](#issue-record). Pull requests among the entries carry a `pull_request` field that distinguishes them from issues.

### Development Snapshot

One issue's Development field as observed, saved as JSON at a local path: the issue's repository and number, whether the whole field was read, the repository's [auto-close setting](#auto-close-setting) as confirmed or `null` when unknown, and every linked pull request URL across repositories and states. An empty list in a complete snapshot means the field holds no link; an incomplete snapshot is incomplete evidence.

### Linked Pull Request Records

A fresh record of every pull request a [Development snapshot](#development-snapshot) names, across repositories and states, saved as JSON lines at a local path, each with its [state](pull-request.md#state) and merge result.

### Completion Result

The normal delivery result of one task, epic or initiative: complete, or incomplete with each unmet condition. A task's comes from its [task delivery result](task-body.md#task-delivery-result), an epic's from its [delivery state](epic.md#delivery-state), and an initiative's from its [delivery state](initiative.md#delivery-state).

### Transfer Destination

The issue tracking another issue's work: its [identity](#issue-identity) and saved body, which contains that work and cites the source issue.

### Review Feedback

The reviewer's login and each point they raised in an issue's discussion.

### Auto-Close Setting

GitHub's **Auto-close issues with merged linked pull requests** repository setting, which must be disabled before a delivery pull request is linked or merged, so that closure follows the criteria rather than the merge.

- The setting is confirmed per repository and holds for the session; it is not inferred from an issue that stayed open.
- No REST field and no GraphQL field of `gh` 2.46 carries it, so on such a host the user's explicit answer is the only source.
- An enabled setting closes issues on merge whatever their criteria. Where it cannot be disabled, each affected issue's state is read after every merge and reopened where its criteria are unmet.

## Commands

### Create Tracker Issue

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

### Patch Issue Body

Replaces an issue's body from a file.

**Inputs:** Repository, issue number and complete populated body file.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -F 'body=@<body-file>' --jq .number
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -F body=@body.md --jq .number
```

### Fetch Issue Body

Saves an issue's body alone.

**Inputs:** Repository, issue number and destination file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' --jq .body > '<output-body-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' --jq .body > live-943.md
```

### Retitle Tracker Issue

Replaces an issue's title.

**Inputs:** Repository, issue number and complete title.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f title='<title>' --jq .title
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -f title='<title>' --jq .title
```

### Add Issue Labels

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

### Remove Issue Label

Removes one label from an issue.

**Inputs:** Repository, issue number and label name.

```bash
gh api --method DELETE 'repos/<owner>/<repo>/issues/<issue-number>/labels/<label>' --jq '.[].name'
```

**Example:**

```bash
gh api --method DELETE 'repos/<owner>/<repo>/issues/943/labels/<label>' --jq '.[].name'
```

### Fetch Issue Comments

Prints an issue's comments.

**Inputs:** Repository and issue number.

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/<issue-number>/comments'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/874/comments'
```

### Fetch Tracker Issue

Saves an issue whole, as JSON, for the scripts that read issues.

**Inputs:** Repository, issue number and destination JSON file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' > '<issue-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' > issue-943.json
```

### Check Issue Closure

Checks the issue criteria, the complete link snapshot and every linked pull request.

**Inputs:** Current issue JSON, complete Development snapshot and fresh linked pull request records.

- `--issue`, `--development`, and `--prs` are the fresh issue JSON, Development snapshot, and linked pull request records.
- Exit 0 means the closure gate passes; normal delivery checks must also pass. Exit 1 reports blockers. The command performs no network calls or writes.

Runs as [Helper invocation](../conventions.md) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue '<issue-json-file>' --development '<development-snapshot-file>' --prs '<linked-pull-request-records-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue issue-943.json --development development-943.json --prs development-prs-943.json
```

### Close as Not Planned

Closes an issue whose work another issue tracks.

**Inputs:** Issue identity and confirmed evidence that the work is tracked by its recorded destination.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f state=closed -f state_reason=not_planned --jq .state
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/874' -f state=closed -f state_reason=not_planned --jq .state
```

### Post Inline Comment

Posts one line of exact comment text and returns its URL.

**Inputs:** Repository, issue number and one-line comment text.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -f body='<comment-text>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/637/comments' -f body='Delivered by #950.' --jq .html_url
```

### Post Comment File

Posts a complete comment file and returns its URL.

**Inputs:** Repository, issue number and exact comment file.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -F 'body=@<comment-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/874/comments' -F body=@comment-874.md --jq .html_url
```

### Set Completed State

Sets an issue to closed with the completed reason and returns its state.

**Inputs:** Repository, issue number, passing normal delivery checks and an immediately preceding successful closure gate on current evidence.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f state=closed -f state_reason=completed --jq .state
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -f state=closed -f state_reason=completed --jq .state
```

### Write Development Snapshot

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

### Fetch All Issues

Saves every issue in the repository; the scripts skip the pull requests among them.

**Inputs:** Repository and destination JSON file.

```bash
gh api --paginate "repos/<owner>/<repo>/issues?state=all&per_page=100" > '<issues-json-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/issues?state=all&per_page=100" > issues.json
```

### Find Initiative Issue

Prints an initiative's issue number, found by its title's prefix.

**Inputs:** Repository and initiative prefix.

`<initiative-prefix>` includes the initiative id and its enclosing brackets.

```bash
gh api --paginate "repos/<owner>/<repo>/issues?state=all&per_page=100" --jq '.[] | select(.pull_request == null) | select(.title | startswith("<initiative-prefix>")) | .number'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/issues?state=all&per_page=100" --jq '.[] | select(.pull_request == null) | select(.title | startswith("[I08]")) | .number'
```

### List Prefixed Titles

Lists titles carrying one kind's prefix letter, across all states.

**Inputs:** Repository owner and name, and the kind's prefix letter.

```bash
gh api --paginate 'repos/<owner>/<repository>/issues?state=all&per_page=100' --jq '.[] | select(.title | test("^\\[<prefix-letter>[0-9]{2}\\]")) | .title'
```

**Example:** Initiatives in one repository.

```bash
gh api --paginate 'repos/m2ux/workflow-server/issues?state=all&per_page=100' --jq '.[] | select(.title | test("^\\[I[0-9]{2}\\]")) | .title'
```
