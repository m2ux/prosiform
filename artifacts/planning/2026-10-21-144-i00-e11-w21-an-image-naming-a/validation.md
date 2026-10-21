# Validation — I00:E11:W21

> Observed 2026-10-21 against `i00/e11/w21-an-image-naming-a` at `6c05967`, cut from `i00/e11/main` at `ce4483c`.

The build under test is the worktree's own, named to the corpus and invocation checks as `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"`.

## Procedure

`make check` runs the repository's whole set in one pass: `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `harness`, `corpus`, `smoke`, `layout`, `tables`, `links`, `vocabulary` and `invocation`. It was run twice — once on the predicate and the corpus, and once more after the glossary entry was restated — and each run was observed to completion rather than stopped at its first green target.

## Repository checks

**`make check` exits 0, every target green.**

| Target | Observed |
| --- | --- |
| `lock-check` | the lock resolves nothing new |
| `lint`, `format-check` | clean over `src/prosiform`, `src/tests`, `checks` |
| `typecheck` | no issues in 49 source files |
| `test` | 487 passed |
| `harness` | 672 passed |
| `corpus` | 217 fixtures, 217 pass, 0 fail, 0 awaited, 0 unexpected pass |
| `smoke` | the wheel installs and the command resolves by name outside the repository |
| `layout`, `tables`, `links`, `vocabulary`, `invocation` | 3 trees, 14 commands and 7 declarations, 12 documents, 35 contract terms, 27 invocation statements |

The corpus holding no awaited fixture is itself an observation: the two rows awaited when the preceding unit measured this gap have since landed, so nothing in the tree is declared as pending behaviour.

## AC22 — an image naming a document warns, a bundle naming no resource does not

Both edges of the rule are published in `fixtures/resource`, and both are held again by the build's own suite.

**Observed for the warning.** `resource/an-image-naming-a-document-under-the-root` passes. Its source carries one reference, `![the rules](rules.md)`, naming a Markdown document that exists under the allowed source root. The run exits 0, publishes the image as its author wrote it, carries nothing of `rules.md`, and emits on stderr:

```text
W_RESOURCE_PORTABILITY: the bundle names at least one resource, which it carries as the
text its source wrote, so a reader opening the bundle from another directory may not find it
W_ENTRY_DESTINATION: the entry reference 'guide' resolves to the destination 'guide', which
the bundle's entry line links it to
```

The manifest now declares that warning, so the corpus states the rule rather than the gap. On the base the same fixture declared the entry-destination warning alone.

**Observed for the silence.** `resource/a-bundle-naming-no-resource-does-not-warn` passes unchanged. Its source carries a relative path inside a fenced console example, which the parser reads as text and not as a use, and one link carrying a scheme. Neither is a resource, and the run emits `W_ENTRY_DESTINATION` alone.

**Observed once per bundle.** `resource/a-marked-resource-is-emitted-as-authored` passes unchanged. Its source carries two resource references — a marked link and a marked image, both naming `plan.png` — and the run emits exactly one `W_RESOURCE_PORTABILITY`.

**The build's own suite.** `test_an_image_naming_a_markdown_document_warns_once_on_portability` asserts the code appears exactly once in the JSON diagnostic stream of a run whose only resource is an image naming a Markdown document. `test_a_bundle_naming_no_resource_does_not_warn_on_portability` asserts the code is absent from a run whose only reference carries a scheme. The pre-existing `test_an_image_naming_a_markdown_document_carries_no_document` still holds, so the warning was added without the document becoming bundleable.

## Observations

- **The two classifications now agree.** `source.uses()` marks every image a resource, `cli.required()` passes over one on that mark, and `cli.resourced()` reads the same mark through the same walk. A run gives one answer about a reference whichever question is asked of it.
- **No fixture outside the `resource` family moved.** The predicate widens only for a local image whose destination the profile reads as Markdown, which is a shape no other fixture carries. The five fixtures already declaring `W_RESOURCE_PORTABILITY` — in `traversal`, `diagnostics`, `headings` and `reference` — pass with their manifests untouched.
- **`resourced()` now descends into an image's alternative content.** Reading the bundle through `source.uses()` brings that walk with it. `reference/a-link-inside-image-alternative-content` already declared the warning and still passes, so the reach is wider and the published rule is unchanged.
- **Four imports left `cli.py`.** `HREF`, `SRC`, `INLINE` and `REFERENCE_USES` were read only by the inline walk the shared one replaces, and `lint` is what observed their going.

## Limitations

- **A remote image still warns not at all.** A destination carrying a scheme, an authority or a drive letter names something no directory the bundle is read from decides, so it is a resource under neither use. This follows the design clause, which makes a *relative* image or other non-Markdown reference the text the warning is about, and it is what `resource/a-bundle-naming-no-resource-does-not-warn` publishes. It is a deliberate edge of the rule rather than a gap.
- **The warning says nothing about which reference raised it.** It fires once per bundle and names no destination, so an author with twenty resources is told the bundle has at least one. That is the design's wording and was not in this row's scope.
