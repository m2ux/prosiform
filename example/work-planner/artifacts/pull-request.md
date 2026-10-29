---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Pull Request

A pull request's identity, head and base, issue links, review state and merge result. Its populated body is an input.

## Operations

### Merge Delivery Pull Request

One task or epic pull request's merge result, or its handoff for human approval.

**Inputs:** [Pull request](#pull-request-identity), [Delivery kind](#pull-request-kind), [Verified head](#verified-head), [Target requirements](delivery-branches.md#target-requirements), [Readiness evidence](#merge-readiness), [Auto-close setting](issue.md#auto-close-setting), [Merge authorization](#merge-authorization)

**Outputs:** [Merge result](#merge-result)

#### 1. Read Target Review Requirements

Read the supplied target branch's current required reviews and checks alongside the verified head. A branch whose protection or active rules require an approving review takes that review from a person. An agent cannot approve a pull request it opened; on such a branch, the merge belongs to the reviewer even when every other condition holds.
- Report the pull request as ready for approval, naming what was verified.
- Stop merge attempts. This handoff is a finished outcome.
- Keep approval with that reviewer. Another account, an administrative bypass or a setting change cannot supply it. Changing repository protection requires the user's explicit authorization, asked for separately.
- For example, workflow-server's `main` requires one approving review, so carry an epic to ready and stop.

#### 2. Merge the Approved Pull Request

When approval permits the agent to merge:
- Require current readiness evidence with no unresolved condition, and the auto-close setting confirmed for the repository as [Close Tracker Issue](issue.md#close-tracker-issue) documents.
- For an epic, apply [Merge Epic Pull Request](#merge-epic-pull-request) with the verified readiness evidence, authorization, target requirements and exact verified head SHA, then continue at [3. Return the Delivery Merge Result](#3-return-the-delivery-merge-result).

For a task whose readiness and authorization permit merging, run this merge from the repository checkout using the pull request’s repository and number.

- Require the supplied readiness evidence and authorization before issuing the merge.
- The merge method is a merge commit.

```bash
gh api --method PUT 'repos/<owner>/<repo>/pulls/<pull-request-number>/merge' -f merge_method='merge' --jq .merged
```

**Example:**

```bash
gh api --method PUT 'repos/<owner>/<repo>/pulls/950/merge' -f merge_method='merge' --jq .merged
```

- If the merge is refused, return the refusal to the caller for fresh verification.

#### 3. Return the Delivery Merge Result

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the merge result, including its merge commit when supplied, for the caller to confirm as [Write confirmation](../conventions.md) states.

### Access Development Links

The observed or updated Development relation for a pull request.

**Inputs:** [Pull request](#pull-request-identity), [Link request](#link-request), [Delivery issue](issue.md#issue-record), [Auto-close setting](issue.md#auto-close-setting)

**Outputs:** [Development links](#issue-links)

#### 1. Read the Pull Request Development Links

Use authenticated GitHub or an available supported tool to read the supplied pull request's actual Development field across every page and state, recording the repository and number for each linked issue and whether the field was fully readable. A missing tool or inaccessible field is a blocker, not an empty link set.

#### 2. Return the Read-Only Relation

Return the complete relation for a read-only request.

#### 3. Edit the Development Links

For a link edit, take the supplied repository prerequisite from [Confirm Repository Auto-Close](issue.md#confirm-repository-auto-close); an unconfirmed setting blocks the edit.
- Meet the applicable preconditions in [Close Tracker Issue](issue.md#close-tracker-issue).
- For an addition, use [GitHub's sidebar linking procedure](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue): in the issue's authenticated Development selector, select the pull request's repository and pull request, including a different repository when required. Retain the edit result.
- For removal of an abandoned or incorrect link, require the supplied user decision before deselecting the supplied relation in the authenticated Development selector and saving the edit. Retain the edit result.

#### 4. Re-Read the Pull Request Development Links

Read the same pull request's actual Development field through authenticated GitHub or an available supported tool, as [Write confirmation](../conventions.md) states.
- Include every page and state, recording each linked issue's repository and number and whether the field was fully readable.
- Return a failed edit or unreadable field as a blocker.

#### 5. Compare the Field with the Edit

Compare the field with the intended edit.

#### 6. Return the Verified Link Relation

Return the verified relation or discrepancy.

### Fetch Pull Request Issue Links

The complete issue-link snapshot for a supplied set of pull requests.

**Inputs:** [Pull request records](#pull-request-records), [Link snapshot path](#issue-link-snapshot)

**Outputs:** [Issue-link snapshot](#issue-link-snapshot)

#### 1. Read Links for Each Pull Request

For every pull request in the current records, `prs.json`, apply [Access Development Links](#access-development-links) with a read-only request and its identity. An observed empty field supplies an empty array; an unreadable field leaves the fetch incomplete.

#### 2. Re-Read Links After a Change

Repeat that read after a link changes, as [Write confirmation](../conventions.md) states.

#### 3. Return an Incomplete Link Fetch

If any relation is unreadable, return the incomplete result.

#### 4. Write the Links Snapshot

Write the observed complete relations to the supplied destination, such as `links.json`, in the [Issue-Link Snapshot](#issue-link-snapshot) shape. Include one entry per pull request and every linked issue's repository and number.

#### 5. Return the Links Snapshot

Return the snapshot for the scripts' `--links` input.

### Link Pull Request to Issue

The verified delivery-issue relation for a pull request.

**Inputs:** [Pull request](#pull-request-identity), [Delivery issue](issue.md#issue-record), [Pull request records](#pull-request-records), [Link snapshot path](#issue-link-snapshot), [Auto-close setting](issue.md#auto-close-setting)

**Outputs:** [Development links](#issue-links), [Issue-link snapshot](#issue-link-snapshot)

#### 1. Add the Development Link

Apply [Access Development Links](#access-development-links) with the supplied identities, requested link addition and the repository prerequisite confirmed as [Close Tracker Issue](issue.md#close-tracker-issue) documents.

#### 2. Stop on an Unverified Link Edit

Stop on a blocker or an unverified edit.

#### 3. Refresh the Links Snapshot

Apply [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links) with the current records and destination after the edit.

#### 4. Return the Verified Link and Snapshot

Return the verified relation and refreshed snapshot.

### Merge Epic Pull Request

The epic's verified merge into its long-lived target.

**Inputs:** [Pull request](#pull-request-identity), [Verified head](#verified-head), [Target requirements](delivery-branches.md#target-requirements), [Readiness evidence](#merge-readiness), [Merge authorization](#merge-authorization)

**Outputs:** [Merge result](#merge-result)

#### 1. Require Epic Merge Authorization

Require the supplied target requirements, current readiness evidence with no unresolved condition, and authorization for the agent to merge under the active delivery request and target review requirements.

#### 2. Submit the Epic Merge

From the repository checkout, submit the merge using the pull request identity and exact head SHA whose checks, target requirements and authorization were verified. Return a refusal without continuing.

The merge method is a merge commit. The endpoint refuses a different head.

```bash
gh api --method PUT 'repos/<owner>/<repo>/pulls/<pull-request-number>/merge' -f merge_method='merge' -f sha='<head-sha>' --jq '{merged, message, sha}'
```

**Example:**

```bash
gh api --method PUT 'repos/<owner>/<repo>/pulls/980/merge' -f merge_method='merge' -f sha='<head-sha>' --jq '{merged, message, sha}'
```

#### 3. Read the Epic Merge Result

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

From the repository checkout, read the merge result using the supplied repository and pull request number.

```bash
gh api 'repos/<owner>/<repo>/pulls/<pull-request-number>' --jq '{merged, merge_commit_sha, head: .head.sha, base: .base.ref}'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/pulls/980' --jq '{merged, merge_commit_sha, head: .head.sha, base: .base.ref}'
```

#### 4. Confirm the Merged Epic State

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Confirm the merged state, merge commit, verified head and target.

#### 5. Return the Epic Merge Result

Return the result or discrepancy.

### Fetch All Initiative Pull Requests

The pull request collection covering every supplied board repository.

**Inputs:** [Repositories](board.md#repositories), [Records path](#pull-request-records)

**Outputs:** [Pull request records](#pull-request-records)

#### 1. Fetch the First Repository Pull Requests

From the first repository’s checkout, fetch all initiative-prefixed pull requests to the supplied JSON-lines file, such as `prs.json`. This replaces the destination with a fresh collection.

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' > '<pull-request-records-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' > prs.json
```

#### 2. Stop on a First Fetch Failure

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Stop on failure.

#### 3. Append Further Repository Pull Requests

From each further repository’s checkout, append its initiative-prefixed pull requests to the same destination file. Read each fetch result before continuing; return incomplete evidence on any failure.

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' >> '<pull-request-records-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' >> prs.json
```

#### 4. Return Incomplete Pull Request Evidence

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

If any fetch failed, return incomplete evidence.

#### 5. Return the Complete Pull Request Collection

Return the complete collection only after every fetch succeeds.

### Read Initiative Pull Requests

The current delivery pull requests for one initiative.

**Inputs:** [Repository](repository-labels.md#repository), [Initiative prefix](initiative-issue-body.md#titles), [Records path](#pull-request-records)

**Outputs:** [Pull request records](#pull-request-records)

#### 1. Fetch the Initiative Pull Requests

From the repository checkout, save the initiative’s pull requests using its repository, prefix and destination JSON-lines file.

`<initiative-prefix>` includes the opening bracket and initiative id, matching its task and epic titles.

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("<initiative-prefix>"))' > '<pull-request-records-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I07"))' > prs.json
```

#### 2. Return the Initiative Collection

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the collection or an incomplete-fetch finding.

### Read Pull Request State

One current pull request and its requested supporting records.

**Inputs:** [Pull request](#pull-request-identity), [Requested records](#pull-request-snapshot), [Snapshot paths](#pull-request-snapshot)

**Outputs:** [Pull request snapshot](#pull-request-snapshot)

#### 1. Fetch the Pull Request Snapshot

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

#### 2. Fetch Requested Files or Reviews

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

#### 3. Return the Pull Request Snapshots

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the snapshots or missing evidence.

### Publish Pull Request

One pull request created or updated from supplied content and metadata.

**Inputs:** [Pull request](#pull-request-identity), [Kind](#pull-request-kind), [Pull request content](#pull-request-content), [Delivery issue](issue.md#issue-record), [Auto-close setting](issue.md#auto-close-setting), [Link snapshot path](#issue-link-snapshot)

**Outputs:** [Pull request snapshot](#pull-request-snapshot), [Issue-link snapshot](#issue-link-snapshot)

#### 1. Open a New Pull Request

For creation, select exactly one command for the supplied kind, body, title, head and base, preserving epic and discussion draft state. For an existing pull request, continue at [3. Update the Existing Pull Request](#3-update-the-existing-pull-request).

For task creation, run this command from the repository checkout using the supplied title, task branch, epic base and complete body file as [Bodies](../conventions.md) states.

- Supply the epic prefix and purpose as title, the task branch as head, the epic base as base, and the complete body file.

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='<title>' -f head='<task-branch>' -f base='<epic-base>' -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='[I07:E00] Purpose' -f head='i07/e00/w01-purpose' -f base='i07/e00/main' -F body=@body.md --jq .html_url
```

For epic creation, run this command from the repository checkout using the supplied title, epic base, long-lived target and review body file as [Bodies](../conventions.md) states.

- Supply the epic prefix and name as title, the epic base as head, its long-lived branch as base, and the populated review body file.
- `draft` is true, including when the work is already complete.

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='<title>' -f head='<epic-base>' -f base='<long-lived-base>' -F draft=true -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='[I07:E00] Name' -f head='i07/e00/main' -f base='main' -F draft=true -F body=@body.md --jq .html_url
```

For discussion creation, run this command from the repository checkout using the supplied title, planning branch, target branch and body file as [Bodies](../conventions.md) states.

```bash
gh api --method POST 'repos/<owner>/<repository>/pulls' -f title='<title>' -f head='<planning-branch>' -f base='<target-branch>' -F body=@'<body-file>' -F draft=true
```

**Example:**

```bash
gh api --method POST repos/m2ux/workflow-server/pulls -f title='Queue Planning: Scope and Delivery' -f head=planning/queue -f base=engineering -F body=@discussion.md -F draft=true
```

#### 2. Confirm Creation and Link the Delivery Issue

For a creation request, read the command’s exit code and returned identity; return a failure before attempting a link.
- For a task or epic pull request with a delivery issue, require the confirmed auto-close setting and snapshot destination, then apply [Link Pull Request to Issue](#link-pull-request-to-issue) with them, meeting [Issue Links](#issue-links). A row task without its own issue supplies no delivery issue, auto-close setting or link snapshot for publication.
- After a successful creation and any required link, continue at [4. Re-Read the Published Pull Request](#4-re-read-the-published-pull-request).

#### 3. Update the Existing Pull Request

For an existing pull request, run each command for a supplied change, preserving other fields. After each selected command, read its exit code and output; stop and return any failure before another mutation. If no field changes, continue with the supplied pull request identity.

When changing the body, run this update from the repository checkout using the pull request’s repository, number and complete body file as [Bodies](../conventions.md) states.

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

#### 4. Re-Read the Published Pull Request

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Re-read through [Read Pull Request State](#read-pull-request-state), as [Write confirmation](../conventions.md) states.

#### 5. Return the Published State

Return the saved state or discrepancy, and the issue-link snapshot when the creation path linked a delivery issue. Other publication paths return no issue-link snapshot.

### Align Pull Request Base

Each open delivery pull request pointed at the base its head requires.

**Inputs:** [Repository](repository-labels.md#repository), [Pull request records](#pull-request-records), [Long-lived branches](delivery-branches.md#branches), [Epic bases](delivery-branches.md#epic-bases), [Project checkout](delivery-branches.md#project-checkout)

**Outputs:** [Alignment result](#alignment-result)

#### 1. Take Each Pull Request Target

Take the target of each open pull request in the current records from [Scope](#scope) and [Other Pull Requests](#other-pull-requests), with each long-lived branch as [Epic Bases](delivery-branches.md#epic-bases) names it.
- Report an open pull request for which neither field gives a target for the user's decision, and leave it unchanged.

#### 2. Retarget Mismatched Pull Requests

For each open pull request whose base differs from its target, apply [Publish Pull Request](#publish-pull-request) with its number and that target as the base change.

#### 3. Update Unmergeable Task Branches

For each task pull request whose saved state is not mergeable, apply [Update Task Branch](delivery-branches.md#update-task-branch) with the worktree [Task Branches](delivery-branches.md#task-branches) places under the project checkout, its task branch and its epic base.
- A conflict leaves the pull request open and is reported.

#### 4. Return the Alignment Results

Return the retargeted pull requests, updated task branches, conflicts and the pull requests awaiting a decision.

### Locate Review Pull Request

The review pull request for a supplied epic base.

**Inputs:** [Repository](repository-labels.md#repository), [Epic base](delivery-branches.md#epic-bases)

**Outputs:** [Review pull request](#pull-request-identity)

#### 1. Find the Review Pull Request

From the repository checkout, find the open review pull request using the repository owner and name and supplied epic base as head.

```bash
gh api "repos/<owner>/<repo>/pulls?state=open&head=<owner>:<epic-base>" --jq '.[0].number'
```

**Example:**

```bash
gh api "repos/<owner>/<repo>/pulls?state=open&head=<owner>:i07/e00/main" --jq '.[0].number'
```

#### 2. Return the Review Pull Request Number

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return its number or an absent-review finding.

### Read Head Evidence

The check-run and status evidence for one literal head commit.

**Inputs:** [Repository](repository-labels.md#repository), [Verified head](#verified-head), [Evidence paths](#head-evidence)

**Outputs:** [Head evidence](#head-evidence)

#### 1. Fetch the Head Check Runs

From the repository checkout, save all check runs using the supplied repository, literal head SHA and destination file.

```bash
gh api --paginate 'repos/<owner>/<repo>/commits/<head-sha>/check-runs?per_page=100' > '<check-runs-file>'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/commits/<head-sha>/check-runs?per_page=100' > checks.json
```

#### 2. Fetch the Head Commit Status

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

From the repository checkout, save commit status using the same repository and literal head SHA and its destination file.

```bash
gh api --paginate 'repos/<owner>/<repo>/commits/<head-sha>/status?per_page=100' > '<commit-status-file>'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/commits/<head-sha>/status?per_page=100' > status.json
```

#### 3. Return the Head Evidence Snapshots

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return both snapshots, retaining missing or pending evidence as unresolved. The caller compares them with supplied target requirements and current reviews.

### Merge Task Pull Requests

Merges each open task pull request whose test plan has passed.

**Inputs:** [Task pull request](#pull-request-identity), [Epic base](delivery-branches.md#epic-bases), [Auto-close setting](issue.md#auto-close-setting), [Test plan](pull-request-body.md#test-plan)

**Outputs:** [Merge result](#merge-result)

#### 1. Confirm Auto-Close and Epic Base

Apply [Confirm Repository Auto-Close](issue.md#confirm-repository-auto-close) for the repository, and confirm the task pull request's epic base. The base carries no review requirement of its own; where one applies, [Merge Delivery Pull Request](#merge-delivery-pull-request) governs.

#### 2. Fetch Task Merge Readiness

Apply [Fetch Merge Readiness](#fetch-merge-readiness) with delivery kind task for the task pull request and its epic base as target.

#### 3. Merge the Task Pull Request

Require a passed [test plan](pull-request-body.md#test-plan), then apply [Merge Delivery Pull Request](#merge-delivery-pull-request) with delivery kind task, the verified head, target requirements, repository prerequisite and passing evidence, without further confirmation.
- Stop on a handoff for human approval.
- Return a refusal with its readiness evidence. The pull request stays open.

#### 4. Confirm the Merged Task State

Apply [Read Pull Request State](#read-pull-request-state) to confirm the merged state, head, base and merge commit.
- Return that result to the caller.

### Fetch Merge Readiness

The current pull request's readiness against its target requirements and head checks.

**Inputs:** [Pull request](#pull-request-identity), [Delivery kind](#pull-request-kind), [Target branch](#target-branch), [Epic base](delivery-branches.md#epic-bases), [Evidence paths](#merge-readiness)

**Outputs:** [Readiness evidence](#merge-readiness), [Verified head](#verified-head), [Target requirements](delivery-branches.md#target-requirements)

#### 1. Snapshot the Pull Request State

Apply [Read Pull Request State](#read-pull-request-state) with the pull request identity and destination `epic-pr.json`.
- Retain the literal head SHA and target branch for the evidence calls.
- For an epic pull request, report it as not ready when its head is not the supplied epic base, or its target is not that base's long-lived branch, as [Epic Bases](delivery-branches.md#epic-bases) names it.

#### 2. Read the Merge Target Requirements

Apply [Read Target Requirements](delivery-branches.md#read-target-requirements) with the repository, target and protection/rules output paths.
- Carry any unresolved requirement into the readiness result.

#### 3. Read the Readiness Head Evidence

Read the head evidence.
- Apply [Read Head Evidence](#read-head-evidence) with the exact head SHA and check/status output paths.
- Request reviews through [Read Pull Request State](#read-pull-request-state) with the pull request identity and reviews output path. A conflict, a failed, missing or pending check, a blocked merge state or an unmet required review leaves readiness unresolved.

#### 4. Re-Read the Pull Request State

Apply [Read Pull Request State](#read-pull-request-state) again with the same identity and destination.
- Compare its head with the retained SHA; a changed head requires fresh evidence.
- Return the verified head, target requirements and readiness result, including unresolved conditions.

## Fields

### State

A pull request is open, draft, ready for review, merged or closed without merge. A merged result identifies the verified head, target and merge commit.

- An epic's review pull request is published as a draft when the first task merges into its epic base, and an unmerged epic base with work merged into it has one.
- The review stays draft, and its epic open, until the epic is complete and the user marks it ready.

### Scope

A task pull request delivers one task, or a set of tasks that name each other in Joins. It targets the epic base for the long-lived branch its work changes.

### Other Pull Requests

- A pull request whose head is an epic base targets that base's long-lived branch.
- A pull request outside epic delivery targets a long-lived branch. An open stacked pull request targets its long-lived branch once its base merges.
- A merged pull request keeps the base it merged into.

### Issue Links

- GitHub shows the link in the pull request's Development field and in the issue's Linked pull requests field, which the project board reads.
- A task pull request links the task's issue, and a review pull request links its epic's issue.
- The link is addressed by issue, so a pull request whose work carries no issue links nothing. A task pull request delivering rows that have no issue of their own is the whole of what stays unlinked.
- The link is stored on the pull request. It holds on any base branch and on a pull request that has merged, and a later body edit leaves it standing.
- A linked issue remains open until its criteria and delivery requirements hold and every Development-linked pull request is merged.
- The field is the whole of the relation: neither body links the other. The pull request's References carry its sources, and the issue it delivers is not among them.
- A pull request with a delivery issue but no Development link is uncited.

### Pull Request Identity

A pull request's [repository](repository-labels.md#repository) and number. A pull request yet to be created has its repository alone.

### Pull Request Kind

Task, epic or planning discussion. A delivery pull request is a task or an epic one: a task pull request meets [Scope](#scope), and an epic's review pull request has an epic base as its head.

### Target Branch

The base a pull request merges into: the epic base [Scope](#scope) names for a task pull request, or the long-lived branch [Other Pull Requests](#other-pull-requests) names otherwise.

### Verified Head

The literal head commit SHA whose checks, reviews and target requirements were read. Verification applies to that exact SHA.

### Pull Request Content

The fields a publication writes: a body file at its path, meeting [Template](pull-request-body.md#template), its title, head and base. A change to an existing pull request names only the fields it changes.

### Pull Request Snapshot

One pull request's REST record as a local JSON file at its path, with its identity, state, head SHA, base and mergeable state. Its requested supporting records are its changed paths and its reviews, each in a file of its own.

### Pull Request Records

A local JSON-lines file at its path, one pull request's REST record per line. An initiative's records hold every pull request whose title carries its prefix, in all states, across its repositories; a failed fetch leaves them incomplete.

### Issue-Link Snapshot

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

### Link Request

A read, an addition or a removal of one pull request's Development link. An edit names the issue; a removal carries the user's decision naming the abandoned or incorrect link.

### Head Evidence

The check runs and the combined commit status for one verified head, each a local JSON file at its path. Missing or pending evidence is unresolved.

### Merge Readiness

The readiness of one pull request at its verified head: its snapshot, [target requirements](delivery-branches.md#target-requirements), [head evidence](#head-evidence) and reviews, each a local JSON file at its path, with every unresolved condition. A conflict, a failed, missing or pending check, a blocked merge state, an unmet required review, or an epic pull request whose head or target departs from [Epic Bases](delivery-branches.md#epic-bases) is unresolved; readiness passes when none remains.

### Merge Authorization

The authorization result for the agent to merge the named pull request under the active delivery request and target review requirements, including any required human approval.

### Merge Result

One of: the merged [state](#state) with its verified head, target and merge commit; a handoff for human approval naming what was verified; or a refusal with its readiness evidence.

### Alignment Result

The pull requests retargeted, the task branches updated, the conflicts met, and the pull requests whose target awaits the user's decision.
