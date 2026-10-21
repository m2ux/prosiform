# Validation

The checks this row ran, the revision they ran against, and what each observed.

## Revision

- **Branch.** `i00/e12/w02-a-deferred-link-carried` at `79af747`, rebased onto `i00/e12/main` at `8e84fee`, which carries the merges of `W06`, `W03`, `W04` and `W05`.
- **Build under test.** `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"`, the build the change produces, reached through its console entry point.
- **Commands.** Each is a named target of the repository's `Makefile`, run from the repository root. Every result below was taken after the rebase.

## Unit suite

`make test` — 632 tests, all passing. Eleven of them are this row's and observe the deferral.

- **AC3, the withholding.** `test_a_marked_reference_under_the_root_is_not_compiled` runs the command against a root holding a document that defers a second one. The run succeeds, the target's file heading is absent from the bundle and so is its body, so the document was not opened through that reference. `test_a_deferred_fragment_of_its_own_document_is_not_compiled` says the same of a fragment-only reference: the section it names is not carried.
- **AC3, the carrying.** `test_a_deferred_link_carries_the_mark_its_author_wrote` reads the published link back out of the bundle with its mark and its authored destination. `test_the_bytes_between_the_mark_and_the_text_are_carried` runs the same check against `[¬the rules]` and `[¬\tthe rules]`, so the spaces or tabs an author wrote after the mark reach the bundle as written.
- **A deferral is read from the link.** `test_a_deferral_stands_where_another_reference_carried_its_target` declares a root where one document defers `rules.md` and a second requires it. The bundle carries `rules.md`, rewrites the second document's link to the destination it assigned, and publishes the deferred link exactly as authored.
- **The classifier.** `test_a_marked_reference_under_the_root_is_no_dependency`, `test_the_same_reference_unmarked_is_a_dependency` and `test_a_mark_written_inside_a_link_text_defers_nothing` hold `closure.bundled()` to the rule directly: the mark opens the link text or it defers nothing.
- **The emission.** `test_a_compiled_link_is_written_to_its_destination` pairs each link a token carries with the destination the bundle assigned it; a deferred link is assigned none and is published with the bytes its author wrote, its mark and its reference-style title included.
- **A heading.** `test_an_ancestor_title_keeps_the_mark_a_link_it_carries_was_deferred_by` reads a deferred link written inside a heading: the ancestor title the bundle emits and the title the record names both carry the mark.

## Corpus

`make corpus` — 207 fixtures, 205 passing, 0 failing, 2 awaiting later work, 0 passing while awaiting it. The two awaiting fixtures are the ones the corpus already carried: `reference/a-link-inside-image-alternative-content` awaits `I00:E11:W10` and `grouping/a-rule-matching-no-document-in-the-closure` awaits `I00:E11:W14`.

- **AC3.** `deferral/a-marked-reference-is-not-compiled` declares a root of two documents, the first deferring the second. The published bundle is the entry line and the first document alone, carrying `[¬ the shared rules](rules.md)` as authored.
- **AC3, a fragment.** `deferral/a-deferred-fragment-of-its-own-document` defers a section of the document carrying the link. The selected section is published with the link as authored, and the deferred section is nowhere in the bundle.
- **AC3, against another author's reference.** `deferral/a-deferral-stands-where-another-reference-carried-its-target` declares three documents: the entry defers `rules.md` and requires `house.md`, which requires `rules.md`. The bundle carries all three, rewrites the house style's link to `#rules`, and leaves the deferred link as its author wrote it.
- **The corpus the row inherited.** Every fixture the base carried produced the bytes its manifest declares, the `citation/` and `self-reference/` families included, so withholding the compilation changed nothing a reference outside the root, a resource or a refused self-reference does.

## Repository checks

Each ran against the same revision.

| Command | Result |
| --- | --- |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | no issues in 44 source files |
| `make lock-check` | the lockfile describes the declared dependencies |
| `make layout` | 3 trees present |
| `make tables` | 14 commands and 7 declarations, each declared and named |
| `make vocabulary` | 34 contract terms, every one defined in the glossary |
| `make links` | every reference in 12 documents resolved |
| `make invocation` | 27 statements of the documented invocation held to the build |
| `make smoke` | the wheel installs and bundles from a source root, outside the repository |

## The harness suite

`make harness` — 379 tests, all passing.

`I00:E12:W01` recorded this suite failing on the two error codes [D59](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) withdrew from the design while the build still raised them. `W04` and `W05` retired `E_MARKED_RESOURCE` and `E_SELF_REFERENCE` with the rules that replace them, and both merged into the epic base before this row was rebased onto it, so the catalogue the schema enumerates is the catalogue the design declares.

## A deferred reference naming nothing

A reference under the root that resolves to no document fails with `E_TARGET_NOT_FOUND` where the bundle compiles it, and succeeds where its author deferred it.

```text
[the steps](procedure.md)    E_TARGET_NOT_FOUND, exit status 1
[¬ the steps](procedure.md)  published as authored, exit status 0
```

`AC5` states the failure for a deferred reference as well, and `W03` delivered it against a base on which a marked reference was compiled, so the compiled path is the one it could observe. Withholding the compilation is what opens the difference: a deferred reference is passed over before the traversal reads anything, so nothing confirms the document and the heading it names.

Confirming them is the work the design's *A deferred link's target* clause describes — the reference resolved, the document and the heading confirmed, and the document not bundled through that reference — and it is the same resolution `W07` performs to rebase a deferred destination to the target's root-relative path. This row records it rather than widening into it; the [change list](changes.md) carries the recommendation.
