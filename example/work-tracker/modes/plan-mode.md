---
metadata:
  prosiform-group: "modes"
  prosiform-group-depth: "2"
---
# Plan Mode

Scopes the solution: the design, the criteria, and the breakdown of an initiative and its epics, and keeps them current as work lands.

## Prerequisites

Read these files first.

- [Epic Issue Body](../artifacts/epic-issue-body.md)
- [Epic](../artifacts/epic.md)

The caller reached this mode through the routing document [¬ SKILL.md](../SKILL.md), which this procedure defers to a run of its own.

## Procedure

The main path meets [Outcomes](#outcomes).

1. **Populate the epics.**
   Run [Populate Epic Issue Body](../artifacts/epic-issue-body.md#populate-epic-issue-body) for each epic and each new task row.
   - Register each returned file in the planning record.
   - Resolve Open Questions before work starts.
   - Return each epic draft and its format results to the review step.
2. **Publish.**
   - Save the epics in dependency order, each carrying its confirmed priority label.
   - Replace every temporary link in the initiative and epic bodies with the saved issue identity.
   - Call [Validate Epic Body](../artifacts/epic-issue-body.md#validate-epic-body) with the saved initiative context.
   - Resolve findings.
   - Save the corrected bodies.
3. **Record delivered work.**
   When work has landed:
   - Run [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery) with the epic's current evidence.
   - Resolve each line of the returned [Delivery Findings](../artifacts/epic.md#delivery-findings).
   - Return the saved delivery state or blockers.

## Outcomes

- **A scoped initiative.**
  The user has an initiative scoped to the proposal they named, or to a proposal raised for that problem.
- **A goal made true.**
  Each clause of the goal the user confirmed is made true by the initiative's criteria, and the epics the initiative lists are the work that delivers those criteria.
- **Review before creation.**
  Findings on that initiative are folded in before any of its issues are created.
