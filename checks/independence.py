#!/usr/bin/env python3
"""Assert the corpus and its report bind behaviour rather than an implementation.

The corpus is what a second implementation of the contract is held to, so a
fixture naming a module, a language or the wording one build gives a fault
states a requirement that can only be met by copying the first build. The
manifest schema states that nothing in a manifest names an implementation
and the runner reaches its build through configuration so that it names
none, but both are facts about the shape of a declaration. A description, a
clause, a carried substring and a clause name the design states are free
text, and free text is where such a term arrives.

What is scanned is the claims, not the documents under test. A manifest
states what its fixture establishes about the contract, so every string it
declares is held to this rule, as is the fixture's own identity. A
fixture's source tree and the bytes it expects back are the input the run
consumes and the output it must reproduce: the corpus deliberately bundles
real documents that name real source files, and holding those to the rule
would refuse the corpus its realism without saying anything about what the
corpus binds. The conformance report is scanned whole, which brings the
design's own clause names and the declared surface under the same rule.

The inventory is three kinds of term: an implementation language or
runtime, the machinery of modules and packaging with the source-file paths
and reserved identifiers that go with it, and the wording a build's fault
reporting uses in place of the contract's codes. Each term says what it
names, so a hit reads as the reason it is refused.

The contract's own declared names are interface terms: the error codes, the
warning codes and the exit statuses the schema declares, and the options
the documented invocation names. They are held apart from the inventory
rather than subtracted from each scanned text — the check scans those
declared names themselves, and one matching the inventory is a reported
failure. The two sets are then disjoint by the check's own verdict, the
scan needs no exclusion of its own, and a contract that came to declare an
implementation term is reported rather than quietly admitted.
"""

import re
import sys
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

from conformance import render, report
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
from vocabulary import design_reference, git_ref, git_show

README = ROOT / "README.md"
OPTION = "Option"
REPORT = "the conformance report"

LANGUAGES = (
    "an implementation language or runtime",
    (
        "python",
        "cpython",
        "pypy",
        "rust",
        "golang",
        "java",
        "jvm",
        "kotlin",
        "scala",
        "clojure",
        "javascript",
        "typescript",
        "nodejs",
        "node.js",
        "deno",
        "ruby",
        "perl",
        "php",
        "haskell",
        "erlang",
        "elixir",
        "swift",
        "dotnet",
        "csharp",
        "ocaml",
    ),
)

MACHINERY = (
    "the machinery of modules and packaging",
    (
        "module",
        "submodule",
        "package",
        "namespace",
        "classpath",
        "import",
        "venv",
        "virtualenv",
        "pip",
        "pypi",
        "setuptools",
        "pyproject",
        "sdist",
        "wheel",
        "npm",
        "cargo",
        "crate",
        "maven",
        "gradle",
        "gemspec",
        "stdlib",
        "dunder",
    ),
)

WORDING = (
    "the wording a build gives its own fault",
    (
        "traceback",
        "stacktrace",
        "stack trace",
        "panic",
        "unwrap",
        "errno",
        "segfault",
        "segmentation fault",
        "core dump",
        "assertion failed",
    ),
)

SOURCE_SUFFIXES = (
    "py",
    "pyi",
    "pyc",
    "rs",
    "go",
    "ts",
    "tsx",
    "js",
    "mjs",
    "cjs",
    "rb",
    "java",
    "jar",
    "kt",
    "swift",
    "cs",
    "cpp",
    "cc",
    "hpp",
    "php",
    "pl",
    "whl",
)

SHAPES = (
    (
        re.compile(
            r"(?<![\w/.-])[\w./-]*\.(?:" + "|".join(SOURCE_SUFFIXES) + r")(?![\w-])"
        ),
        "a source file of an implementation",
    ),
    (re.compile(r"\b__\w+__\b"), "an identifier a language reserves"),
    (
        re.compile(r"\b[A-Z][A-Za-z]*(?:Error|Exception)\b"),
        "a fault class of an implementation",
    ),
    (
        re.compile(r"(?<![\w+])c\+\+(?![\w+])", re.IGNORECASE),
        "an implementation language",
    ),
    (re.compile(r"(?<![\w#])c#(?![\w#])", re.IGNORECASE), "an implementation language"),
)


