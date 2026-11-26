# Test Evidence

Validation observed at `i19/e02/w02-build-obligations-silent` head 6e6685615, based on `i19/e02/main` at 6eb02cb5c, with the design pinned at engineering da12bcbec.

## Build Obligations (W02)

- **T1, AC2.** `checks/tests/test_independence.py::test_a_declaration_naming_the_pinned_design_s_build_words_is_reported` reads the design the README pins and reports `crate` and `wheel` in a fixture description, each naming the `Production build obligations` section.
- **Design edit.** The sentences naming `pulldown-cmark`, its APIs, the Rust dependency pins, the slugger crate, the package name and the wheel move from Parser and source-preserving edits, Mandatory parser viability gates, Markdown and source-heading profile, Source-heading resolution, CLI contract and the two acceptance-fixture tables into a new `### Production build obligations` under Design status. The behavioural text keeps what each states of a run: a semantic parser behind a version-pinned source-range adapter, explicit parser options, a fixture-validated slug adapter. "installed-wheel smoke" reads "installed-command smoke".
- **Wording.** "no specific slugger crate is selected yet" reads "the choice of slugger crate remains open": `yet` appeared in behavioural text only in that sentence, so moving it made `yet` a build word and two dispatch-brief descriptions failed.
- **Conformance before and after.** `make conformance` over the old and new pin: 396 clauses, 74 uncovered, 43 declared names reached, 16 clauses no run states, in both. The only differences are the added line `section Production build obligations: non-behavioural, …` and the section count, 3 to 4. No clause is lost.
- **Vocabulary.** Build word forms 39 to 48; contract terms 2,954 to 2,936.

## Avoided Terms in Identities (W03)

- **T2, AC3.** `test_an_identity_stating_an_avoided_term_is_reported_with_its_reason` reports `branch` in an identity with the glossary's reason; `test_an_avoided_term_in_any_segment_of_an_identity_is_reported` reports `included` in a family segment.
- **Real corpus.** The first run reported six identities. Each is renamed in its description's words:

  | Old identity | New identity |
  | --- | --- |
  | `composition/a-link-inside-a-contribution-includes-its-target` | `composition/a-link-inside-a-contribution-bundles-its-target` |
  | `reference/an-html-anchor-in-a-node-label-naming-a-local-document` | `reference/an-html-link-in-a-node-label-naming-a-local-document` |
  | `reference/an-html-anchor-mermaid-draws-as-no-anchor-is-text` | `reference/an-html-link-a-renderer-draws-as-no-link-is-text` |
  | `rewriting/a-sequence-diagram-link-and-links-line-anchors` | `rewriting/a-sequence-diagram-link-and-links-line-destinations` |
  | `self-reference/a-link-back-to-an-including-ancestor` | `self-reference/a-link-back-to-an-already-selected-ancestor` |
  | `validation-scope/the-sibling-once-closure-includes-it` | `validation-scope/the-sibling-once-closure-reaches-it` |

- **References.** `checks/render.py` and `docs/composition.md` named old identities and name the new ones; `git grep` finds no other.

## Suites

- **T3.** `make check`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`, exits 0: lint, format, types, reachability, 2,125 build tests, 1,237 harness tests, 708 corpus fixtures (708 pass), smoke, layout, tables, links (445 documents), vocabulary, invocation, conformance and independence.
