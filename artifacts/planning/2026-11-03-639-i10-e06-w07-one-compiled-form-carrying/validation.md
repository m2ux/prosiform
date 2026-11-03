# Validation

The checks W07's work item names, run against task branch `i10/e06/w07-one-compiled-form-carrying` at `f3758e5a`, on a base holding W00 to W05 and W08.

## T1 Claude Shell Limited To pf

`test_a_claude_session_given_pf_carries_a_shell_limited_to_pf` in `evals/diagram-following/test_harness.py`: a Claude session given `pf` has `--tools Read,Write,Edit,Glob,Grep,Task,Bash` and `--allowedTools Bash(pf:*)`; one not given it has neither. `test_claude_reads_the_shell_commands_a_session_ran` reads a session's `pf` command from its `Bash` call. Result: held. Observes AC12.

## T2 Compiled Session Given pf

`test_a_compiled_session_is_given_pf_and_a_shell_limited_to_it` runs the stub agent over `dispatch-chain` in the `compiled` form: every session's workspace holds `bin/pf`, its command line carries `Bash(pf:*)`, and its transcript holds the `pf` command. `test_each_session_starts_in_a_fresh_workspace_of_its_form_and_inputs` holds the default matrix: a session carries the shell exactly where its workspace holds `bin/pf`. Result: held. Observes AC12.

## T3 pf Bare And A Composition Line

`test_a_compiled_session_runs_pf_bare_and_compiles_a_composition_line` prepares a `compiled` workspace, runs its `bin/pf` bare, which prints the guide, and compiles a document holding a `↳` line, whose bundle carries the composed section. Result: held. Observes AC12.

## T4 README States One Compiled Form

`test_the_page_states_one_compiled_form_carrying_the_run_pf_line` reads the README's forms table: one `compiled` row stating the run-pf line, the build as `pf` and a shell limited to `pf`, and neither `staged` nor `Prosiform section` appears on the page. `test_the_readme_states_every_form_the_runner_offers_and_its_default` holds the table to the runner's forms. Result: held. Observes AC13.

## T5 staged Refused

`test_a_run_naming_the_staged_form_is_refused_as_an_unknown_form`: `--forms staged` raises `unknown form staged` before any session starts. Result: held. Observes AC18.

## T6 Make Check

`make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`: harness 1299 passed, which carries the corpus test; lint, format, types, corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence: ok.
