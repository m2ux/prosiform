# W04 Change List

Plan changes arising in delivery. Allowance: none, so every non-trivial change is held for the planner.

## Applied

| Change | Reason |
| --- | --- |
| `run.json` records the run's `date`, the UTC time it began. | The baseline names its run's date, and a run id need not be a timestamp. |
| `SESSION`, `RUN` and `TIMEOUT` live in `report.py`, and `run.py` imports them with `names`. | The runner calls the report at the end of a run, so the report cannot import the runner without a cycle. |
| A cell's key carries the workflow beside the scenario. | A scenario name is unique only within its workflow. |
| The roll-ups carry differences too, against rows summed from the baseline's cells. | The baseline holds cells alone, as directed; summing gives the same counts a run's roll-up gives. |
| `in_baseline` and `baseline_only` mark rows absent from either side. | The directed marking of absent cells, at every level. |

## Held

| Change | Reason |
| --- | --- |
| Once W05 commits `baseline.json`, the README's cost section names the measured figure. | The measured cost arrives with W05's run; the README now states the USD 75 bound and points at the baseline's `cost_usd`. |
| The stub-agent runner tests write their report against the committed baseline once it exists. | Harmless — they assert no comparison — but a `--baseline` runner option would let them name none. Not added: no requirement asks for it. |
