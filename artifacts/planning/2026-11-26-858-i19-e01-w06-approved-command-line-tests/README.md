# W06: Approved Command-Line Tests Removed

> Task record. Created 2026-11-26.

## Executive Summary

Each command-line test the overlap table approves for removal leaves `src/tests/test_cli.py`, and the agent instructions state which suite a new behaviour's test belongs to.

A behaviour a fixture holds is then restated once on a change, not twice.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [w06.md](w06.md) | Work item for W06. |
| [collect_items.py](collect_items.py) | Pytest plugin writing each collected test as its node id and its case: the function with its parameter values. |
| [check_removed.py](check_removed.py) | Compares the overlap table's verdicts with the cases collected before and after the removal. |

## AC13 check

The overlap table's rows name node ids at `b0eb7a2`, where `src/tests/test_cli.py` equals the removal's base `81c5ca0`. Removing an entry renumbers a position-numbered id (`entries0`, `arguments2`) in five functions, so each row is matched by its case, not its id.

```bash
# from src/, the base file exported to BASE/test_cli.py
PYTHONPATH=<this folder> W06_ITEMS=before.json uv run --frozen pytest -p collect_items -o addopts= --collect-only -q -p no:cacheprovider BASE/test_cli.py
# 542 tests collected
PYTHONPATH=<this folder> W06_ITEMS=after.json uv run --frozen pytest -p collect_items -o addopts= --collect-only -q -p no:cacheprovider tests/test_cli.py
# 337 tests collected
python3 check_removed.py ../2026-11-26-858-i19-e01-w05-command-line-tests-read/overlap.md before.json after.json
# 542 collected before, 337 after; 205 approved rows, 0 still collected; 337 refused or undecided rows, 0 not collected; 0 tests before with no row; 0 cases after with no kept row
```

The removal takes 122 whole functions (141 cases) and 64 cases from 25 functions that keep their other cases.

## AC14 check

`make conformance` ran at `81c5ca0` and at the removal's head `7afaed8`. The two reports are byte-identical: 311 clauses list at least one fixture at both, and the same 90 list none.

## Make check

`make check` at `041a19b`, with `PROSIFORM_BUILD` naming the worktree's own `pf`, exits 0: 2125 build tests pass (2330 collected at `81c5ca0`), 1182 harness tests pass, and the corpus runs 708 fixtures, 708 pass.

## Links

| Resource | URL |
| --- | --- |
| Epic I19 E01 | https://github.com/m2ux/prosiform/issues/858 |
| Epic plan | https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-test-turnaround |
