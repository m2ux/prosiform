# I10 criterion verification

## Decision

On 2026-11-05 the user selected: "Reconcile with delivered behavior" for I10 and its open Composition Following epic, preserving task IDs and checking affected completion ticks.

## E04 delivered revision

- Revision: `1076ef5293c0da74163d1289adf56ab0ef8cfbb0`, the merge of PR #651 into `i10/e04/main`.
- Instrument: `make harness`, using the existing locked-environment Python interpreter with the detached checkout's `src` first on `PYTHONPATH`. The same interpreter's command directory supplies `pf`, which imports that checkout's source.
- Checkout: a temporary detached worktree created and removed by `revision-check.py`.
- Result: **1482 passed, 1 skipped**, exit 0, in 167.33 seconds.
- The skip is `checks/tests/test_layout.py`'s absent-build-environment case. It does not cover a changed criterion.
- The suite uses stub agents and starts no paid model session.

### Changed criteria

| Criteria | Observing tests |
| --- | --- |
| AC2, AC3 | `test_a_compiled_session_receives_its_sources_the_bundle_set_and_the_build`, `test_a_compiled_session_is_given_pf_and_a_shell_limited_to_it`, `test_a_run_gives_each_harness_the_compiled_scenarios_its_stream_reports` |
| AC7 | Conditional and nested deferral corpus scenarios, including their required and forbidden compile runs |
| AC10, AC11 | `test_a_state_composed_under_a_conditional_step_is_entered_where_it_holds`, `test_a_composed_state_entered_off_its_condition_is_a_fault`, `test_a_footnote_opens_its_target_and_a_composition_composes_in_place` |
| AC13 | `test_a_deferred_dispatch_is_compiled_where_reached_and_its_bundle_dispatches`, `test_a_deferred_dispatch_stated_off_its_walk_is_a_fault` |
| AC17, AC18 | The first-hop and deep-hop corpus cases and `test_each_compiled_sub_agent_states_the_actions_its_runs_compile` |
| AC26 | `test_a_compiled_claude_run_scores_each_nested_scenario_on_its_starts_runs` |
| AC27 | `test_no_edge_workflow_source_writes_a_retired_mark` |
| AC28 | Compiled scenario admission and `test_a_run_naming_the_staged_form_is_refused_as_an_unknown_form` |
| AC29 | `test_each_compiled_sub_agent_states_the_actions_its_runs_compile`, `test_a_set_publishes_parallel_items_linking_bundles_opening_with_the_run_pf_line`, `test_a_dispatched_bundle_opening_without_the_run_pf_line_is_a_fault` |

The changed completed criteria retain their ticks after this passing verification. AC28 and AC29 isolate conditions already delivered and tested by W19; its Coverage is AC27, AC28 and AC29. AC21 remains unticked because the live-run results it documents do not exist.

## Merged guide revision

- Revision: `ba93ca60860f0dc46722f27acd471740465279da`, current merged `main`.
- Instrument: the existing `src/tests/test_cli.py` tests `test_a_bare_command_prints_the_guide`, `test_the_guide_states_each_rule_an_agent_follows_a_bundle_by` and `test_the_guide_is_plain_text`, in a temporary detached checkout.
- Result: **3 passed**, exit 0.
- I10 AC16 states the marks and dispatch-set subsection the guide currently describes; it requires no returned-question marker. Its tick retains verified evidence.

## Merged bundle opening

At the same merged main revision, the existing tests `test_every_bundle_opens_with_the_run_pf_line`, `test_a_bundle_dispatching_nothing_opens_with_the_run_pf_line` and `test_a_dispatched_bundle_carrying_a_deferral_opens_with_the_run_pf_line` all pass in a detached checkout: **3 passed**, exit 0. [Console output](test-opening.txt).

Their expected complete outputs place the generated `§ Instructions` heading before the run-pf instruction and selected source content, with no generated per-bundle dispatch protocol. I10 AC17 states the instruction before source content; AC18 separately states the absence of a generated dispatch protocol. Both have verified evidence and pass the initiative readiness gate against completed E06. E04 AC29 states the run-pf instruction before source content without requiring it to be the bundle's first bytes; its delivered corpus tests also observe that condition.

## Revision boundary

E04's base still carries the guide wording and `In parallel` heading from its integration of E06. Merged `main` carries the fixed `⫽ Dispatch Set` heading, the `§ Instructions` opening and a guide with no question marker. Passing E04's tests does not establish that its base includes these later changes. W16's analysis reads the merged guide before the shakedown, and base integration and new test results remain necessary before epic completion.

The guide's description still names a section-derived dispatch-set heading, while `src/prosiform/dispatch.py` declares the fixed heading. The three guide tests check its printed text, so their pass does not prove agreement with the emitter. This integration finding remains in the source review.

No live edge run, shakedown or new baseline is claimed by this verification.
