"""Dispatch: the bundles a run's dispatches name, and where each is handed off.

A `⇉` link states that a sub-agent follows its target, so a run compiles
every target its dispatches reach, transitively, each distinct document
and fragment once as its own entry, and publishes each as a bundle of its
own beside the one that dispatches it. A *dispatch depth* is the number
of dispatch hops along one chain of those bundles, counted from the
run's entry: a dispatch the entry carries is the first hop, a dispatch
that target's bundle carries is the second, and so on.

A dispatched link publishes no mark. It points at a *dispatch
sub-section* of the section holding it: a heading `Dispatch <link
text>` one level below that section, after the section's own content
and before its child sections, whose one line names the target's
bundle file. A dispatch above the group's first heading takes that
heading's level. Links in one section naming one target share its
sub-section, and each section dispatching a target carries its own.
The sub-sections are inserted into a group once it is built, before the
bundle's destinations are assigned, so the ordinal a renderer gives a
repeated heading counts them as it counts every other heading.

A dispatch has to be one a sub-agent can finish and one the bundle can
place, so three dispatches publish nothing:

- A chain of bundles returning to one already on it is a cycle: its
  sub-agents would dispatch one another without end. A dispatch naming
  the run's own single selection closes the shortest one.
- A dispatch in a level-6 section leaves no level for its sub-section.
- An authored heading whose text equals one pf emits in the same bundle
  — `Prosiform`, `Dispatch in parallel` or a sub-section's — would give
  two sections one name.

A chain deeper than the limit still publishes, and warns: flattening it
is the author's optimisation rather than a defect. A dispatch naming
the document that writes it, which closes no cycle, hands a sub-agent
material its own session compiles, so it warns as well. A target's
shape is the corpus's convention, so a dispatch states no rule on it.

A chain is deeper than the limit where it reaches a hop past it, and
the search for one stops there. A target already on a chain is not
followed again, so both searches terminate on any graph of dispatches.
"""

from collections.abc import Callable, Collection, Iterator, Mapping, Sequence
from dataclasses import dataclass, replace

from markdown_it.token import Token

from prosiform.bundle import (
    ATX,
    HEADING_DEPTH_OVERFLOW,
    HEADING_OPEN,
    MAX_LEVEL,
    Group,
    carried_headings,
    escaped,
)
from prosiform.closure import Reference, dispatched, identity, unmarked
from prosiform.closure import withholding_target as withheld
from prosiform.diagnostics import (
    ERROR,
    WARNING,
    Diagnostic,
    Location,
    RelatedLocation,
)
from prosiform.provenance import (
    DISPATCH_SECTION,
    FILENAME_WRAPPER,
    Ancestor,
    Carried,
    Emitted,
    Generated,
    Instruction,
    Part,
    Range,
    Record,
    Target,
)
from prosiform.source import (
    LINK_OPEN,
    Source,
    events,
    inlines,
    opening_text,
    regions,
    shown,
)

DISPATCH_DEPTH = "W_DISPATCH_DEPTH"
DISPATCH_SELF = "W_DISPATCH_SELF"
DISPATCH_CYCLE = "E_DISPATCH_CYCLE"
HEADING_COLLISION = "E_HEADING_COLLISION"

CODES = (DISPATCH_DEPTH, DISPATCH_SELF, DISPATCH_CYCLE, HEADING_COLLISION)

PROSIFORM = "Prosiform"
PARALLEL = "Dispatch in parallel"
DISPATCH = "Dispatch"

LINK_CLOSE = "link_close"

LIMIT = 3

DEPTH_REMEDY = (
    "compile an intermediate target into the bundle that dispatches it, or "
    "dispatch its targets from an earlier hop"
)
SELF_REMEDY = (
    "move the procedure to a document of its own, or link it without the "
    "dispatch operator"
)
CYCLE_REMEDY = "compile or cite one target of the cycle rather than dispatching it"
LEVEL_REMEDY = "move the dispatch to a section above the sixth level"
COLLISION_REMEDY = "retitle the authored heading"

Placed = dict[tuple[str, int], dict[Target, int]]
"""Each dispatch sub-section's heading, by the region and target it serves.

A region is the document and the first line of content it opens on, so
every link one region writes naming one target reaches one sub-section,
and the value is that heading's position among every heading the bundle
emits.
"""

Anchors = Mapping[tuple[str, int], Mapping[Target, str]]
"""The destination each region's dispatched links take, by target."""


