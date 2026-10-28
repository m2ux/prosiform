---
prosiform:
  root: ".."
---
# Propose Mode

Scopes one problem: the friction, the evidence, and the boundary, and states the goal as clauses the user confirms. It raises one proposal on the [proposals board](../configuration.md#proposals-board).

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md) and ensure all [Outcomes](#outcomes) are met.

## Procedure

### 1. Understand the Problem

Ask the user until the friction and the boundary are clear.
- State the goal back as clauses meeting [Goal](../artifacts/proposal-body.md#goal).
- Have the user confirm those clauses.

### 2. Gather Evidence

- Measure the current state: counts, paths, and file:line.
- Delegate broad sweeps to parallel sub-agents.
- Spot-check what they return before recording it.

### 3. Draft the Body

Apply [Populate Proposal Body](../artifacts/proposal-body.md#populate-proposal-body) with the confirmed problem, evidence, goal clauses, boundary and output body path. The local file is the source for the issue.
- Obtain the proposal's number through [Select Tracker Number](../artifacts/issue.md#select-tracker-number) with the proposal prefix letter, and carry it in the title.
- The goal clauses are the clauses the user confirmed. The Non-Goals are the boundary.
- The design, the acceptance criteria, and the breakdown belong to a later goal.

### 4. Validate

Apply [Build Body Snapshot](../artifacts/issue-body.md#build-body-snapshot) with the body file, title, labels and a JSON path.
- Apply [Validate Proposal Body](../artifacts/proposal-body.md#validate-proposal-body) with the returned JSON and the output file.
- Resolve each finding it leaves unresolved in the problem, evidence, goal clauses or boundary, and repeat Populate Proposal Body with them and the same output path.
- Repeat Build Body Snapshot and Validate Proposal Body with the revised body and the same paths. Proceed to publication only when validation passes.

### 5. Publish

Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the repository, the validated body file, its title, the proposal's labels and each label's colour and description, leaving it unassigned.

### 6. Confirm Placement

Ask whether to add the issue to the proposals board.
- On acceptance, continue to [7. Place](#7-place).
- On a decline, skip placement and continue to [8. Report](#8-report) with the issue URL.
- Wait for an unanswered decision.

### 7. Place

Apply [Ensure Project Board](../artifacts/board.md#ensure-project-board) with the board owner, the repository and the proposals-board selection.
- Apply [Place Issue on Board](../artifacts/board.md#place-issue-on-board) with the returned owner and board number, the repository, the saved issue number, an output file and initial status Suggested.
- Leave the issue unassigned.

### 8. Report

Give the issue's URL, and the board's when the issue was placed.

## Outcomes

- **A scoped problem.**
  The user has one problem scoped, and has confirmed its goal.
- **One proposal.**
  The user has that problem raised as one proposal.
- **On the proposals board.**
  When the user wants the proposal on the proposals board, it is there, raised, and unassigned.
