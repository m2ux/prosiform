"""Dispatch: the bundles a run's dispatches name, and where each is handed off.

A `⇉` link states that a sub-agent follows its target, and a `⫽` link
that a sub-agent follows it together with the other `⫽` links of its
section, so a run compiles every target either reaches, transitively,
each distinct document and fragment once as its own entry, and
publishes each as a bundle of its own beside the one that dispatches
it. A *dispatch depth* is the number of dispatch hops along one chain
of those bundles, counted from the run's entry: a dispatch the entry
carries is the first hop, a dispatch that target's bundle carries is
the second, and so on.

A `⇉` link publishes where its author wrote it, with its mark, pointing
at the file its target was compiled to. The `⫽` links in a section's own
content are one *set*. A set of two or more distinct targets points at
the section's one `In parallel` sub-section: a heading one level below
the section, after the section's own content and before its child
sections, whose list holds each target once as a `⇉` link to its file.
A set of one target publishes as that single `⇉` link and carries no
sub-section. A set states no order. A set above the group's first
heading takes that heading's level. Each section carrying a set
carries its own sub-section. The sub-sections are inserted into a group
once it is built, before the bundle's destinations are assigned, so the
ordinal a renderer gives a repeated heading counts them as it counts
every other heading.

A dispatch has to be one a sub-agent can finish and one the bundle can
place, so three dispatches publish nothing:

- A chain of bundles returning to one already on it is a cycle: its
  sub-agents would dispatch one another without end. A dispatch naming
  the run's own single selection closes the shortest one.
- A set in a level-6 section leaves no level for its sub-section.
- An authored heading whose text equals `In parallel` in a bundle that
  emits one would give two sections one name.

A chain deeper than the limit still publishes, and warns: flattening it
is the author's optimisation rather than a defect. A dispatch naming
the document that writes it, which closes no cycle, hands a sub-agent
material its own session compiles, so it warns as well. A target's
shape is the corpus's convention, so a dispatch states no rule on it.

A chain is deeper than the limit where it reaches a hop past it, and
the search for one stops there. A target already on a chain is not
followed again, so both searches terminate on any graph of dispatches.
The dispatches a bundle carries name each target once, at the first
link naming it, so each search follows each target once from a bundle.

A set member's link text is written with each run of whitespace, a line
break among them, as one space.
"""

