---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Delivery Branches

The long-lived branches, epic bases and task branches used for delivery.

## Operations

### *Prepare* Delivery Bases

The branches a task pull request targets.

**Inputs:** Project checkout, epic identifier, changed long-lived branches and confirmed prerequisite evidence.

#### 1. List the Long-Lived Branches

Run [List Long-Lived Branches](#list-long-lived-branches) with `--project` set to the project checkout.

#### 2. List the Epic Bases

Run [List Epic Bases](#list-epic-bases) for the epic.

#### 3. Report Missing Branch Configuration

If `config/branches` is missing or empty:
- Report the names as unevaluable.
- Obtain the project's branch names before creating delivery branches.

#### 4. Require Base Prerequisite Evidence

Require the caller's confirmed prerequisite evidence before creating a base. The board status alone supplies no such evidence.

#### 5. Create Each Missing Epic Base

Apply [Create Epic Base](#create-epic-base) for each missing base, passing the project checkout, corresponding long-lived branch, epic base name and confirmed prerequisite evidence.

### *Create* Epic Base

The missing epic branch rooted in its remote long-lived branch.

**Inputs:** Repository checkout, long-lived source branch, missing epic base name and confirmed prerequisite evidence.

#### 1. Require a Missing Destination Base

Require the confirmed prerequisites and a missing destination. Refuse a destination that already exists.

#### 2. Fetch the Long-Lived Source Branch

Run [Fetch Remote Branch](#fetch-remote-branch) in the supplied repository checkout with the corresponding long-lived source branch, such as `main`.

#### 3. Publish the New Epic Base

After a successful fetch:
- Run [Publish Epic Base](#publish-epic-base) with that remote source and the missing epic base name, such as `i07/e00/main`, meeting [Epic Bases](#epic-bases).
- Return the created branch or the failure.

### *Update* Epic Base

The current long-lived target merged into an epic base.

**Inputs:** Project checkout and epic base branch.

#### 1. Derive the Epic Base Target and Worktree

Take the long-lived target and the worktree path from the base name, meeting [Epic Bases](#epic-bases).

#### 2. Fetch the Epic Base

Run [Fetch Remote Branch](#fetch-remote-branch) in the project checkout with that epic base; stop on failure.

#### 3. Add or Reuse the Epic Base Worktree

Run [Add Epic Base Worktree](#add-epic-base-worktree) for an absent worktree, and reuse an existing one; stop on failure, which a base checked out elsewhere returns.

#### 4. Fetch the Long-Lived Target

Run [Fetch Remote Branch](#fetch-remote-branch) in that worktree with the long-lived target, such as `main`; stop on failure.

#### 5. Merge the Long-Lived Target

Run [Merge Remote Branch](#merge-remote-branch) in that worktree with the target branch name, such as `main`, to merge `origin/main`. A conflict stops the update, leaves the pull request open and is reported.

#### 6. Push the Updated Epic Base

After a successful merge:
- Run [Push Epic Base](#push-epic-base) in the same worktree.
- Return the updated branch or the failure.

### *Update* Task Branch

The current epic base merged into a unit's task branch.

**Inputs:** Task worktree, task branch name and corresponding epic base branch.

#### 1. Fetch the Epic Base into the Task Worktree

Run [Fetch Remote Branch](#fetch-remote-branch) in the unit's worktree with the epic base, such as `i07/e00/main`.

#### 2. Stop on a Task Branch Fetch Failure

Stop on failure.

#### 3. Merge the Epic Base into the Task Branch

Run [Merge Remote Branch](#merge-remote-branch) in that worktree with the epic base name, such as `i07/e00/main`, to merge `origin/i07/e00/main`. A conflict stops the update, leaves the pull request open and is reported.

#### 4. Push the Updated Task Branch

After a successful merge:
- Run [Push Task Branch](#push-task-branch) with the task branch as destination.
- Return the updated branch or the failure.

### *Create* Task Worktree

The worktree and branch one unit's session works in.

**Inputs:** Project checkout, worktree path, task branch, epic base and confirmed prerequisite evidence.

#### 1. Require Task Worktree Prerequisites

Require the supplied prerequisites and names meeting [Task Branches](#task-branches).

#### 2. Select the Worktree Epic Base

When the unit changes several long-lived branches, select the corresponding epic base for this worktree.

#### 3. Fetch the Selected Epic Base

Run [Fetch Remote Branch](#fetch-remote-branch) from the checkout of the repository the work changes, passing that epic base; stop on failure.

#### 4. Add the Task Worktree

Run [Add Task Worktree](#add-task-worktree) with the supplied path and task branch, rooted in the fetched epic base.

#### 5. Return the Task Worktree

Return the worktree path and branch or the failure.

### *Create* Pull Request Worktree

The detached worktree where the graph reads the reviewed change.

**Inputs:** Repository, repository checkout, pull request number and verified head commit.

#### 1. Fetch the Review Head

Run [Fetch Review Head](#fetch-review-head) in the checkout of the repository the pull request changes, passing its number; stop on failure.

#### 2. Read the Fetched Revision

Run [Read Checkout Revision](#read-checkout-revision) in the repository checkout for `FETCH_HEAD`.

#### 3. Recheck a Differing Fetched Head

If it differs from the verified head:
- Apply [Read Pull Request State](pull-request.md#read-pull-request-state) for the same pull request, and take its head as the verified head.
- Repeat [1. Fetch the Review Head](#1-fetch-the-review-head) and [2. Read the Fetched Revision](#2-read-the-fetched-revision) once.
- If the fetched head still differs, return a changed-head finding before creating a worktree.

#### 4. Derive the Review Worktree Path

Take the worktree path from the pull request number, meeting [Review Worktrees](#review-worktrees).

#### 5. Check an Existing Review Worktree

If that worktree already exists:
- Run Read Checkout Revision there for `HEAD`.
- Run [Read Checkout Status](#read-checkout-status) there.
- Reuse it only at the verified head and when its status reports detached HEAD with no tracked or untracked changes.
- Otherwise retain it and select an unused path suffixed with the verified commit.

#### 6. Add the Review Worktree

For an unused path, run [Add Review Worktree](#add-review-worktree) with that path and the verified commit.

#### 7. Confirm the Review Worktree Head

Confirm its HEAD through Read Checkout Revision.

#### 8. Return the Review Worktree

Return the selected detached worktree path and head, or the discrepancy before measuring.

### *Read* Target Requirements

The protection and active rules governing one target branch.

**Inputs:** Repository, target branch and output files.

#### 1. Fetch the Target Branch Protection

Run [Fetch Branch Protection](#fetch-branch-protection) for the supplied target.

#### 2. Fetch the Target Active Rules

Run [Fetch Active Branch Rules](#fetch-active-branch-rules) for the same target.

#### 3. Return the Target Requirement Records

Return both records. An unreadable requirement remains unresolved; a protection 404 does not establish the absence of active rules.

### *Read* Delivery Branches

The configured long-lived branches and existing epic bases.

**Inputs:** Project checkout and epic identity.

#### 1. Read the Long-Lived Branch Configuration

Run [List Long-Lived Branches](#list-long-lived-branches) with the supplied checkout. Missing or empty configuration leaves branch names unevaluable.

#### 2. Read the Epic Base Names

Run [List Epic Bases](#list-epic-bases) for the supplied epic.

#### 3. Return the Delivery Branch Collections

Return both collections and any missing configuration.

## Fields

### Branches

A project states its long-lived branches in `config/branches` at its root, one name per line. A run from a linked worktree reads the statement its main working tree holds.

- **Example.**
  workflow-server's `config/branches` names `docker`, `main`, `workflows` and `workspace`.

### Epic Bases

- Each long-lived branch an epic changes has a base branch, named for the initiative, the epic and that branch, and rooted in that long-lived branch. Its prerequisite epics are closed as completed with every delivery base merged.
- **Example.**
  An epic base cut from `main` is `i07/e00/main`.
- The base's last segment is its long-lived branch, which gives the target it merges and is merged into.
- Each base is worked in one worktree, named by the base under the worktree directory of the repository's main working tree.
- **Example.**
  `i07/e00/main` merges `main`, and is checked out at `.worktrees/i07/e00/main`.
- A completed epic is delivered by merging each base into its long-lived branch. The epic stays open until every base has merged.

### Review Worktrees

A reviewed pull request is read in a detached worktree, named by its number under the worktree directory of the repository's main working tree.

- **Example.**
  Pull request 950 is read at `.worktrees/pr-950`.

### Task Branches

A unit's task branch is cut from the epic base for the long-lived branch the unit changes, named for its initiative, epic and first task in lowercase separated by slashes, and hyphenated with a slug of at most four words from its Description when one exists: `i01/e02/w04-write-defaults`. Every pull request delivering the unit's work is opened from this branch.

Its worktree is named by that branch under the worktree directory of the repository's main working tree.

## Commands

### List Epic Bases

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

### List Long-Lived Branches

Prints the long-lived branch names, one per line.

**Inputs:** Project checkout.

- The names meet [Branches](#branches).
- `--project` is any checkout of the project. The names are the ones `config/branches` states in its main working tree, which a linked worktree resolves for itself.
- A missing or empty statement prints `unevaluable:`, names what is missing, and exits 1.

Runs as [Helper invocation](../conventions.md) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py --names --project '<checkout>'
```

### Fetch Remote Branch

Fetches one source branch from origin.

**Inputs:** Repository checkout and source branch.

```bash
git fetch origin '<source-branch>'
```

### Publish Epic Base

Creates a remote epic base from the fetched source branch.

**Inputs:** Repository checkout, fetched long-lived source branch, destination epic-base name, confirmed missing destination and prerequisite evidence.

```bash
git push origin 'origin/<source-branch>:refs/heads/<epic-base>'
```

### Merge Remote Branch

Merges one fetched remote branch into the current worktree branch.

**Inputs:** Destination worktree and fetched source branch name without the origin prefix.

```bash
git merge --no-edit 'origin/<source-branch>'
```

### Push Epic Base

Pushes the current epic base to its configured upstream.

**Inputs:** Epic-base worktree and successful merge result.

```bash
git push
```

### Push Task Branch

Pushes the task worktree head to its named remote task branch.

**Inputs:** Task worktree, destination task branch and successful merge result.

```bash
git push origin 'HEAD:refs/heads/<task-branch>'
```

**Example:**

```bash
git push origin HEAD:refs/heads/i07/e00/w01-queue-plan
```

### Add Task Worktree

Creates a task branch and worktree at the fetched epic base.

**Inputs:** Project checkout, worktree path, task branch, fetched epic base and confirmed prerequisite evidence.

- The path resolves against the directory the command runs in, so supply it as [Task Branches](#task-branches) anchors it rather than relative to a linked worktree.

```bash
git worktree add '<worktree-path>' -b '<task-branch>' 'origin/<epic-base>'
```

**Example:**

```bash
git worktree add .worktrees/i07-e00-w01 -b i07/e00/w01-queue-plan origin/i07/e00/main
```

### Fetch Review Head

Fetches one pull request head into FETCH_HEAD.

**Inputs:** Repository checkout and pull request number.

```bash
git fetch origin 'pull/<pull-request-number>/head'
```

**Example:**

```bash
git fetch origin pull/950/head
```

### Add Epic Base Worktree

Creates the worktree for an existing epic base.

**Inputs:** Project checkout, worktree path and fetched epic base.

- The path resolves against the directory the command runs in, so supply it as [Epic Bases](#epic-bases) anchors it rather than relative to a linked worktree.

```bash
git worktree add '<worktree-path>' '<epic-base>'
```

**Example:**

```bash
git worktree add .worktrees/i07/e00/main i07/e00/main
```

### Add Review Worktree

Creates a detached worktree at the fetched review head.

**Inputs:** Repository checkout, worktree path and fetched head commit.

- The path resolves against the directory the command runs in, so supply it as [Review Worktrees](#review-worktrees) anchors it rather than relative to a linked worktree.

```bash
git worktree add --detach '<worktree-path>' '<head-commit>'
```

### Fetch Branch Protection

Saves the target branch protection response.

**Inputs:** Repository, target branch and destination file.

```bash
gh api 'repos/<owner>/<repo>/branches/<target-branch>/protection' > '<branch-protection-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/branches/main/protection' > protection.json
```

### Fetch Active Branch Rules

Saves every active rule for the target branch.

**Inputs:** Repository, target branch and destination file.

```bash
gh api --paginate 'repos/<owner>/<repo>/rules/branches/<target-branch>' > '<branch-rules-file>'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/rules/branches/main' > branch-rules.json
```

### Read Checkout Revision

Resolves one revision to its commit in the selected checkout.

**Inputs:** Checkout and revision, such as HEAD or FETCH_HEAD.

```bash
git -C '<checkout>' rev-parse '<revision>^{commit}'
```

### Read Checkout Status

Reports branch or detached-HEAD state and tracked and untracked changes in one checkout.

**Inputs:** Checkout path.

```bash
git -C '<checkout>' status --porcelain --branch
```
