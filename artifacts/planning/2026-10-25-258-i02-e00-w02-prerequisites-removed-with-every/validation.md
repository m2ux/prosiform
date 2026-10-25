# Validation — W02

> Delivery Record · Created 2026-10-25

## Overview

AC2's instrument is a search across the tree. AC3's is a link comparison before
and after the migration, measured twice: on the file text, and on the bundle the
build compiles from each file. Both pass. The removal also shortens every mode's
bundle, and one mode crosses the default hop budget as a result; that is recorded
below as the row's finding, not as a failed criterion.

Every command ran in `.worktrees/i02-e00-w02` at the branch head the pull request
publishes, from `example/work-planner` where the invocation is relative to that
directory.

## Before — the Target Set

The inventory records, for each of the 35 files carrying `## Prerequisites`, the
heading, the opening line and every link target in its list.

| Measure | Value |
| --- | --- |
| Files carrying the heading | 35 |
| Markdown files under `example/work-planner` | 49 |
| Bulleted link lines across the 35 lists | 180 |
| Distinct destinations | 65 |
| Opening line, all 35 | `Read these files first.` |
| Targets carrying a fragment | 0 |

| Folder | Files |
| --- | --- |
| `artifacts/` | 19 |
| `modes/` | 10 |
| `protocols/` | 6 |

The 14 files without the heading are `SKILL.md`, `guidelines.md` and 12
`artifacts/` files.

## After — AC2

The instrument is the command the brief names.

```text
grep -rl '^## Prerequisites' example/work-planner --include=*.md
```

| Outcome | Value |
| --- | --- |
| Exit status | `1` |
| Files matching | 0 |

`Prerequisites` survives as a word in the tree, and every remaining occurrence is
a different subject: the `Check Epic Prerequisites` operation in `artifacts/epic.md`
and the three modes that call it, and the section-shape rules in `guidelines.md`
and `SKILL.md` that state what a mode's own Prerequisites section holds. Those are
prose about the skill, not sections of the example. Removing them is not this
row's work: `guidelines.md` and `SKILL.md` are the parts of the example whose
prose W07 owns.

## After — AC3

`closure.py` states two resolution rules that differ. A link carrying a parent
segment resolves from the declaring file's own directory, with the root bounding
the result. A link carrying no parent segment resolves from the declaring file's
root. A link whose target lands outside that root stays authored and compiles
nothing, so it was never an edge the bundle followed from that file.

Of the 180 target occurrences the 35 lists named, 108 compiled under those rules
and 72 were citations. The comparison is made on the 108, because those are the
edges a bundle of the file carried.

| Measure | Value |
| --- | --- |
| Targets the lists named | 180 |
| List links that compiled | 108 |
| List links that were citations | 72 |
| Targets the body still names | 180 of 180 |
| Targets the body reaches by a compiling link | 108 of 108 |
| Targets reached from Procedure, Operations or Fields | 108 of 108 |
| Edges lost by the removal | 0 |
| Files that needed a link placed | 0 |

Every one of the 108 edges survives, and every one survives inside the file's own
Procedure, Operations or Fields rather than in a trailing section. The 72
citations remain citations, because a citation names a document outside the
declaring file's root and no body link can make one compile.

### The same comparison on the bundle

Text is one reading. The bundle is the stronger one, because it is what a reader
of the file receives. Each of the 49 files was opened as an entry and the build's
own `traverse` read for every document and section target the run reached, before
the removal and after it.

| Measure | Value |
| --- | --- |
| Named targets measured | 180 |
| Named targets that leave their own file's bundle | 0 |

No file's own bundle loses a document its list named.

## Bundle Output

Each mode is a whole-document entry. A bundle's authored `.md` links are the
destinations it carried as written rather than compiling, which is W04's subject;
the count below is its starting figure.

| Mode | Bytes | Authored links | Authored `.md` links | Prerequisites headings |
| --- | --- | --- | --- | --- |
| `advance-mode` | 63450 | 80 | 78 | 0 |
| `align-mode` | 129795 | 3 | 3 | 0 |
| `deliver-mode` | 162144 | 145 | 143 | 0 |
| `hoist-mode` | 83911 | 3 | 3 | 0 |
| `plan-mode` | 88525 | 77 | 75 | 0 |
| `propose-mode` | 23084 | 0 | 0 | 0 |
| `revise-mode` | 42098 | 9 | 9 | 0 |
| `standup-mode` | 61472 | 67 | 65 | 0 |
| `sync-mode` | 57490 | 54 | 52 | 0 |
| `understand-mode` | 44041 | 2 | 0 | 0 |

