#!/usr/bin/env python3
"""Report which behavioural clause of the design each fixture exercises.

A fixture states the design clauses it encodes in its manifest, and the
design states those clauses. This report reads both and prints the mapping
between them, so coverage of the contract is measured rather than assumed.

A clause is a heading of the design, or an enumerated rule under one: a
bold-led bullet, a step of a numbered sequence, or a row of a table. A
heading names the rule its own prose states, `Block boundaries`, and a rule
under it is named by both, `Heading-only structural ancestors - Depth`. The
design's own title names the document rather than a rule of it.

A manifest names a clause exactly and may add the case it takes after a
comma, `Adversarial acceptance fixtures - Partial outlines, original skipped
heading levels`. The clause is the identifier and the case is what this
fixture establishes about it, so two fixtures taking different cases of one
clause both map to it. A declaration matching no clause fails the report:
the mapping is only as good as the declarations it reads, and one that
lands nowhere would otherwise leave a clause uncovered while reading as
covered.

A clause no manifest names is listed as uncovered. That listing is the
report's measurement rather than its verdict: a clause with no fixture is
work for the epic that owns it, and a report that failed on one would be red
until the whole contract is fixtured and would say nothing in the meantime.

The declared surface is the error codes, the warning codes and the exit
statuses the contract declares, each listed with the fixtures reaching it. A
fixture awaiting later work declares behaviour the build does not yet meet,
so an entry only such fixtures declare is one no run of the corpus reaches:
it is listed as unfixturable and the work those fixtures await is the reason.
An entry no fixture declares at all has no reason to state and fails the
report.

The build under test states the same surface from the other side: invoked
with `--codes` it writes every code it can report, and each code entry
records whether that listing carries it. The two statements are held to
each other in both directions — a code the contract declares that the
build reports nowhere, and a code the build reports that the contract
declares nowhere, each fail the report — so the set of codes a build
reports for itself is exactly the set the design declares. The build is
named by configuration, `PROSIFORM_BUILD` holding its command line as it
does for the corpus, so this report reaches an implementation as a command
line alone and fails without one.

The declared surface also lists the installation claims no run of the
corpus observes. An installation is not a thing a fixture can name: a
fixture declares a source tree and the bytes a run must return for it, and
the corpus reaches the build under test through configuration. Each claim
is therefore declared here, beside the surface this report renders, with
the reason the smoke run cannot reach it and what a run would have to do to
observe it. A claim a run comes to observe leaves the listing by leaving
this declaration.

The design is read from the branch and path the README's Design link names,
as the vocabulary check reads the same document, so no path into a dated
planning folder is written here.
"""

import re
import subprocess
import sys
from collections import Counter
from collections.abc import Collection
from dataclasses import dataclass
from pathlib import Path

from documents import ROOT, cells, is_delimiter, plain
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
from runner import BUILD, BuildNotConfigured, build_under_test
from vocabulary import design_reference, git_ref, git_show

FENCE = re.compile(r"^(?:```|~~~)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")
BULLET = re.compile(r"^- \*\*(.+?)[:.]?\*\*")
STEP = re.compile(r"^(\d+)\.\s+\S")
SEPARATOR = " — "
AWAITING = "awaiting"
CODES = "--codes"
STATUS_KIND = "exit status"
REPORTED_KIND = "reported code"


class Unreadable(Exception):
    """Something the report needs that the run could not read."""


def reported_codes() -> tuple[str, ...]:
    """Every code the build under test reports, in the order it writes them."""
    command = build_under_test() + [CODES]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )
    if result.returncode != 0:
        raise Unreadable(
            f"the build {BUILD} names exited {result.returncode} for {CODES}\n"
            f"{result.stderr.strip()}"
        )
    return tuple(
        stripped for line in result.stdout.splitlines() if (stripped := line.strip())
    )


@dataclass(frozen=True)
class Clause:
    """One addressable rule of the design."""

    heading: str
    rule: str | None

    @property
    def name(self) -> str:
        if self.rule is None:
            return self.heading
        return f"{self.heading}{SEPARATOR}{self.rule}"


@dataclass(frozen=True)
class Entry:
    """One name the contract declares, with the fixtures declaring it."""

    kind: str
    name: str
    reached: tuple[str, ...]
    awaited: dict[str, tuple[str, ...]]
    reported: bool | None
    """Whether the build reports this name, and nothing for an exit status."""

    @property
    def unfixturable(self) -> bool:
        """Whether only fixtures awaiting later work declare it."""
        return not self.reached and bool(self.awaited)

    @property
    def undeclared(self) -> bool:
        return not self.reached and not self.awaited


@dataclass(frozen=True)
class Claim:
    """One installation claim no run of the corpus observes."""

    name: str
    reason: str
    observable: str


