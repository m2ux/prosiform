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
section of its target into this bundle, ahead of the dispatch line, so
the dispatching agent reads it before handing the bundle on. A `⇉`
link carrying one, or a set of one, is lifted into a sub-section of its
own, headed by its mark and its text and placed as a set's is and after
it, beside the section's pick sub-sections in the order their links are
written; a picking dispatch's sub-section
holds its brief above its pick lines; a set's holds each briefed
member's brief above that member's line.

A dispatch has to be one a sub-agent can finish and one the bundle can
place, so four dispatches publish nothing:

- A chain of bundles returning to one already on it is a cycle: its
  sub-agents would dispatch one another without end. A dispatch naming
  the run's own single selection closes the shortest one.
- A set, a picking dispatch or a briefed one in a level-6 section
  leaves no level for its sub-section.
- A brief emitting a heading or writing a dispatch leaves its dispatch
  line governed by something other than the brief, as `unbriefable`
  states.
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
from prosiform.profile import UNSUPPORTED_CONSTRUCT
from prosiform.provenance import (
    BRIEF_SECTION,
    COMPOSED_HEADINGS,
    FILENAME_WRAPPER,
    PARALLEL_SECTION,
    PICK_SECTION,
    Ancestor,
    Carried,
    Emitted,
    Generated,
    Instruction,
    Located,
    Part,
    Preamble,
    Range,
    Record,
    Served,
    Target,
    click_at,
    link_at,
)
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
LEVEL_REMEDY = "move the dispatch to a section above the sixth level"
COLLISION_REMEDY = "retitle the authored heading"
LIFT_REMEDY = "write one of the two dispatches with other link text"
BRIEF_REMEDY = (
    "name a brief holding no heading and no dispatch, and link the rest of its material"
)

Placed = dict[tuple[str, int], dict[Served, int | str]]
"""Where each dispatched link points, by the region and link it serves.

A region is the document and the first line of content it opens on, so
every link one region writes naming one target with the same requested
tags and operator points at one place. The place is the position of a dispatch-set
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


Briefer = Callable[[Link, Reference, int], tuple[list[str], list[Part], list[Emitted]]]
"""What composes one dispatch's brief beneath a heading at a depth.

It takes the dispatch, the brief's composing reference and the depth,
and gives the text, parts and headings the brief emits.
"""


def unbriefable(link: Link, brief: Reference, what: str) -> Refused:
    """The refusal of a brief its dispatch line could not follow as it governs.

    A brief is content its dispatcher reads before the dispatch line, so
    a brief emitting a heading, for a subsection or a composition
    directive it holds, would put that line beneath the heading, and one
    writing a dispatch would hand on a bundle of its own beside the
    line. `what` names which the brief does.
    """
    return Refused(
        Diagnostic(
            ERROR,
            f"the dispatch {link.written!r} carries the brief "
            f"{identity(brief)!r}, which {what}, so its dispatch line would "
            f"not follow the brief it governs",
            code=UNSUPPORTED_CONSTRUCT,
            reference=link.written,
            resolved=identity(brief),
            remedy=BRIEF_REMEDY,
            location=link.location,
        )
    )


def fits(depth: int, first: Link) -> None:
    """Refuse a sub-section a level-6 section would emit beyond the last level."""
    if depth <= MAX_LEVEL:
        return
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
    """One bundle's groups rebuilt with the dispatch-set sub-sections its sets take.

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
        self.serving: list[tuple[tuple[str, int], Served]] = []
        self.level: int | None = None
        self.title = ""
        """The title of the heading whose section a set's sub-section sits under."""
        self.inner: dict[Served, Link] = {}
        self.inner_serving: list[tuple[tuple[str, int], Served]] = []
        self.inner_level = 0
        self.briefer = briefer
        self.briefs: dict[Served, Reference | None] = {}
        self.lifts: dict[str, str] = {}
        """The bundle file each lifted sub-section's heading names."""

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

    def brief(self, link: Link, depth: int) -> None:
        """Emit the brief one dispatch carries, as `briefing` names it, or nothing.

        The brief stands beneath a sub-section heading at `depth`, as the
        briefer composes it, and the dispatch line follows it. A brief
        writing a dispatch is refused, as `unbriefable` states.
        """
        found = self.briefs.get(link.served)
        if found is None:
            return
        emitted, parts, headings = self.briefer(link, found, depth)
        if any(
            written_in(
                part.path,
                self.read[part.path],
                self.parsed[part.path],
                region_of(self.parsed[part.path], part),
                self.declarations,
                self.substitution,
            )
            for part in parts
            if isinstance(part, Range)
        ):
            raise unbriefable(link, found, "writes a dispatch")
        self.emitted.extend(emitted)
        self.parts.extend(parts)
        self.headings.extend(headings)

    def lifted(self, link: Link, file: str, depth: int) -> int:
        """Emit the sub-section a dispatch carrying a brief is lifted into.

        Its heading is the dispatch mark and the link's text, its body
        the brief and then the dispatch line naming the target's bundle
        file. A heading is held to one effective selection across the
        bundle, so a second dispatch naming another selection under the
        same heading, or one equal to the dispatch-pick heading, is
        refused.
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
        fits(depth, link)
        at = self.heading(text, depth, BRIEF_SECTION)
        self.brief(link, depth)
        self.say(Instruction(listing([(file, link.text)])))
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
        links: Sequence[tuple[tuple[str, int], Served]],
        depth: int,
        title: str = "",
    ) -> None:
        """Say where one section's dispatched links point, emitting its sub-sections.

        A `⇉` link and every `⫽` link in a set of one effective selection
        point at their target's bundle file. A set of two or more
        selections points at the dispatch-set sub-section emitted here.
        Equivalent requests share one member, retaining its first link's
        label. Each distinct `⇉` link carrying the pick token, and each
        link outside a set of two or more carrying a brief, then points at
        a sub-section of its own, in the order its first link is written:
        a dispatch-pick sub-section listing its target's alternatives in
        declaration order, or the one `lifted` emits, which links sharing
        their text and effective selection share.
        """
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
            bare: list[tuple[str, str]] = []
            for file, link in together.items():
                if self.briefs[link.served] is None:
                    bare.append((file, link.text))
                    continue
                if bare:
                    self.say(Instruction(listing(bare)))
                bare = []
                self.brief(link, depth)
                self.say(Instruction(listing([(file, link.text)])))
            if bare:
                self.say(Instruction(listing(bare)))
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

    def picked(self, link: Link, depth: int) -> int:
        """Emit the dispatch-pick sub-section of one dispatch carrying the pick token.

        Its body is the brief the dispatch carries, where it carries one,
        then one line for each alternative its target declares.
        """
        fits(depth, link)
        conversion = self.read[link.reference.path].conversion
        at = self.heading(PICKING, depth, PICK_SECTION)
        self.brief(link, depth)
        listed = choices(
            [
                (self.bundle_file(one), link.text, alternative.choice or "")
                for one, alternative in alternatives_of(link.reference, conversion)
            ]
        )
        self.say(Instruction(listed))
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
                key = (part.path, part.lines[0])
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
