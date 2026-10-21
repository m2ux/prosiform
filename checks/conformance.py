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

The declared surface also lists the installation claims no run of the
corpus observes. An installation is not a thing a fixture can name: a
fixture declares a source tree and the bytes a run must return for it, and
the corpus reaches the build under test through configuration. Each claim
is therefore declared here, beside the surface this report renders, with
the reason the smoke run cannot reach it and the property of an installed
command that would observe it.

That property is written in the words the smoke run declares its own
properties in, so the two are read from one vocabulary. A claim naming a
property the run observes states a limit the corpus no longer has, so it
fails the report rather than printing: the entry leaves the listing because
the run came to observe it, and the closing count counts what is left.

The design is read from the branch and path the README's Design link names,
as the vocabulary check reads the same document, so no path into a dated
planning folder is written here.
"""

import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from documents import cells, is_delimiter, plain
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
from smoke import OBSERVED
from vocabulary import design_reference, git_ref, git_show

FENCE = re.compile(r"^(?:```|~~~)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")
BULLET = re.compile(r"^- \*\*(.+?)[:.]?\*\*")
STEP = re.compile(r"^(\d+)\.\s+\S")
SEPARATOR = " — "
AWAITING = "awaiting"


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

    @property
    def unfixturable(self) -> bool:
        """Whether only fixtures awaiting later work declare it."""
        return not self.reached and bool(self.awaited)

    @property
    def undeclared(self) -> bool:
        return not self.reached and not self.awaited


@dataclass(frozen=True)
class Claim:
    """One installation claim, and the property that would observe it."""

    name: str
    reason: str
    observes: str

    @property
    def observed(self) -> bool:
        """Whether the smoke run observes the property this claim names."""
        return self.observes in OBSERVED

    @property
    def observable(self) -> str:
        """The property that would observe it, as the listing states it."""
        return f"observable once the smoke run observes a command {self.observes}"


CLAIMS = (
    Claim(
        name="another platform",
        reason=(
            "the smoke run observes this host and the continuous-integration "
            "runner, and a platform whose command wrapper and path resolution "
            "differ is a different mechanism"
        ),
        observes="named on another platform's path",
    ),
    Claim(
        name="a machine that never held the repository",
        reason=(
            "the repository is on disk throughout the run and merely "
            "unreachable by path, working directory and environment, and "
            "removing it is not something a check inside it can do"
        ),
        observes="installed on a machine that never held this repository",
    ),
    Claim(
        name="the command line the documentation gives a reader",
        reason=(
            "the run installs an artefact it builds rather than running the "
            "command line the documentation's installation section states"
        ),
        observes="installed by the command line the documentation gives a reader",
    ),
)


def listed() -> tuple[Claim, ...]:
    """Each installation claim the smoke run does not observe."""
    return tuple(claim for claim in CLAIMS if not claim.observed)


@dataclass(frozen=True)
class Report:
    """The conformance report: the mapping, its gaps and the declared surface."""

    mapping: tuple[tuple[Clause, tuple[str, ...]], ...]
    unnamed: tuple[tuple[str, tuple[str, ...]], ...]
    surface: tuple[Entry, ...]

    @property
    def uncovered(self) -> tuple[Clause, ...]:
        return tuple(clause for clause, named in self.mapping if not named)

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
                f"installation claim {claim.name} names a command "
                f"{claim.observes}, which the smoke run observes, so the "
                "listing states a limit the corpus no longer has"
                for claim in CLAIMS
                if claim.observed
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


def surface(corpus: Path) -> list[Entry]:
    """Each code and exit status the contract declares, and what declares it."""
    declared: dict[tuple[str, str], list[tuple[str, str | None]]] = {}
    for fixture in fixtures(corpus):
        manifest = read(fixture / MANIFEST_NAME)
        where = identity(fixture, corpus)
        awaiting = manifest.get(AWAITING)
        expected = manifest["expected"]
        names = [("exit status", str(expected["exit_status"]))] + [
            (diagnostic["severity"], diagnostic["code"])
            for diagnostic in expected["diagnostics"]
        ]
        for name in set(names):
            declared.setdefault(name, []).append((where, awaiting))
    inventory = [("exit status", str(status)) for status in statuses()] + [
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
            )
        )
    return entries


def report(design: str, corpus: Path) -> Report:
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
    return Report(
        mapping=tuple(
            (clause, tuple(covering.get(clause.name, []))) for clause in inventory
        ),
        unnamed=tuple(
            (declaration, tuple(where))
            for declaration, where in sorted(unnamed.items())
        ),
        surface=tuple(surface(corpus)),
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
        if entry.reached:
            lines.append(f"{entry.kind} {entry.name}: {len(entry.reached)} fixture(s)")
        elif entry.unfixturable:
            works = ", ".join(entry.awaited)
            lines.append(f"{entry.kind} {entry.name}: unfixturable, awaiting {works}")
        else:
            lines.append(f"{entry.kind} {entry.name}: declared by no fixture")
        for work, where in entry.awaited.items():
            lines.extend(f"    {name} (awaiting {work})" for name in where)
        lines.extend(f"    {name}" for name in entry.reached)
    for claim in listed():
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
        f"{len(listed())} installation claim(s) no run observes",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    branch, path = design_reference()
    found = report(git_show(git_ref(branch), path), CORPUS)
    print(render(found), end="")
    for failure in found.failures:
        print(f"FAIL {failure}", file=sys.stderr)
    return 1 if found.failures else 0


if __name__ == "__main__":
    sys.exit(main())
