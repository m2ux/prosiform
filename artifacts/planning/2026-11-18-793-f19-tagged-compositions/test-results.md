# Test Results

Results for F19 at `622c1f6ff` on `f19-tagged-compositions`, stacked on `f16-dispatch-brief` at `4cbd9db52`, run on 2026-11-18 in the unit checkout. Each refusal or wrong route a fixture names for the base was observed with the build of `f16-dispatch-brief` at `d252f2233`.

## T1 Contributions Under Their Own Presets

`fixtures/composition/each-contribution-follows-its-own-presets`: `stage.md` declares `task: {subst: [{body.md: task-body.md}]}` and its Given section links `body.md#body`. The guide composes Given once with the title `task` and once with none. The run publishes at exit status 0: the tagged contribution's link points at the task body and the untagged one's at the body, both bundled, with one `W_SUBST_USED` at `stage.md:10`. The base publishes both contributions pointing at the task body and bundles no body. Held.

## T2 Copy Mapping, Dispatch Places and Warnings

In `src/tests/test_subst.py`:

- `test_a_composed_copy_resolves_under_its_own_selections_pairs`, `test_a_copy_whose_selection_puts_no_pair_in_force_redirects_nothing` and `test_a_copys_selection_leaves_another_documents_links_to_its_group`: the copy mapping's lookup.
- `test_a_copy_routing_its_dispatches_apart_from_the_group_places_its_own`: a section the guide includes and composes with and without a preset routing a dispatch-set member; the untagged copy shares the group's set and the tagged copy places its own.
- `test_a_default_pair_in_force_for_a_copy_alone_warns_where_unused`: a `default` pair in force for a copy alone that no reference used warns as `W_SUBST_UNUSED`.
- `test_a_copys_route_stays_quiet_beside_a_groups_standing_pair`: a copy taking its alternative's route raises no `W_SUBST_USED` where the group's ordinary preset states a stand-in for the same key.

Held.

## T3 Briefs Under Their Own Dispatch's Presets

`fixtures/dispatch-brief/each-brief-follows-its-own-dispatch-s-presets`: one briefed target dispatched with the title `task`, which routes `rules.md` to `task-rules.md`, and with none. The run publishes at exit status 0, each brief copy with its own route, both rules bundled, with one `W_SUBST_USED` at `investigate.md:12`. The base routes both copies to the task rules. `fixtures/dispatch-brief/a-brief-walked-for-loops-follows-its-own-dispatch-s-presets`: the loop walk reads each brief under its own dispatch's presets, so a brief only the tagged copy routes into a loop closes none; the run publishes the nested briefs with `W_DISPATCH_DEPTH` and `W_SUBST_USED`. `fixtures/dispatch-brief/a-briefed-dispatch-two-copies-route-apart-is-refused`: two copies routing one briefed dispatch to two targets fail with `E_HEADING_COLLISION` at `stage.md:10`. Held.

## T4 Full Check

`make check`, with `PROSIFORM_BUILD` naming the unit checkout's `pf` and its `src/.venv/bin` first on `PATH`, exits 0: lock, lint, format, typecheck, `make test` (2266 passed), harness (1116 passed), corpus (677 fixtures, 677 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## T5 Copies Mapping One Key Apart

`fixtures/composition/two-copies-mapping-one-key-to-two-substitutes-publish` and `fixtures/dispatch-brief/two-briefs-mapping-one-key-to-two-substitutes-publish`: two directives, and two dispatches of one briefed target, selecting presets that map one key to two substitutes. Each run publishes at exit status 0, each copy with its own substitute, with one `W_SUBST_USED` for each. The base fails both with `E_INVALID_USAGE`. In `test_subst.py`, `test_a_copys_presets_clash_with_no_including_references` publishes a group under one preset beside a copy under the clashing one, and `test_two_including_references_mapping_one_key_apart_are_refused` still refuses two including references with `E_INVALID_USAGE`. Held.

## T6 Copies Picking Different Alternatives

`fixtures/composition/two-copies-picking-different-alternatives-publish` and `fixtures/dispatch-brief/two-briefs-picking-different-alternatives-publish`: two directives, and two dispatches, picking the alpha and beta alternatives that route one key. Each run publishes at exit status 0 with no diagnostic, each copy under its own pick. The base fails both with `E_ALTERNATIVE_UNRESOLVED`. `fixtures/composition/a-copy-picking-no-alternative-beside-one-picking-one-is-refused`: a copy needing an alternative and picking none fails with `E_ALTERNATIVE_UNRESOLVED` beside one picking alpha. In `test_subst.py`, `test_a_copy_needs_no_alternative_that_states_only_a_group_pair` publishes a copy whose alternatives state only `group` pairs. Held.
