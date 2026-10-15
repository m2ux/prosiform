# Hoist Mode

Brings the chosen standalone issues into the agent-engineering structure, or leaves them open according to the user's decision.

## Prerequisites

Read these files first.

- [Issue](../artifacts/issue.md)
- [Placement](../artifacts/placement.md)
- [Guidelines](../guidelines.md)
- [Issue Body](../artifacts/issue-body.md)
- [Plan Mode](plan-mode.md)
- [Epic Issue Body](../artifacts/epic-issue-body.md)
- [Initiative Issue Body](../artifacts/initiative-issue-body.md)
- [Task Body](../artifacts/task-body.md)
- [Standalone Body](../artifacts/standalone-body.md)

## Procedure

The main path meets [Outcomes](#outcomes).

1. **Fetch.**
   Fetch every issue with [Read Repository Issues](../artifacts/issue.md#read-repository-issues).
2. **List candidates.**
   - Call [Find Placement Candidates](../artifacts/placement.md#find-placement-candidates) with the complete issue collection.
   - Use its candidates and available destinations for triage.
3. **Triage.**
   - Read each candidate's body and discussion through [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue), with the initiative and epic bodies whose themes or criteria it touches.
   - Supply that evidence and planning-record references to [Draft Issue Placement](../artifacts/placement.md#draft-issue-placement) for each option.
   - Present the returned options best first, with Leave last.
4. **Offer.**
   - Offer each orphan as an [Interview](../guidelines.md#modes). The grounding paragraph says what the orphan asks and where it fits.
   - Leave is last.
   - Placing an orphan in another initiative's issue needs that answer as its approval.
   - A caller naming the placement, settled with the user before the hoist, has it applied rather than offered again.
5. **Apply.**
   - Run [Apply Issue Placement](#apply-issue-placement) with each confirmed placement and its current source and destination records.
   - After it returns the saved destination, run exactly one disposition procedure with the returned destination and source records: [Rewrite Orphan Issue](#rewrite-orphan-issue) for kept or left issues, or [Subsume Orphan Work](#subsume-orphan-work) for work taken by another issue.
   - Resume review.
6. **Review.**
   - Run [Validate Issue Body](../artifacts/issue-body.md#validate-issue-body) on every issue the hoist changed or created.
   - Run [Check Dependencies](plan-mode.md#check-dependencies) on each initiative that gained a task or epic.
   - Resolve each finding with the user.
   - Apply confirmed body corrections through [Apply Body Corrections](../artifacts/issue-body.md#apply-body-corrections).
   - Publish through [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue).
   - Repeat Validate Issue Body with the saved affected bodies.
   - Repeat Check Dependencies with the saved affected bodies.
   - Report any unresolved finding.
7. **Report.**
   Report each orphan's placement, the issues changed, created or closed, and the orphans left.

### Apply Issue Placement

One selected destination for an orphan's work.

**Inputs:** Confirmed placement, source issue and body, current destination bodies and planning-record references.

Only the numbered branch matching the confirmed destination executes. Its result is the saved destination and confirmed disposition; the calling apply step performs the rewrite or closure.

1. **Existing task.**
   - Add the orphan's outcomes to the task criteria.
   - Add its design to Proposal.
   - When they exceed the epic's criteria, add epic criteria cited by the task row.
   - Publish the affected bodies through [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue).
   - Return their identities.
2. **New task.**
   - Run [Populate Epic Issue Body](../artifacts/epic-issue-body.md#populate-epic-issue-body) with the confirmed task scope, current epic context and output path.
   - Number the row where it can start.
   - When movable rows change number, run [Check Dependencies and Numbering](plan-mode.md#check-dependencies-and-numbering) with the affected initiative and epic drafts and confirmed numbering map.
   - Publish the checked bodies through Save Tracker Issue.
   - Return the destination epic and row.
3. **New epic.**
   - Run [Populate Epic Issue Body](../artifacts/epic-issue-body.md#populate-epic-issue-body).
   - Populate the covering row through [Draft Initiative Issue Body](../artifacts/initiative-issue-body.md#draft-initiative-issue-body).
   - Publish the epic through [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue).
   - Link its issue in the initiative row.
   - Return the saved destination and confirmed disposition to the caller.
4. **New initiative.**
   - Run [Populate Initiative Issue Body](../artifacts/initiative-issue-body.md#populate-initiative-issue-body) from the orphan's scoped problem and confirmed goal.
   - Publish through [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue).
   - Return the saved destination and confirmed disposition to the caller.
5. **Leave.**
   Return the source issue as the destination with disposition Leave. The caller rewrites its standalone body and keeps the issue open.

### Rewrite Orphan Issue

The selected layout, with the original wording preserved for readers.

**Inputs:** Source issue identity and live body, confirmed kept or left disposition, selected kind, destination context, planning-record references and output body path.

1. **Preserve.**
   - Fetch the body live with [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue).
   - Post it word for word through [Comment on Issue](../artifacts/issue.md#comment-on-issue), preceded by the line in [Original Body](../artifacts/placement.md#original-body) and a blank line.
2. **Populate.**
   - Use the selected [Populate Task Body](../artifacts/task-body.md#populate-task-body), [Populate Epic Issue Body](../artifacts/epic-issue-body.md#populate-epic-issue-body), [Populate Initiative Issue Body](../artifacts/initiative-issue-body.md#populate-initiative-issue-body) or [Populate Standalone Body](../artifacts/standalone-body.md#populate-standalone-body) body.
   - Carry evidence into Problem and design into Proposal.
3. **Publish.**
   - Run [Check Round of Edits](../artifacts/issue-body.md#check-round-of-edits) with the populated body and selected kind conditions before publishing.
   - Resolve findings.
   - Run [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the validated body, title and labels.
   - Return the saved identity to the caller.

### Subsume Orphan Work

The work remains tracked by the taking issue.

**Inputs:** Source issue, confirmed saved destination, transferred outcomes and design, planning-record references and exact closure comment file.

1. **Transfer.**
   - Make each outcome a criterion of one invariant.
   - Put the design in Proposal.
   - Cite the orphan and any planning record in References.
2. **Explain.**
   Prepare the comment file naming the taking issue and task, for example `Tracked in [I07:E01](…/issues/937) W04.` The closure operation records it once.
3. **Close.**
   - Run [Close Transferred Work](../artifacts/issue.md#close-transferred-work) with the orphan identity, confirmed destination evidence and closure comment file, retaining the orphan's body.
   - Return the confirmed closure or blocker to the calling apply step.

## Outcomes

- **Each orphan placed.**
  The user has each chosen standalone issue joined to an initiative, epic or task, or left open.
- **Cited work included.**
  A standalone issue an agent-engineering issue cites is placed, or taken into the issue that already carries that work.
- **The user's choice.**
  An orphan moves only on the user's word, including a placement settled before the hoist.
