# Validation

The checks [W15](w15.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Branch head | `ad7623ff` on `i08/e01/w15-a-preset-s-group` |
| Epic base | `c8189098` on `i08/e01/main` |
| Design pin | `c1c68415` on `engineering`, stating `group` as one pair and `E_GROUP_CONFLICT` |

## T1 Unit Tests

`uv run --project src --frozen pytest` at `ad7623ff`: every test passes. `test_group_and_marks` reads `group:` holding `" règles ": 2` into `Preset.membership` at the key's and depth's columns; `test_a_malformed_group_pair_is_refused_at_its_value` refuses `{modes: 1, targets: 2}`, `{3: 1}`, `{null: 1}`, `{true: 1}`, `{2.0: 1}`, `{}`, `modes` and `[modes, 1]` with `prosiform.default.group must` at the value. `test_a_selected_preset_pair_holds_over_default` reads the selected pair over `default`'s, `default`'s where the selected preset states none, and none where neither states one. `test_two_selected_presets_stating_different_group_pairs_are_refused` refuses `{reviews: 1}` beside `{reviews: 2}` and beside `{drafts: 1}` with `E_INVALID_USAGE`, exit 2, at both pairs' group keys. The corpus fixture `fixtures/inclusion/two-presets-stating-two-groups-are-refused` holds the two-group case end to end.

Result: pass.

## T2 Tree Search

`git grep -n -i "group-depth\|GROUP_DEPTH_CONFLICT\|group: \["` at `ad7623ff` returns nothing. `cli.group_depths`, the per-group depth table, is the one identifier carrying the words, and names no key.

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `ad7623ff`, exit 0. The unit suite reported 1574 passed and the harness 1150 passed. The corpus reported 423 fixtures, 423 pass, 0 fail, 0 awaited. `make conformance` reads the design at `c1c68415` with 0 declarations naming no clause, so every fixture's clause, *`group` holds one pair* among them, is one the pinned design states; `make independence` and `make mock-scenarios` pass.

Result: pass.

## Findings

- **Four fixtures depended on one link placing a document in two divisions.** `a-title-matching-two-keywords-selects-both` and `default-applies-in-every-section` showed selection by joining a second division, and are rewritten to show it with one pair; `a-dependencys-preset-comes-from-itself` and `an-entry-name-reads-its-documents-presets` are re-recorded with the selected pair holding over `default`'s. `a-document-joins-two-divisions` existed only for the list and is removed.
- **A selected preset's pair replaces `default`'s.** With one pair per link, `default`'s pair and a selected preset's naming another group cannot both hold; the selected pair holds, as *`default` always applies* states.
