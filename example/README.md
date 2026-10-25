# Worked examples

These examples use [work-planner](work-planner/SKILL.md), a skill with a routing document, ten modes, six protocols and thirty artifact documents. The [usage-example fixtures](../fixtures/usage-example) use this same source tree and record the expected bundles.

Run the commands from the repository root after [installation](../README.md#installation). Markdown blocks below are exact excerpts; links beside them open the complete files. File and directory names use hyphens rather than underscores. An entry's `prosiform.root`, when present, is a directory path relative to that file.

## Bundle a procedure and its dependencies

### Input

The [planning procedure](work-planner/modes/plan-mode.md) links the documents its publish step reaches, and defers a third that a run of its own opens:

```markdown
6. **Publish.**
   Put the proposed [Epic Priority](artifacts/dependency-graph.md#epic-priority) map for the reviewed epics to the user as an [¬ Interview](guidelines.md#modes), the proposal the recommended answer.
   - Take the positive integer the user confirms for each epic.
   - Call [Ensure Repository Labels](artifacts/repository-labels.md#ensure-repository-labels) with the required definitions, the priority label each confirmed number names among them, before saving the issues.
```

### Command

```bash
cd example/work-planner
pf modes/plan-mode.md
```

### Output

The [expected bundle](../fixtures/usage-example/a-procedure-and-everything-it-reaches/expected/stdout.md) opens with:

```markdown
Follow [Procedure](#procedure). The other sections are material that procedure references.
```

Its publish step reads:

```markdown
6. **Publish.**
   Put the proposed [Epic Priority](#epic-priority) map for the reviewed epics to the user as an [Interview](guidelines.md#modes), the proposal the recommended answer.
   - Take the positive integer the user confirms for each epic.
   - Call [Ensure Repository Labels](#ensure-repository-labels) with the required definitions, the priority label each confirmed number names among them, before saving the issues.
```

The two documents the step links arrive in the bundle, and their headings are destinations its links point at. The deferred link drops its `¬` marker and keeps the root-relative path `guidelines.md`; that document is excluded, and the published path alone states the deferral.

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
2. Return the updated body and [Delivery Findings](artifacts/epic.md#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.
```

### Command

```bash
cd example/work-planner
pf -f artifacts/epic-issue-body.md '#record-epic-delivery'
```

### Output

The [expected bundle](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/expected/stdout.md) begins:

```markdown
Follow [Record Epic Delivery](#record-epic-delivery). The other sections are material that procedure references.

## Operations
```

The selected operation follows, beneath the section the artifacts' group merges into:

```markdown
### *Record* Epic Delivery

One epic body with supplied delivery matches and completed rows recorded.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches, project checkout and output body file.

1. Run [Sync Epic](#sync-epic), mapping pull requests to `--prs`, links to `--links`, task issues to `--tasks`, each confirmed match to `--link`, the checkout to `--project` and the output file to `--fix`.
   - Row changes must meet [Task Delivery](#task-delivery) and [Work Breakdown](#work-breakdown).
2. Return the updated body and [Delivery Findings](#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.
```

The selection retains its structural ancestor and rewrites the links the operation carries to bundle fragments. The rest of the bundle contains the sections those links reach.

[Fixture and expected diagnostics](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/manifest.toml).

## Declare groups per file

### Above-depth prose

```bash
cd example/work-planner
pf modes/plan-mode.md
```

Every artifact file declares group `artifacts` at depth `2`, with the group's own heading suppressed. A mode file declares its root and no group.

For example, the [epic](work-planner/artifacts/epic.md) begins with this declaration:

```yaml
---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 2
  group-heading: false
---
```

Place the declaration in every contributing file that belongs to the group. A shared directory alone supplies no membership. See [conversion metadata](../invocation.md#conversion-metadata) for validation and source ownership.

The [expected bundle](../fixtures/usage-example/every-document-under-a-directory-merged/expected/stdout.md) merges the artifacts into one `Overview` and one `Operations`, with each member named beneath them:

```markdown
## Overview

### Planning Record

A planning record is a folder. README.md is its entry point: it answers what the work is, and links to every other artifact the plan produces. Each artifact is the home of its own content. The progress of the work is the theme's project board.

## Operations

### Acceptance Criteria
```

`group-heading: false` omits the group's own heading, so each member is named by its H3 rather than a document title. Only a member reached as a whole document contributes prose above the grouping depth, which is why `Planning Record` is the member `Overview` holds.

### Named members beneath the group

The [my-skill](my-skill/SKILL.md) rules have no source headings. Their generated member headings name each contribution directly beneath `Rules`:

```bash
cd example/my-skill
pf -o - procedure.md rules/common.md
```

The grouped portion is:

```markdown
# Rules

## Agents

Select rules for your harness:

- If you are Codex, compile [Codex](rules/codex.md).
- If you are Claude, compile [Claude](rules/claude.md).

## Common

- Check every link.
- Use clear headings.

Follow [Agents](#agents).
```

`Overview` is absent here. Each member keeps a distinct destination, `#agents` or `#common`. Generated headings use title case, while deferred filesystem paths keep the source spelling. The [README diagrams](../README.md#how-it-works) show this Rules grouping and the subsequent compilation of deferred agent-specific rules.

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
