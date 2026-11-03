# Validation — I10:E04 W01–W04

Every check ran in the unit's worktree, at the task branch's head, with the stub agent and recorded transcripts `make harness` uses; no paid agent session ran. The revision is the head the pull request carries when its Test Plan is recorded.

| Item | Value |
| --- | --- |
| Branch | `i10/e04/w01-scenarios-stating-the-pf` |
| Tested revision | `cef5a2f8` |
| Command | `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` |

## Checks

### T1 Stated runs read from the corpus

`make harness`, `test_workflow.py`: `test_a_scenario_states_each_pf_run_in_order_with_its_arguments` reads `bootstrap-audit`'s two scenarios as bare `pf` then `pf sources/workflow.md`, both by the session, and `dispatch-set`'s as stating none; `test_a_sub_agents_run_is_read_by_the_section_it_follows` reads a run whose `by` names `review#tests`; `test_each_scenario_path_is_the_walk_its_inputs_determine` holds every scenario's runs to the corpus with no fault. Passed.

### T2 A stated run naming no document is refused

`make harness`, `test_workflow.py`: `test_a_stated_run_naming_no_document_of_the_sources_is_a_fault` refuses `absent.md#work` and `#source` as naming no document of the sources, and `by = "review#absent"` as a run by no start; `test_a_run_stated_by_a_workflow_running_no_command_is_a_fault` refuses a run stated by `dispatch-chain`, written in no shell form; `test_a_run_whose_fields_are_not_references_is_refused` refuses a string `args`, a non-string reference and a non-string `by`. Passed.

### T3 A staged session's workspace and path

`make harness`, `test_run.py::test_a_staged_session_receives_the_bundle_set_and_the_build`: a run of `dispatch-set` in `staged` on the Cursor harness starts one stub session whose workspace holds every bundle `pf` compiles from the staged form under `workflow.bundles/`, the same set the compiled form publishes, beside the sources; the `pf` its path resolves to is `<workspace>/bin/pf`; its instruction names `workflow.bundles/workflow.bundle.md` and says `pf` with no arguments prints the guide. Passed.

### T4 Staged sessions only where named, on a shell harness

`make harness`, `test_run.py`: `test_a_run_gives_staged_sessions_only_when_named_to_a_shell_harness` finds no staged cell in the default forms on any harness, the `dispatch-set` staged cell on Cursor and opencode when `--forms staged`, and no cell on Claude; `test_the_readme_states_every_form_the_runner_offers_and_its_default` holds the README's form table to every form and the `--forms` default, which `options` builds, to the default forms. Passed.

### T5 No sub-agent run for a harness reporting no sub-agent's commands

`make harness`, `test_run.py::test_a_harness_reporting_no_sub_agent_command_gets_no_sub_agent_run`: a scenario stating a run by `review#tests` is observable on no declared harness, is observable on an opencode harness declared to carry sub-agent calls, and a run by the session stays observable on opencode; a matrix over that scenario on opencode holds no session. Passed.

### T6 A session held to its stated runs

`make harness`, `test_score.py`: a correct walk of `dispatch-set` whose scenario states the session's bare `pf` and `pf fetch.md#implementation` and the `review#tests` sub-agent's bare `pf` and `pf net.md#retry` passes when both agents make them; omitting one, by the session or the sub-agent, fails `uncompiled`; a run on a reference no stated run names fails `overcompiled`, including on a scenario stating no run; the stated runs reversed fail `misordered_compile`; an omission beside an addition takes `uncompiled`. A bare `pf` beyond those stated passes, a reference from the workspace root names one stated from the skill's directory, a record naming no commands asks nothing, and a record failing a dispatch check takes it first. `test_each_command_splits_into_the_pf_runs_it_makes` reads runs across `&&`, `|`, `;` and `||`, past `-o`, `-d` and `--budget` and their values, and not from `echo pf` or `pfx`. Passed.

### T7 Each sub-agent's starts and commands under its section

`make harness`, `test_harness.py`: `test_claude_files_each_start_under_the_sub_agent_that_made_it` reads a recorded Claude stream three dispatches deep, with a set at the second depth and a start under the set's second member, and files each start under the index of the start whose sub-agent made it; `test_the_record_lists_each_sub_agents_starts_and_commands` writes `subagents.json` with the session's `commands` and each start's `parent` and `commands`, and reads a record holding a sub-agent's commands back under its start; `test_each_harness_declares_whether_a_sub_agents_calls_reach_its_stream` holds Claude to carrying them and Cursor and opencode to not. Passed.

### T8 make check

The whole repository check, at the tested revision, exits 0. Passed.

## Findings

- **opencode prints only its own session's parts.** The installed opencode CLI, 1.19.5, skips a `message.part.updated` event whose part's `sessionID` is not the session `run` started, and a `task` call runs its sub-agent in a child session. A sub-agent's starts and commands therefore never reach the stream, so the harness declares `sub_agent_calls` false and `dispatch-chain`'s `chain` scenario is outside the opencode matrix, as it is outside Cursor's.
- **No declared harness reports a sub-agent's commands.** Claude has no shell, and neither Cursor's stream nor opencode's carries a sub-agent's own calls, so a scenario stating a sub-agent's `pf` run is given to no harness. The record and the scorer read such runs wherever a stream reports them.
- **The triage rubric is not on this base.** `RUNBOOK.md` arrives with I10:E05 W00, so the three run classes reach its rubric in a further task.
