# Diagram-Following Report: mvp-proof

- **Run:** `mvp-proof`, 2026-11-03T07:15:02+00:00; models `claude-haiku-5-5`; 5 repetitions.
- **Sessions:** 150 of 150 started; 0 not started.
- **Tokens:** 19268512.
- **Managed plugins:** `shielded-core-rules@shieldedtech` 0.7.3, whose injected rules every session carried; environment added: `CLAUDE_CODE_ENABLE_TELEMETRY`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL`, `OTEL_METRICS_EXPORTER`, `OTEL_METRICS_INCLUDE_SESSION_ID`, `OTEL_METRIC_EXPORT_INTERVAL`.
- **Cost:** USD 0.67671.
- **Baseline:** `20261028T165414Z`, 2026-10-28T16:54:14+00:00. Change is this run's pass rate less the baseline's, and a failure count's change follows it in brackets.

## By Model

| Model | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `claude-haiku-5-5` | 150 | 148 | 99% | -1 pts | missing_action 1 (+1), unfinished 1 (+1) | 0 | 128457 | 0.004511 |

## By Model and Form

| Model | Form | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `claude-haiku-5-5` | `bundle` | 75 | 75 | 100% | +0 pts | none | 0 | 121109 | 0.004213 |
| `claude-haiku-5-5` | `tree` | 75 | 73 | 97% | -3 pts | missing_action 1 (+1), unfinished 1 (+1) | 0 | 135804 | 0.00481 |

## By Model, Form and Scenario

| Model | Form | Workflow | Scenario | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `claude-haiku-5-5` | `bundle` | `declared-inclusion` | `declared-link-followed` | 5 | 5 | 100% | new | none | 0 | 125479 | 0.004087 |
| `claude-haiku-5-5` | `bundle` | `declared-inclusion` | `undeclared-link-as-text` | 5 | 5 | 100% | new | none | 0 | 87409.6 | 0.003376 |
| `claude-haiku-5-5` | `bundle` | `group-placement` | `leaf-group` | 5 | 5 | 100% | new | none | 0 | 119331 | 0.00405 |
| `claude-haiku-5-5` | `bundle` | `group-placement` | `nested-intermediate` | 5 | 5 | 100% | new | none | 0 | 185653 | 0.005491 |
| `claude-haiku-5-5` | `bundle` | `group-placement` | `two-presets-one-document` | 5 | 5 | 100% | new | none | 0 | 155518 | 0.005138 |
| `claude-haiku-5-5` | `bundle` | `preset-selection` | `default-alone` | 5 | 5 | 100% | new | none | 0 | 109351 | 0.004089 |
| `claude-haiku-5-5` | `bundle` | `preset-selection` | `title-selected` | 5 | 5 | 100% | new | none | 0 | 131473 | 0.004454 |
| `claude-haiku-5-5` | `bundle` | `preset-selection` | `two-presets-one-title` | 5 | 5 | 100% | new | none | 0 | 145082 | 0.005113 |
| `claude-haiku-5-5` | `bundle` | `section-composition` | `deferred-occurrence` | 5 | 5 | 100% | new | none | 0 | 110087 | 0.004173 |
| `claude-haiku-5-5` | `bundle` | `section-composition` | `merged-sources` | 5 | 5 | 100% | new | none | 0 | 108165 | 0.003745 |
| `claude-haiku-5-5` | `bundle` | `section-composition` | `nested-composition` | 5 | 5 | 100% | new | none | 0 | 109187 | 0.004085 |
| `claude-haiku-5-5` | `bundle` | `section-entry` | `document-fragment` | 5 | 5 | 100% | new | none | 0 | 83561.8 | 0.00296 |
| `claude-haiku-5-5` | `bundle` | `subst-redirect` | `document-redirect` | 5 | 5 | 100% | new | none | 0 | 63509 | 0.00296 |
| `claude-haiku-5-5` | `bundle` | `subst-redirect` | `preset-over-default` | 5 | 5 | 100% | new | none | 0 | 155718 | 0.005235 |
| `claude-haiku-5-5` | `bundle` | `subst-redirect` | `section-redirect` | 5 | 5 | 100% | new | none | 0 | 127114 | 0.004233 |
| `claude-haiku-5-5` | `tree` | `declared-inclusion` | `declared-link-followed` | 5 | 5 | 100% | new | none | 0 | 131232 | 0.004367 |
| `claude-haiku-5-5` | `tree` | `declared-inclusion` | `undeclared-link-as-text` | 5 | 5 | 100% | new | none | 0 | 85848.8 | 0.003645 |
| `claude-haiku-5-5` | `tree` | `group-placement` | `leaf-group` | 5 | 5 | 100% | new | none | 0 | 129010 | 0.004252 |
| `claude-haiku-5-5` | `tree` | `group-placement` | `nested-intermediate` | 5 | 5 | 100% | new | none | 0 | 179958 | 0.005821 |
| `claude-haiku-5-5` | `tree` | `group-placement` | `two-presets-one-document` | 5 | 5 | 100% | new | none | 0 | 134545 | 0.004911 |
| `claude-haiku-5-5` | `tree` | `preset-selection` | `default-alone` | 5 | 5 | 100% | new | none | 0 | 120505 | 0.004404 |
| `claude-haiku-5-5` | `tree` | `preset-selection` | `title-selected` | 5 | 5 | 100% | new | none | 0 | 137884 | 0.00485 |
| `claude-haiku-5-5` | `tree` | `preset-selection` | `two-presets-one-title` | 5 | 5 | 100% | new | none | 0 | 150473 | 0.005742 |
| `claude-haiku-5-5` | `tree` | `section-composition` | `deferred-occurrence` | 5 | 5 | 100% | new | none | 0 | 158454 | 0.005009 |
| `claude-haiku-5-5` | `tree` | `section-composition` | `merged-sources` | 5 | 5 | 100% | new | none | 0 | 120599 | 0.003913 |
| `claude-haiku-5-5` | `tree` | `section-composition` | `nested-composition` | 5 | 3 | 60% | new | missing_action 1, unfinished 1 | 0 | 144448 | 0.005034 |
| `claude-haiku-5-5` | `tree` | `section-entry` | `document-fragment` | 5 | 5 | 100% | new | none | 0 | 93821 | 0.003457 |
| `claude-haiku-5-5` | `tree` | `subst-redirect` | `document-redirect` | 5 | 5 | 100% | new | none | 0 | 99581.6 | 0.003832 |
| `claude-haiku-5-5` | `tree` | `subst-redirect` | `preset-over-default` | 5 | 5 | 100% | new | none | 0 | 216419 | 0.007727 |
| `claude-haiku-5-5` | `tree` | `subst-redirect` | `section-redirect` | 5 | 5 | 100% | new | none | 0 | 134285 | 0.005188 |

## Baseline Only

- `claude-sonnet-5-5`
- `claude-haiku-5-5` / `prose`
- `claude-sonnet-5-5` / `bundle`
- `claude-sonnet-5-5` / `prose`
- `claude-sonnet-5-5` / `tree`
- `claude-haiku-5-5` / `bundle` / `branching` / `high-severity`
- `claude-haiku-5-5` / `bundle` / `branching` / `low-severity`
- `claude-haiku-5-5` / `bundle` / `linear` / `straight-through`
- `claude-haiku-5-5` / `bundle` / `looping` / `no-rework`
- `claude-haiku-5-5` / `bundle` / `looping` / `two-rounds`
- `claude-haiku-5-5` / `prose` / `branching` / `high-severity`
- `claude-haiku-5-5` / `prose` / `branching` / `low-severity`
- `claude-haiku-5-5` / `prose` / `linear` / `straight-through`
- `claude-haiku-5-5` / `prose` / `looping` / `no-rework`
- `claude-haiku-5-5` / `prose` / `looping` / `two-rounds`
- `claude-haiku-5-5` / `tree` / `branching` / `high-severity`
- `claude-haiku-5-5` / `tree` / `branching` / `low-severity`
- `claude-haiku-5-5` / `tree` / `linear` / `straight-through`
- `claude-haiku-5-5` / `tree` / `looping` / `no-rework`
- `claude-haiku-5-5` / `tree` / `looping` / `two-rounds`
- `claude-sonnet-5-5` / `bundle` / `branching` / `high-severity`
- `claude-sonnet-5-5` / `bundle` / `branching` / `low-severity`
- `claude-sonnet-5-5` / `bundle` / `linear` / `straight-through`
- `claude-sonnet-5-5` / `bundle` / `looping` / `no-rework`
- `claude-sonnet-5-5` / `bundle` / `looping` / `two-rounds`
- `claude-sonnet-5-5` / `prose` / `branching` / `high-severity`
- `claude-sonnet-5-5` / `prose` / `branching` / `low-severity`
- `claude-sonnet-5-5` / `prose` / `linear` / `straight-through`
- `claude-sonnet-5-5` / `prose` / `looping` / `no-rework`
- `claude-sonnet-5-5` / `prose` / `looping` / `two-rounds`
- `claude-sonnet-5-5` / `tree` / `branching` / `high-severity`
- `claude-sonnet-5-5` / `tree` / `branching` / `low-severity`
- `claude-sonnet-5-5` / `tree` / `linear` / `straight-through`
- `claude-sonnet-5-5` / `tree` / `looping` / `no-rework`
- `claude-sonnet-5-5` / `tree` / `looping` / `two-rounds`

## Failing Sessions

| Session | Class | Disposition | Evidence |
| --- | --- | --- | --- |
| `claude-haiku-5-5/section-composition/nested-composition/tree/2` | `missing_action` | miss | states/assess.md names actions/assess.txt and assessed, the file and value the scorer reads; the transcript writes lodge.txt, amend.txt and close.txt but never assess.txt, though its result message claims it did |
| `claude-haiku-5-5/section-composition/nested-composition/tree/3` | `unfinished` | miss | exit status 0, not timeout; the session ended on its own at Amend after writing lodge.txt and assess.txt, and its result message asks the user how to proceed rather than writing amend.txt, though states/amend.md says to write amended |
