# Delivery Brief

The instructions and context supplied to one delivery session.

## Prerequisites

Read these files first.

- [Pull Request Body](pull-request-body.md)

## Operations

### *Populate* Delivery Brief

One complete prompt file for a confirmed delivery unit.

**Inputs:** Epic URL, task ids, Descriptions, criteria, test obligations, branch and bases, worktree, reserved folder, engineering worktree, supplied session procedure and output path.

1. Write the supplied identity, context and execution instructions to the prompt file.
   - Each part must meet [Fields](#fields).
2. Return the brief path and any missing context. The caller resolves gaps before dispatch.

## Fields

### Work Identity

The brief names the epic issue URL, task ids, Descriptions and covered acceptance criteria. It includes the selected branch, each epic base and the worktree where the session executes.

### Planning Record

The brief names the reserved planning folder and engineering worktree. Each task has one work-item file, registered in that folder's README. Its row retains the folder link while reserved.

### Validation Scope

The brief carries the tests required by the unit's criteria, meeting [Test Coverage](pull-request-body.md#test-coverage). It identifies the work item's test rows and requires implementation and verification of that scope.

### Execution Instructions

The caller supplies the session procedure and its invocation context. The brief includes that procedure with its planning, publication, merge, debt and arising-issue obligations, plus the confirmed decisions and evidence needed to execute it. A missing instruction or prerequisite is a finding returned to the caller.
