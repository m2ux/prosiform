# Validation — W04

> Delivery Record · Created 2026-10-25

## Overview

AC6's instrument is a bundle of each mode, counting authored in-root links. Every one of the ten modes compiles at the default `-E 8`, every bundle is inside the 262,144-byte budget, and no bundle leaves an in-root link authored.

The change is two things only: each file's declared root now resolves to `example/work-planner`, and each in-root link destination is written as a path from that directory. Nothing else moved. Each command ran in `.worktrees/i02-e00-w04` at the branch head the pull request publishes; the "before" figures are the merged base `1e2dc068` and the "after" figures are the merged branch.

## The ten bundles

Each mode is a whole-document entry, bundled at the default `-E 8`. An authored link is read from the bundle's text with fenced code blocks set aside, since a template's spelling inside a fence is not a reference the compiler follows. A destination is in-root when its path carries no parent segment and lands on a Markdown document inside `example/work-planner`; a destination carrying `..` leaves the example and is a citation.

| Mode | Base bytes | Fixed bytes | In-root links left authored, base | In-root links left authored, fixed | Budget |
| --- | --- | --- | --- | --- | --- |
| `advance-mode` | 63,429 | 172,874 | 78 | 0 | ok |
| `align-mode` | 129,745 | 129,667 | 3 | 0 | ok |
| `deliver-mode` | refused at `-E 8` | 247,540 | — | 0 | ok |
| `hoist-mode` | 83,889 | 86,680 | 3 | 0 | ok |
| `plan-mode` | 88,442 | 208,204 | 75 | 0 | ok |
| `propose-mode` | 23,034 | 23,034 | 0 | 0 | ok |
| `revise-mode` | 42,097 | 44,948 | 9 | 0 | ok |
| `standup-mode` | 61,451 | 169,009 | 65 | 0 | ok |
| `sync-mode` | 57,469 | 158,933 | 52 | 0 | ok |
| `understand-mode` | 44,020 | 44,020 | 0 | 0 | ok |
| **Total** | **593,576** | **1,284,909** | **285** | **0** | |

The base column reproduces the brief's measurement exactly: 78, 75, 65, 52, 9, 3, 3, 0 and 0 authored in-root links, 285 in all. `deliver-mode` is refused at the default budget on the base with `E_RESOURCE_LIMIT` at nine link hops. After the change every mode compiles at `-E 8`, and the ten bundles total 1,284,909 bytes against a budget of 262,144 each.

The bundles grow because they carry the artifacts their links name. `advance-mode` goes from 63,429 bytes to 172,874. `align-mode` shrinks by 78 bytes, because its links already resolved inside its own folder on the base and its destinations are now shorter. `propose-mode` and `understand-mode` are unchanged in size: their in-root links already landed inside their declared root and their destination spellings were already correct.

## In-root links left authored

Zero in every mode. The base's 285 authored in-root links named content the bundle did not carry. After the change each destination resolves from the example directory and its content is included, so no in-root link survives as authored text.

## Out-of-root links left as authored

Eight occurrences remain, and all name a document outside the example. They are citations and stay as written. None is deferred with the negation mark; that instrument is AC8's and belongs to W05.

| Document | Destination | Resolves to |
| --- | --- | --- |
| `guidelines.md` | `../guidelines.md` | `example/guidelines.md` |
| `guidelines.md` | `../guidelines.md#progressive-disclosure` | `example/guidelines.md` |
| `guidelines.md` | `../guidelines.md#disclosure-verification` | `example/guidelines.md` |
| `guidelines.md` | `../guidelines.md#changes` | `example/guidelines.md` |
| `modes/revise-mode.md` | `../../guidelines.md` (2 occurrences) | `skills/guidelines.md` |
| `modes/revise-mode.md` | `../../guidelines.md#progressive-disclosure` | `skills/guidelines.md` |
| `modes/revise-mode.md` | `../../guidelines.md#disclosure-verification` | `skills/guidelines.md` |

## Proof of inclusion

The base's `advance-mode` bundle carries nine of the example's 49 documents and leaves 78 in-root links authored. Its Procedure runs `[Select Project Board](../artifacts/board.md#select-project-board)` and `board.md`'s text is nowhere in the bundle. The fixed bundle carries `board.md` by its text at line 173:

```text
### Board

#### *Select* Project Board

The theme or proposals board the request names.

**Inputs:** Board owner and either a theme name or the proposals-board selection.
```

The base bundle contains no occurrence of "The theme or proposals board the request names." and two authored `../artifacts/board.md` links; the fixed bundle contains the text and no authored `../artifacts/board.md` link. That is the criterion: the link disappeared because its target arrived.

The same holds for the seven modes whose bundles grew. `plan-mode` gains 119,762 bytes, `standup-mode` 107,558, `sync-mode` 101,464 and `deliver-mode` compiles where it was refused. Each gain is artifact text the base's links named and the base's bundle left out.

## Declarations

| Declaration | Files | Directory it resolves to |
| --- | --- | --- |
| `root: "."` | 2 | `example/work-planner` |
| `root: ".."` | 47 | `example/work-planner` |
| **Total** | **49** | |

Two spellings name one directory. The split is by depth: the top-level files `SKILL.md` and `guidelines.md` declare `"."`, and every file in `artifacts/`, `modes/`, `protocols/` and `references/` declares `".."`. The declaration resolves from the declaring file's folder, so one directory needs two spellings — #263's W03 owns that limitation and this row works within it.

## Checks

| Command | Result | Notes |
| --- | --- | --- |
| `make links` | pass | `--online`; every reference in 101 documents resolved |
| `make layout` | pass | 3 trees present: `docs/` 10, `fixtures/` 964, `src/` 39 |
| `make tables` | not run | The brief directs `make links` and `make layout` only |
| `make vocabulary` | not run | The brief directs `make links` and `make layout` only |
| `make check` | not run | The brief directs the targets individually |

## Debt This Row Finds

| Item | Classification | Disposition |
| --- | --- | --- |
| A declaration resolves from the declaring file's folder, so one root for a tree needs two spellings | non-trivial | Deferred to #263 as its W03, which owns it and whose criterion states what its fix makes true |
| A link leaving the declared root is silently a citation, so a wrong root produces a smaller bundle at exit zero rather than an error | trivial | Recorded here; it is the governing rule working as designed, and the row's own measurement catches the symptom |
| `deliver-mode`'s hop refusal disappears without raising `-E` | trivial | Recorded here; the included artifacts shorten the chains that ran through mode-to-mode links |

No new row is raised. The one non-trivial item already has its row on #263.

## Plan Changes

| Change | Kind | Applied or held |
| --- | --- | --- |
| W04's row on #258 links the merged pull request [#267](https://github.com/m2ux/prosiform/pull/267) | Task delivery | Applied |
| AC6 on #258 ticked | Criterion evidence | Applied |
| `README.md`'s measured-result figures replaced with the delivered ones | Folded work | Applied |
| `w04.md`'s Proposal states the two spellings and the out-of-root set | Folded work | Applied |
| #258 stays In Progress on board 18 | Board state | Applied |
| #258 moved to Done on board 18 | Folded work | Held — three rows remain undelivered |
| A row on #263 for the two-spelling constraint | Task creation | Not needed — #263's W03 already owns it with a criterion |

## Merge

| Fact | Value |
| --- | --- |
| Pull request | [#267](https://github.com/m2ux/prosiform/pull/267) |
| Merge commit | `820b5cb681de57ef8e1473f92497cb125b5e2a3c` |
| Method | merge commit |
| Epic base after | `820b5cb6`, three rows undelivered |
| Check | `Checks` completed `pass` in 1m18s |
