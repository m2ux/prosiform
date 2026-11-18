# Test Results

Results for F19 at `151462ea3` on `f19-tagged-compositions`, stacked on `f16-dispatch-brief` at `d252f2233`, run on 2026-11-18 in the unit checkout.

## T1 Contributions Under Their Own Presets

`fixtures/composition/each-contribution-follows-its-own-presets`: `stage.md` declares `task: {subst: [{body.md: task-body.md}]}` and its Given section links `body.md#body`. The guide composes Given once with the title `task` and once with none. The run publishes at exit status 0: the tagged contribution's link points at the task body and the untagged one's at the body, both bundled, with one `W_SUBST_USED` at `stage.md:10`. The build of `f16-dispatch-brief` at `d252f2233` publishes both contributions pointing at the task body and bundles no body. Held.

## T2 Copy Mapping and Dispatch Places

In `src/tests/test_subst.py`:

- `test_a_composed_copy_resolves_under_its_own_selections_pairs`: a copy's link resolves through its own selection's pair, and the group's link through the group's.
- `test_a_copy_whose_selection_puts_no_pair_in_force_redirects_nothing`: a copy whose selection states no pair keeps its link, whatever the group's pairs.
- `test_a_copys_selection_leaves_another_documents_links_to_its_group`: a link another document writes while a copy is read resolves under that document's group pairs.
- `test_a_copy_routing_its_dispatches_apart_from_the_group_places_its_own`: a section the guide includes and composes with and without a preset routing a dispatch-set member; the tagged copy shares the group's set, which dispatches the task target, and the untagged copy places a set of its own dispatching the authored target.

Held.

## T3 Briefs Under Their Own Dispatch's Presets

`fixtures/dispatch-brief/each-brief-follows-its-own-dispatch-s-presets`: `investigate.md` declares a `default` brief `#given` and `task: {subst: [{rules.md: task-rules.md}]}`; the guide dispatches it once with the title `task` and once with none. The run publishes at exit status 0: the tagged brief copy's link points at the task rules and the untagged one's at the rules, both bundled beside the briefs, each dispatched bundle carrying the section under its own presets, with one `W_SUBST_USED` at `investigate.md:12`. The build of `f16-dispatch-brief` at `d252f2233` publishes both brief copies pointing at the task rules. Held.

## T4 Full Check

`make check`, with `PROSIFORM_BUILD` naming the unit checkout's `pf` and its `src/.venv/bin` first on `PATH`, exits 0: lock, lint, format, typecheck, `make test` (2261 passed), harness (1106 passed), corpus (667 fixtures, 667 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
