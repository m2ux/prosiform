# Diagram-Following Report: dispatch-brief

- **Run:** `dispatch-brief`, 2026-11-18T12:24:38+00:00; models `openrouter/deepseek/deepseek-v4.1-flash-1017`; 5 repetitions.
- **Sessions:** 20 of 20 started; 0 not started.
- **Tokens:** 3583711.
- **Managed configuration:** none.
- **Cost:** USD 0.116679.
- **Baseline:** `baseline`, 2026-11-05T05:49:46+00:00. Change is this run's pass rate less the baseline's, and a failure count's change follows it in brackets.

## By Model

| Model | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | 20 | 5 | 25% | -70 pts | undispatched 0 (-19), unstated_run 9 (+9), read_source 6 (+6) | 0 | 179186 | 0.005834 |

## By Model and Form

| Model | Form | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `briefed` | 10 | 3 | 30% | new | unstated_run 4, read_source 3 | 0 | 169894 | 0.005748 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle-set` | 10 | 2 | 20% | -53 pts | undispatched 0 (-4), unstated_run 5 (+5), read_source 3 (+3) | 0 | 188478 | 0.00592 |

## By Model, Form and Scenario

| Model | Form | Workflow | Scenario | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `briefed` | `dispatch-brief` | `ledger-brief` | 5 | 3 | 60% | new | unstated_run 2 | 0 | 164993 | 0.005909 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `briefed` | `dispatch-brief` | `payroll-brief` | 5 | 0 | 0% | new | unstated_run 2, read_source 3 | 0 | 174794 | 0.005587 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle-set` | `dispatch-brief` | `ledger-brief` | 5 | 1 | 20% | new | unstated_run 2, read_source 2 | 0 | 187364 | 0.006935 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle-set` | `dispatch-brief` | `payroll-brief` | 5 | 1 | 20% | new | unstated_run 3, read_source 1 | 0 | 189591 | 0.004904 |

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
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle-set` / `dispatch-beside` / `set-beside-a-dispatch`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle-set` / `dispatch-question` / `returned-question`
- `openrouter/deepseek/deepseek-v4.1-flash-1017` / `bundle-set` / `dispatch-set` / `parallel-set`
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
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/ledger-brief/briefed/4` | `unstated_run` | miss | the transcript's own bash calls run `pf -o /tmp/opencode/pfout 'workflow.bundles/ledger__steps.bundle.md#ledger'`, each pf on a reference no line of the form states, or with no entry as invalid usage, which the scorer reads as an unstated run; workflows/dispatch-brief/scenarios.toml states no [[scenario.run]] run, so bare pf, the guide, is the only run a correct session makes; the form's bundles carry no deferred or ↳ line and the Contract preamble's links are fragments of the bundle, so no stated line names any other reference; the agent, not the harness, made each call |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/ledger-brief/briefed/5` | `unstated_run` | miss | the transcript's own bash calls run `pf -o workflow.bundles 'workflow.md#trace'`, each pf on a reference no line of the form states, or with no entry as invalid usage, which the scorer reads as an unstated run; workflows/dispatch-brief/scenarios.toml states no [[scenario.run]] run, so bare pf, the guide, is the only run a correct session makes; the form's bundles carry no deferred or ↳ line and the Contract preamble's links are fragments of the bundle, so no stated line names any other reference; the agent, not the harness, made each call |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/ledger-brief/bundle-set/1` | `read_source` | miss | the transcript's read calls open the source documents ['ledger.md', 'states/entry.md', 'states/exit.md', 'states/receive.md', 'states/trace.md'] beside the bundles, which the form hands it as workflow.bundles/; subagents.json records the same reads |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/ledger-brief/bundle-set/2` | `read_source` | miss | the transcript's read calls open the source documents ['ledger.md', 'states/audit.md', 'states/entry.md', 'states/exit.md', 'states/receive.md', 'states/trace.md', 'workflow.md'] beside the bundles, which the form hands it as workflow.bundles/; subagents.json records the same reads |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/ledger-brief/bundle-set/4` | `unstated_run` | miss | the transcript's own bash calls run `pf -o . workflow.bundles/workflow.bundle.md`, each pf on a reference no line of the form states, or with no entry as invalid usage, which the scorer reads as an unstated run; workflows/dispatch-brief/scenarios.toml states no [[scenario.run]] run, so bare pf, the guide, is the only run a correct session makes; the form's bundles carry no deferred or ↳ line and the Contract preamble's links are fragments of the bundle, so no stated line names any other reference; the agent, not the harness, made each call |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/ledger-brief/bundle-set/5` | `unstated_run` | miss | the transcript's own bash calls run `pf .`, each pf on a reference no line of the form states, or with no entry as invalid usage, which the scorer reads as an unstated run; workflows/dispatch-brief/scenarios.toml states no [[scenario.run]] run, so bare pf, the guide, is the only run a correct session makes; the form's bundles carry no deferred or ↳ line and the Contract preamble's links are fragments of the bundle, so no stated line names any other reference; the agent, not the harness, made each call |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/payroll-brief/briefed/1` | `unstated_run` | miss | the transcript's own bash calls run `pf -o . 'workflow.bundles/workflow.bundle.md'`, `pf -o out '[⇉ Payroll](payroll__steps.bundle.md)'`, each pf on a reference no line of the form states, or with no entry as invalid usage, which the scorer reads as an unstated run; workflows/dispatch-brief/scenarios.toml states no [[scenario.run]] run, so bare pf, the guide, is the only run a correct session makes; the form's bundles carry no deferred or ↳ line and the Contract preamble's links are fragments of the bundle, so no stated line names any other reference; the agent, not the harness, made each call |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/payroll-brief/briefed/2` | `read_source` | miss | the transcript's read calls open the source documents ['ledger.md', 'payroll.md', 'states/audit.md', 'states/entry.md', 'states/exit.md', 'states/receive.md', 'states/trace.md', 'workflow.md'] beside the bundles, which the form hands it as workflow.bundles/; subagents.json records the same reads |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/payroll-brief/briefed/3` | `read_source` | miss | the transcript's read calls open the source documents ['ledger.md', 'payroll.md', 'states/audit.md', 'states/entry.md', 'states/exit.md', 'states/receive.md', 'states/trace.md', 'workflow.md'] beside the bundles, which the form hands it as workflow.bundles/; subagents.json records the same reads |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/payroll-brief/briefed/4` | `read_source` | miss | the transcript's read calls open the source documents ['payroll.md', 'states/audit.md', 'states/entry.md', 'states/exit.md', 'states/receive.md', 'workflow.md'] beside the bundles, which the form hands it as workflow.bundles/; subagents.json records the same reads |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/payroll-brief/briefed/5` | `unstated_run` | miss | the transcript's own bash calls run `pf -o out 'payroll__steps.bundle.md'`, each pf on a reference no line of the form states, or with no entry as invalid usage, which the scorer reads as an unstated run; workflows/dispatch-brief/scenarios.toml states no [[scenario.run]] run, so bare pf, the guide, is the only run a correct session makes; the form's bundles carry no deferred or ↳ line and the Contract preamble's links are fragments of the bundle, so no stated line names any other reference; the agent, not the harness, made each call |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/payroll-brief/bundle-set/1` | `unstated_run` | miss | the transcript's own bash calls run `pf -o . 2>/dev/null \|\| true`, each pf on a reference no line of the form states, or with no entry as invalid usage, which the scorer reads as an unstated run; workflows/dispatch-brief/scenarios.toml states no [[scenario.run]] run, so bare pf, the guide, is the only run a correct session makes; the form's bundles carry no deferred or ↳ line and the Contract preamble's links are fragments of the bundle, so no stated line names any other reference; the agent, not the harness, made each call |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/payroll-brief/bundle-set/2` | `unstated_run` | miss | the transcript's own bash calls run `pf -o . '[⇉ Payroll](payroll__steps.bundle.md)'`, `pf -o . 'workflow.bundles/payroll__steps.bundle.md'`, each pf on a reference no line of the form states, or with no entry as invalid usage, which the scorer reads as an unstated run; workflows/dispatch-brief/scenarios.toml states no [[scenario.run]] run, so bare pf, the guide, is the only run a correct session makes; the form's bundles carry no deferred or ↳ line and the Contract preamble's links are fragments of the bundle, so no stated line names any other reference; the agent, not the harness, made each call |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/payroll-brief/bundle-set/3` | `unstated_run` | miss | the transcript's own bash calls run `pf -o inputs-out 'x' 2>&1 \| head -5; ls inputs`, each pf on a reference no line of the form states, or with no entry as invalid usage, which the scorer reads as an unstated run; workflows/dispatch-brief/scenarios.toml states no [[scenario.run]] run, so bare pf, the guide, is the only run a correct session makes; the form's bundles carry no deferred or ↳ line and the Contract preamble's links are fragments of the bundle, so no stated line names any other reference; the agent, not the harness, made each call |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-brief/payroll-brief/bundle-set/5` | `read_source` | miss | the transcript's read calls open the source documents ['ledger.md', 'payroll.md', 'states/audit.md', 'states/entry.md', 'states/exit.md', 'states/receive.md', 'states/trace.md', 'workflow.md'] beside the bundles, which the form hands it as workflow.bundles/; subagents.json records the same reads |
