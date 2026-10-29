---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Planning Record

A planning record is a folder. README.md is its entry point: it answers what the work is, and links to every other artifact the plan produces. Each artifact is the home of its own content. The progress of the work is the theme's project board.

## Operations

### Populate Planning Record

One planning directory and its artifact inventory.

**Inputs:** [Record identity](#record-folder), [Folder path](#record-folder), [Artifact files](#artifacts), [External links](#links), [Removed artifacts](#artifacts), [Commit message](#commit-message)

**Outputs:** [Folder path](#record-folder), [Publication](#publication)

#### 1. Prepare the Selected Planning Record

For a new record, run this command from the engineering worktree with the caller-composed [Record Folder](#record-folder) path.

```bash
mkdir -p '<planning-folder-path>'
```

**Example:**

```bash
mkdir -p artifacts/planning/2026-10-15-950-queue-plan
```

#### 2. Populate the Record Entry Point

For a new record, inspect the folder-creation result. Return any error without writing or publishing further files. On success, populate README.md from the [Template](#template).

For an existing record, read its README, retaining its creation date, other artifacts and links.
- Update only the supplied content.

For either kind of record, the folder must meet [Layout](#layout), and every populated README field must meet [Fields](#fields).

#### 3. Register the Supplied Artifact Files

Register the artifact files supplied by the caller, using their chosen names.
- Each file must have a row meeting [Layout](#layout) and [Artifacts](#artifacts).
- File content remains supplied by the caller; this operation does not author that artifact's content.
- Delete each artifact the caller names as removed, with its row.

#### 4. Publish the Populated Planning Record

When the caller asks to publish, apply [Publish Planning Record](#publish-planning-record) with the folder path, the files this call wrote and the commit message file.

#### 5. Return the Planning Record Folder

Return the folder path, and the publication result when it published.

### Publish Planning Record

The record's folder committed and pushed, so every link into it resolves for a reader.

**Inputs:** [Folder path](#record-folder), [Record files](#layout), [Commit message](#commit-message)

**Outputs:** [Publication](#publication)

#### 1. Find the Publishing Worktree

From any project checkout, list the worktree for the configured [engineering branch](../configuration.md#engineering-branch).

- The engineering branch has one long-lived worktree and takes no further one.

```bash
git worktree list | grep '\[<engineering-branch>\]'
```

#### 2. Commit the Planning Record Folder

Inspect the worktree lookup. Return a lookup error or missing-worktree finding before any write. Use the returned path as `<engineering-worktree>`.

Stage and commit the supplied folder with the supplied message file. Resolve the message file against the engineering worktree, or pass its absolute path.

- Staging and committing are one call, and the commit names its folder, so a concurrent session's staged work cannot ride along. See [Shared Worktree](#shared-worktree).
- Pass the message as [Bodies](../conventions.md) states. The worktree is a linked one, so git writes here run unsandboxed.

```bash
cd '<engineering-worktree>' && git add '<planning-folder-path>' && git commit -F '<message-file>' -- '<planning-folder-path>'
```

**Example:**

```bash
cd .engineering && git add artifacts/planning/2026-10-15-950-queue-plan && git commit -F msg.txt -- artifacts/planning/2026-10-15-950-queue-plan
```

#### 3. Push the Engineering Branch

Inspect the commit result; return a failure without pushing. Confirm the commit holds the files this record wrote, meeting [Shared Worktree](#shared-worktree), then push from the engineering worktree.

- Planning records go straight to the branch; they take no pull request.

```bash
cd '<engineering-worktree>' && git push
```

#### 4. Return the Publication Result

Inspect the push result. Report a non-fast-forward refusal or other push failure without rewriting the branch. Return the published commit and record path only after a successful push.

### Locate Planning Record

The existing planning folder whose reference is one issue or pull request number.

**Inputs:** [Reference](#record-folder)

**Outputs:** [Folder paths](#record-folder)

#### 1. Find the Engineering Worktree

From any project checkout, list the worktree for the configured [engineering branch](../configuration.md#engineering-branch).

- The engineering branch has one long-lived worktree and takes no further one.

```bash
git worktree list | grep '\[<engineering-branch>\]'
```

#### 2. List the Matching Planning Records

Inspect the worktree lookup. Return a lookup error or missing-worktree finding before continuing. In the returned worktree, list folders under its configured [records folder](../configuration.md#engineering-branch) with the supplied reference number.

- The pattern places the reference directly after the date, as the [planning-folder path](#record-folder) does, so a number inside the date does not match.

```bash
cd '<engineering-worktree>' && ls -d '<records-folder>'????-??-??-'<reference>'-*/
```

**Example:**

```bash
cd .engineering && ls -d artifacts/planning/????-??-??-950-*/
```

#### 3. Return the Matching Record Paths

Inspect the listing's exit code and output. Return each matching folder path. If the pattern has no match, return that no record has the reference; report any other listing failure as an execution error.

## Fields

### Template

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

### Shared Worktree

The engineering branch has one worktree and every session writes its records there, so they share one index. A commit therefore names the folder it is for, and a session confirms its own files landed in its own commit rather than assuming the index held only its staging.

### Layout

README.md is the one file the folder must hold. Any file beyond README.md is added as the work needs it.

```text
./
├── README.md
└── …
```

Each file beyond README.md is a row in the README's Artifacts.

An overview record explains one pull request's change. Its folder's reference is the pull request number and its slug comes from the pull request's title. A pull request has one overview record, and a later overview of it reuses that folder.

### Header

One blockquote: the classifier, the day the record was created, and a revised date when the README is updated after the work is done.

### Executive Summary

Two paragraphs: the purpose of this work, and why it matters.

### Artifacts

- One row for every artifact in the record other than README.md, added when the file is produced and removed with it.
- The link sits on the artifact's name. The row says what the artifact holds, and the artifact is the home of that content.
- In an overview record, the architecture overview is the one row, and its pull request is under Links.

### Dependency Check

`dependencies.md`, an Artifacts row: the longest chains, contending pairs and proposed epic priority map the initiative's latest dependency check printed. A later check replaces it.

### Goal Trace

`goal-trace.md`, an Artifacts row: the trace table of the initiative's latest goal review. A later review replaces it.

### Links

External references only: a tracker issue, a parent epic, a pull request. An artifact of this plan is an Artifacts row.

### Record Folder

- `<planning-folder-path>` is `<records-folder><yyyy-mm-dd>[-<ref>]-<slug>/`, under the [records folder](../configuration.md#engineering-branch). The date is the day the record is opened.
- `<ref>` is the bare number of the issue or the pull request the record is for. A record for ad hoc work, which has neither, has no ref segment.
- The slug is lowercase words separated by hyphens, a short name of the work.
- The folder's files are the [planning layout](planning-record.md#layout).
- Edits are made on that worktree. The engineering branch takes no further worktree and no branch.

One planning record's folder, at `<records-folder><yyyy-mm-dd>[-<ref>]-<slug>/` under the [records folder](../configuration.md#engineering-branch). The date is the day the record opened. The reference is the bare number of the issue or pull request the record is for, absent for ad hoc work. The slug is lowercase hyphenated words naming the work. The folder's name is the record identity.

### Commit Message

A file holding the message of the commit that publishes the record, as [Bodies](../conventions.md) states.

### Publication

The engineering-branch commit holding the record's folder, pushed to its remote.