class Refused(Exception):
    """A dispatch the bundle cannot carry, as the diagnostic reporting it."""

    def __init__(self, diagnostic: Diagnostic) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


@dataclass(frozen=True)
class Hop:
    """One dispatched link: the target it names and where it is written."""

    target: Reference
    location: Location

    @property
    def own(self) -> bool:
        """Whether the link names the document that writes it."""
        return self.target.path == self.location.file

    @property
    def name(self) -> str:
        """The target as the document and section it names."""
        return identity(self.target)


Onward = Callable[[Reference], Sequence[Hop]]


class Graph:
    """The dispatches each target's own bundle carries, read once per target."""

    def __init__(self, onward: Onward) -> None:
        self.onward = onward
        self.read: dict[str, tuple[Hop, ...]] = {}

    def beyond(self, hop: Hop) -> tuple[Hop, ...]:
        """Each distinct dispatch the bundle of one hop's target carries."""
        if hop.name not in self.read:
            distinct: dict[str, Hop] = {}
            for one in self.onward(hop.target):
                distinct.setdefault(one.name, one)
            self.read[hop.name] = tuple(distinct.values())
        return self.read[hop.name]


def deepest(graph: Graph, first: Hop, entries: Collection[str]) -> list[Hop] | None:
    """The first chain from one hop that reaches a hop past the limit.

    A chain is followed in the order each bundle writes its dispatches,
    and only through targets not already on it, so a cycle adds no depth.
    """
    chain = [first]
    on = {*entries, first.name}
    pending: list[Iterator[Hop]] = [iter(graph.beyond(first))]
    while pending:
        if len(chain) > LIMIT:
            return chain
        following = next(pending[-1], None)
        if following is None:
            pending.pop()
            on.discard(chain.pop().name)
            continue
        if following.name in on:
            continue
        chain.append(following)
        on.add(following.name)
        pending.append(iter(graph.beyond(following)))
    return None


def returning(graph: Graph, first: Hop, entries: Collection[str]) -> list[Hop] | None:
    """The first chain from one hop whose last hop names a target already on it.

    The entries stand on every chain, so a dispatch naming the run's own
    selection closes a cycle. A target every chain through which was
    followed to its end without returning is not followed again.
    """
    if first.name in entries:
        return [first]
    chain = [first]
    on = {*entries, first.name}
    done: set[str] = set()
    pending: list[Iterator[Hop]] = [iter(graph.beyond(first))]
    while pending:
        following = next(pending[-1], None)
        if following is None:
            pending.pop()
            name = chain.pop().name
            on.discard(name)
            done.add(name)
            continue
        if following.name in on:
            return [*chain, following]
        if following.name in done:
            continue
        chain.append(following)
        on.add(following.name)
        pending.append(iter(graph.beyond(following)))
    return None


def reported(
    severity: str,
    code: str,
    message: str,
    remedy: str,
    entry: str,
    chain: Sequence[Hop],
) -> Diagnostic:
    """One diagnostic naming a chain: its first link, then every later hop."""
    first, *later = chain
    return Diagnostic(
        severity,
        message,
        code=code,
        reference=first.target.original,
        chain=(entry, *(hop.name for hop in chain)),
        remedy=remedy,
        location=first.location,
        related=tuple(
            RelatedLocation(
                hop.location.file,
                hop.location.line,
                hop.location.column,
                f"dispatches {hop.name!r}",
            )
            for hop in later
        ),
    )


def distinct(hops: Sequence[Hop]) -> list[Hop]:
    """Each target the hops name, at the first hop naming it."""
    found: dict[str, Hop] = {}
    for hop in hops:
        found.setdefault(hop.name, hop)
    return list(found.values())


def cycle(hops: Sequence[Hop], entries: Collection[str], onward: Onward) -> None:
    """Refuse the first chain of the run's dispatches returning to a target on it.

    Each distinct target the entry dispatches is followed from the first
    link naming it, in the order the entry's bundle wrote them.
    """
    graph = Graph(onward)
    for first in distinct(hops):
        loop = returning(graph, first, entries)
        if loop is None:
            continue
        entry = first.target.chain[0] if first.target.chain else first.name
        raise Refused(
            reported(
                ERROR,
                DISPATCH_CYCLE,
                f"the dispatch {first.target.original!r} starts a chain that "
                f"dispatches {loop[-1].name!r} again, so its sub-agents would "
                f"dispatch one another without end",
                CYCLE_REMEDY,
                entry,
                loop,
            )
        )


