"""Dispatch: the bundles a run's dispatches name, and where each is handed off.

A `⇉` link states that a sub-agent follows its target, and a `⫽` link
that a sub-agent follows it together with the other `⫽` links of its
section, so a run compiles every target either reaches, transitively,
each distinct document, fragment and effective preset selection once as
its own entry, and publishes each as a bundle beside the one that dispatches
it. A *dispatch depth* is the number of dispatch hops along one chain
of those bundles, counted from the run's entry: a dispatch the entry
carries is the first hop, a dispatch that target's bundle carries is
the second, and so on.

A `⇉` link publishes where its author wrote it, with its mark, pointing
at the file its target was compiled to. The `⫽` links in a section's own
content are one *set*. A set of two or more distinct selections points at
the section's one `⫽ Dispatch Set` sub-section: a heading one level below
the section, after the section's own content and before its child
sections, whose list holds each selection once as a `⇉` link to its file.
A set of one selection publishes as that single `⇉` link and carries no
sub-section. A set states no order. A set above the group's first
heading takes that heading's level. Each section carrying a set
carries its own sub-section. The sub-sections are inserted into a group
once it is built, before the bundle's destinations are assigned, so the
ordinal a renderer gives a repeated heading counts them as it counts
every other heading.

A `⇉` link carrying the pick token names one selection for each
alternative its target declares, and points at a `⇉ Dispatch Pick`
sub-section of its own, placed as a set's is and after it, whose lines
list each alternative's bundle beside its choice line in declaration
order, so the dispatching agent hands on one.

A dispatch whose target's presets in force name a *brief* carries that
section of its target into this bundle around the dispatch line, so the
dispatching agent reads it before handing the bundle on. A `⇉`
link carrying one, or a set of one, is lifted into a sub-section of its
own, headed by its mark and its text and placed as a set's is and after
it, beside the section's pick sub-sections in the order their links are
written; a picking dispatch's sub-section holds its brief around its
pick lines; a set's lists its members carrying no brief as bare lines,
then lifts each briefed member into a sub-section of its own one level
below the set's, each in the set's order. A brief is published as its lead content, the
content above its first heading, then the dispatch line, then its child
sections and the sections its directives compose, each one level below
the sub-section holding it, so the line stands under no heading the
brief emits. A dispatch a brief writes is a dispatch of its own, never a
member of a set around it: it publishes where the brief writes it, and
takes its sub-sections one level below the sub-section holding the
brief, after the brief. Each copy of a brief places its dispatches
anew, as `Placing` states.

A dispatch has to be one a sub-agent can finish and one the bundle can
place, so four dispatches publish nothing:

- A chain of bundles returning to one already on it is a cycle: its
  sub-agents would dispatch one another without end. A dispatch naming
  the run's own single selection closes the shortest one.
- A set, a picking dispatch or a briefed one in a level-6 section
  leaves no level for its sub-section.
- A brief whose dispatches carry briefs leading back to it would be
  lifted into itself without end, a cycle as a chain of bundles
  returning to one already on it is.
- An authored heading whose text equals `⫽ Dispatch Set`,
  `⇉ Dispatch Pick` or a lifted sub-section's heading in a bundle that
  emits one would give two sections one name, as would one lifted
  heading naming two selections.

A chain deeper than the limit still publishes, and warns: flattening it
is the author's optimisation rather than a defect. A dispatch naming
the document that writes it, which closes no cycle, hands a sub-agent
material its own session compiles, so it warns as well. A target's
shape is the corpus's convention, so a dispatch states no rule on it.

A chain is deeper than the limit where it reaches a hop past it, and
the search for one stops there. A target already on a chain is not
followed again, so both searches terminate on any graph of dispatches.
The dispatches a bundle carries name each effective selection once, at
the first link naming it, so each search follows each selection once.

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
    UNSUBSTITUTED,
    BundleSelection,
    Declarations,
    Reference,
    Substitution,
    alternatives_of,
    briefing,
    dispatched,
    identity,
    parallel,
    picking,
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
from prosiform.marks import DISPATCH_MARK
from prosiform.provenance import (
    BRIEF_SECTION,
    COMPOSED_HEADINGS,
    FILENAME_WRAPPER,
    PARALLEL_SECTION,
    PICK_SECTION,
    Ancestor,
    Carried,
    Dispatching,
    Emitted,
    Generated,
    Instruction,
    Located,
    Part,
    Preamble,
    Range,
    Record,
    Region,
    Served,
    Target,
    click_at,
    link_at,
)
from prosiform.provenance import Placing as Chain
from prosiform.source import (
    ANCHOR,
    FENCE,
    INLINE,
    LINK_OPEN,
    Click,
    Source,
    clicks,
    events,
    opening_text,
    regions,
    shown,
    within,
)
from prosiform.tags import read as read_tags

DISPATCH_DEPTH = "W_DISPATCH_DEPTH"
DISPATCH_SELF = "W_DISPATCH_SELF"
DISPATCH_CYCLE = "E_DISPATCH_CYCLE"
HEADING_COLLISION = "E_HEADING_COLLISION"

CODES = (DISPATCH_DEPTH, DISPATCH_SELF, DISPATCH_CYCLE, HEADING_COLLISION)

PARALLEL = "\u2afd Dispatch Set"
"""The heading a set's sub-section takes.

