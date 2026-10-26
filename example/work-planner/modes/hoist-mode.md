---
prosiform:
  root: ".."
---
# Hoist Mode

Brings the chosen standalone issues into the agent-engineering structure, or leaves them open according to the user's decision.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md) and ensure all [Outcomes](#outcomes) are met.

## Procedure

1. **Fetch.**
   Fetch every issue with [Read Repository Issues](../artifacts/issue.md#read-repository-issues).
2. **List candidates.**
   Apply [Find Placement Candidates](../artifacts/placement.md#find-placement-candidates) with the complete issue collection.
   - Use its candidates and available destinations for triage.
3. **Triage.**
   Read each candidate's body and discussion through [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue), with the initiative and epic bodies whose themes or criteria it touches.
   - Apply [Draft Issue Placement](../artifacts/placement.md#draft-issue-placement) with that orphan body, those bodies as candidate destinations, the work it proposes and the planning-record references, and take the options it returns in their order.
4. **Decide each placement.**
   Apply [Settle Plan Change](../artifacts/plan-change.md#settle-plan-change) for each orphan's best option that changes the plan, with the orphan as its subject, that option as the recommended one, the affected issue identities, the allowance the caller supplied and the run's change list.
   - **Applied or answered.**
     - Take the applied option, or the option the user chose, as the confirmed placement.
   - **Held.**
     - Leave the orphan where it is.
   - Where Settle Plan Change puts the option to the user, offer the returned options in their order. The grounding paragraph says what the orphan asks and where it fits.
     - Placing an orphan in another initiative's issue needs that answer as its approval.
   - A best option that leaves the orphan where it is is confirmed as it stands.
   - A caller naming the placement, settled with the user before the hoist, has it applied rather than offered again.
   - Carry the updated change list into the next orphan.
5. **Place.**
   Follow [⇉ Issue Placement](../protocols/issue-placement.md) once for each confirmed placement, with the placement, its current source and destination records, the affected initiative and epic bodies with an output path for each body it changes, the planning record that registered each task row, current pull request records, the confirmed numbering map when there is one, the caller's allowance when it has one, the run's change list, each label's colour and description, and the caller's commit message file when it asks to publish.
   - Carry the change list it returns into the next placement.
   - Keep each blocker and unresolved finding it returns for the report.
6. **Set epic priority.**
   When a placement added an epic, apply [Settle Plan Change](../artifacts/plan-change.md#settle-plan-change) with the [Epic Priority](../artifacts/dependency-graph.md#epic-priority) map Issue Placement returned as a re-prioritisation of each epic whose number it sets or moves, the map as the recommended option, those epics' identities, the caller's allowance and the run's change list.
   - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) for each epic whose confirmed number differs from its priority label, with its identity, the label change that number names, and the label's colour and description.
   - A held map leaves each epic's priority label as it stands.
7. **Review.**
   Apply [Repair Issue Format](../artifacts/issue-body.md#repair-issue-format) once for each kind among the issues the hoist changed or created, with those issues, each with its identity, current JSON and output body path, the kind's template, required related evidence, and the kind's validator:
   - **Initiative.**
     - [Validate Initiative Body](../artifacts/initiative-issue-body.md#validate-initiative-body), with every linked epic JSON and the requirement sources as its further inputs.
   - **Epic.**
     - [Validate Epic Body](../artifacts/epic-issue-body.md#validate-epic-body), with the initiative JSON, current pull request records and the corpus branch as its further inputs.
   - **Task or standalone.**
     - [Validate Issue Body](../artifacts/issue-body.md#validate-issue-body), with the [task](../artifacts/task-body.md#fields) or [standalone](../artifacts/standalone-body.md#fields) field conditions.
   - Keep each blocker and unresolved finding it returns for the report.
8. **Report.**
   Report each orphan's placement, the issues changed, created or closed, the priority labels saved, the orphans left, and each blocker and unresolved finding.
   - Return the [change list](../artifacts/plan-change.md#change-list) with it, so the caller reports each placement this mode made and each it held.

## Outcomes

- **Each orphan placed.**
  The user has each chosen standalone issue joined to an initiative, epic or task, or left open.
- **Cited work included.**
  A standalone issue an agent-engineering issue cites is placed, or taken into the issue that already carries that work.
- **The decision respected.**
  An orphan moves on the user's word, or on the allowance its caller supplied, and work needing a decision outside that allowance stays where it is.
