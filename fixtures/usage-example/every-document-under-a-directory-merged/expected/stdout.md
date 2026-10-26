# Hoist Mode

Brings the chosen standalone issues into the agent-engineering structure, or leaves them open according to the user's decision.

Follow the [Procedure](#procedure), adhering to [Rules](#rules) and [Conventions](#conventions) and ensure all [Outcomes](#outcomes) are met.

## Procedure

1. **Fetch.**
   Fetch every issue with [Read Repository Issues](#read-repository-issues).
2. **List candidates.**
   Apply [Find Placement Candidates](#find-placement-candidates) with the complete issue collection.
   - Use its candidates and available destinations for triage.
3. **Triage.**
   Read each candidate's body and discussion through [Read Tracker Issue](#read-tracker-issue), with the initiative and epic bodies whose themes or criteria it touches.
   - Supply that evidence and planning-record references to [Draft Issue Placement](#draft-issue-placement) for each option.
   - Order the returned options best first, with Leave last.
4. **Decide each placement.**
   Apply [Check Plan Change Autonomy](#check-plan-change-autonomy) for each orphan's best option that changes the plan, with the allowance the caller supplied.
   - An automatic option is confirmed as it stands, and recorded through [Record Plan Change](#record-plan-change).
   - A held option is settled as [Held Change](#held-change) states, leaving the orphan where it is.
   - An option put to the user is offered as an [interview](#rules). The grounding paragraph says what the orphan asks and where it fits.
     - Leave is last.
     - Placing an orphan in another initiative's issue needs that answer as its approval.
   - A caller naming the placement, settled with the user before the hoist, has it applied rather than offered again.
5. **Apply.**
   Apply [Apply Issue Placement](#apply-issue-placement) with each confirmed placement and its current source and destination records.
   - After it returns the saved destination, run exactly one disposition procedure with the returned destination and source records: [Rewrite Orphan Issue](#rewrite-orphan-issue) for kept or left issues, or [Subsume Orphan Work](#subsume-orphan-work) for work taken by another issue.
   - Resume review.
6. **Review.**
   - Apply [Validate Issue Body](#validate-issue-body) to every issue the hoist changed or created.
   - Apply [Check Dependencies and Numbering](#check-dependencies-and-numbering) to each initiative that gained a task or epic.
   - Resolve each finding as [Check Plan Change Autonomy](#check-plan-change-autonomy) returns it: an automatic correction is applied, and a held one is settled as [Held Change](#held-change) states.
   - Apply confirmed body corrections through [Apply Body Corrections](#apply-body-corrections).
   - Publish through [Save Tracker Issue](#save-tracker-issue).
   - Repeat Validate Issue Body with the saved affected bodies.
   - Repeat Check Dependencies and Numbering with the saved affected bodies.
   - Report any unresolved finding.
7. **Report.**
   Report each orphan's placement, the issues changed, created or closed, and the orphans left.
   - Return the [change list](#change-list) with it, so the caller reports each placement this mode made and each it held.

## Outcomes

- **Each orphan placed.**
  The user has each chosen standalone issue joined to an initiative, epic or task, or left open.
- **Cited work included.**
  A standalone issue an agent-engineering issue cites is placed, or taken into the issue that already carries that work.
- **The decision respected.**
  An orphan moves on the user's word, or on the allowance its caller supplied, and work needing a decision outside that allowance stays where it is.

# Rules

- **Decisions.**
  A question the user must decide is put as an interview, one question at a time. A decision the run's [allowance](#allowance) covers is taken with its recommended option rather than asked. Record each decision in the affected issues and, when there is one, the planning record.
  - A plain-language paragraph before the question gives the context the user needs to answer it.
  - The question offers more than one choice. The recommended choice is marked on its option.
  - Wait for the user's answer. An unanswered question stays pending. A recommendation or elapsed time supplies no answer.
  - The user can select Other and specify a response beyond the options.
  - Use the native tool for presenting the question when one is available.
- **Bootstrap.**
  A link whose text opens with a symbol is compiled and used as the [bootstrap](#bootstrap) states.
- **Layers.**
  Modes, protocols, artifacts. A mode aggregates protocol calls, as an application calls services; a protocol applies artifact operations and follows other protocols; an artifact does neither. A call goes down the stack, never up. A mode reaches an artifact operation directly only where no protocol owns that change.
- **Execution.**
  A call passes its named inputs. A protocol is one change that lands in several artifacts together, and is followed whole. Follow another mode, a protocol or a named procedure subsection, and apply an artifact operation, only where the procedure calls for it; finish that call and return its result before continuing, unless the procedure explicitly dispatches concurrent work.

# Conventions

- **Session.**
  Once per session, before the first `gh` call, unset `GH_TOKEN` and `GITHUB_TOKEN` so `gh` uses its keyring login. Where shell state does not persist between commands, confirm instead that neither is set in the shell profile.
- **Repository.**
  `gh` resolves `{owner}/{repo}` from the git remote of the directory it runs in, so run `gh` commands inside a checkout of the repository that holds the issues. `{other}` is a further repository the board's issues live in.
- **Bodies.**
  - Bodies and long comments always go through a file (`-F body=@file`), never inline, which avoids quoting.
  - **Example.**  workflow-server's dynamic-shell restrictions deny a body inlined in the command.
  - Keep these files in a working directory outside the repository.
- **Scripts.**
  Scripts run under `sbx`, invoked by its absolute path from `<workspace>`, the checkout holding this skill.
- **Boards.**
  A project board sits under `users/{owner}`, or `orgs/{owner}` when `gh api repos/{owner}/{repo} --jq .owner.type` is `Organization`.
- **Example values.**  Substitute the real ones:
  - `936` an initiative issue, `943` and `937` its epics, `637` a task issue, `874` an orphan, `946` an initiative off the board, `960` a proposal;
  - `950` a pull request, `I07` and `I08` initiative numbers;
  - board `9`, workflow-server's Canon theme, and `419167630` its Status field id;
  - `1` the Initiative Template board, `13` a board copied from it;
  - `14` the Proposals Template, `15` the Proposals board;
  - `m2ux` the user.
  - `<checkout>` any checkout of the project, a linked worktree included.

# Artifacts

## Issue

### Operations

#### *Read* Tracker Issue

The current issue, its saved body and discussion.

**Inputs:** Repository, issue number and output files; whether discussion is needed.

1. Run [Fetch Tracker Issue](#fetch-tracker-issue) for the complete JSON, or [Fetch Issue Body](#fetch-issue-body) for its body, with the issue number and destination file.
2. Run [Fetch Issue Comments](#fetch-issue-comments) when the request depends on the discussion.

#### *Save* Tracker Issue

One populated body and its metadata, written to the tracker.

**Inputs:** Repository, optional existing issue number, populated body file, title and labels for creation; selected body or metadata changes for an existing issue; each assigned label's colour and description. Optional comment file.

1. Take the supplied body and metadata, preserving each field the caller does not change for an existing issue.
2. Apply [Ensure Repository Labels](#ensure-repository-labels) with every label the save assigns and its colour and description.
   - Return an unknown label definition to the caller before any write.
3. For a new issue, run [Create Tracker Issue](#create-tracker-issue) with the body's file, title and labels.
4. For an existing issue, run [Patch Issue Body](#patch-issue-body), [Retitle Tracker Issue](#retitle-tracker-issue), [Add Issue Labels](#add-issue-labels) or [Remove Issue Label](#remove-issue-label) for the fields being changed.
5. Apply [Comment on Issue](#comment-on-issue) for an answer or a preserved body the caller requires, with the issue number and comment file.
6. Re-read with [Fetch Tracker Issue](#fetch-tracker-issue).
7. Compare the saved fields with the intended body and metadata.

#### *Close* Transferred Work

An issue whose work is tracked by another issue.

**Inputs:** Issue identity, confirmed destination evidence and comment file.

1. Confirm the supplied destination contains the work and cites its source issue.
2. Apply [Comment on Issue](#comment-on-issue) with the destination reference and supplied comment file.
3. Run [Close as Not Planned](#close-as-not-planned), retaining the issue's body.
4. Re-read it with [Fetch Tracker Issue](#fetch-tracker-issue) to confirm its state and reason.

#### *Comment* on Issue

The supplied discussion text saved on one issue.

**Inputs:** Repository, issue number and exact comment text or file; reviewer identity and addressed feedback when replying to a review.

1. When replying to feedback already folded into the body, compose a precise, factual reply addressing each point and mentioning the reviewer, with no thanks or filler. Name what the body now says, by criterion id where one carries it, or the issue that takes the point.
2. Publish the supplied comment:
   - For a one-line comment, run [Post Inline Comment](#post-inline-comment) with the exact text.
   - For a longer comment, run [Post Comment File](#post-comment-file) with the complete file.
3. Return the saved comment URL.

#### *Read* Repository Issues

The issue collection used for repository-wide selection.

**Inputs:** Repository and destination JSON file.

1. Run [Fetch All Issues](#fetch-all-issues), saving the complete collection.
2. Return it with pull requests distinguishable from issues.

### Commands

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

#### Close as Not Planned

Closes an issue whose work another issue tracks.

**Inputs:** Issue identity and confirmed evidence that the work is tracked by its recorded destination.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f state=closed -f state_reason=not_planned --jq .state
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/874' -f state=closed -f state_reason=not_planned --jq .state
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

#### Fetch All Issues

Saves every issue in the repository; the scripts skip the pull requests among them.

**Inputs:** Repository and destination JSON file.

```bash
gh api --paginate "repos/<owner>/<repo>/issues?state=all&per_page=100" > '<issues-json-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/issues?state=all&per_page=100" > issues.json
```

## Placement

### Operations

#### *Draft* Issue Placement

The placement options for one orphan, from the supplied orphan and candidate destinations.

**Inputs:** Current orphan body, candidate destinations, proposed work and supplied planning-record references.

1. Identify each option among an existing task, a new task, a new epic, a new initiative, and Leave.
2. For each option, record the destination and the work it takes, meeting [Fields](#fields).
3. For each option, record whether the orphan is kept, subsumed or left, meeting [Disposition Conditions](#disposition-conditions), including the reason, the original-body preservation requirement and any planning record reference.
4. Return the options for the caller to offer and apply, each a [Placement](#placement-record) with its draft issue changes, in the order that field states.

#### *Find* Placement Candidates

The issue candidates and available destinations from supplied records.

**Inputs:** Complete repository issue collection.

1. Run [List Orphans](#list-orphans) with the supplied issue file.
2. Return the [Candidate Issues](#candidate-issues) and open initiative and epic destinations for the caller to investigate.

#### *Apply* Issue Placement

One selected destination for an orphan's work.

**Inputs:** Confirmed placement, current source and destination records, and the affected initiative and epic bodies.

1. Execute only the branch matching the confirmed destination:
   - **Existing task.**
     - Add the orphan's outcomes to the task criteria.
     - Add its design to Proposal.
     - When they exceed the epic's criteria, add epic criteria cited by the task row.
     - Publish the affected bodies through [Save Tracker Issue](#save-tracker-issue).
   - **New task.**
     - Apply [Populate Epic Issue Body](#populate-epic-issue-body) with the confirmed task scope, current epic context and output path.
     - Add the epic criteria the row's Coverage needs where the orphan's outcomes exceed the epic's, as [Destination Work](#destination-work) states.
     - Link the kept orphan's issue in the row's Task cell, as [Task Delivery](#task-delivery) states for a task with its own issue. A subsumed orphan leaves the cell holding the row id alone until the work is planned and the row gains its work-item file.
     - Number the row where it can start.
     - When movable rows change number, apply [Check Dependencies and Numbering](#check-dependencies-and-numbering) with the affected initiative and epic drafts and confirmed numbering map.
     - Publish the checked bodies through Save Tracker Issue.
   - **New epic.**
     - Apply [Populate Epic Issue Body](#populate-epic-issue-body).
     - Populate the covering row through [Draft Initiative Issue Body](#draft-initiative-issue-body).
     - Publish the epic through [Save Tracker Issue](#save-tracker-issue).
     - Link its issue in the initiative row.
   - **New initiative.**
     - Apply [Populate Initiative Issue Body](#populate-initiative-issue-body) from the orphan's scoped problem and confirmed goal.
     - Publish through [Save Tracker Issue](#save-tracker-issue).
   - **Leave.**
     - Use the source issue as the destination with disposition Leave. The caller rewrites its standalone body and keeps the issue open.
2. Return the saved destination, the identities of all affected bodies and the confirmed disposition to the caller, including the destination epic and row for a new task. The caller performs the rewrite or closure.

#### *Rewrite* Orphan Issue

The selected layout, with the original wording preserved for readers.

**Inputs:** Source issue identity, selected destination kind, and the evidence and design the body carries.

1. Fetch the body and discussion live with [Read Tracker Issue](#read-tracker-issue).
   - Post the body word for word through [Comment on Issue](#comment-on-issue), preceded by the line in [Original Body](#original-body) and a blank line.
   - Skip the comment where the discussion already carries one, since a second hoist of the same issue would otherwise repeat it.
2. Use the selected [Populate Task Body](#populate-task-body), [Populate Epic Issue Body](#populate-epic-issue-body), [Populate Initiative Issue Body](#populate-initiative-issue-body) or [Populate Standalone Body](#populate-standalone-body) body.
   - Carry evidence into Problem and design into Proposal.
3. Apply [Check Round of Edits](#check-round-of-edits) with the populated body and selected kind conditions before publishing.
   - Resolve findings.
   - Apply [Save Tracker Issue](#save-tracker-issue) with the validated body, title and labels.
   - Return the saved identity to the caller.

#### *Subsume* Orphan Work

The work remains tracked by the taking issue.

**Inputs:** Orphan identity and body, confirmed destination evidence, and the planning record it references when it has one.

1. Transfer the work to the taking issue.
   - Make each outcome a criterion of one invariant.
   - Put the design in Proposal.
   - Cite the orphan and any planning record in References.
2. Prepare the comment file naming the taking issue and task, for example `Tracked in [I07:E01](…/issues/937) W04.` The closure operation records it once.
3. Apply [Close Transferred Work](#close-transferred-work) with the orphan identity, confirmed destination evidence and closure comment file, retaining the orphan's body.
   - Return the confirmed closure or blocker to the caller.

### Fields

- **Source.** The orphan's repository, issue number and current body.
- **Destination.** The selected issue or proposed work, with the criteria and design it takes.
- **Disposition.**
  Kept, subsumed or left, with a reason. A referenced planning record is carried with the source reference.
- **Draft bodies.**
  Each proposed body meets its own kind's shape and states the result. It carries no account of how the work arrived. A source reference says what detail it holds.
- **Links.**
  An initiative row identifies its epic issue. A task issue has its delivery link through Development.
- **Preservation.**
  A kept or left issue has the complete original-body comment ready before its rewrite. A subsumed issue retains its body.

#### Placement Record

| Destination | Work | Issue Disposition |
| --- | --- | --- |
| Existing task | Criteria and design in a task that has its own issue | Subsumed |
| New task | A row in an existing epic, with its criteria | Kept or subsumed |
| New epic | An epic in an existing initiative | Kept or subsumed |
| New initiative | An initiative | Kept or subsumed |
| Leave | Work outside the initiative structure | Left open |

Placement options are offered best first, the destination that most nearly holds the orphan's work leading, with Leave last.

#### Original Body

The comment starts with `The body before this issue took the [I07:E01:W04] layout:` for a kept issue, or `The body before this issue took the standalone layout:` for one left in place. A blank line separates that lead from the complete original body.

#### Disposition Conditions

A source with a planning-record reference is subsumed, with that folder cited beside the source in the destination. Otherwise the source is kept when its work needs its own discussion or evidence, and subsumed when its detail fits in rows, criteria and a reference. Work an existing criterion already states is subsumed into the issue holding that criterion, without a new row; for cited standalone work this is usually the citing issue.

#### Candidate Issues

Candidates are open issues without an agent-engineering prefix. Orphans have no incoming link from an open initiative, epic or task. Cited standalone issues have such a link in prose or References; their records include labels, citing issues and any linked planning folder. An investigation cited by an epic is a candidate, with disposition determined from supplied criteria.

#### Destination Work

An existing-epic option identifies the row to add, with Description, criteria, Depends on and Joins, or the existing task already delivering the work. Leave applies when no initiative goal covers it or it is not planned work. Each option names whether the source is kept or subsumed.

### Commands

#### List Orphans

Lists the hoist candidates, and the open initiatives and epics they could join.

**Inputs:** Complete supplied repository issue collection.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/orphans.py '<issues-json-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/orphans.py issues.json
```

## Plan Change

### Operations

#### *Check* Plan Change Autonomy

One pending change assessed against the run's allowance.

**Inputs:** The pending change, its subject, the option recommended for it, and the allowance the caller was supplied.

1. Match the change to one kind in [Change Kinds](#change-kinds).
2. Return it as automatic where the supplied allowance names that kind, with the supplied recommendation as the option the caller applies.
3. Return it as [held](#held-change) otherwise.
   - A change matching no kind is held, as is one matching [Initiative Creation](#initiative-creation).
   - An absent allowance holds every change, so a run the user drives decides nothing on their behalf.

#### *Record* Plan Change

One entry in the run's list, for a change it applied or held.

**Inputs:** The change, its kind, the option applied or recommended, the affected issue identities and the run's current list.

1. Add one entry meeting [Entry](#entry) to the supplied [Change List](#change-list), marked applied or held.
2. Return the updated list for the caller to publish and report.

#### *Settle* Plan Change

One pending change carried to its outcome: applied, held, or answered by the user.

**Inputs:** The pending change, its subject, the option recommended for it, the affected issue identities, the allowance the caller was supplied, and the run's current [Change List](#change-list).

1. Apply [Check Plan Change Autonomy](#check-plan-change-autonomy) with the change, its subject, the recommended option and the supplied allowance.
2. Settle the change by what it returns:
   - **Automatic.**
     - Take the recommended option as the applied option.
     - Apply [Record Plan Change](#record-plan-change) with the change, its kind, that option, the affected issue identities and the current list, marked applied.
   - **Held, with an allowance supplied.**
     - Leave the change unapplied, meeting [Held Change](#held-change).
     - Apply Record Plan Change with the change, its kind, the recommended option, the affected issue identities and the current list, marked held.
     - Ask nothing, since the work the run was dispatched for does not wait on an answer.
   - **Held, with no allowance supplied.**
     - Put the change to the user as an [interview](#rules), with the recommended option marked, and wait for the answer.
     - Where the answer applies a change, apply Record Plan Change with the change, its kind, the option the user chose, the affected issue identities and the current list, marked applied.
     - An answer leaving the work where it is takes no entry, as [Change Kinds](#change-kinds) states.
3. Return the applied option, held, or the user's answer, with the updated change list.

### Fields

#### Allowance

The caller names the change kinds its run applies without asking. A run the user drives directly is supplied none.

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

#### Change List

One list for the run, holding every change it applied and every change it held. It is what the run reports and what its record keeps.

#### Entry

One line: the kind, the issue or row it concerns, and the option applied or recommended. The entry states the change, not the alternatives weighed against it.

#### Held Change

A held change is left unapplied and its subject stays as it stands, so the next run sees the same decision. Its entry carries the recommended option, which is what the user is answering.

## Issue Body

### Operations

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

1. Check each section of the issue against the field conditions for its kind and against [Fields](#fields-2) in this file.
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

### Fields

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
- Meets [Requirement Characteristics](#requirement-characteristics).
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

### Commands

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

## Dependency Graph

### Operations

#### *Check* Dependencies and Numbering

The task graph and the row numbers it permits, checked and renumbered across the supplied bodies.

**Inputs:** Initiative and epic bodies or local drafts, the planning record that registered each task row, current pull request records, confirmed numbering maps when any, the caller's change allowance when it has one, the run's current [change list](#change-list), and explicitly authorized outside-initiative files.

1. Use the supplied local drafts when reviewing unpublished work.
   - For published issues, fetch the initiative and each epic body with [Read Tracker Issue](#read-tracker-issue).
   - Read each task row's work-item file from the planning record that registered it, as its [Artifacts](#artifacts-1) list it. The record holds one per task whatever that row currently links, so contention is measured rather than reported as unchecked.
   - Run [Check Dependencies](#check-dependencies) with the initiative body, every epic body, every work-item file read and each record file accounting for independent pairs.
2. Settle each finding through [Settle Plan Change](#settle-plan-change), with the correction below as its recommended option, the affected issue identities, the supplied allowance and the current change list.
   - The correction each finding takes:
     - Name the producing row for each consumed output, meeting [Edges](#edges), replacing an epic a task row names with the rows the task consumes.
     - Read tasks for implied consumption edges.
     - Account for every independent pair as [Joins](#joins) states.
     - Account for every contending pair as [Component Contention](#component-contention) states: the proposed map separates the two epics by a number, or the contending rows move into one epic.
     - Resolve backward references by moving work to the epic owning its inputs, or removing duplicate work already owned there. Work claimed twice has one owner and a boundary in both bodies.
   - Make the correction Settle Plan Change returns as applied, or the one the user's answer chooses, carrying its updated change list into the next finding.
   - Keep each held finding unresolved.
3. Renumber the confirmed maps, preserving the numbers [Numbering Map](#numbering-map) protects.
   - For a confirmed epic map, run [Renumber Epics](#renumber-epics) with current pull request records and every affected body.
   - For a confirmed task map, run [Renumber Tasks](#renumber-tasks) with the initiative and epic identities, owning epic body, confirmed old-to-new task-number map and every affected body file.
   - Re-sort rewritten tables.
   - Inspect every reported range.
   - Search prose for references the script cannot see.
   - Repeat Check Dependencies after each edge or numbering change until it reports no problem but the held findings.
   - Return the checked bodies, the printed longest chains, each printed contending pair, the proposed [Epic Priority](#epic-priority) map, the updated change list and the unresolved findings to the caller; do not publish a failed renumbering.

### Fields

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

### Commands

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

## Repository Labels

### Operations

#### *Ensure* Repository Labels

The required label definitions available for issue publication.

**Inputs:** Repository and required label names, colours and descriptions.

1. Run [List Labels](#list-labels) for the repository.
2. Compare the returned labels with the supplied required names.
3. Run [Create Label](#create-label) for each absent required definition.
4. Return the available labels; an unknown definition is a finding for the caller to resolve before publication.

### Commands

#### List Labels

Lists the labels that exist in the repository.

**Inputs:** Repository.

```bash
gh api "repos/<owner>/<repo>/labels?per_page=100" --jq '.[].name'
```

#### Create Label

Creates the label specified by its name, colour and description.

**Inputs:** Repository, label name, colour and description.

```bash
gh api --method POST 'repos/<owner>/<repo>/labels' -f name='<label>' -f color='<hex-colour>' -f description='<description>' --jq .name
```

## Epic Issue Body

Populates one epic body. The body states one slice of the design and lists the tasks that deliver it.

### Operations

#### *Populate* Epic Issue Body

One epic body and its local validation findings.

**Inputs:** Initiative context, epic scope, draft title and labels, criteria, proposed task rows, available pull request records, corpus branch and output path.

1. Populate the body from the [Template](#template) at the supplied output path.
   - Every section must meet [Fields](#fields-4).
   - Shared content must meet the common [body conditions](#fields-2).
2. Populate the shared table through [Write Issue Table](#write-issue-table).
3. Fill the epic-specific cells.
   - Each row must meet [Work Breakdown](#work-breakdown).
4. Apply [Build Body Snapshot](#build-body-snapshot) with the draft body, title, labels and existing issue JSON when present.
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
3. Publish the returned body through [Save Tracker Issue](#save-tracker-issue).
4. Return the saved body with each task id linked to its lowercase work-item file inside the reserved folder, meeting [Task Delivery](#task-delivery).

#### *Validate* Epic Body

The body's local format and field findings.

**Inputs:** Epic JSON, initiative context, current pull request records, corpus branch and output file.

1. Apply [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#fields-4), supplied related evidence and output file, supplying initiative JSON as `--initiative`, pull requests as `--prs` and corpus branch as `--corpus`.
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
   - On acceptance, apply [Revise Epic Rows](#revise-epic-rows) with the further row and the criteria it adopts from the delivered task's Coverage.
   - Return an unanswered draft as pending without continuing to the reconcile step.
3. Apply [Record Epic Delivery](#record-epic-delivery) with the revised epic and the supplied delivery evidence.
   - Publish the returned body through [Save Tracker Issue](#save-tracker-issue).
   - Return the saved row and criterion disposition to the caller. Done follows [Tables](#tables).

#### *Place* Unplaced Task Row

One epic body given the row its table lacks for a task issue of the epic.

**Inputs:** Epic JSON, the unplaced task issue, the run's allowance and change list when supplied, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches, project checkout and output body file.

1. Draft the task issue's row, meeting [Work Breakdown](#work-breakdown).
2. Apply [Settle Plan Change](#settle-plan-change) with the drafted row as a task creation, the task issue as its subject, the drafted row as the recommended option, the epic and task issue identities, the supplied allowance and the change list.
   - Return a row left held, unanswered or declined to the caller as pending, with the updated change list, without continuing to the revise step.
3. Apply [Revise Epic Rows](#revise-epic-rows) with the row as applied.
4. Publish the returned body through [Save Tracker Issue](#save-tracker-issue).
5. Apply [Record Epic Delivery](#record-epic-delivery) again with the saved epic JSON and refreshed task issue records, retaining the pull request records, complete issue-link snapshot, confirmed matches, project checkout and output body file.
6. Return the recorded body, its [Delivery Findings](#delivery-findings) and the change list to the caller.

### Fields

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
- **The audit row is a unit of its own.**
  It is joined to no other row, so its Joins cell is empty.
- **A finding closes by a fix on this epic's branch or by an issue that takes it.**
  Outstanding means neither.
- **Definitions change when a task row's work reaches the branch the corpus lives on.**
  A row that only changes the engine, continuous integration or the workspace does not bring the criterion.

#### Task Delivery

- **Holds.**
  - A unit's record exists and its rows link it before its session starts.
  - A row another session holds is not dispatched.
  - A held row stays held while its session plans and implements. The pull request's link replaces the record's link, which frees the row.
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

### Commands

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

## Initiative Issue Body

### Operations

#### *Populate* Initiative Issue Body

One initiative body and its local validation findings.

**Inputs:** Scoped proposal, confirmed goal clauses, requirement sources, epic summaries and output path.

1. Populate the body through [Draft Initiative Issue Body](#draft-initiative-issue-body).
2. Apply [Check Round of Edits](#check-round-of-edits).
3. Return the populated body and its local format findings to the caller.

#### *Draft* Initiative Issue Body

One initiative body, scoped to one proposal.

**Inputs:** Scoped proposal, confirmed goal clauses, requirement sources, epic summaries and output path.

1. Populate the body from the [Template](#template-1) into a local file at the supplied output path.
   - That file must be the source for every later edit.
   - All populated fields must meet [Fields](#fields-5).
2. Derive the Problem and Non-Goals from the proposal this initiative is scoped to.
   - The Problem must meet [Problem and Proposal](#problem-and-proposal).
   - Each Non-Goal must meet [Non-Goals](#non-goals).
3. Write the acceptance criteria before the Work Breakdown, so each row's Coverage can cite them.
   - Each criterion must come from a confirmed clause and meet [Initiative Acceptance Criteria](#initiative-acceptance-criteria).
   - The criteria must come from the requirements sources the proposal references. Where the proposal references none, they must come from the proposal's body alone.
4. Populate the shared table through [Write Issue Table](#write-issue-table).
5. Fill the initiative-specific cells.
   - Each row must meet [Work Breakdown](#work-breakdown-1).
   - An item a test cannot observe must stay named as [Coverage Reports](#coverage-reports) define.

### Fields

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

An initiative criterion meets the [shared acceptance criteria](#shared-acceptance-criteria) and [Requirement Characteristics](#requirement-characteristics), and:

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
- A departure from a marked source is corrected in the criterion, unless a Non-Goal records it.
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

## Task Body

### Operations

#### *Populate* Task Body

One task body within its supplied epic context.

**Inputs:** Task scope, epic context, design, criteria and output path.

- Populate the body from the [Template](#template-2) at the supplied output path.
  - The title must meet the shared [Titles](#titles) conditions.
  - The Problem and Proposal must meet [Problem and Proposal](#problem-and-proposal).
  - Acceptance criteria must meet the [shared acceptance criteria](#shared-acceptance-criteria).
  - All populated fields must meet [Fields](#fields-6), including the required [Sections](#sections).

### Fields

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

## Standalone Body

### Operations

#### *Populate* Standalone Body

One standalone issue body from its supplied scope.

**Inputs:** Problem, design, criteria, open questions and output path.

- Populate the body from the [Template](#template-3) at the supplied output path.
  - The title must meet the shared [Titles](#titles) conditions.
  - The Problem and Proposal must meet [Problem and Proposal](#problem-and-proposal).
  - All populated fields must meet [Fields](#fields-7), including the required [Sections](#sections-1).

### Fields

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

## Planning Record

### Fields

#### Artifacts

- One row for every artifact in the record other than README.md, added when the file is produced.
- The link sits on the artifact's name. The row says what the artifact holds, and the artifact is the home of that content.
- In an overview record, the architecture overview is the one row, and its pull request is under Links.

## Work Item

### Fields

#### Component

One declaration line ahead of the first heading, naming the single component the Implementation part extends as the path to it in the repository that holds it.

- A task that creates the component names the path it creates.
- A task whose implementation extends more than one component is split into a task for each.

## Epic

### Fields

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

## Pull Request

### Fields

#### Issue Links

- GitHub shows the link in the pull request's Development field and in the issue's Linked pull requests field, which the project board reads.
- A task pull request links the task's issue, and a review pull request links its epic's issue.
- The link is addressed by issue, so a pull request whose work carries no issue links nothing. A task pull request delivering rows that have no issue of their own is the whole of what stays unlinked.
- The link is stored on the pull request. It holds on any base branch and on a pull request that has merged, and a later body edit leaves it standing.
- A linked issue remains open until its criteria and delivery requirements hold and every Development-linked pull request is merged.
- The field is the whole of the relation: neither body links the other. The pull request's References carry its sources, and the issue it delivers is not among them.
- A pull request with a delivery issue but no Development link is uncited.

# Bootstrap

A link whose text opens with a matching [symbol](#symbols) follows the usage instructions and is *not* read as a file.

## Compile

Compile a target file. Run from the skill's directory, which holds `SKILL.md`.

```bash
pf -o <scratch>/<name>.bundle.md <destination>
```

- `<destination>`  The link's destination as written.
- `<name>`  The destination's file name without its suffix.
- `<scratch>`  An existing working directory outside the repository.

> A non-zero exit stops the run and reports `pf`'s diagnostics.

## Symbols

| Symbol | Description | Usage |
| --- | --- | --- |
| `↳` | An inline target | [Compile](#compile) it, read the whole bundle and follow the instructions in its preamble. |
| `⇉` | A dispatched target | [Compile](#compile) it, hand the bundle to one sub-agent, with the inputs the request names, to follow the instructions in its preamble, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered to the session that dispatched it. That session puts each returned question to the user, or returns it in turn when it was itself dispatched, then dispatches again with the answers. A step that dispatches for each item of a set in parallel hands every item at once to a sub-agent of its own, with that item's inputs, and continues when all have returned; only the sub-agents that returned questions are dispatched again, with their answers. |

# References

## Requirement Characteristics

The characteristics an acceptance criterion meets, and the characteristics a set of them meets. Condensed from ISO/IEC/IEEE 29148:2018, clauses 5.2.4 to 5.2.7.

### Individual

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

### A Set

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

### Wording

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
