# Test Evidence

Validation observed at `i19/e03/w02-build-words-marked` head 02918bc2e, which merges `i19/e03/main` at 151ccf399 and `i19/e03/w04-documentation-without-boundary` at 583bfd4fc, with the design pinned at engineering 6abf65a2d.

## Marked Build Words

- **T1, AC2.** `checks/tests/test_independence.py` over a design written for the test: `test_a_word_a_silent_section_writes_unmarked_is_admitted` passes "meanwhile", which only the silent section carries and writes outside a code span; `test_a_declaration_naming_a_word_only_a_silent_section_carries_is_reported` and `test_a_word_only_a_silent_section_carries_is_refused_whatever_its_shape` report `crate` and `Oracle`, each in a code span there; `test_a_term_a_silent_section_marks_and_the_contract_states_is_admitted` passes "build", which the silent section writes in a code span and a behavioural section states.
- **T2, AC2.** `test_a_declaration_naming_the_pinned_design_s_build_words_is_reported` reads the design the README pins and reports `crate` and `wheel`, each naming the `Production build obligations` section; `test_a_bold_label_the_pinned_design_s_silent_sections_carry_is_admitted` passes "calibration", "iterator" and "regression".
- **Marks.** A build word is a word of a code span's code in a section stating no behaviour, read in the forms `independence.forms` gives a contract term; one the contract states in any form is not a build word. Bold is not a mark: the design's bold list labels name topics, not a build's words.

### Build Words on the Pinned Design

| Section | Every word, design da12bcbec (48 forms) | Code spans and bold, da12bcbec (8 forms) | Code spans, 6abf65a2d (8 forms) |
| --- | --- | --- | --- |
| Design status | differential, oracle, prototype, python, rust | cmark, pulldown | cmark, pulldown |
| Production build obligations | cmark, crate, packag, package, packaged, product, pulldown, slugger, specification, wheel | into_offset_iter, reference_definition(s) | crate, into_offset_iter, reference_definition(s), slugger, wheel |
| Implementation verification and residual policy detail | appropriate, assumption(s), authorization, calibration, concern(s), freeze, ingestion, numerical, performance, pr, proven, revision | calibration | none |
| Upstream follow-up reference | advance, backport, demonstrat(e, es), discussion, growth, introduc(e, ed), iterator, mitigation, observability, opt, project, propose, quadratic, regression, tracker | iterator, regression | none |

- **Code spans alone at da12bcbec.** 5 forms: cmark, pulldown, into_offset_iter, reference_definition(s); "crate" and "wheel" were written unmarked there.
- **Design 6abf65a2d.** W04's design edit writes "crate", "wheel" and the slugger in code spans, so they are build words again.

## Suites

- **T3.** `make check-all`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`, passes every check: lint, format, types, reachability, 2,116 build tests, 1,263 harness tests, 708 corpus fixtures (708 pass), smoke, layout, tables, links (445 documents), vocabulary, invocation, conformance and independence (8 build word forms).
