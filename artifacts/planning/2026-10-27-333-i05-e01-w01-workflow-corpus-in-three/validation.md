# W01 Validation

**Branch:** `i05/e01/w01-workflow-corpus-in-three` at `0ec13698`, cut from `i05/e01/main` at `e111e2ad`. **Pull request:** [#335](https://github.com/m2ux/prosiform/pull/335).

Every check ran in the task worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`. The corpus tests are `evals/diagram-following/test_workflow.py`, run by `make harness`; 26 pass.

## T1 Each form bundles cleanly carrying every state

**Covers:** AC1. **Result:** ✓

`test_each_form_bundles_cleanly_carrying_every_state` runs `pf workflow.md -o -` from each of the six form directories (three workflows, diagram and prose). Each exits `0` with nothing on stderr, and each bundle carries a `# <State>` heading for every state the diagram draws, including `Check`, which `looping`'s diagram does not click and its `Revise` section links.

**Fails when broken.** `test_a_state_the_bundle_does_not_reach_is_a_fault` removes the click on `Ship` from a copy of `linear`'s diagram and gets `the diagram bundle carries no section for Ship`. The same edit to the corpus itself fails `test_each_form_bundles_cleanly_carrying_every_state[linear-diagram]` with that fault.

## T2 The forms differ only in their transitions

**Covers:** AC2. **Result:** ✓

`test_the_forms_differ_only_in_their_transitions` compares, per workflow, the two forms' state documents: the same states as the diagram, the same file names, and the same text up to the `**Next.**` paragraph; terminal in both or neither; the same condition where a state decides. The prose entry document carries no diagram.

**Fails when broken.** `test_a_prose_section_edited_beyond_its_transition_is_a_fault` changes `branching`'s prose `Queue` action content and gets `Queue: the prose section differs from the diagram's`; the same edit to the corpus fails the AC2 test for `branching`.

## T3 Each scenario path is the walk its inputs determine

**Covers:** AC3. **Result:** ✓

`test_each_scenario_path_is_the_walk_its_inputs_determine` holds each of the five scenarios (`linear` straight-through; `branching` high- and low-severity; `looping` no-rework and two-rounds): the path opens at the state `start` points at, every step is an edge the diagram draws, it ends at a state that points at `stop`, its inputs are exactly the files the conditions read, and walking either form's sections for those inputs gives the path. `test_each_section_states_the_transition_the_diagram_draws` holds each diagram section's labels to the edges leaving its state, each prose section's named states to those edges' targets, terminals to the diagram's, and each click to its state's document. `test_every_decision_is_exercised_both_ways` holds every decision to being taken both ways across its workflow's scenarios.

**Fails when broken.** `test_a_scenario_path_with_a_step_the_diagram_does_not_draw_is_a_fault` shortens `no-rework` to `Draft, Publish` and gets `the diagram draws no edge ('Draft', 'Publish')`; `test_a_scenario_path_its_inputs_do_not_lead_through_is_a_fault` gives `low-severity` the input `high` and gets a fault from each form's walk; `test_a_prose_transition_naming_another_state_is_a_fault` points `linear`'s prose `Build` at `Ship` and gets `Build: the prose names states the diagram does not`. The path edit made to the corpus itself fails the AC3 test for `looping-no-rework`.

## T4 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits `0` at `0ec13698`: lock, lint, format and typecheck (now over `evals` too), `test` (1176 passed), `harness` (687 passed, `checks/tests` and `evals/diagram-following`), `corpus`, smoke, layout (`evals/` — 42 tracked files, four trees), tables, links (the corpus documents and `instruction.md` included), vocabulary, invocation, conformance and independence.
