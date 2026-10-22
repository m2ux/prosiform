This bundle was built for [Revise Mode](#revise-mode); everything else is material it references.

# SKILL

## Work Planner

### Conventions

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

## Overview

### Repository Graph

The indexed symbols, relationships and ordered flows for a repository revision.

## Fields

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

### Pull Request Body

#### Template

````markdown
## Overview

{{One paragraph: what this pull request delivers and why.}}

## Changes

{{One sentence on what changed and why it was needed. Then one heading per area the changes sit in. A heading is two to five words, in title case, such as Queue Placement or Task Readiness. Under each heading, one bullet per functional change in that area. The bullet opens with a bold lead, as the scheme's Bold leads rule lays one out. The change is at most two lines, the lead included: the lead names what it does, and the behavior is the single line under it.}}

### {{Queue Placement}}

- **{{What it does.}}**
  {{The behavior as it is.}}

## Test Plan

| Test | Description | Coverage | Pass |
| --- | --- | --- | --- |
| T1 | {{Check name, per [Test Plan](#test-plan).}} | {{Observed criteria, if any.}} | [{{Result}}]({{Planning document URL#test-section}}) |

## Open Questions

- {{An undecided point. Resolve it, then delete the section.}}

## References

- **R1.** [{{Title}}]({{URL}}) — {{What the reader finds there. The issue this pull request delivers is not a reference: the Development field carries that link, as [Issue Links](pull-request.md#issue-links) state. Delete the section when there is none.}}
````

#### Titles

- A pull request's title starts with the epic it works on: `[I07:E00] Purpose`.
- A pull request working on no epic takes `Name: Subtitle`, with no prefix, as a revision of the skill itself does.
- The prefix is how an epic's pull requests are found, and each one, open or merged, is matched to the tasks it works on from its changes and the tasks' Descriptions.
- The pull request that merges an epic base carries the same prefix. Its head is the epic base, which tells it from a task pull request.

#### Review Body

- Overview is one paragraph on what the base carries.
- Changes holds one heading per area, with a bullet per functional change.
- References cites each task pull request merged into that base.
- It carries no Test Plan, since it delivers no task of its own, and no statement about what the epic has yet to deliver. The epic's Work Breakdown is where delivery state is read.

#### Test Plan

A task pull request carries a Test Plan.

- **Table.**
  The pull request's Test Plan section contains only one table, with columns Test, Description, Coverage and Pass, in that order.
- **Columns.**
  - Test names the id.
  - Description briefly names the check.
  - Coverage names the criteria the check observes, `AC1, AC3`, and is empty when the check observes none.
  - A row whose Test cell is empty names a criterion no check observes, and its Pass cell is empty.
  - Pass is empty while a check awaits a result. A recorded result uses ✓ when the check ran and held, or an accurate label such as Partial, Fail or Not run.
- **Evidence.**
  - Test procedures, tested revisions, observations, limitations and supporting evidence belong in the work's published planning document.
  - Each recorded result in Pass links to its relevant section in that document, using the result as link text: `[✓](URL#check)` or `[Partial](URL#check)`.
  - Each evidence link is accessible to the pull request's readers and resolves to the intended section.
- **Completion.**
  The test plan has passed when every row with a Test id carries ✓ as its result. Partial, failed and unexecuted checks remain incomplete.

#### Test Coverage

- Every criterion a unit's Coverage names has an observing test in its work item and pull request. A criterion no test can observe remains in the [coverage report](#coverage-reports) and in a test-plan row with an empty Test cell.
- The criterion selects the test kind: a unit test for one component, an integration test for a seam between components, and an end-to-end or system test for running-system behaviour. That evidence meets [Coverage Reports](#coverage-reports).
- An instrument that does not exist yet is work the task carries, as the verified rule defines. Use the project's own system test where it can observe the criterion.
- One row per check, in execution order, followed by any unobserved criteria. Every criterion in the unit's Coverage appears in at least one row.

### Repository Graph

#### Revision

The graph identifies its worktree and indexed commit. Measurements describe the supplied pull request head and its difference from the supplied base branch.

#### Freshness

Graph responses carry a JSON `staleness` block. A behind index is not current with the requested head; measurements from it are invalid.

#### Changed Symbols

The surface identifies symbols touched by the diff and the flows containing them. It compares with the supplied base branch, rather than the branch's whole history.

#### Symbol Relationships

Each changed symbol has callers, callees, containing flows and file locations. Files group into component areas; their measured relationships determine edges between areas.

#### Flow Traces

Each flow contains symbols in step order. Each `process_symbols` entry includes `step_index`, file and lines. Those ordered measurements supply sequence-diagram participants and interactions. A manually inferred call order does not establish a graph trace.

## Operations

### *Measure* Repository Change

Current graph evidence for the supplied change.

**Inputs:** Worktree, verified head commit and base branch.

1. Run [Index Status](#index-status) in the supplied worktree. Every graph command runs in that worktree.
2. If the repository is unindexed or behind the verified head:
   - Run [Index Repository](#index-repository).
   - Confirm freshness.
3. Run [Change Surface](#change-surface) against the supplied base using `--base-ref`.
4. For each changed symbol, run [Symbol Context](#symbol-context).
5. For each reported flow, run [Flow Trace](#flow-trace).
6. Inspect the staleness block on every response. For a behind index:
   - Discard its measurements.
   - Reindex.
   - Repeat the affected measurements.
7. Return only evidence current with the supplied head, meeting [Fields](#repository-graph-1), or a freshness blocker.

## Commands

### Index Status

Reports whether the repository is indexed, and how far behind the index sits.

**Inputs:** Repository worktree and requested revision.

```bash
gitnexus status
```

### Index Repository

Indexes the repository, which an unindexed or behind repository needs before any measurement.

**Inputs:** Repository worktree and requested revision.

```bash
gitnexus analyze
```

### Change Surface

Reports the symbols a pull request's diff touches and the flows they sit in, against the base branch.

**Inputs:** Current indexed worktree and comparison base branch.

- `--base-ref` is the pull request's base, so the surface is the change rather than the branch's whole history.

```bash
gitnexus detect-changes --scope compare --base-ref '<base-branch>'
```

**Example:**

```bash
gitnexus detect-changes --scope compare --base-ref main
```

### Symbol Context

Reports one symbol's callers, its callees and the flows it sits in, each with the file it sits in.

**Inputs:** Symbol identity from the supplied change surface and the current graph worktree.

```bash
gitnexus context '<symbol-identity>'
```

**Example:**

```bash
gitnexus context reserveRow
```

### Flow Trace

Reports one flow's symbols in step order, the structure a sequence diagram is drawn from.

**Inputs:** Flow identity from the supplied change surface and the current graph worktree. The result meets [Flow Traces](#flow-traces).

```bash
gitnexus query --query '<flow-identity>' --limit 1
```

**Example:**

```bash
gitnexus query --query "Queue Placement" --limit 1
```

# Guidelines

The rules this skill's files follow alongside the [shared skill guidelines](../guidelines.md). Modes, protocols and artifacts use the directory-specific structures below. A rule that binds only modes, only protocols, only artifacts, or only references is in that section.

## Titles

- **Title case.**
  A heading, a board title, an issue or pull request name and subtitle, and a template section heading are in title case.
  - A short word stays lowercase unless it is first or last: a, an, the, and, but, or, nor, for, as, at, by, in, of, on, to, up, with.
  - Each part of a hyphenated word is capitalized.
- **Action titles.**
  Operation, command and mode procedure titles name the action and subject directly, without articles such as a, an or the. Use meaningful subject words to meet the procedure title length.
- **Italicised verb.**
  An artifact operation's title italicises its leading verb, and nothing else: `### *Apply* Issue Placement`. The emphasis leaves the heading's anchor unchanged, so a link to it keeps its plain text and fragment.
  - The verb separates from the subject, so the anchors one procedure reaches read together as its input and output contract: `*Read*` and `*Fetch*` take evidence in, `*Populate*`, `*Record*` and `*Save*` put state out, `*Check*` and `*Validate*` assert against what they are given.
  - A title whose leading word does not carry that sense is the wrong title; name the action first.

## Procedure

These rules apply to mode procedures and artifact operations.

- **Explicit execution.**
  State the action, its inputs and any condition that selects it. Name the result used by the next step. Branches state where to continue or stop; retries name the repeated operation and refreshed inputs. Distinguish reading a definition from executing a procedure. Resolve timing, caller responsibility and return points in the instructions.

- **Subsection titles.**
  A procedure subsection title contains at least three words and names the action and its subject.
- **Numbered steps.**
  A procedure with multiple steps uses consecutive numbers starting at `1.`. Supporting bullets and command blocks are indented beneath their step. A single-step procedure has no numbering or bold action label.
- **Sub-bullets.**
  A sub-bullet under a numbered procedure step is in sentence case. The first word is capitalized, and a name keeps its own capitals.
- **Separate actions.**
  After a step's opening instruction or scope, put each sentence that advances the sequence in its own bullet, including sequences written as a paragraph. Split comma- and semicolon-separated actions the same way. Keep numbered steps as the outer sequence; use bullets for the actions within a step. Put a shared condition or iteration above its nested actions, preserving order, inputs, validation gates and return points. Keep an input list, action condition or explanatory sentence with the action it qualifies; these are not separate sequence elements.
- **List introductions.**
  Within a procedure step, a line that introduces or governs one list is plain text at the enclosing level, with the governed items as bullets directly beneath it. Determine this relationship from the meaning of the instructions, regardless of the opening verb, punctuation or existing indentation. Apply the rule at every nesting level. Use bullets for peer actions, alternative branches and sibling groups. Give actions outside an introduction's scope an explicit continuation at the enclosing level.
- **Dependent instructions.**
  Nest instructions that handle an action's specific output beneath that action. Keep peer actions at the enclosing list level. Name the returned object explicitly when a pronoun would leave its referent unclear.
- **Branch headers.**
  Nest named findings and conditional branches as sub-bulleted headers beneath the action or scope that governs them. Each header is a bold label on its own line, with its instructions in child bullets. Mutually exclusive choices share one decision step. Place actions common to all branches after the branch group at the enclosing sequence level, including a shared return to the caller.

## Prose

- **Input labels.**
  Artifact operation and command input declarations start with the bold label **Inputs:**. The input description uses normal text.

- **One home per rule.**
  A rule is stated once. Its home is the field or outcome it constrains, the procedure step it binds, or the Modes, Artifacts, or References section below. Operation inputs name the evidence that the caller must supply for those preconditions.
- **Terms.**  The scheme is agent-engineering: an agent-engineering prefix, title, issue or table.
- **Examples.**
  A name, label, branch, path or board that belongs to one project is an example. The rule states what holds for every project.
- **Consumers.**
  A document states what it is and what it requires. A document may cite its own rules. The documents that use it are the ones that cite it.

- **Measured claims.**
  A count or a chain comes from a command's output.
- **Reachable dependencies.**
  Each required file, heading and operation has a resolving link. Prerequisites include the files those operations require; links to another file's operation include that file.

## Operations

These rules govern command and access specifications. Procedural operations follow Procedure and Artifacts below.

- **Spec layout.**
  A command specification opens with one line on what it does. Its inputs and parameter conditions follow, then its command block or access instructions. Specifications have no numbered steps or bold action labels. The calling operation or mode procedure states when the command runs and what it passes; action preconditions and refusals belong to the governing step.
- **One command.**
  Each specification exposes one command or access action. Put sequencing, branching, repetition and readback in an artifact operation or mode procedure. A working-directory prefix and output-filter pipeline belong to the command they serve. Optional flags for one command share its specification.
- **One home.**
  A command specification sits under Commands in an artifact, or Operations in a mode. Artifact operations call their implementation commands by heading link. A kind supplies only its additional parameters to a common operation.
- **Direction.**
  The procedure names the command it runs. A command does not name that procedure.

- **Execution.**
  Run a command in the checkout of the repository it addresses. Resolve placeholders from the supplied inputs before execution. Use `orgs/<owner>` for an organisation's board and `users/<owner>` for a user's board.
- **Placed paths.**
  A command that creates a worktree or other lasting location takes a path its caller composes. Its specification cites the field that places that kind and states that the path resolves against the directory the command runs in.
- **Parameter placeholders.**
  Command templates use descriptive `<input-name>` placeholders for variable identities, branches, paths, dates, filters and values, aligned with their **Inputs:**. Quote shell arguments containing placeholders and escape substituted values for their shell, URL, query or payload context. Keep required literals, enum values, field names and installed script paths literal. State list separators, mapping syntax and repeated arguments beside the command. JSON templates preserve the required value types.
- **Concrete examples.**
  Retain hard-coded values in explicitly labelled examples alongside the generic command or payload template so their shape remains clear. Examples illustrate input values; they do not supply defaults or identify the current target.
- **Local scripts.**
  `<workspace>` is the checkout holding the installed scripts. Run its scripts with the absolute `<workspace>/scripts/sbx` path from that checkout.
- **Bodies.**
  Pass a complete body or multiline comment through a file. The file holds the exact intended text.

## Modes

Read this before adding or changing a mode.

- **Orchestration.**
  Modes coordinate; artifact operations perform and validate work on their own subject. Mode procedures are lean orchestration wrappers: they select scope, call artifact operations with named inputs, route returned findings and user decisions, and coordinate changes across artifacts. A procedure that manages multiple artifacts belongs in a mode. A mode keeps commands only for work spanning artifacts or validating the skill itself.
- **One goal.**
  A mode is the lifecycle of one user goal. It changes when that lifecycle changes.
- **Outcomes.**
  A mode outcome is a user goal to be met. It does not state an artifact shape, a table column, or a criterion.
- **No procedure in an outcome.**
  An outcome does not name a procedure, a step, or a command, and it does not link to one.
- **Procedure.**
  The top-level procedure is the main path. A short sequence that no other file references stays there. A subsection is an alternative path, a loop whose steps would otherwise be repeated, a unit another file references, or a sequence long enough that the top-level step only names it. Plan mode keeps review, and keeping the goal current, in that sequence. Keeping the goal current repeats the review. A subsection opens with one line on what it is for, and that line does not restate the steps. A step links to the user-goal outcome and does not restate it. A step calls the body artifact's procedure rather than copying it.
- **Prerequisites.**
  Prerequisites open with `Read these files first.` They list every file the mode's Procedure, Outcomes or Operations link to, including another mode that step runs. They do not list a family common the mode does not link to. Reading the body artifact includes the common file, because that artifact lists it. Recalculate the list after changing calls or references: retain direct dependencies, including files owning called subsections; remove entries whose last direct use is gone. Caller attribution and descriptions of another mode's internals do not create dependencies for the callee.
- **Procedure steps.**
  Each numbered step opens with a bold sentence-case action label, with its instructions on the next line. Mode procedures identify required context in their instructions and call sites, without a separate Inputs declaration.
- **Body files.**
  A file that populates a body is named `<subject>-body.md`. The mode owns how many of that subject a request becomes.
- **Other modes.**
  Invoke another mode with Run or Follow, naming the selected scope and the whole mode or exact subsection to execute. A subsection call executes that subsection only. Calls are sequential unless concurrency is explicitly stated: complete the called work, then resume the calling step with its result; a blocker returns to the caller. Prerequisites require reading documents, not executing their procedures. Define findings in their artifact and identify the operation returning them; passive attribution to a mode does not establish a call, prior execution or a concurrent process. Called modes are listed under Prerequisites.
- **No spare parts.**
  A mode does not carry an outcome, a procedure unit, or a command its procedure never uses.
- **A new mode.**
  A new mode is a new file. An artifact is not edited to name it.
- **Interview.**
  A question the user must decide is put this way.
  - A plain-language paragraph before the question gives the context the user needs to answer it.
  - The question offers more than one choice. The recommended choice is marked on its option.
  - Wait for the user's answer. An unanswered question stays pending. A recommendation or elapsed time supplies no answer.
  - The user can select Other and specify a response beyond the options.
  - Use the native tool for presenting the question when one is available.
- **Step rules.**
  A rule that binds one step sits in that step. A rule that binds every mode is added to this section.
- **Sections.**
  Prerequisites, Procedure, Outcomes, then Guidance when the file has an assistive statement that is not a step, a condition, or a mode outcome, then Operations. Procedure and Outcomes are required, and Operations holds cross-artifact command specifications. A mode has no Rules section.

## Protocols

Read this before adding or changing a protocol.

- **One change.**
  A protocol is one change to the work that lands in several artifacts together. It changes when that change does. Where the sequence produces one nameable output shape it is an artifact operation, not a protocol, and a derived shape with no persisted document still counts.
- **Named for the situation.**
  A protocol is named for the situation it governs, as a noun phrase: Task Merge, Issue Closure, Epic Integration. Its file is `<situation>.md`.
- **Entered whole.**
  One file holds one protocol. A caller runs the file; it does not link a step. A sequence worth calling on its own is its own protocol.
- **Procedure.**
  The steps follow the mode procedure rules: numbered, each opening with a bold sentence-case action label with its instructions on the next line. Protocols identify required context in their instructions and call sites, without a separate Inputs declaration.
- **No closing summary.**
  What a protocol changes, and what a blocker leaves unchanged, is stated by the step that changes it. A protocol carries no section restating the result; a reader following the procedure and its links has it already, and a summary goes stale against the steps it describes.
- **Prerequisites.**
  Prerequisites open with `Read these files first.` They list every file the protocol's Procedure links to, including each protocol it runs.
- **No spare parts.**
  A protocol nothing runs is not a protocol. One exists because a mode or another protocol follows it.
- **A new protocol.**
  A new protocol is a new file. An artifact is not edited to name it.
- **Step rules.**
  A rule that binds one step sits in that step. A rule that binds every protocol is added to this section.
- **Sections.**
  Prerequisites, Procedure, then Guidance when the file has an assistive statement that is not a step. Procedure is required. A protocol has no Outcomes, Fields, Rules, Operations or Commands section.

## Artifacts

Read this before adding or changing an artifact.

- **One shape.**
  An artifact owns one shape and the transformations that produce it. It changes when that shape changes. Locate a procedure by the object and state it produces. A caller or a shared command does not determine ownership.
- **Virtual artifacts.**
  A derived artifact owns its output shape even when it has no persisted document. Fields defines that shape; its operations consume supplied evidence.
- **Descriptions.**
  Describe the artifact's subject and contents directly. Omit inconsequential implementation qualifiers such as virtual. Distinguish proposed changes from applied state where the caller needs that distinction; a queue is not itself proposed merely because its changes await application.
- **Prose API.**
  Artifact operations form a prose-based API addressed by subsection titles. Each names its inputs, the artifact state it reads or changes, and the output it returns. Modes call operation headings; operations call command headings. Related artifacts are supplied as evidence rather than managed through the operation.
- **Operation inputs.**
  Callers address an artifact operation through descriptive input names, such as board fields. CLI flags such as `--fields` belong to the artifact's implementation details, not the calling mode procedure. Repeated calls identify the inputs they refresh and retain.
- **Operation scope.**
  An operation exists because a procedure calls it. Classify the work by its subject and behaviour, not its verb or script name: a read that sequences access steps is an operation, and a plan that derives an artifact's state is an operation.
  - Reading, inspecting, planning, populating and validating are shapes an operation can take, not a set an artifact fills. A sibling operation is no reason to add its counterpart, and a wrapper whose body is one call to another operation is that operation.
- **Bodies and lifecycle.**
  A body artifact populates and validates document content. A subject artifact owns its readiness and completion checks from supplied evidence. Reading evidence about related artifacts does not make a check orchestration; coordinating changes to those artifacts does. Creation, metadata, linking and closure belong to the artifact for the tracked object.
- **No mode, no protocol.**
  An artifact never links to a mode or a protocol, including by naming one in prose.
- **Fields.**
  Fields defines the artifact's shape and the conditions on its elements. Common field conditions hold for the family; a kind supplements them. Fields is a `##` section, with each named field or group under `###`. The kind's template is a subsection of Fields and holds that kind's table. Field conditions do not state user goals. A condition that gates an action sits in the procedure step that performs it.
- **No procedure in Fields.**
  A field condition does not name a procedure, a step, or a command, and it does not link to one.
- **Name.**
  A file that populates a body is named `<subject>-body.md`. Its scope is that population. `issue-body.md` is the shared issue body. A kind file is `proposal-body.md`, `initiative-issue-body.md`, `epic-issue-body.md`, `task-body.md`, or `standalone-body.md`.
- **Subject names.**
  Name an artifact for its subject and an operation for its action: `board-queue.md` owns Board Queue, and Plan Board Queue is its operation. A computation script can take the subject name, such as `board-queue.py`.
- **Common file.**
  The common file names no kind. A kind's table, its title, and a check that applies only to that kind live on that kind's file. The common file holds the rules every body shares.
- **Operations.**
  Every procedural sequence occupies a named `###` subsection under Operations, including a kind's population path. Operations itself contains no steps; incorporate any overarching sequence into the named operations that perform its constituent work. Omit Operations when the artifact has only command specifications. Each subsection opens with one line on what it is for, followed by its **Inputs:** line and instructions. The opening line does not restate the steps. A step links to the shape it produces and does not restate it. A kind step links to the common procedure unit it uses and adds only the further population. It does not copy the shared rules.
- **Prerequisites.**
  Prerequisites open with `Read these files first.` They list every file the artifact's Operations, Fields or Commands link to. A kind lists `issue-body.md` because it links to it. The common file does not link to a kind.
- **Operation steps.**
  Address instructions directly to the agent, leading each step with its action. Steps have no separate bold introductory label. Multiple steps use consecutive numbering; an operation with one step uses one bullet and counts as a procedure.
- **Returned output.**
  State what the operation returns within its instructions. Do not add a separate Result line.
- **Population conditions.**
  A population step leads with the writing action and its template or owning operation. Mandatory field conditions follow as nested bullets under that step, linked to their local or shared definitions. Each condition states what must hold; field rules remain at their linked home.
- **Command implementation.**
  Commands holds the artifact's command and access specifications. Operations holds the sequences that call them. Both expose named subsections to callers.
- **No spare parts.**
  An artifact does not carry an operation, a field or a command nothing reaches. An operation no procedure cites is surface that drifts from whatever it wraps, and its capability is already reachable through the operation it would call.
- **A new kind.**
  A new kind is a new file. The common file is not edited to name it.
- **Detail.**
  A change keeps every existing condition. A shorter file is not a reason to drop one.
- **Step rules.**
  Put each action's preconditions and refusal conditions in its governing procedure step. Shared preconditions belong to a common procedure that callers invoke. Command specifications require the resulting evidence or authorization as inputs. A rule that binds every artifact is added to this section.
- **Sections.**
  Prerequisites, Operations, Fields, then Guidance when it has an assistive statement that is not a step or a field condition, then Commands when the file has command specifications. Fields is required. An artifact has no Procedure, Outcomes or Rules section.

## References

Read this before adding or changing a reference.

- **Support.**
  A reference is an ad hoc document that supports the process. It is neither a mode nor an artifact.
- **Shape.**
  It follows the shared sections above. It does not use Prerequisites, Procedure, Fields, Operations, Commands, and Outcomes.
- **Cited only.**
  A reference is only ever referred to. It cites neither a mode nor an artifact.
- **Names.**
  A sentence that names a mode or an artifact loses that name. The statement it made stays.
- **Rules.**
  A rule that binds every reference is added to this section.

## Entry Point

- **Opening.**  The bulleted list has one item for each issue type.
- **Section order.**  Rules precedes Dependencies.
- **Issue bodies.**
  The skill's prose layout applies to its instructions. Issue bodies follow [Issue Body](#issue-body); pull request bodies follow [Pull Request Body](#pull-request-body).
- **Common conventions.**
  The entry point supplies [Conventions](#conventions) before mode selection. Graph-specific setup belongs to [Repository Graph](#repository-graph).

## Progressive Disclosure

Apply the shared [progressive disclosure](../guidelines.md#progressive-disclosure) and [disclosure verification](../guidelines.md#disclosure-verification) rules to affected callers. Modes are read whole; supporting section reads inherit the mode's command prerequisites.

- **Mode routes.**
  Trace each affected mode through its common conventions, selected operations and supporting guides. Include cross-mode calls and explicit whole-file requirements.
- **Board operations.**
  Exercise a Standup request with captured board inputs, selecting multiple operations and reusing conventions. Preserve the generator's format and unresolved evidence.
- **Graph operations.**
  Exercise an Understand request with a named pull request, verifying graph-specific setup before selected graph commands and exclusion of unrelated command bodies.
- **Revision.**
  Exercise a bounded skill edit with its consumer guidance, required whole-file guidelines, local checks and reused common prerequisites.

## Changes

Follow the shared [change rules](../guidelines.md#changes) for worktree isolation, current user preferences and validation.

- **Planning adoption.**
  Commit and push the reviewed planning folder before applying its design to the installed skill. Keep the planning and installed guidelines aligned with the current preference set.
- **Integrated implementation.**
  Map the complete live skill to its intended homes. Apply document moves, embedded templates, consuming readers, script names, callers and tests together; preserve the existing conditions and remove obsolete paths.
- **Delivery.**
  Run the associated tests and integration checks before opening or updating the implementation pull request. Commit and push the changes from their owning worktrees; subsequent corrections update the same pull request.

# Modes

## Revise Mode

Changes the skill itself: SKILL.md, its modes, artifacts, references and scripts.

### Procedure

The main path meets [Outcomes](#outcomes).

1. **Read the guidelines.**
   Read the [shared skill guidelines](../../guidelines.md) and [skill guidelines](#guidelines) whole before the first edit.
2. **Understand the request.**
   Interview the user, as an [Interview](#modes), until the change and its scope are clear.
   - Find every file the change touches: the rule's home, each file that cites it, and any script, docstring or test that states it.
3. **Work in a worktree.**
   Branch a worktree for the change.
   - Commit each distinct change as its own commit.
4. **Revise.**
   Make the change in the rule's one home.
   - Link to it from every other file that needs it.
   - Write it to the guidelines' layout, prose, link and command rules as it is written, not in a later pass.
   - When the user states a new writing rule, add it to the applicable shared or skill-specific guidelines before validation and delivery.
5. **Check against the guidelines.**
   Read every changed file against the [shared skill guidelines](../../guidelines.md) and [skill guidelines](#guidelines), checking:
   - The description, when the skill's reach changed.
   - One line per item, bold leads on their own line, and sub-bullets for discrete points.
   - Each rule stated once, and no description of replaced behaviour left anywhere.
   - Every command linked to its operation section.
   - Every link and anchor resolving.
   - [Progressive disclosure](../../guidelines.md#progressive-disclosure), including complete common sections and caller prerequisites.
   - Fix each departure.
6. **Verify.**
   - Run [Run Tests](#run-tests) when an executable script, its consumed template or a test changed.
   - When SKILL.md changes, confirm its frontmatter opens and closes with `---` and holds `name` and `description`.
   - Run [Check Skill Files](#check-skill-files) for every affected skill.
   - Apply [disclosure verification](../../guidelines.md#disclosure-verification) with the skill's [representative scenarios](#progressive-disclosure).
   - Resolve every required file, command and heading without an implicit external dependency.
7. **Deliver.**
   - Commit.
   - Push.
   - Report what changed in each file.

### Outcomes

- **The skill matches the request.**
  The user has the change they asked for in the skill, committed and pushed.
- **The guidelines hold.**
  The change agrees with the guidelines, and a new rule the user stated for how the skill is written is part of that change.

### Operations

#### Run Tests

Runs the skill's script tests.

**Inputs:** Workspace checkout containing the installed skill and its tests.

```bash
cd "<workspace>/skills/work-planner" && "<workspace>/scripts/sbx" python3 -m unittest discover -s test
```

#### Check Skill Files

Checks the affected skill's Markdown structure and links.

**Inputs:** Workspace checkout and affected skill directory; repeat the skill argument for additional affected skills.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/scripts/check_skill_files.py "<skill-directory>"
```

**Example:** Work Planner in the selected checkout.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/scripts/check_skill_files.py skills/work-planner
```

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
