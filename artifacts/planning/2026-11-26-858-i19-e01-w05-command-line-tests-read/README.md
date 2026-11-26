# W05: Command-Line Tests Read Against the Corpus

> Task record. Created 2026-11-26.

## Executive Summary

Every test in `src/tests/test_cli.py` is listed beside the fixtures that hold its assertion, or as held by none, in [overlap.md](overlap.md).

The table is what the user reads before any command-line test is removed.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [w05.md](w05.md) | Work item for W05. |
| [overlap.md](overlap.md) | Every collected test beside the fixtures that hold its assertion, with an empty Verdict column for the user. |
| [shortlist.py](shortlist.py) | Lists, per test, the fixtures whose covered lines contain the test's. |
| [percontext.py](percontext.py) | Pytest plugin giving each test its own coverage context. |
| [pfcov.py](pfcov.py) | The build the corpus runner invokes: `pf` under coverage, one context per fixture. |
| [check_rows.py](check_rows.py) | Compares the table's rows with the tests pytest collects. |

## Reproduction

Run against an export of prosiform `b0eb7a2` (`git archive`), so the source checkout stays untouched. `W` is a scratch directory holding the export at `W/repo`, these scripts at `W/tools`, and coverage data at `W/data`.

```bash
# Per-test coverage, from W/repo/src
PYTHONPATH=W/tools uv run --frozen --with coverage coverage run --rcfile=W/tools/tests.coveragerc -m pytest -p percontext -o addopts= -q -p no:cacheprovider tests/test_cli.py
# tests.coveragerc: [run] source = prosiform, data_file = W/data/tests.coverage

# Per-fixture coverage, from W/repo
W05_COVERAGE_DATA=W/data/corpus.coverage PROSIFORM_BUILD="python W/tools/pfcov.py" uv run --project src --frozen --with coverage python checks/corpus.py
# corpus check: 708 fixture(s), 708 pass, 0 fail, 0 awaited, 0 unexpected pass
uv run --project W/repo/src --frozen --with coverage coverage combine --data-file=W/data/corpus.coverage W/data

# Shortlist; the four fault fixtures run in a temporary copy and are mapped back by name
uv run --project W/repo/src --frozen --with coverage python shortlist.py W/data/tests.coverage W/data/corpus.coverage shortlist.json an-unknown-fault-is-invalid-usage=cli/an-unknown-fault-is-invalid-usage a-run-that-fails-in-itself=diagnostics/a-run-that-fails-in-itself an-earlier-set-the-run-cannot-remove-warns=publication/an-earlier-set-the-run-cannot-remove-warns a-source-that-changes-during-bundling=source-consistency/a-source-that-changes-during-bundling
# 534 test contexts, 708 fixture contexts
# 272 tests with a containing fixture, 262 without
```

## AC12 check

The table's test names equal the tests pytest collects from `src/tests/test_cli.py` at `b0eb7a2`.

```bash
# from W/repo/src
uv run --frozen pytest -o addopts= --collect-only -q tests/test_cli.py > collected.txt
# 542 tests collected
python3 check_rows.py overlap.md collected.txt
# 542 collected, 542 rows, 0 without a row, 0 rows naming no collected test, 0 repeated rows
```

## Links

| Resource | URL |
| --- | --- |
| Epic I19 E01 | https://github.com/m2ux/prosiform/issues/858 |
| Epic plan | https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-test-turnaround |
