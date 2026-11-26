# Test Evidence

Validation observed at `i19/e00/w06-build-words-in-design` head 72fd9575e, based on `i19/e00/main` at 3c400526d.

## Build Words (W06)

- **T1, AC7.** `checks/tests/test_independence.py` supplies a design whose `Design status` section carries `crate` and `oracle`:
  - `test_a_declaration_naming_a_word_only_a_silent_section_carries_is_reported` reports `crate` in a fixture description, naming the `Design status` section.
  - `test_a_report_entry_naming_a_word_only_a_silent_section_carries_is_reported` reports `crate` on the conformance report line listing a fixture whose identity carries it.
  - `test_a_word_only_a_silent_section_carries_is_refused_whatever_its_shape` reports `crates` and `Oracle`.
  - `test_a_word_a_silent_section_shares_with_the_contract_is_admitted` passes `build`, which a behavioural section also states.
  - `test_a_word_naming_a_file_the_fixture_carries_is_the_tree_s` passes `oracle` in a fixture carrying `oracle.md`.
- **T1, partition.** `checks/tests/test_conformance.py::test_a_section_stating_no_behaviour_is_partitioned_from_the_contract` holds the silent section's text apart and keeps its heading behavioural.
- **Real corpus.** Over the pinned design, 39 word forms are build words, among them `python`, `prototype`, `oracle`, `freeze`, `calibration` and `backport`. The first run reported `freeze` in four Gantt fixtures' carried messages, which quote the task named after the fixture's `freeze.md`; the tree rule admits it. It also reported `obligations`, `project` and `proven` in conformance's own reasons for its silent sections, which are reworded.

## Avoided Terms (W07)

- **T2, AC8.** `test_a_description_stating_an_avoided_term_is_reported_with_its_reason` reports `branches` with the reason `is a term docs/glossary.md deliberately does not use: Collides with the version-control sense.`
  - `test_the_glossary_states_why_each_avoided_term_is_avoided` reads the table's terms and reasons.
  - `test_an_avoided_term_the_design_s_prose_states_is_still_reported` reports `included` in a description although the design's prose states it.
- **Real corpus.** The first run reported 27 avoided terms in 26 descriptions (`include`, `anchor` and `branch` in their inflections). Each description is reworded; no expected output changes.

## Suites

- **T3.** `make check`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`, exits 0: lint, format, types, 2,125 build tests, 1,206 harness tests, 708 corpus fixtures (708 pass), smoke, layout, tables, links (445 documents), vocabulary, invocation, conformance and independence.
