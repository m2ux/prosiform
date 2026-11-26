"""Shortlist the corpus fixtures whose covered lines contain each test's.

Reads two coverage data files of src/prosiform:

- TESTS: src/tests/test_cli.py run with one dynamic context per test node id.
- CORPUS: the corpus run with one context per fixture identity, its
  subprocess data files combined.

A fixture is a candidate for a test when, in every module the test covers,
the fixture covers every line the test covers. Candidates are ranked by the
lines the fixture covers beyond the test's in those modules, closest first.
A test with no containing fixture lists the fixtures covering the largest
share of its lines instead, marked partial, so the reading step still has
somewhere to start.

Usage:
    uv run --project src --frozen --with coverage python shortlist.py \\
        TESTS CORPUS OUT.json [--copy LEAF=IDENTITY ...]

`--copy` maps a fault fixture's context, recorded under the name of the
temporary copy it ran in, back to its identity.
"""

import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

from coverage.numbits import numbits_to_nums

TOP = 8


def contexts(path: str) -> dict[str, dict[str, set[int]]]:
    """Every context's covered lines, by module path relative to the package."""
    db = sqlite3.connect(path)
    files = {
        file_id: name[name.rindex("/prosiform/") + 1 :]
        for file_id, name in db.execute("select id, path from file")
    }
    names = dict(db.execute("select id, context from context"))
    covered: dict[str, dict[str, set[int]]] = defaultdict(lambda: defaultdict(set))
    for file_id, context_id, bits in db.execute(
        "select file_id, context_id, numbits from line_bits"
    ):
        covered[names[context_id]][files[file_id]].update(numbits_to_nums(bits))
    return covered


def shortlist(
    test: dict[str, set[int]], corpus: dict[str, dict[str, set[int]]]
) -> dict[str, object]:
    """The containing fixtures, closest first, or the best partial ones."""
    modules = sorted(test)
    total = sum(len(test[module]) for module in modules)
    containing, partial = [], []
    for fixture, lines in corpus.items():
        missing = sum(len(test[module] - lines.get(module, set())) for module in modules)
        excess = sum(len(lines.get(module, set()) - test[module]) for module in modules)
        if missing == 0:
            containing.append((excess, fixture))
        else:
            partial.append((missing, excess, fixture))
    containing.sort()
    partial.sort()
    return {
        "modules": modules,
        "lines": total,
        "containing_count": len(containing),
        "containing": [
            {"fixture": fixture, "excess": excess} for excess, fixture in containing[:TOP]
        ],
        "partial": []
        if containing
        else [
            {"fixture": fixture, "missing": missing, "excess": excess}
            for missing, excess, fixture in partial[:TOP]
        ],
    }


def main(argv: list[str]) -> int:
    tests_path, corpus_path, out_path, *rest = argv
    copies = dict(one.split("=", 1) for one in rest if "=" in one)
    tests = contexts(tests_path)
    corpus = {
        copies.get(name.removeprefix("copy:"), name): lines
        for name, lines in contexts(corpus_path).items()
        if name
    }
    result = {
        node: shortlist(lines, corpus)
        for node, lines in sorted(tests.items())
        if node
    }
    Path(out_path).write_text(json.dumps(result, indent=1) + "\n")
    held = sum(1 for one in result.values() if one["containing_count"])
    print(f"{len(result)} test contexts, {len(corpus)} fixture contexts")
    print(f"{held} tests with a containing fixture, {len(result) - held} without")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