`deliver-mode` is bundled at `-E 9`. At the default `-E 8` it is refused with
`E_RESOURCE_LIMIT`, and the finding below states why.

The whole example through `SKILL.md` bundles to 259958 bytes at `-O 1048576`,
against 302531 before the copy's removal and 299068 when the epic planned it. It
carries no `Prerequisites` heading; the 17 occurrences of the word in that bundle
are the same prose the tree search found.

## Checks

| Command | Result | Notes |
| --- | --- | --- |
| `make links` | pass | `--online`, 101 documents, every reference resolved |
| `make layout` | pass | `docs/` 10, `fixtures/` 964, `src/` 39 |
| `make tables` | pass | 16 commands, 8 declarations |
| `make vocabulary` | pass | 38 terms across 24 sources |
| `make test` | pass | 1725 passed |
| `make check` | not run | Stops at the first failing target and runs the corpus |
| `make corpus` | not run | Needs `PROSIFORM_BUILD`; binding the example is W06's work |
| `make invocation`, `make conformance`, `make independence` | not run | Each needs a configured `PROSIFORM_BUILD` |
| `make lint`, `make format-check`, `make typecheck` | not run | No Python source in this row's diff |
| `make smoke` | not run | Builds and installs a wheel this row does not change |

## The Finding

Removing the lists shortens every mode's bundle, and the mechanism is a difference
in selection rather than a lost document.

A list link names a document whole, so its selection is the entire file. A body
link almost always names one operation of the same document, so its selection is
that operation's subtree. Of the 108 compiling list links, 19 were matched by a
body link naming the same document whole and 89 were matched only by section:

| Measure | Value |
| --- | --- |
| Compiled list links matched by a whole-document body link | 19 |
| Compiled list links matched only by section body links | 89 |
| Compiled list links with no body link to the document | 0 |

So no file loses an edge to a document. What leaves the bundles is the content a
whole-document selection carried and the operation selections do not.

| Mode | Bytes before | Bytes after | Documents before | Documents after |
| --- | --- | --- | --- | --- |
| `advance-mode` | 113316 | 63450 | 12 | 11 |
| `align-mode` | 174860 | 129795 | 22 | 21 |
| `deliver-mode` | 234500 | 162144 | 26 | 24 |
| `hoist-mode` | 181071 | 83911 | 19 | 14 |
| `plan-mode` | 135139 | 88525 | 16 | 16 |
| `propose-mode` | 48009 | 23084 | 6 | 6 |
| `revise-mode` | 42220 | 42098 | 6 | 6 |
| `standup-mode` | 111305 | 61472 | 12 | 11 |
| `sync-mode` | 106993 | 57490 | 11 | 10 |
| `understand-mode` | 92732 | 44041 | 10 | 9 |

`deliver-mode` crossed the default hop budget because the route to
`artifacts/issue.md#set-completed-state` grew from eight hops to nine. The list
was the shortcut that had kept it at eight, so removing it lengthened the path the
operation is reached by, which now runs
`modes/deliver-mode.md` → `modes/hoist-mode.md` →
`artifacts/issue.md#read-repository-issues` → `artifacts/issue.md#set-completed-state`.

Neither of these is AC3's failure. AC3 requires that no document a list named
leaves the body of the file that wrote the list, and no document does. What the
removal changes is the closure of files that reached those documents through the
list, and the hop depth of one operation. Both follow from the lists having been
real edges, and both are properties of the tree the epic asks for rather than
defects in the removal.

`deliver-mode` at the default budget is what W05 and W06 need to know: a per-mode
bundle of it needs `-E 9`, or the source needs an edge restored. Restoring one is
not this row's work, because the row's rule places a link only where a body would
otherwise lose a document, and no body does.

## Debt This Row Finds

| Item | Classification | Disposition |
| --- | --- | --- |
| `deliver-mode` crosses the default `-E 8` at nine hops | non-trivial | Deferred to #263 |
| 108 authored `.md` links survive in the mode bundles | non-trivial | Already planned: W04 owns the rewrite |

The hop item is deferred rather than fixed here because the choice is between
raising the budget for the example and restoring an edge the example's own
guidelines would not ask for, and that decision belongs to the row that states
what a per-mode bundle is. Its fix makes a bundle of every mode compile at the
default hop budget.

## Plan Changes

| Change | Kind | Applied or held |
| --- | --- | --- |
| W02's row on #258 links the merged pull request | Task delivery | Applied |
| AC2 and AC3 on #258 ticked | Criterion evidence | Applied |
| The hop-depth item deferred to #263 | Task creation | Applied |
| #258 moved to Done on board 18 | Folded work | Held — four rows remain undelivered |