def analysed(
    hops: Sequence[Hop], entries: Collection[str], onward: Onward
) -> list[Diagnostic]:
    """The depth warnings the dispatches the run's entry carries raise.

    Each distinct target the entry dispatches is followed from the first
    link naming it, and raises at most one warning: for the first chain
    from it reaching a hop past the limit.
    """
    graph = Graph(onward)
    found: list[Diagnostic] = []
    for first in distinct(hops):
        deep = deepest(graph, first, entries)
        if deep is None:
            continue
        entry = first.target.chain[0] if first.target.chain else first.name
        found.append(
            reported(
                WARNING,
                DISPATCH_DEPTH,
                f"the dispatch {first.target.original!r} starts a chain reaching "
                f"{len(deep)} dispatches, deeper than the {LIMIT} a chain is "
                f"held to",
                DEPTH_REMEDY,
                entry,
                deep,
            )
        )
    return found


def selfward(hop: Hop) -> Diagnostic:
    """One warning naming a dispatch of the document that writes it."""
    return Diagnostic(
        WARNING,
        f"the dispatch {hop.target.original!r} names {hop.name!r} in the document "
        f"that writes it, so it hands a sub-agent material the dispatching "
        f"session compiles itself",
        code=DISPATCH_SELF,
        reference=hop.target.original,
        resolved=hop.name,
        chain=hop.target.chain,
        remedy=SELF_REMEDY,
        location=hop.location,
    )


@dataclass(frozen=True)
class Link:
    """One dispatched link a region writes: its target, text and position."""

    target: Target
    text: str
    written: str
    location: Location


def link_text(children: Sequence[Token], at: int) -> str:
    """The text a reader reads in the link opened at one position."""
    depth = 0
    shows: list[str] = []
    for child in children[at + 1 :]:
        if child.type == LINK_OPEN:
            depth += 1
        elif child.type == LINK_CLOSE:
            if depth == 0:
                break
            depth -= 1
        shows.append(shown(child))
    return "".join(shows)


def written_in(
    path: str, source: Source, tokens: Sequence[Token], region: Token
) -> list[Link]:
    """Every dispatched link one region writes, in written order."""
    found: list[Link] = []
    for inline in inlines(tokens, [region]):
        line = source.line(None if inline.map is None else inline.map[0] + 1)
        for children, at, child in events(inline.children or []):
            if child.type != LINK_OPEN:
                continue
            opening = opening_text(children, at)
            if not dispatched(opening):
                continue
            destination = str(child.attrGet("href") or "")
            target = withheld(path, destination, opening, source.root)
            if target is None:
                continue
            found.append(
                Link(
                    (target.path, target.fragment),
                    unmarked(link_text(children, at)),
                    destination,
                    Location(path, 1 if line is None else line, 1),
                )
            )
    return found


def instruction(bundle_file: str) -> str:
    """The one line a dispatch sub-section carries."""
    return f"Dispatch `{bundle_file}` to a sub-agent."


