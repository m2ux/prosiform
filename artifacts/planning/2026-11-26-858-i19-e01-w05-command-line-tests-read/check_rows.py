"""Compare overlap.md's test rows with the tests pytest collects from test_cli.py.

Usage: python3 check_rows.py overlap.md COLLECTED

COLLECTED is the output of
`pytest -o addopts= --collect-only -q tests/test_cli.py` run from src/.
Exits nonzero when a collected test has no row or a row names no collected test.
"""

import re
import sys
from pathlib import Path

ROW = re.compile(r"^\| (`+) ?(test_.*?) ?\1 \|")

table, collected = sys.argv[1:3]
rows = [
    match.group(2).replace("\\|", "|")
    for line in Path(table).read_text().splitlines()
    if (match := ROW.match(line))
]
tests = [
    line.strip().split("::", 1)[1]
    for line in Path(collected).read_text().splitlines()
    if "::" in line
]
missing = sorted(set(tests) - set(rows))
extra = sorted(set(rows) - set(tests))
repeated = len(rows) - len(set(rows))
print(f"{len(tests)} collected, {len(rows)} rows, {len(missing)} without a row, "
      f"{len(extra)} rows naming no collected test, {repeated} repeated rows")
for one in missing:
    print(f"no row: {one}")
for one in extra:
    print(f"no test: {one}")
sys.exit(1 if missing or extra or repeated else 0)
