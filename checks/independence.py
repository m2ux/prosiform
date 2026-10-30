#!/usr/bin/env python3
"""Assert the corpus and its report name no implementation.

The corpus is what a second implementation of the contract is held to, so a
fixture naming a module, a language or the wording one build gives a fault
states a requirement that can only be met by copying the first build. The
manifest schema states that nothing in a manifest names an implementation
and the runner reaches its build through configuration so that it names
none, but both are facts about the shape of a declaration. A description, a
clause, a carried substring and a fixture's own identity are free text, and
free text is where such a term arrives.

A term names an implementation by its shape, not by its spelling. A struct
field, a function, a package, a constant and a language name all carry a
capital, an underscore or a dot: `KeyError`, `E_ROOT_NOT_FOUND`,
`prosiform.group`, `Python`. The prose a claim is written in carries none of
these, so the shape alone separates the two, and no list of admitted words
is needed to tell them apart.

A shaped term is admissible where the contract states it: the design's
prose, the names the design gives its own clauses, the terms
`docs/glossary.md` defines, and the interface the manifest schema and the
documented invocation declare by name — the codes, severities, exit
statuses and options. A shaped term the contract states is the contract's
own name for something; a shaped term it does not state is a build's.

What is scanned is the claims, not the documents under test. A fixture's
source tree and the bytes it expects back are the input the run consumes
and the output it must reproduce: the corpus deliberately bundles real
documents that name real source files, and holding those to the rule would
refuse the corpus its realism without saying anything about what the corpus
binds. The paths, reference texts and arguments a manifest declares name
that same tree, and the harness check holds each of them to the files the
fixture carries, so they are read as the tree they name rather than as
terms. A dotted term written as a path in a claim names that same tree, and
is read the same way. The conformance report is scanned whole, which brings
the design's own clause names and the declared surface under the same rule.
That surface states the codes the build under test reports for itself, so
this check reaches the build the conformance report reads — named by
configuration, as the corpus names it — and fails without one.

A term is read as the contract states it rather than as a sentence inflects
it: a plural, the past tense and the present participle resolve to the term
they are formed from. Case is folded on both sides, so a claim writing
`python` and one writing `Python` are the same term.
"""

import re
import sys
from collections.abc import Collection, Sequence
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

from conformance import clauses, render, report, reported_codes
from documents import ROOT, plain, rows
from manifests import (
    CORPUS,
    MANIFEST_NAME,
    catalogue,
    fixtures,
    identity,
    read,
    severities,
    statuses,
)
from runner import BuildNotConfigured
from vocabulary import SHIPPED_GLOSSARY, design_reference, git_ref, git_show

INVOCATION = ROOT / "invocation.md"
EXAMPLE = ROOT / "example"
OPTION = "Option"
REPORT = "the conformance report"

WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
DOTTED = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)+")
DOUBLED = re.compile(r"([bdfglmnprt])\1$")
PATH_NAME = re.compile(r"\.(?:md|toml|json|ya?ml|txt)$", re.IGNORECASE)
HEADING = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)
CODE_SPAN = re.compile(r"`[^`\n]*`")
LINK_DESTINATION = re.compile(r"\]\([^)\n]*\)")
TABLE_TERM = re.compile(r"^\|\s*\*\*([^*]+)\*\*", re.MULTILINE)

CARRIED = "message_contains"
DESCRIPTION = "description"
DIAGNOSTICS = "diagnostics"
EXPECTED = "expected"
STDOUT_CARRIED = "stdout_contains"


@dataclass(frozen=True)
class Reference:
    """One shaped term a claim states that the contract does not."""

    where: str
    found: str


def forms(term: str) -> set[str]:
    """The term as written and as the term it is formed from.

    One spelling of a term stands for the contract's name however a
    sentence inflects it, so a claim writing `documents` states the term
    the design writes as `document`.
    """
    spelling = term.lower()
    found = {spelling}
    if spelling.endswith("ies") and len(spelling) > 4:
        found.add(spelling[:-3] + "y")
    elif spelling.endswith("es") and len(spelling) > 4:
        found.add(spelling[:-2])
    if spelling.endswith("s") and not spelling.endswith("ss") and len(spelling) > 3:
        found.add(spelling[:-1])
    if spelling.endswith("ing") and len(spelling) > 5:
        found.add(spelling[:-3])
        found.add(DOUBLED.sub(r"\1", spelling[:-3]))
        found.add(spelling[:-3] + "e")
    elif spelling.endswith("ed") and len(spelling) > 4:
        found.add(spelling[:-2])
        found.add(DOUBLED.sub(r"\1", spelling[:-2]))
        found.add(spelling[:-1])
    return found