class Placing:
    """One bundle's groups rebuilt with a sub-section after each dispatching section."""

    def __init__(
        self,
        parsed: Mapping[str, Sequence[Token]],
        read: Mapping[str, Source],
        bundle_file: Callable[[Target], str],
    ) -> None:
        self.parsed = parsed
        self.read = read
        self.bundle_file = bundle_file
        self.placed: Placed = {}
        self.at = 0
        self.emitted: list[str] = []
        self.parts: list[Part] = []
        self.headings: list[Emitted] = []
        self.pending: dict[Target, Link] = {}
        self.serving: list[tuple[tuple[str, int], Target]] = []
        self.level: int | None = None

    def flush(self, following: int | None) -> None:
        """Emit the sub-sections the section just closed carries."""
        if not self.pending:
            return
        depth = (following or 1) if self.level is None else self.level + 1
        if depth > MAX_LEVEL:
            first = next(iter(self.pending.values()))
            raise Refused(
                Diagnostic(
                    ERROR,
                    f"the dispatch {first.written!r} sits in a level-{MAX_LEVEL} "
                    f"section, so its sub-section would be emitted at level "
                    f"{depth}, which is beyond H{MAX_LEVEL}",
                    code=HEADING_DEPTH_OVERFLOW,
                    reference=first.written,
                    remedy=LEVEL_REMEDY,
                    location=first.location,
                )
            )
        serving: dict[Target, int] = {}
        for target, link in self.pending.items():
            text = f"{DISPATCH} {link.text}"
            body = instruction(self.bundle_file(target))
            serving[target] = self.at + len(self.headings)
            self.emitted.append(f"{ATX * depth} {escaped(text)}")
            self.parts.append(Generated(text, depth, DISPATCH_SECTION))
            self.headings.append(Generated(text, depth, DISPATCH_SECTION))
            self.emitted.append(body)
            self.parts.append(Instruction(body))
        for key, target in self.serving:
            self.placed.setdefault(key, {})[target] = serving[target]
        self.pending = {}
        self.serving = []

    def group(self, one: Group) -> Group:
        """One group with its sub-sections, the headings before it counted."""
        offset = 1 if one.wrapped else 0
        self.emitted = list(one.parts[:offset])
        self.parts = []
        self.headings = list(one.record.headings[:offset])
        self.level = 1 if one.wrapped else None
        at = offset
        for part, text in zip(one.record.parts, one.parts[offset:], strict=True):
            if isinstance(part, Ancestor | Generated):
                self.flush(part.level)
                self.level = part.level
                self.headings.append(one.record.headings[at])
                at += 1
            elif isinstance(part, Range):
                tokens = self.parsed[part.path]
                region = next(t for t in regions(tokens) if t.map == list(part.lines))
                held = len(carried_headings(tokens, region))
                if region.type == HEADING_OPEN:
                    self.flush(one.record.headings[at].level)
                    self.level = one.record.headings[at].level
                self.headings.extend(one.record.headings[at : at + held])
                at += held
                key = (part.path, part.lines[0])
                for link in written_in(part.path, self.read[part.path], tokens, region):
                    self.pending.setdefault(link.target, link)
                    if (key, link.target) not in self.serving:
                        self.serving.append((key, link.target))
            self.emitted.append(text)
            self.parts.append(part)
        self.flush(None)
        self.at += len(self.headings)
        return Group(
            tuple(self.emitted),
            replace(one.record, headings=tuple(self.headings), parts=tuple(self.parts)),
            one.order,
            wrapped=one.wrapped,
        )


def subsections(
    groups: Sequence[Group],
    parsed: Mapping[str, Sequence[Token]],
    read: Mapping[str, Source],
    bundle_file: Callable[[Target], str],
) -> tuple[list[Group], Placed]:
    """Every group with its dispatch sub-sections, and where each one stands.

    A group's sections are read in the order it emits them: a heading
    part closes the section above it, and the sub-sections that section
    collected are emitted ahead of the heading. A wrapped group's file
    heading opens its first section; a group the parent's title opens
    has no section above that title, so a dispatch there takes the
    level of the heading that follows it.
    """
    placing = Placing(parsed, read, bundle_file)
    rebuilt = [placing.group(one) for one in groups]
    return rebuilt, placing.placed


def authored(record: Record) -> Iterator[tuple[Emitted, Location | None]]:
    """Each heading of a group whose text an author or a source path gave it."""
    for one in record.headings:
        if isinstance(one, Carried | Ancestor):
            origin = one.origins[0]
            yield one, Location(origin.path, origin.line or 1, 1)
        elif isinstance(one, Generated) and one.kind == FILENAME_WRAPPER:
            yield one, None


def collisions(groups: Sequence[Group]) -> None:
    """Refuse an authored heading whose text equals one pf emits in the bundle."""
    emitted = {PROSIFORM, PARALLEL} | {
        one.text
        for group in groups
        for one in group.record.headings
        if isinstance(one, Generated) and one.kind == DISPATCH_SECTION
    }
    for group in groups:
        for one, at in authored(group.record):
            if one.text not in emitted:
                continue
            where = (
                f"{at.file}:{at.line}" if at is not None else f"{group.record.path!r}"
            )
            raise Refused(
                Diagnostic(
                    ERROR,
                    f"the heading {one.text!r} at {where} equals the heading "
                    f"{one.text!r} pf emits in the same bundle",
                    code=HEADING_COLLISION,
                    source=group.record.path if at is None else at.file,
                    remedy=COLLISION_REMEDY,
                    location=at,
                )
            )


def anchors(
    placed: Placed, assigned: Sequence[str]
) -> dict[tuple[str, int], dict[Target, str]]:
    """The destination each region's dispatched links take, by target."""
    return {
        key: {target: assigned[at] for target, at in served.items()}
        for key, served in placed.items()
    }