CLAIMS = (
    Claim(
        name="another platform",
        reason=(
            "the smoke run observes this host and the continuous-integration "
            "runner, and a platform whose command wrapper and path resolution "
            "differ is a different mechanism"
        ),
        observable=(
            "observable once a run installs the build and invokes it by name "
            "on that platform"
        ),
    ),
    Claim(
        name="a machine that never held the repository",
        reason=(
            "the repository is on disk throughout the run and merely "
            "unreachable by path, working directory and environment, and "
            "removing it is not something a check inside it can do"
        ),
        observable=(
            "observable once a run installs the build on a machine the "
            "repository was never copied to"
        ),
    ),
    Claim(
        name="the command line the documentation gives a reader",
        reason=(
            "the run installs an artefact it builds rather than running the "
            "command line the documentation's installation section states"
        ),
        observable=(
            "observable once a run executes that documented command line and "
            "invokes the command it installs"
        ),
    ),
)


@dataclass(frozen=True)
class Report:
    """The conformance report: the mapping, its gaps and the declared surface."""

    mapping: tuple[tuple[Clause, tuple[str, ...]], ...]
    unnamed: tuple[tuple[str, tuple[str, ...]], ...]
    surface: tuple[Entry, ...]
    surplus: tuple[str, ...]
    """The codes the build reports that the contract declares nowhere."""

    @property
    def uncovered(self) -> tuple[Clause, ...]:
        return tuple(clause for clause, named in self.mapping if not named)

    @property
    def unreported(self) -> tuple[Entry, ...]:
        """Each code the contract declares that the build reports nowhere."""
        return tuple(entry for entry in self.surface if entry.reported is False)

    @property
    def failures(self) -> tuple[str, ...]:
        return tuple(
            [
                f"{declaration} is declared by "
                f"{', '.join(where)} and names no clause the design states"
                for declaration, where in self.unnamed
            ]
            + [
                f"{entry.kind} {entry.name} is declared by the contract and by no "
                "fixture, so the corpus states nothing about the run it names"
                for entry in self.surface
                if entry.undeclared
            ]
            + [
                f"{entry.kind} {entry.name} is declared by the contract and the "
                "build reports it nowhere"
                for entry in self.unreported
            ]
            + [
                f"{name} is reported by the build and the contract declares it nowhere"
                for name in self.surplus
            ]
        )


def text(markup: str) -> str:
    """One piece of design markup as the words it states."""
    return plain(markup.replace("\\|", "|"))


def clauses(design: str) -> list[Clause]:
    """Every clause the design states, in the order it states them."""
    found: list[Clause] = []
    heading: str | None = None
    fenced = False
    delimited = False
    for line in design.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        marked = HEADING.match(line)
        if marked:
            heading = None if len(marked.group(1)) == 1 else text(marked.group(2))
            delimited = False
            if heading is not None:
                found.append(Clause(heading, None))
            continue
        if heading is None:
            continue
        rule = None
        bullet = BULLET.match(line)
        step = STEP.match(line)
        if bullet:
            rule = text(bullet.group(1))
        elif step:
            rule = f"step {step.group(1)}"
        elif line.strip().startswith("|"):
            row = cells(line)
            if is_delimiter(line):
                delimited = True
                continue
            rule = text(row[0]) if delimited and row else None
        if rule:
            found.append(Clause(heading, rule))
    return found


def declarations(corpus: Path) -> list[tuple[str, str]]:
    """Each clause a manifest declares, against the fixture declaring it."""
    return [
        (declaration, identity(fixture, corpus))
        for fixture in fixtures(corpus)
        for declaration in read(fixture / MANIFEST_NAME)["clauses"]
    ]


def named(declaration: str, inventory: set[str]) -> str | None:
    """The clause a declaration names, before the case it adds after a comma."""
    parts = declaration.split(",")
    for count in range(len(parts), 0, -1):
        candidate = ",".join(parts[:count]).strip()
        if candidate in inventory:
            return candidate
    return None


