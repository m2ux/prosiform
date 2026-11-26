"""Compare the overlap table's verdicts with the tests collected before and after the removal.

Usage: python3 check_removed.py OVERLAP BEFORE AFTER

OVERLAP is W05's overlap.md. BEFORE and AFTER are the files collect_items.py
writes for `src/tests/test_cli.py` at the revision before the removal and at
the revision after it. A row names a node id at the revision before; its case
is looked up there and sought after, so a renumbered id is matched by case.
Exits nonzero when an approved row's case is still collected, when a refused
or undecided row's case is not, or when a collected case has no row.
"""

import json
import re
import sys
from pathlib import Path

ROW = re.compile(r"^\| (`+) ?(test_.*?) ?\1 \|")
CELL = re.compile(r"(?<!\\)\|")

table, before_path, after_path = sys.argv[1:4]
verdicts: dict[str, str] = {}
for line in Path(table).read_text().splitlines():
    if match := ROW.match(line):
        cells = [cell.strip() for cell in CELL.split(line)[1:-1]]
        verdicts[match.group(2).replace("\\|", "|")] = cells[-1]

before = {one["id"]: one["case"] for one in json.loads(Path(before_path).read_text())}
after = {one["case"] for one in json.loads(Path(after_path).read_text())}

unrowed = sorted(set(before) - set(verdicts))
approved = [test for test, verdict in verdicts.items() if verdict == "approved"]
kept = [test for test, verdict in verdicts.items() if verdict != "approved"]
still = sorted(test for test in approved if before[test] in after)
lost = sorted(test for test in kept if before[test] not in after)
foreign = len(after - {before[test] for test in kept})
print(
    f"{len(before)} collected before, {len(after)} after; "
    f"{len(approved)} approved rows, {len(still)} still collected; "
    f"{len(kept)} refused or undecided rows, {len(lost)} not collected; "
    f"{len(unrowed)} tests before with no row; {foreign} cases after with no kept row"
)
for one in still:
    print(f"approved but collected: {one}")
for one in lost:
    print(f"kept but not collected: {one}")
for one in unrowed:
    print(f"no row: {one}")
sys.exit(1 if still or lost or unrowed or foreign else 0)
