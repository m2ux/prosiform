Material a marked link names is compiled by a sub-agent, as [the dispatch rule](#dispatch) states.

# Plan Mode

Scopes the solution: the design, the criteria, and the breakdown of an initiative and its epics, and keeps them current as work lands.

Follow [Procedure](#procedure). The other sections are material that procedure references. Compile the marked link and hand it to a sub-agent.

## Procedure

1. **Populate the epics.**
   Run [Populate Epic Issue Body](#populate-epic-issue-body) for each epic and each new task row.
   - Register each returned file in the planning record.
   - Resolve Open Questions before work starts.
   - Return each epic draft and its format results to the review step.
2. **Publish.**
   - Save the epics in dependency order, each carrying its confirmed priority label.
   - Replace every temporary link in the initiative and epic bodies with the saved issue identity.
   - Call [Validate Epic Body](#validate-epic-body) with the saved initiative context.
   - Resolve findings.
   - Save the corrected bodies.
3. **Record delivered work.**
   When work has landed:
   - Run [» Record Epic Delivery](artifacts/epic-issue-body.md#record-epic-delivery) with the epic's current evidence.
   - Resolve each line of the returned [» Delivery Findings](artifacts/epic.md#delivery-findings).
   - Return the saved delivery state or blockers.
4. **Verify outcomes met**
   - Ensure each of the [Outcomes](#outcomes) is met.

## Outcomes

- **A scoped initiative.**
  The user has an initiative scoped to the proposal they named, or to a proposal raised for that problem.
- **A goal made true.**
  Each clause of the goal the user confirmed is made true by the initiative's criteria, and the epics the initiative lists are the work that delivers those criteria.
- **Review before creation.**
  Findings on that initiative are folded in before any of its issues are created.

# SKILL

## Work Tracker

### Dispatch

A link whose text opens with `»` names material a sub-agent compiles. Each mode links this section from its preamble, so a bundle of that mode carries it.

## Operations

### *Populate* Epic Issue Body

One epic body and its local validation findings.

**Inputs:** Initiative context, epic scope, draft title and labels, criteria, proposed task rows, available pull request records and output path.

1. Populate the body from the [Template](#template) at the supplied output path.
2. Fill the epic-specific cells.
   - Each row must meet [Work Breakdown](#work-breakdown).
3. Pass the draft, initiative context and output file to [Validate Epic Body](#validate-epic-body).
4. Return the draft rows, their dependency references and the validation findings for the caller's cross-body ordering check.

### *Validate* Epic Body

The body's local format and field findings.

**Inputs:** Epic JSON, initiative context, current pull request records and output file.

1. Check the current body against the local [Fields](#fields), supplying initiative JSON as `--initiative` and pull requests as `--prs`.
2. Include any epic criterion no task row delivers in the findings.
3. Return the corrected body, mechanical diff and unresolved findings for the caller.

## Fields

### Template

````markdown
## Overview

{{One paragraph: what this epic delivers and why it exists within the initiative.}}

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
````

### Work Breakdown

The columns are `Task | Description | Coverage | Depends on | Joins | Done`.

- **Done.**
  A task row is complete when it is delivered, and every criterion its Coverage names is ticked.
- **Row id.**
  The row id is the task, `W01`. `W00` holds preparatory work that must land before the first real task.
- **Coverage.**
  Coverage names the epic's criteria the task must meet. Each row claims only criteria its work makes true; it cannot claim a criterion another row delivers alone or one its work cannot meet. A complete task's cell is empty.
- **Depends on.**
  A task row names the rows it depends on, never an epic. It names the row producing each output it consumes, and where the task consumes from every row of an epic that is what establishes the whole-epic reach.

### Task Delivery

- **Task ids.**
  - Every link on a task row names that row's id, and the row carries one delivery per long-lived branch its unit changes.
  - Once a pull request is open, its link replaces the planning link. A unit changing two long-lived branches links the pull request on each.
  - The task is delivered when a linked pull request has merged, or its id links a commit. A link to an open pull request does not deliver the task.
- **Tasks with their own issue.**
  - A task issue belongs to one epic. Its title carries that epic's prefix.
  - When that epic's table has no row for its id, the issue is unplaced. Once the row exists, that epic's planning manages the issue.
  - The row links the pull request, not the issue.
- **Work another issue takes.**
  It leaves the table. Its criteria go with it, or to another row that delivers them.
