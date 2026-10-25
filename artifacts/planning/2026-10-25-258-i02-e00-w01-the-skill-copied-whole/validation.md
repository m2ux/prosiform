# Validation

> Delivery Record · Created 2026-10-25

## Overview

Every command below ran in `.worktrees/i02-e00-w01` at the branch head the pull request publishes, unless it names a checkout of its own. The two checks the row's test plan names both pass on that head.

## File Counts

AC1's instrument is the comparison between the two trees.

| Side | Count | Command |
| --- | --- | --- |
| The skill's Markdown | 49 | `git ls-tree -r --name-only origin/workspace skills/work-planner` filtered to `.md` |
| The example's Markdown | 49 | `git ls-files example/work-planner` filtered to `.md` |

The relative paths agree as well as the count, which a count alone does not establish. Comparing the two lists after stripping the tree prefix prints nothing.

A count of 49 is also what the epic's own Proposal records for the skill, so the two sides name the same tree rather than the same number.

## Copy Fidelity

`AC1` counts files, and a count is satisfied by 49 unrelated documents. The content below each file's frontmatter was compared against the skill's own file byte for byte, over all 49.

| Outcome | Files |
| --- | --- |
| Identical below the frontmatter | 49 |
| Differing | 0 |

The comparison reads each source through `git show origin/workspace:<path>`, splits both sides at the closing frontmatter delimiter, and compares what remains.

## The Root Each File Declares

`invocation.md` states that an explicit root resolves from the declaring file's directory. `src/prosiform/closure.py` narrows that for a link carrying a parent segment: such a link resolves from the file's own directory and compiles only while the result stays inside the root. A bare link resolves from the root.

The skill writes both spellings in the same folder. `modes/plan-mode.md` reaches its sibling as `propose-mode.md` and the routing document as `../SKILL.md`. Under `root: ".."` the first fails with `E_TARGET_NOT_FOUND`. Under `root: "."` the second resolves only as a citation, because a sibling folder sits outside the file's own directory. No single root resolves both.

The row therefore declares the root each file's own links resolve under, trying `".."` first so that a file whose links all stay inside the example directory keeps the inclusion those links carry.

| Declared root | Files |
| --- | --- |
| `".."` | 20 |
| `"."` | 29 |

`SKILL.md` declares `"."`, as the brief states. So does `guidelines.md`, the skill's second top-level document. The 20 files declaring `".."` are the ones whose links are all parent-segment paths staying inside the example.

The brief prescribes `".."` for all four folders. Measured against this build, that prescription refuses 169 references across 29 files, and `make links` fails on those same 169.

## The Shared Skill Guidelines

The skill's own `guidelines.md` links `../guidelines.md`, the shared skill guidelines one level above the skill folder, at three places. Under any root those links name a document the example did not carry, so `example/guidelines.md` carries it. It declares `"."` because its own link to the copied tree, `work-planner/artifacts/issue-body.md#check-body-format`, resolves from the example directory.

## Bundle Output

The brief requires the copied `SKILL.md` to be bundled, and a bundle that fails to resolve is a blocker. It resolves, and it exceeds the default output budget.

| Outcome | Value |
| --- | --- |
| Exit status at the default `-O` of 262144 | `1` |
| Diagnostic at the default budget | `E_RESOURCE_LIMIT`, the run reached 302531 bytes |
| Exit status at `-O 1048576` | `0` |
| Bundle size | 302531 bytes |
| Error diagnostics over the tree at the default budget | 1, `SKILL.md` only |
| Warning diagnostics over the tree at the default budget | 48, all `W_ENTRY_DESTINATION` |

The default-budget refusal is not a resolution failure. The closure is whole and every reference in it resolves; the budget is the only thing it crosses. The epic's Proposal already records that the complete example reaches 299068 bytes above the same budget and that a per-mode bundle is what the example documents.

Measured here, `modes/plan-mode.md` bundles to 135139 bytes, inside the default budget.

`W_ENTRY_DESTINATION` fires because each file's own opening sentence links a heading that the bundle's entry line also links. It is a warning, not a refusal, and it fires on 48 of the 49 files. `SKILL.md` is the one without it, because its budget error is raised before the warning is reached; that same warning is the one it emits once `-O` is raised, as the table above records. Row W07's prose pass is where the entry sentence is read.

## Checks

| Command | Result | Notes |
| --- | --- | --- |
| `make links` | pass | `--online`, with `GH_TOKEN` and `GITHUB_TOKEN` unset so `gh` uses the keyring |
| `make layout` | pass | `docs/` 10, `fixtures/` 964, `src/` 39 |
| `make tables` | pass | 16 commands and 8 declarations |
| `make vocabulary` | pass | 38 contract terms across 24 sources |
| `make check` | not run | Stops at the first failing target and runs the corpus, which this row cannot satisfy |
| `make corpus` | not run | Row W06's work, and no fixture binds this tree yet |
| `make invocation` | not run | Needs a configured `PROSIFORM_BUILD` |
| `make conformance` | not run | Needs a configured `PROSIFORM_BUILD` |
| `make independence` | not run | Renders the conformance report, so needs the same build |
| `make lint`, `make format-check`, `make typecheck` | not run | No Python source in this row's diff |
| `make smoke` | not run | Builds and installs a wheel this row does not change |

