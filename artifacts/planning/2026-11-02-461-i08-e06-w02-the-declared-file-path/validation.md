# Validation

Evidence for each check the work items [w02.md](w02.md), [w06.md](w06.md) and [w08.md](w08.md) name, on branch `i08/e06/w02-the-declared-file-path`.

## Unit Tests

`cd src && uv run --frozen pytest` at `cd4b10828`: every test passes. `src/tests/test_mock.py` holds the tests these criteria read:

- `test_a_preset_pair_reads_the_same_from_any_working_directory` compiles one declaration from `modes/` and from the directory above and compares the bundles (AC3).
- `test_a_substitutes_fragment_only_link_names_its_own_section` resolves a substitute's `#part` under the substitute's own pairs (AC8).
- `test_two_documents_declaring_one_key_are_two_pairs` holds `W_SUBST_USED` and `W_SUBST_UNUSED` to the declaring document of each pair (AC8).
- `test_a_folder_side_is_refused_naming_the_entry` holds `subst: [{rules/: stubs/}]` to exit `1` and `E_INVALID_CONVERSION_METADATA` naming `prosiform.default.subst[0]` (AC11).

## Corpus

`make corpus` at `cd4b10828`, with `PROSIFORM_BUILD` naming the worktree's build: 432 fixtures, 432 pass. The four fixtures this unit adds pass:

- `fixtures/inclusion/a-preset-pair-resolves-from-its-file` (AC3)
- `fixtures/inclusion/a-subst-pair-stays-in-its-document` (AC8)
- `fixtures/inclusion/a-dispatched-bundle-reads-its-own-subst` (AC9)
- `fixtures/inclusion/a-folder-subst-is-refused` (AC11)

The six folder-form fixtures under `fixtures/mock/` are withdrawn.

## Make Check

`make check` at `cd4b10828`, with `PROSIFORM_BUILD` naming the worktree's build: exit `0`. The conformance report names no declaration naming no clause, and every fixture added names a clause the pinned design carries.
