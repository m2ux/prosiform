# Validation — I10:E04 W18

Every check ran in the unit's worktree, at the task branch's head, with the stub agent and the build `make harness` uses; no paid agent session ran. The revision is the head the pull request carries when its Test Plan is recorded.

| Item | Value |
| --- | --- |
| Branch | `i10/e04/w18-a-staged-claude-session` |
| Tested revision | `fb0bcad6` |
| Command | `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` |

## Checks

### T1 Only the staged form's Claude session carries a shell

`make harness`, `test_harness.py`: `test_a_staged_claude_session_carries_a_shell_and_no_other_form_does` builds the Claude command line for every corpus form; the `staged` one names `--tools Read,Write,Edit,Glob,Grep,Task,Bash` and `--allowedTools Bash(pf:*)`, every other names no `Bash` and no `--allowedTools`, and `Claude.shell(form)` holds for `staged` alone. `runnable` gives Claude `staged` and withholds `bootstrap`. Passed.

### T2 Each shell call read under the start whose sub-agent made it

`make harness`, `test_harness.py`: `test_claude_reads_each_shell_call_under_the_start_whose_sub_agent_made_it` reads a stream in which the session runs `pf reference/loading.md#crew`, the review's sub-agent runs `pf steps/weighing.md#weigh` and starts the ruling, and the ruling's sub-agent runs `pf -o out steps/recording.md#file`. `commands()` holds the session's run alone; the review's start and the ruling's start, parent 0, each hold their own. `record_calls` writes the session's command list for the `staged` form and null for `compiled`. Passed.

### T3 Each sub-agent's stated runs held to its bundle's lines

`make harness`, `test_workflow.py`: `test_each_staged_sub_agent_states_the_actions_its_runs_compile` now also holds the runs a scenario states `by` a section to the lines that section's sub-agents compile. `first-hop-run` states the ledger's `pf steps/closing.md#close`; `deep-hop-runs` the review's `pf steps/weighing.md#weigh` and the ruling's `pf steps/recording.md#file`. Before the scenarios stated them, the check reported each of the three as unstated. Passed.

### T4 A staged Claude record scored on each hop's runs

`make harness`, `test_score.py`: `test_a_staged_claude_record_holds_each_hops_runs` writes `deep-hop-runs`' record from a Claude stream three hops deep through `record_calls` for the `staged` form. The stated runs pass; the ruling also compiling `steps/closing.md#close` fails `overcompiled`; the ruling compiling nothing fails `uncompiled`. Passed.

### T5 The matrix gives Claude the nested scenarios

`make harness`, `test_run.py`: `test_a_run_gives_staged_sessions_only_when_named_to_a_shell_harness` finds Claude's staged matrix holding every scenario of every workflow written in `staged`, `three-hop-chain`, `three-hop-set`, `three-hop-question` and `deep-hop-runs` among them, and no default-form matrix holding a staged cell. `test_a_harness_reporting_no_sub_agent_command_gets_no_sub_agent_run` finds a sub-agent's stated run observable on Claude in `staged`, not in `compiled`, and on neither Cursor nor opencode. Passed.

### T6 A stub run scores each nested cell

`make harness`, `test_run.py`: `test_a_staged_claude_run_scores_each_nested_scenario_on_its_starts_runs` runs the runner, `make eval-diagrams`'s entry point, with the stub agent over `dispatch-depth` and `subagent-first-run` in `staged` on the Claude harness. It starts five sessions, each passing, the four nested scenarios among them, each given `--tools …,Bash`; `deep-hop-runs`' `subagents.json` holds the review's and the ruling's `pf` runs under their own starts and an empty session command list. Passed.

### T7 make check

The whole repository check, at the tested revision, exits 0; `make harness` runs 1441 tests. Passed.

## Findings

- **A sub-agent's unstated run reads as overcompiled.**
  With per-start commands read, the scorer holds every sub-agent's `pf` run, so a correct run of `first-hop-run` or `deep-hop-runs` would fail `overcompiled` while the scenario stated none. Both now state each sub-agent's run, and the corpus test holds them to the lines each bundle reaches.
- **`first-hop-run` leaves Cursor and opencode.**
  A scenario stating a sub-agent's run is given only to a harness reporting that sub-agent's commands (AC22), so the two shell harnesses no longer run it; Claude measures it on its start, run and action. Held for the user; see the change list.
- **Matrix counts read every form.**
  Four runner tests counted sessions over every form while running the default ones; once Claude ran `staged` the counts diverged. They count over the default forms.
