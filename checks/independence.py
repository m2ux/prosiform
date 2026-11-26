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
capital, an underscore or a dot: `KeyError`, `E_TARGET_NOT_FOUND`,
`prosiform.default.group`, `Python`. The prose a claim is written in carries
none of these, so the shape alone separates the two, and no list of admitted
words is needed to tell them apart.

A shaped term is admissible where the contract states it: the prose of the
design's behavioural sections, the names the design gives its own clauses, the terms
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

The design states the contract where it states behaviour. A section the
conformance report records as stating no behaviour states what the project
decided about its builds, what each is made with, what remains to be proven
of them and what an upstream contribution would say, so the terms it writes
in code spans are a build's words rather than the contract's. Such a term is a build's
however it is written: `crate` names packaging in lower case as plainly as
`Cargo` does with a capital, so it is reported whatever its shape. The rest
of that section's prose is the ordinary words its sentences are written in,
which name nothing. A claim quoting the tree its fixture carries states
that tree's words, so a word naming one of the tree's files is the tree's
rather than a build's.

The glossary names the terms it deliberately does not use and why each was
refused. A fixture's description is the text a second implementor reads
for what the contract means, and its identity is the name a reader meets
first, printed by the corpus report and named in every request for that
fixture, so each is the text that avoidance was written for. A description
or an identity stating an avoided term, in any segment of the identity's
path, is reported with the reason the glossary gives, whatever the design's
prose states: the design writes some of those words in their ordinary
sense. The other claims quote the design or a build — a clause the design
names and the bytes a build writes — and are held to the design's words by
the rules above.

