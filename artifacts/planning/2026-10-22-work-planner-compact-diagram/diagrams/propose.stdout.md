This bundle was built for [Modes/Propose-Mode](#modespropose-mode); everything else is material it references.

# Artifacts

## Operations

### Board

#### *Create* Proposals Board

A new proposals board linked to the supplied repository.

**Inputs:** Board owner and repository.

1. Run [Find Board Template](#find-board-template) with the owner and the exact title `Proposals Template`.
2. Use the returned number as the copy source.
3. Run [Copy Board Template](#copy-board-template) with that template number, the owner and the title `Proposals`.
4. Retain the new board number. The copy meets [Proposals](#proposals).
5. Run [Link Board to Repository](#link-board-to-repository) with the owner, new board number and repository.
6. Return the new board number after linking succeeds.

#### *Place* Issue on Board

One issue's membership and initial status.

**Inputs:** Board owner and number, issue id and selected initial status.

1. Run [Fetch Board Fields](#fetch-board-fields) for the Status options, using the caller's supplied board and issue identities.
2. Run [Add Issue to Board](#add-issue-to-board) with the issue id.
3. Run [Set Item Status](#set-item-status) with the caller's selected status and the matching field and option ids.
4. Run [Fetch Board Item](#fetch-board-item) for the saved item.

#### *Locate* Project Board

The board identity matching a supplied purpose or theme.

**Inputs:** Owner and proposals-board purpose or theme title.

1. Run [Find Proposals Board](#find-proposals-board) for proposals, or [Find Theme Board](#find-theme-board) for a theme.
2. Return the identity or an absent-board finding for the caller's selection or creation path.

### Issue Body

#### *Validate* Issue Body

One body checked against its supplied kind and template.

**Inputs:** Issue JSON, kind field conditions, required related evidence and output body file.

1. Run [Check Body Format](#check-body-format) with the supplied issue JSON, kind inputs and output file as `--fix`.
2. Review the body against the supplied field conditions.
3. Return the [Format Findings](#format-findings), mechanical diff and field findings, including missing sections, extra sections, wrong-kind layout, historical narration and criteria that fail their named instrument. A mechanical correction preserves wording; new content and scope decisions require caller-supplied resolutions.

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

#### *Comment* on Issue

The supplied discussion text saved on one issue.

**Inputs:** Repository, issue number and exact comment text or file; reviewer identity and addressed feedback when replying to a review.

1. When replying to feedback already folded into the body, compose a precise, factual reply addressing each point and mentioning the reviewer, with no thanks or filler. Name what the body now says, by criterion id where one carries it, or the issue that takes the point.
2. Publish the supplied comment:
   - For a one-line comment, run [Post Inline Comment](#post-inline-comment) with the exact text.
   - For a longer comment, run [Post Comment File](#post-comment-file) with the complete file.
3. Return the saved comment URL.

#### *Select* Tracker Number

The next unused number for one prefixed issue kind in the repository.

**Inputs:** Repository, the kind's prefix letter and its existing titles.

1. Run [List Prefixed Titles](#list-prefixed-titles) for the supplied repository and prefix letter, covering all issue states.
2. Read the highest prefix carrying that letter.
3. Confirm the following number, or `00` when there is no prefix, remains unused before creation.
4. Return the confirmed number.

### Proposal Body

#### *Populate* Proposal Body

One proposal body from a confirmed problem and goal.

**Inputs:** Confirmed problem, evidence, goal clauses, boundary and output path.

- Populate the body from the [Template](#template) at the supplied output path.
  - The title must meet the shared [Titles](#titles) conditions.
  - The Problem must meet the shared [Problem and Proposal](#problem-and-proposal) conditions.
  - All populated fields must meet [Fields](#proposal-body-1), including the required [Sections](#sections).

#### *Validate* Proposal Body

The body's local format and field findings.

**Inputs:** Proposal issue JSON and output file.

1. Call [Validate Issue Body](#validate-issue-body) with the current body, local [Fields](#proposal-body-1), supplied related evidence and output file, using the proposal field conditions and required title and label metadata.
2. Return the corrected body, mechanical diff and unresolved findings for the caller.

### Repository Labels

#### *Ensure* Repository Labels

The required label definitions available for issue publication.

**Inputs:** Repository and required label names, colours and descriptions.

1. Run [List Labels](#list-labels) for the repository.
2. Compare the returned labels with the supplied required names.
3. Run [Create Label](#create-label) for each absent required definition.
4. Return the available labels; an unknown definition is a finding for the caller to resolve before publication.

## Fields

### Board

#### Proposals

- The board is titled `Proposals`. It holds proposal issues, the incoming funnel for work that may become an initiative.
- Its copy source is the open board titled `Proposals Template`. That template carries Priority: High, Medium and Low, and its view is a board grouped by Status.
- **Suggested.**
  Raised, and nobody has taken it up. A new proposal lands here, with no assignee.
- **Considering.**
  Someone is weighing the goal, the evidence and the criteria. That person is the assignee.
- **Approved.**
  Qualified to become an initiative. The assignee is the user.
- **Held.**
  Not now. It stays on the board, with no assignee.
- **Declined.**
  It will not become an initiative. It has no assignee.

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

#### Format Findings

- **Fixed.**
  Structural changes preserve the wording and are present in the returned body file, with a body diff.
- **Apply.** Title or label changes for the caller to publish on the issue.
- **Decide.** Missing content or a judgement for the caller to resolve.

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

## Commands

### Board

#### Find Board Template

Prints the number of the open board with the supplied exact template title.

**Inputs:** Board owner and template title.

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "<template-title>") | .number'
```

#### Copy Board Template

Copies the supplied template into a new open board with the supplied title and prints its number.

**Inputs:** Board owner, template board number and new board title.

- The copy's JSON is one project; `.number` identifies the new board.

```bash
gh project copy '<template-number>' --source-owner '<owner>' --target-owner '<owner>' --title '<board-title>' --format json --jq .number
```

#### Link Board to Repository

Links one board to the supplied repository.

**Inputs:** Board owner, board number and repository.

```bash
gh project link '<board-number>' --owner '<owner>' --repo '<repo>'
```

#### Find Proposals Board

Prints the number of the open board titled `Proposals`.

**Inputs:** Board owner.

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "Proposals") | .number'
```

#### Add Issue to Board

Adds the caller-supplied issue id to a board and prints the new item's id. The input is the issue id, not its number.

**Inputs:** Board owner and number, and issue id.

```bash
gh api --method POST 'users/<owner>/projectsV2/<board-number>/items' -f type=Issue -F 'id=<issue-id>' --jq .id
```

**Example:**

```bash
gh api --method POST 'users/<owner>/projectsV2/13/items' -f type=Issue -F id=3040123456 --jq .id
```

#### Set Item Status

Sets one board item's Status.

**Inputs:** Board owner and number, item id, and input file containing the Status field id and selected option id.

The input body names the Status field id and option id from [Fetch Board Fields](#fetch-board-fields): `{"fields":[{"id":<status-field-id>,"value":"<status-option-id>"}]}`. Substitute the field id as a JSON integer and the option id as a JSON string.

**Example payload:** `{"fields":[{"id":419167630,"value":"OPTION"}]}`.

```bash
gh api --method PATCH 'users/<owner>/projectsV2/<board-number>/items/<item-id>' --input '<status-input-file>' --jq .id
```

**Example:**

```bash
gh api --method PATCH 'users/<owner>/projectsV2/13/items/1001' --input status-backlog.json --jq .id
```

#### Fetch Board Fields

Saves a board's fields.

**Inputs:** Board owner, board number and destination file.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/fields?per_page=100" > '<board-fields-file>'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/fields?per_page=100" > fields.json
```

#### Find Theme Board

Prints the number of the open board for one theme, by its theme name after any proposal designator.

**Inputs:** Board owner and theme name.

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title | sub("^\\[P[0-9]+\\] "; "") | startswith("<theme-name>: ")) | .number'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title | sub("^\\[P[0-9]+\\] "; "") | startswith("Canon: ")) | .number'
```

#### Fetch Board Item

Reads one board item, including its current Status.

**Inputs:** Board owner and number, item id and Status field id.

```bash
gh api "users/<owner>/projectsV2/<board-number>/items/<item-id>?fields=<status-field-id>"
```

**Example:**

```bash
gh api "users/<owner>/projectsV2/9/items/1001?fields=419167630"
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

#### List Prefixed Titles

Lists titles carrying one kind's prefix letter, across all states.

**Inputs:** Repository owner and name, and the kind's prefix letter.

```bash
gh api --paginate 'repos/<owner>/<repository>/issues?state=all&per_page=100' --jq '.[] | select(.title | test("^\\[<prefix-letter>[0-9]{2}\\]")) | .title'
```

**Example:** Initiatives in one repository.

```bash
gh api --paginate 'repos/m2ux/workflow-server/issues?state=all&per_page=100' --jq '.[] | select(.title | test("^\\[I[0-9]{2}\\]")) | .title'
```

### Repository Labels

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

# Modes/Propose-Mode

Scopes one problem: the friction, the evidence, and the boundary, and states the goal as clauses the user confirms. It raises one proposal on the board titled `Proposals`.

## Procedure

The main path meets [Outcomes](#outcomes).

1. **Understand the problem.**
   Ask the user until the friction and the boundary are clear.
   - State the goal back as clauses meeting [Goal](#goal).
   - Have the user confirm those clauses.
2. **Gather evidence.**
   - Measure the current state: counts, paths, and file:line.
   - Delegate broad sweeps to parallel sub-agents.
   - Spot-check what they return before recording it.
3. **Draft the body.**
   Run [Populate Proposal Body](#populate-proposal-body) with the confirmed problem, evidence, goal clauses, boundary and output body path. The local file is the source for the issue.
   - Obtain the proposal's number through [Select Tracker Number](#select-tracker-number) with the proposal prefix letter, and carry it in the title.
   - The goal clauses are the clauses the user confirmed. The Non-Goals are the boundary.
   - The design, the acceptance criteria, and the breakdown belong to a later goal.
4. **Validate.**
   Call [Validate Proposal Body](#validate-proposal-body) with the draft issue JSON and output file.
   - Resolve each finding.
   - Update the draft.
   - Repeat Validate Proposal Body with the revised JSON and the same output path. Proceed to publication only when validation passes.
5. **Publish.**
   Call [Ensure Repository Labels](#ensure-repository-labels) with the proposal's required label definitions.
   - Pass the validated body, title and labels to [Save Tracker Issue](#save-tracker-issue), leaving it unassigned.
6. **Confirm placement.**
   Ask whether to add the issue to the proposals board.
   - On acceptance, continue to the place step.
   - On a decline, skip placement and continue to the report step with the issue URL.
   - Wait for an unanswered decision.
7. **Place.**
   Call [Locate Project Board](#locate-project-board) for proposals.
   - Create an absent board through [Create Proposals Board](#create-proposals-board).
   - Read the saved issue id through [Read Tracker Issue](#read-tracker-issue).
   - Run [Place Issue on Board](#place-issue-on-board) with that id and initial status Suggested.
   - Leave the issue unassigned.
8. **Report.**
   Give the issue's URL, and the board's when the issue was placed.

## Outcomes

- **A scoped problem.**
  The user has one problem scoped, and has confirmed its goal.
- **One proposal.**
  The user has that problem raised as one proposal.
- **On the proposals board.**
  When the user wants the proposal on the proposals board, it is there, raised, and unassigned.
