# Validation — W05

> Delivery Record · Created 2026-10-25

## Overview

AC8's instrument is a search of each bundle for guideline content. Every in-root link to the example's own `guidelines.md` now carries the deferral marker on its text, and no mode bundle carries the document's H1 or any of its section headings. AC7's instrument is each bundle's byte count against 262,144; all ten are inside it.

The change is link text only. Ten in-root links across seven documents gain `¬ ` at the start of their text. No destination changes, no prose changes, and no out-of-root link is marked. Each command ran in `.worktrees/i02-e00-w05` at the branch head the pull request publishes; the "base" figures are `820b5cb6`, W04's merge.

## The ten bundles

Each mode is a whole-document entry, bundled at the default `-E 8` with `pf`. A bundle's guideline content is present when its text carries `# Guidelines` or a section heading the document writes. "Guideline links emitted" counts the guideline links the bundle still carries as text: the in-root ones are marked in their source and the bundle drops the marker on output, and the out-of-root ones stay as authored citations.

| Mode | Base bytes | Delivered bytes | Budget 262,144 | Guideline content | Guideline links emitted | In-root | Out-of-root |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `advance-mode` | 172,874 | 168,576 | ok | absent | 2 | 2 | 0 |
| `align-mode` | 129,667 | 129,667 | ok | absent | 0 | 0 | 0 |
| `deliver-mode` | 247,540 | 243,268 | ok | absent | 4 | 4 | 0 |
| `hoist-mode` | 86,680 | 82,369 | ok | absent | 1 | 1 | 0 |
| `plan-mode` | 208,204 | 203,906 | ok | absent | 2 | 2 | 0 |
| `propose-mode` | 23,034 | 23,034 | ok | absent | 0 | 0 | 0 |
| `revise-mode` | 44,948 | 3,482 | ok | absent | 8 | 4 | 4 |
| `standup-mode` | 169,009 | 164,698 | ok | absent | 1 | 1 | 0 |
| `sync-mode` | 158,933 | 154,622 | ok | absent | 1 | 1 | 0 |
| `understand-mode` | 44,020 | 44,020 | ok | absent | 0 | 0 | 0 |
| **Total** | **1,284,909** | **1,215,638** | | **10 of 10 absent** | **19** | **15** | **4** |

Every delivered figure matches the brief's expectation exactly. The largest is `deliver-mode` at 243,268 bytes, 92.8% of the budget; the base's largest was 247,540 at 94.4%. Three modes are byte-identical to the base because they carry no in-root guideline link: `align-mode`, `propose-mode` and `understand-mode`.

A mode can carry a marked link without writing one: `standup-mode` and `sync-mode` write none of their own and reach the guidance through `protocols/epic-integration.md`, which they include. `advance-mode`, `deliver-mode` and `plan-mode` carry one or two of their own and also include that protocol. The ten source documents hold ten marked links; the ten bundles emit fifteen in-root occurrences, because a document reached through more than one path appears more than once. The four out-of-root occurrences are all in `revise-mode`'s bundle and all stay as authored citations.

## Guideline content absent from every bundle

The search looks for the document's H1 and for the opening line each section writes — "Read this before adding or changing a mode", and the same for a protocol, an artifact and a reference. All ten bundles return zero for every mark. For comparison, the base returned the H1 and the `### Modes` opening in seven bundles, and the other three openings in `revise-mode` alone.

| Mode | `# Guidelines` base → delivered | `### Modes` opening, base → delivered | Other section openings, base → delivered |
| --- | --- | --- | --- |
| `advance-mode` | 1 → 0 | 1 → 0 | 0 → 0 |
| `align-mode` | 0 → 0 | 0 → 0 | 0 → 0 |
| `deliver-mode` | 1 → 0 | 1 → 0 | 0 → 0 |
| `hoist-mode` | 1 → 0 | 1 → 0 | 0 → 0 |
| `plan-mode` | 1 → 0 | 1 → 0 | 0 → 0 |
| `propose-mode` | 0 → 0 | 0 → 0 | 0 → 0 |
| `revise-mode` | 1 → 0 | 1 → 0 | 3 → 0 |
| `standup-mode` | 1 → 0 | 1 → 0 | 0 → 0 |
| `sync-mode` | 1 → 0 | 1 → 0 | 0 → 0 |
| `understand-mode` | 0 → 0 | 0 → 0 | 0 → 0 |