from collections.abc import Callable, Collection, Iterator, Mapping, Sequence
from dataclasses import dataclass, replace
from urllib.parse import quote

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
from prosiform.closure import (
    DECLARING,
    DISPATCH_MARK,
    UNSUBSTITUTED,
    Declarations,
    Reference,
    Substitution,
    dispatched,
    identity,
    parallel,
    unmarked,
)
from prosiform.closure import withholding_target as withheld
from prosiform.diagnostics import (
    ERROR,
    WARNING,
    Diagnostic,
    Location,
    RelatedLocation,
)
from prosiform.provenance import (
    COMPOSED_HEADINGS,
    FILENAME_WRAPPER,
    PARALLEL_SECTION,
    Ancestor,
    Carried,
    Emitted,
    Generated,
    Instruction,
    Part,
    Range,
    Record,
    Served,
    Target,
)
from prosiform.source import (
    ANCHOR,
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

PARALLEL = "In parallel"

TOGETHER = (
    "Give each of these to its own sub-agent at the same time, and continue "
    "when all have answered:"
)

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

Placed = dict[tuple[str, int], dict[Served, int | str]]
"""Where each dispatched link points, by the region and link it serves.

A region is the document and the first line of content it opens on, so
every link one region writes naming one target with one operator
points at one place. The place is the position of an `In parallel`
sub-section among every heading the bundle emits, or the destination of
a bundle file.
"""

Anchors = Mapping[tuple[str, int], Mapping[Served, str]]
"""The destination each region's dispatched links take, by link."""


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
"""The dispatches the bundle of one target carries, each target once."""


def deepest(onward: Onward, first: Hop, entries: Collection[str]) -> list[Hop] | None:
    """The first chain from one hop that reaches a hop past the limit.

    A chain is followed in the order each bundle writes its dispatches,
    and only through targets not already on it, so a cycle adds no depth.
    """
    chain = [first]
    on = {*entries, first.name}
    pending: list[Iterator[Hop]] = [iter(onward(first.target))]
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
        pending.append(iter(onward(following.target)))
    return None


def returning(onward: Onward, first: Hop, entries: Collection[str]) -> list[Hop] | None:
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
    pending: list[Iterator[Hop]] = [iter(onward(first.target))]
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
        pending.append(iter(onward(following.target)))
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


def cycle(hops: Sequence[Hop], entries: Collection[str], onward: Onward) -> None:
    """Refuse the first chain of the run's dispatches returning to a target on it.

    Each distinct target the entry dispatches is followed from the first
    link naming it, in the order the entry's bundle wrote them.
    """
    for first in hops:
        loop = returning(onward, first, entries)
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
    found: list[Diagnostic] = []
    for first in hops:
        deep = deepest(onward, first, entries)
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

    reference: Reference
    text: str
    written: str
    location: Location
    parallel: bool
    opening: str

    @property
    def target(self) -> Target:
        """The document and section the link names."""
        return (self.reference.path, self.reference.fragment)

    @property
    def served(self) -> Served:
        """The sub-section the link points at, as its target and operator."""
        return (self.target, self.parallel)


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
    path: str,
    source: Source,
    tokens: Sequence[Token],
    region: Token,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
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
            target = withheld(path, destination, opening, declarations, substitution)
            if target is None:
                continue
            found.append(
                Link(
                    target,
                    " ".join(unmarked(link_text(children, at)).split()),
                    destination,
                    Location(path, 1 if line is None else line, 1),
                    parallel(opening),
                    opening,
                )
            )
    return found


def file_destination(bundle_file: str) -> str:
    """The destination a link takes to one bundle file beside the bundle."""
    return quote(bundle_file, safe="")


def listing(entries: Sequence[tuple[str, str]]) -> str:
    """The list an `In parallel` sub-section carries, one `⇉` link to a bundle each."""
    return "\n".join(
        f"- [{DISPATCH_MARK} {escaped(text)}]({file_destination(file)})"
        for file, text in entries
    )


def region_of(tokens: Sequence[Token], part: Range) -> Token:
    """The region of a parse one selected range holds."""
    return next(one for one in regions(tokens) if one.map == list(part.lines))


class Placing:
    """One bundle's groups rebuilt with the `In parallel` sub-sections its sets take.

    The grouped regions are those a group carries as its own, by the
    document and first line naming each. A dispatch a contribution
    carries points where its source's own region is given where a group
    carries that region. Where none does, the region's first contribution
    gives the dispatch a place of its own: a set's sub-section sits
    beneath the composed section holding the link and ahead of the next
    composed heading, so a scope's own sub-sections still follow its
    destination sections.
    """

    def __init__(
        self,
        parsed: Mapping[str, Sequence[Token]],
        read: Mapping[str, Source],
        bundle_file: Callable[[Target], str],
        grouped: Collection[tuple[str, int]],
        declarations: Declarations = DECLARING,
        substitution: Substitution = UNSUBSTITUTED,
    ) -> None:
        self.parsed = parsed
        self.grouped = grouped
        self.read = read
        self.bundle_file = bundle_file
        self.declarations = declarations
        self.substitution = substitution
        self.placed: Placed = {}
        self.at = 0
        self.emitted: list[str] = []
        self.parts: list[Part] = []
        self.headings: list[Emitted] = []
        self.pending: dict[Served, Link] = {}
        self.serving: list[tuple[tuple[str, int], Served]] = []
        self.level: int | None = None
        self.inner: dict[Served, Link] = {}
        self.inner_serving: list[tuple[tuple[str, int], Served]] = []
        self.inner_level = 0

    def heading(self, text: str, depth: int, body: Sequence[Instruction]) -> int:
        """Emit one generated section, returning its heading's bundle position."""
        at = self.at + len(self.headings)
        self.emitted.append(f"{ATX * depth} {escaped(text)}")
        self.parts.append(Generated(text, depth, PARALLEL_SECTION))
        self.headings.append(Generated(text, depth, PARALLEL_SECTION))
        for one in body:
            self.emitted.append(one.text)
            self.parts.append(one)
        return at

    def flush(self, following: int | None) -> None:
        """Emit the sub-section the section just closed carries.

        The section's `⫽` set takes one where it holds two or more
        targets. Content above the bundle's first heading takes that
        heading's level.
        """
        self.close()
        if not self.pending:
            return
        depth = (following or 1) if self.level is None else self.level + 1
        self.place(self.pending, self.serving, depth)
        self.pending = {}
        self.serving = []

    def close(self) -> None:
        """Emit the sub-section the composed section just closed carries."""
        if self.inner:
            self.place(self.inner, self.inner_serving, self.inner_level + 1)
        self.inner = {}
        self.inner_serving = []

    def place(
        self,
        pending: Mapping[Served, Link],
        links: Sequence[tuple[tuple[str, int], Served]],
        depth: int,
    ) -> None:
        """Say where one section's dispatched links point, emitting its set's section.

        A `⇉` link, and the one `⫽` link of a set of one target, point at
        their target's bundle file. A set of two or more targets points
        at the `In parallel` sub-section emitted here.
        """
        together = [link for link in pending.values() if link.parallel]
        serving: dict[Served, int | str] = {
            served: file_destination(self.bundle_file(link.target))
            for served, link in pending.items()
        }
        if len(together) > 1:
            if depth > MAX_LEVEL:
                first = together[0]
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
            listed = listing(
                [(self.bundle_file(link.target), link.text) for link in together]
            )
            at = self.heading(
                PARALLEL, depth, [Instruction(TOGETHER), Instruction(listed, True)]
            )
            serving.update((link.served, at) for link in together)
        for key, served in links:
            self.placed.setdefault(key, {})[served] = serving[served]

    def group(self, one: Group) -> Group:
        """One group with its sub-sections, the headings before it counted."""
        offset = 1 if one.wrapped else 0
        self.emitted = []
        self.parts = []
        self.headings = []
        self.level = None
        if one.wrapped:
            wrapper = one.record.headings[0]
            self.emitted.append(one.parts[0])
            self.headings.append(wrapper)
            self.level = wrapper.level
        at = offset
        for part, text in zip(one.record.parts, one.parts[offset:], strict=True):
            if isinstance(part, Generated) and part.kind in COMPOSED_HEADINGS:
                # A section a directive composes is content of the scope
                # holding the directive, so it closes no section here.
                self.close()
                self.inner_level = part.level
                self.headings.append(one.record.headings[at])
                at += 1
            elif isinstance(part, Range) and part.composed:
                tokens = self.parsed[part.path]
                region = region_of(tokens, part)
                held = len(carried_headings(tokens, region))
                if region.type == HEADING_OPEN:
                    self.close()
                    self.inner_level = one.record.headings[at].level
                self.headings.extend(one.record.headings[at : at + held])
                at += held
                key = (part.path, part.lines[0])
                if key not in self.grouped and key not in self.placed:
                    for link in written_in(
                        part.path,
                        self.read[part.path],
                        tokens,
                        region,
                        self.declarations,
                        self.substitution,
                    ):
                        self.inner.setdefault(link.served, link)
                        if (key, link.served) not in self.inner_serving:
                            self.inner_serving.append((key, link.served))
            elif isinstance(part, Ancestor | Generated):
                self.flush(part.level)
                self.level = part.level
                self.headings.append(one.record.headings[at])
                at += 1
            elif isinstance(part, Range):
                tokens = self.parsed[part.path]
                region = region_of(tokens, part)
                held = len(carried_headings(tokens, region))
                if region.type == HEADING_OPEN:
                    self.flush(one.record.headings[at].level)
                    self.level = one.record.headings[at].level
                self.headings.extend(one.record.headings[at : at + held])
                at += held
                key = (part.path, part.lines[0])
                for link in written_in(
                    part.path,
                    self.read[part.path],
                    tokens,
                    region,
                    self.declarations,
                    self.substitution,
                ):
                    self.pending.setdefault(link.served, link)
                    if (key, link.served) not in self.serving:
                        self.serving.append((key, link.served))
            self.emitted.append(text)
            self.parts.append(part)
        self.flush(None)
        self.at += len(self.headings)
        return Group(
            tuple(self.emitted),
            replace(one.record, headings=tuple(self.headings), parts=tuple(self.parts)),
            wrapped=one.wrapped,
            level=one.level,
        )


def subsections(
    groups: Sequence[Group],
    parsed: Mapping[str, Sequence[Token]],
    read: Mapping[str, Source],
    bundle_file: Callable[[Target], str],
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> tuple[list[Group], Placed]:
    """Every group with its `In parallel` sub-sections, and where each link points.

    A group's sections are read in the order it emits them: a heading
    part closes the section above it, and the sub-section that section
    collected is emitted ahead of the heading. A wrapped group's file
    heading opens its first section; a group the parent's title opens
    has no section above that title, so a set there takes the level of
    the heading that follows it.

    A destination section and the contributions beneath it are content
    of the scope that composes them, so they close none of its sections,
    and a dispatch a contribution carries points where `Placing` states.
    """
    grouped = {
        (part.path, part.lines[0])
        for one in groups
        for part in one.record.ranges
        if not part.composed
    }
    placing = Placing(parsed, read, bundle_file, grouped, declarations, substitution)
    rebuilt = [placing.group(one) for one in groups]
    return rebuilt, placing.placed


def authored(
    record: Record, read: Mapping[str, Source]
) -> Iterator[tuple[Emitted, Location | None]]:
    """Each heading of a group whose text an author or a source path gave it.

    An authored heading is located at the line of the file it stands on,
    which its origin states as a line of its source's content.
    """
    for one in record.headings:
        if isinstance(one, Carried | Ancestor):
            origin = one.origins[0]
            yield (
                one,
                Location(origin.path, read[origin.path].line(origin.line) or 1, 1),
            )
        elif isinstance(one, Generated) and one.kind == FILENAME_WRAPPER:
            yield one, None


def collisions(groups: Sequence[Group], read: Mapping[str, Source]) -> None:
    """Refuse an authored heading whose text equals one pf emits in the bundle."""
    emitted = {
        one.text
        for group in groups
        for one in group.record.headings
        if isinstance(one, Generated) and one.kind == PARALLEL_SECTION
    }
    for group in groups:
        for one, at in authored(group.record, read):
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
) -> dict[tuple[str, int], dict[Served, str]]:
    """The destination each region's dispatched links take, by link."""
    return {
        key: {
            link: f"{ANCHOR}{assigned[at]}" if isinstance(at, int) else at
            for link, at in served.items()
        }
        for key, served in placed.items()
    }