def shaped(term: str, opening: bool = False) -> bool:
    """Whether a term carries the shape an implementation names something by.

    An underscore, a dot or a capital past the term's first letter is what a
    type, a function, a field, a constant, a package and a language share.
    A term that merely opens with a capital is orthography, and one written
    in full capitals names a format or an encoding, so `opening` is answered
    by the caller, which knows the sentence, and an all-capital term is
    admitted by the contract's own vocabulary like any other term.
    """
    if "_" in term or "." in term:
        return True
    if term.isupper() and len(term) > 1:
        return False
    if any(character.isupper() for character in term[1:]):
        return True
    return not opening and term[:1].isupper()


def prose(text: str) -> str:
    """One document as the terms it states, its code and its addresses apart.

    A code span and a link destination name something rather than stating
    it, so neither contributes to the contract's own names nor is read as
    a claim.
    """
    return LINK_DESTINATION.sub("]", CODE_SPAN.sub(" ", text))


def registered(text: str) -> list[str]:
    """Every term the contract defines, as its tables name them."""
    return [plain(term).strip() for term in TABLE_TERM.findall(text)]


def declared_names(text: str) -> list[str]:
    """Every name the contract declares as its interface.

    The codes, the severities and the exit statuses come from the manifest
    schema, which is where the corpus reads them, and the options from the
    tables the documented invocation enumerates them in.
    """
    return (
        [str(status) for status in statuses()]
        + list(severities())
        + [code for severity in severities() for code in sorted(catalogue(severity))]
        + [plain(record.get(OPTION, "")) for record in rows(text, OPTION)]
    )


def example_headings() -> list[str]:
    """Every heading the example tree carries, which the corpus bundles by name.

    A usage-example fixture names the documents it bundles by the headings
    those documents carry, so a title there names the corpus's own source
    rather than a build. The tree is read rather than listed, so a heading
    added to it needs no second registration.
    """
    return [
        title.strip()
        for path in sorted(EXAMPLE.rglob("*.md"))
        for title in HEADING.findall(path.read_text(encoding="utf-8"))
    ]


def stated(
    design: str, glossary: str, documentation: str, examples: Sequence[str] = ()
) -> set[str]:
    """Every term the contract names.

    The design's prose states the contract's own words, the design's clause
    names state what it calls things, the glossary's terms define them, the
    documented invocation and the schema declare its interface, and the
    example tree's headings name the documents the corpus bundles.
    """
    names: set[str] = set()
    for term in re.findall(r"[A-Za-z_][A-Za-z0-9_.]*", prose(design)):
        names |= forms(term)
    for clause in clauses(design):
        for term in WORD.findall(clause.name):
            names |= forms(term)
    for source in (
        registered(glossary),
        declared_names(documentation),
        examples,
    ):
        for term in source:
            for word in WORD.findall(term):
                names |= forms(word)
    return names


def claims(manifest: dict[str, Any], where: str) -> list[str]:
    """Every claim one fixture's declaration makes, its own identity among them.

    A fixture states what it establishes, the clauses it encodes and the
    text an output must carry. Its paths, its reference texts and its
    arguments name the tree it carries, which the run consumes rather than
    the contract binds.
    """
    expected = manifest.get(EXPECTED, {})
    carried = [
        text
        for diagnostic in expected.get(DIAGNOSTICS, [])
        for text in diagnostic.get(CARRIED, [])
    ]
    return (
        [where, manifest.get(DESCRIPTION, "")]
        + list(manifest.get("clauses", []))
        + list(expected.get(STDOUT_CARRIED, []))
        + carried
    )


