# Validation

The checks [W14](w14.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Branch head | `c2899ca2` on `i08/e01/w14-a-preset-holds-group` |
| Epic base | `bb404015` on `i08/e01/main` |
| Design pin | `d73d4ead` on `engineering`, stating a preset of two keys |

## T1 Unit Tests

`uv run --project src --frozen pytest src/tests/test_metadata.py` at `c2899ca2`: every test passes. `test_reserved_mapping_has_exact_keys` refuses unlisted preset keys with `unknown field prosiform.default.<key>`, the refusal an `exclude` key now meets; `test_a_field_outside_its_preset_names_the_preset_it_belongs_in` and `test_a_list_field_holds_a_list` run over the two admitted keys.

Result: pass.

## T2 Tree Search

`git grep -n -i -w "exclude\|exclusion\|exclusions"` at `c2899ca2` returns three lines, all workflow prose in `example/` and a usage-example expected bundle ("exclusion of unrelated sections"). No source, test, fixture or page names a preset `exclude` entry.

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `c2899ca2`, exit 0. The unit suite reported 1586 passed and the harness 1152 passed. The corpus reported 425 fixtures, 425 pass, 0 fail, 0 awaited. `make conformance` reads the design at `d73d4ead`, where no clause names `exclude`; `make independence` passes.

Result: pass.

## Findings

None. Nothing read `Preset.exclusions`, so removing the field changes no bundle.
