# Worked examples

These examples use [work-tracker](work-tracker/SKILL.md), a skill with a routing document, a planning procedure, and linked artifact documents. The [usage-example fixtures](../fixtures/usage-example) use this same source tree and record the expected bundles.

Run the commands from the repository root after [installation](../README.md#installation). Markdown blocks below are exact excerpts; links beside them open the complete files. File and directory names use hyphens rather than underscores. An entry's `prosiform.root`, when present, is a directory path relative to that file.

## Bundle a procedure and its dependencies

### Input

The [planning procedure](work-tracker/modes/plan-mode.md) links two prerequisites and defers the routing document:

```markdown
## Prerequisites

Read these files first.

- [Epic Issue Body](artifacts/epic-issue-body.md)
- [Epic](artifacts/epic.md)

The caller reached this mode through the routing document [¬ SKILL.md](SKILL.md), which this procedure defers to a run of its own.
```

### Command

```bash
cd example/work-tracker
pf modes/plan-mode.md
```

### Output

The [expected bundle](../fixtures/usage-example/a-procedure-and-everything-it-reaches/expected/stdout.md) opens with:

```markdown
This bundle was built for [Plan](#plan); everything else is material it references.
```

Its planning procedure contains:

```markdown
## Prerequisites

Read these files first.

- [Epic Issue Body](#epic-issue-body)
- [Epic](#epic)

The caller reached this mode through the routing document [¬ SKILL.md](SKILL.md), which this procedure defers to a run of its own.
```

The two prerequisites appear in the bundle, and their links point to bundle headings. The deferred link keeps its `¬` marker and uses the root-relative path `SKILL.md`; that document is excluded.

[Fixture and expected diagnostics](../fixtures/usage-example/a-procedure-and-everything-it-reaches/manifest.toml).

## Select a section

### Input

The [epic issue body](work-tracker/artifacts/epic-issue-body.md) contains this operation beneath its `Operations` heading:

```markdown
### *Record* Epic Delivery

One epic body with supplied delivery matches and completed rows recorded.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches and output body file.

1. Run [Sync Epic](#sync-epic), mapping pull requests to `--prs`, links to `--links`, task issues to `--tasks`, each confirmed match to `--link` and the output file to `--fix`.
   - Row changes must meet [Task Delivery](#task-delivery) and [Work Breakdown](#work-breakdown).
2. Return the updated body and [Delivery Findings](artifacts/epic.md#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.
```

### Command

```bash
cd example/work-tracker
pf -f artifacts/epic-issue-body.md '#record-epic-delivery'
```

### Output

The [expected bundle](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/expected/stdout.md) begins:

```markdown
This bundle was built for [Record Epic Delivery](#record-epic-delivery); everything else is material it references.

# Artifacts

## Operations

### *Record* Epic Delivery

One epic body with supplied delivery matches and completed rows recorded.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches and output body file.

1. Run [Sync Epic](#sync-epic), mapping pull requests to `--prs`, links to `--links`, task issues to `--tasks`, each confirmed match to `--link` and the output file to `--fix`.
   - Row changes must meet [Task Delivery](#task-delivery) and [Work Breakdown](#work-breakdown).
2. Return the updated body and [Delivery Findings](#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.
```

The selection retains its structural ancestor, places the selected heading beneath its declared group, and rewrites links to bundle fragments. The rest of the bundle contains the sections those links reach.

[Fixture and expected diagnostics](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/manifest.toml).

## Declare groups per file

### Above-depth prose

```bash
cd example/work-tracker
pf modes/plan-mode.md
```

The artifact files declare group `artifacts`, and the mode file declares `modes`, each at depth `2` in its frontmatter. Each linked file supplies its own settings.

For example, both artifact files begin with this declaration:

```yaml
---
prosiform:
  group: artifacts
  group-depth: 2
---
```

Place the declaration in every contributing file that belongs to the group. A shared directory alone supplies no membership. See [conversion metadata](../invocation.md#conversion-metadata) for validation and source ownership.

The [expected bundle](../fixtures/usage-example/every-document-under-a-directory-merged/expected/stdout.md) includes an `Overview` because each artifact's introductory prose needs a section:

```markdown
# Artifacts

## Overview

### Epic Issue Body

Populates one epic body. The body states one slice of the design and lists the tasks that deliver it.

The delivery lines this body records are defined in [Epic](#epic).

### Epic

An epic's task delivery findings, integration readiness and completion state.

## Operations

### Epic Issue Body
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

## Agents

Select rules for your harness:

- If you are Codex, compile [¬ Codex](rules/codex.md).
- If you are Claude, compile [¬ Claude](rules/claude.md).

## Common

- Check every link.
- Use clear headings.

Follow [Agents](#agents).
```

`Overview` is absent here. Each member keeps a distinct destination, `#agents` or `#common`. Generated headings use title case, while deferred filesystem paths keep the source spelling. The [README diagrams](../README.md#how-it-works) show this Rules grouping and the subsequent compilation of deferred agent-specific rules.

## More fixture examples

Every case below uses the same [source tree](work-tracker/SKILL.md). Each manifest records the arguments, exit status, and diagnostics.

| Example | Invocation fixture | Expected output |
| --- | --- | --- |
| Bundle a procedure | [Manifest](../fixtures/usage-example/a-procedure-and-everything-it-reaches/manifest.toml) | [Bundle](../fixtures/usage-example/a-procedure-and-everything-it-reaches/expected/stdout.md) |
| Select a fragment with `-f` | [Manifest](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/manifest.toml) | [Bundle](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/expected/stdout.md) |
| Select two sections | [Manifest](../fixtures/usage-example/two-selected-sections/manifest.toml) | [Bundle](../fixtures/usage-example/two-selected-sections/expected/stdout.md) |
| Compile declared groups | [Manifest](../fixtures/usage-example/every-document-under-a-directory-merged/manifest.toml) | [Bundle](../fixtures/usage-example/every-document-under-a-directory-merged/expected/stdout.md) |
| Validate with `-c` | [Manifest](../fixtures/usage-example/validation-without-publication/manifest.toml) | [Empty stdout](../fixtures/usage-example/validation-without-publication/expected/stdout.md) |

## Source and validation

The example prose is adapted from a real skill procedure and maintained in this repository. Each usage fixture points to this tree through a `source` symbolic link, keeping the documented inputs and corpus inputs identical. The [corpus check](../checks.md) compares actual output and diagnostics with each fixture's expectations.
