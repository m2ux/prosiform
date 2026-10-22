# Worked examples

These examples use [work-tracker](work-tracker/SKILL.md), a skill with a routing document, a planning procedure, and linked artifact documents. The [usage-example fixtures](../fixtures/usage-example) use this same source tree and record the expected bundles.

Run the commands from the repository root after [installation](../README.md#installation). Markdown blocks below are exact excerpts; links beside them open the complete files.

## Bundle a procedure and its dependencies

### Input

The [planning procedure](work-tracker/modes/plan-mode.md) links two prerequisites and defers the routing document:

```markdown
## Prerequisites

Read these files first.

- [Epic Issue Body](../artifacts/epic-issue-body.md)
- [Epic](../artifacts/epic.md)

The caller reached this mode through the routing document [¬ SKILL.md](../SKILL.md), which this procedure defers to a run of its own.
```

### Command

```bash
prosiform --root example/work-tracker modes/plan-mode.md
```

### Output

The [expected bundle](../fixtures/usage-example/a-procedure-and-everything-it-reaches/expected/stdout.md) opens with:

```markdown
This bundle was built for [Modes/Plan-Mode](#modesplan-mode); everything else is material it references.
```

Its planning procedure contains:

```markdown
## Prerequisites

Read these files first.

- [Epic Issue Body](#artifactsepic-issue-body)
- [Epic](#artifactsepic)

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
2. Return the updated body and [Delivery Findings](epic.md#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.
```

### Command

```bash
prosiform --root example/work-tracker \
  --from artifacts/epic-issue-body.md '#record-epic-delivery'
```

### Output

The [expected bundle](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/expected/stdout.md) begins:

```markdown
This bundle was built for [Record Epic Delivery](#record-epic-delivery); everything else is material it references.

# Artifacts/Epic-Issue-Body

### Operations

#### *Record* Epic Delivery

One epic body with supplied delivery matches and completed rows recorded.

**Inputs:** Epic JSON, pull request records, complete issue-link snapshot, task issue records, confirmed task-to-pull-request matches and output body file.

1. Run [Sync Epic](#sync-epic), mapping pull requests to `--prs`, links to `--links`, task issues to `--tasks`, each confirmed match to `--link` and the output file to `--fix`.
   - Row changes must meet [Task Delivery](#task-delivery) and [Work Breakdown](#work-breakdown).
2. Return the updated body and [Delivery Findings](#delivery-findings) for the caller to resolve and publish. An unmerged epic base prevents a closable result.
```

The selection retains its structural ancestor, shifts the selected heading down one level, and rewrites links to bundle fragments. The rest of the bundle contains the sections those links reach.

[Fixture and expected diagnostics](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/manifest.toml).

## More fixture examples

Every case below uses the same [source tree](work-tracker/SKILL.md). Each manifest records the arguments, exit status, and diagnostics.

| Example | Invocation fixture | Expected output |
| --- | --- | --- |
| Bundle a procedure | [Manifest](../fixtures/usage-example/a-procedure-and-everything-it-reaches/manifest.toml) | [Bundle](../fixtures/usage-example/a-procedure-and-everything-it-reaches/expected/stdout.md) |
| Select a fragment with `--from` | [Manifest](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/manifest.toml) | [Bundle](../fixtures/usage-example/a-bare-fragment-and-its-referring-document/expected/stdout.md) |
| Select two sections | [Manifest](../fixtures/usage-example/two-selected-sections/manifest.toml) | [Bundle](../fixtures/usage-example/two-selected-sections/expected/stdout.md) |
| Merge directories with `--group` | [Manifest](../fixtures/usage-example/every-document-under-a-directory-merged/manifest.toml) | [Bundle](../fixtures/usage-example/every-document-under-a-directory-merged/expected/stdout.md) |
| Validate with `--check` | [Manifest](../fixtures/usage-example/validation-without-publication/manifest.toml) | [Empty stdout](../fixtures/usage-example/validation-without-publication/expected/stdout.md) |

## Source and validation

The example prose is adapted from a real skill procedure and maintained in this repository. Each usage fixture points to this tree through a `source` symbolic link, keeping the documented inputs and corpus inputs identical. The [corpus check](../checks.md) compares actual output and diagnostics with each fixture's expectations.
