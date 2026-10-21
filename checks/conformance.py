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

The report records, beside that surface, the behavioural clauses no fixture
can reach. A clause recorded there is one no source tree and one invocation
can state: it binds how a build goes about its work, what a calling wrapper
does with the output, or how sources are authored, and the outcome it
serves is stated by other clauses carrying fixtures of their own. That is a
different thing from a section of the design stating no behaviour at all. A
section naming what the project has decided, what remains to be proven once
implementation is authorized, or what an upstream contribution would say
states no rule a corpus could cover, so it is declared here and leaves the
inventory of clauses entirely, it and the rules beneath it: a heading that
can carry no fixture is not a gap, and counting it as one measures nothing.

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
class Declaration:
    """One name this report accounts for rather than measures.

    The reason says why no run of the corpus reaches it, and the
    observable what a run would have to do to observe it, or what states
    the rule in its place where no run would.
    """

    name: str
    reason: str
    observable: str = ""


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

SECTIONS = (
    Declaration(
        name="Design status",
        reason=(
            "it states what the project has decided about its builds and the "
            "obligations each carries, and no outcome a run produces"
        ),
    ),
    Declaration(
        name="Implementation verification and residual policy detail",
        reason=(
            "it states what remains to be proven once implementation is "
            "authorized, and no outcome a run produces"
        ),
    ),
    Declaration(
        name="Upstream follow-up reference",
        reason=(
            "it states what an upstream contribution would say and what is to "
            "be consulted before one is drafted, and no outcome a run produces"
        ),
    ),
)

RECORDED = (
    Declaration(
        name="Input and output contract",
        reason="the heading opens straight onto the rules beneath it",
        observable=(
            "each rule beneath it states its own outcome and carries its own clause"
        ),
    ),
    Declaration(
        name="Resolution sequence",
        reason="the heading opens straight onto the numbered steps beneath it",
        observable=(
            "each step beneath it states its own outcome and carries its own clause"
        ),
    ),
    Declaration(
        name="Parser and source-preserving edits",
        reason=(
            "its prose binds how a build identifies and edits the spans of a "
            "source rather than what a run emits"
        ),
        observable=(
            "the invariants state what those means must produce, each carrying "
            "its own clause"
        ),
    ),
    Declaration(
        name="Parser and source-preserving edits — Parsing authority",
        reason="it binds what the reading of a source is let identify",
        observable=(
            "the rules governing what a bundle carries state the outcome, each "
            "carrying its own clause"
        ),
    ),
    Declaration(
        name="Parser and source-preserving edits — Source positions",
        reason="it binds how the spans of a source are built and retained",
        observable=(
            "the invariants a candidate is held to state what those spans must "
            "produce, each carrying its own clause"
        ),
    ),
    Declaration(
        name="Parser and source-preserving edits — Source model",
        reason="it binds what a build derives from the stream it reads",
        observable=(
            "the selection, boundary and destination rules state the outcome "
            "that derivation reaches, each carrying its own clause"
        ),
    ),
    Declaration(
        name="Parser and source-preserving edits — Edits",
        reason=("it binds how edits are applied and how overlapping ones are resolved"),
        observable=(
            "the bytes a bundle carries state the outcome, under the rules "
            "governing that content"
        ),
    ),
    Declaration(
        name="Parser and source-preserving edits — Validation",
        reason=(
            "it requires the candidate be read again and the declared "
            "invariants checked"
        ),
        observable=("each invariant states its own outcome and carries its own clause"),
    ),
    Declaration(
        name="Mandatory parser viability gates",
        reason=(
            "it states when its gates apply, before a production reading of "
            "sources is selected or any bundle is published"
        ),
        observable=(
            "the gates are met in choosing that reading rather than by any run "
            "over a source tree"
        ),
    ),
    Declaration(
        name="Explicitly linked source structure",
        reason="it states how sources are to be authored",
        observable=(
            "the rules beneath it state what a run does with sources so "
            "authored, each carrying its own clause"
        ),
    ),
    Declaration(
        name="Explicitly linked source structure — Reading versus execution",
        reason=(
            "it holds that inclusion makes material available without "
            "authorizing its execution, which no bundle's bytes show"
        ),
        observable=(
            "the authored instructions carry the execution verbs and the call "
            "boundaries that state it"
        ),
    ),
    Declaration(
        name="Heading-only structural ancestors — Provenance",
        reason=(
            "it requires ancestry be recorded apart from selected content, "
            "which a bundle states nothing of on its own"
        ),
        observable=(
            "the depth and deduplication rules state its effects, each "
            "carrying its own clause"
        ),
    ),
    Declaration(
        name="Agent delivery contract",
        reason=(
            "it states what a successful compilation does and does not "
            "establish about a transport"
        ),
        observable=(
            "a run produces a bundle and an exit status, and neither states "
            "what a transport delivered"
        ),
    ),
    Declaration(
        name="Agent delivery contract — Response limit",
        reason=(
            "it binds the calling wrapper's buffering and the response size it enforces"
        ),
        observable=(
            "observable once a consumer of the run's output is declared beside "
            "the source tree"
        ),
    ),
    Declaration(
        name="Agent delivery contract — Broken pipes",
        reason="it binds the wrapper's reporting of a transport failure",
        observable=(
            "a fixture declares a source tree and an invocation, and reaches "
            "no consumer of the run's output"
        ),
    ),
    Declaration(
        name="Adversarial acceptance fixtures",
        reason=("it instructs that a corpus be written before broad implementation"),
        observable="the corpus this report reads is what states it",
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
        """Each clause no fixture names that a fixture could reach."""
        recorded = {clause.name for clause in RECORDED}
        return tuple(
            clause
            for clause, where in self.mapping
            if not where and clause.name not in recorded
        )

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
    """Every behavioural clause the design states, in the order it states them.

    A section declared as stating no behaviour carries no clause, nor does
    any rule beneath it.
    """
    silent = {section.name for section in SECTIONS}
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
            title = None if len(marked.group(1)) == 1 else text(marked.group(2))
            heading = None if title in silent else title
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


def listing(
    kind: str, verdict: str, declared: tuple[Declaration, ...] | tuple[Claim, ...]
) -> list[str]:
    """One group of declarations, each with its reason and what it rests on."""
    lines = []
    for entry in declared:
        lines.append(f"{kind} {entry.name}: {verdict}, {entry.reason}")
        if entry.observable:
            lines.append(f"    {entry.observable}")
    return lines


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
    lines.extend(listing("installation claim", "unfixturable", listed()))
    lines += ["", "# Clauses no run states", ""]
    lines.extend(listing("clause", "unfixturable", RECORDED))
    lines += ["", "# Sections stating no behaviour", ""]
    lines.extend(listing("section", "non-behavioural", SECTIONS))
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
        f"{len(RECORDED)} clause(s) no run states, "
        f"{len(SECTIONS)} section(s) stating no behaviour, "
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
