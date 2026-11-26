#!/usr/bin/env python3
"""Assert the glossary, the contract and the documentation carry one vocabulary.

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

The glossary also names the terms it deliberately does not use, each with
the reason it was refused. The pages under `docs/` are what a user reads, so
the reasons hold for them: a page stating such a term, in its prose, fails
the check with the glossary's reason. A term a page quotes in a code span is
the word under discussion rather than a use of it.
"""

import argparse
import re
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

from documents import ROOT, documents, strip_code_blocks

README = ROOT / "README.md"
DOCS = ROOT / "docs"
SHIPPED_GLOSSARY = DOCS / "glossary.md"

DESIGN_LINK = re.compile(
    r"https://github\.com/m2ux/prosiform/blob/([^/\s)]+)/(\S*design\.md)\b"
)
EPIC_PATTERN = re.compile(r"^i\d\d-e\d\d\.md$")

SECTION = re.compile(r"^##\s+(.*)$", re.MULTILINE)
TABLE_TERM = re.compile(r"^\|\s*\*\*([^*]+)\*\*", re.MULTILINE)
CRITERIA_SECTION = re.compile(
    r"^## Acceptance Criteria\s*$(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL
)
AVOIDED_ROW = re.compile(r"^\|\s*\*\*([^*]+)\*\*\s*\|\s*(.*?)\s*\|\s*$", re.MULTILINE)
MARKED_TERM = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])")
CODE_SPAN = re.compile(r"`[^`\n]*`")
LINK_DESTINATION = re.compile(r"\]\([^)\n]*\)")
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
    """Blank out code, whose contents are examples rather than prose.

    A code block is the one `documents.strip_code_blocks` finds, and a code
    span is a single backtick pair on one line.
    """
    return CODE_SPAN.sub(" ", strip_code_blocks(text))


def marked_terms(design: str) -> list[str]:
    """Every contract term the design marks, in the order it marks them."""
    terms: list[str] = []
    for mark in MARKED_TERM.findall(strip_code(design)):
        term = re.sub(r"\s+", " ", mark).strip().lower()
        if term and term not in terms:
            terms.append(term)
    return terms


def term_name(term: str) -> str:
    return PARENTHETICAL.sub("", term).strip().lower()


def glossary_terms(text: str) -> tuple[set[str], dict[str, str]]:
    """The terms a glossary defines, and each it names as avoided against its reason."""
    defined: set[str] = set()
    avoided: dict[str, str] = {}
    heading = None
    for index, part in enumerate(re.split(SECTION, text)):
        if index == 0:
            continue
        if index % 2 == 1:
            heading = part.strip()
            continue
        if heading == AVOIDED_SECTION:
            for term, why in AVOIDED_ROW.findall(part):
                avoided[term_name(term)] = why
            continue
        for term in TABLE_TERM.findall(part):
            defined.add(term_name(term))
    return defined, avoided


def avoidance_pattern(term: str) -> re.Pattern[str]:
    """An avoided term in any case and in each form a sentence inflects it to.

    A plural, the third person, the past tense and the present participle
    are each the term, so `included` and `branching` state `include` and
    `branch`. A longer word is not the term: `compiler` does not state
    `compile`, and the glossary names it apart where it avoids it too.
    """
    if term.endswith("e"):
        inflected = rf"{re.escape(term[:-1])}(?:e|es|ed|ing)"
    else:
        inflected = rf"{re.escape(term)}(?:s|es|ed|ing)?"
    return re.compile(rf"\b{inflected}\b", re.IGNORECASE)


def prose(page: str) -> str:
    """A page as the words it states, line for line.

    Code, as `strip_code` blanks it, and a link's destination name something
    rather than state it, so each is blanked. A code span is how a page
    quotes a term rather than using it. A table under the heading
    `AVOIDED_SECTION` names the terms it holds rather than using them, so its
    rows are blanked too; that table is the glossary's own.
    """
    lines = []
    heading = None
    for line in LINK_DESTINATION.sub("]", strip_code(page)).splitlines():
        marked = SECTION.match(line)
        if marked:
            heading = marked.group(1).strip()
        avoiding = heading == AVOIDED_SECTION and line.lstrip().startswith("|")
        lines.append("" if avoiding else line)
    return "\n".join(lines)


def avoided_uses(page: str, avoided: dict[str, str]) -> Iterator[tuple[int, str, str]]:
    """Each avoided term a page states, as its line, its spelling and the term."""
    patterns = {term: avoidance_pattern(term) for term in sorted(avoided)}
    for number, line in enumerate(prose(page).splitlines(), 1):
        for term, pattern in patterns.items():
            for match in pattern.finditer(line):
                yield number, match.group(0), term


def pages() -> list[Path]:
    """Every document under `docs/`, as `documents.documents` finds them."""
    return [path for path in documents() if path.is_relative_to(DOCS)]


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
        if holds(term, set(avoided)):
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

    read = pages()
    for page in read:
        name = page.relative_to(ROOT).as_posix()
        for number, found, term in avoided_uses(page.read_text(), avoided):
            failures.append(
                f"{name}:{number} states {found!r} — docs/glossary.md deliberately "
                f"does not use {term}: {avoided[term]}"
            )

    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if failures:
        print(
            f"\nvocabulary check: {len(failures)} term(s) the glossary, the "
            "contract and the documentation disagree on",
            file=sys.stderr,
        )
        return 1
    print(
        f"vocabulary check: {len(inventory)} contract term(s) marked in "
        f"{design_path} on {ref}, every one defined in docs/glossary.md, and every "
        f"definition carried by the contract across {len(sources)} source(s), and "
        f"no avoided term stated across {len(read)} page(s) under docs/"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
