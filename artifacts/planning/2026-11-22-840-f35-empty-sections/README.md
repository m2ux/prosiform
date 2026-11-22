# F35: Empty Generated Wrappers

## Retrospective Scope

[Issue #840](https://github.com/m2ux/prosiform/issues/840) records the implemented pruning correction. The selected boundary removes empty, unreferenced generated group, overview and preamble wrappers. Authored headings, referenced identities, meaningful descendants, code examples, containers and dispatch/composition structure remain.

The standalone delivering branch is f35-empty-sections at 9232c012dd2ee3a893a7066812bc55a3577d25a2, based on main at bf42862ef3757c8f62b0b8522481d27c4518dd0d. It contains the F35 delta alone. F34 is separately registered under issue #839 and is not part of this PR's code diff. The combined local build c956908d9 includes both corrections for consumer validation.

## Validation

[Full make check](make-check.txt) passes at the exact standalone revision:

- 2,305 compiler tests, including 15 focused pruning regressions.
- 1,154 harness tests and all 707 corpus fixtures.
- Lint, formatting, strict typing, lock consistency, wheel/install smoke, layout, tables, links, vocabulary, invocation, conformance and independence.

Focused tests cover empty generated wrapper removal and warning locations; meaningful bodies, containers and code examples; authored empty anchors; inline, reference-style and diagram whole-document links to grouped member identities; retained dispatch positions; and protected ancestors. Each construction pass protects its own heading identities. Existing dispatch and per-copy composition regressions pass.

One corpus expectation omits an empty generated Beta heading and records W_EMPTY_SECTION. Its source documents retain their bytes. The canonical contract, shipped documentation and warning catalogue describe the same narrow boundary. This replaces the broad prototype that could remove valid document addresses; exploratory source-padding edits are excluded.

## Delivery State

The operator authorizes retrospective draft PR publication. Implementation and checks are complete; agent review and merge remain open. Draft status keeps the hotfix In Progress. The saved [hotfix body](proposed-hotfix.md) reflects the selected narrow scope; criteria remain unticked pending delivery verification.

[Draft PR #842](https://github.com/m2ux/prosiform/pull/842) targets main and is linked to #840 through Development. CI passes at the recorded head; the hotfix remains In Progress. The [publication receipt](publication.json) records both directions of the link and the operator-confirmed disabled auto-close setting.

## Current Main Integration

F34 merges while F35 is open. Merge commit 4737171c6db91e4c9735fcfcbb1f775e6d39382c incorporates main at e2dde5e569800e5584797bb194bb989f8fb2843b and keeps the F35 canonical contract pin in README and references. The PR diff against main remains scoped to F35. [Fresh full make check](current-main-make-check.txt) passes: 2,318 compiler tests, 1,155 harness tests and all 708 corpus fixtures, plus the remaining guards and smoke checks. The [current CI readback](current-main-ci.json) confirms passing checks, a mergeable branch and draft state at this head. The combined consumer-evaluation checkout remains at c956908d9 throughout its native cohort.

## Side-Effect Review

[The implementation review](pruning-review.md) finds no correctness regression within the checked boundary. All 28 focused tests and six additional probes pass. It records warning-stream compatibility and historical external-anchor changes as the remaining observable integration effects.
