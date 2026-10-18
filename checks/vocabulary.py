#!/usr/bin/env python3
"""Assert the shipped glossary defines every contract term the design marks.

The design italicises a contract term where it first uses it, so the
contract carries its own inventory of its vocabulary. The design and each
epic's Acceptance Criteria are the text that uses that vocabulary, and
`docs/glossary.md` is the one glossary the repository holds.

Both sources are read from the branch and path the README's Design link
names, so no path into a dated planning folder is written here: superseding
that folder changes the link, and the link check holds that link to
resolving. Reading them needs git and no network.

A term the design marks that `docs/glossary.md` does not define fails the
check, and so does a definition that neither the design marks nor an
acceptance criterion uses.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

README = ROOT / "README.md"
SHIPPED_GLOSSARY = ROOT / "docs" / "glossary.md"

DESIGN_LINK = re.compile(
    r"https://github\.com/m2ux/prosiform/blob/([^/\s)]+)/(\S*design\.md)\b"
)
EPIC_PATTERN = re.compile(r"^i\d\d-e\d\d\.md$")

SECTION = re.compile(r"^##\s+(.*)$", re.MULTILINE)
TABLE_TERM = re.compile(r"^\|\s*\*\*([^*]+)\*\*", re.MULTILINE)
CRITERIA_SECTION = re.compile(
    r"^## Acceptance Criteria\s*$(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL
)
MARKED_TERM = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])")
FENCE = re.compile(r"^(?:```|~~~)", re.MULTILINE)
CODE_SPAN = re.compile(r"`[^`\n]*`")
AVOIDED_SECTION = "Terms deliberately not used"
PARENTHETICAL = re.compile(r"\s*\([^)]*\)\s*$")


def design_reference() -> tuple[str, str]:
    """The git ref and path the README's Design link names."""
    match = DESIGN_LINK.search(README.read_text())
    if match is None:
        raise SystemExit(
            "vocabulary check: README.md carries no link to the design, which is "
            "where the contract's terms are marked"
        )
    return match.group(1), match.group(2)


def git_ref(name: str) -> str:
    for candidate in (f"origin/{name}", name):
        result = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{candidate}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return candidate
    raise SystemExit(
        f"vocabulary check: no ref named {name} or origin/{name}; the branch the "
        "contract is stated on is out of reach"
    )


def git_show(ref: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise SystemExit(f"vocabulary check: {path} is absent from {ref}")
    return result.stdout


def epic_paths(ref: str, directory: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-tree", "--name-only", f"{ref}:{directory}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        f"{directory}/{name}"
        for name in result.stdout.splitlines()
        if EPIC_PATTERN.match(name)
    ]


def strip_code(text: str) -> str:
    """Blank out code, whose contents are examples rather than prose."""
    out, fenced = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else CODE_SPAN.sub(" ", line))
    return "\n".join(out)


def marked_terms(design: str) -> list[str]:
    """Every contract term the design marks, in the order it marks them."""
    terms: list[str] = []
    for mark in MARKED_TERM.findall(strip_code(design)):
        term = re.sub(r"\s+", " ", mark).strip().lower()
        if term and term not in terms:
            terms.append(term)
    return terms


def glossary_terms(text: str) -> tuple[set[str], set[str]]:
    """The terms a glossary defines, and the ones it names as avoided."""
    defined: set[str] = set()
    avoided: set[str] = set()
    heading = None
    for index, part in enumerate(re.split(SECTION, text)):
        if index == 0:
            continue
        if index % 2 == 1:
            heading = part.strip()
            continue
        target = avoided if heading == AVOIDED_SECTION else defined
        for term in TABLE_TERM.findall(part):
            target.add(PARENTHETICAL.sub("", term).strip().lower())
    return defined, avoided


def forms(term: str) -> set[str]:
    """The term as written and as a plural of a defined singular."""
    spellings = {term}
    if term.endswith("s"):
        spellings.add(term[:-1])
    if term.endswith("es"):
        spellings.add(term[:-2])
    return spellings


def holds(term: str, terms: set[str]) -> bool:
    return bool(forms(term) & terms)


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
        help="print each contract term the design marks and where it is used",
    )
    arguments = parser.parse_args()

    branch, design_path = design_reference()
    ref = git_ref(branch)
    directory = design_path.rsplit("/", 1)[0]

    design = git_show(ref, design_path)
    sources = {design_path: design}
    for path in epic_paths(ref, directory):
        sources[f"{path} (Acceptance Criteria)"] = criteria_text(git_show(ref, path))

    inventory = marked_terms(design)
    defined, avoided = glossary_terms(SHIPPED_GLOSSARY.read_text())

    used: dict[str, list[str]] = {}
    for term in inventory:
        pattern = usage_pattern(term)
        used[term] = [name for name, text in sources.items() if pattern.search(text)]

    if arguments.list:
        for term, where in used.items():
            print(f"{term}: {len(where)} source(s)")

    failures = []
    for term in inventory:
        if holds(term, avoided):
            failures.append(
                f"{term} — the design marks it as a contract term, and "
                "docs/glossary.md names it as a term deliberately not used"
            )
        elif not holds(term, defined):
            failures.append(
                f"{term} — the design marks it as a contract term, and "
                "docs/glossary.md does not define it"
            )

    marked = {spelling for term in inventory for spelling in forms(term)}
    for term in sorted(defined):
        if term in marked:
            continue
        pattern = usage_pattern(term)
        if any(pattern.search(text) for text in sources.values()):
            continue
        failures.append(
            f"{term} — docs/glossary.md defines it, and neither the design nor an "
            "acceptance criterion carries it"
        )

    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if failures:
        print(
            f"\nvocabulary check: {len(failures)} term(s) the glossary and the "
            "contract disagree on",
            file=sys.stderr,
        )
        return 1
    print(
        f"vocabulary check: {len(inventory)} contract term(s) marked in "
        f"{design_path} on {ref}, every one defined in docs/glossary.md, and every "
        f"definition carried by the contract across {len(sources)} source(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
