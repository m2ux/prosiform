# Validation

The checks [W09](w09.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Branch head | `cfed4302` on `i08/e01/w09-subst-holds-colon-pairs` |
| Epic base | `46f683ef` on `i08/e01/main` |
| Design pin | `3b55d654` on `engineering` |

## T1 Unit Tests

`uv run --project src --frozen pytest src/tests/test_metadata.py src/tests/test_cli.py` at `cfed4302`: every test passes, among them `test_a_subst_entry_is_a_colon_pair` (`{rules.md: stub.md}`, `{a.md#Checks: b/c%20d.md}` and the quoted `{"rules.md#Step 1: Setup": stub.md}` read whole, each at its entry's location), `test_a_subst_entry_that_is_no_colon_pair_is_refused_naming_it` (twelve cases: a string pair, two keys, an empty mapping, a list, a number and null refused as no mapping; a non-string key; a number, null and list value; an empty value and an empty key, each naming `prosiform.default.subst[n]` at the entry), `test_a_subst_side_is_read_by_the_reference_grammar` (a query, a malformed escape, an encoded separator, a root-relative path, a drive path, a backslash and an external side, each naming `prosiform.default.subst[1]` and the side) and `test_a_subst_pair_the_reference_grammar_reads_is_admitted` (a side above the working directory, a percent-encoded side and a quoted side holding `: `).

Result: pass.

## T2 Corpus Fixtures

`make corpus` at `cfed4302` reports `inclusion/a-subst-entry-is-a-colon-pair`, `inclusion/a-subst-side-is-read-by-the-reference-grammar` and `inclusion/a-preset-key-holds-a-mapping` (its preset now holding `subst: [{checks.md: stub.md}]`) as `pass`.

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `cfed4302`, exit 0. The unit suite reported 1580 passed and the harness 1140 passed. The corpus reported 415 fixtures, 415 pass, 0 fail, 0 awaited. `make conformance` cites *Conversion metadata — subst holds colon pairs* by 2 fixtures; `make independence` finds every shaped term one the contract names.

Result: pass.

## Findings

- **The design gave a wrong reason for the string form.** It said a reference in a mapping key would collide with a path's colons; YAML splits a plain key only at a colon followed by a space, and a quoted key carries one. The clause now states the colon pair and the quoting.
- **`SUBSTITUTION` served `-m` alone.** The `=` separator moved to `cli`, beside `mock`, its one reader.