def surface(corpus: Path, reported: Collection[str]) -> list[Entry]:
    """Each code and exit status the contract declares, and what declares it."""
    declared: dict[tuple[str, str], list[tuple[str, str | None]]] = {}
    for fixture in fixtures(corpus):
        manifest = read(fixture / MANIFEST_NAME)
        where = identity(fixture, corpus)
        awaiting = manifest.get(AWAITING)
        expected = manifest["expected"]
        names = [(STATUS_KIND, str(expected["exit_status"]))] + [
            (diagnostic["severity"], diagnostic["code"])
            for diagnostic in expected["diagnostics"]
        ]
        for name in set(names):
            declared.setdefault(name, []).append((where, awaiting))
    inventory = [(STATUS_KIND, str(status)) for status in statuses()] + [
        (severity, code)
        for severity in severities()
        for code in sorted(catalogue(severity))
    ]
    entries = []
    for kind, name in inventory:
        found = declared.get((kind, name), [])
        awaited: dict[str, list[str]] = {}
        for where, awaiting in found:
            if awaiting is not None:
                awaited.setdefault(awaiting, []).append(where)
        entries.append(
            Entry(
                kind=kind,
                name=name,
                reached=tuple(where for where, awaiting in found if awaiting is None),
                awaited={work: tuple(where) for work, where in sorted(awaited.items())},
                reported=None if kind == STATUS_KIND else name in reported,
            )
        )
    return entries


def report(design: str, corpus: Path, reported: Collection[str]) -> Report:
    """The mapping between one design and one corpus, with its gaps."""
    inventory = clauses(design)
    names = {clause.name for clause in inventory}
    covering: dict[str, list[str]] = {}
    unnamed: dict[str, list[str]] = {}
    for declaration, where in declarations(corpus):
        clause = named(declaration, names)
        if clause is None:
            unnamed.setdefault(declaration, []).append(where)
        elif where not in covering.setdefault(clause, []):
            covering[clause].append(where)
    entries = surface(corpus, reported)
    declared = {entry.name for entry in entries if entry.kind != STATUS_KIND}
    return Report(
        mapping=tuple(
            (clause, tuple(covering.get(clause.name, []))) for clause in inventory
        ),
        unnamed=tuple(
            (declaration, tuple(where))
            for declaration, where in sorted(unnamed.items())
        ),
        surface=tuple(entries),
        surplus=tuple(sorted(set(reported) - declared)),
    )


def render(found: Report) -> str:
    """The report as the text one run prints, identical for identical inputs."""
    lines = ["# Clause mapping", ""]
    for clause, where in found.mapping:
        lines.append(f"{clause.name}: {len(where)} fixture(s)")
        lines.extend(f"    {name}" for name in where)
    lines += ["", "# Uncovered clauses", ""]
    lines.extend(clause.name for clause in found.uncovered)
    lines += ["", "# Unnamed declarations", ""]
    for declaration, where in found.unnamed:
        lines.append(declaration)
        lines.extend(f"    {name}" for name in where)
    lines += ["", "# Declared surface", ""]
    for entry in found.surface:
        if entry.reported is None:
            states = ""
        elif entry.reported:
            states = ", the build reports it"
        else:
            states = ", the build reports it nowhere"
        if entry.reached:
            lines.append(
                f"{entry.kind} {entry.name}: {len(entry.reached)} fixture(s){states}"
            )
        elif entry.unfixturable:
            works = ", ".join(entry.awaited)
            lines.append(
                f"{entry.kind} {entry.name}: unfixturable, awaiting {works}{states}"
            )
        else:
            lines.append(f"{entry.kind} {entry.name}: declared by no fixture{states}")
        for work, where in entry.awaited.items():
            lines.extend(f"    {name} (awaiting {work})" for name in where)
        lines.extend(f"    {name}" for name in entry.reached)
    for name in found.surplus:
        lines.append(f"{REPORTED_KIND} {name}: the contract declares it nowhere")
    for claim in CLAIMS:
        lines.append(f"installation claim {claim.name}: unfixturable, {claim.reason}")
        lines.append(f"    {claim.observable}")
    counted = Counter(
        "unfixturable" if entry.unfixturable else "reached" for entry in found.surface
    )
    lines += [
        "",
        f"conformance report: {len(found.mapping)} clause(s) the design states, "
        f"{len(found.uncovered)} covered by no fixture, "
        f"{len(found.unnamed)} declaration(s) naming no clause; "
        f"{counted['reached']} declared name(s) reached, "
        f"{counted['unfixturable']} unfixturable, "
        f"{len(found.unreported)} declared code(s) the build reports nowhere, "
        f"{len(found.surplus)} reported code(s) the contract declares nowhere, "
        f"{len(CLAIMS)} installation claim(s) no run observes",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    try:
        reported = reported_codes()
    except BuildNotConfigured as absent:
        print(f"conformance report: {absent}", file=sys.stderr)
        return 1
    except Unreadable as unreadable:
        print(f"conformance report: {unreadable}", file=sys.stderr)
        return 1

    branch, path = design_reference()
    found = report(git_show(git_ref(branch), path), CORPUS, reported)
    print(render(found), end="")
    for failure in found.failures:
        print(f"FAIL {failure}", file=sys.stderr)
    return 1 if found.failures else 0


if __name__ == "__main__":
    sys.exit(main())
