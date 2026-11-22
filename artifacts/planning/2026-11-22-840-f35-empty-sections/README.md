# F35: Empty Generated Wrappers

## Retrospective Scope

[Issue #840](https://github.com/m2ux/prosiform/issues/840) records the implemented pruning correction. The selected boundary removes empty, unreferenced generated group, overview and preamble wrappers. Authored headings, referenced identities, meaningful descendants, code examples, containers and dispatch/composition structure remain.

The delivering branch is f35-empty-sections at 5c1917343080bb0f8328ac119571049b41abee0d, based on main at a38b065114f3f4d7f5d61b9d5ae52d393da3ec5f. It contains the F35 delta alone. F34 is separately registered under issue #839 and is not part of this PR's code diff. The combined local build c956908d9 includes both corrections for consumer validation.

## Validation

[Full make check](make-check.txt) passes at the exact standalone revision:

- 2,305 compiler tests, including 15 focused pruning regressions.
- 1,154 harness tests and all 707 corpus fixtures.
- Lint, formatting, strict typing, lock consistency, wheel/install smoke, layout, tables, links, vocabulary, invocation, conformance and independence.

Focused tests cover empty generated wrapper removal and warning locations; meaningful bodies, containers and code examples; authored empty anchors; inline, reference-style and diagram whole-document links to grouped member identities; retained dispatch positions; and protected ancestors. Each construction pass protects its own heading identities. Existing dispatch and per-copy composition regressions pass.

One corpus expectation omits an empty generated Beta heading and records W_EMPTY_SECTION. Its source documents retain their bytes. The canonical contract, shipped documentation and warning catalogue describe the same narrow boundary. This replaces the broad prototype that could remove valid document addresses; exploratory source-padding edits are excluded.

## Delivery State

[PR #842](https://github.com/m2ux/prosiform/pull/842) merges into main as dde69b04669940993b79529381df240cf068b26a and is linked to #840 through Development. The [publication receipt](publication.json) records both directions of the link and the operator-confirmed disabled auto-close setting. The saved [hotfix body](proposed-hotfix.md) reflects the selected narrow scope.

Make check passes at the merged revision, which verifies AC1 to AC8. #840 carries every criterion ticked and the delivery comment, is closed as completed, and stands Done on board 18.

## Current Main Integration

F34 and the comment cleanup (#843) merge while F35 is open. The branch is rebased onto main at a38b065114f3f4d7f5d61b9d5ae52d393da3ec5f as a1d6a6039, which keeps the F35 canonical contract pin and main's F34 dispatch-label sentence in references. 5c1917343 names each pruned heading's generated kind in W_EMPTY_SECTION. The PR diff against main remains scoped to F35. [Fresh full make check](current-main-make-check.txt) passes at 5c1917343: 2,318 compiler tests, 1,155 harness tests and all corpus fixtures, plus the remaining guards and smoke checks. The [current CI readback](current-main-ci.json) records the checks, mergeability and draft state at this head. The combined consumer-evaluation checkout remains at c956908d9 throughout its native cohort.

## Side-Effect Review

[The implementation review](pruning-review.md) finds no correctness regression within the checked boundary. All 28 focused tests and six additional probes pass. It records warning-stream compatibility and historical external-anchor changes as the remaining observable integration effects.
