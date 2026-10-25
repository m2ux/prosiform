# Validation — W03

> Delivery Record · Created 2026-10-25

## Overview

AC4's instrument is the frontmatter of every file and a bundle of each mode.
AC5's is the headings of each mode's bundle. Both pass: every file declares only
the four admitted keys — thirty-seven adding declarations and twelve left with
the single key they carried — and every mode's bundle shows the folder groups the
declarations call for.

Each command ran in `.worktrees/i02-e00-w03` at the branch head the pull request
publishes, from `example/work-planner` where the invocation is relative to that
directory. Before and after figures come from the same build: the pre-change
tree exported with `git archive dab65c4c`, the post-change tree the branch
carries.

## After — AC4

The instrument is the declaration every file reports. Each file's frontmatter was
read as YAML and its `prosiform` key set recorded.

| `prosiform` key set | Files |
| --- | --- |
| `group`, `group-depth`, `group-heading`, `root` | 30 |
| `group`, `group-depth`, `root` | 7 |
| `root` | 12 |
| **Total** | **49** |
| Files carrying a key outside the four | 0 |

The thirty that carry all four are the artifacts. The seven carrying three are
the six protocols and the one reference, whose group heading is emitted by
default and so is not declared. The twelve carrying one are the ten modes,
`SKILL.md` and `guidelines.md`.

`dispatch` is the fifth key the build admits, and no file declares it. A copy of
the tree with `grouping: "x"` added to `artifacts/issue.md` is refused with
`E_INVALID_CONVERSION_METADATA: unknown field prosiform.grouping` at
`artifacts/issue.md:7:3`, reached from `modes/plan-mode.md` through
`modes/propose-mode.md` — so a key outside the four fails the bundle that reaches
it rather than passing unobserved.

Two further copies hold the value validations:

```text
E_GROUP_DEPTH_CONFLICT: prosiform.group-depth for group 'artifacts' is 2; another member declares 1
  location: artifacts/architecture-overview.md:5:16
  related: artifacts/issue.md:5:16: prosiform.group-depth for group 'artifacts' is 1

E_GROUP_DEPTH_CONFLICT: prosiform.group-heading for group 'artifacts' is false; another member declares true
  location: artifacts/architecture-overview.md:6:18
  related: artifacts/issue.md:6:18: prosiform.group-heading for group 'artifacts' is true
```

Each member of a group thus has to agree with every other, and the failure names
both locations.

Every file was also compiled as its own entry, so each declaration was read in
a run of its own: 48 of the 49 compile, and `modes/deliver-mode.md` is refused at
the default hop budget as the next section records. That refusal is a closure
depth, not a metadata defect, and `-E 9` compiles it.

## After — AC5

Each mode is a whole-document entry. The table records what its bundle's headings
show, read from the bundle as CommonMark so that headings inside a template's
fenced block are not counted.

| Mode | `Artifacts` H1 | Sections at H2 | Artifact variants at H3 | `Protocols` H1 | Protocol members at H2 | `References` H1 | Reference members at H2 | Other H1s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `advance-mode` | absent | 3: Commands, Fields, Operations | 7 | present | Change Overview | absent | — | Advance Mode, Modes/Understand-Mode, Sync-Mode |
| `align-mode` | absent | 4: Commands, Fields, Operations, Overview | 19 | absent | — | present | Requirement Characteristics | Align Mode |
| `deliver-mode` | absent | 5: Commands, Fields, Guidance, Operations, Overview | 17 | present | Change Overview | absent | — | Deliver Mode, Advance-Mode, Guidelines, Modes/Hoist-Mode, Modes/Understand-Mode, Sync-Mode |
| `hoist-mode` | absent | 4: Commands, Fields, Operations, Overview | 12 | absent | — | absent | — | Hoist Mode, Guidelines |
| `plan-mode` | absent | 3: Commands, Fields, Operations | 11 | present | Change Overview | absent | — | Plan Mode, Modes/Propose-Mode, Modes/Understand-Mode, Sync-Mode |
| `propose-mode` | absent | 3: Commands, Fields, Operations | 5 | absent | — | absent | — | Propose Mode |
| `revise-mode` | absent | 4: Commands, Fields, Operations, Overview | 3 | absent | — | absent | — | Revise Mode, SKILL, Guidelines |
| `standup-mode` | absent | 3: Commands, Fields, Operations | 7 | present | Change Overview | absent | — | Standup Mode, Modes/Understand-Mode, Sync-Mode |
| `sync-mode` | absent | 3: Commands, Fields, Operations | 7 | present | Change Overview | absent | — | Sync Mode, Modes/Understand-Mode |
| `understand-mode` | absent | 3: Commands, Fields, Operations | 7 | present | Change Overview | absent | — | Understand Mode |

