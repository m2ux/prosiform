# Validation — I10:E04 W19

Every check ran in the unit's worktree, at the task branch's head, with the stub agent and the build `make harness` uses; no paid agent session ran.

| Item | Value |
| --- | --- |
| Branch | `i10/e04/w19-the-edge-corpus-test` |
| Tested revision | `68f78edb` |
| Command | `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` |

## Epic Base Update

Before the task branch, `origin/main` (`11a87291`, I10:E06 merged) was merged into `i10/e04/main` as `7ab77824`. The merge folds `staged` into `compiled` on E04's side: a compiled session receives the compiled sources, the bundle set in the folder `pf` writes it to, the build as `pf` and a shell limited to `pf`; E04's per-start command reading, stated runs and run classes apply to `compiled`; `staged`, `runnable()` and `Harness.shell()` are gone; each `staged/` tree moved to `compiled/`, `dispatch-set`'s duplicate dropped. The default matrix grows to 78 cells (780 sessions), so `EVAL_BUDGET_TOKENS` is 46 800 000. The README keeps main's design pin.

The merge was pushed with named failures: the corpus and runner tests bundling the edge workflows, whose sources still wrote the retired marks, and the README test finding the retired Prosiform section. This unit fixes every one of them; T6 shows the whole check passing.

## Checks

### T1 No source writes a retired mark

`make harness`, `test_workflow.py`: `test_no_edge_workflow_source_writes_a_retired_mark` scans every workflow source for `¬⇉`, `¬⫽`, `[→](` and `[¬→](` and finds none; the workflows writing `↳ ` are `conditional-composition`, `deferred-composition`, `deferred-dispatch`, `directive-labels`, `preset-deferral` and `subagent-first-run`. Before the rewrite, `pf` refused eleven links across those sources with `E_UNSUPPORTED_CONSTRUCT`. Passed.

### T2 Every compiled workflow bundles and states its walk

`make harness`, `test_workflow.py`: `test_each_form_bundles_cleanly_carrying_every_state` bundles every compiled workflow with the build under test at exit 0 with no undeclared diagnostic; `test_each_compiled_scenario_states_the_runs_and_path_its_bundles_state` walks each compiled scenario's entry bundle, runs `pf` on each `↳` line a step reaches, and finds the stated path and session runs, for the four dispatch workflows and the eight edge workflows alike. Passed.

### T3 Each dispatched bundle held to the run-pf line and its links

`make harness`, `test_workflow.py`: `test_each_compiled_sub_agent_states_the_actions_its_runs_compile` compiles each bundle a scenario's trace follows, from the entry's set or a run on a `↳` line, and finds each opening with the run-pf line, each `⇉` link in any bundle written, inline or as an `In parallel` item, naming a file that run wrote, and each followed bundle named by a `⇉` link. `deep-hop-runs` reaches the ruling's bundle through the `⇉` link in the bundle the review's `pf steps/weighing.md#weigh` writes. Passed.

### T4 The set's In parallel items and the failing opening

`make harness`, `test_workflow.py`: `test_a_set_publishes_parallel_items_linking_bundles_opening_with_the_run_pf_line` finds `dispatch-set`'s `In parallel` section linking `review__source.bundle.md` and `review__tests.bundle.md`, each opening with the run-pf line, and `dispatch-chain`'s inline `⇉` link naming `plan__work.bundle.md`. `test_a_dispatched_bundle_opening_without_the_run_pf_line_is_a_fault` holds the same set to another opening and finds both members reported. Passed.

### T5 The former staged scenarios run in compiled

`make harness`: `test_run.py::test_a_run_gives_each_harness_the_compiled_scenarios_its_stream_reports` gives Claude every compiled scenario, the nested ones among them; `test_a_compiled_claude_run_scores_each_nested_scenario_on_its_starts_runs` runs the stub agent over `dispatch-depth` and `subagent-first-run` in `compiled` and scores all five cells a pass, the review's and the ruling's runs under their own starts; `test_readme.py::test_the_page_states_one_compiled_form_carrying_the_run_pf_line` finds one `compiled` form and no `staged` or Prosiform section in the README. Passed.

### T6 make check

The whole repository check, at the tested revision, exits 0; `make harness` runs 1483 tests. Passed.

## Review

Each edge criterion AC6–AC18 keeps its scenario: no scenario retires. `deferred-dispatch` keeps both scenarios, its dispatch now reached through a deferred composition of the section that dispatches.

## Findings

- **A compiled session needs the sources.**
  A `↳` line names its target from the sources, so a bundle set alone cannot compile one. The fold gives the compiled workspace the sources beside the bundle set, which every compiled session, the four dispatch workflows' included, now receives. Held for the user; see the change list.
- **The edge workflows join the default matrix.**
  With one compiled form, the default `--forms` reaches every edge workflow, so the baseline's matrix grows from 60 to 78 cells. Held for the user.
- **Section lookup by slug.**
  A source's `¬↳` naming `#read-mirror` failed the reader's heading lookup, which compared the fragment to the heading text; the reader now matches a heading by its slug.
