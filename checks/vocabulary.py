#!/usr/bin/env python3
"""Assert the shipped glossary defines every contract term the plan uses.

The contract's vocabulary is inventoried by the planning record's glossary,
which is the upstream the shipped glossary is derived from. The design and
the epic acceptance criteria are the text that uses it. Both live on the
engineering branch and are read from it with git, so the check needs no
network and no second copy in this tree.

A term the design or a criterion uses, and `docs/glossary.md` does not
define, fails the check.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PLAN_BRANCH = "engineering"
PLAN_DIR = "artifacts/planning/2026-10-17-prosiform-v1"
INVENTORY = f"{PLAN_DIR}/glossary.md"
DESIGN = f"{PLAN_DIR}/design.md"
EPIC_PATTERN = re.compile(r"i\d\d-e\d\d\.md$")

SHIPPED_GLOSSARY = ROOT / "docs" / "glossary.md"

SECTION = re.compile(r"^##\s+(.*)$", re.MULTILINE)
TABLE_TERM = re.compile(r"^\|\s*\*\*([^*]+)\*\*", re.MULTILINE)
CRITERIA_SECTION = re.compile(
    r"^## Acceptance Criteria\s*$(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL
)
AVOIDED_SECTION = "Terms deliberately not used"
PARENTHETICAL = re.compile(r"\s*\([^)]*\)\s*$")


def git_ref() -> str:
    for candidate in (f"origin/{PLAN_BRANCH}", PLAN_BRANCH):
        result = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{candidate}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return candidate
    raise SystemExit(
        f"vocabulary check: no ref named {PLAN_BRANCH} or origin/{PLAN_BRANCH}; "
        "the plan the contract's vocabulary is inventoried from is out of reach"
    )


def git_show(ref: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise SystemExit(f"vocabulary check: {path} is absent from {ref}")
    return result.stdout


def epic_paths(ref: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-tree", "--name-only", f"{ref}:{PLAN_DIR}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        f"{PLAN_DIR}/{name}"
        for name in result.stdout.splitlines()
        if EPIC_PATTERN.search(name)
    ]


def glossary_terms(text: str) -> set[str]:
    """Every term a glossary defines, less the ones it names as avoided."""
    terms: set[str] = set()
    heading = None
    for index, part in enumerate(re.split(SECTION, text)):
        if index == 0:
            continue
        if index % 2 == 1:
            heading = part.strip()
            continue
        if heading == AVOIDED_SECTION:
            continue
        for term in TABLE_TERM.findall(part):
            terms.add(PARENTHETICAL.sub("", term).strip().lower())
    return terms


def usage_pattern(term: str) -> re.Pattern[str]:
    words = [re.escape(word) for word in term.split()]
    words[-1] += r"(?:s|es)?"
    return re.compile(r"\b" + r"\s+".join(words) + r"\b", re.IGNORECASE)


def criteria_text(body: str) -> str:
    return "\n".join(CRITERIA_SECTION.findall(body))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--list",
        action="store_true",
        help="print the contract terms the design and the criteria use",
    )
    arguments = parser.parse_args()

    ref = git_ref()
    inventory = glossary_terms(git_show(ref, INVENTORY))
    shipped = glossary_terms(SHIPPED_GLOSSARY.read_text())

    sources = {DESIGN: git_show(ref, DESIGN)}
    for path in epic_paths(ref):
        sources[f"{path} (Acceptance Criteria)"] = criteria_text(git_show(ref, path))

    used: dict[str, list[str]] = {}
    for term in sorted(inventory):
        pattern = usage_pattern(term)
        where = [name for name, text in sources.items() if pattern.search(text)]
        if where:
            used[term] = where

    if arguments.list:
        for term, where in used.items():
            print(f"{term}: {len(where)} source(s)")

    missing = {term: where for term, where in used.items() if term not in shipped}
    for term, where in missing.items():
        print(
            f"FAIL {term} — used in {', '.join(where)}, and docs/glossary.md "
            "does not define it",
            file=sys.stderr,
        )

    if missing:
        print(
            f"\nvocabulary check: {len(missing)} undefined contract term(s)",
            file=sys.stderr,
        )
        return 1
    print(
        f"vocabulary check: {len(used)} contract term(s) used across "
        f"{len(sources)} source(s), every one defined in docs/glossary.md"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
