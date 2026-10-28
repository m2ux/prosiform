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

A dispatched link publishes no mark. A `⇉` link points at a *dispatch
sub-section* of the section holding it: a heading `Dispatch <link
text>` one level below that section, after the section's own content
and before its child sections, whose one line names the target's
bundle file. The `⫽` links in a section's own content are one *set*,
and every one of them points at the section's one `Dispatch in
parallel` sub-section, placed after its dispatch sub-sections, which
lists each target's bundle file once with its link text. A set states
no order. Each sub-section's instruction links the protocol it follows.
A dispatch above the group's first heading takes that heading's level.
Links in one section naming one target with one operator share its
sub-section, and each section dispatching a target
carries its own. The sub-sections are inserted into a group once it is
built, before the bundle's destinations are assigned, so the ordinal a
renderer gives a repeated heading counts them as it counts every other
heading.

A bundle that dispatches opens with a *Prosiform section*: a heading
`Prosiform`, then a `Dispatch` protocol sub-section whenever the bundle
dispatches at all, and a `Parallel dispatch` one when it carries a set,
each stating its protocol in wording the profile fixes. The section is
the bundle's first heading, ahead of a file heading and of any
sub-section content above the first heading takes, so its protocols
take the destinations their slugs name and an agent reading top-down
meets each before the instruction that invokes it. Its levels are
fixed, so each protocol sub-section is the same bytes in every bundle
carrying it. A bundle that dispatches nothing carries none.

A dispatch has to be one a sub-agent can finish and one the bundle can
place, so three dispatches publish nothing:

- A chain of bundles returning to one already on it is a cycle: its
  sub-agents would dispatch one another without end. A dispatch naming
  the run's own single selection closes the shortest one.
- A dispatch in a level-6 section leaves no level for its sub-section.
- An authored heading whose text equals one pf emits in the same bundle
  — `Prosiform`, `Dispatch in parallel`, a protocol sub-section's or a
  dispatch sub-section's — would give two sections one name.

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

A dispatched link's text names its sub-section, so the text is written
with each run of whitespace, a line break among them, as one space.
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
from prosiform.closure import Reference, dispatched, identity, parallel, unmarked
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
    PROSIFORM_SECTION,
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
    LINK_OPEN,
    Source,
    events,
    inlines,
    opening_text,
    regions,
    shown,
    slug,
)

DISPATCH_DEPTH = "W_DISPATCH_DEPTH"
DISPATCH_SELF = "W_DISPATCH_SELF"
DISPATCH_CYCLE = "E_DISPATCH_CYCLE"
HEADING_COLLISION = "E_HEADING_COLLISION"

CODES = (DISPATCH_DEPTH, DISPATCH_SELF, DISPATCH_CYCLE, HEADING_COLLISION)

PROSIFORM = "Prosiform"
PARALLEL = "Dispatch in parallel"
DISPATCH = "Dispatch"
PARALLEL_DISPATCH = "Parallel dispatch"

DISPATCH_PROTOCOL = (
    "Hand the named bundle to one sub-agent, with the inputs the invoking step "
    "names, to follow from its start, and continue with the result it returns. "
    "A dispatched run puts no question to the user: it returns each question, "
    "with its context paragraph and options, unanswered. The dispatching "
    "session puts each returned question to the user, or returns it in turn "
    "when itself dispatched, then dispatches again with the answers."
)


def protocol_link(name: str) -> str:
    """A link to one protocol sub-section of the Prosiform section."""
    return f"[{name}](#{slug(name)})"


PARALLEL_PROTOCOL = (
    "Dispatch every listed bundle at once, each to a sub-agent of its own as "
    f"{protocol_link(DISPATCH)} states; an item the invoking step applies "
    '"for each" of several values is dispatched once per value, together. '
    "Continue when every item has returned. A failed item cancels nothing: the "
    "set returns every failure together as blockers. Questions items return "
    "are put to the user together once every item has returned, and only the "
    "items that asked are dispatched again."
)

TOGETHER = (
    "Dispatch these bundles together, each to a sub-agent, as "
    f"{protocol_link(PARALLEL_DISPATCH)} states:"
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

Placed = dict[tuple[str, int], dict[Served, int]]
"""Each dispatch sub-section's heading, by the region and link it serves.

A region is the document and the first line of content it opens on, so
every link one region writes naming one target with one operator
reaches one sub-section, and the value is that heading's position among
every heading the bundle emits.
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
                    target,
                    " ".join(unmarked(link_text(children, at)).split()),
                    destination,
                    Location(path, 1 if line is None else line, 1),
                    parallel(opening),
                    opening,
                )
            )
    return found


def instruction(bundle_file: str) -> str:
    """The one line a dispatch sub-section carries."""
    return (
        f"Dispatch `{bundle_file}` to a sub-agent, as {protocol_link(DISPATCH)} states."
    )


def listing(entries: Sequence[tuple[str, str]]) -> str:
    """The list a `Dispatch in parallel` sub-section carries, one bundle an item."""
    return "\n".join(f"- `{file}` ({escaped(text)})" for file, text in entries)


def region_of(tokens: Sequence[Token], part: Range) -> Token:
    """The region of a parse one selected range holds."""
    return next(one for one in regions(tokens) if one.map == list(part.lines))


class Placing:
    """One bundle's groups rebuilt with its Prosiform section and its sub-sections.

    The operators are those the bundle's dispatched links carry, `False`
    for `⇉` and `True` for `⫽`, which decide the protocols the
    Prosiform section states.
    """

    def __init__(
        self,
        parsed: Mapping[str, Sequence[Token]],
        read: Mapping[str, Source],
        bundle_file: Callable[[Target], str],
        operators: Collection[bool],
    ) -> None:
        self.parsed = parsed
        self.read = read
        self.bundle_file = bundle_file
        self.operators = operators
        self.opened = False
        self.placed: Placed = {}
        self.at = 0
        self.emitted: list[str] = []
        self.parts: list[Part] = []
        self.headings: list[Emitted] = []
        self.pending: dict[Served, Link] = {}
        self.serving: list[tuple[tuple[str, int], Served]] = []
        self.level: int | None = None

    def heading(
        self,
        text: str,
        depth: int,
        body: Sequence[Instruction],
        kind: str = DISPATCH_SECTION,
    ) -> int:
        """Emit one generated section, returning its heading's bundle position."""
        at = self.at + len(self.headings)
        self.emitted.append(f"{ATX * depth} {escaped(text)}")
        self.parts.append(Generated(text, depth, kind))
        self.headings.append(Generated(text, depth, kind))
        for one in body:
            self.emitted.append(one.text)
            self.parts.append(one)
        return at

    def open(self) -> bool:
        """Emit the Prosiform section once, where the bundle dispatches.

        It is called ahead of the bundle's first heading, and reports
        whether it emitted the section there.
        """
        if self.opened or not self.operators:
            return False
        self.opened = True
        self.heading(PROSIFORM, 1, [], PROSIFORM_SECTION)
        self.heading(DISPATCH, 2, [Instruction(DISPATCH_PROTOCOL)], PROSIFORM_SECTION)
        if True in self.operators:
            self.heading(
                PARALLEL_DISPATCH,
                2,
                [Instruction(PARALLEL_PROTOCOL)],
                PROSIFORM_SECTION,
            )
        return True

    def flush(self, following: int | None) -> None:
        """Emit the sub-sections the section just closed carries.

        Each `⇉` target takes a sub-section of its own, in the order its
        first link is written, and the section's `⫽` set takes one after
        them. Ahead of the bundle's first heading, and ahead of content
        above it that dispatches, the Prosiform section comes first.
        """
        if self.level is None and (following is not None or self.pending):
            self.open()
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
        serving: dict[Served, int] = {}
        together: list[Link] = []
        for served, link in self.pending.items():
            if link.parallel:
                together.append(link)
                continue
            body = Instruction(instruction(self.bundle_file(link.target)))
            serving[served] = self.heading(f"{DISPATCH} {link.text}", depth, [body])
        if together:
            listed = listing(
                [(self.bundle_file(link.target), link.text) for link in together]
            )
            at = self.heading(
                PARALLEL, depth, [Instruction(TOGETHER), Instruction(listed, True)]
            )
            serving.update((link.served, at) for link in together)
        for key, served in self.serving:
            self.placed.setdefault(key, {})[served] = serving[served]
        self.pending = {}
        self.serving = []

    def group(self, one: Group) -> Group:
        """One group with its sub-sections, the headings before it counted.

        A file heading the Prosiform section precedes is a part of the
        group rather than the heading it opens on.
        """
        offset = 1 if one.wrapped else 0
        wrapped = one.wrapped
        self.emitted = []
        self.parts = []
        self.headings = []
        self.level = None
        if one.wrapped:
            wrapper = one.record.headings[0]
            assert isinstance(wrapper, Generated)
            if self.open():
                wrapped = False
                self.parts.append(wrapper)
            self.emitted.append(one.parts[0])
            self.headings.append(wrapper)
            self.level = 1
        at = offset
        for part, text in zip(one.record.parts, one.parts[offset:], strict=True):
            if isinstance(part, Ancestor | Generated):
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
                for link in written_in(part.path, self.read[part.path], tokens, region):
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
            one.order,
            wrapped=wrapped,
        )


def subsections(
    groups: Sequence[Group],
    parsed: Mapping[str, Sequence[Token]],
    read: Mapping[str, Source],
    bundle_file: Callable[[Target], str],
) -> tuple[list[Group], Placed]:
    """Every group with the bundle's generated sections, and where each one stands.

    A group's sections are read in the order it emits them: a heading
    part closes the section above it, and the sub-sections that section
    collected are emitted ahead of the heading. A wrapped group's file
    heading opens its first section; a group the parent's title opens
    has no section above that title, so a dispatch there takes the
    level of the heading that follows it. The operators the bundle's
    links carry are read first, because the Prosiform section stating
    their protocols precedes every one of them.
    """
    operators = {
        link.parallel
        for one in groups
        for part in one.record.ranges
        for link in written_in(
            part.path,
            read[part.path],
            parsed[part.path],
            region_of(parsed[part.path], part),
        )
    }
    placing = Placing(parsed, read, bundle_file, operators)
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
    emitted = {
        one.text
        for group in groups
        for one in group.record.headings
        if isinstance(one, Generated)
        and one.kind in (DISPATCH_SECTION, PROSIFORM_SECTION)
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
) -> dict[tuple[str, int], dict[Served, str]]:
    """The destination each region's dispatched links take, by link."""
    return {
        key: {link: assigned[at] for link, at in served.items()}
        for key, served in placed.items()
    }
