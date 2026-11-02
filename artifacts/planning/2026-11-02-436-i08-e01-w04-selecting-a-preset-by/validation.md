# Validation

The checks [W04](w04.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Branch head | `065d5bc2` on `i08/e01/w04-selecting-a-preset-by` |
| Epic base | `1e53329e` on `i08/e01/main` |
| Design pin | `425037d6` on `engineering` |

## T1 Unit Tests

`uv run --project src --frozen pytest src/tests/test_cli.py` at `065d5bc2`: every test passes, among them `test_a_preset_name_appears_as_whole_words_in_a_title` (thirteen cases: `checks` and `Draft` in `Checks and Draft`, `CHECKS` in `checks`, `checks` in `Self-checks`, `checks_v2` and `Checklist and checks`, `release checks` in `Release Checks`; `checks` in `Checklist`, `Prechecks`, `checks2` and `Rückchecks`, `check` in `Checks` and an empty name each selecting nothing), `test_default_is_selected_by_no_title`, `test_a_selected_preset_holds_over_default_for_the_group_it_pairs`, `test_a_whole_document_entry_selects_by_its_title` (`# Release Checks` puts `Checks` in force), `test_an_untitled_whole_document_entry_selects_no_preset`, `test_a_reference_in_a_preamble_selects_no_preset`, `test_a_reference_selects_by_the_nearest_heading_rooting_a_section` (a link under `### Detail` selects nothing; one past a quoted `### Quoted` selects by `## Checks`) and `test_a_depth_disagreement_names_the_selected_preset` (`prosiform.default` on one side, `prosiform.Checks` on the other).

Result: pass.

## T2 Corpus Fixtures

`make corpus` at `065d5bc2` reports `inclusion/a-section-title-selects-its-preset`, `inclusion/a-title-matching-two-keywords-selects-both`, `inclusion/default-applies-in-every-section`, `inclusion/a-section-matching-no-preset-selects-default`, `inclusion/a-whole-document-entry-selects-default`, `inclusion/an-entry-name-reads-its-documents-presets` and `inclusion/a-presets-pairs-reach-the-reference-it-governs` as `pass`.

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `065d5bc2`, exit 0. The unit suite reported 1576 passed and the harness 1140 passed. The corpus reported 415 fixtures, 415 pass, 0 fail, 0 awaited. `make conformance` cites *Presets — Selection by keyword* by 6 fixtures, *Presets — A command-line entry reads the file it names* by 2 and *Presets — What a selection governs* by 1; `make independence` finds every shaped term one the contract names.

Result: pass.

## Findings

- **Three documents said `default` alone placed a document.** The invocation, the source page and the hierarchy page now state selection above `default`.
- **`E_GROUP_DEPTH_CONFLICT` named `prosiform.default` for every pair.** Each side now names the preset stating its pair.
- **The epic plan's `path-sub` fixtures could not observe selection.** A preset's `path-sub` takes effect in [I08:E06](https://github.com/m2ux/prosiform/issues/461), so the fixtures observe selection through `group-depth`, the setting a run reads.
- **The epic plan's governing-preset fixture read the old model.** `b-w02.md` described the linking document's preset placing its target; the fixture states the target's own preset, selected by the linking section, as the design does.
