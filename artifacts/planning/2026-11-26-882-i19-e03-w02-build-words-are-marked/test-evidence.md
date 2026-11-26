# Test Evidence

Validation observed at `i19/e03/w02-build-words-marked` head 62b9102d1, based on `i19/e03/main` at 798f11ed9, with the design pinned at engineering da12bcbec.

## Marked Build Words

- **T1, AC2.** `checks/tests/test_independence.py` over a design written for the test: `test_a_word_a_silent_section_writes_unmarked_is_admitted` passes "meanwhile", which only the silent section carries and writes unmarked; `test_a_declaration_naming_a_word_only_a_silent_section_carries_is_reported` and `test_a_word_only_a_silent_section_carries_is_refused_whatever_its_shape` report `crate` (a code span) and `Oracle` (bold); `test_a_term_a_silent_section_marks_and_the_contract_states_is_admitted` passes "build", which the silent section bolds and a behavioural section states.
- **T2, AC2.** `test_a_declaration_naming_the_pinned_design_s_build_words_is_reported` reads the design the README pins and reports `cmark` and `pulldown` in a fixture description naming "pulldown-cmark".
- **Marks.** A build word is a word of a code span's code or of a bold span in a section stating no behaviour, read in the forms `independence.forms` gives a contract term; one the contract states in any form is not a build word.

### Build Words on the Pinned Design

| Section | Before (48 forms) | After (8 forms) |
| --- | --- | --- |
| Design status | differential, oracle, prototype, python, rust | cmark, pulldown |
| Production build obligations | cmark, crate, packag, package, packaged, product, pulldown, slugger, specification, wheel | into_offset_iter, reference_definition, reference_definitions |
| Implementation verification and residual policy detail | appropriate, assumption(s), authorization, calibration, concern(s), freeze, ingestion, numerical, performance, pr, proven, revision | calibration |
| Upstream follow-up reference | advance, backport, demonstrat(e, es), discussion, growth, introduc(e, ed), iterator, mitigation, observability, opt, project, propose, quadratic, regression, tracker | iterator, regression |

- **Previous delivery's build obligations.** `pulldown-cmark` is marked (a code span in Design status and Production build obligations) and is still reported. "crate" ("the choice of slugger crate remains open") and "wheel" ("packaged as a wheel") are written unmarked, so neither is a build word now; the design would need to mark them for the check to report them.
- **Bold labels.** The bold list labels of the silent sections contribute "calibration", "iterator" and "regression"; their other words are contract terms.

## Suites

- **T3.** `make check`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`, exits 0: lint, format, types, reachability, 2,116 build tests, 1,254 harness tests, 708 corpus fixtures (708 pass), smoke, layout, tables, links (445 documents), vocabulary, invocation, conformance and independence (8 build word forms, 708 fixtures, the report).
