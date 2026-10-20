#!/usr/bin/env python3
"""Assert the repository carries the trees this stage needs.

A tree exists when git tracks at least one file under it. An untracked
directory is invisible to a fresh checkout, so it does not count.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_TREES = {
    "fixtures": "the language-neutral fixture corpus",
    "src": "the build",
    "docs": "the documentation this repository owns",
}


def tracked_files(tree: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--", tree],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def main() -> int:
    failures = []
    for tree, purpose in sorted(REQUIRED_TREES.items()):
        files = tracked_files(tree)
        if not files:
            failures.append(f"{tree}/ holds no tracked file; it is {purpose}")
            continue
        if not (ROOT / tree).is_dir():
            failures.append(f"{tree}/ is tracked but is not a directory")
            continue
        print(f"ok   {tree}/ — {len(files)} tracked file(s), {purpose}")

    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)

    if failures:
        print(f"\nlayout check: {len(failures)} failure(s)", file=sys.stderr)
        return 1
    print(f"\nlayout check: {len(REQUIRED_TREES)} tree(s) present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
