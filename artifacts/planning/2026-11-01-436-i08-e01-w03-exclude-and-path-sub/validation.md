# Validation

The checks [W03](w03.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Branch head | `3571797e` on `i08/e01/w03-exclude-and-path-sub` |
| Epic base | `41bf6cc2` on `i08/e01/main` |
| Design pin | `425037d6` on `engineering` |

## T1 Unit Tests

`uv run --project src --frozen pytest src/tests/test_metadata.py` at `3571797e`: every test passes, among them `test_an_exclude_list_holds_names_and_levels_together` (a bare name, a level mapping, `#Notes` held as a name and `Draft: old` at level 6, each with its entry location), `test_a_malformed_exclude_entry_is_refused_naming_it` (seventeen entries, each named `prosiform.default.exclude[<n>]` at the entry), `test_a_path_sub_entry_is_a_pair_string` (split at the first `=`), `test_a_path_sub_entry_that_is_no_pair_string_is_refused_naming_it` (eight entries) and `test_every_key_names_a_preset_holding_a_mapping`.

Result: pass.

## T2 Run Tests

`uv run --project src --frozen pytest src/tests/test_cli.py -k path_sub` at `3571797e`: `test_a_path_sub_side_is_read_by_the_reference_grammar` (a query, a malformed escape, an escaped separator, a root-relative path, a drive path, a backslash and an external side, each `E_INVALID_CONVERSION_METADATA` at `guide.md:6:9` naming `prosiform.default.path-sub[1]` and the side) and `test_a_path_sub_pair_the_reference_grammar_reads_is_admitted` pass.

Result: pass.

## T3 Corpus Fixtures

`make corpus` at `3571797e` reports `inclusion/an-exclude-list-holds-names-and-levels`, `inclusion/a-malformed-exclude-entry-is-refused`, `inclusion/a-path-sub-entry-is-a-pair-string` and `inclusion/a-path-sub-side-is-read-by-the-reference-grammar` as `pass`.

Result: pass.

## T4 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `3571797e`, exit 0. The unit suite reported 1555 passed and the harness 1133 passed. The corpus reported 408 fixtures, 408 pass, 0 fail, 0 awaited. `make conformance` cites *Conversion metadata — An entry is one string key with an integer value* by 4 fixtures, *Conversion metadata — `exclude` holds names* by 1 and *Conversion metadata — `path-sub` holds pairs written as strings* by 2.

Result: pass.

## Findings

- **The source page's key table listed `group-depth` alone.** `exclude` and `path-sub` were admitted but unstated; the table now lists both with their shapes.
- **The `=` was stated twice.** The `-m` parser and the entry split at one constant, `metadata.SUBSTITUTION`.
