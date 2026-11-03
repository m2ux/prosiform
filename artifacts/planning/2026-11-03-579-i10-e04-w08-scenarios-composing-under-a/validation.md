# Validation — I10:E04 W08–W09

Every check ran in the unit's worktree, at the task branch's head, with the stub agent and the build `make harness` uses; no paid agent session ran. The revision is the head the pull request carries when its Test Plan is recorded.

| Item | Value |
| --- | --- |
| Branch | `i10/e04/w08-scenarios-composing-under-a` |
| Tested revision | `fa76aa0b` |
| Command | `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` |

## Checks

### T1 A state composed under a conditional step

`make harness`, `test_workflow.py`: `test_a_state_composed_under_a_conditional_step_is_entered_where_it_holds` finds `conditional-composition`'s diagram clicking no `Convert`, compiles the staged entry and finds `Convert` composed beneath `Gauge`'s `Rows`, and holds `composed-entered`, reading `large`, to `Sample`, `Gauge`, `Convert`, `Finish` and `composed-omitted`, reading `small`, to `Sample`, `Gauge`, `Finish`, each the staged walk's path; `test_a_composed_state_entered_off_its_condition_is_a_fault` refuses `composed-omitted` stating `Convert` on its path, and finds no way into `Convert` once `Gauge` links its section with a text label rather than `[→]`. Passed.

### T2 A footnote opened and an arrow read in place

`make harness`, `test_workflow.py`: `test_a_footnote_opens_its_target_and_an_arrow_composes_in_place` finds `Compose` writing `[→](../reference/style.md#rules)` and `[†](vet.md#vet)`, and the diagram clicking no `Vet`; the staged bundle places the style's rules beneath `Compose` and `Vet` as a top-level document the footnote, rewritten `[†](#vet)`, links; `footnote-opened` walks `Compose`, `Vet`, `Issue`. `test_a_path_the_footnote_does_not_open_is_a_fault` drops the footnote and finds the walk reaching no `Vet`. Passed.

### T3 A self-composed section published with its warning

`make harness`, `test_workflow.py`: `test_a_self_composed_section_warns_and_states_its_bundles_path` finds the run reporting `W_COMPOSE_SELF` alone, which the workflow declares, the composed copy of `Summary` beneath `Issue`'s `Release` beside the section it copies, and `self-composed` walking `Compose`, `Issue`, the staged walk's path; `test_a_self_composed_scenario_stating_another_path_is_a_fault` refuses the scenario stating `Vet` on its path. Passed.

### T4 make check

The whole repository check, at the tested revision, exits 0. Passed.

## Findings

- **A composed section needs a heading above it.**
  `pf` refuses a directive naming a document's top heading, so `Convert`'s action and transition sit under its `## Rows`, which `Gauge` composes; the bundle heads the placed copy `Convert` beneath `Rows`.
- **The bundle walk entered a state only by a link naming it.**
  A directive or footnote mark is labelled with one symbol, so the walk enters a state at the heading such a label links as well; `workflow.py` and the README state the rule.
- **The stub agent took a subset workflow for its superset.**
  It recognised the first workflow whose states all head a section in the workspace, so a workflow written with `looping`'s `Draft`, `Review` and `Publish` was taken for `looping`'s. It now takes the workflow holding the most such states, which `test_the_stub_recognises_the_workflow_holding_the_most_states` holds.
