# Test Results

Results for W00 at `21bb235d8` on `i15/e02/w00-agent-pick-scoring-accepts`, run on 2026-11-13, `make check` with `PROSIFORM_BUILD` naming the worktree's `src/.venv/bin/pf`.

## T1 Either Path Scores as Compiled

`test_score.py::test_each_agent_pick_scenario_passes_by_either_path_and_names_it` scores a stub record for each of the four agent-pick scenarios by each path: the guide then `--pick` on the first run of the link, and the guide, the listing, then the rerun with `--pick`. Each passes with `picks` naming `first-run` or `after-listing`. The same session picking another alternative fails `uncompiled` with no path, and one reading `reference/work-kind.md` fails `read_source` with its path named. `test_an_agent_pick_session_is_held_to_its_runs_and_its_reads` keeps the existing departures: a listing with no pick is `uncompiled`, a second pick beside the stated one `overcompiled`, and a listing after the pick `misordered_compile`. Held.

## T2 Stub Sessions Through the Runner

`test_run.py::test_a_stub_run_of_each_agent_pick_scenario_passes_only_its_own_pick` runs the runner against the stub agent for every scenario, once per path (`STUB_AGENT_LISTING` set or unset), with each departure: a passing session records `picks` as `["first-run"]` or `["after-listing"]`; another kind's path fails `wrong_branch`; a source read fails `read_source`; a listing never rerun fails `uncompiled`. Held.

## T3 Scenario Shape

`test_workflow.py::test_each_agent_pick_scenario_states_its_pick_once` holds each scenario to one stated run, the link with the input's pick. The corpus walk still lists, then reruns, and `compiled_faults` holds the stated runs to the walk's runs less its listing; the two fault fixtures still name the walk's runs. Held.

## T4 Eval Harness

`make eval-harness`: 785 passed. Held.

## T5 Full Check

`make check` passes: lock-check, lint, format (491 files), typecheck (98 sources), `make test` (2137 passed), harness (1054 passed), corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
