---
prosiform:
  root: ".."
---
# Align Mode

Brings one or more existing proposal, initiative, epic, task, and standalone issues and/or PRs into line with the plan they belong to and structurally aligns them with the guidelines they are held to. 

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md) and ensure all [Outcomes](#outcomes) are met.

## Procedure

1. **Discover every issue.**
   - Scope: issues the user names, an initiative with its open epics or a board with it's complete set of initiatives and epics.
   - Open issues only. A closed issue is aligned only when named.
   - Naming another initiative's issue approves format edits to it.
   - An open standalone issue that an aligned initiative, epic, or task cites is aligned with it.
2. **Fetch each issue.**
   - Use [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue) for its JSON and body.
   - A board fetch includes every initiative it holds.
   - An initiative's fetch includes every epic its table links, closed epics included, as supplied context for validation.
   - A closed epic's own body is checked only when the epic is named.
   - For initiative or epic scope:
     - Apply [Read Requirement Sources](../artifacts/initiative-issue-body.md#read-requirement-sources) with the initiative's References, checkout, authenticated access and destination files, for the epic as for the initiative.
     - Apply [Locate Planning Record](../artifacts/planning-record.md#locate-planning-record) with the initiative's number, and use the record it returns in the steps below.
3. **Repair the format.**
   For each kind among the fetched issues:
   - Apply [Repair Issue Format](../artifacts/issue-body.md#repair-issue-format) with that kind's validator, the fetched context and source evidence as the validator's further inputs, the kind's template, and each fetched issue of that kind with its identity, current JSON and output body path.
     - The validator is [Validate Proposal Body](../artifacts/proposal-body.md#validate-proposal-body), [Validate Initiative Body](../artifacts/initiative-issue-body.md#validate-initiative-body) or [Validate Epic Body](../artifacts/epic-issue-body.md#validate-epic-body), or [Validate Issue Body](../artifacts/issue-body.md#validate-issue-body) with [task field conditions](../artifacts/task-body.md#fields) or [standalone field conditions](../artifacts/standalone-body.md#fields).
   - Carry each cross-body finding and unanswered decision it returns to step 6.
4. **Review the goal.**
   - For initiative or epic scope:
     - Apply [Review Initiative Goal](../artifacts/goal-trace.md#review-initiative-goal) with the current initiative and epic evidence, confirmed goal clauses, marked sources and the epic format results step 3 returned.
     - Apply [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record) with the record identity, folder path, the returned trace table as its [Goal Trace](../artifacts/planning-record.md#goal-trace) and a commit message file, asking it to publish. With no planning record, give the trace table to the user.
   - For proposal, task or standalone scope, apply [Check Round of Edits](../artifacts/issue-body.md#check-round-of-edits) with the selected body, its kind's field conditions and format inputs.
   - Present each finding through [Report Review Finding](../artifacts/review-finding.md#report-review-finding).
   - Carry each confirmed resolution to step 6.
5. **Check criteria.**
   Apply [Check Criteria Quality](../artifacts/acceptance-criteria.md#check-criteria-quality) with each aligned issue body, the initiative's References, checkout, authenticated source access and source destination files.
   - Present each failing criterion, departure and gap it returns through Report Review Finding, proposing the correction [Sources](../artifacts/initiative-issue-body.md#sources) calls for, and for a gap a drafted criterion.
   - For each marked source it could not read, put to the user the choice between a repaired link and a removed mark with the criteria it bound decided with them.
   - Carry each confirmed resolution to step 6.
6. **Resolve content decisions.**
   Decide each finding carried here with the user, and pass its confirmed resolution to the operation that owns the change:
   - **One body.**
     - Apply [Apply Body Corrections](../artifacts/issue-body.md#apply-body-corrections) with the current body, the kind's template and field conditions, related context, the confirmed resolution and output path.
     - For a standalone body, apply [Revise Standalone Body](../artifacts/standalone-body.md#revise-standalone-body).
   - **Task rows.**
     - Pass confirmed task splits and Coverage corrections to [Revise Epic Rows](../artifacts/epic-issue-body.md#revise-epic-rows).
   - **Misplaced Non-Goals.**
     - For an initiative boundary an epic or task states as a Non-Goal, apply Apply Body Corrections to the initiative body with the boundary added to its Non-Goals, and to the epic or task body with the section removed.
   - **Wrong kind.**
     - Put to the user the choice between the body's rewrite to the intended template and its tracker kind and title change.
     - For a rewrite, apply Apply Body Corrections with the intended template.
     - For an epic title change, apply Apply Body Corrections to the initiative body with the epic's row as [Work Breakdown](../artifacts/initiative-issue-body.md#work-breakdown) states it.
   - **One issue under several rows.**
     - Put to the user the choice between one issue per task and a shared reference.
     - For a shared reference, apply Apply Body Corrections to the epic body with the row links removed and the issue cited under its References.
   - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with each returned body and each title, label or kind change. An unanswered decision stays pending.
   - Apply Repair Issue Format again for the affected bodies, as step 3 does.
7. **Check dependencies.**
   For initiative or epic scope:
   - Apply [Check Dependencies and Numbering](../artifacts/dependency-graph.md#check-dependencies-and-numbering) with the initiative and every epic body, the planning record that registered each task row, current pull request records, confirmed numbering maps when any, no allowance, the run's change list and explicitly authorized outside-initiative files.
   - Apply Save Tracker Issue with each checked body it returns that differs from the saved one.
   - Apply Populate Planning Record with the record identity, folder path, the returned longest chains, contending pairs and proposed [Epic Priority](../artifacts/dependency-graph.md#epic-priority) map as its [Dependency Check](../artifacts/planning-record.md#dependency-check) and a commit message file, asking it to publish.
   - Put each unresolved finding it returns to the user.
8. **Record delivery.**
   When no initiative or epic is selected, continue at step 10, Re-run.
   - Apply [Confirm Repository Auto-Close](../artifacts/issue.md#confirm-repository-auto-close) for the repository holding the issues.
   - Follow [Delivery Recording](../protocols/delivery-recording.md) with the selected repositories, initiative prefix, fetched epic JSON and task issue records, project checkout, named instruments, the confirmed setting, no allowance, the run's change list, and output body and comment files.
   - Put each pending or unresolved finding it returns to the user.
   - For an initiative being aligned:
     - Apply [Record Initiative Delivery](../artifacts/initiative-issue-body.md#record-initiative-delivery) with the current initiative JSON, every linked epic's current JSON and an output body file.
     - Apply Save Tracker Issue with the returned body when its Done cells differ from the current one, without asking.
     - Present the returned [Delivery Findings](../artifacts/initiative.md#delivery-findings) to the user.
     - When the user chooses to verify ready criteria now, apply [Record Verified Criteria](../artifacts/acceptance-criteria.md#record-verified-criteria) with the repository, those criterion ids, the current initiative JSON and body, delivery findings, delivery revisions, named instruments, project checkout, output body file and every linked epic record.
     - Report each criterion it refuses or leaves unverified as pending.
9. **Prepare delivery bases.**
   For the open epics of the selected initiative:
   - Follow [Delivery Base Preparation](../protocols/delivery-base-preparation.md) with those epics, the current initiative and epic bodies, prerequisite issue and base-merge records, project checkout, changed long-lived branches, repository, initiative prefix and the pull request records Delivery Recording returned.
   - Put each prerequisite finding, conflict and pull request awaiting a decision it returns to the user.
10. **Re-run.**
    After a published correction:
    - Fetch the changed bodies with Read Tracker Issue.
    - Repeat steps 3–9 for the affected issues.
    - Stop when the checks are clear or every remaining finding is one the user chose to keep. A finding from the criteria check is not one the user keeps. The alignment is not clear while a criterion that fails [Requirement Characteristics](../references/requirement-characteristics.md) remains.

    With or without a correction:
    - Report what changed on each issue, including each finding the criteria check reported, and criterion evidence as [Coverage Reports](../artifacts/issue-body.md#coverage-reports) defines.

## Outcomes

- **Issues brought into line.**
  The issues the user named, or an initiative and its open epics, agree with the plan they state, and the user has decided what still needs a judgement.
- **Delivery brought into line.**
  Each epic's recorded delivery matches the pull requests that landed, and a gap the user accepts is drafted with them.
- **Branches brought into line.**
  Each open epic's branches follow the delivery structure.