A term is read as the contract states it rather than as a sentence inflects
it: a plural, the past tense and the present participle resolve to the term
they are formed from. Case is folded on both sides, so a claim writing
`python` and one writing `Python` are the same term.
"""

import re
import sys
from collections.abc import Collection
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

from conformance import clauses, partition, render, report, reported_codes
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
OPTION = "Option"
AVOIDED = "Avoided"
WHY = "Why"
REPORT = "the conformance report"

WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
DOTTED = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)+")
DOUBLED = re.compile(r"([bdfglmnprt])\1$")
PATH_NAME = re.compile(r"\.(?:md|toml|json|ya?ml|txt)$", re.IGNORECASE)
CODE_SPAN = re.compile(r"`[^`\n]*`")
LINK_DESTINATION = re.compile(r"\]\([^)\n]*\)")
TABLE_TERM = re.compile(r"^\|\s*\*\*([^*]+)\*\*", re.MULTILINE)

CARRIED = "message_contains"
DESCRIPTION = "description"
DIAGNOSTICS = "diagnostics"
EXPECTED = "expected"
STDOUT_CARRIED = "stdout_contains"


UNNAMED = "is a term the contract does not name"


@dataclass(frozen=True)
class Reference:
    """One term a claim states, and why the contract refuses it."""

    where: str
    found: str
    reason: str = UNNAMED


@dataclass(frozen=True)
class Vocabulary:
    """What the contract states, and the words it refuses.

    `names` holds every term the contract states, in each form a sentence
    inflects it to. `built` holds each form of a build word, against the
    name of the section stating no behaviour that marks it. `avoided` holds each
    term the glossary deliberately does not use, against the reason it
    gives.
    """

    names: set[str]
    built: dict[str, str]
    avoided: dict[str, str]


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


def marked(text: str) -> list[str]:
    """Every term one text marks, as the code of its code spans."""
    return [span[1:-1] for span in CODE_SPAN.findall(text)]


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


def avoided(glossary: str) -> dict[str, str]:
    """Each term the glossary deliberately does not use, against its reason."""
    return {
        plain(record.get(AVOIDED, "")).strip("* ").lower(): plain(record.get(WHY, ""))
        for record in rows(glossary, AVOIDED)
    }


def stated(design: str, glossary: str, documentation: str) -> Vocabulary:
    """Every term the contract names, and the words it refuses.

    The prose of the design's behavioural sections states the contract's
    own words, the design's clause names state what it calls things, the
    glossary's terms define them, the documented invocation and the schema
    declare its interface. A word of a term a section stating no behaviour
    marks, as `marked` reads it, that none of those states in any of its
    forms is a build's, the design divided as `conformance.partition`
    divides it. A word that section writes unmarked is not.
    """
    behavioural, silent = partition(design)
    names: set[str] = set()
    for term in re.findall(r"[A-Za-z_][A-Za-z0-9_.]*", prose(behavioural)):
        names |= forms(term.strip("."))
    for clause in clauses(design):
        for term in WORD.findall(clause.name):
            names |= forms(term)
    for source in (
        registered(glossary),
        declared_names(documentation),
    ):
        for term in source:
            for word in WORD.findall(term):
                names |= forms(word)
    built: dict[str, str] = {}
    for section, carried in silent.items():
        for word in WORD.findall(" ".join(marked(carried))):
            spellings = forms(word)
            if spellings & names:
                continue
            for spelling in spellings:
                built.setdefault(spelling, section)
    return Vocabulary(names, built, avoided(glossary))


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


def refused(
    term: str,
    opening: bool,
    vocabulary: Vocabulary,
    avoiding: bool,
    tree: Collection[str],
) -> str | None:
    """Why the contract refuses one word a claim states, or nothing.

    An avoided term is refused whatever the design's prose states, where
    the claim is one `avoiding` marks. A build word, as `stated` reads it,
    is refused whatever its shape, unless it is a word of
    the `tree` the claim's fixture carries, which a claim quoting that tree
    states as the tree's. A shaped word is refused where the contract does
    not name it.
    """
    spellings = forms(term)
    if avoiding:
        for avoided_term, why in sorted(vocabulary.avoided.items()):
            if avoided_term in spellings:
                return f"is a term docs/glossary.md deliberately does not use: {why}"
    if spellings & vocabulary.names:
        return None
    for spelling in [] if spellings & set(tree) else sorted(spellings):
        if spelling in vocabulary.built:
            return (
                f"is a build word the design's {vocabulary.built[spelling]!r} "
                "section marks, which states no behaviour"
            )
    if shaped(term, opening) and not PATH_NAME.search(term):
        return UNNAMED
    return None


def scan(
    text: str,
    where: str,
    vocabulary: Vocabulary,
    avoiding: bool = False,
    tree: Collection[str] = (),
) -> list[Reference]:
    """Every term one claim states that the contract refuses, as `refused` reads it.

    A term a claim repeats is one reference: the claim is a single
    statement, and naming the term once locates the claim to fix. A dotted
    term is read whole, because `prosiform.default.group` names a key where
    its parts name a declaration, a preset and a grouping; a term carrying a
    path's extension names the tree the claim is about and is read as that
    tree.
    """
    names = vocabulary.names
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
        reason = refused(
            term, opening_at(body, match.start()), vocabulary, avoiding, tree
        )
        if reason is not None:
            found.setdefault(term.lower(), Reference(where, term, reason))
    return sorted(found.values(), key=lambda reference: reference.found.lower())


def tree_words(fixture: Path) -> set[str]:
    """Every form of every word naming a file or directory one fixture carries."""
    return {
        spelling
        for path in fixture.rglob("*")
        for word in WORD.findall(path.name)
        for spelling in forms(word)
    }


def corpus_references(corpus: Path, vocabulary: Vocabulary) -> list[Reference]:
    """Every term the corpus's declarations state that the contract refuses.

    A fixture's identity and description are read for the glossary's
    avoided terms too, and a term they and another claim both state is one
    reference. The words naming the files a fixture carries are its tree.
    """
    found = []
    for fixture in fixtures(corpus):
        where = identity(fixture, corpus)
        manifest = read(fixture / MANIFEST_NAME)
        tree = tree_words(fixture)
        named = "\n".join([where, manifest.get(DESCRIPTION, "")])
        described = scan(named, where, vocabulary, True, tree)
        own = {reference.found.lower(): reference for reference in described}
        declared = "\n".join(claims(manifest, where))
        for reference in scan(declared, where, vocabulary, False, tree):
            own.setdefault(reference.found.lower(), reference)
        found += sorted(own.values(), key=lambda reference: reference.found.lower())
    return found


def report_references(
    design: str, corpus: Path, vocabulary: Vocabulary, reported: Collection[str]
) -> list[Reference]:
    """Every term the report's entries state that the contract refuses."""
    rendered = render(report(design, corpus, reported)).splitlines()
    return [
        reference
        for number, line in enumerate(rendered, start=1)
        for reference in scan(line, f"{REPORT}, line {number}", vocabulary)
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
    vocabulary = stated(design, SHIPPED_GLOSSARY.read_text(), documentation)

    corpus = corpus_references(CORPUS, vocabulary)
    emitted = report_references(design, CORPUS, vocabulary, reported_codes())

    counted = [
        (
            f"ok   vocabulary  {len(vocabulary.names)} term(s) from {path}, "
            f"docs/glossary.md and {len(declared_names(documentation))} declared "
            "name(s)"
        ),
        (
            f"ok   refused     {len(vocabulary.built)} build word form(s) and "
            f"{len(vocabulary.avoided)} avoided term(s)"
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
            f"FAIL {reference.where}: {reference.found!r} {reference.reason}",
            file=sys.stderr,
        )
    if failures:
        print(
            f"\nindependence check: {len(failures)} term(s) the contract refuses",
            file=sys.stderr,
        )
        return 1
    print(
        "\nindependence check: every shaped term of every fixture declaration and "
        "every report entry is one the contract names, none is a build word a "
        "section stating no behaviour marks, and no identity or description "
        "states an avoided term"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
