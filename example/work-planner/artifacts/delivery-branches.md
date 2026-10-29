---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Delivery Branches

The long-lived branches, epic bases and task branches used for delivery.

## Operations

### Prepare Delivery Bases

The branches a task pull request targets.

**Inputs:** [Project checkout](#project-checkout), [Epic prefix](#epic-bases), [Changed long-lived branches](#branches), [Prerequisite evidence](epic.md#prerequisite-evidence)

**Outputs:** [Epic bases](#epic-bases)

#### 1. List the Long-Lived Branches

From `<workspace>`, read the long-lived branch configuration with `--project` set to the supplied project checkout.

- The names meet [Branches](#branches).
- `--project` is any checkout of the project. The names are the ones `config/branches` states in its main working tree, which a linked worktree resolves for itself.
- A missing or empty statement prints `unevaluable:`, names what is missing, and exits 1.

Runs as [Helper invocation](../conventions.md) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py --names --project '<checkout>'
```

#### 2. List the Epic Bases

Read the branch-name helper result. Preserve an expected `unevaluable:` result with exit 1 for the configuration decision below; return other execution errors.

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

#### 3. Report Missing Branch Configuration

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

If `config/branches` is missing or empty:
- Report the names as unevaluable.
- Obtain the project's branch names before creating delivery branches.

#### 4. Require Base Prerequisite Evidence

Require the caller's confirmed prerequisite evidence before creating a base. The board status alone supplies no such evidence.

#### 5. Create Each Missing Epic Base

Apply [Create Epic Base](#create-epic-base) for each missing base, passing the project checkout, corresponding long-lived branch, epic base name and confirmed prerequisite evidence.

### Create Epic Base

The missing epic branch rooted in its remote long-lived branch.

**Inputs:** [Project checkout](#project-checkout), [Long-lived branch](#branches), [Epic base](#epic-bases), [Prerequisite evidence](epic.md#prerequisite-evidence)

**Outputs:** [Epic base](#epic-bases)

#### 1. Require a Missing Destination Base

Require the confirmed prerequisites and a missing destination. Refuse a destination that already exists.

#### 2. Fetch the Long-Lived Source Branch

From the supplied repository checkout, fetch the corresponding long-lived source branch, such as `main`.

```bash
git fetch origin '<source-branch>'
```

#### 3. Publish the New Epic Base

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

After a successful fetch:

From the repository checkout, publish the fetched source as the confirmed missing epic base, such as `i07/e00/main`, meeting [Epic Bases](#epic-bases).

```bash
git push origin 'origin/<source-branch>:refs/heads/<epic-base>'
```


#### 4. Confirm the Published Epic Base

Read the push exit code and output. Return the created base only on success; return a refused or non-fast-forward push without rewriting the remote branch.

### Update Epic Base

The current long-lived target merged into an epic base.

**Inputs:** [Project checkout](#project-checkout), [Epic base](#epic-bases)

**Outputs:** [Epic base](#epic-bases)

#### 1. Derive the Epic Base Target and Worktree

Take the long-lived target and the worktree path from the base name, meeting [Epic Bases](#epic-bases).

#### 2. Fetch the Epic Base

From the project checkout, fetch the supplied epic base; stop on failure.

```bash
git fetch origin '<source-branch>'
```

#### 3. Add or Reuse the Epic Base Worktree

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

For an absent worktree, run this command from the project checkout using the supplied path and fetched epic base. Reuse an existing worktree; stop on failure, including a base checked out elsewhere.

- The path resolves against the directory the command runs in, so supply it as [Epic Bases](#epic-bases) anchors it rather than relative to a linked worktree.

```bash
git worktree add '<worktree-path>' '<epic-base>'
```

**Example:**

```bash
git worktree add .worktrees/i07/e00/main i07/e00/main
```

#### 4. Fetch the Long-Lived Target

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

From the epic-base worktree, fetch its long-lived target, such as `main`; stop on failure.

```bash
git fetch origin '<source-branch>'
```

#### 5. Merge the Long-Lived Target

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

From the epic-base worktree, merge the fetched target by its branch name without the `origin/` prefix, such as `main`. A conflict stops the update, leaves the pull request open and is reported.

```bash
git merge --no-edit 'origin/<source-branch>'
```

#### 6. Push the Updated Epic Base

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

After a successful merge:
After a successful merge, push from the same epic-base worktree.

```bash
git push
```


#### 7. Confirm the Epic Base Push

Read the push exit code and output. Return the updated base only on success; report a failed or non-fast-forward push without rewriting the remote branch.

### Update Task Branch

The current epic base merged into a unit's task branch.

**Inputs:** [Task worktree](#task-branches), [Task branch](#task-branches), [Epic base](#epic-bases)

**Outputs:** [Task branch](#task-branches)

#### 1. Fetch the Epic Base into the Task Worktree

From the unit’s worktree, fetch its epic base, such as `i07/e00/main`.

```bash
git fetch origin '<source-branch>'
```

#### 2. Stop on a Task Branch Fetch Failure

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Stop on failure.

#### 3. Merge the Epic Base into the Task Branch

From the unit’s worktree, merge its fetched epic base using the branch name without the `origin/` prefix, such as `i07/e00/main`. A conflict stops the update, leaves the pull request open and is reported.

```bash
git merge --no-edit 'origin/<source-branch>'
```

#### 4. Push the Updated Task Branch

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

After a successful merge:
After a successful merge, push from the task worktree with the supplied task branch as destination.

```bash
git push origin 'HEAD:refs/heads/<task-branch>'
```

**Example:**

```bash
git push origin HEAD:refs/heads/i07/e00/w01-queue-plan
```


#### 5. Confirm the Task Branch Push

Read the push exit code and output. Return the updated task branch only on success; report a failed or non-fast-forward push without rewriting the remote branch.

### Create Task Worktree

The worktree and branch one unit's session works in.

**Inputs:** [Project checkout](#project-checkout), [Task worktree](#task-branches), [Task branch](#task-branches), [Epic base](#epic-bases), [Prerequisite evidence](epic.md#prerequisite-evidence)

**Outputs:** [Task worktree](#task-branches), [Task branch](#task-branches)

#### 1. Require Task Worktree Prerequisites

Require the supplied prerequisites and names meeting [Task Branches](#task-branches).

#### 2. Select the Worktree Epic Base

When the unit changes several long-lived branches, select the corresponding epic base for this worktree.

#### 3. Fetch the Selected Epic Base

From the checkout of the repository the work changes, fetch the supplied epic base; stop on failure.

```bash
git fetch origin '<source-branch>'
```

#### 4. Add the Task Worktree

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

From the project checkout, add the supplied task worktree path and task branch, rooted in the fetched epic base.

- The path resolves against the directory the command runs in, so supply it as [Task Branches](#task-branches) anchors it rather than relative to a linked worktree.

```bash
git worktree add '<worktree-path>' -b '<task-branch>' 'origin/<epic-base>'
```

**Example:**

```bash
git worktree add .worktrees/i07-e00-w01 -b i07/e00/w01-queue-plan origin/i07/e00/main
```

#### 5. Return the Task Worktree

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the worktree path and branch or the failure.

### Create Pull Request Worktree

The detached worktree where the graph reads the reviewed change.

**Inputs:** [Pull request](pull-request.md#pull-request-identity), [Project checkout](#project-checkout), [Verified head](pull-request.md#verified-head)

**Outputs:** [Review worktree](#review-worktrees), [Verified head](pull-request.md#verified-head)

#### 1. Fetch the Review Head

From the checkout of the repository the pull request changes, fetch its supplied number’s review head; stop on failure.

```bash
git fetch origin 'pull/<pull-request-number>/head'
```

**Example:**

```bash
git fetch origin pull/950/head
```

#### 2. Read the Fetched Revision

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

From the repository checkout, resolve `FETCH_HEAD` as the revision and use that checkout path for `<checkout>`.

```bash
git -C '<checkout>' rev-parse '<revision>^{commit}'
```

#### 3. Recheck a Differing Fetched Head

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

If it differs from the verified head:
- Apply [Read Pull Request State](pull-request.md#read-pull-request-state) for the same pull request, and take its head as the verified head.
- Repeat [1. Fetch the Review Head](#1-fetch-the-review-head) and [2. Read the Fetched Revision](#2-read-the-fetched-revision) once.
- If the fetched head still differs, return a changed-head finding before creating a worktree.

#### 4. Derive the Review Worktree Path

Take the worktree path from the pull request number, meeting [Review Worktrees](#review-worktrees).

#### 5. Check an Existing Review Worktree

If the review worktree exists, read its `HEAD` from the repository checkout, using the review worktree path for `<checkout>` and `HEAD` for `<revision>`. If it is absent, continue at [6. Add the Review Worktree](#6-add-the-review-worktree).

```bash
git -C '<checkout>' rev-parse '<revision>^{commit}'
```

After the existing-worktree revision read succeeds, run the following status command for the same path; return a read error before creating or reusing any worktree.

From the repository checkout, read status using the same review worktree path for `<checkout>`.

```bash
git -C '<checkout>' status --porcelain --branch
```

Read both results. Reuse the existing worktree only at the verified head and when its status reports detached HEAD with no tracked or untracked changes.
- Return a status read error.
- Otherwise retain a mismatching or dirty worktree and select an unused path suffixed with the verified commit.

#### 6. Add the Review Worktree

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

For an unused path, add a detached worktree from the repository checkout using that path and the verified fetched commit.

- The path resolves against the directory the command runs in, so supply it as [Review Worktrees](#review-worktrees) anchors it rather than relative to a linked worktree.

```bash
git worktree add --detach '<worktree-path>' '<head-commit>'
```

#### 7. Confirm the Review Worktree Head

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Confirm the selected review worktree’s HEAD.

From the repository checkout, resolve the selected review worktree’s `HEAD`, using its path for `<checkout>` and `HEAD` for `<revision>`.

```bash
git -C '<checkout>' rev-parse '<revision>^{commit}'
```

#### 8. Return the Review Worktree

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the selected detached worktree path and head, or the discrepancy before measuring.

### Read Target Requirements

The protection and active rules governing one target branch.

**Inputs:** [Repository](repository-labels.md#repository), [Target branch](pull-request.md#target-branch), [Requirement paths](#target-requirements)

**Outputs:** [Target requirements](#target-requirements)

#### 1. Fetch the Target Branch Protection

From the repository checkout, save protection using the supplied repository, target branch and destination file.

```bash
gh api 'repos/<owner>/<repo>/branches/<target-branch>/protection' > '<branch-protection-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/branches/main/protection' > protection.json
```

#### 2. Fetch the Target Active Rules

Read the protection response and exit code; retain an inaccessible or absent protection response as unresolved evidence while fetching active rules. A protection 404 alone does not establish the absence of active rules.

From the repository checkout, save active rules using the same repository and target branch and its destination file.

```bash
gh api --paginate 'repos/<owner>/<repo>/rules/branches/<target-branch>' > '<branch-rules-file>'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/rules/branches/main' > branch-rules.json
```

#### 3. Return the Target Requirement Records

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return both records. An unreadable requirement remains unresolved; a protection 404 does not establish the absence of active rules.

### Read Delivery Branches

The configured long-lived branches and existing epic bases.

**Inputs:** [Project checkout](#project-checkout), [Epic prefix](#epic-bases)

**Outputs:** [Long-lived branches](#branches), [Epic bases](#epic-bases)

#### 1. Read the Long-Lived Branch Configuration

From `<workspace>`, read the branch configuration using the supplied project checkout. Missing or empty configuration leaves branch names unevaluable.

- The names meet [Branches](#branches).
- `--project` is any checkout of the project. The names are the ones `config/branches` states in its main working tree, which a linked worktree resolves for itself.
- A missing or empty statement prints `unevaluable:`, names what is missing, and exits 1.

Runs as [Helper invocation](../conventions.md) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py --names --project '<checkout>'
```

#### 2. Read the Epic Base Names

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

#### 3. Return the Delivery Branch Collections

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

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

### Project Checkout

A checkout of the repository whose branches are delivered. Its main working tree holds the [Branches](#branches) statement, and its worktree directory holds every epic-base, task and review worktree.

### Target Requirements

The branch protection and the active rules governing one [target branch](pull-request.md#target-branch), each a local JSON file at its path, with the reviews and checks they require. An unreadable requirement is unresolved.