The mark leads, so a reader meets the symbol before the words, and the
words name the structure rather than repeating the section the sub-section
already stands under. A bundle's sets share this heading, so the renderer's
ordinals keep them apart as it keeps any repeated heading apart.
"""

PICKING = "⇉ Dispatch Pick"
"""The heading a `⇉` link carrying the pick token takes for its sub-section.

The mark leads, as the set's does, and the words name the structure: a
listing of one bundle for each alternative, of which the dispatching
agent hands on one.
"""

CHOICE_SEPARATOR = "—"
"""What stands between a picking dispatch's line and its choice line."""

TOGETHER = ""
"""A set's sub-section states no instruction of its own.

The guide holds what a `⫽` link means and how its members are handed over,
so a bundle that restated it would be a second home of the same rule.
"""

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
LEVEL_REMEDY = "move the dispatch to a shallower section"
COLLISION_REMEDY = "retitle the authored heading"
LIFT_REMEDY = "write one of the two dispatches with other link text"
BRIEF_CYCLE_REMEDY = "dispatch one target of the cycle without a brief"

Placed = dict[Region, dict[Served, int | str]]
"""Where each dispatched link points, by the placed region and link it serves.

A placed region is the document, the first line of content it opens on
and the placing of the copy carrying it, so every link one copy of a
region writes naming one target with the same requested tags and
operator points at one place. The place is the position of a dispatch-set
sub-section among every heading the bundle emits, or the destination of
a bundle file.
"""

Anchors = Dispatching
"""The destination each placed region's dispatched links take, by link."""


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


Onward = Callable[[BundleSelection], Mapping[BundleSelection, Hop]]
"""The dispatches one bundle carries, keyed by effective destination selection."""


def deepest(
    onward: Onward,
    selection: BundleSelection,
    first: Hop,
    entries: Collection[BundleSelection],
) -> list[Hop] | None:
    """The first chain from one hop that reaches a hop past the limit.

    A chain is followed in the order each bundle writes its dispatches,
    and only through targets not already on it, so a cycle adds no depth.
    """
    chain = [(selection, first)]
    on = {*entries, selection}
    pending = [iter(onward(selection).items())]
    while pending:
        if len(chain) > LIMIT:
            return [hop for _selection, hop in chain]
        following = next(pending[-1], None)
        if following is None:
            pending.pop()
            on.discard(chain.pop()[0])
            continue
        target, hop = following
        if target in on:
            continue
        chain.append((target, hop))
        on.add(target)
        pending.append(iter(onward(target).items()))
    return None


