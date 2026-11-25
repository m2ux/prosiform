"""Inspect dispatch chains and place dispatch sections in built groups.

Chain searches return diagnostics or refusals. `Placing` rebuilds
groups and records link destinations; `anchors` binds those records
to assigned fragments. Link operations use `closure`, and diagram
links use `source.Click`.
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
    started_on,
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
    model_of,
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
    section,
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
"""The heading of a parallel dispatch set's subsection."""

CHOICE_SEPARATOR = "—"
"""What stands between a picking dispatch's line and its choice line."""

TOGETHER = ""
"""The instruction text emitted with a dispatch set."""

LINK_CLOSE = "link_close"

LIMIT = 3

DEPTH_REMEDY = (
    "bundle an intermediate target into the bundle that dispatches it, or "
    "dispatch its targets from an earlier hop"
)
SELF_REMEDY = (
    "move the procedure to a document of its own, or link it without the "
    "dispatch operator"
)
CYCLE_REMEDY = "bundle or cite one target of the cycle rather than dispatching it"
LEVEL_REMEDY = "move the dispatch to a shallower section"
COLLISION_REMEDY = "retitle the authored heading"
NAMED_REMEDY = (
    "write one of the two dispatches with other link text, or compose the "
    "section writing it under presets routing it alike"
)
BRIEF_CYCLE_REMEDY = "dispatch one target of the cycle without a brief"

Placed = dict[Region, dict[Served, int | str]]
"""A heading position or bundle-file destination for each region and served link."""

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
    """Refuse the first dispatch whose `returning` search finds a cycle.

    Search the supplied hops in their mapping order and report the first
    cycle through `reported`.
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
    """Return depth warnings from a `deepest` search of each supplied hop.

    Each mapping entry yields at most one diagnostic through `reported`.
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
        f"session bundles itself",
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
        """Whether `closure.picking` selects alternatives for this link."""
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
    """Normalize an unmarked `source.Click` opening, using its node when empty.

    Each whitespace run becomes one space. `closure.unmarked` owns
    operator removal.
    """
    return " ".join(unmarked(click.opening).split()) or click.node