Six of the base's seven bundles carried 4,323 bytes each of the document — its H1 and the `### Modes` section the `#modes` anchor selects. `revise-mode`'s carried 23,797 bytes, the document's text from its H1 through `## Changes`. The base's total guidance across the seven was 49,735 bytes. The delivered bundles carry none of it.

## Source-side link inventory

Eighteen links in `example/work-planner` name a `guidelines.md`. Ten are in-root and all ten carry the marker; eight are out-of-root and none is marked. Resolution is against the declaring file's `prosiform.root`, as W04 set it, so a bare `guidelines.md` resolves from the example directory and one carrying `..` leaves it. Three further mentions in `example/guidelines.md` are prose naming that file and carry no link to the example's document.

The brief's list of seven files names `modes/standup-mode.md` and `modes/sync-mode.md` and omits `protocols/epic-integration.md`. The count is right and the set is not: `standup-mode.md` and `sync-mode.md` write no guideline link at all, and `protocols/epic-integration.md` writes one, which their bundles reach because both include it. The set measured here is the seven documents the links actually sit in.

| Document | Line | Link text | Destination | Resolves to | Root | Marked |
| --- | --- | --- | --- | --- | --- | --- |
| `SKILL.md` | 76 | `¬ interview rules` | `guidelines.md#modes` | `example/work-planner/guidelines.md` | in | yes |
| `modes/advance-mode.md` | 40 | `¬ guidelines` | `guidelines.md#modes` | `example/work-planner/guidelines.md` | in | yes |
| `modes/deliver-mode.md` | 49 | `¬ Interview` | `guidelines.md#modes` | `example/work-planner/guidelines.md` | in | yes |
| `modes/hoist-mode.md` | 26 | `¬ Interview` | `guidelines.md#modes` | `example/work-planner/guidelines.md` | in | yes |
| `modes/plan-mode.md` | 46 | `¬ Interview` | `guidelines.md#modes` | `example/work-planner/guidelines.md` | in | yes |
| `modes/revise-mode.md` | 14 | `¬ skill guidelines` | `guidelines.md` | `example/work-planner/guidelines.md` | in | yes |
| `modes/revise-mode.md` | 16 | `¬ Interview` | `guidelines.md#modes` | `example/work-planner/guidelines.md` | in | yes |
| `modes/revise-mode.md` | 27 | `¬ skill guidelines` | `guidelines.md` | `example/work-planner/guidelines.md` | in | yes |
| `modes/revise-mode.md` | 39 | `¬ representative scenarios` | `guidelines.md#progressive-disclosure` | `example/work-planner/guidelines.md` | in | yes |
| `protocols/epic-integration.md` | 19 | `¬ Interview` | `guidelines.md#modes` | `example/work-planner/guidelines.md` | in | yes |
| `guidelines.md` | 7 | `shared skill guidelines` | `../guidelines.md` | `example/guidelines.md` | out | no |
| `guidelines.md` | 231 | `progressive disclosure` | `../guidelines.md#progressive-disclosure` | `example/guidelines.md` | out | no |
| `guidelines.md` | 231 | `disclosure verification` | `../guidelines.md#disclosure-verification` | `example/guidelines.md` | out | no |
| `guidelines.md` | 244 | `change rules` | `../guidelines.md#changes` | `example/guidelines.md` | out | no |
| `modes/revise-mode.md` | 14 | `shared skill guidelines` | `../../guidelines.md` | `skills/guidelines.md` | out | no |
| `modes/revise-mode.md` | 27 | `shared skill guidelines` | `../../guidelines.md` | `skills/guidelines.md` | out | no |
| `modes/revise-mode.md` | 33 | `Progressive disclosure` | `../../guidelines.md#progressive-disclosure` | `skills/guidelines.md` | out | no |
| `modes/revise-mode.md` | 39 | `disclosure verification` | `../../guidelines.md#disclosure-verification` | `skills/guidelines.md` | out | no |

Ten in-root links in seven documents: `SKILL.md` 1, `protocols/epic-integration.md` 1, `modes/advance-mode.md` 1, `modes/deliver-mode.md` 1, `modes/hoist-mode.md` 1, `modes/plan-mode.md` 1 and `modes/revise-mode.md` 4. `modes/standup-mode.md` and `modes/sync-mode.md` write none of their own; their bundles reach the guidance through `protocols/epic-integration.md`.

The eight out-of-root links keep their text as authored. Four name the shared guidelines from `guidelines.md` at `../guidelines.md` and four name the skill guidelines from `modes/revise-mode.md` at `../../guidelines.md`. They are citations to documents outside the example root and already stay links, so the marker is neither needed nor applied.

## Destinations still resolve

