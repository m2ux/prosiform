# Diagram-Following Report: agent-pick

- **Run:** `agent-pick`, 2026-11-12T12:43:01+00:00; models `openrouter/deepseek/deepseek-v4.1-flash-1017`; 5 repetitions.
- **Sessions:** 20 of 20 started; 0 not started.
- **Tokens:** 5037116.
- **Managed configuration:** none.
- **Cost:** USD 0.158708.
- **Baseline:** `baseline`, 2026-11-05T05:49:46+00:00. Change is this run's pass rate less the baseline's, and a failure count's change follows it in brackets.

## By Model

| Model | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | 20 | 0 | 0% | -95 pts | undispatched 0 (-19), uncompiled 1 (+1), overcompiled 4 (+4), read_source 15 (+15) | 0 | 251856 | 0.007935 |

## By Model and Form

| Model | Form | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `compiled` | 20 | 0 | 0% | -73 pts | undispatched 0 (-4), uncompiled 1 (+1), overcompiled 4 (+4), read_source 15 (+15) | 0 | 251856 | 0.007935 |

## By Model, Form and Scenario

| Model | Form | Workflow | Scenario | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `compiled` | `agent-pick` | `epic-picked` | 5 | 0 | 0% | new | read_source 5 | 0 | 237362 | 0.010276 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `compiled` | `agent-pick` | `initiative-picked` | 5 | 0 | 0% | new | overcompiled 2, read_source 3 | 0 | 278327 | 0.007729 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `compiled` | `agent-pick` | `task-picked` | 5 | 0 | 0% | new | uncompiled 1, overcompiled 1, read_source 3 | 0 | 279648 | 0.006756 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `compiled` | `agent-pick` | `unknown-kind-held` | 5 | 0 | 0% | new | overcompiled 1, read_source 4 | 0 | 212086 | 0.006981 |

## Baseline Only

- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `authored`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `linked`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `prose`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `authored` / `dispatch-beside` / `set-beside-a-dispatch`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `authored` / `dispatch-question` / `returned-question`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `authored` / `dispatch-set` / `parallel-set`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `branching` / `high-severity`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `branching` / `low-severity`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `declared-inclusion` / `declared-link-followed`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `declared-inclusion` / `undeclared-link-as-text`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `group-placement` / `leaf-group`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `group-placement` / `nested-intermediate`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `group-placement` / `two-presets-one-document`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `linear` / `straight-through`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `looping` / `no-rework`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `looping` / `two-rounds`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `preset-selection` / `default-alone`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `preset-selection` / `title-selected`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `preset-selection` / `two-presets-one-title`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `pricing` / `clear-discount`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `pricing` / `flagged-list-price`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `rework` / `four-rounds`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `rework` / `one-round`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `section-composition` / `deferred-occurrence`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `section-composition` / `merged-sources`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `section-composition` / `nested-composition`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `section-entry` / `document-fragment`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `subst-redirect` / `document-redirect`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `subst-redirect` / `preset-over-default`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle` / `subst-redirect` / `section-redirect`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `compiled` / `dispatch-beside` / `set-beside-a-dispatch`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `compiled` / `dispatch-question` / `returned-question`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `compiled` / `dispatch-set` / `parallel-set`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `linked` / `branching` / `high-severity`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `linked` / `branching` / `low-severity`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `linked` / `linear` / `straight-through`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `linked` / `looping` / `no-rework`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `linked` / `looping` / `two-rounds`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `linked` / `pricing` / `clear-discount`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `linked` / `pricing` / `flagged-list-price`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `linked` / `rework` / `four-rounds`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `linked` / `rework` / `one-round`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `prose` / `branching` / `high-severity`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `prose` / `branching` / `low-severity`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `prose` / `linear` / `straight-through`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `prose` / `looping` / `no-rework`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `prose` / `looping` / `two-rounds`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `prose` / `pricing` / `clear-discount`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `prose` / `pricing` / `flagged-list-price`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `prose` / `rework` / `four-rounds`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `prose` / `rework` / `one-round`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `branching` / `high-severity`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `branching` / `low-severity`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `declared-inclusion` / `declared-link-followed`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `declared-inclusion` / `undeclared-link-as-text`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `group-placement` / `leaf-group`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `group-placement` / `nested-intermediate`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `group-placement` / `two-presets-one-document`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `linear` / `straight-through`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `looping` / `no-rework`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `looping` / `two-rounds`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `preset-selection` / `default-alone`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `preset-selection` / `title-selected`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `preset-selection` / `two-presets-one-title`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `pricing` / `clear-discount`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `pricing` / `flagged-list-price`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `rework` / `four-rounds`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `rework` / `one-round`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `section-composition` / `deferred-occurrence`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `section-composition` / `merged-sources`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `section-composition` / `nested-composition`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `section-entry` / `document-fragment`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `subst-redirect` / `document-redirect`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `subst-redirect` / `preset-over-default`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `tree` / `subst-redirect` / `section-redirect`

## Failing Sessions

| Session | Class | Disposition | Evidence |
| --- | --- | --- | --- |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/epic-picked/compiled/1` | `read_source` | miss | the transcript's read calls open reference/work-kind.md, workflow.md, states/classify.md, sources of the compiled form; its runs pass the run checks, the rerun naming epic, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/epic-picked/compiled/2` | `read_source` | miss | the transcript's read calls open reference/work-kind.md, workflow.md, states/classify.md, reference/kind.md, reference/breakdown.md, states/breakdown.md, reference/charter.md, reference/change.md, reference/hold.md, states/entry.md, states/exit.md, sources of the compiled form; its runs pass the run checks, the rerun naming epic, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/epic-picked/compiled/3` | `read_source` | miss | the transcript's read calls open reference/work-kind.md, workflow.md, reference/kind.md, reference/breakdown.md, reference/charter.md, reference/change.md, reference/hold.md, states/classify.md, states/entry.md, states/exit.md, states/breakdown.md, states/charter.md, states/change.md, states/hold.md, sources of the compiled form; its runs pass the run checks, the rerun naming epic, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/epic-picked/compiled/4` | `read_source` | miss | the transcript's read calls open reference/work-kind.md, reference/kind.md, reference/charter.md, reference/change.md, reference/breakdown.md, reference/hold.md, workflow.md, states/entry.md, states/classify.md, states/charter.md, states/breakdown.md, states/change.md, states/hold.md, states/exit.md, sources of the compiled form; its runs pass the run checks, the rerun naming epic, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/epic-picked/compiled/5` | `read_source` | miss | the transcript's read calls open workflow.md, reference/work-kind.md, reference/kind.md, reference/charter.md, reference/breakdown.md, reference/change.md, reference/hold.md, states/entry.md, states/classify.md, states/charter.md, states/breakdown.md, states/change.md, states/hold.md, states/exit.md, sources of the compiled form; its runs pass the run checks, the rerun naming epic, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/initiative-picked/compiled/1` | `read_source` | miss | the transcript's read calls open reference/work-kind.md, sources of the compiled form; its runs pass the run checks, the rerun naming initiative, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/initiative-picked/compiled/2` | `read_source` | miss | the transcript's read calls open workflow.md, reference/work-kind.md, reference/kind.md, reference/charter.md, reference/breakdown.md, reference/hold.md, reference/change.md, states/classify.md, states/entry.md, states/exit.md, sources of the compiled form; its runs pass the run checks, the rerun naming initiative, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/initiative-picked/compiled/3` | `read_source` | miss | the transcript's read calls open reference/work-kind.md, reference/kind.md, states/classify.md, workflow.md, states/charter.md, states/exit.md, sources of the compiled form; its runs pass the run checks, the rerun naming initiative, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/initiative-picked/compiled/4` | `overcompiled` | miss | the transcript's shell calls run pf on workflow.md, reference/work-kind.md without its fragment, states/classify.md and states/classify.md --presets initiative, none of which the bundle states on the path; it also made the listing and the rerun with initiative and traced the scenario's path |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/initiative-picked/compiled/5` | `overcompiled` | miss | after the stated listing the transcript's shell calls run pf reference/kind.md --presets change and reference/work-kind.md#route --presets change, a transition's label rather than an alternative, before the rerun with initiative; the bundle states neither run |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/task-picked/compiled/1` | `read_source` | miss | the transcript's read calls open workflow.md, states/entry.md, states/classify.md, states/charter.md, states/breakdown.md, states/change.md, states/hold.md, states/exit.md, reference/work-kind.md, reference/charter.md, reference/change.md, reference/breakdown.md, reference/kind.md, reference/hold.md, sources of the compiled form; its runs pass the run checks, the rerun naming task, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/task-picked/compiled/2` | `read_source` | miss | the transcript's read calls open workflow.md, reference/work-kind.md, states/classify.md, states/entry.md, states/exit.md, reference/kind.md, sources of the compiled form; its runs pass the run checks, the rerun naming task, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/task-picked/compiled/3` | `uncompiled` | miss | the bundle's Classify states a ↳ Route line deferring reference/work-kind.md#route with title ? on the path; the transcript's shell calls make only the rerun with task, never the listing with ?, after its read calls opened reference/work-kind.md, the router's source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/task-picked/compiled/4` | `overcompiled` | miss | the transcript's shell calls run pf workflow.bundles/workflow.bundle.md, pf workflow.md, pf . and pf --presets x before the stated listing and rerun with task; the bundle states none of those references |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/task-picked/compiled/5` | `read_source` | miss | the transcript's read calls open workflow.md, reference/work-kind.md, reference/kind.md, sources of the compiled form; its runs pass the run checks, the rerun naming task, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/unknown-kind-held/compiled/1` | `read_source` | miss | the transcript's read calls open reference/work-kind.md, reference/kind.md, reference/charter.md, reference/hold.md, reference/breakdown.md, reference/change.md, sources of the compiled form; its runs pass the run checks, the rerun naming other, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/unknown-kind-held/compiled/2` | `overcompiled` | miss | between the stated listing and the rerun with other, the transcript's shell calls run pf states/classify.md, a reference the bundle states on no line of the path |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/unknown-kind-held/compiled/3` | `read_source` | miss | the transcript's read calls open reference/work-kind.md, reference/kind.md, workflow.md, states/classify.md, states/hold.md, reference/hold.md, reference/change.md, reference/charter.md, reference/breakdown.md, sources of the compiled form; its runs pass the run checks, the rerun naming other, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/unknown-kind-held/compiled/4` | `read_source` | miss | the transcript's read calls open workflow.md, reference/work-kind.md, reference/charter.md, reference/change.md, reference/kind.md, reference/breakdown.md, reference/hold.md, states/entry.md, states/classify.md, states/charter.md, states/breakdown.md, states/change.md, states/hold.md, states/exit.md, sources of the compiled form; its runs pass the run checks, the rerun naming other, and it traced the scenario's path, and the instruction names no source |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/agent-pick/unknown-kind-held/compiled/5` | `read_source` | miss | the transcript's read calls open reference/work-kind.md, states/classify.md, states/entry.md, reference/kind.md, states/charter.md, states/breakdown.md, states/change.md, states/hold.md, states/exit.md, sources of the compiled form; its runs pass the run checks, the rerun naming other, and it traced the scenario's path, and the instruction names no source |