Each column reads against the criterion:

- **No `Artifacts` heading appears in any bundle.** The ten rows report absent.
  The column also records the same word as an authored section: `## Artifacts`
  at depth 2 in `revise-mode`, whose bundle carries `guidelines.md` whole, and
  `#### Artifacts` at depth 4 in the six bundles that reach the planning
  record's own `Artifacts` field. A document's section named Artifacts is not a
  group heading, and its depth follows the document's own arrangement. Where an
  artifact member's H1 was `# Artifacts/Architecture-Overview` before, the text
  `Architecture Overview` names a subsection of a merged section now.
- **Artifacts sit at depth two.** A member's content at the grouping depth is
  merged into the group's `## Operations`, `## Fields`, `## Commands` and
  `## Guidance`, and each document contributing a heading text several members
  contribute is named by a variant at H3. Nineteen such variant names appear in
  `align-mode`'s `Fields`, and five in `propose-mode`'s `Operations`. A member
  whose content is all at the grouping depth is named by the merged sections it
  contributes to, as `grouping.py` states.
- **Protocols and References head their members at depth one.** `Protocols`
  is an H1 whose member `Change Overview` is an H2 in the six modes that run it.
  `References` is an H1 whose member `Requirement Characteristics` is an H2 in
  `align-mode`, the one mode that cites it.
- **Modes and guidelines are ungrouped.** Every mode's bundle carries its
  siblings and the guidelines as document groups named by their root-relative
  path, not merged into a group: `Modes/Understand-Mode`, `Sync-Mode`,
  `Modes/Hoist-Mode`, `Guidelines`, `SKILL`. No bundle carries a `Modes` or
  `Guidelines` group heading, which is what a declaration on those files would
  emit.

### What changed in the arrangement

Before the declarations, each artifact was its own document group headed by its
path — `# Artifacts/Architecture-Overview` — and each protocol and the reference
likewise. After them, the artifacts merge into one group and the protocols and
the reference merge into theirs.

| Mode | Bytes before | Bytes after | Delta | Closure | Merged into a group |
| --- | --- | --- | --- | --- | --- |
| `advance-mode` | 63450 | 63429 | −21 | 11 | 8 |
| `align-mode` | 129795 | 129745 | −50 | 21 | 20 |
| `deliver-mode` | 162144 | 162095 | −49 | 24 | 18 |
| `hoist-mode` | 83911 | 83889 | −22 | 14 | 12 |
| `plan-mode` | 88525 | 88442 | −83 | 16 | 12 |
| `propose-mode` | 23084 | 23034 | −50 | 6 | 5 |
| `revise-mode` | 42098 | 42097 | −1 | 6 | 3 |
| `standup-mode` | 61472 | 61451 | −21 | 11 | 8 |
| `sync-mode` | 57490 | 57469 | −21 | 10 | 8 |
| `understand-mode` | 44041 | 44020 | −21 | 9 | 8 |

The Closure column is the number of documents the run reads, and the last column
counts those that merged into a group: `align-mode` reads 19 artifacts and the
reference. The remainder of each closure is the ungrouped material — the mode
itself, the modes it runs and the guidelines — which the declarations leave as
document groups named by their root-relative path.

Every bundle shrank, because a group heading, a member's own H1 and the blank
lines around them are replaced by merged section headings. No content left any
bundle: after compiled link targets are set aside, the body lines of every mode's
bundle are identical before and after, at 789 lines for `advance-mode` through
1815 for `deliver-mode`.

`deliver-mode` is bundled at `-E 9`; at the default `-E 8` it is refused with
`E_RESOURCE_LIMIT` at nine link hops, which is the finding W02 recorded and #263
carries as its W04. The declarations do not change its hop depth: it is refused
before and after with the same diagnostic, and the 162095-byte figure is the
`-E 9` bundle.

### Compiled links

Every compiled in-bundle link in every mode resolves to a heading the bundle
emits, apart from one target per bundle: `#test-plan`, which appears inside the
pull request body's template as `[Test Plan](#test-plan)` and is a placeholder in
authored template text rather than a link the run compiled. The count of that
target is the same before and after in every mode.

