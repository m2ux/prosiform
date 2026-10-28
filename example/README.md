# Worked examples

These examples use [work-planner](work-planner/SKILL.md), a skill with a routing document, ten modes, twelve protocols and thirty-one artifact documents. The [usage-example fixtures](../fixtures/usage-example) use this same source tree and record the expected bundles.

Run the commands from the repository root after [installation](../README.md#installation). Markdown blocks below are exact excerpts; links beside them open the complete files. File and directory names use hyphens rather than underscores. Each link resolves from the directory of the file that writes it, the path a reader follows. A file's `prosiform.root`, when present, is a directory path relative to that file, and bounds what its links reach.

## Bundle a procedure and its dependencies

### Input

The [planning procedure](work-planner/modes/plan-mode.md) links the documents its publish step reaches:

```markdown
### 6. Publish

Put the proposed [Epic Priority](../artifacts/dependency-graph.md#epic-priority) map for the reviewed epics to the user as an [interview](../rules.md), the proposal the recommended answer.
- Take the positive integer the user confirms for each epic.
- Follow [Initiative Publication](../protocols/initiative-publication.md) with the repository, initiative prefix letter, the reviewed initiative and epic body files with their existing issue numbers, titles and labels, each epic's confirmed [priority label](../artifacts/board-queue.md#priority-sets) among them, each label's colour and description, the current pull request records, corpus branch and requirement sources, the kind templates, the record identity, folder path, evidence and decisions, and a commit message file.
- Put each blocker it returns to the user.
```

### Command

The command runs from the skill's directory and names the entry, the planning procedure, relative to it:

```bash
cd example/work-planner
pf modes/plan-mode.md
```

It writes the bundle to `modes_plan-mode.bundles/modes_plan-mode.bundle.md` in that directory, the [derived output name](../invocation.md#output) for the entry, beside a bundle for each target its dispatches reach, and writes nothing to stdout. Each run writes the same bytes, those of the expected bundle below.

### Output

The [expected bundle](../fixtures/usage-example/a-procedure-and-everything-it-reaches/expected/modes_plan-mode.bundle.md) opens with its Prosiform section, which states the Dispatch protocol its dispatch sub-section follows, then the mode's own title and preamble, which tell the agent what to follow:

```markdown
# Prosiform

## Dispatch

Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Plan Mode

Scopes the solution: the design, the criteria, and the breakdown of an initiative and its epics, and keeps them current as work lands.

Follow the [Procedure](#procedure), adhering to [Rules](#rules) and [Conventions](#conventions) and ensure all [Outcomes](#outcomes) are met.
```

Its publish step reads:

```markdown
### 6. Publish

Put the proposed [Epic Priority](#epic-priority) map for the reviewed epics to the user as an [interview](#rules), the proposal the recommended answer.

- Take the positive integer the user confirms for each epic.
- Follow [Initiative Publication](#initiative-publication) with the repository, initiative prefix letter, the reviewed initiative and epic body files with their existing issue numbers, titles and labels, each epic's confirmed [priority label](#priority-sets) among them, each label's colour and description, the current pull request records, corpus branch and requirement sources, the kind templates, the record identity, folder path, evidence and decisions, and a commit message file.
- Put each blocker it returns to the user.
```

The four documents the step links arrive in the bundle, and their headings are destinations its links point at. A link to a whole document points at the heading the bundle gives it, here `Rules` and `Initiative Publication`.

### Constructs

The bundle shows each of these constructs:

- **The Prosiform section.** The bundle dispatches, so it opens with `# Prosiform` and its `## Dispatch` protocol, in wording every bundle shares.
- **The entry's own content.** Plan Mode's title, preamble, `Procedure` and `Outcomes` follow, without the entry's frontmatter.
- **Whole documents under their titles.** Rules, Conventions and Propose Mode declare no group, and each stands as an H1 headed by its own title.
- **Declared groups.** `Artifacts`, `Protocols` and `References` head their members in title case, each member's H1 an H2 beneath the group: the eighteen artifacts the bundle's links reach, two protocols and one reference.
- **Dependency order.** Rules and Conventions follow the entry's own sections, in the order its preamble links them.
- **Compiled links.** Every link to a document or section under the root points at a heading in the bundle.
- **Distinct destinations for coinciding headings.** The `Procedure` headings of Propose Mode and Initiative Publication take `#procedure-1` and `#procedure-2`, the destinations their preambles link.
- **A dispatched link.** The `⇉` mark is dropped, the link points at a sub-section of its step naming the Sync Mode bundle the run publishes beside this one, and Sync Mode contributes no content here:

  ```markdown
  ### 9. Record Delivered Work

  When work has landed:

  - Follow [Sync Mode](#dispatch-sync-mode) for the affected initiative.
  - For each unplaced task row it returns pending:
    - Apply [Place Unplaced Task Row](#place-unplaced-task-row) with the epic JSON, that task issue, no allowance, the returned change list and delivery evidence, and an output body file.
    - Repeat Sync Mode with the refreshed epic.
  - Return the saved delivery state or blockers.

  #### Dispatch Sync Mode

  Dispatch `modes_sync-mode.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states.
  ```

- **An outside-root link.** The pull request artifact's link to GitHub's documentation keeps its authored destination.

[Fixture and expected diagnostics](../fixtures/usage-example/a-procedure-and-everything-it-reaches/manifest.toml).

## Select a section

### Input

The [epic issue body](work-planner/artifacts/epic-issue-body.md) contains this operation beneath its `Operations` heading:

```markdown
### *Record* Epic Delivery

One epic body with supplied delivery matches and completed rows recorded.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches, project checkout and output body file.

1. Run [Sync Epic](#sync-epic), mapping pull requests to `--prs`, links to `--links`, task issues to `--tasks`, each confirmed match to `--link`, the checkout to `--project` and the output file to `--fix`.
   - Row changes must meet [Task Delivery](#task-delivery) and [Work Breakdown](#work-breakdown).
2. Return the updated body and [Delivery Findings](epic.md#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.
```

### Command

```bash
cd example/work-planner
pf -f artifacts/epic-issue-body.md '#record-epic-delivery'
```

### Output

The [expected bundle](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/expected/artifacts_epic-issue-body__record-epic-delivery.bundle.md) begins with the artifacts' group heading, the epic issue body's block beneath it, and that block's `Operations` heading:

```markdown
# Artifacts

## Epic Issue Body

### Operations
```

The selected operation follows beneath it:

```markdown
#### *Record* Epic Delivery

One epic body with supplied delivery matches and completed rows recorded.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches, project checkout and output body file.

1. Run [Sync Epic](#sync-epic), mapping pull requests to `--prs`, links to `--links`, task issues to `--tasks`, each confirmed match to `--link`, the checkout to `--project` and the output file to `--fix`.
   - Row changes must meet [Task Delivery](#task-delivery) and [Work Breakdown](#work-breakdown).
2. Return the updated body and [Delivery Findings](#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.
```

The selection retains its structural ancestors and rewrites the links the operation carries to bundle fragments. The rest of the bundle contains the sections those links reach.

[Fixture and expected diagnostics](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/manifest.toml).

## Defer a document to a run of its own

### Input

The [revision procedure](work-planner/modes/revise-mode.md) opens on a step that marks the skill guidelines with `¬`:

```markdown
### 1. Read the Guidelines

Read the [shared skill guidelines](../../guidelines.md) and [¬ skill guidelines](../guidelines.md) whole before the first edit.
```

### Command

```bash
cd example/work-planner
pf modes/revise-mode.md
```

### Output

The [expected bundle](../fixtures/usage-example/a-mode-and-the-guidelines-it-defers/expected/modes_revise-mode.bundle.md) carries the step with the deferral mark removed:

```markdown
### 1. Read the Guidelines

Read the [shared skill guidelines](../../guidelines.md) and [skill guidelines](guidelines.md) whole before the first edit.
```

The deferred link's destination names the guidelines from the working directory, so `pf guidelines.md` run from that directory compiles them. The guidelines contribute no content to this bundle. The shared guidelines lie outside the root, so their link keeps its authored destination.

[Fixture and expected diagnostics](../fixtures/usage-example/a-mode-and-the-guidelines-it-defers/manifest.toml).

## Read in steps

### Input

The [delivery evidence](work-planner/artifacts/delivery-evidence.md) artifact reads a board through a step sub-section that links its `Run Board Reads` section, whose reads are step sub-sections of their own, in the order their results are taken:

```markdown
#### 1. Apply the Board Reads

Apply the [board reads](#run-board-reads).

#### 2. Return the Board Delivery Evidence

Return the [board snapshot](#board-snapshot), pull request records and complete issue-link snapshot to the caller, reporting incomplete evidence as a blocker.

#### Run Board Reads

##### 1. Read Board State

Apply [Read Board State](board.md#read-board-state) with the board owner and number for its items, Status field and [repositories](board.md#repositories).

##### 2. Fetch Initiative Pull Requests

Apply [Fetch All Initiative Pull Requests](pull-request.md#fetch-all-initiative-pull-requests) for each repository Read Board State returned, for the pull request records.
```

### Command

The [board procedure](work-planner/modes/advance-mode.md) applies that operation in its read step:

```bash
cd example/work-planner
pf modes/advance-mode.md
```

### Output

The [expected bundle](../fixtures/usage-example/a-mode-and-the-board-reads-it-steps-through/expected/modes_advance-mode.bundle.md) points the link at the compiled `Run Board Reads` section, whose steps sit one level below it and whose calls point at their headings in the bundle:

```markdown
##### 1. Apply the Board Reads

Apply the [board reads](#run-board-reads).

##### 2. Return the Board Delivery Evidence

Return the [board snapshot](#board-snapshot), pull request records and complete issue-link snapshot to the caller, reporting incomplete evidence as a blocker.

##### Run Board Reads

###### 1. Read Board State

Apply [Read Board State](#read-board-state) with the board owner and number for its items, Status field and [repositories](#repositories).

###### 2. Fetch Initiative Pull Requests

Apply [Fetch All Initiative Pull Requests](#fetch-all-initiative-pull-requests) for each repository Read Board State returned, for the pull request records.
```

[Fixture and expected diagnostics](../fixtures/usage-example/a-mode-and-the-board-reads-it-steps-through/manifest.toml).

## Declare groups per file

### One block per document

```bash
cd example/work-planner
pf modes/hoist-mode.md
```

Every artifact file declares group `artifacts` at depth `1`. A mode file declares its root and no group.

For example, the [epic](work-planner/artifacts/epic.md) begins with this declaration:

```yaml
---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
```

Place the declaration in every contributing file that belongs to the group. A shared directory alone supplies no membership. See [conversion metadata](../invocation.md#conversion-metadata) for validation and source ownership.

The [expected bundle](../fixtures/usage-example/artifacts-and-references-under-declared-groups/expected/modes_hoist-mode.bundle.md) opens the group with its name in title case. Each artifact's H1 becomes one H2 beneath it, carrying that artifact's own `Operations`, `Fields` and `Commands`. The artifacts stand in the order the bundle first links to each, so the issue the mode's first step applies leads:

```markdown
# Artifacts

## Issue

### Operations

#### *Read* Tracker Issue
```

No two artifacts share a title, so each heading keeps its source text, and a link to a whole artifact resolves to the H2 its title heads.

The [requirement characteristics](work-planner/references/requirement-characteristics.md) document declares group `references` at depth `1` in the same way, so the bundle opens that group with its name in title case and carries the member's H1 beneath it:

```markdown
# References

## Requirement Characteristics
```

### Named members beneath the group

The [my-skill](my-skill/SKILL.md) rules have no source headings. Their generated member headings name each contribution directly beneath `Rules`:

```bash
cd example/my-skill
pf procedure.md rules/common.md
```

The grouped portion is:

```markdown
# Rules

## Common

- Check every link.
- Use clear headings.

Follow [Agents](#agents).

## Agents

Select rules for your harness:

- If you are Codex, compile [Codex](rules/codex.md).
- If you are Claude, compile [Claude](rules/claude.md).
```

`Common` leads because the command line names it, and `Agents` follows at the link `Common` carries. Each member keeps a distinct destination, `#agents` or `#common`. Generated headings use title case, while deferred filesystem paths keep the source spelling. The [README diagram](../README.md#how-it-works) shows this Rules grouping.

## More fixture examples

Every case below uses the same [source tree](work-planner/SKILL.md). Each manifest records the arguments, exit status, and diagnostics.

| Example | Invocation fixture | Expected output |
| --- | --- | --- |
| Bundle a procedure | [Manifest](../fixtures/usage-example/a-procedure-and-everything-it-reaches/manifest.toml) | [Bundle](../fixtures/usage-example/a-procedure-and-everything-it-reaches/expected/modes_plan-mode.bundle.md) |
| Select a fragment with `-f` | [Manifest](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/manifest.toml) | [Bundle](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/expected/artifacts_epic-issue-body__record-epic-delivery.bundle.md) |
| Select two sections | [Manifest](../fixtures/usage-example/two-selected-sections/manifest.toml) | [Bundle](../fixtures/usage-example/two-selected-sections/expected/artifacts_epic-issue-body__record-epic-delivery+artifacts_epic__delivery-findings.bundle.md) |
| Defer a document with `¬` | [Manifest](../fixtures/usage-example/a-mode-and-the-guidelines-it-defers/manifest.toml) | [Bundle](../fixtures/usage-example/a-mode-and-the-guidelines-it-defers/expected/modes_revise-mode.bundle.md) |
| Read in steps | [Manifest](../fixtures/usage-example/a-mode-and-the-board-reads-it-steps-through/manifest.toml) | [Bundle](../fixtures/usage-example/a-mode-and-the-board-reads-it-steps-through/expected/modes_advance-mode.bundle.md) |
| Compile declared groups | [Manifest](../fixtures/usage-example/artifacts-and-references-under-declared-groups/manifest.toml) | [Bundle](../fixtures/usage-example/artifacts-and-references-under-declared-groups/expected/modes_hoist-mode.bundle.md) |
| Validate with `-c` | [Manifest](../fixtures/usage-example/validation-without-publication/manifest.toml) | None: the run writes no bundle |

## Source and validation

The example prose is adapted from a real skill procedure and maintained in this repository. Each usage fixture points to this tree through a `source` symbolic link, keeping the documented inputs and corpus inputs identical. The [corpus check](../checks.md) compares actual output and diagnostics with each fixture's expectations.
