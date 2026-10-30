# W05 Findings

From run `20261028T165414Z`, the baseline run: 150 sessions, 2026-10-28.

## Which forms and models follow which workflows

| Model | `bundle` | `tree` | `prose` |
| --- | --- | --- | --- |
| `claude-haiku-5-5` | 25/25 | 25/25 | 25/25 |
| `claude-sonnet-5-5` | 25/25 | 25/25 | 25/25 |

Every model follows every workflow — `linear`, `branching` (both severities) and `looping` (no rework and two rounds) — in every form, five times out of five. The bundled diagram is followed as reliably as the unbundled tree and the prose.

## Dominant failure classes

None. No session failed, reached its timeout or wrote to stderr.

The eval is at its ceiling on this corpus: both models pass every cell, so the baseline detects a regression in diagram following but cannot rank the forms. What separates the forms is effort, not correctness:

- The `tree` form costs the most: mean USD 0.0044 a Haiku session and 0.0554 a Sonnet one, against 0.0037 and 0.0476 for the bundle, from reading the linked section files one by one.
- `prose` is the cheapest form for both models.
- `looping` `two-rounds` is the costliest scenario in every form, about twice a straight-through session.

## Per-model cost and duration

| Model | Sessions | Run cost (USD) | Mean per session (USD) | Costliest session (USD) | Mean duration | Longest |
| --- | --- | --- | --- | --- | --- | --- |
| `claude-haiku-5-5` | 75 | 0.2865 | 0.0038 | 0.0080 | 15.4 s | 37.5 s |
| `claude-sonnet-5-5` | 75 | 3.7203 | 0.0496 | 0.0880 | 17.6 s | 32.7 s |

The run cost USD 4.0068 and took about 10.5 minutes at four sessions at once. No session came near its USD 0.25 cap.

## Corpus defects fixed

None. With no failing session there was no transcript to review for an ambiguous section or scenario, and no cell was re-run. The baseline is the one complete run.

## Spend

| Run | Purpose | Recorded cost (USD) |
| --- | --- | --- |
| `20261028T165414Z` | Default matrix, baseline | 4.0068 |
| **Total** | | **4.0068** of the USD 40 cap |