def written_in(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    region: Token,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> list[Link]:
    """Collect dispatched links in one region, in source order.

    Diagram uses follow `source.Click` and `element_text`; Markdown text
    uses `link_text` and `closure.unmarked`, with whitespace runs joined
    by one space. `dispatched_link` owns target classification.
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
    """Build a link for a target accepted by `closure.withholding_target`.

    `closure.dispatched` selects its operation, `closure.parallel` its
    parallel flag, and `tags.read` its requested presets. Other uses
    yield none.
    """
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


def listing(entries: Sequence[tuple[str, str, str | None]]) -> str:
    """The lines a set's sub-section carries, one `⇉` link to a bundle each.

    The mark stands where a bullet would: every line opens with `⇉`, so a
    reader meets the dispatch symbol first and no second list marker is
    needed to tell the members apart. Each entry is a bundle file, its
    link text and the model its sub-agent starts on, which `started_on`
    writes after the link.
    """
    return "\n".join(
        f"[{DISPATCH_MARK} {escaped(text)}]({file_destination(file)})"
        f"{started_on(model)}"
        for file, text, model in entries
    )


def choices(entries: Sequence[tuple[str, str, str, str | None]]) -> str:
    """The lines a picking dispatch's sub-section carries, one per alternative.

    Use the dispatch-member format `listing` owns, followed by
    `CHOICE_SEPARATOR` and the escaped choice text.
    """
    return "\n".join(
        f"[{DISPATCH_MARK} {escaped(text)}]({file_destination(file)})"
        f"{started_on(model)} {CHOICE_SEPARATOR} {escaped(choice)}"
        for file, text, choice, model in entries
    )


def region_of(tokens: Sequence[Token], part: Range) -> Token:
    """The region of a parse one selected range holds."""
    return next(one for one in regions(tokens) if one.map == list(part.lines))


class Placing:
    """Rebuild groups with dispatch sections and retain each link's placement.

    `group` owns source and composed-region placement, `place` owns section
    contents, and `shared` binds repeated copies to their first placement.
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
        self.named_files: dict[str, tuple[str, ...]] = {}
        """The selected bundle files each named dispatch subsection addresses."""
        self.first: dict[tuple[str, int, tuple[Served, ...]], Region] = {}
        """The copy of each composed region whose dispatches its later copies share.

        A copy is held by the targets its dispatched links serve, in order.
        """
        self.aliases: list[tuple[Region, Region]] = []
        """Each later copy of a region, beside the copy whose places it takes."""
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
        outer: Chain,
    ) -> None:
        """Emit a dispatch's brief around its hand-off lines.

        `Briefer` supplies the composed parts. Emit their lead content, the
        lines, then their heading content. Each brief section's dispatches
        take sections below it through `close` and `place`. A link with no
        brief emits its lines alone. `outer` identifies the writing copy.
        """
        found = self.briefs.get(link.served)
        if found is None:
            for one in lines:
                self.say(one)
            return
        self.expanding.append(((found.path, found.fragment, found.tags), link))
        emitted, parts, headings = self.briefer(link, found, depth, outer)
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
            links = written_in(
                part.path,
                self.read[part.path],
                tokens,
                region_of(tokens, part),
                self.declarations,
                self.substitution.composed(part.path, part.selecting),
            )
            self.first.setdefault(
                (part.path, part.lines[0], tuple(each.served for each in links)),
                region,
            )
            for each in links:
                nested.setdefault(each.served, each)
                if (region, each.served) not in nesting:
                    nesting.append((region, each.served))
        for nested, nesting in sections:
            self.place(nested, nesting, depth + 1)
        self.expanding.pop()

    def model(self, target: Reference) -> str | None:
        """Return the dispatch model selected by `closure.model_of`."""
        return model_of(target, self.read[target.path].conversion)

    def brief_of(self, link: Link) -> Reference | None:
        """Cache the brief reference selected by `closure.briefing`."""
        if link.served not in self.briefs:
            self.briefs[link.served] = briefing(
                link.reference, self.read[link.reference.path].conversion
            )
        return self.briefs[link.served]

    def looping(self, link: Link) -> None:
        """Refuse a dispatch whose brief leads back to a brief carrying it.

        The briefs a dispatch's brief reaches are walked through the
        dispatches each brief writes, before the dispatch's sub-section is
        fitted to a level, so a loop is reported as the dispatch cycle it
        is wherever it starts, naming each dispatch on it. A brief being
        lifted around this dispatch is on the loop's chain already.
        """
        carrying = [key for key, _link in self.expanding]
        chain: list[tuple[tuple[str, str | None, frozenset[str]], Link]] = []
        # A brief whose every reachable brief was walked without closing a
        # loop closes none from any later path either, since a loop through
        # it would have returned to it while it stood on the chain.
        cleared: set[tuple[str, str | None, frozenset[str]]] = set()

        def walk(one: Link) -> None:
            found = self.brief_of(one)
            if found is None:
                return
            key = (found.path, found.fragment, found.tags)
            if key in carrying or any(each == key for each, _one in chain):
                raise self.cycling(one, [each for _key, each in chain])
            if key in cleared:
                return
            chain.append((key, one))
            tokens = self.parsed[found.path]
            for region in section(tokens, found.fragment or "") or ():
                for each in written_in(
                    found.path,
                    self.read[found.path],
                    tokens,
                    region,
                    self.declarations,
                    self.substitution.composed(found.path, found.tags),
                ):
                    walk(each)
            chain.pop()
            cleared.add(key)

        walk(link)

    def cycling(self, link: Link, reaching: Sequence[Link] = ()) -> Refused:
        """Build a brief-cycle refusal from the expanding and reaching links.

        The chain starts with the outermost writer and includes each target,
        the closing one last. Earlier dispatches supply related locations.
        """
        earlier = [*(each for _key, each in self.expanding), *reaching]
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

    def named(self, link: Link, files: tuple[str, ...]) -> str:
        """Reserve a dispatch's link text for its selected bundle files.

        One heading names one effective selection throughout the bundle;
        a different selection using that heading raises `HEADING_COLLISION`.
        """
        text = link.text
        earlier = self.named_files.get(text)
        if earlier is not None and earlier != files:
            raise Refused(
                Diagnostic(
                    ERROR,
                    f"the dispatch {link.written!r} uses the "
                    f"heading {text!r}, which pf emits in the same bundle for "
                    f"another dispatch",
                    code=HEADING_COLLISION,
                    reference=link.written,
                    remedy=NAMED_REMEDY,
                    location=link.location,
                )
            )
        self.named_files[text] = files
        return text

    def lifted(self, link: Link, file: str, depth: int, outer: Chain) -> int:
        """Emit a briefed dispatch's subsection and return its heading position.

        `named` reserves its heading, `looping` checks its brief chain,
        `fits` its depth, and `briefed` places its contents.
        """
        text = self.named(link, (file,))
        self.looping(link)
        fits(depth, link)
        at = self.heading(text, depth, BRIEF_SECTION)
        self.briefed(
            link,
            depth,
            [Instruction(listing([(file, link.text, self.model(link.reference))]))],
            outer,
        )
        return at

    def flush(self, following: int | None) -> None:
        """Place a closed section's dispatches through `place` and reset it.

        Use one level below its heading, or one below the following heading
        for content preceding the group's first heading. With neither
        heading present, use level two.
        """
        self.close()
        if not self.pending:
            return
        depth = (following or 1) if self.level is None else self.level + 1
        if self.level is None:
            # Content above the bundle's first heading stands inside the
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

        Parallel links share a set when they name more than one bundle
        file; each file retains its first member's label. The set takes
        the supplied depth, and its links point at its heading. When any
        member has a brief, `lifted` places every member below the set;
        otherwise `listing` supplies its lines. Other links point at
        their files, `picked` subsections, or `lifted` subsections as their
        selections require. Matching text and bundle files share a lift.
        Record every supplied occurrence's destination in `placed`.
        """
        writing: dict[Served, Chain] = {}
        for key, served in links:
            writing.setdefault(served, key[2])
        files = {
            served: self.bundle_file(link.reference)
            for served, link in pending.items()
            if not link.picking
        }
        for link in pending.values():
            self.brief_of(link)
        together: dict[str, Link] = {}
        for served, link in pending.items():
            if link.parallel:
                together.setdefault(files[served], link)
        serving: dict[Served, int | str] = {
            served: file_destination(file) for served, file in files.items()
        }
        if len(together) > 1:
            for link in together.values():
                self.looping(link)
            fits(depth, next(iter(together.values())))
            at = self.heading(PARALLEL, depth, PARALLEL_SECTION)
            if any(self.briefs[link.served] is not None for link in together.values()):
                for file, link in together.items():
                    self.lifted(link, file, depth + 1, writing.get(link.served, ()))
            else:
                self.say(
                    Instruction(
                        listing(
                            [
                                (file, link.text, self.model(link.reference))
                                for file, link in together.items()
                            ]
                        )
                    )
                )
            serving.update(
                (served, at) for served, link in pending.items() if link.parallel
            )
        lifts: dict[tuple[str, str], int] = {}
        for served, link in pending.items():
            if link.picking:
                serving[served] = self.picked(link, depth, writing.get(served, ()))
                continue
            if self.briefs[served] is None or (link.parallel and len(together) > 1):
                continue
            lift = (link.text, files[served])
            if lift not in lifts:
                lifts[lift] = self.lifted(
                    link, files[served], depth, writing.get(served, ())
                )
            serving[served] = lifts[lift]
        for key, served in links:
            self.placed.setdefault(key, {})[served] = serving[served]

    def picked(self, link: Link, depth: int, outer: Chain) -> int:
        """Emit one dispatch-pick subsection and return its heading position.

        `closure.alternatives_of` supplies the choices, `named` reserves
        their heading, and `choices` renders them. `briefed` places the
        brief around their lines, `looping` checks its chain, and `fits`
        checks the heading depth.
        """
        self.looping(link)
        fits(depth, link)
        conversion = self.read[link.reference.path].conversion
        alternatives = list(alternatives_of(link.reference, conversion))
        files = tuple(self.bundle_file(one) for one, _ in alternatives)
        at = self.heading(self.named(link, files), depth, PICK_SECTION)
        listed = choices(
            [
                (
                    file,
                    link.text,
                    alternative.choice or "",
                    model_of(one, conversion),
                )
                for file, (one, alternative) in zip(files, alternatives, strict=True)
            ]
        )
        self.briefed(link, depth, [Instruction(listed)], outer)
        return at

    def group(self, one: Group) -> Group:
        """Rebuild one group and count its emitted headings.

        A wrapped heading opens the group's first section; each later
        authored heading flushes its preceding section through `flush`.
        Composed headings open inner sections without closing their outer
        scope. A composed region shares its grouped source's placement when
        its dispatched selections agree; otherwise identical copies share
        their first placement. `closure.Substitution.composed` supplies each
        copy's mapping. Preambles pass through without dispatch placement.
        """
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
                links = written_in(
                    part.path,
                    self.read[part.path],
                    tokens,
                    region,
                    self.declarations,
                    self.substitution.composed(part.path, part.selecting),
                )
                serves = tuple(link.served for link in links)
                copied = (*written, serves)
                if written in self.grouped and serves == tuple(
                    link.served
                    for link in written_in(
                        part.path,
                        self.read[part.path],
                        tokens,
                        region,
                        self.declarations,
                        self.substitution,
                    )
                ):
                    self.aliases.append((key, (part.path, part.lines[0], ())))
                elif self.first.setdefault(copied, key) != key:
                    self.aliases.append((key, self.first[copied]))
                else:
                    for link in links:
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
    """Rebuild groups through `Placing.group` and return its shared placements."""
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
