#!/usr/bin/env python3
"""Assert the corpus and its report state the contract's vocabulary and no other.

The corpus is what a second implementation of the contract is held to, so a
fixture naming a module, a language or the wording one build gives a fault
states a requirement that can only be met by copying the first build. The
manifest schema states that nothing in a manifest names an implementation
and the runner reaches its build through configuration so that it names
none, but both are facts about the shape of a declaration. A description, a
clause, a carried substring and a fixture's own identity are free text, and
free text is where such a term arrives.

The bound is the vocabulary a declaration is entitled to use. The design
states the contract's words, `docs/glossary.md` defines each term the
design marks, the manifest schema and the documented invocation declare the
contract's interface by name, and `docs/corpus-vocabulary.md` registers the
words the corpus's own declarations and this report's entries add. A word
outside all four is a term the contract does not state, and is reported
wherever a claim carries it. Nothing is refused by name, so a term is not
reached by spelling it differently: a word the vocabulary does not hold is
reported whatever it names.

What is scanned is the claims, not the documents under test. A fixture's
source tree and the bytes it expects back are the input the run consumes
and the output it must reproduce: the corpus deliberately bundles real
documents that name real source files, and holding those to the rule would
refuse the corpus its realism without saying anything about what the corpus
binds. The paths, reference texts and arguments a manifest declares name
that same tree, and the harness check holds each of them to the files the
fixture carries, so they are read as the tree they name rather than as
words. The conformance report is scanned whole, which brings the design's
own clause names and the declared surface under the same rule. That
surface states the codes the build under test reports for itself, so this
check reaches the build the conformance report reads — named by
configuration, as the corpus names it — and fails without one. A code the
build reports that the contract declares nowhere is rendered into the
report and so is read against the vocabulary like every other entry.

A word is read as the contract states it rather than as a sentence inflects
it: plurals, the past tense, the present participle and the adverb resolve
to the word they are formed from, and a hyphenated compound is its parts.
Case is folded on the reading side, so `Python` is the word `python`. It is
not folded on the stating side: a word the design writes only capitalised
names a product, a language or a build rather than stating a term of the
contract, so the design's prose contributes the words it writes in lower
case, and the names the design gives its own clauses whatever their case.
"""

import re
import sys
from collections.abc import Collection
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

README = ROOT / "README.md"
REGISTER = ROOT / "docs" / "corpus-vocabulary.md"
OPTION = "Option"
REPORT = "the conformance report"

WORD = re.compile(r"(?<![A-Za-z])[A-Za-z](?:\+\+|#)|[A-Za-z][A-Za-z']*")
LOWER = re.compile(r"(?<![A-Za-z])[a-z][a-z']*(?![A-Za-z])")
CODE_SPAN = re.compile(r"`[^`\n]*`")
LINK_DESTINATION = re.compile(r"\]\([^)\n]*\)")
TABLE_TERM = re.compile(r"^\|\s*\*\*([^*]+)\*\*", re.MULTILINE)
DOUBLED = re.compile(r"([bdfglmnprt])\1$")

CARRIED = "message_contains"
DESCRIPTION = "description"
DIAGNOSTICS = "diagnostics"
EXPECTED = "expected"
STDOUT_CARRIED = "stdout_contains"


@dataclass(frozen=True)
class Reference:
    """One word a claim states that the contract's vocabulary does not."""

    where: str
    found: str


def forms(word: str) -> set[str]:
    """The word as written and as the word it is formed from.

    One spelling of a word stands for the contract's term however a
    sentence inflects it, so a claim writing `documents` states the word
    the design writes as `document`.
    """
    spelling = word.lower().replace("'", "")
    found = {spelling}
    if spelling.endswith("ied") and len(spelling) > 4:
        found.add(spelling[:-3] + "y")
    if spelling.endswith("ies") and len(spelling) > 4:
        found.add(spelling[:-3] + "y")
    if re.search(r"(?:s|x|z|ch|sh)es$", spelling):
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
    if spelling.endswith("ly") and len(spelling) > 4:
        found.add(spelling[:-2])
    return found