@dataclass(frozen=True)
class Reference:
    """One implementation term found in text the contract's claims are made in."""

    where: str
    found: str
    names: str


@cache
def inventory() -> tuple[tuple[re.Pattern[str], str], ...]:
    """Every form of implementation reference, each with what it names.

    The named terms come before the shapes, so a span both describe is
    read as the term it is rather than as the shape it fits.
    """
    named = [
        (re.compile(rf"(?<!\w){re.escape(term)}(?!\w)", re.IGNORECASE), names)
        for names, terms in (LANGUAGES, MACHINERY, WORDING)
        for term in terms
    ]
    return tuple(named) + SHAPES


def scan(text: str, where: str) -> list[Reference]:
    """Every implementation term one piece of text names, each named once.

    A term one piece of text names repeatedly is one reference: the text
    is a single claim, and naming it once locates the claim to fix.
    """
    found: dict[str, Reference] = {}
    for pattern, names in inventory():
        for match in pattern.finditer(text):
            found.setdefault(
                match.group(0).lower(), Reference(where, match.group(0), names)
            )
    return sorted(found.values(), key=lambda reference: reference.found.lower())


def strings(value: Any) -> list[str]:
    """Every string a parsed manifest declares, at whatever depth it declares it."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [found for item in value.values() for found in strings(item)]
    if isinstance(value, list):
        return [found for item in value for found in strings(item)]
    return []


def corpus_references(corpus: Path) -> list[Reference]:
    """Every implementation term the corpus's declarations name."""
    found = []
    for fixture in fixtures(corpus):
        where = identity(fixture, corpus)
        declared = [where] + strings(read(fixture / MANIFEST_NAME))
        found += scan("\n".join(declared), where)
    return found


def report_references(design: str, corpus: Path) -> list[Reference]:
    """Every implementation term the conformance report's entries name."""
    rendered = render(report(design, corpus)).splitlines()
    return [
        reference
        for number, line in enumerate(rendered, start=1)
        for reference in scan(line, f"{REPORT}, line {number}")
    ]


def declared_names(text: str) -> list[str]:
    """Every name the contract declares as its interface.

    The codes and the exit statuses come from the manifest schema, which is
    where the corpus reads them, and the options from the tables the
    documented invocation enumerates them in.
    """
    return (
        [str(status) for status in statuses()]
        + [code for severity in severities() for code in sorted(catalogue(severity))]
        + [plain(record.get(OPTION, "")) for record in rows(text, OPTION)]
    )


def declared_references(text: str) -> list[Reference]:
    """Every interface term the contract declares that the inventory would refuse."""
    return [
        reference
        for name in declared_names(text)
        for reference in scan(name, f"the contract's declared name {name}")
    ]


def check() -> tuple[list[str], list[Reference]]:
    """The corpus, the report and the contract's declared names, each scanned."""
    branch, path = design_reference()
    design = git_show(git_ref(branch), path)
    documentation = README.read_text()

    corpus = corpus_references(CORPUS)
    emitted = report_references(design, CORPUS)
    declared = declared_references(documentation)

    counted = [
        f"ok   corpus      {len(fixtures(CORPUS))} fixture(s) and their identities",
        f"ok   report      {REPORT} as it renders",
        f"ok   interface   {len(declared_names(documentation))} declared name(s)",
    ]
    return counted, corpus + emitted + declared


def main() -> int:
    passed, failures = check()
    for line in passed:
        print(line)
    for reference in failures:
        print(
            f"FAIL {reference.where}: {reference.found!r} names {reference.names}",
            file=sys.stderr,
        )
    if failures:
        print(
            f"\nindependence check: {len(failures)} implementation reference(s)",
            file=sys.stderr,
        )
        return 1
    print(
        f"\nindependence check: {len(inventory())} term(s), named by no fixture "
        f"declaration, no report entry and no name the contract declares"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
