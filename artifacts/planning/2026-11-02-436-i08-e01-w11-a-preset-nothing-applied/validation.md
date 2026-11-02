# Validation

The checks [W11](w11.md) and [W13](w13.md) name, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Branch head | `b18fb6f1` on `i08/e01/w11-a-preset-nothing-applied` |
| Epic base | `e520dfa4` on `i08/e01/main`, merged into the branch at `5f71e409` |
| Design pin | `fe234f2d` on `engineering`: the *Presets* clause names `W_PRESET_UNUSED` and the *Groups* rule marks *presets* |

## T1 Unit Tests

`pytest src/tests/test_cli.py` at `b18fb6f1`: every test passes, among them `test_a_preset_no_title_selects_warns_and_the_run_publishes` (two unselected presets of `rules.md` warned in declared order, each `W_PRESET_UNUSED` with `source` `rules.md`, no `location`, a remedy, exit `0` and the bundle published under `default`'s group), `test_selected_presets_and_default_warn_nothing`, `test_a_preset_one_reference_selects_is_used_though_another_leaves_it`, `test_a_preset_a_dispatched_bundle_selects_is_used` (two bundles), `test_a_preset_on_a_deferred_only_document_warns_nothing` (the deferred link published as authored, no diagnostic), `test_a_document_both_deferred_and_compiled_is_weighed`, and `test_the_codes_reported_are_the_codes_the_build_declares` holding `-C` to `W_PRESET_UNUSED`.

Result: pass.

## T2 Corpus Fixtures

`make corpus` at `b18fb6f1` reports each as `pass`: `inclusion/an-unused-preset-warns` (AC6: `W_PRESET_UNUSED` naming `guide.md` and `Draft`, exit `0`, the bundle published), `inclusion/a-deferred-target-keeps-its-preset` (AC7: the deferral published as authored, no diagnostic), `inclusion/a-followed-deferral-reads-its-preset` (AC7: the run naming `noted.md#draft` places it under `Drafts` by the `Draft` preset, no diagnostic), and the four settled fixtures `a-preset-key-holds-a-mapping`, `a-section-matching-no-preset-selects-default`, `a-section-title-selects-its-preset` and `a-whole-document-entry-selects-default`, each declaring the warning its unselected preset raises. W12's `one-document-two-presets` passes with no warning.

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `b18fb6f1`, exit 0. The unit suite reported 1606 passed and the harness 1154 passed. The corpus reported 427 fixtures, 427 pass, 0 fail, 0 awaited. The catalogue test holds the warning catalogue to the codes the pinned design names and to a declaring fixture; `make conformance` cites *Presets — A preset nothing selected warns* by 7 fixtures and reports `W_PRESET_UNUSED` declared by 5 fixtures and reported by the build; `make independence` finds every shaped term one the contract names.

Result: pass.

## T4 Pages

Within the same `make check` at `b18fb6f1`: `make invocation` holds 30 statements of the documented invocation to the build's help output; `make vocabulary` finds 47 contract terms marked at `fe234f2d`, *presets* among them, each defined in `docs/glossary.md`; `make links` resolves every reference in 237 documents; `make tables` holds every command table.

Result: pass.

## Findings

- **A second reference to one document from another section was dropped before W12.** The traversal kept only the first reference to a `(path, fragment)`, so per-reference selection, and therefore the unused set, saw one title. W12 (#515) carries each newly titled reference; this branch merges it, and the per-reference unit test reaches distinct sections so it holds either way.
- **`exclude` is retired by W14.** The pages this row writes name only `group-depth` and `subst`; the existing `exclude` code and text are W14's.
- **`subst` takes effect in I08:E06.** The invocation states a `subst` pair redirecting a reference, as the contract and the source page already do.
