---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Task Body

Populates one task body.

## Operations

### Populate Task Body

One task body within its supplied epic context.

**Inputs:** [Task scope](#task-scope), [Epic body](epic-issue-body.md#template), [Output body path](issue-body.md#body-file)

**Outputs:** [Task body](#template)

- Populate the body from the [Template](#template) at the supplied output path.
  - The title must meet the shared [Titles](issue-body.md#titles) conditions.
  - The Problem and Proposal must meet [Problem and Proposal](issue-body.md#problem-and-proposal).
  - Acceptance criteria must meet the [shared acceptance criteria](issue-body.md#shared-acceptance-criteria).
  - All populated fields must meet [Fields](#fields), including the required [Sections](#sections).

### Record Task Delivery

One task body with its confirmed delivery and verified criteria recorded.

**Inputs:** [Task issue](issue.md#issue-record), [Pull request records](pull-request.md#pull-request-records), [Issue-link snapshot](pull-request.md#issue-link-snapshot), [Delivering pull request](pull-request.md#pull-request-identity), [Verified criterion ids](acceptance-criteria.md#criterion), [Output body path](issue-body.md#body-file), [Comment path](issue.md#issue-comment)

**Outputs:** [Task delivery result](#task-delivery-result)

#### 1. Sync the Task Issue

From `<workspace>`, update the task JSON with records as `--prs`, snapshot as `--links`, delivering pull request number as `--pr`, verified criterion ids as `--tick` and output body file as `--fix`. Tick only criteria the caller has verified.

`<criterion-ids>` is a comma-separated list of verified criterion ids.

Runs as [Helper invocation](../conventions.md) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<task-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --pr '<pull-request-number>' --tick '<criterion-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-637.json --prs prs.json --links links.json --pr 950 --tick AC1 --fix fixed-637.md
```

#### 2. Write the Delivery Comment

Read the helper’s exit code, output and written body. Return an invocation failure before writing the comment, retaining any eligibility findings.

Write `Delivered by #<pull-request-number>.` to the output comment file, with the delivering pull request number.

#### 3. Return the Task Delivery Result

Return the body, the comment file and the eligibility findings. The caller saves the body, posts the comment file through [Comment on Issue](issue.md#comment-on-issue) and closes the tracker issue.

## Fields

### Template

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

### Titles

- The title is `[I07:E00:W01] Name: Subtitle`.
- The label is the task [kind label](../configuration.md#kind-labels).
- `W` is the task within the epic. Tasks count from `W01`.

### Open Questions

- Each holds only what is undecided, and is resolved before the task starts.

### Acceptance Criteria

- A task criterion meets the [shared acceptance criteria](issue-body.md#shared-acceptance-criteria).

### Sections

- A task has the [epic issue body](epic-issue-body.md)'s sections without the Work Breakdown table.
- New task planning follows [Work Breakdown](epic-issue-body.md#work-breakdown). This body describes an existing issue kept as a task.

### Task Scope

The work one task delivers within its epic: its problem, design and acceptance criteria, as the [Template](#template) sections hold them.

### Task Delivery Result

One task's delivery as recorded: the body with its delivering pull request and verified criteria ticked, a comment file reading `Delivered by #<pull-request-number>.`, and the eligibility findings stating whether the task is closable.
