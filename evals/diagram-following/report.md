# Diagram-Following Report: 20261028T165414Z

- **Run:** `20261028T165414Z`, 2026-10-28T16:54:14+00:00; models `claude-haiku-5-5`, `claude-sonnet-5-5`; 5 repetitions.
- **Sessions:** 150 of 150 started; 0 not started.
- **Cost:** USD 4.0068.
- **Baseline:** none.

## By Model

| Model | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens (in / out / cache write / cache read) | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `claude-haiku-5-5` | 75 | 75 | 100% | — | none | 0 | 19.5 / 2687.5 / 7945.2 / 88478.7 | 0.00382 |
| `claude-sonnet-5-5` | 75 | 75 | 100% | — | none | 0 | 13.9 / 1974.3 / 6171.5 / 51477.7 | 0.049604 |

## By Model and Form

| Model | Form | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens (in / out / cache write / cache read) | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `claude-haiku-5-5` | `bundle` | 25 | 25 | 100% | — | none | 0 | 19 / 2531.2 / 7805.2 / 87457.1 | 0.003703 |
| `claude-haiku-5-5` | `prose` | 25 | 25 | 100% | — | none | 0 | 16.9 / 2361 / 7383.9 / 72150.2 | 0.00338 |
| `claude-haiku-5-5` | `tree` | 25 | 25 | 100% | — | none | 0 | 22.6 / 3170.3 / 8646.6 / 105829 | 0.004375 |
| `claude-sonnet-5-5` | `bundle` | 25 | 25 | 100% | — | none | 0 | 13.4 / 1829.9 / 6075.2 / 50202.6 | 0.047646 |
| `claude-sonnet-5-5` | `prose` | 25 | 25 | 100% | — | none | 0 | 13 / 1782.9 / 5797.7 / 46877.7 | 0.045733 |
| `claude-sonnet-5-5` | `tree` | 25 | 25 | 100% | — | none | 0 | 15.4 / 2310 / 6641.7 / 57352.9 | 0.055433 |

## By Model, Form and Scenario