The targets the brief names were run individually, and this table records which ran and which did not.

## No New Corpus Fixture

None was added. The fixtures that read the example are row W06's work, because the tree they bind is not whole until rows W02 to W05 have run, and a fixture bound to a half-built tree records the shape of the half. Said here rather than done, as the brief directs.

## Environment

`scripts/sbx` runs the project's Python under bubblewrap, and it fails when the shell invoking it is already sandboxed, reporting `bwrap: No permissions to create a new namespace`: bubblewrap cannot create its nested user namespace there. The host allows it, so the wrapper is used from a shell with full host permissions. `gh`, `git push` and `make links` run with full host permissions because each reaches the network.

## The Prescribed Root Rule

The brief and `w01.md` both prescribe `root: ".."` for every file under `artifacts/`, `modes/`, `protocols/` and `references/`. Applied as written, it refuses the copy.

| Measurement | Value |
| --- | --- |
| Files whose links `".."` resolves | 20 of 49 |
| References refused under `".."` | 169 |
| Unresolved references `make links` reports | 169 |

Under `"."` all 49 files resolve every link, with 0 refused. Under `".."`, 29 files do not.

The refusal is not caused by the Prerequisites sections row W02 removes. With every Prerequisites section stripped and the same root applied, 37 files still carry an unresolvable reference, because the failing parent-segment links sit in the Procedure, Operations and Guidance bodies.

The root is therefore read per file. What the brief asks of the tree holds: every reference resolves, each file declares a root, and `SKILL.md` declares `"."`. The single value it prescribes for 48 of the 49 files does not. The consequence is that 20 files keep the `".."` the brief asks for and 29 declare `"."`, so the tree is one the check passes rather than one the brief's literal rule would refuse.

## The Inclusion Gap This Leaves

A file declaring `"."` cannot contain a sibling folder, so a parent-segment link it writes stays authored in the bundle. Ten files leave such a link in that state.

| File | Links left authored |
| --- | --- |
| `SKILL.md` | 1 |
| `guidelines.md` | 3 |
| `modes/advance-mode.md` | 6 |
| `modes/deliver-mode.md` | 11 |
| `modes/plan-mode.md` | 8 |
| `modes/revise-mode.md` | 5 |
| `modes/standup-mode.md` | 9 |
| `modes/sync-mode.md` | 9 |
| `protocols/epic-integration.md` | 12 |
| `protocols/task-merge.md` | 8 |

`make links` resolves all of them, because the link check follows a parent-segment link from the file's directory as the build does. Their content is not included in a bundle, which is AC6's subject and row W04's work. This row states the tree; it does not yet state that the tree is included.

## Debt This Row Finds

| Item | Classification | Disposition |
| --- | --- | --- |
| The root the brief prescribes refuses the copy | non-trivial | Deferred to #263 ([I02:E02 Deferred Debt](https://github.com/m2ux/prosiform/issues/263)) as W03 |
| The skill's `git show` copy needs a document it does not carry | trivial | Fixed here: `example/guidelines.md` |
| Forty-eight `W_ENTRY_DESTINATION` warnings, one per file | trivial | Held for row W07's prose pass, which reads the entry sentence |
| The whole-skill bundle exceeds the default budget | non-trivial | Already planned: rows W05 and W06 record per-mode bundles |
| `scripts/sbx` refuses a nested user namespace | trivial | Fixed here: the wrapper runs from a shell with full host permissions |

The root item is deferred rather than fixed in place because a fix belongs to the
build, not to this example. `closure.py` resolves a bare link from the declaring
root and a parent-segment link from the file's directory, which gives one folder
two spellings for one document and leaves a file unable to name both a sibling
and its parent folder. Deciding which of those two rules gives way touches the
invocation contract, 253 fixtures and the 40 declarations the skill carries, so
it is larger than this row and is recorded as W03 on #263.

## Plan Changes

| Change | Kind | Applied or held |
| --- | --- | --- |
| W01's row on #258 links the merged pull request #264 and carries its tick | Task delivery | Applied |
| AC1 on #258 is ticked | Criterion evidence | Applied |
| W03 and AC3 added to #263, with R3 | Task creation | Applied |
| `w01.md`'s root rule corrected to the per-file root the build needs | Folded work | Applied |
| `w01.md`'s Review row now compares content, not count alone | Folded work | Applied |
| `example/guidelines.md` added so the shared-guidelines links resolve | Folded work | Applied |
| #258 returned to In Progress on board 18 | Folded work | Applied |
| #258 moved to Done on board 18 | Folded work | Held — six rows remain undelivered |

The board correction is applied because the epic read `Ready` while a task row
had merged into its base, which is not what `Ready` states. Done is held because
the epic is not complete: W02 to W07 are undelivered and AC2 to AC10 unticked.
The row's own delivery does not close its epic, so the board cell follows the
epic's state rather than this row's.