def returning(
    onward: Onward,
    selection: BundleSelection,
    first: Hop,
    entries: Collection[BundleSelection],
) -> list[Hop] | None:
    """The first chain from one hop whose last hop names a target already on it.

    The entries stand on every chain, so a dispatch naming the run's own
    selection closes a cycle. A target every chain through which was
    followed to its end without returning is not followed again.
    """
    if selection in entries:
        return [first]
    chain = [(selection, first)]
    on = {*entries, selection}
    done: set[BundleSelection] = set()
    pending = [iter(onward(selection).items())]
    while pending:
        following = next(pending[-1], None)
        if following is None:
            pending.pop()
            target = chain.pop()[0]
            on.discard(target)
            done.add(target)
            continue
        target, hop = following
        if target in on:
            return [*(one for _selection, one in chain), hop]
        if target in done:
            continue
        chain.append((target, hop))
        on.add(target)
        pending.append(iter(onward(target).items()))
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


def cycle(
    hops: Mapping[BundleSelection, Hop],
    entries: Collection[BundleSelection],
    onward: Onward,
) -> None:
    """Refuse the first chain of the run's dispatches returning to a target on it.

    Each distinct selection the entry dispatches is followed from the first
    link naming it, in the order the entry's bundle wrote them.
    """
    for selection, first in hops.items():
        loop = returning(onward, selection, first, entries)
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
    hops: Mapping[BundleSelection, Hop],
    entries: Collection[BundleSelection],
    onward: Onward,
) -> list[Diagnostic]:
    """The depth warnings the dispatches the run's entry carries raise.

    Each distinct selection the entry dispatches is followed from the first
    link naming it, and raises at most one warning: for the first chain
    from it reaching a hop past the limit.
    """
    found: list[Diagnostic] = []
    for selection, first in hops.items():
        deep = deepest(onward, selection, first, entries)
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
    at: Located

    @property
    def target(self) -> Target:
        """The document and section the link names."""
        return (self.reference.path, self.reference.fragment)

    @property
    def served(self) -> Served:
        """Where the occurrence points, as its target, requested tags and operator."""
        return (self.target, self.reference.tags, self.parallel)

    @property
    def picking(self) -> bool:
        """Whether the link is a `⇉` dispatch leaving its pick to its agent."""
        return picking(self.opening, self.reference.tags)


Briefer = Callable[
    [Link, Reference, int, Chain], tuple[list[str], list[Part], list[Emitted]]
]
"""What composes one dispatch's brief beneath a heading at a depth.

It takes the dispatch, the brief's composing reference, the depth and
the placing of the copy writing the dispatch, and gives the text, parts
and headings the brief emits.
"""


def fits(depth: int, first: Link) -> None:
    """Refuse a sub-section a dispatch would emit beyond the last level."""
    if depth <= MAX_LEVEL:
        return
    raise Refused(
        Diagnostic(
            ERROR,
            f"the dispatch {first.written!r} would emit its sub-section at "
            f"level {depth}, which is beyond H{MAX_LEVEL}",
            code=HEADING_DEPTH_OVERFLOW,
            reference=first.written,
            remedy=LEVEL_REMEDY,
            location=first.location,
        )
    )


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


def element_text(click: Click) -> str:
    """One diagram link's `source.Click` opening, its marks taken off, or its node."""
    return " ".join(unmarked(click.opening).split()) or click.node


