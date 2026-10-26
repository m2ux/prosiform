# Worked examples

These examples use [work-planner](work-planner/SKILL.md), a skill with a routing document, ten modes, six protocols and thirty artifact documents. The [usage-example fixtures](../fixtures/usage-example) use this same source tree and record the expected bundles.

Run the commands from the repository root after [installation](../README.md#installation). Markdown blocks below are exact excerpts; links beside them open the complete files. File and directory names use hyphens rather than underscores. Each link resolves from the directory of the file that writes it, the path a reader follows. A file's `prosiform.root`, when present, is a directory path relative to that file, and bounds what its links reach.

## Bundle a procedure and its dependencies

### Input

The [planning procedure](work-planner/modes/plan-mode.md) links the documents its publish step reaches:

```markdown
6. **Publish.**
   Put the proposed [Epic Priority](../artifacts/dependency-graph.md#epic-priority) map for the reviewed epics to the user as an [interview](../rules.md), the proposal the recommended answer.
   - Take the positive integer the user confirms for each epic.
   - Follow [Initiative Publication](../protocols/initiative-publication.md) with the repository, initiative prefix letter, the reviewed initiative and epic body files with their existing issue numbers, titles and labels, each epic's confirmed priority label among them, each label's colour and description, the current pull request records, corpus branch and requirement sources, the kind templates, the record identity, folder path, evidence and decisions, and a commit message file.
   - Put each blocker it returns to the user.
```

### Command

```bash
cd example/work-planner
pf modes/plan-mode.md
```

### Output

The [expected bundle](../fixtures/usage-example/a-procedure-and-everything-it-reaches/expected/stdout.md) opens on the mode's own title and preamble, which tell the agent what to follow:

```markdown
# Plan Mode

Scopes the solution: the design, the criteria, and the breakdown of an initiative and its epics, and keeps them current as work lands.

Follow the [Procedure](#procedure), adhering to [Rules](#rules) and [Conventions](#conventions) and ensure all [Outcomes](#outcomes) are met.
```

Its publish step reads:

```markdown
6. **Publish.**
   Put the proposed [Epic Priority](#epic-priority) map for the reviewed epics to the user as an [interview](#rules), the proposal the recommended answer.
   - Take the positive integer the user confirms for each epic.
   - Follow [Initiative Publication](#initiative-publication) with the repository, initiative prefix letter, the reviewed initiative and epic body files with their existing issue numbers, titles and labels, each epic's confirmed priority label among them, each label's colour and description, the current pull request records, corpus branch and requirement sources, the kind templates, the record identity, folder path, evidence and decisions, and a commit message file.
   - Put each blocker it returns to the user.
```

The three documents the step links arrive in the bundle, and their headings are destinations its links point at. A link to a whole document points at the heading the bundle gives it, here `Rules` and `Initiative Publication`.

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

The [expected bundle](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/expected/stdout.md) begins with the artifacts' group heading, the epic issue body's block beneath it, and that block's `Operations` heading:

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

The [expected bundle](../fixtures/usage-example/every-document-under-a-directory-merged/expected/stdout.md) opens the group with its name in title case. Each artifact's H1 becomes one H2 beneath it, carrying that artifact's own `Operations`, `Fields` and `Commands`. The artifacts stand in the order the bundle first links to each, so the issue the mode's first step applies leads:

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
pf -o - procedure.md rules/common.md
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

`Common` leads because the command line names it, and `Agents` follows at the link `Common` carries. Each member keeps a distinct destination, `#agents` or `#common`. Generated headings use title case, while deferred filesystem paths keep the source spelling. The [README diagrams](../README.md#how-it-works) show this Rules grouping and the subsequent compilation of deferred agent-specific rules.

## More fixture examples

Every case below uses the same [source tree](work-planner/SKILL.md). Each manifest records the arguments, exit status, and diagnostics.

| Example | Invocation fixture | Expected output |
| --- | --- | --- |
| Bundle a procedure | [Manifest](../fixtures/usage-example/a-procedure-and-everything-it-reaches/manifest.toml) | [Bundle](../fixtures/usage-example/a-procedure-and-everything-it-reaches/expected/stdout.md) |
| Select a fragment with `-f` | [Manifest](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/manifest.toml) | [Bundle](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/expected/stdout.md) |
| Select two sections | [Manifest](../fixtures/usage-example/two-selected-sections/manifest.toml) | [Bundle](../fixtures/usage-example/two-selected-sections/expected/stdout.md) |
| Compile declared groups | [Manifest](../fixtures/usage-example/every-document-under-a-directory-merged/manifest.toml) | [Bundle](../fixtures/usage-example/every-document-under-a-directory-merged/expected/stdout.md) |
| Validate with `-c` | [Manifest](../fixtures/usage-example/validation-without-publication/manifest.toml) | [Empty stdout](../fixtures/usage-example/validation-without-publication/expected/stdout.md) |

## Source and validation

The example prose is adapted from a real skill procedure and maintained in this repository. Each usage fixture points to this tree through a `source` symbolic link, keeping the documented inputs and corpus inputs identical. The [corpus check](../checks.md) compares actual output and diagnostics with each fixture's expectations.
