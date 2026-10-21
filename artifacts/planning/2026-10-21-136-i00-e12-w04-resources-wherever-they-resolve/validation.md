# Validation

The checks these two rows ran, the revision they ran against, and what each observed.

## Revision

`3e2f6a8` on `i00/e12/w04-resources-wherever-they-resolve`, rebased onto `i00/e12/main` at `f8b67f0`, which carries the W01, W06 and W03 merges. Every result below was taken after that rebase, on the full `make check` sequence with `PROSIFORM_BUILD` naming this worktree's build.

The epic base moved twice while this unit was in flight. The second rebase, onto W03's merge, conflicted in `src/tests/test_cli.py` where W03 added two `E_TARGET_NOT_FOUND` tests immediately above a test this unit renamed. Both sides were kept: W03's two tests stand, and the renamed test keeps its new name. The suites below were rerun in full after that resolution.

The base was red before the work started: `checks/tests/test_catalogue.py` failed its `error` parameter, naming `E_SELF_REFERENCE` and `E_MARKED_RESOURCE` as codes the schema catalogue held and the design declared nowhere. That failure was the work these rows carried, not a defect of the base, and it is the first result recorded below.

## Catalogue

`make harness`, the whole of `checks/tests`, which holds each schema catalogue to the codes the design declares under its prefix.

**376 passed, 0 failed.** `test_a_catalogue_is_the_codes_the_design_declares[error-E_]` passes, where on the base it failed with both retired codes listed as extra items in the schema's set. The warning catalogue was green throughout and stayed so: `W_RESOURCE_PORTABILITY` is unchanged by this work.

The check reads `design.md` from `origin/engineering` rather than from the worktree, so the result is the schema in this branch held against the published design — which is the pairing that was broken.

## Resources

`fixtures/resource` and `fixtures/traversal`, through `make corpus`, and the `cli` tests in `src/tests/test_cli.py`.

**Corpus: 204 fixtures, 202 pass, 0 fail, 2 awaited, 0 unexpected pass.** The two awaited fixtures are `I00:E11:W10` and `I00:E11:W14`, neither touched here.

Observed for AC6:

- `resource/a-marked-resource-is-emitted-as-authored` — a marked link and a marked image, both naming a file that exists under the allowed source root, are published with every byte their author wrote, the mark included. The run exits 0 and warns once with `W_RESOURCE_PORTABILITY`. On the base each of these failed the run with `E_MARKED_RESOURCE`.
- `resource/an-image-naming-a-document-under-the-root` — an image naming `rules.md` under the root is published as authored, and `rules.md` is not opened or carried. The run exits 0.
- `traversal/a-relative-resource-warns` and `traversal/resources-are-not-dependencies` — unchanged, and still green, so a resource outside the root and one carrying a scheme behave as they did.

The unit tests observing the same rule are `test_a_marked_resource_is_emitted_with_its_mark`, `test_a_marked_image_is_emitted_with_its_mark`, `test_a_marked_reference_carrying_a_scheme_is_emitted_as_authored` and `test_an_image_naming_a_markdown_document_carries_no_document`.

### A limitation this row recorded rather than fixed

`W_RESOURCE_PORTABILITY` does not fire for an image whose destination names a Markdown document. `cli.resource()` reads the destination alone and answers "not a resource" for any `.md` path, so the image's own syntax — which the design says makes it a resource whatever it points at — is not reachable at the point the warning is decided.

AC6 is about what the bundle emits, and the bundle emits the image as authored, so this does not block the criterion. `resource/an-image-naming-a-document-under-the-root` therefore declares the run's present diagnostics, and the gap is deferred as an issue of its own rather than widened into this unit.

## Self and ancestor references

`fixtures/self-reference`, `fixtures/ownership` and `fixtures/validation-scope`, through `make corpus`, and the `cli` tests in `src/tests/test_cli.py`.

Observed for AC7:

- `self-reference/a-link-to-the-same-section` — a link from Alpha to Alpha resolves to `#alpha`, the section's own destination, and the section is emitted once. The run exits 0, where on the base it failed with `E_SELF_REFERENCE`.
- `self-reference/a-link-spelled-another-way-to-the-same-section` — `./%67uide.md#alpha` produces the identical bundle, so identity is read after the path and the fragment resolve.
- `self-reference/a-preamble-link-to-its-own-document` — a preamble link to its own document resolves to `#guide`.
- `ownership/a-self-reference-after-consolidation` — the same link resolves to `#detail` when the whole document is what the run selected, so consolidation changes nothing.
- `self-reference/a-link-back-to-an-including-ancestor`, `self-reference/a-section-link-to-its-whole-document`, `self-reference/a-link-to-another-section-of-the-same-file` and the other two `ownership` fixtures — unchanged, and still green.

The unit tests observing the same rule are `test_a_link_to_the_section_carrying_it_resolves_to_that_section`, `test_identity_is_compared_after_the_path_and_the_fragment_resolve`, `test_a_preamble_link_to_its_own_document_resolves_to_that_document` and `test_a_self_reference_resolves_the_same_after_consolidation`.

### A fixture retired rather than restated

`validation-scope/an-unselected-self-link` established that a self-link in an unselected sibling does not fail a run. A self-link in a selected section does not fail a run either now, so the fixture demonstrates nothing about scope. `validation-scope/an-unselected-broken-link` carries that statement with a link that does fail wherever it sits, and the other three `validation-scope` fixtures are unchanged.

## Build and repository checks

`make check` in full, on the rebased revision.

**All targets passed.**

- `lock-check`, `lint`, `format-check`, `typecheck` — clean. `ruff` reported `closure.marked` and `source.owner` as unused imports of `cli` once the two refusals went; both imports were removed.
- `test` — 628 passed.
- `harness` — 376 passed.
- `corpus` — 204 fixtures, 202 pass, 2 awaited.
- `smoke` — the wheel installs into a throwaway environment and bundles from a source root.
- `layout`, `tables`, `links --online`, `vocabulary`, `invocation` — each green. `vocabulary` confirms the glossary still defines every marked contract term, which is why the published prose is left to `W08`.

### A second limitation recorded rather than fixed

`source.owner()` has no caller in the product once `cli.self_referent()` goes; its unit tests in `src/tests/test_source.py` are all that reach it. `ruff` does not report it, because it is a module-level function with tests of its own. Removing it would take the design's **Link ownership** clause out of the code and would rewrite the **Ownership stability** note in `candidate`, so it is deferred as an issue of its own rather than carried here.
