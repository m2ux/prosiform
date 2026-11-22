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
