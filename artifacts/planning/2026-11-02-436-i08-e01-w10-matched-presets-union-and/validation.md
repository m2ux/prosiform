# Validation

The checks [W10](w10.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Branch head | `16d85a8e` on `i08/e01/w10-matched-presets-union-and` |
| Epic base | `19711a10` on `i08/e01/main` |
| Design pin | unchanged; the *Selected presets union* and *What a selection governs* clauses already state this row |

## T1 Unit Tests

`pytest src/tests/test_cli.py` at `16d85a8e`: every test passes, among them `test_a_group_its_preset_names_twice_is_refused` (one depth and two, each `E_INVALID_USAGE`, exit `2`, naming `prosiform.default.group-depth[1]` with `[0]` related), `test_a_subst_rule_stated_twice_or_against_itself_is_refused` (`rules.md` and `./rules.md` as two keys, one key with a section twice, `notes/../rules.md`, a key naming its value, `#Checks` as the value of `guide.md#Checks` in `guide.md`, and a section-only key), `test_subst_keys_naming_distinct_identities_are_admitted`, `test_two_selected_presets_pairing_one_group_at_two_depths_are_refused` (the message, both locations and the related message), `test_two_selected_presets_mapping_one_key_two_ways_are_refused`, `test_selected_presets_agreeing_about_a_setting_union`, `test_a_selected_preset_disagreeing_with_default_holds_over_it`, `test_presets_one_title_leaves_unselected_disagree_with_nothing` and `test_a_linking_documents_presets_never_reach_the_document_it_links`.

Result: pass.

## T2 Corpus Fixtures

`make corpus` at `16d85a8e` reports each as `pass`: `inclusion/a-preset-governs-its-own-document`, `inclusion/a-dependencys-preset-comes-from-itself` (AC5), `inclusion/two-presets-disagreeing-are-refused`, `inclusion/a-duplicate-subst-entry-is-refused`, `inclusion/a-section-only-subst-key-is-refused` (AC16, as named), and `inclusion/two-presets-disagreeing-about-a-subst-key-are-refused`, `inclusion/a-subst-key-naming-its-value-is-refused`, `inclusion/a-group-named-twice-in-one-preset-is-refused` (the AC16 cases the named three leave unshown).

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `16d85a8e`, exit 0. The unit suite reported 1596 passed and the harness 1148 passed. The corpus reported 423 fixtures, 423 pass, 0 fail, 0 awaited. `make conformance` cites *Presets — Selected presets union* by 7 fixtures and *Presets — What a selection governs* by 3; `make independence` finds every shaped term one the contract names.

Result: pass.

## Findings

- **A repeated group was deduplicated rather than refused.** `cli.joined` collapsed two equal `group-depth` entries of one preset, and two depths surfaced as a cross-document `E_GROUP_DEPTH_CONFLICT`, exit `1`. Both are now refused at the entry with `E_INVALID_USAGE`, exit `2`.
- **The work item refused `default` against a selected preset.** The design layers `default` beneath every selection, which W04 built, so only selected presets are compared.
