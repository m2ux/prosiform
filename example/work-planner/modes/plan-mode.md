---
prosiform:
  root: ".."
---
# Plan Mode

Scopes the solution: the design, the criteria, and the breakdown of an initiative and its epics, and keeps them current as work lands.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md) and ensure all [Outcomes](#outcomes) are met.

## Procedure

### 1. Take the Proposal

- When the user names a proposal, its associated issue body defines the problem scope.
- When the user names an initiative that already exists, fetch its body with [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue). That body defines the problem scope, and no proposal is raised for work it already carries.
- When neither a proposal nor an existing initiative is named:
  - Follow [Propose Mode](propose-mode.md) with the user's goal.
  - Resume this selection step with its published proposal; an unresolved proposal blocks initiative drafting.

### 2. Prepare the Planning Record

- For an initiative, epic or complex plan, apply [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record) with the record identity, folder and supplied evidence files.
- For initiative or epic planning:
  - Populate a discussion body through [Populate Pull Request Body](../artifacts/pull-request-body.md#populate-pull-request-body).
  - Apply [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request) as a draft with the planning branch, target, title and body file. Only the user decides to merge that discussion pull request.

### 3. Draft Each Initiative Body

- For a new initiative, obtain its proposed prefix through [Select Tracker Number](../artifacts/issue.md#select-tracker-number) with the initiative prefix letter.
- Apply [Draft Initiative Issue Body](../artifacts/initiative-issue-body.md#draft-initiative-issue-body) for each initiative with the scoped proposal, confirmed goal clauses, requirement sources, epic summaries and output path.

### 4. Populate the Epics

Apply [Populate Epic Issue Body](../artifacts/epic-issue-body.md#populate-epic-issue-body) for each epic and each new task row.
- Apply [Populate Work Item](../artifacts/work-item.md#populate-work-item) for each task with its scope, design, the component its implementation extends, criteria and test requirements.
- Apply Populate Planning Record with the record identity, folder path and each returned work-item file.
- Apply [Check Dependencies and Numbering](../artifacts/dependency-graph.md#check-dependencies-and-numbering) with the initiative and epic drafts, the planning record, current pull request records, confirmed numbering maps when any, no allowance and the run's change list.
- Apply Populate Planning Record with the record identity, folder path and the returned longest chains, contending pairs and proposed [Epic Priority](../artifacts/dependency-graph.md#epic-priority) map as its [Dependency Check](../artifacts/planning-record.md#dependency-check).
- Return each checked epic draft and its format results to the review step.

### 5. Review the Drafts

Apply [Review Initiative Goal](../artifacts/goal-trace.md#review-initiative-goal) with the initiative and epic drafts, confirmed goal clauses, marked sources and the epic format results.
- Apply Populate Planning Record with the record identity, folder path and the returned trace table as its [Goal Trace](../artifacts/planning-record.md#goal-trace). With no planning record, give the trace table to the user.
- Apply [Report Review Finding](../artifacts/review-finding.md#report-review-finding) for each returned finding, with its scope, evidence and proposed resolution.
- Apply each confirmed resolution to the drafts:
  - For a local epic finding, apply Populate Epic Issue Body with the confirmed Proposal, row and criterion changes, including every new or renumbered criterion in Coverage.
  - For a confirmed distinct concern:
    - Apply Populate Epic Issue Body for its own epic.
    - Apply Draft Initiative Issue Body with the epic summaries that include it.
    - Repeat Check Dependencies and Numbering for the new epic and initiative row, and record its result as step 4 does.
- Apply Populate Planning Record with the record identity, folder path and each finding, resolution and decision.
- Repeat Review Initiative Goal with the revised initiative and epic bodies and retained goal clauses and sources. No issue is created while a content or structural finding remains. Unresolved links to unpublished issues are recorded with their intended row identities and resolved during publication; no other finding is deferred.

### 6. Publish

Put the proposed [Epic Priority](../artifacts/dependency-graph.md#epic-priority) map for the reviewed epics to the user as an [interview](../rules.md), the proposal the recommended answer.
- Take the positive integer the user confirms for each epic.
- Follow [Initiative Publication](../protocols/initiative-publication.md) with the repository, initiative prefix letter, the reviewed initiative and epic body files with their existing issue numbers, titles and labels, each epic's confirmed [priority label](../artifacts/board-queue.md#priority-sets) among them, each label's colour and description, the current pull request records, corpus branch and requirement sources, the kind templates, the record identity, folder path, evidence and decisions, and a commit message file.
- Put each blocker it returns to the user.

### 7. Keep the Goal Current

When the goal, a criterion, a Problem, a Proposal or an epic changes:
- Repeat Review Initiative Goal with the revised bodies and current sources, and record its trace table as step 5 does.
- Apply Report Review Finding for each finding.
- Apply confirmed resolutions as step 5 does.
- Repeat that review until clear.
- After each round, apply [Check Round of Edits](../artifacts/issue-body.md#check-round-of-edits) to affected bodies.
- Whenever tasks, edges or a work item's component change, repeat Check Dependencies and Numbering, and record its result as step 4 does.
  - Put the proposed Epic Priority map to the user again where the edges or the contention moved an epic's number.
  - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with each confirmed change as that epic's [priority label](../artifacts/board-queue.md#priority-sets), with its colour and description.
- Apply Save Tracker Issue with each affected body, its title matching current numbers.
- Keep local body files as the source for the next pass.
- Apply Populate Work Item for each added or renamed task.
- Apply Populate Pull Request Body with the discussion pull request's current body.
- Apply Publish Pull Request with the discussion pull request's number and the returned body file.
- Apply Populate Planning Record with the record identity, folder path, each added or renamed task's work-item file, each removed task's work-item file as removed, and a commit message file, asking it to publish.

### 8. Prepare Epic Delivery

Before any task starts:
- Apply [Resolve Open Questions](../artifacts/issue-body.md#resolve-open-questions) for each affected issue with its identity, current JSON, its kind's template and field conditions, related context and an output body path.
  - Apply Populate Planning Record with each decision it returns.
  - Stop on a question it leaves open.
- Apply [Apply Body Corrections](../artifacts/issue-body.md#apply-body-corrections) to each body with a criterion joining several conditions, with the split criteria at the end of the list and their Coverage as [Shared Acceptance Criteria](../artifacts/issue-body.md#shared-acceptance-criteria) states.
  - Apply Save Tracker Issue with each returned body.
- Follow [Delivery Base Preparation](../protocols/delivery-base-preparation.md) with the initiative's epics, the current initiative and epic bodies, prerequisite issue and base-merge records, project checkout, changed long-lived branches, repository and initiative prefix.
  - Stop on a prerequisite finding it returns.
  - Put each conflict and pull request awaiting a decision it returns to the user.
- Repeat goal and ordering review on changed bodies, as step 7 does, before returning readiness.

### 9. Record Delivered Work

When work has landed:
- Follow [⇉ Sync Mode](sync-mode.md) for the affected initiative.
- For each unplaced task row it returns pending:
  - Apply [Place Unplaced Task Row](../artifacts/epic-issue-body.md#place-unplaced-task-row) with the epic JSON, that task issue, no allowance, the returned change list and delivery evidence, and an output body file.
  - Repeat Sync Mode with the refreshed epic.
- Return the saved delivery state or blockers.

## Outcomes

- **A scoped initiative.**
  The user has an initiative scoped to the proposal they named, or to a proposal raised for that problem.
- **Several initiatives.**
  One proposal may become several initiatives. A partition by solution maturity, such as an MVP demo, a functional prototype, and a production-intent version, is an example of that result. Those initiatives may run in series or in parallel. The example does not limit the partition.
- **A goal made true.**
  Each clause of the goal the user confirmed is made true by the initiative's criteria, and the epics the initiative lists are the work that delivers those criteria.
- **Epics that start together.**
  The user has settled which of the initiative's epics start alongside each other, from a proposal the dependency graph makes.
- **Review before creation.**
  Findings on that initiative are folded in before any of its issues are created.
