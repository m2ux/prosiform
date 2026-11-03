# Validation — I10:E04 W10–W12

Every check ran in the unit's worktree, at the task branch's head, with the stub agent and the build `make harness` uses; no paid agent session ran. The revision is the head the pull request carries when its Test Plan is recorded.

| Item | Value |
| --- | --- |
| Branch | `i10/e04/w10-a-scenario-compiling-a` |
| Tested revision | `00fd112c` |
| Command | `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` |

## Checks

### T1 A deferred dispatch compiled where its step reaches it

`make harness`, `test_workflow.py`: `test_a_deferred_dispatch_is_compiled_where_reached_and_its_bundle_dispatches` finds the staged entry bundle carrying `[¬⇉ the loading crew]` as the plain link `reference/loading.md#crew` with no mark left, `deferred-dispatch-compiled`, reading `bulk`, stating `pf reference/loading.md#crew` and the trace `reference/crew#lift`, `reference/crew#strap`, both started by the session, and `deferred-dispatch-passed`, reading `single`, stating no run and no trace; `test_a_deferred_dispatch_stated_off_its_walk_is_a_fault` refuses the passed scenario reaching the link and the compiled one stating no run. `test_each_staged_scenario_states_the_runs_and_path_its_bundles_state` holds both to the staged walk. `test_run.py`: `test_a_harness_reporting_only_the_sessions_starts_gets_those_scenarios` gives Cursor the compiled scenario, whose starts are the session's own. Passed.

### T2 A chain three hops deep

`make harness`, `test_workflow.py`: `test_a_three_hop_chain_starts_each_hop_in_order_with_no_depth_warning` compiles `dispatch-depth`'s staged set with an empty stderr, no `W_DISPATCH_DEPTH` among it, and finds `three-hop-chain`'s starts `line/scope#frame`, `line/detail#expand`, `line/tally#count` at depths 0, 1, 2, each `done`; `test_a_hop_missing_from_a_deep_trace_is_a_fault` refuses the trace with its third hop dropped. Passed.

### T3 A set at the second hop

`make harness`, `test_workflow.py`: `test_a_set_three_hops_deep_starts_together_before_the_chain_goes_on` finds `fan/east#east` and `fan/west#west` started together at depth 1, ahead of `fan/join#join` and `fan/seal#seal` at depth 2, the trace stating that walk, each `done`. Passed.

### T4 A question returned from the third hop

`make harness`, `test_workflow.py`: `test_a_question_three_hops_deep_is_relayed_and_the_chain_dispatched_again` finds `three-hop-question`'s trace `ask/enquiry#pose`, `ask/probe#probe`, `ask/choice#elect` each returning `question`, then the same chain, dispatched again from `Resume`, each returning `done`, at depths 0, 1, 2 twice. Passed.

### T5 A first-hop sub-agent's pf run shown by its action

`make harness`, `test_workflow.py`: `test_a_first_hop_bundle_runs_pf_first_and_its_line_states_its_action` finds `hop_ledger__balance.bundle.md` opening with the line referring to `Run pf first` above `# Prosiform`, carrying `[↳ Close](steps/closing.md#close)`, and `first-hop-run` stating `closing.txt` = `closed` for the ledger; `test_each_staged_sub_agent_states_the_actions_its_runs_compile` compiles the line and holds the stated action to the material's; `test_a_sub_agent_action_its_runs_do_not_alone_state_is_a_fault` refuses a stated value the material does not state and an action the bundle itself states. `test_score.py`: `test_a_sub_agent_running_no_pf_on_its_line_misses_its_action[first-hop-run]` fails a record with every start and state action but no `closing.txt` as `missing_action`, and passes it once the file is written. Passed.

### T6 Second- and third-hop sub-agents' pf runs shown by their actions

`make harness`, `test_workflow.py`: `test_each_deep_hop_carrying_a_line_states_the_action_its_run_compiles` finds `deep-hop-runs`' starts `hop/audit#sweep`, `hop/review#scan`, `steps/ruling#rule` at depths 0, 1, 2, the review stating `weighing.txt` from its deferred dispatch's material and the ruling `ruling.txt` from its `↳` line's; `test_each_staged_sub_agent_states_the_actions_its_runs_compile` compiles the review's bundle, the weighing its deferred dispatch names, and the ruling's bundle that run writes, and holds both to their material. `test_score.py`: `test_a_sub_agent_running_no_pf_on_its_line_misses_its_action[deep-hop-runs]` fails the record lacking both files as `missing_action`; `test_a_sub_agent_never_started_is_undispatched_before_its_action` fails one whose ruling never started as `undispatched`. Passed.

### T7 make check

The whole repository check, at the tested revision, exits 0. Passed.

## Findings

- **The dispatch walk read no deferred dispatch.**
  A `[¬⇉]` step carries no operator `pf` compiles into the entry's set, so the walk stated no start for the deferred target's dispatches. It now follows a reached deferred dispatch to its target's own steps, and records each start's depth.
- **The runner counted only the path's own starts as a shell harness's.**
  The starts a deferred dispatch's bundle makes are the session's, so `observable` counts every start at depth 0, and Cursor and opencode are given `deferred-dispatch-compiled`.
- **A bundle of a document in a folder was matched by its last path segment.**
  `pf` names `ask/enquiry.md#pose`'s bundle `ask_enquiry__pose.bundle.md`, so the scorer's `names()` and the corpus test's bundle-set check spell a document's folders with `_`.
- **A sub-agent's nested starts reach no shell harness.**
  Neither Cursor's stream nor opencode's carries a sub-agent's own calls, and Claude runs no `staged` session, so `dispatch-depth`'s three scenarios and `deep-hop-runs` are given to no harness. Held for the user; see the change list.
