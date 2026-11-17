# Test Results

Results for #772 at `ecc747933` on `772-stub-presets`, run on 2026-11-17 in the unit checkout.

## T1 Stub Below a Dispatch

`fixtures/inclusion/an-entry-name-selects-a-stub-below-a-dispatch`: under `[Entry](entry.md "recorded")` the dispatched stage reads the recorded review, takes the `--p-` qualifier, and warns `W_SUBST_USED`. `test_stub_presets.py::test_the_entry_name_selects_a_stub_below_a_dispatch` and `test_a_link_title_naming_a_stub_selects_it`. Held.

## T2 Deferral Titles

`fixtures/deferral/a-deferral-carries-the-runs-names`: `"checks"` publishes `"checks, recorded"`, and an untitled deferral `"recorded"`. `test_a_deferral_carries_the_runs_names` (inline, quoted, empty and reference-style titles), `test_a_deferring_click_carries_the_runs_names`, `test_a_deferred_directive_carries_the_runs_names` and `test_a_deferral_omits_a_name_its_target_declares_otherwise`. Held.

## T3 Silent Stub

`fixtures/inclusion/a-run-naming-no-stub-raises-no-warning-for-it`: a plain-path entry publishes the live stage under `stage.bundle.md` with no diagnostic. `test_a_run_naming_no_stub_is_silent`, and `test_an_entry_name_leaves_an_ordinary_preset_unselected` for the ordinary preset that still warns. Held.

## T4 Pair Reported Once

`fixtures/mock/a-stubs-pair-warns-once-across-bundles`: the pair redirects the review link in the entry's bundle and the dispatched one, and one `W_SUBST_USED` is raised. `test_a_used_stub_pair_warns_once_across_bundles`. Held.

## T5 Refusals

`fixtures/frontmatter/a-stub-beside-a-choice-fails`, `a-stub-in-default-fails` and `a-multi-line-stub-fails` each exit 1 with `E_INVALID_CONVERSION_METADATA` at the field. `test_a_malformed_stub_is_refused` and `test_a_stub_in_default_is_refused`. Held.

## T6 Documents

`docs/sources.md` (Frontmatter table and paragraph), `docs/selection.md` (Presets in force, The substitution mapping), `docs/glossary.md` (stub row), `invocation.md` (presets paragraphs) and the design at `e333bb447` (Conversion metadata, Presets, Link classification, Metadata failures) each state the stub kind; `make vocabulary` holds the glossary to the design's marked term. Held.

## T7 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's built `pf`, exits 0: lint, format, typecheck, `make test` (2158 passed), harness (1061 passed), corpus (622 fixtures, 622 pass), smoke, layout, tables, links (online), vocabulary, invocation, conformance and independence. Held.
