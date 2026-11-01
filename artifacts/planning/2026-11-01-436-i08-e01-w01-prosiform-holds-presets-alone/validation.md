# Validation

The checks [W01](w01.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Branch head | `489977f8` on `i08/e01/w01-prosiform-holds-presets-alone` |
| Epic base | `228a5faf` on `i08/e01/main` |

## T1 Unit Tests

`uv run --project src --frozen pytest src/tests/test_metadata.py` at `489977f8`: every test passes, among them `test_every_key_names_a_preset_holding_a_mapping`, `test_a_preset_key_holding_anything_but_a_mapping_is_refused` (six value kinds, each refused at `rules/a.md:3:11` naming `prosiform.Target`), `test_a_field_outside_its_preset_names_the_preset_it_belongs_in`, `test_a_document_declaring_no_default_is_compiled_under_an_empty_one`, `test_an_empty_preset_states_nothing`, `test_a_list_field_holds_a_list` and `test_a_root_within_a_preset_is_refused_at_its_key`.

Result: pass.

## T2 Corpus Fixtures

`make corpus` at `489977f8` reports `inclusion/a-preset-key-holds-a-mapping: pass` (exit `0`, the bundle compiled, no diagnostic) and `inclusion/a-preset-key-holding-a-scalar-is-refused: pass` (exit `1`, `E_INVALID_CONVERSION_METADATA` carrying `prosiform.Target must be a mapping` at `rules.md:3:11`). Both cite *Conversion metadata — The admitted keys*.

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `489977f8`, exit 0. The unit suite reported 1510 passed and the harness 1125 passed. The corpus reported 400 fixtures, 400 pass, 0 fail, 0 awaited. `make conformance` read 323 clauses with 0 declarations naming no clause; *Presets — `default` always applies* is cited by the 35 fixtures whose sources group, and *Conversion metadata — The admitted keys* by 4.

Result: pass.

## Findings

- **`docs/images/groups.svg` had drifted from the build.** Rendered from the epic base, the drawing differed from the committed one before this change; it is regenerated here with `dispatch.svg` and `parallel.svg`, all three from `scripts/examples.json` against the build under test.