A deferred link's destination must exist. `make links --online` resolves all 18 in source, and each anchor names a heading the destination document writes: `#modes` its `## Modes` section, `#progressive-disclosure` its `## Progressive Disclosure` section, `#disclosure-verification` and `#changes` the shared guidelines' own sections. No destination was repointed.

## Only link text changed

The branch's diff is ten lines removed and ten added across seven files. Every added line is its removed counterpart with one `¬ ` inserted at the start of the link text. Every destination is byte-identical between the pair. No heading, sentence or table cell moves, so each document's prose is what the base carried.

## The finding: `revise-mode` collapses to its Procedure

`revise-mode`'s bundle falls 44,948 → 3,482 bytes, a loss of 41,466. Its four in-root links all name guidance and its only other links are same-file anchors — `[Outcomes](#outcomes)`, `[Run Tests](#run-tests)` and `[Check Skill Files](#check-skill-files)` — so deferring the guidance removes the mode's only cross-file content. The 3,482 bytes are its Procedure section and nothing else.

The loss is larger than the 23,797 bytes of guidance it carried, because the guidance document's own links were what carried two more documents in. `guidelines.md` links `[Conventions](SKILL.md#conventions)`, `[Issue Body](artifacts/issue-body.md#fields)`, `[Pull Request Body](artifacts/pull-request-body.md#fields)`, `[Repository Graph](artifacts/repository-graph.md)` and the shared guidelines. The base's revise bundle therefore also held `# SKILL` at 14,832 bytes and `# References` at 2,866 bytes, both reached through the guidance. Deferring the guidelines link removes that whole chain: 3,453 for the mode's own Procedure, 14,832, 23,797 and 2,866 make the base's 44,948.

That is the marker working as designed and a design signal about the mode: a mode whose only cross-file references are guidance has nothing else to bundle. It is recorded as a finding; no artifact or protocol link was added to `revise-mode` in this row. The row's debt entry carries the criterion a later fix must meet.

## Checks

| Command | Result | Output |
| --- | --- | --- |
| `make links --online` | pass | `link check: every reference in 101 document(s) resolved` |
| `make layout` | pass | `layout check: 3 tree(s) present` |
| `make tables` | pass | `table check: 16 command(s) and 8 declaration(s), each declared by the project and named by a table` |
| `make vocabulary` | pass | `vocabulary check: 38 contract term(s)` marked and defined, carried across 24 source(s) |

`make check` was not run. The brief directs these four targets and forbids `make check`.

## Debt This Row Finds

| Item | Classification | Disposition |
| --- | --- | --- |
| `revise-mode`'s only cross-file references are guidance, so its bundle is its Procedure alone once they are deferred | non-trivial | Raised on #263; its criterion states that the mode carries the artifacts and protocols its work actually calls |
| A deferred link's destination survives in the emitted bundle as text while its content does not, so a bundle can name a document it does not contain | trivial | Recorded here; it is the marker working as designed, and the destination still resolves in source |

One row on #263. No row for the trivial item.

## Plan Changes

| Change | Kind | Applied or held |
| --- | --- | --- |
| W05's row on #258 links the merged pull request [#268](https://github.com/m2ux/prosiform/pull/268) | Task delivery | Applied |
| AC7 and AC8 on #258 ticked | Criterion evidence | Applied |
| `README.md`'s "23,900 bytes whole in seven bundles" corrected: six carry 4,323 bytes and `revise-mode` carries 23,797 | Folded work | Applied |
| `w05.md`'s "23,900 of those bytes are guidance" and "carry its text whole" corrected the same way | Folded work | Applied |
| `w05.md`'s "five in-root links" in `revise-mode` corrected to four | Folded work | Applied |
| The seven-file set named: `standup-mode.md` and `sync-mode.md` write none, `protocols/epic-integration.md` does | Folded work | Applied |
| #258 stays In Progress on board 18 | Board state | Applied |
| #258 moved to Done on board 18 | Folded work | Held — two rows remain undelivered |
| A row on #263 for the `revise-mode` reference gap: W05, "A mode whose only references are guidance carries its own artifacts", with AC5 stating the criterion its fix makes true | Task creation | Applied |

## Merge

| Fact | Value |
| --- | --- |
| Pull request | [#268](https://github.com/m2ux/prosiform/pull/268) |
| Merge commit | `3a623c9cb721fbf9012726621cce91d49804e0e6` |
| Method | merge commit |
| Epic base after | `3a623c9c`, two rows undelivered |
| Check | `Checks` completed `pass` in 1m15s |
