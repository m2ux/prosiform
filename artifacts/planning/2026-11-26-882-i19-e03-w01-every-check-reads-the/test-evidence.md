# Test Evidence

> Tested revision: `bf5c4f326` on `i19/e03/w01-shared-reading-and-docs`, based on `i19/e03/main` at `798f11ed9`. Recorded 2026-11-26.

## Indented fence in the vocabulary check

`checks/tests/test_vocabulary.py::test_a_mark_inside_a_fence_indented_in_a_list_item_is_an_example` passes: a design carrying `*indented term*` inside a fence indented under a list item inventories no such term. The check's former left-margin fence pattern read it as a mark.

## Indented fence in the conformance report

`checks/tests/test_conformance.py::test_a_fence_indented_in_a_list_item_states_no_clause` passes: a pipe table inside a fence indented under a list item yields no clause, where the former reader yielded `Resource limits — bytes`. `test_a_fence_indented_in_a_list_item_stays_in_its_section_as_written` passes: `partition` keeps the fenced lines, as written, in the section holding them, so `independence.py` reads the same text.

## The pinned design before and after

The marked terms, the clause list and the partition (lengths and SHA-256 of each part) of the design the README pins (`da12bcbec664becb169c073de013b9c9f00c21a0:artifacts/planning/2026-10-17-prosiform-v1/design.md`) are identical before and after the change. The design holds one indented fence (lines 138 to 195, the guide's text under **The text**), and nothing in it reads as a marked term, a heading, a bold-led bullet, a numbered step or a table row, so nothing moves.

## Avoided terms under docs/

`checks/tests/test_vocabulary.py::test_a_page_stating_an_avoided_term_reports_it_by_line`, `test_an_avoided_term_is_read_in_each_form_a_sentence_inflects_it_to` and `test_code_a_link_destination_and_the_avoided_table_are_not_prose` pass. Before the rewording, `make vocabulary` reported 41 uses across 13 pages; after it, `make vocabulary` reports none across the 15 pages under `docs/`.

## make check

`make check-all` with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`, run unsandboxed so `make links` reaches the network: every check passed, the corpus 708 of 708.