| Model | Form | Workflow | Scenario | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens (in / out / cache write / cache read) | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `claude-haiku-5-5` | `bundle` | `branching` | `high-severity` | 5 | 5 | 100% | — | none | 0 | 15.6 / 2423 / 7713.8 / 66027.6 | 0.003416 |
| `claude-haiku-5-5` | `bundle` | `branching` | `low-severity` | 5 | 5 | 100% | — | none | 0 | 14.4 / 1998.8 / 6999.4 / 58752 | 0.002988 |
| `claude-haiku-5-5` | `bundle` | `linear` | `straight-through` | 5 | 5 | 100% | — | none | 0 | 13.6 / 1764.8 / 6504.4 / 53508 | 0.00272 |
| `claude-haiku-5-5` | `bundle` | `looping` | `no-rework` | 5 | 5 | 100% | — | none | 0 | 12.4 / 1956.2 / 6602 / 48183.2 | 0.002782 |
| `claude-haiku-5-5` | `bundle` | `looping` | `two-rounds` | 5 | 5 | 100% | — | none | 0 | 38.8 / 4513.4 / 11206.2 / 210815 | 0.00661 |
| `claude-haiku-5-5` | `prose` | `branching` | `high-severity` | 5 | 5 | 100% | — | none | 0 | 15.2 / 2305.2 / 7357 / 62402.2 | 0.00325 |
| `claude-haiku-5-5` | `prose` | `branching` | `low-severity` | 5 | 5 | 100% | — | none | 0 | 16.8 / 1976 / 6785.6 / 68540.8 | 0.003032 |
| `claude-haiku-5-5` | `prose` | `linear` | `straight-through` | 5 | 5 | 100% | — | none | 0 | 13.2 / 1785.6 / 6362.8 / 51195.2 | 0.002679 |
| `claude-haiku-5-5` | `prose` | `looping` | `no-rework` | 5 | 5 | 100% | — | none | 0 | 13.6 / 1792.2 / 6247.4 / 52545.4 | 0.002672 |
| `claude-haiku-5-5` | `prose` | `looping` | `two-rounds` | 5 | 5 | 100% | — | none | 0 | 25.6 / 3945.8 / 10166.6 / 126068 | 0.005269 |
| `claude-haiku-5-5` | `tree` | `branching` | `high-severity` | 5 | 5 | 100% | — | none | 0 | 22.8 / 3012.8 / 8494.8 / 103401 | 0.004242 |
| `claude-haiku-5-5` | `tree` | `branching` | `low-severity` | 5 | 5 | 100% | — | none | 0 | 20.8 / 2458.4 / 7599.6 / 90302.6 | 0.003654 |
| `claude-haiku-5-5` | `tree` | `linear` | `straight-through` | 5 | 5 | 100% | — | none | 0 | 23.2 / 2330.8 / 7322.8 / 98840.2 | 0.003621 |
| `claude-haiku-5-5` | `tree` | `looping` | `no-rework` | 5 | 5 | 100% | — | none | 0 | 16 / 2396.8 / 7215.6 / 66951.4 | 0.003313 |
| `claude-haiku-5-5` | `tree` | `looping` | `two-rounds` | 5 | 5 | 100% | — | none | 0 | 30 / 5652.8 / 12600.4 / 169648 | 0.007046 |
| `claude-sonnet-5-5` | `bundle` | `branching` | `high-severity` | 5 | 5 | 100% | — | none | 0 | 12.8 / 1807.8 / 6081.6 / 46597.2 | 0.04709 |
| `claude-sonnet-5-5` | `bundle` | `branching` | `low-severity` | 5 | 5 | 100% | — | none | 0 | 9.6 / 1438 / 5336.2 / 32014.2 | 0.038945 |
| `claude-sonnet-5-5` | `bundle` | `linear` | `straight-through` | 5 | 5 | 100% | — | none | 0 | 12 / 1432.4 / 5306.4 / 41028 | 0.039676 |
| `claude-sonnet-5-5` | `bundle` | `looping` | `no-rework` | 5 | 5 | 100% | — | none | 0 | 10 / 1224.6 / 5039.2 / 33223.2 | 0.035745 |
| `claude-sonnet-5-5` | `bundle` | `looping` | `two-rounds` | 5 | 5 | 100% | — | none | 0 | 22.4 / 3246.6 / 8612.4 / 98150.4 | 0.076775 |
| `claude-sonnet-5-5` | `prose` | `branching` | `high-severity` | 5 | 5 | 100% | — | none | 0 | 14.4 / 1931.6 / 6105.6 / 52829.8 | 0.04905 |
| `claude-sonnet-5-5` | `prose` | `branching` | `low-severity` | 5 | 5 | 100% | — | none | 0 | 12 / 1596.2 / 5525.2 / 41604.8 | 0.042247 |
| `claude-sonnet-5-5` | `prose` | `linear` | `straight-through` | 5 | 5 | 100% | — | none | 0 | 12 / 1395.2 / 5139.4 / 40404.2 | 0.038574 |
| `claude-sonnet-5-5` | `prose` | `looping` | `no-rework` | 5 | 5 | 100% | — | none | 0 | 9.6 / 1173.4 / 4739.8 / 30945 | 0.033807 |
| `claude-sonnet-5-5` | `prose` | `looping` | `two-rounds` | 5 | 5 | 100% | — | none | 0 | 16.8 / 2818 / 7478.6 / 68604.8 | 0.064988 |
| `claude-sonnet-5-5` | `tree` | `branching` | `high-severity` | 5 | 5 | 100% | — | none | 0 | 16.8 / 2482 / 7040.8 / 64464.6 | 0.059463 |
| `claude-sonnet-5-5` | `tree` | `branching` | `low-severity` | 5 | 5 | 100% | — | none | 0 | 14 / 2034.8 / 6209.4 / 50937.6 | 0.050307 |
| `claude-sonnet-5-5` | `tree` | `linear` | `straight-through` | 5 | 5 | 100% | — | none | 0 | 16 / 1955 / 5969 / 57436.2 | 0.049202 |
| `claude-sonnet-5-5` | `tree` | `looping` | `no-rework` | 5 | 5 | 100% | — | none | 0 | 13.2 / 1694 / 5477.8 / 45734.8 | 0.043451 |
| `claude-sonnet-5-5` | `tree` | `looping` | `two-rounds` | 5 | 5 | 100% | — | none | 0 | 16.8 / 3384.4 / 8511.4 / 68191.4 | 0.074742 |
