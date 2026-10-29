---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Work Item

The local plan for one task's work.

## Operations

### Populate Work Item

One task's local implementation plan.

**Inputs:** [Task id](#identity), [Task scope](epic-issue-body.md#work-breakdown), [Epic context](epic-issue-body.md#template), [Design](#sections), [Component](#component), [Criteria](epic-issue-body.md#acceptance-criteria), [Test requirements](pull-request-body.md#test-coverage), [Work-item path](#identity)

**Outputs:** [Work item](#template)

- Write the supplied task's file from [Template](#template), returning its path for registration in the planning record.
  - Its name and content must meet [Identity](#identity) and [Sections](#sections).
  - The supplied component must meet [Component](#component).
  - The test row must meet [Test Coverage](pull-request-body.md#test-coverage), using the supplied criteria without copying them into the file.

### Read Work Item

The component and test row one task's plan declares.

**Inputs:** [Task id](#identity), [Planning folder](planning-record.md#record-folder)

**Outputs:** [Component](#component), [Test row](#sections)

#### 1. Read the Task Work-Item File

Read the task's file in that folder, named as [Identity](#identity) states.
- Report a missing file to the caller.

#### 2. Return the Component and Test Row

Return its [Component](#component) declaration and the Test row of its Work Breakdown.
- Report a missing declaration or Test row to the caller.

## Fields

### Template

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

### Identity

One file per task, named for its id in lowercase, such as `w01.md`. The record's README links each file. The file names no other task and carries no acceptance criteria, Coverage, dependency or Joins; those belong to the epic table.

### Component

One declaration line ahead of the first heading, naming the single component the Implementation part extends as the path to it in the repository that holds it.

- A task that creates the component names the path it creates.
- A task whose implementation extends more than one component is split into a task for each.

### Sections

- Component names the component the Implementation part extends, meeting [Component](#component).
- Overview states what the task delivers and why.
- Problem and Proposal meet [Problem and Proposal](issue-body.md#problem-and-proposal); the Proposal starts with the scene.
- Work Breakdown decomposes the work into parts, such as analysis, plan, implementation, review and test. Its columns are Part and Description. The test row names the checks required by the work.
