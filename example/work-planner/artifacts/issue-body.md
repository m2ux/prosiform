---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Issue Body

The shape every issue body shares: its title, its Problem and Proposal, its acceptance criteria, and its work-breakdown table.

## Operations

### *Write* Issue Table

The shared table, before a kind fills its cells.

**Inputs:** Current body, the kind's table columns and supplied row data.

#### 1. Populate the Shared Table Cells

Populate the shared Done, Coverage and Depends on cells from the supplied row data.
- The columns must match the kind's table.
- The shared cells must meet [Tables](#tables).

#### 2. Read the Finished Issue Table

Read the finished table against [Tables](#tables), [Numbering](#numbering), and [Reference form](#reference-form). A Depends on cell that holds prose fails [Tables](#tables). Numbering that does not follow start order is advisory, as [Numbering](#numbering) states.

### *Check* Round of Edits

The shared check after a round of edits.

**Inputs:** Changed issue bodies, their kind's field conditions and format inputs.

#### 1. Check Each Section Against Fields

Check each section of the issue against the field conditions for its kind and against [Fields](#fields) in this file.

#### 2. Check the Changed Body Formats

Run [Check Body Format](#check-body-format) on every issue the round changed.

### *Validate* Issue Body

One body checked against its supplied kind and template.

**Inputs:** Issue JSON, kind field conditions, required related evidence and output body file.

#### 1. Run the Body Format Check

Run [Check Body Format](#check-body-format) with the supplied issue JSON, kind inputs and output file as `--fix`.

#### 2. Review the Body Field Conditions

Review the body against the supplied field conditions.

#### 3. Return the Body Validation Findings

Return the [Format Findings](#format-findings), mechanical diff and field findings, including missing sections, extra sections, wrong-kind layout, historical narration and criteria that fail their named instrument. A mechanical correction preserves wording; new content and scope decisions require caller-supplied resolutions.

### *Apply* Body Corrections

One body rewritten from confirmed local findings.

**Inputs:** Current body, selected kind template and field conditions, related context, confirmed resolutions and output path.

#### 1. Populate Missing Body Sections

Populate missing sections from the supplied issue and related context.

#### 2. Apply Extra-Section Decisions

Apply each confirmed decision to keep, fold or remove an extra section, and rewrite a wrong-kind body in the selected template.

#### 3. Record the Tracker-Kind Change

Record a required tracker-kind change for the caller.

#### 4. Restate Historical Narration

Restate historical narration as the current design.

#### 5. Apply Confirmed Criterion Changes

Apply confirmed criterion changes.
- The body must meet [Body](#body), [Shared Acceptance Criteria](#shared-acceptance-criteria) and the supplied kind conditions.

#### 6. Validate the Corrected Body

Validate the body through [Validate Issue Body](#validate-issue-body).

#### 7. Return the Corrected Body

Return the corrected file, validation findings and any required cross-body or metadata changes for the caller.

### *Build* Body Snapshot

A local issue-shaped record for body validation.

**Inputs:** Current body file, title, labels, optional existing issue JSON and destination JSON path.

#### 1. Write the Body Snapshot JSON

Write the body's exact text, title and labels to the destination as JSON.

#### 2. Preserve the Issue Identity

Preserve the existing issue's identity and state when supplied.

#### 3. Mark an Unpublished Draft

For an unpublished draft, use `number: null` and `state: "open"`; labels are strings or objects with a name.

#### 4. Return the Snapshot Path

Return the JSON path for validation. No tracker issue is created by this operation.

### *Repair* Issue Format

The saved format corrections for a set of issues of one kind and any unresolved content findings.

**Inputs:** The kind's validator, either its body file's Validate operation or [Validate Issue Body](#validate-issue-body) with the kind's field conditions; that validator's further inputs; a set of issue bodies, each with its identity, current JSON and output body path; kind template and required related evidence.

#### 1. Apply the Format Validator

Apply the supplied validator to each issue body with its current JSON, output path and the validator's further inputs.
- Return an unreadable source as a blocker before editing.

#### 2. Review Each Format Diff

Review each returned diff.
- Publish wording-preserving format, title and label corrections through [Save Tracker Issue](issue.md#save-tracker-issue), without asking.
- Retain content decisions and cross-body findings separately; do not publish them as mechanical fixes.

#### 3. Resolve Single-Body Findings

Resolve a non-mechanical finding confined to one body.
- Obtain the user's decision.
- Apply [Apply Body Corrections](#apply-body-corrections) with the current body, kind template and conditions, related context, confirmed resolution and output path.
- Publish through Save Tracker Issue. An unanswered decision or a finding requiring changes to other issues returns to the caller as a blocker.

#### 4. Re-Read Each Repaired Issue

Apply [Read Tracker Issue](issue.md#read-tracker-issue) for each saved issue.
- Repeat the supplied validator with the saved JSON and the same further inputs, context and output path.
- Return each saved body, whether a correction was made, and the validation result to the caller. A remaining failure is a blocker.

### *Resolve* Open Questions

The answers to an issue's Open Questions saved in its body, and the questions that stay open.

**Inputs:** Issue identity, current JSON, kind template and field conditions, related context and output body path.

#### 1. Interview on Open Questions

Put each question in the body's Open Questions section to the user as an [interview](../rules.md).

#### 2. Apply the Question Answers

Apply [Apply Body Corrections](#apply-body-corrections) with the current body, kind template and conditions, related context, each confirmed answer and output path, removing each settled question from Open Questions.

#### 3. Publish the Answered Body

Publish the corrected body through [Save Tracker Issue](issue.md#save-tracker-issue).

#### 4. Re-Read the Answered Issue

Apply [Read Tracker Issue](issue.md#read-tracker-issue) for the saved issue.

#### 5. Return the Question Decisions

Return the saved body, each decision taken and the questions still open in its Open Questions section. A question still open is a blocker to work that depends on it.

## Fields

### Titles

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

### Problem and Proposal

- **Friction.**
  A Problem states the friction as it is now. Its evidence is a count or a code link for that friction. A Problem does not describe the plan.
- **Plan ids.**
  A Problem or Proposal names no epic, task or acceptance criterion of its own initiative. The Work Breakdown table holds those references; a sibling boundary is plain language.
- **Evidence that may be cited.**
  Code, a merged pull request, and an issue outside this initiative may be cited.

### Shared Acceptance Criteria

An acceptance criterion meets these. A kind adds its own under its Acceptance Criteria.

- States an end state, not an activity.
- Names or implies the instrument that observes it: a test, a guard, a command or a measure.
- Is unambiguous, so two readers agree on whether it holds.
- Meets [Requirement Characteristics](../references/requirement-characteristics.md).
- **One invariant.**
  Each criterion states a single condition that holds or does not. One joining several is split, and the Coverage cells cite the new ones. A condition over a list of subjects is one condition.

#### Verifiable

- Subjective wording is an observable pass or fail, or the criterion is absent.
- A fact that inspection, analysis, demonstration, or test can check is kept, such as every option having a description.
- A judgment about meaning, such as a claim that a description states what choosing means, is subjective wording.
- An item none of those methods can observe is named as [Coverage Reports](#coverage-reports) define, and it stays named there.

### Tables

- **Done.**
  The last column. Its cell is empty while the row is open, and a tick, ✓, when the row is complete.
- **Description.**
  A short phrase naming what the row delivers, at most eight words, with no list, semicolon or detail.
- **Coverage.**
  The acceptance criteria the row delivers, `AC2, AC5`, and nothing else. Every criterion is delivered by at least one row.
- **Depends on.**
  References only, with no prose, and only what no other entry in the cell already implies.

### Numbering

Rows are numbered in the order they can start, so every dependency points to an earlier row. Numbering that does not follow start order is advisory.

Work a pull request names keeps its number. Renumbering touches only a row no pull request names.

### Reference Form

Tables write references with colons, the form the scripts read. Prose uses a space.

### Body

- **Stale references.**
  A row number, issue link or decision wording agrees with the current plan.
- **Body.**
  A body states the plan as it is. It carries no change narrative. How the plan evolved belongs in the planning record and in commit and pull request bodies.

### Stale References

Task and epic numbers, issue links and wording must agree with the current decisions and bodies. References to superseded decisions are findings.

### References

An issue's References section does not link issues or pull requests on the same board.

### Coverage Reports

- **Unobservable items.**
  An item a test cannot observe is named in the plan or the coverage report. It stays in the report.
- **The check matches the criterion.**
  - A file or string check counts as coverage only when the criterion is a fact about that file.
  - A criterion about a run is covered by a run that shows it.
- **The specified set.**
  A coverage report lists every acceptance criterion the work under review is specified to cover.

### Format Findings

- **Fixed.**
  Structural changes preserve the wording and are present in the returned body file, with a body diff.
- **Apply.** Title or label changes for the caller to publish on the issue.
- **Decide.** Missing content or a judgement for the caller to resolve.

## Commands

### Check Body Format

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