def opening_at(body: str, position: int) -> bool:
    """Whether the term at `position` opens the sentence it is written in.

    A sentence opens at its first word, after the punctuation that ends
    one, and after a list or table marker standing alone, which a term then
    follows. A hyphen does not open one: the fixtures write a fixture's
    identity with hyphens, and the compound a sentence carries reads as one
    word either side of it.
    """
    before = body[:position]
    stripped = before.rstrip(" \t")
    if not stripped or stripped[-1] in ".!?:;(\"'\n":
        return True
    last_line = before.rsplit("\n", 1)[-1]
    return not last_line.strip(" \t#-*|>0123456789.")


def scan(text: str, where: str, names: set[str]) -> list[Reference]:
    """Every shaped term one claim states that the contract does not.

    A term a claim repeats is one reference: the claim is a single
    statement, and naming the term once locates the claim to fix. A dotted
    term is read whole, because `prosiform.group` names a key where its
    parts name a document and a grouping; a term carrying a path's
    extension names the tree the claim is about and is read as that tree.
    """
    body = prose(text)
    found: dict[str, Reference] = {}
    seen: set[int] = set()
    for match in DOTTED.finditer(body):
        term = match.group().strip(".")
        seen.update(range(match.start(), match.end()))
        if PATH_NAME.search(term):
            continue
        parts = term.split(".")
        if all(forms(part) & names for part in parts):
            continue
        found.setdefault(term.lower(), Reference(where, term))
    for match in WORD.finditer(body):
        if match.start() in seen:
            continue
        term = match.group().strip("_")
        if not term:
            continue
        if not shaped(term, opening_at(body, match.start())):
            continue
        if PATH_NAME.search(term):
            continue
        if forms(term) & names:
            continue
        found.setdefault(term.lower(), Reference(where, term))
    return sorted(found.values(), key=lambda reference: reference.found.lower())


def corpus_references(corpus: Path, names: set[str]) -> list[Reference]:
    """Every shaped term the corpus's declarations state that the contract does not."""
    found = []
    for fixture in fixtures(corpus):
        where = identity(fixture, corpus)
        declared = claims(read(fixture / MANIFEST_NAME), where)
        found += scan("\n".join(declared), where, names)
    return found


def report_references(
    design: str, corpus: Path, names: set[str], reported: Collection[str]
) -> list[Reference]:
    """Every shaped term the report's entries state that the contract does not."""
    rendered = render(report(design, corpus, reported)).splitlines()
    return [
        reference
        for number, line in enumerate(rendered, start=1)
        for reference in scan(line, f"{REPORT}, line {number}", names)
    ]


@cache
def sources() -> tuple[str, str]:
    """The design the contract is stated on, and the path it is read from."""
    branch, path = design_reference()
    return git_show(git_ref(branch), path), path


def check() -> tuple[list[str], list[Reference]]:
    """The corpus's declarations and the report, each read against the contract."""
    design, path = sources()
    documentation = INVOCATION.read_text()
    names = stated(
        design, SHIPPED_GLOSSARY.read_text(), documentation, example_headings()
    )

    corpus = corpus_references(CORPUS, names)
    emitted = report_references(design, CORPUS, names, reported_codes())

    counted = [
        (
            f"ok   vocabulary  {len(names)} term(s) from {path}, docs/glossary.md "
            f"and {len(declared_names(documentation))} declared name(s)"
        ),
        f"ok   corpus      {len(fixtures(CORPUS))} fixture(s) and their identities",
        f"ok   report      {REPORT} as it renders",
    ]
    return counted, corpus + emitted


def main() -> int:
    try:
        passed, failures = check()
    except BuildNotConfigured as absent:
        print(f"independence check: {absent}", file=sys.stderr)
        return 1
    for line in passed:
        print(line)
    for reference in failures:
        print(
            f"FAIL {reference.where}: {reference.found!r} is a term the contract "
            "does not name",
            file=sys.stderr,
        )
    if failures:
        print(
            f"\nindependence check: {len(failures)} shaped term(s) the contract "
            "does not name",
            file=sys.stderr,
        )
        return 1
    print(
        "\nindependence check: every shaped term of every fixture declaration and "
        "every report entry is one the contract names"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
