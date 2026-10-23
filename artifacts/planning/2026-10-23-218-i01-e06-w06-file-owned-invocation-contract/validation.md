# Invocation Contract Review

## Revision And Scope

Reviewed task commit: `977e4eb`, based on `373bc1f9e1052eb94cf35dfce7f3bce9e2da82d7`, on `i01/e06/w06-file-owned-invocation-contract`. The change is confined to `artifacts/planning/2026-10-17-prosiform-v1/design.md` and delivers epic #218 AC13. The accepted inputs are the file-owned invocation design, reconciliation, review and work item in `2026-10-23-218-derived-bundle-names`.

This is contract review evidence. Runtime schema, resolver, output and corpus verification belong to the subsequent delivery layers; no compiler conformance or current fixture pass is claimed.

## Invocation Contract

**Pass.** Read the complete changed contract against the accepted decisions and check the example and edge-case matrices below. Independent review identified and resolved deferred-output coordinates, ordering ties across roots, entry scheme/authority handling, verified no-follow bootstrap parents and fragment-only identity outside its own root.

| Area | Review observation |
| --- | --- |
| File command | `pf work-planner/modes/align-mode.md` resolves the file from invocation cwd. Its `root: ".."` resolves from `modes/`; `group: modes` and integer `group-depth: 2` are independent of root. |
| Schema | Top-level `prosiform` accepts only full root/group/group-depth keys; root and group are strings, depth is an integer 1–6. Group fields are paired; root is independent. Empty mapping and absent settings use documented defaults; malformed types and unknown keys fail. |
| Default roots | Both an entry and a linked source with absent roots use invocation cwd even when their containing directories differ from it. A linked source never inherits its parent's root. |
| Explicit roots | Relative roots resolve from their declaring file. Parent traversal can select a sibling library that does not contain the authoring file. Fragment-only links retain their captured-source identity. |
| Bounded capture | Entries and referrers use bounded no-follow bootstrap access before references are followed. Per-file and aggregate raw bytes, UTF-8, YAML nesting, original physical coordinates and immutable metadata apply to the captured bytes. |
| Shared sources | Each canonical path has one capture and effective root. Incoming accesses retain the referring source's confinement checks; repeated parents and cycles cannot alter the captured source's outgoing resolution. Distinct hard-linked paths remain distinct identities. |
| Determinism | Own-root-relative path sorts first, canonical absolute path breaks ties. Group conflicts follow that order. Ambiguous displayed file and full member names fail explicitly. |
| Deferred links | Deferred targets are validated without following their outgoing links; emitted targets use URI-escaped invocation-cwd-relative paths. Outside-root citations and resources remain unopened. |
| Diagnostics | Invalid settings, nonexistent roots, symlinks, confinement, missing targets, access failures and source changes have explicit stable codes. `E_SOURCE_ACCESS` classifies otherwise unclassified source/root filesystem access failures. Cwd-relative diagnostic file identities distinguish files under different roots. |
| Publication | Derived and explicit outputs share capture-overlap checks, candidate validation and atomic replacement. Full source/root consistency is checked before publication. Check mode publishes nothing; explicit stdout is `-o -`; informational responses use stdout. |
| Consumers | In-document CLI, pipeline, link classification, path identity, diagnostic catalogue, conformance cases and source-language handoff agree. Runtime consumers are assigned to their respective implementation layers, including installed-wheel and diagram-renderer commands. |

### Name And Selection Matrix

| Selection | Expected destination rule |
| --- | --- |
| `work-planner/modes/align-mode.md`, own root work-planner | `modes_align-mode.bundle.md` in cwd |
| Same source, resolved section prerequisites | `modes_align-mode__prerequisites.bundle.md` |
| `work-planner/SKILL.md`, own root work-planner | `SKILL.bundle.md` |
| `work-planner/artifacts/epic.markdown`, own root work-planner | `artifacts_epic.bundle.md` |
| `work-planner/guide.md`, declared sibling library root | `.._work-planner_guide.bundle.md`; flattened parent segments cannot traverse output directories |
| Equivalent `guide.md`, `./guide.md#` | One normalized whole-document entry |
| `-f work-planner/modes/align-mode.md '#prerequisites'` | Same source and section naming as the explicit file-plus-fragment reference |
| Two sections of one file, or whole file plus a section | Distinct entries require explicit `-o`, including check mode |
| Several explicit files with different valid roots | One combined bundle at the explicit destination; no root agreement requirement |
| Literal underscores, long names, case-insensitive filesystem | No uniqueness or shortening promise; atomic replacement and filesystem failure diagnostics apply |

## Document Hygiene

**Pass.** `git diff --check` passed before commit. A targeted search of the canonical contract found no obsolete `prosiform-group`, `pf -r`, required-global-root, default-stdout, numeric-depth-rejection or source-directory-link-resolution claims. All existing heading anchors remain available; the contract adds automatic naming, bounded bootstrap and conformance subsections.

The task branch contains one changed documentation file. Historical planning and runtime snapshots retain their recorded evidence. The task checkout contains no runtime CLI, fixture catalogue or invocation guide to update; their migration obligations are explicit in the normative contract. No code tests were run for this documentation-only unit.

## Delivery Boundary

The user explicitly confirmed the repository's **Auto-close issues with merged linked pull requests** setting is **Disabled** and authorized the merge. W06 has no standalone task issue and therefore requires no task Development link. The epic contract base was refreshed from `engineering` to `b8d0464` before merge.

PR [#226](https://github.com/m2ux/prosiform/pull/226) merged into `i01/e06/engineering` at `eabf709dcb7f21845abf0659b8c8ecf3f3ae70c4`, guarded by exact task head `977e4ebeaedca77d28ce4bf271768b8205e4ab28`. Fresh API reads before merge reported `mergeable: true`, `mergeable_state: clean` and the intended base. Exact-head check runs and commit statuses were empty; GitHub's aggregate status was `pending` for the empty status set. No CI pass is claimed. Target protection returned 404 (unprotected), active branch rules were empty, and reviews were empty. The passing Test Plan records the documentation review and hygiene checks above. Merge API readback confirmed the merged state and merge commit; the merged contract diff passed `git diff --check`.

The epic's W06 row links PR #226 and carries Done; AC13 is verified and ticked against this review. A fresh-body surgical update changed only those completion markers, and API readback matched the intended body exactly. The epic remains open.

Successor contract review [#227](https://github.com/m2ux/prosiform/pull/227) is draft from `i01/e06/engineering` into `engineering`, with its body populated from the actual W06 merge and citing task PR #226. API readback confirmed the complete body, branches and draft state. Runtime review #222 remains open and draft. Neither review was marked ready or merged.

The residual delivery limitation is the actual Development relation between review #227 and epic #218: this session has no tool that can read or edit that field completely. The review is created but its required Development link is unverified. Full issue-link synchronization remains incomplete; no body link or inferred empty relation substitutes for the field. No epic closure or board completion is claimed.
