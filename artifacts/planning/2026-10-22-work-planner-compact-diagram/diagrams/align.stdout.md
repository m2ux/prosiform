This bundle was built for [Align Mode](#align-mode); everything else is material it references.

# Artifacts

## Overview

### Epic Issue Body

Populates one epic body. The body states one slice of the design and lists the tasks that deliver it.

### Planning Record

A planning record is a folder. README.md is its entry point: it answers what the work is, and links to every other artifact the plan produces. Each artifact is the home of its own content. The progress of the work is the theme's project board.

## Operations

### Acceptance Criteria

#### *Verify* Selected Criteria

The verification evidence for a supplied set of criteria whose delivery is ready.

**Inputs:** Criterion ids, current issue body, delivery findings, delivery revisions, named instruments and the project checkout to run them in.

1. Confirm the supplied delivery findings establish [Readiness](#readiness) for each selected criterion.
   - Return an undelivered or unreadable dependency as a blocker for that criterion.
2. Check out each branch the delivering pull requests merged into, in the supplied project checkout, meeting [Instrument Checkout](#instrument-checkout).
   - Run each criterion's named instrument there.
   - Record the result against the tested revisions, meeting [Instrument Result](#instrument-result).
3. Return verified criterion ids with their evidence and each unresolved criterion with what is missing.
   - Leave body publication and further planning to the caller.

#### *Tick* Verified Criteria

The confirmed criteria and completed rows recorded in an epic or initiative body.

**Inputs:** Issue JSON, verified criterion ids, output body file, and the pull request records with the complete issue-link snapshot for an epic or every linked epic record for an initiative.

1. Record the criteria, meeting [Tick State](#tick-state).
   - For an epic, run [Record Epic Criteria](#record-epic-criteria) with the issue JSON, pull request records, complete issue-link snapshot, verified criterion ids and output body file.
   - For an initiative, run [Record Initiative Criteria](#record-initiative-criteria) with the issue JSON, every linked epic record, verified criterion ids and output body file.
2. Return the resulting body and any criteria refused as not ready to verify. The artifact operations return the updated bodies for publication.

### Delivery Branches

#### *Prepare* Delivery Bases

The branches a task pull request targets.

**Inputs:** Project checkout, epic identifier, changed long-lived branches and confirmed prerequisite evidence.

1. Run [List Long-Lived Branches](#list-long-lived-branches) with `--project` set to the project checkout.
2. Run [List Epic Bases](#list-epic-bases) for the epic.
3. If `config/branches` is missing or empty:
   - Report the names as unevaluable.
   - Obtain the project's branch names before creating delivery branches.
4. Require the caller's confirmed prerequisite evidence before creating a base. The board status alone supplies no such evidence.
5. Run [Create Epic Base](#create-epic-base) for each missing base, passing the project checkout, corresponding long-lived branch, epic base name and confirmed prerequisite evidence.

#### *Create* Epic Base

The missing epic branch rooted in its remote long-lived branch.

**Inputs:** Repository checkout, long-lived source branch, missing epic base name and confirmed prerequisite evidence.

1. Require the confirmed prerequisites and a missing destination. Refuse a destination that already exists.
2. Run [Fetch Remote Branch](#fetch-remote-branch) in the supplied repository checkout with the corresponding long-lived source branch, such as `main`.
3. After a successful fetch:
   - Run [Publish Epic Base](#publish-epic-base) with that remote source and the missing epic base name, such as `i07/e00/main`, meeting [Epic Bases](#epic-bases).
   - Return the created branch or the failure.

#### *Update* Task Branch

The current epic base merged into a unit's task branch.

**Inputs:** Task worktree, task branch name and corresponding epic base branch.

1. Run [Fetch Remote Branch](#fetch-remote-branch) in the unit's worktree with the epic base, such as `i07/e00/main`.
2. Stop on failure.
3. Run [Merge Remote Branch](#merge-remote-branch) in that worktree with the epic base name, such as `i07/e00/main`, to merge `origin/i07/e00/main`. A conflict stops the update, leaves the pull request open and is reported.
4. After a successful merge:
   - Run [Push Task Branch](#push-task-branch) with the task branch as destination.
   - Return the updated branch or the failure.

#### *Read* Delivery Branches

The configured long-lived branches and existing epic bases.

**Inputs:** Project checkout and epic identity.

1. Run [List Long-Lived Branches](#list-long-lived-branches) with the supplied checkout. Missing or empty configuration leaves branch names unevaluable.
2. Run [List Epic Bases](#list-epic-bases) for the supplied epic.
3. Return both collections and any missing configuration.

### Delivery Evidence

#### *Read* Delivery Evidence

The pull requests and issue links that establish current delivery.

**Inputs:** Selected repositories and initiative prefix, fetched epic JSON, authenticated access and destination snapshot files.

1. Fetch the pull requests and their links.
   - Run [Read Initiative Pull Requests](#read-initiative-pull-requests).
   - Run [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links).
   - Use [Access Development Links](#access-development-links) for the actual complete link sets.
2. Run [Inspect Epic Delivery](#inspect-epic-delivery) with the epic JSON, pull request records and complete issue-link snapshot.
   - Route the returned [Delivery Findings](#delivery-findings) to matching, verification or user decisions.
   - Fetch any linked pull request absent from the input with [Read Pull Request State](#read-pull-request-state).
   - Repeat Inspect Epic Delivery with the same epic JSON, refreshed pull request records and complete issue-link snapshot.
3. Repair a title the user confirms delivers an epic it does not name, meeting [Named Delivery](#named-delivery).
   - Run [Publish Pull Request](#publish-pull-request) with the confirmed epic prefix and purpose.
   - Repeat the fetch and match steps with the saved title before returning.
4. Return the current pull request records, complete issue-link snapshot and per-epic findings to the caller, reporting incomplete evidence as a blocker.

### Dependency Graph

#### *Check* Dependencies and Numbering

The task graph and the row numbers it permits, checked and renumbered across the supplied bodies.

**Inputs:** Initiative and epic bodies or local drafts, the work-item file of each task that has one, current pull request records, confirmed numbering maps when any, the caller's change allowance when it has one, and explicitly authorized outside-initiative files.

1. Use the supplied local drafts when reviewing unpublished work.
   - For published issues, fetch the initiative and each epic body with [Read Tracker Issue](#read-tracker-issue).
   - Run [Check Dependencies](#check-dependencies) with the initiative body, every epic body and every supplied work-item file.
2. Resolve each finding, as [Check Plan Change Autonomy](#check-plan-change-autonomy) returns it for the supplied allowance: an automatic correction is taken, and a held one is settled as [Held Change](#held-change) states.
   - Name the producing row for each consumed output, meeting [Edges](#edges), replacing an epic a task row names with the rows the task consumes.
   - Read tasks for implied consumption edges.
   - Account for every independent pair as [Joins](#joins) states.
   - Account for every contending pair as [Component Contention](#component-contention) states: the proposed map separates the two epics by a number, or the contending rows move into one epic.
   - Resolve backward references by moving work to the epic owning its inputs, or removing duplicate work already owned there. Work claimed twice has one owner and a boundary in both bodies.
3. Renumber the confirmed maps, preserving the numbers [Numbering Map](#numbering-map) protects.
   - For a confirmed epic map, run [Renumber Epics](#renumber-epics) with current pull request records and every affected body.
   - For a confirmed task map, run [Renumber Tasks](#renumber-tasks) with the initiative and epic identities, owning epic body, confirmed old-to-new task-number map and every affected body file.
   - Re-sort rewritten tables.
   - Inspect every reported range.
   - Search prose for references the script cannot see.
   - Repeat Check Dependencies after each edge or numbering change until it reports no problem.
   - Record the printed longest chains and each printed contending pair in the planning record.
   - Return the checked bodies, the proposed [Epic Priority](#epic-priority) map and unresolved findings to the caller; do not publish a failed renumbering.

### Epic Issue Body

#### *Populate* Epic Issue Body

One epic body and its local validation findings.

**Inputs:** Initiative context, epic scope, draft title and labels, criteria, proposed task rows, available pull request records, corpus branch and output path.

1. Populate the body from the [Template](#template) at the supplied output path.
   - Every section must meet [Fields](#epic-issue-body-2).
   - Shared content must meet the common [body conditions](#issue-body-1).
2. Populate the shared table through [Write Issue Table](#write-issue-table).
3. Fill the epic-specific cells.
   - Each row must meet [Work Breakdown](#work-breakdown).
4. Call [Build Body Snapshot](#build-body-snapshot) with the draft body, title, labels and existing issue JSON when present.
5. Pass that snapshot, initiative context, available pull request records, corpus branch and output file to [Validate Epic Body](#validate-epic-body).
6. Identify unresolved publication links separately; they remain pending until tracker identities exist.
7. Return the draft rows, their dependency references and the validation findings for the caller's cross-body ordering check.

#### *Record* Epic Delivery

One epic body with supplied delivery matches and completed rows recorded.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches, project checkout and output body file.

1. Run [Sync Epic](#sync-epic), mapping pull requests to `--prs`, links to `--links`, task issues to `--tasks`, each confirmed match to `--link`, the checkout to `--project` and the output file to `--fix`.
   - Row changes must meet [Task Delivery](#task-delivery) and [Work Breakdown](#work-breakdown).
2. Return the updated body and [Delivery Findings](#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.

#### *Record* Epic Criteria

Verified criteria and completed rows in one epic body.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, verified criterion ids and output body file.

1. Run [Tick Epic Criteria](#tick-epic-criteria) with the epic JSON, records as `--prs`, snapshot as `--links`, verified ids as `--tick` and output as `--fix`. Refuse criteria not ready to verify.
2. Return the body and refused criteria. Complete rows receive Done ticks.

#### *Reserve* Task Rows

Task rows held for one confirmed delivery session.

**Inputs:** Epic JSON, confirmed task ids, supplied planning-folder identity, planning-records base URL, record date and output body file.

1. Require the caller's confirmed unit and existing planning folder. Refuse a row already held or linked to a pull request or commit.
2. Run [Reserve Row](#reserve-row) with the epic as `--epic`, ids as `--reserve`, supplied base URL as `--records`, record date as `--date` and output as `--fix`.
3. Return the body with the folder as each row's single link, meeting [Task Delivery](#task-delivery).

#### *Release* Task Rows

Held task rows returned to their work-item links.

**Inputs:** Epic JSON, task ids, explicit user decision releasing the hold and output body file.

1. Require the supplied release decision and refuse any row that is not held.
2. Run [Release Row](#release-row) with the epic as `--epic`, ids as `--release` and output as `--fix`.
3. Return the body with each task id linked to its lowercase work-item file inside the reserved folder, meeting [Task Delivery](#task-delivery).

#### *Validate* Epic Body

The body's local format and field findings.

**Inputs:** Epic JSON, initiative context, current pull request records, corpus branch and output file.

1. Call [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#epic-issue-body-2), supplied related evidence and output file, supplying initiative JSON as `--initiative`, pull requests as `--prs` and corpus branch as `--corpus`.
2. Read reach from each epic pull request's base, through an epic base or initiative branch. Without both pull requests and the corpus branch, reach is unevaluable.
3. Include a missing [Corpus Audit](#corpus-audit) criterion on a corpus-changing epic and any epic criterion no task row delivers in the findings.
4. Return the corrected body, mechanical diff and unresolved findings for the caller.

#### *Revise* Epic Rows

One epic body with confirmed task-grain and coverage corrections.

**Inputs:** Epic body, confirmed row changes, field findings, supplied dependency references and output path.

1. Apply the confirmed row changes through [Populate Epic Issue Body](#populate-epic-issue-body), preserving unrelated content.
   - Description, Coverage, Depends on, Joins and task grain must meet [Work Breakdown](#work-breakdown).
   - Split a task exceeding the allowed criterion grain into the confirmed tasks.
2. Return the revised body and any cross-body numbering or dependency changes for the caller.

#### *Plan* Gap Task

The agreed disposition of criteria a delivered row left unmet.

**Inputs:** Current epic JSON and body, delivered task row, unmet criterion ids, delivery records, complete issue-link snapshot and output body path.

1. Present each unmet criterion and its missing evidence to the user.
   - Return the criteria the user confirms already hold to the caller for verification and ticking. The delivered task retains them.
   - Record an unanswered decision as pending.
   - If no criteria need further work, return the pending findings to the caller.
   - Continue to the draft step with only the criteria the user confirms need further work.
2. Draft a further task for the criteria selected for further work, meeting [Work Breakdown](#work-breakdown).
   - Confirm the draft with the user.
   - On acceptance, call [Revise Epic Rows](#revise-epic-rows) with the further row and the criteria it adopts from the delivered task's Coverage.
   - Return an unanswered draft as pending without continuing to the reconcile step.
3. Run [Record Epic Delivery](#record-epic-delivery) with the revised epic and the supplied delivery evidence.
   - Publish the returned body through [Save Tracker Issue](#save-tracker-issue).
   - Return the saved row and criterion disposition to the caller. Done follows [Tables](#tables).

### Epic

#### *Check* Epic Prerequisites

The evidence required before starting an epic's work.

**Inputs:** Current initiative and epic bodies, and current issue and base-merge records for every prerequisite the initiative row names.

1. Identify each prerequisite the supplied initiative row names.
2. Apply the initiative's [whole-epic dependency rule](#work-breakdown-1); a task row's reference to a row of another epic gates that row rather than this epic.
3. Confirm each prerequisite epic is closed as completed and every one of its bases has merged. Missing records leave the prerequisite unconfirmed.
4. Return the [Prerequisite Evidence](#prerequisite-evidence), identifying each confirmed prerequisite and missing condition. Only a confirmed result permits an unstarted epic to be marked Ready, its bases to be created or its task to be dispatched.

#### *Inspect* Epic Delivery

The delivery findings for one epic from supplied evidence.

**Inputs:** Epic JSON, current pull request records and complete issue-link snapshot.

1. Run [Match Pull Requests](#match-pull-requests) with the epic JSON, pull request records as `--prs` and link snapshot as `--links`.
2. Return the [Delivery Findings](#delivery-findings); missing linked pull requests are missing evidence for the caller to supply.

### Goal Trace

#### *Review* Initiative Goal

The draft checked against the initiative outcomes.

**Inputs:** Current initiative and epic bodies or drafts, confirmed goal clauses, marked requirement sources, and the supplied epic format results.

1. Take the goal the user stated and confirmed, as clauses, each an outcome someone could observe.
2. Build the [Trace Table](#trace-table) from those clauses, the initiative criteria, the epics whose Coverage cells cite them and the epic criteria that deliver them.
   - Every goal clause has an initiative criterion that makes it true.
   - Every initiative criterion is delivered by an epic, and that epic's criteria make the criterion wholly true.
   - Every initiative criterion traces to a goal clause.
   - Remove one that traces to none, or put that scope to the user.
   - Record any criterion no task row delivers as a gap from the supplied epic format results.
3. Call [Read Requirement Sources](#read-requirement-sources) with the initiative References, checkout, authenticated access and output files.
   - Extend the trace table with the source requirement each criterion answers to. Each unmatched requirement, each criterion that departs from the one it cites, and each source that could not be read is a gap [Sources](#sources) names.
4. Check each criterion against the [shared acceptance criteria](#shared-acceptance-criteria) and [Initiative Acceptance Criteria](#initiative-acceptance-criteria).
5. Call [Build Body Snapshot](#build-body-snapshot) for each supplied local draft with its title, labels and existing identity when present.
   - Use the returned initiative and epic JSON for [Validate Initiative Body](#validate-initiative-body) with the initiative JSON, every linked epic's current JSON, source evidence and output file.
   - Incorporate its local findings into this review.
6. Follow [Check Outside Threats](#check-outside-threats).
7. Rank the gaps, meeting [Gaps](#gaps).
   - Flag the few that most threaten the goal.
   - Record the trace table in the [planning record](#planning-record), or give it to the user when the change has none.
   - Return the trace and ranked findings to the caller.

#### *Check* Outside Threats

An item the draft leaves open is a gap.

**Inputs:** Current initiative and epic bodies or drafts, and the artifacts and consumers the plan changes.

1. Check for anything outside the plan that reads, builds or ships what the plan changes or removes.
2. Check for a skip, a fallback, or a fail-closed path that hides a violation.
3. Check that done has a threshold, a baseline, and an instrument that is independent of the thing measured. The baseline is fixed before the plan changes what it measures.
4. Check for skew between an artifact the plan produces and an implementation that reads it.
5. Check for a change elsewhere that alters the ground the plan stands on.
   - Return the evidenced threats and gaps to [Review Initiative Goal](#review-initiative-goal).

### Initiative Issue Body

#### *Record* Initiative Delivery

One initiative body with its epic delivery recorded.

**Inputs:** Initiative JSON, every linked epic's current JSON and optional output body file.

1. Run [Sync Initiative](#sync-initiative) with the initiative and all linked epic records as `--epics`, supplying `--fix` when an output body is requested.
2. Return the body and [Delivery Findings](#delivery-findings-1) from the supplied initiative and epic records. Delivery eligibility follows [Delivery State](#delivery-state).

#### *Record* Initiative Criteria

Verified criteria and completed rows in one initiative body.

**Inputs:** Initiative JSON, every linked epic's current JSON, verified criterion ids and output body file.

1. Run [Tick Initiative Criteria](#tick-initiative-criteria) with the initiative, linked epics as `--epics`, verified ids as `--tick` and output as `--fix`. Refuse criteria not ready to verify.
2. Return the body and refused criteria. Complete rows receive Done ticks.

#### *Validate* Initiative Body

The body's local format and field findings.

**Inputs:** Initiative JSON, every linked epic JSON, source evidence and output file.

1. Call [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#initiative-issue-body-1), supplied related evidence and output file, supplying each linked epic as `--epic`.
2. Use its current title for the initiative row.
3. Include excluded names in Problem and Proposal and criterion/source departures in the findings.
4. Return the corrected body, mechanical diff and unresolved findings for the caller.

#### *Read* Requirement Sources

The requirements evidence used to validate an initiative's criteria.

**Inputs:** Initiative References, checkout, authenticated source access and destination files.

1. Read each local source at its checkout path.
2. For a pinned GitHub blob, run [Fetch Source](#fetch-source) with its repository, path, pinned revision and output file.
3. Fetch other URLs through the harness's web access.
4. Record an unreadable or empty source as a [Sources](#sources) finding; its criteria remain unevaluated.
5. Return each source's contents and identity with those findings.

### Issue Body

#### *Write* Issue Table

The shared table, before a kind fills its cells.

**Inputs:** Current body, the kind's table columns and supplied row data.

1. Populate the shared Done, Coverage and Depends on cells from the supplied row data.
   - The columns must match the kind's table.
   - The shared cells must meet [Tables](#tables).
2. Read the finished table against [Tables](#tables), [Numbering](#numbering), and [Reference form](#reference-form). A Depends on cell that holds prose fails [Tables](#tables). Numbering that does not follow start order is advisory, as [Numbering](#numbering) states.

#### *Check* Round of Edits

The shared check after a round of edits.

**Inputs:** Changed issue bodies, their kind's field conditions and format inputs.

1. Check each section of the issue against the field conditions for its kind and against [Fields](#issue-body-1) in this file.
2. Run [Check Body Format](#check-body-format) on every issue the round changed.

#### *Validate* Issue Body

One body checked against its supplied kind and template.

**Inputs:** Issue JSON, kind field conditions, required related evidence and output body file.

1. Run [Check Body Format](#check-body-format) with the supplied issue JSON, kind inputs and output file as `--fix`.
2. Review the body against the supplied field conditions.
3. Return the [Format Findings](#format-findings), mechanical diff and field findings, including missing sections, extra sections, wrong-kind layout, historical narration and criteria that fail their named instrument. A mechanical correction preserves wording; new content and scope decisions require caller-supplied resolutions.

#### *Apply* Body Corrections

One body rewritten from confirmed local findings.

**Inputs:** Current body, selected kind template and field conditions, related context, confirmed resolutions and output path.

1. Populate missing sections from the supplied issue and related context.
2. Apply each confirmed decision to keep, fold or remove an extra section, and rewrite a wrong-kind body in the selected template.
3. Record a required tracker-kind change for the caller.
4. Restate historical narration as the current design.
5. Apply confirmed criterion changes.
   - The body must meet [Body](#body), [Shared Acceptance Criteria](#shared-acceptance-criteria) and the supplied kind conditions.
6. Validate the body through [Validate Issue Body](#validate-issue-body).
7. Return the corrected file, validation findings and any required cross-body or metadata changes for the caller.

#### *Build* Body Snapshot

A local issue-shaped record for body validation.

**Inputs:** Current body file, title, labels, optional existing issue JSON and destination JSON path.

1. Write the body's exact text, title and labels to the destination as JSON.
2. Preserve the existing issue's identity and state when supplied.
3. For an unpublished draft, use `number: null` and `state: "open"`; labels are strings or objects with a name.
4. Return the JSON path for validation. No tracker issue is created by this operation.

### Issue

#### *Read* Tracker Issue

The current issue, its saved body and discussion.

**Inputs:** Repository, issue number and output files; whether discussion is needed.

1. Run [Fetch Tracker Issue](#fetch-tracker-issue) for the complete JSON, or [Fetch Issue Body](#fetch-issue-body) for its body, with the issue number and destination file.
2. Run [Fetch Issue Comments](#fetch-issue-comments) when the request depends on the discussion.

#### *Save* Tracker Issue

One populated body and its metadata, written to the tracker.

**Inputs:** Repository, optional existing issue number, populated body file, title and existing labels for creation; selected body or metadata changes for an existing issue. Optional comment file.

1. Take the supplied body and metadata, preserving each field the caller does not change for an existing issue.
2. Return a missing-label result when an assignment names a label the repository does not contain.
3. For a new issue, run [Create Tracker Issue](#create-tracker-issue) with the body's file, title and labels.
4. For an existing issue, run [Patch Issue Body](#patch-issue-body), [Retitle Tracker Issue](#retitle-tracker-issue), [Add Issue Labels](#add-issue-labels) or [Remove Issue Label](#remove-issue-label) for the fields being changed.
5. Run [Comment on Issue](#comment-on-issue) for an answer or a preserved body the caller requires, with the issue number and comment file.
6. Re-read with [Fetch Tracker Issue](#fetch-tracker-issue).
7. Compare the saved fields with the intended body and metadata.

#### *Close* Tracker Issue

Verified completion of an issue and its linked delivery.

**Inputs:** Issue identity, successful normal delivery result, current issue JSON, complete Development snapshot, confirmed repository setting and fresh linked pull request records.

1. Run [Capture Issue Development](#capture-issue-development) for the issue's complete links and confirmed repository setting.
2. Take the caller's fresh records for every linked pull request, across repositories and states; return missing evidence to the caller.
   - Confirm GitHub's **Auto-close issues with merged linked pull requests** setting is disabled before any delivery pull request is linked or merged. An enabled or unknown setting blocks those actions until configuration is confirmed. Changing repository settings requires explicit authorization.
   - Use the issue's entire Development field to establish membership. Titles, branch names, body mentions and a list filtered to one initiative do not establish completeness. An explicitly empty field adds no pull request requirement.
3. Run [Check Issue Closure](#check-issue-closure) with `--issue`, `--development`, and `--prs` for those fresh records.
4. Require normal delivery checks to pass, every criterion to be verified and ticked, and every currently linked pull request to be merged.
   - Keep the issue open for an open, draft, closed without merge, or unreadable linked pull request.
   - Obtain the user's decision before removing an abandoned or incorrect Development link. A replacement pull request does not remove the requirement on a link still present.
5. Run [Close as Completed](#close-as-completed), which repeats the gate immediately before the write. A changed link set requires another capture and check.

#### *Comment* on Issue

The supplied discussion text saved on one issue.

**Inputs:** Repository, issue number and exact comment text or file; reviewer identity and addressed feedback when replying to a review.

1. When replying to feedback already folded into the body, compose a precise, factual reply addressing each point and mentioning the reviewer, with no thanks or filler. Name what the body now says, by criterion id where one carries it, or the issue that takes the point.
2. Publish the supplied comment:
   - For a one-line comment, run [Post Inline Comment](#post-inline-comment) with the exact text.
   - For a longer comment, run [Post Comment File](#post-comment-file) with the complete file.
3. Return the saved comment URL.

#### *Close* as Completed

An issue closed after its final evidence check.

**Inputs:** Repository, issue number, authenticated access, confirmed repository auto-closing setting, passing normal delivery checks and absolute paths to the current issue, Development and linked pull request evidence.

1. Run [Capture Issue Development](#capture-issue-development) immediately before closure with the issue identity, authenticated access, confirmed repository setting and evidence paths.
2. Compare its links with the supplied fresh pull request records; return a changed link set or missing evidence to the caller for refresh.
3. Run [Check Issue Closure](#check-issue-closure) with the current issue, Development and linked pull request files, using absolute evidence paths when changing directory.
4. Require exit 0 and passing normal delivery checks; a sync report of closable does not permit skipping this gate.
5. Immediately after the gate passes, run [Set Completed State](#set-completed-state) with the issue's repository and number and the passing evidence.
6. Return the saved state or failure.

#### *Capture* Issue Development

The issue's current content and complete Development snapshot.

**Inputs:** Issue identity, authenticated access, observed repository auto-closing setting and issue and Development output paths.

1. Run [Read Issue Development](#read-issue-development) for the entire field across repositories and states. An inaccessible field returns incomplete evidence; an empty array means the field was checked and empty.
2. Run [Write Development Snapshot](#write-development-snapshot) with the issue identity, observed link set, completeness result and repository setting, saving `development-943.json` or the supplied path.
   - Set `complete` true only after the full read, and `auto_close_issues` false only after the repository setting is confirmed disabled.
3. Run [Fetch Tracker Issue](#fetch-tracker-issue) into `issue-943.json` or the supplied path.
4. Return both files and any incomplete evidence. The caller supplies fresh linked pull request records in `development-prs-943.json`.

#### *Read* Issue Development

The Development links observed for one issue through authenticated GitHub.

**Inputs:** Issue identity and authenticated access.

1. Read every page and state, across repositories, recording each linked pull request's identity.
2. Return the observed links and whether the entire field was readable.

#### *Confirm* Repository Auto-Close

Whether the repository auto-closes issues whose linked pull requests merge, established for this session.

**Inputs:** Repository and authenticated access.

1. Read the setting where the authenticated API exposes it, and take a read value as the answer.
2. Where no API field carries it, put the setting to the user and take their explicit answer, meeting [Auto-Close Setting](#auto-close-setting).
3. Return the confirmed value. An unconfirmed setting is a blocker, and an enabled one leaves the caller to obtain authorization before the repository is reconfigured.

### Plan Change

#### *Check* Plan Change Autonomy

One pending change assessed against the run's allowance.

**Inputs:** The pending change, its subject, the option recommended for it, and the allowance the caller was supplied.

1. Match the change to one kind in [Change Kinds](#change-kinds).
2. Return it as automatic where the supplied allowance names that kind, with the supplied recommendation as the option the caller applies.
3. Return it as held otherwise, for the caller to settle as [Held Change](#held-change) states.
   - A change matching no kind is held, as is one matching [Initiative Creation](#initiative-creation).
   - An absent allowance holds every change, so a run the user drives decides nothing on their behalf.

### Planning Record

#### *Populate* Planning Record

One planning directory and its artifact inventory.

**Inputs:** Record identity, folder path and supplied artifact files and links.

1. Prepare the selected record:
   - For a new record:
     - Create the folder with [Add Planning Record](#add-planning-record).
     - Populate README.md from the [Template](#template-2).
   - For an existing record:
     - Read its README, retaining its creation date, other artifacts and links.
     - Update only the supplied content.
   - The folder must meet [Layout](#layout).
   - All populated README fields must meet [Fields](#planning-record-2).
2. Register the artifact files supplied by the caller, using their chosen names.
   - Each file must have a row meeting [Layout](#layout) and [Artifacts](#artifacts-1).
   - File content remains supplied by the caller; this operation does not author that artifact's content.

#### *Publish* Planning Record

The record's folder committed and pushed, so every link into it resolves for a reader.

**Inputs:** Planning-folder path, the files written into it and a commit message file.

1. Run [Find Engineering Worktree](#find-engineering-worktree) for the path the record is written on.
2. Run [Commit Planning Record](#commit-planning-record), which stages and commits that folder in one call.
   - Confirm the commit holds the files this record wrote, meeting [Shared Worktree](#shared-worktree).
3. Run [Push Engineering Branch](#push-engineering-branch).
   - Report a push that will not fast-forward rather than rewriting the branch.

### Proposal Body

#### *Validate* Proposal Body

The body's local format and field findings.

**Inputs:** Proposal issue JSON and output file.

1. Call [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#proposal-body-1), supplied related evidence and output file, using the proposal field conditions and required title and label metadata.
2. Return the corrected body, mechanical diff and unresolved findings for the caller.

### Pull Request

#### *Access* Development Links

The observed or updated Development relation for a pull request.

**Inputs:** Pull request identity, authenticated access and requested relation read or write; for an edit, the issue identity, confirmed repository prerequisite and any user decision authorizing removal of an abandoned or incorrect link, meeting the applicable preconditions in [Close Tracker Issue](#close-tracker-issue).

1. Run [Read Development Links](#read-development-links) for the actual field, including every page and state. A missing tool or inaccessible field is a blocker, not an empty link set.
2. Return the complete relation for a read-only request.
3. For a link edit:
   - Take the supplied repository prerequisite from [Confirm Repository Auto-Close](#confirm-repository-auto-close); an unconfirmed setting blocks the edit.
   - For an addition, run [Set Development Link](#set-development-link) with the pull request and issue identities.
   - For removal of an abandoned or incorrect link:
     - Require the supplied user decision.
     - Run [Remove Development Link](#remove-development-link) with those identities.
4. Run [Read Development Links](#read-development-links) again for the same pull request.
5. Compare the field with the intended edit.
6. Return the verified relation or discrepancy.

#### *Fetch* Pull Request Issue Links

The complete issue-link snapshot for a supplied set of pull requests.

**Inputs:** Current pull request records, authenticated access and destination link-snapshot file.

1. For every pull request in `prs.json`, run [Access Development Links](#access-development-links) with a read-only request and its identity. An observed empty field supplies an empty array; an unreadable field leaves the fetch incomplete.
2. Repeat that read after a link changes.
3. If any relation is unreadable, return the incomplete result.
4. Run [Write Pull Request Links](#write-pull-request-links) with the observed complete relations and destination `links.json`, including one entry per pull request and every linked issue's repository and number.
5. Return the snapshot for the scripts' `--links` input.

#### *Link* Pull Request to Issue

The verified delivery-issue relation for a pull request.

**Inputs:** Pull request identity, delivery issue identity, current pull request records, link-snapshot destination, authenticated access and the caller's confirmed repository prerequisite documented in [Close Tracker Issue](#close-tracker-issue).

1. Run [Access Development Links](#access-development-links) with the supplied identities, requested link addition and confirmed repository prerequisite.
2. Stop on a blocker or an unverified edit.
3. Run [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links) with the current records and destination after the edit.
4. Return the verified relation and refreshed snapshot.

#### *Read* Initiative Pull Requests

The current delivery pull requests for one initiative.

**Inputs:** Repository, initiative prefix and destination collection file.

1. Run [Fetch Initiative Pull Requests](#fetch-initiative-pull-requests) with the supplied repository and prefix, saving the collection to the supplied file.
2. Return the collection or an incomplete-fetch finding.

#### *Read* Pull Request State

One current pull request and its requested supporting records.

**Inputs:** Repository, pull request number, output paths and requested records: metadata, changed paths or reviews.

1. Run [Fetch Pull Request](#fetch-pull-request) or [Save Pull Request Snapshot](#save-pull-request-snapshot) for current identity, state, head and base.
2. Run [Fetch Pull Request Files](#fetch-pull-request-files) or [Fetch Pull Request Reviews](#fetch-pull-request-reviews) when the caller requests those records.
3. Return the snapshots or missing evidence.

#### *Publish* Pull Request

One pull request created or updated from supplied content and metadata.

**Inputs:** Repository, optional pull request number, task, epic or planning-discussion kind, body file and selected title, head or base changes, and, for a created delivery pull request, its delivery issue identity, the repository setting confirmed for the session and a link-snapshot destination.

1. For creation, run [Open Task Pull Request](#open-task-pull-request), [Open Epic Pull Request](#open-epic-pull-request) or [Open Discussion Pull Request](#open-discussion-pull-request) for the supplied kind, body, title, head and base, preserving epic and discussion draft state.
   - For a task or epic pull request, run [Link Pull Request to Issue](#link-pull-request-to-issue) with it, the supplied delivery issue, that confirmed setting and the snapshot destination, meeting [Issue Links](#issue-links).
2. For an existing pull request, run [Patch Pull Request Body](#patch-pull-request-body), [Retitle Pull Request](#retitle-pull-request) or [Retarget Pull Request](#retarget-pull-request) for the supplied changes, preserving other fields.
3. Re-read through [Read Pull Request State](#read-pull-request-state).
4. Return the saved state or discrepancy.

### Review Finding

#### *Populate* Review Finding

One finding verified against its supplied source.

**Inputs:** Area, severity, problem, proposed solution, source text and file:line, decision requirement and any confirmed answer.

1. Verify the problem against the supplied source.
2. If evidence is missing or contradictory, return that finding for the caller to resolve.
3. Populate the finding with its source quotation.
   - It must meet [Finding Content](#finding-content) and [Decision State](#decision-state).
4. Return the finding and any pending decision.

#### *Report* Review Finding

The verified findings presented for resolution.

**Inputs:** Area, severity, problem, solution and source evidence for each finding.

1. Call [Populate Review Finding](#populate-review-finding) with the area, severity, problem, solution and source evidence.
   - Resolve any evidence gap before reporting it.
   - Group the returned findings by area.
2. Put each pending decision to the user, one question at a time.
   - Wait for the answer.
   - Record the confirmed answer on the finding, meeting [Decision State](#decision-state).
   - Return each confirmed resolution to the caller for application to its selected issue kind. A pending decision returns without applying a change.

### Standalone Body

#### *Populate* Standalone Body

One standalone issue body from its supplied scope.

**Inputs:** Problem, design, criteria, open questions and output path.

- Populate the body from the [Template](#template-4) at the supplied output path.
  - The title must meet the shared [Titles](#titles-2) conditions.
  - The Problem and Proposal must meet [Problem and Proposal](#problem-and-proposal).
  - All populated fields must meet [Fields](#standalone-body-1), including the required [Sections](#sections-1).

#### *Revise* Standalone Body

One standalone body with its confirmed boundary integrated.

**Inputs:** Current body, confirmed content and boundary decisions, and output path.

1. Populate the body through [Populate Standalone Body](#populate-standalone-body), folding any Non-Goals into Proposal as a closing boundary.
2. Return the revised file for publication.

## Fields

### Acceptance Criteria

#### Readiness

A criterion is ready to verify when the supplied delivery findings show the work its evidence depends on delivered and readable. An undelivered or unreadable dependency leaves it unready.

#### Instrument Checkout

An instrument runs in a checkout of the project at the merged revision it is verifying, which the caller supplies. A checkout the caller is editing is not that revision, so a criterion verified against uncommitted work is unverified.

#### Instrument Result

A criterion is verified only on a passing run of its named instrument, recorded against the tested revisions as [Coverage Reports](#coverage-reports) define. A failed, unavailable or inconclusive instrument leaves it unverified, and an unverified criterion is not ticked.

#### Tick State

A ticked criterion carries verification evidence. Done on the row or table that cites it follows [Tables](#tables) and [Work Breakdown](#work-breakdown). A criterion refused as not ready to verify is returned unticked with what it is missing.

### Delivery Branches

#### Branches

A project states its long-lived branches in `config/branches` at its root, one name per line. A run from a linked worktree reads the statement its main working tree holds.

- **Example.**
  workflow-server's `config/branches` names `docker`, `main`, `workflows` and `workspace`.

#### Epic Bases

- Each long-lived branch an epic changes has a base branch, named for the initiative, the epic and that branch, and rooted in that long-lived branch. Its prerequisite epics are closed as completed with every delivery base merged.
- **Example.**
  An epic base cut from `main` is `i07/e00/main`.
- The base's last segment is its long-lived branch, which gives the target it merges and is merged into.
- Each base is worked in one worktree, named by the base under the worktree directory of the repository's main working tree.
- **Example.**
  `i07/e00/main` merges `main`, and is checked out at `.worktrees/i07/e00/main`.
- Every pull request delivering the epic's tasks targets that epic base.
- A completed epic is delivered by merging each base into its long-lived branch. The epic stays open until every base has merged.

### Delivery Evidence

#### Named Delivery

A pull request that delivers an epic carries that epic's reference in its title, as `[I07:E00] Purpose`. A delivery the user confirms whose title omits its epic is repaired before the evidence returns.

### Dependency Graph

#### Edges

A task edge names the producing row for each output the depending row consumes. An edge a task's prose implies is carried explicitly.

- **An edge names rows, never an epic.**
  A row naming an epic gates its task on every row of that epic, including the rows it consumes nothing from, which is how a [whole-epic edge](#whole-epic-edges) the rows do not justify reaches the initiative.
- **A task consuming from every row of an epic names the producing row for each output.**
  An edge another in the cell already implies is dropped, so a prerequisite chain is named by its last row, and the whole-epic reach is what the rows establish either way.
- **An entry that cannot resolve is a permanent condition, not a prerequisite to come.**
  An entry naming no row and linking no issue, naming an issue the run was not given, or naming a row the epic it points to does not carry, cannot resolve. Every tool reading the cell names the entry as written, leaves the row where it stands rather than placing it as work still to come, and exits nonzero.

#### Whole-Epic Edges

An initiative Depends on cell takes the epics it derives, as [Work Breakdown](#work-breakdown-1) states. It derives one only where every row of the dependent epic requires every row of the prerequisite, through the task edges alone: a task row names rows, so no cell can assert a whole epic that the rows do not already establish.

- **The edge is the coarsest gate the plan has.**
  It holds the dependent epic until the prerequisite closes, not until the row it consumes merges, and it drops the dependent a [priority](#epic-priority) number, so the board keeps it out of Ready while the prerequisite runs.
- **Its cost is why it is derived and never written.**
  A narrower dependency stays in the task graph, where it gates the row that consumes the output rather than the epic around it.

#### Epic Priority

The map proposes one positive integer for each epic supplied, derived from the whole-epic edges and the components its rows declare. Epics sharing a number start together, so the number asserts they can run in parallel, and it holds a set only where both of these do.

- **Prerequisite depth establishes when an epic may start.**
  An epic with no prerequisite epic, one whose tasks are not yet written among them, carries the largest number, and each other epic takes one less than the smallest its prerequisites carry.
- **Component contention establishes whether it can.**
  An epic holding a row that contends with a row of an epic of the same depth takes the number below that depth, and the epics depending on it follow it down, as [Component Contention](#component-contention) states.

#### Component Contention

Two task rows in different epics whose work items declare one [component](#component) contend. Concurrent epics are two bases and two pull requests, so one component written from both is a merge conflict.

- Rows of one epic are out of scope: they land on one base, in the order Depends on and [Joins](#joins) set, so one component written twice is a rebase on that base rather than a conflict between two of them.
- A contending pair is answered by the number that separates its epics, or by moving the rows into one epic.

#### Joins

Every pair of tasks in an epic where neither depends on the other is named in the epic's Joins, or accounted for in the planning record.

- **Both resolutions are stated where the pair is reported.**
  Naming the pair in Joins asserts one pull request; the record entry says why there are two. A report naming only the first makes the assertion the cheaper answer.
- **The record is read, so the second resolution closes the line.**
  A record file gives each pair a line of its own naming its two ids, which is the form a joins artifact takes, and the pair leaves the report. A line naming more rows than that is prose about them and accounts for none, so no enumeration empties the report. What remains is the set named in neither.

#### Numbering Map

A comma-separated list of `<old-number>:<new-number>` pairs assigning each old number one distinct new number. A number a pull request already names is preserved, and a row a pull request names is not renumbered. A source absent from the supplied files, or a duplicate destination, is refused.

### Epic Issue Body

#### Template

````markdown
## Overview

{{One paragraph: what this epic delivers and why it exists within the initiative.}}

## Problem

{{The friction as it is now. Bullets for distinct facets, sub-bullets for several items.}}

## Proposal

{{The design, in bullets or paragraphs, each opening with a bold statement, and its body on the next line.}}

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W01 | {{What the task delivers, at most eight words}} | AC{{n}}, AC{{m}} | {{Earlier task in this epic, [Exx:Wyy](…) or [Exx](…) in an earlier epic, or #issue}} | {{Tasks that can land in the same pull request}} | |

## Acceptance Criteria

- [ ] **AC1.** {{An end state of one invariant. It ends by naming its instrument.}}

## Open Questions

- {{An undecided point the epic cannot start without, with a recommendation in the planning record. Resolve every one before the first task starts, then delete the section.}}

## References

- **R1.** [Planning record]({{PLANNING_RECORD_URL}}) — {{What the reader finds there.}}
````

#### Titles

- The title is `[I07:E00] Name: Subtitle`. Its prefix matches its row in the initiative table.
- Labels are `type:epic` and its initiative's `theme:*`.
- `E` is the epic within its initiative. Epics count from `00`.
- The prefix separates levels with colons, then a short name, a colon, and a subtitle: `[I07:E06] Reliability Evaluation: Briefs, Measures and the Thresholds That Define Reliable`.

#### Proposal

- A boundary with a sibling epic is plain language.

#### Work Breakdown

New tasks exist as epic rows with their details, discussion and evidence in the epic and planning record. Planning creates no separate task issues. Existing issues hoisted into an epic retain their records and row links when new tasks are planned.

The columns are `Task | Description | Coverage | Depends on | Joins | Done`.

- **Done.**
  A task row is complete when it is delivered, and every criterion its Coverage names is ticked.
- **Row id.**
  The row id is the task, `W01`. `W00` holds preparatory work that must land before the first real task.
- **Description.**
  Each detail beyond the phrase is a criterion stating one invariant.
- **Coverage.**
  Coverage names the epic's criteria the task must meet. Each row claims only criteria its work makes true; it cannot claim a criterion another row delivers alone or one its work cannot meet. A complete task's cell is empty.
- **Depends on.**
  A task row names the rows it depends on. An earlier task in the epic (`W03`, `W04–W09`), a row of an earlier epic (`[E01:W02](…)`), or something outside the initiative (`#750`, `[I05:E00:W02](…)`).
  - A task row names rows, never an epic. It names the row producing each output it consumes (`[E01:W01](…), [E01:W02](…)`), and where the task consumes from every row of an epic that is what establishes the whole-epic reach.
  - Cross-epic dependencies name rows before any issue of the epic is created. Both tables exist, and each edge names the row that produces what the dependent row consumes.
  - A dependency listed twice or already implied by another in the cell is unsound. A task that measures, extends or consumes another task's output depends on it, even when the prose does not say so.
- **Task grain.**
  - A task is one pull request's worth of work.
  - A criterion a merged pull request left unticked belongs to a further task. The further task depends on the delivered task, and its Coverage is that criterion. Criteria one pull request can deliver share one further task. The delivered task's Coverage omits each criterion a further task adopts.
  - A task delivering more than three criteria is split into tasks one pull request each can deliver.
  - A task covers at least one acceptance criterion. A criterion more than one row cites is imprecise: it is split into the invariant each task makes true, and each is cited from the row that delivers it.
  - Every test the work calls for accompanies that task. The content steers which kinds those are, including the project's system test when the work is something that test can exercise. A failure in any test the task carries keeps the task open. None of those tests is a later row.
  - Reusable routines, techniques, and resources are specced, created, and tested before an activity binds them. The grain of an existing resource is in that work.
  - When the behaviour a wired activity produces differs from the behaviour the work expected, that task changes the routine, technique, or resource, and the tests that cover the change, until fit, form, and function hold.
- **Joins.**
  The tasks that share one pull request. Each names the other, and neither depends on the other, directly or through a task outside the pair: the pull request holds their order.
  - Joins are complete before any issue of the epic is created. Every pair of tasks in the epic where neither depends on the other, directly or through another task, is accounted for.
  - A pair that shares a pull request names each other.
  - A pair that does not is named in the planning record, with why.
  - An empty cell is a task that shares no pull request, and only once that record names every such pair.
- **Numbering.**
  Task numbering meets [Numbering](#numbering); a row whose id links a pull request is fixed.
- **Reference form.**
  A table reference uses colons (`E01:W03`, `I05:E00:W02`), and every epic reference links to that epic's issue: `[E01:W03](…/issues/937)`. Prose uses a space (`E01 W03`).

#### Acceptance Criteria

An epic criterion meets the [shared acceptance criteria](#shared-acceptance-criteria). Contradictions between criteria in one epic are findings.

#### Open Questions

Each question holds only what is undecided and has a recommendation in the planning record. A settled point belongs in that record. No question remains when the epic starts.

#### Corpus Audit

An epic whose tasks change workflow definitions carries this criterion, and a final task row delivers it:

```markdown
- [ ] **ACn.** The definitions this epic changes carry no outstanding confirmed finding, as the canon audit's coverage report shows.
```

- **The row is the epic's last.**
  It is named `Canon audit of the changed definitions`, depends on the rows whose definitions it audits, and covers this criterion alone.
- **A finding closes by a fix on this epic's branch or by an issue that takes it.**
  Outstanding means neither.
- **Definitions change when a task row's work reaches the branch the corpus lives on.**
  A row that only changes the engine, continuous integration or the workspace does not bring the criterion.

#### Task Delivery

- **Task ids.**
  - An unreserved task awaiting its pull request links its file in the planning record: `[W01](…/w01.md)`. The file name is the task id in lower case.
  - Every link on a task row names that row's id, and the row carries one delivery per long-lived branch its unit changes. A reserved task links only its planning folder: `[W01](…/2026-10-06-943-i07-e00-w01-queue-plan/)`. The folder's README links the work-item file. Releasing the reservation points the row to that file.
  - Once a pull request is open, its link replaces the planning link: `[W01](…/pull/950)`. A unit changing two long-lived branches links the pull request on each: `[W01](…/pull/950), [W01](…/pull/951)`. Further delivery work on one of those branches gets another task row under Task grain. Joined rows each link their shared pull request.
  - The task is delivered when a linked pull request has merged, or its id links a commit.
  - A link to an open pull request does not deliver the task.
  - A linked pull request whose title names another epic delivers the task once it has merged. The mismatch is reported, and the row stays open while a criterion its Coverage names is unticked.
- **Tasks with their own issue.**
  - A task issue belongs to one epic. Its title carries that epic's prefix.
  - When that epic's table has no row for its id, the issue is unplaced. Once the row exists, that epic's planning manages the issue.
  - The row links the pull request, not the issue.
  - The pull request's Development field links the issue as [Issue Links](#issue-links) state.
  - A completed task issue has all criteria verified and every Development-linked pull request merged.
- **Issues backing several tasks.**
  An issue backing several tasks, such as an investigation, is a reference: the epic cites it under References, no row id links it, and its title carries no agent-engineering prefix.
- **Work another issue takes.**
  It leaves the table. Its criteria go with it, or to another row that delivers them.

#### Breakdown Prose

Work Breakdown contains its table. Explanatory prose belongs in Proposal. The body does not narrate execution order or how the tables work; Depends on carries the order.

### Epic

#### Prerequisite Evidence

Each prerequisite has its issue identity and completion state, expected delivery bases and their merge evidence. The result identifies confirmed and missing conditions for the candidate epic.

#### Delivery Findings

| Line | What it names |
| --- | --- |
| Conflict | Tasks that share a pull request and do not name each other in Joins. A row linked to a pull request whose title names another epic. |
| Unmatched | A merged pull request that names the epic and that no row links. |
| In flight | An open pull request that names the epic and that no row links. A pull request whose head is an epic base is not a task match. |
| Draft | An epic base a merged task targets that has no pull request merging it, while a task is undelivered or a criterion is unticked. |
| Unmerged | An epic base its pull requests target that has not merged into its long-lived branch, once every task is delivered and every criterion is ticked. A draft pull request is named draft. |
| References | A review pull request whose cited pull requests differ from the task pull requests merged into its base. |
| Uncited | A linked pull request whose task has its own issue and does not link it, or a review pull request that does not link the epic's issue. |
| Note | A row that links its task issue. |
| Unplaced | A task issue of this epic whose id is not a row. |
| Open questions | The epic's Open Questions section remains. |
| Ready to verify | A criterion whose delivering rows are all delivered. |
| Ticked early | A criterion ticked while a delivering row is not delivered. |
| Disagreement | A linked pull request's test plan against the Coverage of the rows it delivers. |

An unmet row links a merged pull request while a covered criterion remains unticked. A linked pull request naming another epic is a conflict and delivers its linked task once merged. A missing linked pull request leaves the supplied evidence incomplete.

A coverage disagreement identifies the pull request and row, a criterion absent from either the test plan or row Coverage, an empty Test cell, or prose assigning the criterion to another task. Recording links, verified criteria and Done continues despite that finding.

### Goal Trace

#### Trace Table

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| The outcome the user confirmed | The criteria that make the clause true | The epics whose Coverage cells cite those criteria | The epic criteria that deliver them | The requirement the criterion answers to |

Every clause, criterion and epic the initiative holds occupies a row. A cell with no entry is a gap, not an omission.

#### Gaps

A gap is a clause no criterion makes true, a criterion no epic delivers, a criterion tracing to no clause, a criterion no task row delivers, an unmatched source requirement, a criterion departing from the source it cites, a source that could not be read, or a threat the draft leaves open. Gaps are ranked, and the few that most threaten the goal are flagged.

### Initiative Issue Body

#### Template

````markdown
## Overview

{{One paragraph: what the initiative achieves, stated as the end state. Name the goal the reviews will test against.}}

## Problem

{{One sentence on the friction, then one bullet per facet. Each bullet opens with a bold statement, and its body is on the next line.}}

- **{{Facet}}.**
  {{The evidence.}}

## Proposal

- **{{Move}}.**
  {{What is done, within two lines.}}

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/{{OWNER}}/{{REPO}}/issues/{{EPIC_ISSUE}}) | {{The epic's title name, the part before the colon}} | AC{{n}}, AC{{m}} | {{Earlier epic}} | |

## Acceptance Criteria

- [ ] **AC1.** {{One invariant. It is specific, measurable, achievable, relevant, and time-bound. It carries no stale count. It names no initiative, epic, task, or issue. It states what the initiative achieves as a whole, and it ends by naming its instrument.}}

## Non-Goals

- {{One succinct sentence on what this initiative does not do. It names no initiative, epic, task or issue, and no owner.}}

## References

- **R1.** [{{Title}}]({{URL}}) — {{What the reader finds there.}}
- **R2.** **Source.** [{{Title}}]({{URL}}) — {{The requirements this initiative's criteria answer to.}}
````

#### Titles

- The title is `[I07] Name: Subtitle`.
- Labels are `type:initiative` and a `theme:*`.
- `I` is the initiative number. Initiatives count from `00`.

#### Problem

- A Problem meets [Problem and Proposal](#problem-and-proposal).

#### Proposal

- A Proposal states the design, as [Problem and Proposal](#problem-and-proposal) defines.
- A Proposal names no epic, task, or acceptance criterion of its own initiative.

#### Work Breakdown

The columns are `Epic | Description | Coverage | Depends on | Done`. The table has no Joins column.

- An epic row's id is the epic, linked to its issue: `[E01](…/issues/937)`.
- An epic row's Description is the epic's title name, and its Coverage names the initiative criteria the epic serves.
- An epic row is complete when its issue is closed as completed.
- Depends on names epics only. A cell that names a task fails. Name a prerequisite epic only when every task or joined unit in the dependent epic requires every task in that prerequisite epic, directly or through its dependencies. The consumed output and the work producing it establish that requirement. Dependencies on selected tasks remain in the task tables. An edge another named whole-epic prerequisite already implies is omitted.
- An initiative dependency that only some tasks need, or that requires only part of its prerequisite epic, is overbroad. The output and its producing tasks establish the edge.
- An epic depending on a later epic is a backward reference.
- Epic numbering meets [Numbering](#numbering).

#### Initiative Acceptance Criteria

An initiative criterion meets the [shared acceptance criteria](#shared-acceptance-criteria) and [Requirement Characteristics](#referencesrequirement-characteristics), and:

- **No counts.**
  An initiative criterion carries no counts or figures, which go stale: it measures against a named baseline or check ("against the baseline", "as the budget test measures it"). A figure stays only where it is the criterion's own target, such as a bound it holds to.
- **SMART.**
  Each initiative criterion is specific about what holds, measurable by a named check or baseline, achievable by the epics that cite it, and relevant, tracing to a clause and to the Problem. It is time-bound by a release tag or another named milestone outside the initiative's own work, where one exists, and otherwise by the epics that cite it.
- **Local.**
  An initiative criterion names no initiative, epic, task or issue, and is solution-agnostic. Coverage cells link epics to criteria. One that holds only through another initiative's work is restated as what this initiative achieves, or it is dropped.
- **Whole.**
  An initiative criterion states what the initiative achieves as a whole. One that restates a single epic's criterion is a duplicate: it is raised to what the epics achieve together, or left to the epic.
- **Verified.**
  - An initiative criterion ends by naming its instrument. Which instruments keep a criterion is [Verifiable](#verifiable).
  - An automated test is an end-to-end walk through the real server, a smoke run of an agent against a live server, a live check on a deployed host, or a guard, fixture suite or check that continuous integration runs. The walk, smoke run or live check is preferred where the criterion is about what a run does.
  - A named test that does not exist yet is work the plan holds: a task in the epic whose subject it tests, or a discrete test-infrastructure epic when the tests serve several criteria. That epic's row cites the criteria its tests verify.

#### Non-Goals

- One succinct sentence each on what the initiative does not do, naming no initiative, epic, task or issue, and no owner.

#### References

- A proposal-derived initiative identifies its originating proposal in References with the proposal's exact title and issue URL, labelled as the originating proposal.
- A reference the criteria answer to carries **Source.** after its label: `- **R1.** **Source.** [Title](url) — what it binds`. An unmarked reference is background, and binds no criterion. What a marked one requires of the criteria is [Sources](#sources).
- A cross-initiative overlap is recorded in References. An approved edit to another initiative's issue stays minimal.

#### Sources

A marked source in References is a document the initiative's criteria answer to. The criteria are aligned with it in both directions.

- A criterion that misstates or contradicts a marked source fails the [Correct](#individual) characteristic.
- A requirement a marked source states that no criterion makes true, and no Non-Goal excludes, is a gap.
- An epic is aligned against its initiative's marked sources, through the initiative criteria its row covers.
- A marked source that cannot be read leaves its criteria unaligned until it is read.

#### Deferred Debt

A final epic of the initiative holds the debt that initiative's delivery defers. Its title name is `Deferred Debt` and its subtitle names the clear-up it takes; it carries its initiative's theme label and `tech-debt`, and it is raised when the initiative defers its first item. The initiative carries this criterion, which the epic's row covers:

```markdown
- [ ] **ACn.** The technical debt this initiative's delivery defers is fixed, as the Done column of its final epic's Work Breakdown shows.
```

- **It is the initiative's last epic.**
  Its number follows every other epic of the initiative, so the epics in flight are planned and delivered ahead of it and the clear-up competes with none of them.
- **A deferred item is a task row.**
  Each row covers the criterion stating what fixing that item makes true, and those statements are the epic's criteria.
- **It takes the debt its own delivery defers.**
  Debt a unit of this epic finds in resolving its row becomes a further row of the epic, so the clear-up absorbs what fixing it uncovers.
- **It delivers like any other epic.**
  It takes its bases from the long-lived branches its rows change, carries the [corpus audit](#corpus-audit) criterion where those rows change workflow definitions, and remains open until every delivery base has merged and its completion conditions hold.
- **The initiative stays open while it stands.**
  Its row is undelivered and its criterion unticked until the epic closes.

#### Breakdown Prose

Work Breakdown contains its table. Explanatory prose belongs in Proposal. The body does not narrate execution order or how the tables work; Depends on carries the order.

### Initiative

#### Delivery State

The state records every linked epic's completion, each initiative criterion's verification and tick, and the complete Development-linked pull request set and merge states. Each finding retains its source identity and evidence revision.

An epic is delivered when its issue is closed as completed. A missing, open or cancelled epic remains undelivered, including when all initiative criteria are ticked. Criterion readiness and premature ticks are [Delivery Findings](#delivery-findings-1); delivery alone does not verify a criterion.

Initiative completion requires every linked epic to be closed as completed, every criterion verified and ticked, and every Development-linked pull request merged. Incomplete evidence leaves completion unconfirmed. The result names each missing condition.

#### Delivery Findings

| Finding | Condition in the Supplied Initiative and Epic Records |
| --- | --- |
| Ready to verify | The initiative criterion is unticked and every epic whose Coverage cites it is delivered. |
| Ticked early | The initiative criterion is ticked and an epic whose Coverage cites it is undelivered. |

Epic delivery follows [Delivery State](#delivery-state). Each finding names the criterion and the supporting or missing epic evidence.

### Issue Body

#### Titles

- **Titles.**
  - A title is a short name, a colon, and a subtitle stating the outcome.
  - The name is two or three words and the subtitle a succinct summary of at most ten, in title case.
  - A prefixed title separates its levels with colons, then the name.
- **Bodies.**
  - Every body keeps the section order of its kind template and the columns of that kind's table.
  - Fill each `{{…}}` and delete a section the template marks as optional when it has nothing to say.
- **Code references.**
  A body references code as a link on the words it supports, a permalink pinned to a commit with its line anchors, never a bare `path:line`: `the [extrinsic type](…/blob/<sha>/runtime/src/lib.rs#L1231-L1232)`.
- **Succinct items.**
  Each Problem and Proposal item, and each of its sub-bullets, is at most two lines. A bold opener does not count toward the two. Several distinct points go in a bulleted list, never packed into those two lines.
- **Bold leads.**
  - A Problem or Proposal item that opens with a bold statement puts its body on the next line, indented under the bullet:

    ```markdown
    - **Length is the only check on entry.**
      The data source decodes the key and never checks its value.
    ```

  - A bulleted item with sub-bullets keeps the line introducing them on its bold statement's line:

    ```markdown
    - **Framing is undocumented.** Nothing describes:
      - the runtime's extrinsic type;
    ```
- **Labels.**
  - Add `enhancement`, `bug` and `tech-debt` as they apply.
  - **Example.**  workflow-server adds `workflows`.
  - Only labels that exist are applied.

#### Problem and Proposal

- **Friction.**
  A Problem states the friction as it is now. Its evidence is a count or a code link for that friction. A Problem does not describe the plan.
- **Plan ids.**
  A Problem or Proposal names no epic, task or acceptance criterion of its own initiative. The Work Breakdown table holds those references; a sibling boundary is plain language.
- **Evidence that may be cited.**
  Code, a merged pull request, and an issue outside this initiative may be cited.

#### Shared Acceptance Criteria

An acceptance criterion meets these. A kind adds its own under its Acceptance Criteria.

- States an end state, not an activity.
- Names or implies the instrument that observes it: a test, a guard, a command or a measure.
- Is unambiguous, so two readers agree on whether it holds.
- Meets [Requirement Characteristics](#referencesrequirement-characteristics).
- **One invariant.**
  Each criterion states a single condition that holds or does not. One joining several is split, and the Coverage cells cite the new ones. A condition over a list of subjects is one condition.

##### Verifiable

- Subjective wording is an observable pass or fail, or the criterion is absent.
- A fact that inspection, analysis, demonstration, or test can check is kept, such as every option having a description.
- A judgment about meaning, such as a claim that a description states what choosing means, is subjective wording.
- An item none of those methods can observe is named as [Coverage Reports](#coverage-reports) define, and it stays named there.

#### Tables

- **Done.**
  The last column. Its cell is empty while the row is open, and a tick, ✓, when the row is complete.
- **Description.**
  A short phrase naming what the row delivers, at most eight words, with no list, semicolon or detail.
- **Coverage.**
  The acceptance criteria the row delivers, `AC2, AC5`, and nothing else. Every criterion is delivered by at least one row.
- **Depends on.**
  References only, with no prose, and only what no other entry in the cell already implies.

#### Numbering

Rows are numbered in the order they can start, so every dependency points to an earlier row. Numbering that does not follow start order is advisory.

Work a pull request names keeps its number. Renumbering touches only a row no pull request names.

#### Reference Form

Tables write references with colons, the form the scripts read. Prose uses a space.

#### Body

- **Stale references.**
  A row number, issue link or decision wording agrees with the current plan.
- **Body.**
  A body states the plan as it is. It carries no change narrative. How the plan evolved belongs in the planning record and in commit and pull request bodies.

#### Stale References

Task and epic numbers, issue links and wording must agree with the current decisions and bodies. References to superseded decisions are findings.

#### References

An issue's References section does not link issues or pull requests on the same board.

#### Coverage Reports

- **Unobservable items.**
  An item a test cannot observe is named in the plan or the coverage report. It stays in the report.
- **The check matches the criterion.**
  - A file or string check counts as coverage only when the criterion is a fact about that file.
  - A criterion about a run is covered by a run that shows it.
- **The specified set.**
  A coverage report lists every acceptance criterion the work under review is specified to cover.

#### Format Findings

- **Fixed.**
  Structural changes preserve the wording and are present in the returned body file, with a body diff.
- **Apply.** Title or label changes for the caller to publish on the issue.
- **Decide.** Missing content or a judgement for the caller to resolve.

### Issue

#### Auto-Close Setting

GitHub's **Auto-close issues with merged linked pull requests** repository setting, which must be disabled before a delivery pull request is linked or merged, so that closure follows the criteria rather than the merge.

- The setting is confirmed per repository and holds for the session; it is not inferred from an issue that stayed open.
- No REST field and no GraphQL field of `gh` 2.46 carries it, so on such a host the user's explicit answer is the only source.
- An enabled setting closes issues on merge whatever their criteria. Where it cannot be disabled, each affected issue's state is read after every merge and reopened where its criteria are unmet.

### Plan Change

#### Change Kinds

| Kind | What It Covers |
| --- | --- |
| Task creation | A new task row, and the task issue that delivers it |
| Epic creation | A new epic, and the initiative row that carries it |
| Migration | Work moved from one issue to another, with the renumbering that move forces |
| Re-prioritisation | A priority label, a queue order or a board status |
| Folded work | Criteria, scope or design added to an existing issue because the work in hand needs it |

An option deciding to leave work where it is changes no plan, so it needs no allowance and takes no entry, unlike a change [held](#held-change) for the user to decide.

#### Initiative Creation

A new initiative is outside every allowance. The work stays where it is, open and unplaced, until the user decides where it belongs.

#### Held Change

A held change is left unapplied and its subject stays as it stands, so the next run sees the same decision. Its entry carries the recommended option, which is what the user is answering.

A run working under an allowance records and reports a held change rather than asking, since the work it was dispatched for does not wait on an answer. A run supplied no allowance puts it to the user.

### Planning Record

#### Template

```markdown
# [Descriptive name] — [Month Year]

> [Classifier] · Created [YYYY-MM-DD]

## Executive Summary

[Two paragraphs on the purpose of this work and why it matters.]

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Name](file.md) | What this artifact holds |

## Links

| Resource | Link |
| --- | --- |
| [External reference] | [link] |
```

#### Shared Worktree

The engineering branch has one worktree and every session writes its records there, so they share one index. A commit therefore names the folder it is for, and a session confirms its own files landed in its own commit rather than assuming the index held only its staging.

#### Layout

README.md is the one file the folder must hold. Any file beyond README.md is added as the work needs it.

```text
./
├── README.md
└── …
```

Each file beyond README.md is a row in the README's Artifacts.

#### Header

One blockquote: the classifier, the day the record was created, and a revised date when the README is updated after the work is done.

#### Executive Summary

Two paragraphs: the purpose of this work, and why it matters.

#### Artifacts

- One row for every artifact in the record other than README.md, added when the file is produced.
- The link sits on the artifact's name. The row says what the artifact holds, and the artifact is the home of that content.

#### Links

External references only: a tracker issue, a parent epic, a pull request. An artifact of this plan is an Artifacts row.

### Proposal Body

#### Template

````markdown
## Overview

{{One paragraph: the problem this proposal scopes. Name the goal the clauses state.}}

## Problem

{{One sentence on the friction, then one bullet per facet. Each bullet opens with a bold statement, and its body is on the next line.}}

- **{{Facet}}.**
  {{The evidence.}}

## Goal

- {{A clause: an outcome someone could observe. Not a description of the change.}}

## Non-Goals

- {{One succinct sentence on what this proposal does not do. It names no initiative, epic, task or issue, and no owner.}}

## References

- **R1.** [{{Title}}]({{URL}}) — {{What the reader finds there. Delete the section when there is none.}}
````

#### Titles

- The title is `[P00] Name: Subtitle`.
- The label is `type:proposal`.
- `P` is the proposal number. Proposals count from `00`.

#### Problem

- A Problem meets [Problem and Proposal](#problem-and-proposal).

#### Goal

- Each clause is an outcome someone could observe.
- A clause does not describe the change.

#### Non-Goals

- One succinct sentence each on what the proposal does not do.
- A non-goal names no initiative, epic, task or issue, and no owner.

#### Sections

- Overview, Problem, Goal and Non-Goals are present in that order. References follows when it has content.

### Pull Request

#### Issue Links

- GitHub shows the link in the pull request's Development field and in the issue's Linked pull requests field, which the project board reads.
- A task pull request links the task's issue, and a review pull request links its epic's issue.
- The link is addressed by issue, so a pull request whose work carries no issue links nothing. A task pull request delivering rows that have no issue of their own is the whole of what stays unlinked.
- The link is stored on the pull request. It holds on any base branch and on a pull request that has merged, and a later body edit leaves it standing.
- A linked issue remains open until its criteria and delivery requirements hold and every Development-linked pull request is merged.
- The field is the whole of the relation: neither body links the other. The pull request's References carry its sources, and the issue it delivers is not among them.
- A pull request with a delivery issue but no Development link is uncited.

### Review Finding

#### Finding Content

Each finding has an area, severity, one problem/solution pair and a source quotation with file and line. The source establishes the stated problem. Findings are grouped by area when presented together.

#### Decision State

A finding identifies whether it needs a user decision and records any supplied answer. An unanswered decision remains pending.

### Standalone Body

#### Template

````markdown
## Overview

{{One paragraph: what this issue asks for and why.}}

## Problem

{{The friction as it is now. Bullets for distinct facets, sub-bullets for several items.}}

## Proposal

{{The design, in bullets or paragraphs, each opening with a bold statement, and its body on the next line.}}

## Acceptance Criteria

- [ ] **AC1.** {{An end state of one invariant. It ends by naming its instrument.}}

## Open Questions

- {{An undecided point the work cannot start without. Resolve every one before the work starts, then delete the section.}}

## References

- **R1.** [{{Title}}]({{URL}}) — {{What the reader finds there. Delete the section when there is none.}}
````

#### Titles

- The title is `Name: Subtitle`, with no prefix.
- A standalone issue carries no `type:*` label.

#### Sections

- A standalone issue has the [epic issue body](#epic-issue-body)'s sections without the Work Breakdown table.

### Task Body

#### Template

````markdown
## Overview

{{One paragraph: what this task delivers and why it exists within the epic.}}

## Problem

{{The friction as it is now. Bullets for distinct facets, sub-bullets for several items.}}

## Proposal

{{The design, in bullets or paragraphs, each opening with a bold statement, and its body on the next line.}}

## Acceptance Criteria

- [ ] **AC1.** {{An end state of one invariant. It ends by naming its instrument.}}

## Open Questions

- {{An undecided point the task cannot start without. Resolve every one before the task starts, then delete the section.}}

## References

- **R1.** [{{Title}}]({{URL}}) — {{What the reader finds there. Delete the section when there is none.}}
````

#### Titles

- The title is `[I07:E00:W01] Name: Subtitle`.
- The label is `type:task`.
- `W` is the task within the epic. Tasks count from `W01`.

#### Open Questions

- Each holds only what is undecided, and is resolved before the task starts.

#### Acceptance Criteria

- A task criterion meets the [shared acceptance criteria](#shared-acceptance-criteria).

#### Sections

- A task has the [epic issue body](#epic-issue-body)'s sections without the Work Breakdown table.
- New task planning follows [Work Breakdown](#work-breakdown). This body describes an existing issue kept as a task.

### Work Item

#### Component

One declaration line ahead of the first heading, naming the single component the Implementation part extends as the path to it in the repository that holds it.

- A task that creates the component names the path it creates.
- A task whose implementation extends more than one component is split into a task for each.

## Commands

### Delivery Branches

#### List Epic Bases

Prints one epic's base branch names, one per line.

**Inputs:** Repository checkout and epic branch prefix.

- A base is `<epic-branch-prefix>/<name>` whose `<name>` is a [long-lived branch](#branches), named as [Epic Bases](#epic-bases) states.
- The prefix has the form `i<initiative-number>/e<epic-number>`. **Example:** `i07/e00`; a corresponding base is `i07/e00/main`.
- The output contains one full base branch name per line.

```bash
git ls-remote --heads origin 'refs/heads/<epic-branch-prefix>/*' | cut -f2 | sed 's|refs/heads/||'
```

**Example:**

```bash
git ls-remote --heads origin 'refs/heads/i07/e00/*' | cut -f2 | sed 's|refs/heads/||'
```

#### List Long-Lived Branches

Prints the long-lived branch names, one per line.

**Inputs:** Project checkout.

- The names meet [Branches](#branches).
- `--project` is any checkout of the project. The names are the ones `config/branches` states in its main working tree, which a linked worktree resolves for itself.
- A missing or empty statement prints `unevaluable:`, names what is missing, and exits 1.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py --names --project '<checkout>'
```

#### Fetch Remote Branch

Fetches one source branch from origin.

**Inputs:** Repository checkout and source branch.

```bash
git fetch origin '<source-branch>'
```

#### Publish Epic Base

Creates a remote epic base from the fetched source branch.

**Inputs:** Repository checkout, fetched long-lived source branch, destination epic-base name, confirmed missing destination and prerequisite evidence.

```bash
git push origin 'origin/<source-branch>:refs/heads/<epic-base>'
```

#### Merge Remote Branch

Merges one fetched remote branch into the current worktree branch.

**Inputs:** Destination worktree and fetched source branch name without the origin prefix.

```bash
git merge --no-edit 'origin/<source-branch>'
```

#### Push Task Branch

Pushes the task worktree head to its named remote task branch.

**Inputs:** Task worktree, destination task branch and successful merge result.

```bash
git push origin 'HEAD:refs/heads/<task-branch>'
```

**Example:**

```bash
git push origin HEAD:refs/heads/i07/e00/w01-queue-plan
```

### Dependency Graph

#### Check Dependencies

Checks the task dependency graph across the epics given, and with `I=` the initiative's Depends on cells.

**Inputs:** Initiative body file, each epic id with its body file, each task id with its work-item file, and each planning-record file accounting for independent pairs.

- Keep `I=` for the initiative. Repeat the `<epic-id>=<epic-body-file>` argument once per epic, the `<epic-id>:<task-id>=<work-item-file>` argument once per work item, and `R=<record-file>` once per record.
- The command runs in `<workspace>` while body files are kept outside the repository, so pass each one as an absolute path.

- Initiative edges follow the [whole-epic prerequisite rule](#work-breakdown-1); narrower dependencies stay in the task graph.
- It also reports dependencies listed twice or already implied, and Joins pairs.
- It prints each pair of tasks in an epic where neither depends on the other, the two do not name each other in Joins, and no `R=` record accounts for the pair. Each line names both resolutions, as [Joins](#joins) states. A record accounts for a pair by naming both ids on one of its lines, and an `R=` file it cannot read is a problem.
- An entry it cannot resolve is a problem naming the entry as written, as [Edges](#edges) states. Its second clause says what this run could not find, which is the epics it was given.
- It prints each pair of rows in different epics whose work items declare one component, meeting [Component Contention](#component-contention), and names the rows it was given no work item for, so a partial report says what it passed over.
- A task row naming an epic rather than the rows it consumes is a problem, as [Edges](#edges) states. That row still reaches the epic's rows, so a body carrying the retired form is reported once rather than taking its initiative's gates down with it.
- It reads a declared component without its link, a wrapping code span, a trailing full stop or a leading `./`, and reports a work item it cannot read.
- It prints the proposed [Epic Priority](#epic-priority) of each epic, largest first.
- It reads bodies from [Read Tracker Issue](#read-tracker-issue), or local drafts.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deps.py 'I=<initiative-body-file>' '<epic-id>=<epic-body-file>' '<epic-id>:<task-id>=<work-item-file>' 'R=<record-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deps.py I=/drafts/live-936.md E00=/drafts/live-943.md E01=/drafts/live-937.md E00:W01=/drafts/e00/w01.md E01:W01=/drafts/e01/w01.md R=/records/joins.md
```

#### Renumber Tasks

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

#### Renumber Epics

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

### Epic Issue Body

#### Sync Epic

Links each named task's id to a pull request naming the epic, open or merged, and ticks Done on a row once it is complete.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, task records, confirmed matches, project checkout and output body file.

- A row whose id links its task issue links the pull request instead.
- A pull request whose head is an epic base is the pull request that merges that base, and is not matched to a task.
- An unmerged epic base keeps the epic open, even when every row is delivered and every criterion is ticked.
- `--project` is a checkout of the project. Without the long-lived branch names, an epic that would otherwise be closable is not.
- `--link` names each task id and the pull request number it links. `--tasks` is the task issues. `--links` is the pull requests' Development-linked issues. `--fix` is the body written with the Done ticks.

`<task-pull-request-map>` is a comma-separated list of `<task-id>=<pull-request-number>` pairs. Pass each task JSON file as a separate argument after `--tasks`.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --tasks '<task-json-file>' --link '<task-pull-request-map>' --project '<checkout>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json --tasks issue-637.json --link W01=950,W02=950 --project '<checkout>' --fix fixed-943.md
```

#### Tick Epic Criteria

Ticks confirmed epic criteria, refusing any not ready to verify, and ticks completed rows.

**Inputs:** Current epic JSON, pull request and link snapshots, verified criterion ids and destination body file.

`<criterion-ids>` is a comma-separated list of verified criterion ids.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --tick '<criterion-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json --tick AC1,AC3 --fix fixed-943.md
```

#### Reserve Row

Holds each named task row for one session, by setting its record folder as the row's single link.

**Inputs:** Epic JSON, confirmed reservable task ids, planning-folder identity, record date, records base URL and output body file.

- `--records` is the URL of the planning records folder, needed when no row id in the epic links a record.
- The caller supplies the planned folder identity; `--date` is the day it is opened.

`<task-ids>` is a comma-separated list of task ids; `<records-base-url>` identifies the planning records folder.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic '<epic-json-file>' --reserve '<task-ids>' --records '<records-base-url>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic issue-943.json --reserve W01,W02 --records 'https://github.com/<owner>/<repo>/tree/engineering/artifacts/planning' --fix fixed-943.md
```

#### Release Row

Frees each named task row, by replacing the planning-folder link with its work-item file link.

**Inputs:** Epic JSON, confirmed held task ids, authorized release and output body file.

- The file is the task id in lowercase within that folder, as [Task ids](#task-delivery) defines.

`<task-ids>` is a comma-separated list of task ids.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic '<epic-json-file>' --release '<task-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deliver.py --epic issue-943.json --release W01 --fix fixed-943.md
```

### Epic

#### Match Pull Requests

Reports an epic's delivery state against the pull requests that name it.

**Inputs:** Epic JSON, pull request records and complete issue-link snapshot.

- Results follow [Delivery Findings](#delivery-findings).

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json
```

### Initiative Issue Body

#### Sync Initiative

Reports an initiative's delivery state against its epics, and ticks Done on an epic row whose issue is closed as completed.

**Inputs:** Initiative JSON, every linked epic record and optional output body file.

- It takes every linked epic's current JSON. Delivery findings follow [Delivery State](#delivery-state).

Pass every epic JSON file as a separate argument after `--epics`.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<initiative-json-file>' --epics '<epic-json-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-936.json --epics issue-943.json issue-937.json
```

#### Tick Initiative Criteria

Ticks confirmed initiative criteria, refusing any not ready to verify, and ticks completed rows.

**Inputs:** Current initiative JSON, every linked epic JSON, verified criterion ids and destination body file.

Pass every epic JSON file as a separate argument after `--epics`. `<criterion-ids>` is a comma-separated list of verified criterion ids.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<initiative-json-file>' --epics '<epic-json-file>' --tick '<criterion-ids>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-936.json --epics issue-943.json issue-937.json --tick AC2 --fix fixed-936.md
```

#### Fetch Source

Saves one GitHub source at the revision its permalink pins.

**Inputs:** Repository owner and name, source path, pinned revision and destination file. URL-encode the path and revision for the request.

```bash
gh api 'repos/<owner>/<repository>/contents/<source-path>?ref=<revision>' --jq .content | base64 -d > '<source-file>'
```

**Example:**

```bash
gh api 'repos/m2ux/workflow-server/contents/docs/spec.md?ref=4a217fe6' --jq .content | base64 -d > source-R1.md
```

### Issue Body

#### Check Body Format

Checks one issue against its template, and with `--fix` writes the body with the mechanical fixes made.

**Inputs:** Issue JSON, local output body file and the additional format inputs supplied by the kind.

- The format reader takes the template fence from the body artifact and its table columns where present. A body with a Work Breakdown table requires coverage for every criterion.
- The input is one issue JSON. `--fix` names the output body file for mechanical fixes. Further inputs are specified by the calling body procedure.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/format.py '<issue-json-file>' --fix '<output-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/format.py issue.json --fix fixed.md
```

### Issue

#### Create Tracker Issue

Creates an issue from a body file, with its title and labels, and prints its number.

**Inputs:** Repository, populated body file, title and existing label names.

Repeat `-f 'labels[]=<label>'` for each supplied label.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues' -f title='<title>' -F 'body=@<body-file>' -f 'labels[]=<label>' --jq .number
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues' -f title='<title>' -F body=@body.md -f 'labels[]=<label>' --jq .number
```

#### Patch Issue Body

Replaces an issue's body from a file.

**Inputs:** Repository, issue number and complete populated body file.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -F 'body=@<body-file>' --jq .number
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -F body=@body.md --jq .number
```

#### Fetch Issue Body

Saves an issue's body alone.

**Inputs:** Repository, issue number and destination file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' --jq .body > '<output-body-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' --jq .body > live-943.md
```

#### Retitle Tracker Issue

Replaces an issue's title.

**Inputs:** Repository, issue number and complete title.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f title='<title>' --jq .title
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -f title='<title>' --jq .title
```

#### Add Issue Labels

Adds labels to an issue.

**Inputs:** Repository, issue number and existing label names.

Repeat `-f 'labels[]=<label>'` for each supplied label.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/labels' -f 'labels[]=<label>' --jq '.[].name'
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/943/labels' -f 'labels[]=<label>' --jq '.[].name'
```

#### Remove Issue Label

Removes one label from an issue.

**Inputs:** Repository, issue number and label name.

```bash
gh api --method DELETE 'repos/<owner>/<repo>/issues/<issue-number>/labels/<label>' --jq '.[].name'
```

**Example:**

```bash
gh api --method DELETE 'repos/<owner>/<repo>/issues/943/labels/<label>' --jq '.[].name'
```

#### Fetch Issue Comments

Prints an issue's comments.

**Inputs:** Repository and issue number.

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/<issue-number>/comments'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/874/comments'
```

#### Fetch Tracker Issue

Saves an issue whole, as JSON, for the scripts that read issues.

**Inputs:** Repository, issue number and destination JSON file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' > '<issue-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' > issue-943.json
```

#### Check Issue Closure

Checks the issue criteria, the complete link snapshot and every linked pull request.

**Inputs:** Current issue JSON, complete Development snapshot and fresh linked pull request records.

- `--issue`, `--development`, and `--prs` are the fresh issue JSON, Development snapshot, and linked pull request records.
- Exit 0 means the closure gate passes; normal delivery checks must also pass. Exit 1 reports blockers. The command performs no network calls or writes.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue '<issue-json-file>' --development '<development-snapshot-file>' --prs '<linked-pull-request-records-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue issue-943.json --development development-943.json --prs development-prs-943.json
```

#### Post Inline Comment

Posts one line of exact comment text and returns its URL.

**Inputs:** Repository, issue number and one-line comment text.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -f body='<comment-text>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/637/comments' -f body='Delivered by #950.' --jq .html_url
```

#### Post Comment File

Posts a complete comment file and returns its URL.

**Inputs:** Repository, issue number and exact comment file.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -F 'body=@<comment-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/874/comments' -F body=@comment-874.md --jq .html_url
```

#### Set Completed State

Sets an issue to closed with the completed reason and returns its state.

**Inputs:** Repository, issue number, passing normal delivery checks and an immediately preceding successful closure gate on current evidence.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f state=closed -f state_reason=completed --jq .state
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -f state=closed -f state_reason=completed --jq .state
```

#### Write Development Snapshot

Saves an observed Development field and repository setting as JSON.

**Inputs:** Repository and issue number, observed links, completeness result, confirmed or unknown auto-closing setting and destination file.

Write the supplied values in this shape. Substitute the issue number as a JSON integer, completeness as a boolean, and the auto-closing setting as a boolean or `null` when unknown. Supply every observed pull request URL, or an empty array when there are none. Preserve incomplete evidence as incomplete.

```text
{
  "repo": "<owner>/<repo>",
  "number": <issue-number>,
  "complete": <complete>,
  "auto_close_issues": <auto-close-issues>,
  "pull_requests": ["<pull-request-url>"]
}
```

**Example payload:**

```json
{
  "repo": "owner/repo",
  "number": 943,
  "complete": true,
  "auto_close_issues": false,
  "pull_requests": ["https://github.com/owner/repo/pull/980"]
}
```

### Planning Record

#### Find Engineering Worktree

Prints the checkout holding the engineering branch, which is where every planning record is written.

**Inputs:** Any checkout of the project.

- The engineering branch has one long-lived worktree and takes no further one.

```bash
git worktree list | grep '\[engineering\]'
```

#### Commit Planning Record

Stages and commits one planning folder on the engineering worktree.

**Inputs:** Engineering worktree, planning-folder path and a commit message file.

- Staging and committing are one call, and the commit names its folder, so a concurrent session's staged work cannot ride along. See [Shared Worktree](#shared-worktree).
- Pass the message through a file; the worktree is a linked one, so git writes here run unsandboxed.

```bash
cd '<engineering-worktree>' && git add '<planning-folder-path>' && git commit -F '<message-file>' -- '<planning-folder-path>'
```

**Example:**

```bash
cd .engineering && git add artifacts/planning/2026-10-15-950-queue-plan && git commit -F msg.txt -- artifacts/planning/2026-10-15-950-queue-plan
```

#### Push Engineering Branch

Publishes the engineering branch so a record's links resolve.

**Inputs:** Engineering worktree.

- Planning records go straight to the branch; they take no pull request.

```bash
cd '<engineering-worktree>' && git push
```

#### Add Planning Record

Adds the folder for one planning record on the long-lived engineering worktree.

**Inputs:** Engineering worktree and planning-folder path composed from the date, optional issue or pull request number, and slug.

- `<planning-folder-path>` is `artifacts/planning/<yyyy-mm-dd>[-<ref>]-<slug>/`. The date is the day the record is opened.
- `<ref>` is the bare number of the issue or the pull request the record is for. A record for ad hoc work, which has neither, has no ref segment.
- The slug is lowercase words separated by hyphens, a short name of the work.
- The folder's files are the [planning layout](#layout).
- Edits are made on that worktree. The engineering branch takes no further worktree and no branch.

```bash
mkdir -p '<planning-folder-path>'
```

**Example:**

```bash
mkdir -p artifacts/planning/2026-10-15-950-queue-plan
```

### Pull Request

#### Open Discussion Pull Request

Opens a draft for the supplied planning branch and body.

**Inputs:** Repository owner and name, title, planning branch, target branch and body file.

```bash
gh api --method POST 'repos/<owner>/<repository>/pulls' -f title='<title>' -f head='<planning-branch>' -f base='<target-branch>' -F body=@'<body-file>' -F draft=true
```

**Example:**

```bash
gh api --method POST repos/m2ux/workflow-server/pulls -f title='Queue Planning: Scope and Delivery' -f head=planning/queue -f base=engineering -F body=@discussion.md -F draft=true
```

#### Retarget Pull Request

Points a pull request at another base branch, such as its epic's base branch.

**Inputs:** Repository, pull request number and target branch.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/<pull-request-number>' -f base='<target-branch>' --jq .base.ref
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/950' -f base='i07/e00/main' --jq .base.ref
```

#### Fetch Pull Request

Appends one pull request, as one JSON line, to the supplied file.

**Inputs:** Repository, pull request number and destination JSON-lines file.

```bash
gh api 'repos/<owner>/<repo>/pulls/<pull-request-number>' --jq . >> '<pull-request-records-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/pulls/439' --jq . >> prs.json
```

#### Retitle Pull Request

Replaces a pull request's title.

**Inputs:** Repository, pull request number and complete title.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/<pull-request-number>' -f title='<title>' --jq .title
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/950' -f title='[I07:E00] Purpose' --jq .title
```

#### Open Task Pull Request

Creates a pull request from a unit's branch to its epic base.

**Inputs:** Repository, title, task head, epic base and populated body file.

- Supply the epic prefix and purpose as title, the task branch as head, the epic base as base, and the complete body file.

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='<title>' -f head='<task-branch>' -f base='<epic-base>' -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='[I07:E00] Purpose' -f head='i07/e00/w01-purpose' -f base='i07/e00/main' -F body=@body.md --jq .html_url
```

#### Open Epic Pull Request

Creates the draft pull request from an epic base to its long-lived target.

**Inputs:** Repository, title, epic head, long-lived base and populated review body file.

- Supply the epic prefix and name as title, the epic base as head, its long-lived branch as base, and the populated review body file.
- `draft` is true, including when the work is already complete.

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='<title>' -f head='<epic-base>' -f base='<long-lived-base>' -F draft=true -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/pulls' -f title='[I07:E00] Name' -f head='i07/e00/main' -f base='main' -F draft=true -F body=@body.md --jq .html_url
```

#### Patch Pull Request Body

Replaces a pull request's body.

**Inputs:** Repository, pull request number and complete populated body file.

- The file is the whole body. The issue a pull request delivers is linked on the pull request itself, so this call leaves that link standing.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/<pull-request-number>' -F 'body=@<body-file>' --jq .html_url
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/pulls/950' -F body=@pr-950.md --jq .html_url
```

#### Read Development Links

Returns the complete Development relation through authenticated GitHub or an available supported tool.

**Inputs:** Pull request identity and authenticated access.

Read the actual field across every page and state, recording repository and number for each linked issue. Return the links and whether the field was fully readable.

#### Set Development Link

Adds one pull request to an issue's Development relation.

**Inputs:** Pull request identity, issue identity, authenticated access and confirmed repository prerequisite.

Use [GitHub's sidebar linking procedure](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue): in the issue's Development selector, select the pull request's repository and pull request, including a different repository when required. Return the edit result.

#### Remove Development Link

Removes one selected Development relation.

**Inputs:** Pull request and issue identities, authenticated access and the user's decision authorizing removal of the abandoned or incorrect link.

Deselect the supplied relation in the authenticated Development selector and save the edit. Return the edit result.

#### Write Pull Request Links

Saves complete observed Development-linked issues as a JSON array.

**Inputs:** One complete relation per pull request, with all repository and number pairs, and destination link-snapshot file.

Write the supplied relations in this shape. Substitute numbers as JSON integers. Include each pull request and all its linked issues; use an empty array for a complete relation with no linked issues. Each repository is the one belonging to that pull request or issue.

```text
[
  {
    "repo": "<pull-request-owner>/<pull-request-repo>",
    "number": <pull-request-number>,
    "closingIssuesReferences": [{"repo": "<issue-owner>/<issue-repo>", "number": <issue-number>}]
  }
]
```

**Example payload:**

```json
[
  {
    "repo": "owner/repo",
    "number": 950,
    "closingIssuesReferences": [{"repo": "owner/repo", "number": 637}]
  }
]
```

#### Save Pull Request Snapshot

Saves one complete pull request response, replacing the destination file.

**Inputs:** Repository, pull request number and destination JSON file.

```bash
gh api 'repos/<owner>/<repo>/pulls/<pull-request-number>' > '<pull-request-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/pulls/980' > epic-pr.json
```

#### Fetch Pull Request Reviews

Saves every review on one pull request.

**Inputs:** Repository, pull request number and destination file.

```bash
gh api --paginate 'repos/<owner>/<repo>/pulls/<pull-request-number>/reviews?per_page=100' > '<reviews-file>'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/pulls/980/reviews?per_page=100' > reviews.json
```

#### Fetch Initiative Pull Requests

Saves the task and epic pull requests that name one initiative's epics.

**Inputs:** Repository, initiative prefix and destination JSON-lines file.

`<initiative-prefix>` includes the opening bracket and initiative id, matching its task and epic titles.

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("<initiative-prefix>"))' > '<pull-request-records-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I07"))' > prs.json
```

#### Fetch Pull Request Files

Saves the paths a pull request changes.

**Inputs:** Repository, pull request number and destination path-list file.

```bash
gh api --paginate 'repos/<owner>/<repo>/pulls/<pull-request-number>/files' --jq '.[].filename' > '<changed-paths-file>'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/pulls/950/files' --jq '.[].filename' > changed-files.txt
```

# Modes

## Align Mode

Brings one or more existing proposal, initiative, epic, task, and standalone issues and/or PRs into line with the plan they belong to and structurally aligns them with the guidelines they are held to. 

Alignment checks conformity to work-planning rules; judgement of content fitness belongs to goal review.

### Procedure

The main path meets [Outcomes](#outcomes).

1. **Discover every issue.**
   - Scope: issues the user names, an initiative with its open epics or a board with it's complete set of initiatives and epics.
   - Open issues only. A closed issue is aligned only when named.
   - Naming another initiative's issue approves format edits to it.
   - An open standalone issue that an aligned initiative, epic, or task cites is aligned with it.
2. **Fetch each issue.**
   - Use [Read Tracker Issue](#read-tracker-issue) for its JSON and body.
   - A board fetch includes every initiative it holds.
   - An initiative's fetch includes every epic its table links, closed epics included, as supplied context for validation.
   - The fetch includes each source the initiative's References mark, for an epic as for the initiative.
   - A closed epic's own body is checked only when the epic is named.
3. **Validate the bodies.**
   - Call [Validate Proposal Body](#validate-proposal-body), [Validate Initiative Body](#validate-initiative-body) or [Validate Epic Body](#validate-epic-body) for that kind.
   - Run [Validate Issue Body](#validate-issue-body) with [task field conditions](#task-body) or [standalone field conditions](#standalone-body-1) for those bodies.
   - Supply the fetched context and output files.
   - Route the returned [Format Findings](#format-findings) through the following steps.
4. **Publish mechanical fixes.**
   Confirm the returned diff changes structure only.
   - Publish that body and the returned title or label corrections through [Save Tracker Issue](#save-tracker-issue), without asking.
5. **Review the goal.**
   - For initiative or epic scope, follow [Review Initiative Goal](#review-initiative-goal) with the current initiative and epic evidence, confirmed goal clauses and marked sources.
   - For proposal, task or standalone scope, run [Check Round of Edits](#check-round-of-edits) with the selected body, its kind's field conditions and format inputs; skip initiative goal review when no initiative is in scope.
   - Present each finding through [Report Review Finding](#report-review-finding). Numbering changes affect only rows no pull request names.
6. **Resolve content decisions.**
   Decide each non-mechanical finding with the user.
   - Pass confirmed local resolutions to [Apply Body Corrections](#apply-body-corrections), using the selected kind's template and field conditions.
   - Move initiative boundaries found as Non-Goals in an epic or task into the initiative's Non-Goals.
   - Remove the misplaced section.
   - For a standalone body, call [Revise Standalone Body](#revise-standalone-body).
   - Pass confirmed task splits and Coverage corrections to [Revise Epic Rows](#revise-epic-rows).
   - Replace an epic a task row names with the rows it consumes when correcting dependencies through the dependency step.
   - For a wrong-kind body:
     - Confirm either its rewrite to the intended template or its tracker kind/title change.
     - Keep the initiative row consistent with any epic title change.
   - When several row ids link one issue, obtain the user's choice between one issue per task and a shared reference.
   - For a shared reference:
     - Remove the row links.
     - Cite that issue under the epic's References.
   - Publish returned bodies and metadata through [Save Tracker Issue](#save-tracker-issue).
   - Validate the affected bodies again.
7. **Check criteria.**
   Check every acceptance criterion of the issues being aligned against [Requirement Characteristics](#referencesrequirement-characteristics), through [Verifiable](#verifiable).
   - Report each that fails it. The alignment is not clear while a criterion that fails the characteristics remains, and a finding from this check is not one the user keeps.
   - Align the criteria with the sources the initiative's References mark, as [Sources](#sources) defines.
   - Report each departure and each gap.
   - Draft the criterion a gap calls for.
   - Decide it with the user.
   - The alignment is not clear while a marked source stays unread. A source whose link is dead is repaired, or the mark is removed and the criteria it bound are decided with the user.
   - A departure from a marked source is corrected in the criterion, unless the user records the departure as a Non-Goal.
8. **Check dependencies.**
   Check them whenever an initiative or epic is aligned.
   - Take the initiative's body and every epic's body with [Read Tracker Issue](#read-tracker-issue).
   - Take each task row's work-item file from the planning record that registered it, which holds one per task whatever that row currently links, so contention is measured rather than reported as unchecked.
   - Follow [Check Dependencies and Numbering](#check-dependencies-and-numbering) with those bodies, those work-item files, current pull request records, confirmed maps when any, and explicitly authorized outside-initiative files.
   - Resume this alignment with its checked bodies or unresolved findings.
   - Put each problem it reports to the user. An initiative Depends on cell takes the epics it derives, as [Work Breakdown](#work-breakdown-1) states.
9. **Coverage.**
   When no initiative or epic is selected, continue at step 13, Re-run.
   - For initiative or epic scope, run [Read Delivery Evidence](#read-delivery-evidence) for the selected initiative and epics.
   - Continue with its returned records.
   - For each epic being aligned, run [Record Epic Delivery](#record-epic-delivery) with its current JSON, returned pull request records and complete issue-link snapshot, task records, confirmed matches, project checkout and output body file:
     - **Unmet.**
       - Each task [Record Epic Delivery](#record-epic-delivery) reports unmet is a gap.
       - Follow [Plan Gap Task](#plan-gap-task) with the current epic JSON and body, delivered task row, unmet criterion ids, delivery records, complete issue-link snapshot and output body path.
       - For each criterion it returns as already holding, run [Verify Selected Criteria](#verify-selected-criteria), pass the verified ids to [Tick Verified Criteria](#tick-verified-criteria), and publish through [Save Tracker Issue](#save-tracker-issue).
     - **Repair.**
       - Repair Done cells as [Tables](#tables) states.
       - When the preceding Record Epic Delivery call reports a row done, or a tick cleared, run [Save Tracker Issue](#save-tracker-issue) from the output body file, without asking.
     - **Absent.**
       - Fetch a linked pull request missing from the records with [Read Pull Request State](#read-pull-request-state).
       - Repeat Record Epic Delivery with the refreshed records and the same output body file.
     - **Unlinked.**
       - For a criterion ticked while its row links no pull request and no commit, request issue discussion through [Read Tracker Issue](#read-tracker-issue).
       - Link the one delivery that discussion names, taking a path as the commit that holds it. Several candidates, or none, go to the user before linking.
       - Repeat Record Epic Delivery with the corrected evidence and the same output body file.
   - For an initiative being aligned:
     - Run [Record Initiative Delivery](#record-initiative-delivery) with the current initiative JSON, every linked epic's current JSON and an output body file.
     - Present the returned [Delivery Findings](#delivery-findings-1) to the user.
   - When the user chooses to verify ready criteria now:
     - Run [Verify Selected Criteria](#verify-selected-criteria) with those criterion ids, current initiative body, delivery findings, delivery revisions, named instruments and the project checkout.
     - Pass only returned verified ids to [Tick Verified Criteria](#tick-verified-criteria), with the current initiative JSON, all linked epic records and output body file.
     - Publish the returned body through [Save Tracker Issue](#save-tracker-issue).
     - Report failed verification or deferred findings as pending; no criterion is ticked for them.
   - Apply a Done change in the output body through [Save Tracker Issue](#save-tracker-issue), without asking.
   - Report criterion evidence as [Coverage Reports](#coverage-reports) defines.
10. **Branches.**
    For each open epic of the selected initiative:
    - Run [Check Epic Prerequisites](#check-epic-prerequisites) with the current initiative and epic bodies and prerequisite issue and base-merge records.
    - Pass only a confirmed result, project checkout, epic identity and changed long-lived branches to [Prepare Delivery Bases](#prepare-delivery-bases).
    - Return missing prerequisite evidence before creating a base.

    After preparing the bases, align the selected initiative's pull requests:
    - Read the pull requests through [Read Initiative Pull Requests](#read-initiative-pull-requests).
    - Read each open epic's branches through [Read Delivery Branches](#read-delivery-branches). Unevaluable branch names stop this step with a finding.
    - Use the returned long-lived target; for example, `main` and `i07/e00/main` identify the same target.
    - Point an open task pull request at its epic base with [Publish Pull Request](#publish-pull-request).
    - When that pull request is not mergeable, [Update Task Branch](#update-task-branch) merges the epic base into the task branch. A conflict is reported and the pull request stays open.
    - An open pull request whose head is an epic base targets its corresponding long-lived branch.
    - A merged pull request is left as merged.
    - A base that is none of these is put to the user.
11. **Unplaced task issues.**
    For each task issue returned as unplaced by [Record Epic Delivery](#record-epic-delivery):
    - Draft its row against [Work Breakdown](#work-breakdown).
    - Confirm it with the user; an unanswered placement stays pending.
    - Apply the confirmed row through [Revise Epic Rows](#revise-epic-rows).
    - Publish the returned body through [Save Tracker Issue](#save-tracker-issue).
    - Repeat Record Epic Delivery with the saved epic JSON, current task records, pull request records, complete issue-link snapshot and the same output body file. An unanswered placement stays pending.
12. **Review pull requests.**
    Run [Record Epic Delivery](#record-epic-delivery) for each open epic.
    - Open a reported base as a draft review pull request.
    - Leave the epic open. The user marks the draft ready when the epic is complete.
13. **Re-run.**
    After a published correction:
    - Fetch the changed bodies.
    - Repeat steps 3–12 for the affected issues with refreshed delivery evidence.
    - Stop when the checks are clear or every remaining finding is one the user chose to keep. A finding from the criteria check is not one the user keeps. The alignment is not clear while a criterion that fails [Requirement Characteristics](#referencesrequirement-characteristics) remains.

    With or without a correction:
    - Report what changed on each issue, including each finding the criteria check reported.

### Outcomes

- **Issues brought into line.**
  The issues the user named, or an initiative and its open epics, agree with the plan they state, and the user has decided what still needs a judgement.
- **Delivery brought into line.**
  Each epic's recorded delivery matches the pull requests that landed, and a gap the user accepts is drafted with them.
- **Branches brought into line.**
  Each open epic's branches follow the delivery structure.

# References/Requirement-Characteristics

The characteristics an acceptance criterion meets, and the characteristics a set of them meets. Condensed from ISO/IEC/IEEE 29148:2018, clauses 5.2.4 to 5.2.7.

## Individual

Each criterion has these characteristics.

- **Necessary.**
  It states a capability, constraint, or quality the work must have. Leaving it out leaves that need unmet, and no other criterion meets it. It applies now.
- **Appropriate.**
  The detail matches the level of the work. It states what holds, and does not lock in a design the need does not require.
- **Unambiguous.**
  It can be read in only one way.
- **Complete.**
  It states the condition fully. Knowing whether it holds does not depend on some other text.
- **Singular.**
  It states one capability, constraint, or quality. Several conditions under which that one thing holds are still one criterion.
- **Feasible.**
  It can be met within the cost, schedule, and technical bounds of the work, at an acceptable risk.
- **Verifiable.**
  Its wording lets the realisation be proved, at the level the criterion is written, by inspection, analysis, demonstration, or test. A measure makes that proof easier.
- **Correct.**
  It states the need it came from, accurately.
- **Conforming.**
  It follows the acceptance-criterion form: an end state, one invariant, and a named instrument.

## A Set

The criteria of one issue, taken together, have these characteristics.

- **Complete.**
  Together they state what the work must achieve. Nothing the set needs is left to be defined later.
- **Consistent.**
  No two conflict or overlap. The same word means the same thing throughout.
- **Feasible.**
  The set can be met within the same cost, schedule, and technical bounds, at an acceptable risk.
- **Comprehensible.**
  A reader can see what the work is expected to achieve, and how that sits with the rest of the plan.
- **Able to be validated.**
  Meeting the set achieves the need the plan states, within its constraints.

## Wording

- **What, not how.**
  A criterion states the condition that holds. A design choice belongs in the Proposal.
- **Bounded words.**
  These make a criterion hard to prove, or open to more than one reading, unless a measure defines them:
  - superlatives, such as best or most;
  - subjective praise, such as easy or robust;
  - vague pronouns, such as it or this;
  - open comparatives, such as better or significant;
  - loopholes, such as if possible or as appropriate;
  - words of totality, such as all, always, or never, unless the set they cover is named;
  - an open-ended promise, such as provide support.
- **Assumptions.**
  An assumption is recorded beside the criterion, in the Problem or the Proposal. It is not written as the criterion.
- **Definitions.**
  A definition is a statement of what a term means. It is not a criterion.