def words(text: str) -> list[str]:
    """Every word one piece of text states, a hyphenated compound as its parts.

    A single letter names nothing on its own, and the one a language is
    named by carries its sign with it, so `c++` is a word and the `a` of a
    sentence is not.
    """
    return [found for found in WORD.findall(text.replace("-", " ")) if len(found) > 1]


def prose(text: str) -> str:
    """One document as the words it states, its code and its addresses apart.

    A code span and a link destination name something rather than stating
    it, so neither contributes to the vocabulary nor is read as a claim.
    """
    return LINK_DESTINATION.sub("]", CODE_SPAN.sub(" ", text))


def registered(text: str) -> list[str]:
    """Every word a register of vocabulary admits, as its tables name them."""
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


def vocabulary(
    design: str, glossary: str, documentation: str, register: str
) -> set[str]:
    """Every word a claim is entitled to state.

    The design's prose states the contract's own words, the glossary's
    terms and the design's clause names state what it calls things, the
    documented invocation and the schema declare its interface, and the
    register admits the words the corpus's declarations add.
    """
    stated: set[str] = set()
    for word in LOWER.findall(prose(design)):
        if len(word) > 1:
            stated |= forms(word)
    for clause in clauses(design):
        for word in words(clause.name):
            stated |= forms(word)
    for source in (registered(glossary), registered(register)):
        for term in source:
            for word in words(term):
                stated |= forms(word)
    for name in declared_names(documentation):
        for word in words(name):
            stated |= forms(word)
    return stated


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


def scan(text: str, where: str, stated: set[str]) -> list[Reference]:
    """Every word one claim states that the vocabulary does not hold.

    A word a claim repeats is one reference: the claim is a single
    statement, and naming the word once locates the claim to fix.
    """
    found: dict[str, Reference] = {}
    for word in words(prose(text)):
        if forms(word) & stated:
            continue
        found.setdefault(word.lower(), Reference(where, word))
    return sorted(found.values(), key=lambda reference: reference.found.lower())


def corpus_references(corpus: Path, stated: set[str]) -> list[Reference]:
    """Every word the corpus's declarations state that the vocabulary does not."""
    found = []
    for fixture in fixtures(corpus):
        where = identity(fixture, corpus)
        declared = claims(read(fixture / MANIFEST_NAME), where)
        found += scan("\n".join(declared), where, stated)
    return found


def report_references(
    design: str, corpus: Path, stated: set[str], reported: Collection[str]
) -> list[Reference]:
    """Every word the report's entries state that the vocabulary does not."""
    rendered = render(report(design, corpus, reported)).splitlines()
    return [
        reference
        for number, line in enumerate(rendered, start=1)
        for reference in scan(line, f"{REPORT}, line {number}", stated)
    ]


@cache
def sources() -> tuple[str, str]:
    """The design the contract is stated on, and the path it is read from."""
    branch, path = design_reference()
    return git_show(git_ref(branch), path), path


def check() -> tuple[list[str], list[Reference]]:
    """The corpus's declarations and the report, each read against the vocabulary."""
    design, path = sources()
    documentation = README.read_text()
    stated = vocabulary(
        design,
        SHIPPED_GLOSSARY.read_text(),
        documentation,
        REGISTER.read_text(),
    )

    corpus = corpus_references(CORPUS, stated)
    emitted = report_references(design, CORPUS, stated, reported_codes())

    counted = [
        f"ok   vocabulary  {len(stated)} word(s) from {path}, docs/glossary.md, "
        f"{len(declared_names(documentation))} declared name(s) and "
        "docs/corpus-vocabulary.md",
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
            f"FAIL {reference.where}: {reference.found!r} is a word the contract's "
            "vocabulary does not state",
            file=sys.stderr,
        )
    if failures:
        print(
            f"\nindependence check: {len(failures)} term(s) the contract "
            "does not state",
            file=sys.stderr,
        )
        return 1
    print(
        "\nindependence check: every word of every fixture declaration and every "
        "report entry is one the contract states"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