## Checks

| Command | Result | Notes |
| --- | --- | --- |
| `make links` | pass | `--online`, every reference in 101 documents resolved |
| `make layout` | pass | `docs/` 10, `fixtures/` 964, `src/` 39 |
| `make tables` | pass | 16 commands, 8 declarations |
| `make vocabulary` | pass | 38 terms across 24 sources |
| `make test` | pass | 1099 passed |
| `make harness` | pass | 626 passed |
| `make smoke` | pass | the installed command is reachable and bundles |
| `make lock-check` | pass | 24 packages resolved from the lock |
| `make lint` | pass | `ruff check` |
| `make format-check` | pass | 64 files already formatted |
| `make typecheck` | pass | `mypy`, 63 source files |
| `make corpus` | pass with a bound build | 260 fixtures, 260 pass, 0 fail |
| `make invocation` | pass with a bound build | 28 statements held to the build |
| `make conformance` | pass with a bound build | 305 clauses, 55 covered by no fixture, 0 declaration naming no clause |
| `make independence` | pass with a bound build | every declared word is one the contract states |
| `make check` | not run | Runs the corpus, which needs `PROSIFORM_BUILD`; the targets above were run individually |

The four targets that read a build were run with
`PROSIFORM_BUILD="uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i02-e00-w03/src --frozen pf"`.
The relative form `--project src` fails from the corpus's own working directory
with `Project directory 'src' does not exist`, which reports 260 fixture failures
that are the binding and not the build.

## The Finding

The declarations are one-way for this tree: they compose folders that were flat,
and nothing depends on the flat arrangement. Three properties are worth W05 and
W06 knowing.

- **A group's member headings move down one level per depth.** Artifacts declare
  depth two, so their sections are merged at H2 and their subsections follow at
  H3 and H4. Protocols and the reference declare depth one, so their sections are
  their own H2s under the group's H1. A fixture that records headings records
  these levels.
- **A member's own H1 becomes a variant heading or disappears.** Where a member's
  H1 text is unique in the group, it is the variant heading naming that document
  in each merged section; where several members share a section's heading text,
  the variant names the document. So `# Architecture Overview` no longer heads a
  document group; the text `Architecture Overview` heads a subsection of
  `Operations` and of `Fields`.
- **`deliver-mode` still needs `-E 9`.** The declarations neither fix nor worsen
  it, and a per-mode bundle of every mode at the default budget is #263 W04's
  criterion.

## Debt This Row Finds

| Item | Classification | Disposition |
| --- | --- | --- |
| `deliver-mode` is refused at the default `-E 8` at nine hops | non-trivial | Deferred to #263 as its W04, already raised by W02 |
| `[Test Plan](#test-plan)` inside a template's fenced block names a target no bundle emits | trivial | Recorded here; the text is authored template content, and the run compiles no link for it |
| An artifact member's content wholly at the grouping depth is reachable only through the merged sections it contributes to | trivial | Follows from the declared depth and is `grouping.py`'s stated arrangement; no change is made |

The hop item was raised by W02 and needs no second row. The other two are
properties of the tree rather than defects, and neither blocks a criterion.

## Plan Changes

| Change | Kind | Applied or held |
| --- | --- | --- |
| W03's row on #258 links the merged pull request [#266](https://github.com/m2ux/prosiform/pull/266) | Task delivery | Applied |
| AC4 and AC5 on #258 ticked | Criterion evidence | Applied |
| `declarations.md` added to the record as the declaration table | Folded work | Applied |
| `README.md`'s Artifacts table names the declaration and validation artifacts | Folded work | Applied |
| `w03.md`'s Test row states what depth two means in a bundle | Folded work | Applied |
| #258 stays In Progress on board 18 | Board state | Applied |
| #258 moved to Done on board 18 | Folded work | Held — four rows remain undelivered |
| A row on #263 for the hop depth | Task creation | Not needed — W02 raised it as #263's W04, with AC4 already stating what its fix makes true |

## Merge

| Fact | Value |
| --- | --- |
| Pull request | [#266](https://github.com/m2ux/prosiform/pull/266) |
| Merge commit | `1e2dc068a7e971ac0a7208d7a3466f76c07fbe00` |
| Method | merge commit |
| Epic base after | `1e2dc068`, four rows undelivered |
| Check | `Checks` completed `success` on the head commit `0671572e` |
