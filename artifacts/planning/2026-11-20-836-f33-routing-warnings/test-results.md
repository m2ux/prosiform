# Test Results

Results for F33 at `39e540e34` on `f33-routing-warnings`, run on 2026-11-20 in the unit checkout.

## T1 Ordinary Presets

`inclusion/a-stage-routing-on-two-axes-raises-no-warning`: the specimen's `workflow.md` dispatches `stages/tally.md` under `strict` and `lenient`, each an ordinary preset mapping `../rules/counting.md`, picking the kind among two alternatives; the run publishes five bundles and no diagnostic. `inclusion/a-shared-pair-routes-with-the-ordinary-preset-first` and `test_a_pair_an_ordinary_preset_shares_routes_in_either_order` hold the same for an ordinary preset beside an alternative. Held.

## T2 Default

`inclusion/a-preset-states-the-pair`: a `default` pair compiles `stub.md` in place of `rules.md` and the run raises nothing; `inclusion/a-default-pair-an-alternative-agrees-with-routes` holds it beside an agreeing alternative. Held.

## T3 Stub

- `inclusion/a-shim-s-stub-warns-beside-a-stage-s-routes`: the specimen's shim warns `W_SUBST_USED` for `../rules/source.md` at `stages/tally.md:39`, and `W_PRESET_UNUSED` for `lenient`; the `strict` route raises nothing.
- `mock/a-substitution-warns-with-its-target`, `mock/a-mocked-check-publishes-nothing` and `inclusion/a-stand-in-beside-an-alternative-still-warns` declare their pair in an entry stub and warn as before.

Held.

## T4 Unused Route

`inclusion/an-ordinary-preset-s-pair-no-link-names-warns-unused`: `strict` maps `counting.md`, which the stage links, and `retired.md`, which it does not; the run warns `W_SUBST_UNUSED` for `retired.md` alone. Held.

## T5 Stub Over a Route

`inclusion/an-entry-stub-holds-over-a-stage-s-ordinary-preset`: the entry's `recorded` stub and the stage's ordinary preset `draft` map `review.md`; the stage's bundle carries the recorded review and the run warns `W_SUBST_USED` alone. `inclusion/an-entry-stub-holds-over-a-stage-s-own-pair` holds the same over `default`. Held.

## T6 Bundles

Every one of the 43 existing fixtures the rule touched failed on `expected.diagnostics` alone before its manifest changed, with every bundle comparison passing, so the corpus's bundles are byte-identical. The bundles of T1's and T3's fixtures equal the specimen's 0.32.0 output, `current-live/` and `current-shim/`, byte for byte. Held.

## T7 Documents

`docs/selection.md` owns the rule under The substitution mapping; `docs/glossary.md` defines a routing pair as any preset's but a stub's; `docs/validation.md` names `W_SUBST_USED` as a stub's alone; the design states it under The substitution mapping and the `W_SUBST_USED` catalogue entry, pinned at `d6b825c39`. Held.

## T8 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lint, format, typecheck, `make test` (2290 passed), harness (1152 passed), corpus (707 fixtures), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

`make eval-harness`, outside `make check`, fails 37 tests on `main` at `7419cfd9a` and the same 37 here, which [F02](https://github.com/m2ux/prosiform/issues/681) AC4 holds; the three this change touched pass.
