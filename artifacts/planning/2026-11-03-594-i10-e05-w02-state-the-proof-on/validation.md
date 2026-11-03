# Validation: I10:E05 W02

Run in the task worktree on branch `i10/e05/w02-state-the-proof-on`, with `PROSIFORM_BUILD` naming the worktree's own `pf`.

## T1 Table names each proved scenario

`test_the_feature_table_names_each_workflow_and_scenario_the_proof_runs` compares the table's workflow and scenario pairs with the cells of `mvp-proof.json`. Result: passed. Observes AC4.

## T2 Table names each declared scenario

`test_the_feature_table_names_each_scenario_its_workflow_declares` compares the table with the `scenarios.toml` of each workflow it names. Result: passed. Observes AC4.

## T3 Stated cost matches the file

`test_the_proof_section_states_the_cost_the_file_records` reads `cost_usd` and `sessions` from `mvp-proof.json` and finds them in the proof section. Result: passed, with USD 0.67671 and 150 sessions. Observes AC5.

## T4 Tables

`make tables`, run within `make check`. Result: passed.

## T5 Links

`make links`, run within `make check`. Result: passed.

## T6 Full check

`make check` before opening and before merging. Result: passed.
