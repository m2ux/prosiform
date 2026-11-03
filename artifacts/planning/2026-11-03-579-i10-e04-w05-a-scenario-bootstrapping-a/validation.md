# Validation — I10:E04 W05–W07

Every check ran in the unit's worktree, at the task branch's head, with the stub agent and the build `make harness` uses; no paid agent session ran. The revision is the head the pull request carries when its Test Plan is recorded.

| Item | Value |
| --- | --- |
| Branch | `i10/e04/w05-a-scenario-bootstrapping-a` |
| Tested revision | `52b302e1` |
| Command | `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` |

## Checks

### T1 A skill's line bootstrapped

`make harness`, `test_workflow.py`: `test_each_bootstrap_scenario_states_the_guide_its_line_and_the_walk` reads each bootstrap skill's one `↳` line, holds its title to the heading of the document it names and each scenario's runs to bare `pf` then `pf` on the line's path, and for `inline-bootstrap` compiles `sources/workflow.md` from the skill's directory and walks the bundle it writes to `Freeze`, `Tag`, `Broadcast` and `Freeze`, `Backport`, `Broadcast`, each scenario's path; `test_a_skill_entry_declaring_nothing_holds_its_line_as_written` finds `inline-bootstrap`'s `SKILL.md` declaring no `prosiform` and holding `[↳ Release](sources/workflow.md)`; `test_a_skill_line_its_scenario_does_not_compile_is_a_fault` refuses a line titled other than its document is headed; `test_a_bootstrap_scenario_omitting_the_guide_is_a_fault` refuses a scenario stating `pf sources/workflow.md` without bare `pf` first. Passed.

### T2 A conditional deferral run where its step holds

`make harness`, `test_workflow.py`: `test_each_staged_scenario_states_the_runs_and_path_its_bundles_state` compiles `deferred-composition`'s entry bundle, whose `Relocate` holds `[↳ Steps](reference/migration.md#steps)` beneath a step reading `scope.txt`, and finds `deferral-reached`, reading `large`, running `pf` on that line and `deferral-passed`, reading `small`, running none, each scenario stating exactly those runs; `test_a_conditional_deferral_is_run_where_its_step_holds_and_nowhere_else` reads the four scenarios' stated runs; `test_a_run_on_a_line_the_path_does_not_reach_is_a_fault` refuses `deferral-reached` stating the migration's run once its input no longer reaches the line. Passed.

### T3 A nested deferral run where its path needs it

`make harness`, `test_workflow.py`: the staged walk compiles `reference/migration.md#steps`, whose bundle holds `[↳ Steps](reference/archive.md#steps)` beneath a step reading `history.txt`, and finds `nested-needed`, reading `kept`, running the archive's line after the migration's, and `deferral-reached`, reading `dropped`, and `nested-unreached`, whose migration bundle is never compiled, running no archive run; `test_a_run_on_a_line_the_path_does_not_reach_is_a_fault` refuses `nested-needed` stating the archive's run once its step no longer holds. Passed.

### T4 A deferral under matched presets walks the stand-in

`make harness`, `test_workflow.py`: the staged walk compiles `preset-deferral`'s entry bundle, where `Mirror` holds `[↳ Read mirror](reference/fetch.md#read-mirror)` and writes no transition of its own, runs `pf` on that line under `fetch.md`'s `mirror` preset, which both headings select, and reads the stand-in `cache.md`'s transition, `stored`, so the walk is `Solicit`, `Mirror`, `Restore`, the scenario's path; `test_a_preset_deferral_states_the_stand_ins_path` reads that path, the one stated run and `Mirror`'s deferred transition; `test_the_real_target_of_a_preset_deferral_leads_elsewhere` drops the preset's `subst` and finds the walk leading to `Serve` instead. Passed.

### T5 One class for a missed bootstrap run

`make harness`: the scorer names no `unbootstrapped` class and the runner passes no compiled flag; `test_score.py`'s run checks hold a session making no stated run to `uncompiled`, which a bootstrap scenario's stated bare `pf` and line run reach. Passed.

### T6 make check

The whole repository check, at the tested revision, exits 0. Passed.

## Findings

- **A deferred transition needs a labelled sentence.**
  The diagram form's transitions name a label only beside a condition, so the material a deferral activates states its one edge as "Take the transition labelled `<label>`.", which the walk of a bundle reads; a state document's own transition is held to the existing sentences.
- **The design pin was unreachable in CI.**
  The first CI run, at `29e0dfd7`, failed `test_catalogue.py` because the README's badge named `682cdf7e`, a commit the rewritten engineering history holds on no branch; the base's own head fails the same way. The branch repins it to `2921f91a`, whose `design.md` is identical, and `make check` passes at `52b302e1`.
- **The triage rubric is not on this base.**
  `RUNBOOK.md` arrives with I10:E05 W00, so the removal of `unbootstrapped` from its rubric is W17's to make.