def written_in(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    region: Token,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> list[Link]:
    """Every dispatched link one region writes, diagram links among them, in order.

    A link's text is what its reader reads in it, its marks taken off,
    as `element_text` reads a diagram link's.
    """
    found: list[Link] = []
    for block in within(tokens, [region]):
        if block.type == FENCE:
            found.extend(
                link
                for click in clicks(block)
                if (
                    link := dispatched_link(
                        path,
                        click.destination,
                        click.opening,
                        click.title,
                        element_text(click),
                        source.line(click.line),
                        declarations,
                        substitution,
                        click_at(path, click),
                    )
                )
                is not None
            )
            continue
        if block.type != INLINE:
            continue
        line = source.line(None if block.map is None else block.map[0] + 1)
        start = 0 if block.map is None else block.map[0]
        position = 0
        for children, at, child in events(block.children or []):
            if child.type != LINK_OPEN:
                continue
            here = position
            position += 1
            title = child.attrGet("title")
            link = dispatched_link(
                path,
                str(child.attrGet("href") or ""),
                opening_text(children, at),
                None if title is None else str(title),
                " ".join(unmarked(link_text(children, at)).split()),
                line,
                declarations,
                substitution,
                link_at(path, block, start, here),
            )
            if link is not None:
                found.append(link)
    return found


def dispatched_link(
    path: str,
    destination: str,
    opening: str,
    title: str | None,
    text: str,
    line: int | None,
    declarations: Declarations,
    substitution: Substitution,
    at: Located,
) -> Link | None:
    """The dispatched link one use states, where its operator dispatches a target."""
    if not dispatched(opening):
        return None
    target = withheld(
        path,
        destination,
        opening,
        declarations,
        substitution,
        tags=read_tags(title),
    )
    if target is None:
        return None
    return Link(
        target,
        text,
        destination,
        Location(path, 1 if line is None else line, 1),
        parallel(opening),
        opening,
        at,
    )


def file_destination(bundle_file: str) -> str:
    """The destination a link takes to one bundle file beside the bundle."""
    return quote(bundle_file, safe="")


def listing(entries: Sequence[tuple[str, str]]) -> str:
    """The lines a set's sub-section carries, one `⇉` link to a bundle each.

    The mark stands where a bullet would: every line opens with `⇉`, so a
    reader meets the dispatch symbol first and no second list marker is
    needed to tell the members apart.
    """
    return "\n".join(
        f"[{DISPATCH_MARK} {escaped(text)}]({file_destination(file)})"
        for file, text in entries
    )


def choices(entries: Sequence[tuple[str, str, str]]) -> str:
    """The lines a picking dispatch's sub-section carries, one per alternative.

    Each line is a `⇉` link to the alternative's bundle, as a set's member
    is, followed by the alternative's choice line, so its reader picks the
    bundle whose choice line fits its work.
    """
    return "\n".join(
        f"[{DISPATCH_MARK} {escaped(text)}]({file_destination(file)}) "
        f"{CHOICE_SEPARATOR} {escaped(choice)}"
        for file, text, choice in entries
    )


def region_of(tokens: Sequence[Token], part: Range) -> Token:
    """The region of a parse one selected range holds."""
    return next(one for one in regions(tokens) if one.map == list(part.lines))


class Placing:
    """One bundle's groups rebuilt with the dispatch sub-sections its sections take.

    The grouped regions are those a group carries as its own, by the
    document and first line naming each. A dispatch a contribution
    carries points where its source's own region is given where a group
    carries that region. Where none does, the region's first contribution
    gives the dispatch a place of its own, which every later copy of the
    region shares: a set's sub-section sits beneath the composed section
    holding the link and ahead of the next composed heading, so a scope's
    own sub-sections still follow its destination sections. A brief is
    lifted with the dispatch carrying it, so each copy of a brief places
    the dispatches it writes beneath its own sub-section.
    """

    def __init__(
        self,
        parsed: Mapping[str, Sequence[Token]],
        read: Mapping[str, Source],
        bundle_file: Callable[[Reference], str],
        grouped: Collection[tuple[str, int]],
        briefer: Briefer,
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
        self.serving: list[tuple[Region, Served]] = []
        self.level: int | None = None
        self.title = ""
        """The title of the heading whose section a set's sub-section sits under."""
        self.inner: dict[Served, Link] = {}
        self.inner_serving: list[tuple[Region, Served]] = []
        self.inner_level = 0
        self.briefer = briefer
        self.briefs: dict[Served, Reference | None] = {}
        self.lifts: dict[str, str] = {}
        """The bundle file each lifted sub-section's heading names."""
        self.first: dict[tuple[str, int], Region] = {}
        """The copy of each composed region whose dispatches its later copies share."""
        self.aliases: list[tuple[Region, Region]] = []
        """Each later copy of a region, beside the copy whose places it takes."""
        self.writing: dict[Served, Chain] = {}
        """The placing of the copy writing each dispatch while its section is placed."""
        self.expanding: list[tuple[tuple[str, str | None, frozenset[str]], Link]] = []
        """The briefs being lifted, outermost first, with the dispatch carrying each."""

    def heading(self, text: str, depth: int, kind: str) -> int:
        """Emit one generated heading, returning its bundle position."""
        at = self.at + len(self.headings)
        self.emitted.append(f"{ATX * depth} {escaped(text)}")
        self.parts.append(Generated(text, depth, kind))
        self.headings.append(Generated(text, depth, kind))
        return at

    def say(self, one: Instruction) -> None:
        """Emit one block the bundle writes itself."""
        self.emitted.append(one.text)
        self.parts.append(one)

    def briefed(
        self,
        link: Link,
        depth: int,
        lines: Sequence[Instruction],
    ) -> None:
        """Emit the brief one dispatch carries around the lines handing it on.

        The brief stands beneath a sub-section heading at `depth`, as the
        briefer composes it: its lead content, the content above the
        first heading it emits, then the lines, then its child sections
        and the sections its directives compose, one level below. The
        dispatches it writes then take their sub-sections one level below
        as well, each section of the brief placing its own as a section of
        a group does. A dispatch carrying no brief is followed by its lines
        alone.

        A brief already being lifted on the chain of briefs reaching this
        one would be lifted inside itself without end, so it is refused as
        a dispatch cycle naming each dispatch on that chain.
        """
        found = self.briefs.get(link.served)
        if found is None:
            for one in lines:
                self.say(one)
            return
        self.looping(link)
        self.expanding.append(((found.path, found.fragment, found.tags), link))
        emitted, parts, headings = self.briefer(
            link, found, depth, self.writing.get(link.served, ())
        )
        lead = next(
            (
                at
                for at, part in enumerate(parts)
                if isinstance(part, Generated)
                or (
                    isinstance(part, Range)
                    and region_of(self.parsed[part.path], part).type == HEADING_OPEN
                )
            ),
            len(parts),
        )
        self.emitted.extend(emitted[:lead])
        self.parts.extend(parts[:lead])
        for one in lines:
            self.say(one)
        self.emitted.extend(emitted[lead:])
        self.parts.extend(parts[lead:])
        self.headings.extend(headings)
        sections: list[tuple[dict[Served, Link], list[tuple[Region, Served]]]] = [
            ({}, [])
        ]
        for part in parts:
            if isinstance(part, Generated):
                sections.append(({}, []))
                continue
            if not isinstance(part, Range):
                continue
            tokens = self.parsed[part.path]
            if region_of(tokens, part).type == HEADING_OPEN:
                sections.append(({}, []))
            nested, nesting = sections[-1]
            region: Region = (part.path, part.lines[0], part.placing)
            self.first.setdefault((part.path, part.lines[0]), region)
            for each in written_in(
                part.path,
                self.read[part.path],
                tokens,
                region_of(tokens, part),
                self.declarations,
                self.substitution,
            ):
                nested.setdefault(each.served, each)
                if (region, each.served) not in nesting:
                    nesting.append((region, each.served))
        for nested, nesting in sections:
            self.place(nested, nesting, depth + 1)
        self.expanding.pop()

    def looping(self, link: Link) -> None:
        """Refuse a dispatch whose brief the chain of briefs carrying it carries.

        It runs before the dispatch's sub-section is fitted to a level, so
        a loop is reported as the cycle it is wherever it starts.
        """
        found = self.briefs.get(link.served)
        if found is None:
            return
        key = (found.path, found.fragment, found.tags)
        if any(each == key for each, _link in self.expanding):
            raise self.cycling(link)

    def cycling(self, link: Link) -> Refused:
        """The refusal of a brief reached again through the briefs carrying it.

        It names the chain from the document writing the outermost
        dispatch through each target whose brief is being carried, the
        location of the dispatch closing the loop, and each earlier
        dispatch as related, as a composition cycle is refused.
        """
        earlier = [each for _key, each in self.expanding]
        names = tuple(identity(each.reference) for each in (*earlier, link))
        return Refused(
            Diagnostic(
                ERROR,
                f"the dispatch {link.written!r} carries the brief of "
                f"{names[-1]!r}, which the chain of briefs carrying it already "
                f"carries, so the brief would be lifted inside itself without end",
                code=DISPATCH_CYCLE,
                reference=link.written,
                chain=(earlier[0].location.file, *names),
                remedy=BRIEF_CYCLE_REMEDY,
                location=link.location,
                related=tuple(
                    RelatedLocation(
                        each.location.file,
                        each.location.line,
                        each.location.column,
                        f"carries the brief of {identity(each.reference)!r}",
                    )
                    for each in earlier
                ),
            )
        )

    def lifted(self, link: Link, file: str, depth: int) -> int:
        """Emit the sub-section a dispatch carrying a brief is lifted into.

        Its heading is the dispatch mark and the link's text, its body
        the brief and then the dispatch line naming the target's bundle
        file, as `briefed` places them, and the sub-sections of the
        dispatches the brief writes. A heading is held to one effective
        selection across the bundle, so a second dispatch naming another
        selection under the same heading, or one equal to the dispatch-pick
        heading, is refused.
        """
        text = f"{DISPATCH_MARK} {link.text}"
        earlier = self.lifts.get(text)
        if text == PICKING or (earlier is not None and earlier != file):
            raise Refused(
                Diagnostic(
                    ERROR,
                    f"the dispatch {link.written!r} carries a brief under the "
                    f"heading {text!r}, which pf emits in the same bundle for "
                    f"another dispatch",
                    code=HEADING_COLLISION,
                    reference=link.written,
                    remedy=LIFT_REMEDY,
                    location=link.location,
                )
            )
        self.lifts[text] = file
        self.looping(link)
        fits(depth, link)
        at = self.heading(text, depth, BRIEF_SECTION)
        self.briefed(link, depth, [Instruction(listing([(file, link.text)]))])
        return at

    def flush(self, following: int | None) -> None:
        """Emit the sub-section the section just closed carries.

        The section's `⫽` set takes one where it holds two or more
        targets. Content above the bundle's first heading takes that
        heading's level, and the heading's title is the one the
        sub-section derives its own from.
        """
        self.close()
        if not self.pending:
            return
        depth = (following or 1) if self.level is None else self.level + 1
        if self.level is None:
            # Content above the bundle's first heading now stands inside the
            # instruction heading, so its set belongs one level below that.
            depth += 1
        self.place(self.pending, self.serving, depth, self.title)
        self.title = ""
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
        links: Sequence[tuple[Region, Served]],
        depth: int,
        title: str = "",
    ) -> None:
        """Say where one section's dispatched links point, emitting its sub-sections.

        A `⇉` link and every `⫽` link in a set of one effective selection
        point at their target's bundle file. A set of two or more
        selections points at the dispatch-set sub-section emitted here.
        Equivalent requests share one member, retaining its first link's
        label. Its members carrying no brief are listed first, in the
        set's order, since a line after a member's sub-section would stand
        beneath it, and each carrying one is then lifted into a sub-section
        one level below the set's, in the set's order. Each
        distinct `⇉` link carrying the pick token, and each link outside a
        set of two or more carrying a brief, then points at a sub-section
        of its own, in the order its first link is written: a
        dispatch-pick sub-section holding its brief and listing its
        target's alternatives in declaration order, or the one `lifted`
        emits, which links sharing their text and effective selection
        share.
        """
        for key, served in links:
            self.writing.setdefault(served, key[2])
        files = {
            served: self.bundle_file(link.reference)
            for served, link in pending.items()
            if not link.picking
        }
        for served, link in pending.items():
            if served not in self.briefs:
                self.briefs[served] = briefing(
                    link.reference, self.read[link.reference.path].conversion
                )
        together: dict[str, Link] = {}
        for served, link in pending.items():
            if link.parallel:
                together.setdefault(files[served], link)
        serving: dict[Served, int | str] = {
            served: file_destination(file) for served, file in files.items()
        }
        if len(together) > 1:
            fits(depth, next(iter(together.values())))
            at = self.heading(PARALLEL, depth, PARALLEL_SECTION)
            bare = [
                (file, link.text)
                for file, link in together.items()
                if self.briefs[link.served] is None
            ]
            if bare:
                self.say(Instruction(listing(bare)))
            for file, link in together.items():
                if self.briefs[link.served] is not None:
                    self.lifted(link, file, depth + 1)
            serving.update(
                (served, at) for served, link in pending.items() if link.parallel
            )
        lifts: dict[tuple[str, str], int] = {}
        for served, link in pending.items():
            if link.picking:
                serving[served] = self.picked(link, depth)
                continue
            if self.briefs[served] is None or (link.parallel and len(together) > 1):
                continue
            lift = (link.text, files[served])
            if lift not in lifts:
                lifts[lift] = self.lifted(link, files[served], depth)
            serving[served] = lifts[lift]
        for key, served in links:
            self.placed.setdefault(key, {})[served] = serving[served]
            self.writing.pop(served, None)

    def picked(self, link: Link, depth: int) -> int:
        """Emit the dispatch-pick sub-section of one dispatch carrying the pick token.

        Its body is the brief the dispatch carries, where it carries one,
        then one line for each alternative its target declares, as
        `briefed` places them.
        """
        self.looping(link)
        fits(depth, link)
        conversion = self.read[link.reference.path].conversion
        at = self.heading(PICKING, depth, PICK_SECTION)
        listed = choices(
            [
                (self.bundle_file(one), link.text, alternative.choice or "")
                for one, alternative in alternatives_of(link.reference, conversion)
            ]
        )
        self.briefed(link, depth, [Instruction(listed)])
        return at

    def group(self, one: Group) -> Group:
        """One group with its sub-sections, the headings before it counted."""
        offset = 1 if one.wrapped else 0
        self.emitted = []
        self.parts = []
        self.headings = []
        self.level = None
        self.title = ""
        if one.wrapped:
            wrapper = one.record.headings[0]
            self.emitted.append(one.parts[0])
            self.headings.append(wrapper)
            self.level = wrapper.level
            self.title = wrapper.text
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
                written = (part.path, part.lines[0])
                key: Region = (part.path, part.lines[0], part.placing)
                if written in self.grouped:
                    self.aliases.append((key, (part.path, part.lines[0], ())))
                elif self.first.setdefault(written, key) != key:
                    self.aliases.append((key, self.first[written]))
                else:
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
                self.title = one.record.headings[at].text
                self.headings.append(one.record.headings[at])
                at += 1
            elif isinstance(part, Range):
                tokens = self.parsed[part.path]
                region = region_of(tokens, part)
                preamble = isinstance(part, Preamble)
                held = len(carried_headings(tokens, region))
                if region.type == HEADING_OPEN:
                    self.flush(one.record.headings[at].level)
                    self.level = one.record.headings[at].level
                    self.title = one.record.headings[at].text
                self.headings.extend(one.record.headings[at : at + held])
                at += held
                key = (part.path, part.lines[0], ())
                if preamble:
                    self.emitted.append(text)
                    self.parts.append(part)
                    continue
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

    def shared(self) -> Placed:
        """Where each placed region's links point, a later copy sharing its first's."""
        for later, first in self.aliases:
            if first in self.placed:
                self.placed[later] = dict(self.placed[first])
        return self.placed


def subsections(
    groups: Sequence[Group],
    parsed: Mapping[str, Sequence[Token]],
    read: Mapping[str, Source],
    bundle_file: Callable[[Reference], str],
    briefer: Briefer,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> tuple[list[Group], Placed]:
    """Every group with its dispatch sub-sections, and where each link points.

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
    placing = Placing(
        parsed, read, bundle_file, grouped, briefer, declarations, substitution
    )
    rebuilt = [placing.group(one) for one in groups]
    return rebuilt, placing.shared()


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
        if isinstance(one, Generated)
        and one.kind in (PARALLEL_SECTION, PICK_SECTION, BRIEF_SECTION)
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


def anchors(placed: Placed, assigned: Sequence[str]) -> dict[Region, dict[Served, str]]:
    """The destination each placed region's dispatched links take, by link."""
    return {
        key: {
            link: f"{ANCHOR}{assigned[at]}" if isinstance(at, int) else at
            for link, at in served.items()
        }
        for key, served in placed.items()
    }
