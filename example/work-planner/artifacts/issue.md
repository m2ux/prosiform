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

#### 2. Fetch the Issue Comments

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

When the request depends on the discussion, fetch every comment from the repository checkout using the supplied repository and issue number.

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/<issue-number>/comments'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/874/comments'
```

#### 3. Return the Issue Read

Read each requested response and its exit code; return the issue record and any requested comments, or the failed read as missing evidence. When no discussion was requested, return the issue record alone.

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

For a new issue, run this creation command from the repository checkout using the supplied title, existing labels and complete body file as [Bodies](../conventions.md) states.

Repeat `-f 'labels[]=<label>'` for each supplied label.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues' -f title='<title>' -F 'body=@<body-file>' -f 'labels[]=<label>' --jq .number
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues' -f title='<title>' -F body=@body.md -f 'labels[]=<label>' --jq .number
```

#### 4. Update the Existing Issue

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

For an existing issue, run each command whose field is being changed, preserving all other fields. After each selected command, read its exit code and output; stop and return any failure before another mutation. If no field changes, continue with the supplied issue identity.

When changing the issue body, run this update from the repository checkout using its repository, number and complete body file as [Bodies](../conventions.md) states.

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

#### 5. Comment on the Saved Issue

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Apply [Comment on Issue](#comment-on-issue) for an answer or a preserved body the caller requires, with the issue number and comment file.

#### 6. Re-Read the Saved Issue

As [Write confirmation](../conventions.md) states, read the saved issue.

From the repository checkout, save the current issue using its repository, number and supplied destination JSON file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' > '<issue-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' > issue-943.json
```

#### 7. Compare the Saved Issue Fields

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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

From `<workspace>`, run the closure gate with the fresh issue JSON, complete Development snapshot and linked pull request records as `--issue`, `--development` and `--prs`.

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

#### 4. Require the Closure Gate

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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

With confirmed evidence that the destination tracks the work, run this closure from the repository checkout using the issue’s repository and number, retaining its body.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f state=closed -f state_reason=not_planned --jq .state
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/874' -f state=closed -f state_reason=not_planned --jq .state
```

#### 4. Re-Read the Transferred Issue

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Re-read it with Fetch Tracker Issue for its state and reason, as [Write confirmation](../conventions.md) states.

From the repository checkout, save the current issue using its repository, number and supplied destination JSON file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' > '<issue-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' > issue-943.json
```

#### 5. Confirm the Transferred Issue State

Read the final fetch exit code and response. Return a read failure or discrepancy unless the issue is closed with reason `not_planned`; otherwise return the confirmed closed issue with its retained body.

### Comment on Issue

The supplied discussion text saved on one issue.

**Inputs:** [Issue identity](#issue-identity), [Comment](#issue-comment), [Review feedback](#review-feedback)

**Outputs:** [Saved comment](#issue-comment)

#### 1. Compose the Feedback Reply

When replying to feedback already folded into the body, compose a precise, factual reply addressing each point and mentioning the reviewer, with no thanks or filler. Name what the body now says, by criterion id where one carries it, or the issue that takes the point.

#### 2. Publish the Issue Comment

Publish the supplied comment:
For a one-line comment, post its exact text from the repository checkout using the supplied repository and issue number.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -f body='<comment-text>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/637/comments' -f body='Delivered by #950.' --jq .html_url
```

For a longer comment, post the complete supplied file from the repository checkout using the repository and issue number, as [Bodies](../conventions.md) states.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -F 'body=@<comment-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/874/comments' -F body=@comment-874.md --jq .html_url
```

#### 3. Return the Comment URL

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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

From `<workspace>`, run the closure gate with the current issue JSON, complete Development snapshot and linked pull request records. Use absolute evidence paths when changing directory.

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

#### 4. Require the Completion Gate to Pass

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Require exit 0 and passing normal delivery checks; a sync report of closable does not permit skipping this gate.

#### 5. Set the Completed State

Immediately after the gate passes and normal delivery checks pass, run this closure from the repository checkout using the issue’s repository and number.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f state=closed -f state_reason=completed --jq .state
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -f state=closed -f state_reason=completed --jq .state
```

#### 6. Return the Completed State

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the saved state or failure.

### Capture Issue Development

The issue's current content and complete Development snapshot.

**Inputs:** [Issue identity](#issue-identity), [Auto-close setting](#auto-close-setting), [Record path](#issue-record), [Snapshot path](#development-snapshot)

**Outputs:** [Development snapshot](#development-snapshot), [Issue record](#issue-record)

#### 1. Read the Development Field

Apply [Read Issue Development](#read-issue-development) for the entire field across repositories and states. An inaccessible field returns incomplete evidence; an empty array means the field was checked and empty.

#### 2. Write the Development Snapshot

Write the issue identity, observed links, completeness result and repository setting to the supplied path, such as `development-943.json`, in the [Development Snapshot](#development-snapshot) shape. Preserve incomplete evidence as incomplete and the unknown auto-close setting as `null`.

#### 3. Fetch the Issue Snapshot

From the repository checkout, save the issue’s current JSON using its repository and number and the supplied path, such as `issue-943.json`.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' > '<issue-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' > issue-943.json
```

#### 4. Return the Development Files

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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

From the repository checkout, save every issue in every state using the supplied repository and destination JSON file.

```bash
gh api --paginate "repos/<owner>/<repo>/issues?state=all&per_page=100" > '<issues-json-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/issues?state=all&per_page=100" > issues.json
```

#### 2. Return the Repository Issues

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return it with pull requests distinguishable from issues.

### Locate Initiative Issue

The tracker identity matching one initiative prefix.

**Inputs:** [Repository](#tracker-repository), [Initiative prefix](#tracker-prefix)

**Outputs:** [Initiative issue](#issue-identity)

#### 1. Find the Initiative Issue

From the repository checkout, find the initiative using the supplied repository and initiative prefix.

`<initiative-prefix>` includes the initiative id and its enclosing brackets.

```bash
gh api --paginate "repos/<owner>/<repo>/issues?state=all&per_page=100" --jq '.[] | select(.pull_request == null) | select(.title | startswith("<initiative-prefix>")) | .number'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/issues?state=all&per_page=100" --jq '.[] | select(.pull_request == null) | select(.title | startswith("[I08]")) | .number'
```

#### 2. Return the Initiative Issue Number

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return its issue number or an unresolved identity.

### Select Tracker Number

The next unused number for one prefixed issue kind in the repository.

**Inputs:** [Repository](#tracker-repository), [Prefix letter](#tracker-prefix)

**Outputs:** [Tracker number](#tracker-prefix)

#### 1. List the Prefixed Titles

From the repository checkout, list titles in all issue states using the supplied repository and kind’s prefix letter.

```bash
gh api --paginate 'repos/<owner>/<repository>/issues?state=all&per_page=100' --jq '.[] | select(.title | test("^\\[<prefix-letter>[0-9]{2}\\]")) | .title'
```

**Example:** Initiatives in one repository.

```bash
gh api --paginate 'repos/m2ux/workflow-server/issues?state=all&per_page=100' --jq '.[] | select(.title | test("^\\[I[0-9]{2}\\]")) | .title'
```

#### 2. Read the Highest Prefix

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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
