# Plan Mode

Scopes the solution: the design, the criteria, and the breakdown of an initiative and its epics, and keeps them current as work lands.

## Prerequisites

Read these files first.

- [Propose Mode](propose-mode.md)
- [Planning Record](../artifacts/planning-record.md)
- [Pull Request Body](../artifacts/pull-request-body.md)
- [Pull Request](../artifacts/pull-request.md)
- [Issue](../artifacts/issue.md)
- [Initiative Issue Body](../artifacts/initiative-issue-body.md)
- [Epic Issue Body](../artifacts/epic-issue-body.md)
- [Work Item](../artifacts/work-item.md)
- [Repository Labels](../artifacts/repository-labels.md)
- [Task Body](../artifacts/task-body.md)
- [Issue Body](../artifacts/issue-body.md)
- [Epic](../artifacts/epic.md)
- [Delivery Branches](../artifacts/delivery-branches.md)
- [Sync Mode](sync-mode.md)
- [Review Finding](../artifacts/review-finding.md)

## Procedure

The main path meets [Outcomes](#outcomes).

1. **Take the proposal.**
   - When the user names a proposal, its associated issue body defines the problem scope.
   - When no proposal is named:
     - Run [Propose Mode](propose-mode.md) with the user's goal.
     - Resume this selection step with its published proposal; an unresolved proposal blocks initiative drafting.
2. **Prepare the planning record.**
   - For an initiative, epic or complex plan, call [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record) with the record identity, folder and supplied evidence files.
   - For initiative or epic planning:
     - Populate a discussion body through [Populate Pull Request Body](../artifacts/pull-request-body.md#populate-pull-request-body).
     - Run [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request) as a draft with the planning branch, target, title and body file. Only the user decides to merge that discussion pull request.
3. **Draft each initiative body.**
   - For a new initiative, obtain its proposed prefix through [Select Initiative Number](../artifacts/issue.md#select-initiative-number).
   - Run [Draft Initiative Issue Body](../artifacts/initiative-issue-body.md#draft-initiative-issue-body) for each initiative with the scoped proposal, confirmed goal clauses, requirement sources, epic summaries and output path. The epics' acceptance criteria carry the detail that makes the initiative's criteria true.
4. **Populate the epics.**
   Run [Populate Epic Issue Body](../artifacts/epic-issue-body.md#populate-epic-issue-body) for each epic and each new task row.
   - Call [Populate Work Item](../artifacts/work-item.md#populate-work-item) for each task with its scope, design, criteria and test requirements.
   - Register each returned file in the planning record.
   - Resolve Open Questions before work starts.
   - Run [Check Dependencies and Numbering](#check-dependencies-and-numbering) across the drafts.
   - Return each epic draft and its format results to the review step.
5. **Review the drafts.**
   Follow [Review Initiative Goal](#review-initiative-goal).
   - Run [Report Review Finding](#report-review-finding) for each returned finding, with its scope, evidence and proposed resolution.
   - Apply each confirmed resolution to the drafts:
     - For a local epic finding, call Populate Epic Issue Body with the confirmed Proposal, row and criterion changes, including every new or renumbered criterion in Coverage.
     - For a confirmed distinct concern:
       - Draft its own epic and initiative row.
       - Repeat ordering review for the new epic and initiative row.
   - Record the finding, resolution and decision in the planning record.
   - Repeat Review Initiative Goal with the revised initiative and epic bodies and retained goal clauses and sources. No issue is created while a content or structural finding remains. Unresolved links to unpublished issues are recorded with their intended row identities and resolved during publication; no other finding is deferred.
   - An acceptance criterion is created only once it meets [Initiative Acceptance Criteria](../artifacts/initiative-issue-body.md#initiative-acceptance-criteria).
6. **Publish.**
   Call [Ensure Repository Labels](../artifacts/repository-labels.md#ensure-repository-labels) with the required definitions before saving the issues.
   - For a new initiative:
     - Call [Select Initiative Number](../artifacts/issue.md#select-initiative-number).
     - Save it through [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue), using temporary epic-row links until issue identities exist.
     - Save the epics in dependency order.
     - Replace every temporary link in the initiative and epic bodies with the saved issue identity.
     - Confirm no unresolved epic placeholder remains.
   - For each task needing its own discussion or evidence:
     - Call [Populate Task Body](../artifacts/task-body.md#populate-task-body).
     - Validate it against its kind's fields.
     - Save the task issue.
   - Call [Validate Epic Body](../artifacts/epic-issue-body.md#validate-epic-body) with the saved initiative context.
   - Call [Validate Initiative Body](../artifacts/initiative-issue-body.md#validate-initiative-body) with every saved epic.
   - Resolve findings.
   - Save the corrected bodies.
   - Update the planning record with evidence, decisions and issue links.
7. **Keep the goal current.**
   When the goal, a criterion, a Problem, a Proposal or an epic changes:
   - Repeat Review Initiative Goal with the revised bodies and current sources.
   - Run Report Review Finding for each finding.
   - Apply confirmed resolutions.
   - Repeat that review until clear.
   - After each round, run [Check Round of Edits](../artifacts/issue-body.md#check-round-of-edits) on affected bodies.
   - Whenever tasks or edges change, repeat Check Dependencies and Numbering.
   - Save affected bodies through Save Tracker Issue, matching titles to current numbers and Coverage to current criteria.
   - Keep local body files as the source for the next pass.
   - Update work-item files and the README inventory for added, renamed or removed tasks.
   - Update the discussion pull request body and planning record.
   - Commit.
   - Push.
8. **Prepare epic delivery.**
   Before any task starts:
   - Resolve every Open Question with the user.
   - Record the answer.
   - Update the affected bodies, removing each settled question.
   - Split multi-condition criteria at the end of the list.
   - Update Coverage for the split criteria.
   - Run [Check Epic Prerequisites](../artifacts/epic.md#check-epic-prerequisites) with current initiative and prerequisite evidence; stop on a failed or incomplete result.
   - After prerequisites pass, call [Prepare Delivery Bases](../artifacts/delivery-branches.md#prepare-delivery-bases).
   - Run [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request) to retarget each affected open task pull request to its epic base.
   - Repeat goal and ordering review on changed bodies before returning readiness.
9. **Record delivered work.**
   When work has landed:
   - Run [Sync Mode](sync-mode.md) for the affected initiative.
   - For an unplaced task issue:
     - Add its row through Populate Epic Issue Body.
     - Save that body.
     - Repeat Sync Mode with the refreshed epic.
   - Return the saved delivery state or blockers.

### Report Review Finding

The verified findings presented for resolution.

1. **Prepare.**
   Call [Populate Review Finding](../artifacts/review-finding.md#populate-review-finding) with the area, severity, problem, solution and source evidence.
   - Resolve any evidence gap before reporting it.
   - Group the returned findings by area.
2. **Decide.**
   Put each pending decision to the user, one question at a time.
   - Wait for the answer.
   - Record the confirmed answer on the finding.
   - Return each confirmed resolution to the calling procedure for application to its selected issue kind. A pending decision returns without applying a change.

### Check Dependencies and Numbering

The task graph and the row numbers it permits.

1. **Check.**
   - Use the supplied local drafts when reviewing unpublished work.
   - For published issues, fetch the initiative and each epic body with [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue).
   - Run [Check Dependencies](#check-dependencies) with the initiative body and every epic body.
2. **Correct.**
   Resolve each finding with the user.
   - Preserve task edges when correcting a whole-epic edge.
   - Name the producing row for each consumed output.
   - Retain a whole-epic edge only when every prerequisite row is required.
   - Read tasks for implied consumption edges.
   - Account for every independent pair in Joins or the planning record.
   - Resolve backward references by moving work to the epic owning its inputs, or removing duplicate work already owned there. Work claimed twice has one owner and a boundary in both bodies.
3. **Renumber.**
   Preserve numbers already named by pull requests.
   - For a confirmed epic map, run [Renumber Epics](#renumber-epics) with current pull request records and every affected body.
   - For a confirmed task map, run [Renumber Tasks](#renumber-tasks) with the initiative and epic identities, owning epic body, confirmed old-to-new task-number map and every affected body file.
   - Re-sort rewritten tables.
   - Inspect every reported range.
   - Search prose for references the script cannot see.
   - Repeat Check Dependencies after each edge or numbering change until it reports no problem.
   - Record the printed longest chains and each binding whole-epic edge in the planning record.
   - Return the checked bodies and unresolved findings to the caller; do not publish a failed renumbering.

### Review Initiative Goal

The draft checked against the initiative outcomes.

1. **Clauses.**
   Take the goal the user stated and confirmed, as clauses, each an outcome someone could observe.
2. **Trace.**
   Build a trace table: goal clause, the initiative criteria that make it true, the epics whose Coverage cells cite those criteria, and the epic criteria that deliver them.
   - Every goal clause has an initiative criterion that makes it true.
   - Every initiative criterion is delivered by an epic, and that epic's criteria make the criterion wholly true.
   - Every initiative criterion traces to a goal clause.
   - Remove one that traces to none, or put that scope to the user.
   - Record any criterion no task row delivers as a gap from the supplied epic format results.
3. **Align.**
   Call [Read Requirement Sources](../artifacts/initiative-issue-body.md#read-requirement-sources) with the initiative References, checkout, authenticated access and output files.
   - Extend the trace table with the source requirement each criterion answers to. Each unmatched requirement, each criterion that departs from the one it cites, and each source that could not be read is a gap [Sources](../artifacts/initiative-issue-body.md#sources) names.
4. **Criteria.**
   Check each criterion against the [shared acceptance criteria](../artifacts/issue-body.md#shared-acceptance-criteria) and [Initiative Acceptance Criteria](../artifacts/initiative-issue-body.md#initiative-acceptance-criteria).
5. **Validate the body.**
   Call [Build Body Snapshot](../artifacts/issue-body.md#build-body-snapshot) for each supplied local draft with its title, labels and existing identity when present.
   - Use the returned initiative and epic JSON for [Validate Initiative Body](../artifacts/initiative-issue-body.md#validate-initiative-body) with the initiative JSON, every linked epic's current JSON, source evidence and output file.
   - Incorporate its local findings into this review.
6. **Outside threats.**
   Follow [Check Outside Threats](#check-outside-threats).
7. **Rank.**
   Rank the gaps.
   - Flag the few that most threaten the goal.
   - Record the trace table in the planning record, or give it to the user when the change has none.
   - Return the trace and ranked findings to the calling review step.

### Check Outside Threats

An item the draft leaves open is a gap.

1. **Consumers.**
   Check for anything outside the plan that reads, builds or ships what the plan changes or removes.
2. **Silent failures.**
   Check for a skip, a fallback, or a fail-closed path that hides a violation.
3. **Measurement.**
   Check that done has a threshold, a baseline, and an instrument that is independent of the thing measured. The baseline is fixed before the plan changes what it measures.
4. **Version skew.**
   Check for skew between an artifact the plan produces and an implementation that reads it.
5. **In-flight work.**
   - Check for a change elsewhere that alters the ground the plan stands on.
   - Return the evidenced threats and gaps to Review Initiative Goal.

## Outcomes

- **A scoped initiative.**
  The user has an initiative scoped to the proposal they named, or to a proposal raised for that problem.
- **Several initiatives.**
  One proposal may become several initiatives. A partition by solution maturity, such as an MVP demo, a functional prototype, and a production-intent version, is an example of that result. Those initiatives may run in series or in parallel. The example does not limit the partition.
- **A goal made true.**
  Each clause of the goal the user confirmed is made true by the initiative's criteria, and the epics the initiative lists are the work that delivers those criteria.
- **Review before creation.**
  Findings on that initiative are folded in before any of its issues are created.

## Operations

### Check Dependencies

Checks the task dependency graph across the epics given, and with `I=` the initiative's Depends on cells.

**Inputs:** Initiative body file and each epic id with its body file.

- Keep `I=` for the initiative. Repeat the `<epic-id>=<epic-body-file>` argument once per epic.

- Initiative edges follow the [whole-epic prerequisite rule](../artifacts/initiative-issue-body.md#work-breakdown); narrower dependencies stay in the task graph.
- It also reports dependencies listed twice or already implied, and Joins pairs.
- It prints each pair of tasks in an epic where neither depends on the other and the two do not name each other in Joins.
- It prints each whole-epic dependency with that epic's row count, the binding row and its level, and the earliest row and its level.
- It reads bodies from [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue), or local drafts.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deps.py 'I=<initiative-body-file>' '<epic-id>=<epic-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deps.py I=live-936.md E00=live-943.md E01=live-937.md
```

### Renumber Tasks

Renumbers one epic's tasks by the map given, in the files given.

**Inputs:** Initiative number, epic number, epic body file, task-number map and affected body files.

- `<task-number-map>` is a comma-separated list of `<old-number>:<new-number>` pairs. Pass each affected body file as a separate argument.

- It renumbers `<epic-id> Wxx` and `<epic-id>:Wxx` everywhere, and bare `Wxx` inside that epic's own body. **Example:** for `E01`, the qualified forms are `E01 Wxx` and `E01:Wxx`.
- The map assigns each old task number a distinct new number. A source absent from the files or a duplicate destination is refused.
- Append `--outside` followed by each explicitly authorized outside-initiative body file when supplied; only this initiative's prefixed references change there.
- Only rows no pull request names may be renumbered. Inspect the rewritten files before publishing them.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/renumber.py --initiative '<initiative-number>' --epic '<epic-number>' --own '<epic-body-file>' --tasks '<task-number-map>' '<affected-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/renumber.py --initiative 07 --epic 1 --own live-937.md --tasks 7:3,3:5 live-*.md
```

### Renumber Epics

Renumbers an initiative's epics across supplied body files.

**Inputs:** Initiative number, current pull request records, confirmed epic-number map, body files and explicitly authorized outside-initiative files when present.

- The map is a comma-separated list of `<old-number>:<new-number>` pairs. Pass each body file as a separate argument; append `--outside` followed by each outside-initiative file when supplied.
- Files are rewritten in place. Outside files change only references carrying this initiative's prefix; links retain their targets. A collision or a number already named by a pull request is refused.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/renumber.py --initiative '<initiative-number>' --prs '<pull-request-records-file>' --map '<epic-number-map>' '<body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/renumber.py --initiative 07 --prs prs.json --map 6:0,0:1 live-936.md live-943.md
```
