# I05:E07:W01 Validation

Each check the work item's Test row names, in execution order, with the revision it ran on and what it observed.

- **Branch.** `i05/e07/w01-dispatch-scenarios-in-both`, cut from `i05/e07/main` at `4848cfdc7537d180b014b9d821c206dbb0cdd26f`.
- **Tested revision.** `b108a545` for every check below.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`, `src/.venv/bin/pf`, version `0.15.0 (skill-markdown-v4)`.
- **Corpus.** `evals/diagram-following/workflows/dispatch-chain`, `dispatch-set`, `dispatch-beside` and `dispatch-question`, each in a `compiled/` and an `authored/` form.

## T1 AC1 — both forms bundle clean

Each dispatch scenario's compiled form and its authored-protocol form bundle with `pf` at exit 0 and report no diagnostic, as a test `make check` runs shows.

| Test | Observes |
| --- | --- |
| `test_workflow.py::test_each_dispatch_scenario_bundles_clean_in_both_its_forms` | AC1: for each of the four workflows and each of its two forms, `pf workflow.md` exits 0, writes nothing to stderr, and publishes the entry's bundle. Four workflows × two forms, eight assertions. |
| `test_workflow.py::test_each_form_bundles_cleanly_carrying_every_state` (dispatch rows) | AC1: the same eight runs, held to the entry bundle carrying every state's section, and to the compiled form publishing a bundle for each document its steps dispatch. |
| `test_workflow.py::test_each_dispatch_form_states_steps_naming_their_targets` (dispatch rows) | AC1: every step a dispatch form writes resolves to a document of the same form holding the heading it names, and a set names more than one target. |
| `test_workflow.py::test_each_scenario_path_is_the_walk_its_inputs_determine` (dispatch rows) | AC1 and the epic's scenario rule: each scenario's path is the walk all its forms lead through, and its trace is the `[section, set]` pairs the compiled and authored sources state. |
| `test_score.py::test_a_run_walking_its_scenario_path_with_every_action_passes` (dispatch rows) | A hand-made trace of a dispatch scenario's path with every action done passes, so the scorer reads the new workflows as it reads the existing ones. |

The eight `pf` runs, by hand at `b108a545`:

| Workflow | Form | Exit | Diagnostic | Bundles |
| --- | --- | --- | --- | --- |
| `dispatch-chain` | `compiled` | 0 | none | `workflow`, `plan__work`, `review__check` |
| `dispatch-chain` | `authored` | 0 | none | `workflow` |
| `dispatch-set` | `compiled` | 0 | none | `workflow`, `review__source`, `review__tests` |
| `dispatch-set` | `authored` | 0 | none | `workflow` |
| `dispatch-beside` | `compiled` | 0 | none | `workflow`, `plan__work`, `review__source`, `review__tests` |
| `dispatch-beside` | `authored` | 0 | none | `workflow` |
| `dispatch-question` | `compiled` | 0 | none | `workflow`, `draft__choose` |
| `dispatch-question` | `authored` | 0 | none | `workflow` |

## T2 AC2 — the report gives each scenario's pass rate per model and form

The report gives each dispatch scenario's pass rate per model and form, as a stub-agent test `make check` runs shows.

| Test | Observes |
| --- | --- |
| `test_run.py::test_a_dispatch_scenario_takes_a_session_in_each_of_its_forms` | AC2: each dispatch workflow takes one session in each of its forms; the session passes, its trace is its scenario's path, and its record carries the scenario's dispatch trace. Eight rows. |
| `test_run.py::test_the_report_gives_each_dispatch_scenarios_pass_rate_per_model_and_form` | AC2: a run of two models over the four dispatch scenarios in both forms, two repetitions each, starts `2 × 4 × 2 × 2 = 32` sessions. The report holds one cell per model, form, workflow and scenario — sixteen cells — each reading two sessions, two passes and a pass rate of one, and the Markdown report prints each cell's `100%`. |
| `test_run.py::test_a_compiled_form_gives_its_whole_bundle_set` | AC2's material: a session in the compiled form reaches its workspace with the entry bundle and every bundle its dispatching bundle names, which is what makes its pass rate measurable. |

No paid session ran: every session above starts [`stub_agent.py`](https://github.com/m2ux/prosiform/blob/b108a545/evals/diagram-following/stub_agent.py) in place of the agent.

## T3 The reader holds the trace to the source

The scenario names the trace, and the trace is a walk of the bundle set its source produces.

| Test | Observes |
| --- | --- |
| `test_workflow.py::test_the_dispatch_scenarios_are_the_chain_the_set_the_pair_and_the_question` | The epic's four scenarios are the four the corpus holds, each naming a trace. |
| `test_workflow.py::test_a_chain_dispatches_one_target_from_each_of_two_sections` | The chain's trace is `plan#work` then `review#check`, each returning `done`. |
| `test_workflow.py::test_a_parallel_set_starts_its_second_target_beside_its_first` | The set's trace is `review#source` alone then `review#tests` beside it. |
| `test_workflow.py::test_a_set_beside_a_dispatch_states_the_dispatch_then_the_set` | The pair's trace is `plan#work`, then `review#source`, then `review#tests` beside it. |
| `test_workflow.py::test_a_returned_question_is_dispatched_again_with_the_answers` | The question's trace is `draft#choose` returning `question`, then the same section dispatched again returning `done`. |
| `test_workflow.py::test_a_dispatch_step_naming_no_document_is_a_fault`, `..._naming_no_section_is_a_fault`, `..._a_scenario_naming_no_trace_is_a_fault`, `..._a_trace_disagreeing_with_the_source_is_a_fault` | A copy of the corpus broken on purpose is held to a fault: a step naming an absent document, a step naming an absent heading, a scenario naming no trace, and a set's second target started alone. |
| `test_workflow.py::test_the_compiled_form_publishes_a_bundle_per_target_and_the_authored_none` | What the two forms separate: the compiled form publishes a set, the authored form the entry's bundle alone. |

## T4 make check

`PROSIFORM_BUILD=<pf> make check` exited 0:

- lock check, lint, format check and type check over `src/prosiform`, `src/tests`, `checks` and `evals`;
- 1302 unit tests in `src`;
- 921 harness tests over `checks/tests` and `evals/diagram-following`, up from 864 before this branch: the eval's own suite grew by the dispatch workflows' rows;
- the corpus, the installed-wheel smoke run, layout, tables, links, vocabulary, invocation, conformance, independence, steps and authoring checks.

## What this unit does not claim

- **AC3** is W02's: the scorer's four dispatch checks, each with a class of its own, and the stub agent emitting sub-agent starts. This branch records each scenario's trace beside the verdict and leaves the scoring of a dispatch trace to W02.
- **AC4** is W03's: the first baseline of the dispatch scenarios, which spends money and starts only on the user's approval.
- **No baseline moved.** `baseline.json` and `report.md` are untouched, and every baseline cell is a `linear`, `branching` or `looping` workflow the dispatch scenarios do not join.
