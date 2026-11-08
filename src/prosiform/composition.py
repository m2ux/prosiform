"""Composition: the sections composition directives place.

A composition directive is recognised as the closure module states. An
immediate directive naming a section of a document the bundle
compiles *composes* it. The section containing the directive is its
*scope*, at the heading the bundle emits for it. When the scope's own
content ends, each title its directives' targets carry takes a
*destination section* one level below the scope, in the order its
first directive is written, so directives in one scope naming sections
of one title share one destination and sibling scopes each carry their
own. Beneath it, each directive takes a *contribution*: a heading one
level further down naming the target's immediate parent, then the
target's body and subsections as the regions its source wrote, each
heading moved so the target's own level becomes the contribution
heading's. The directive's link points at its contribution heading.

A contribution is its source's content: its regions are rewritten
against the document that wrote them, so its links resolve from that
document's directory, its fragments against that document's headings
and its reference-style uses against that document's definitions,
whatever the writing document defines. Every directive contributes, a
repeated one and one naming a section another directive or an
ordinary link names included, each in the scope that writes it.

A directive is a reference. It resolves through the substitution in
force for the document writing it, so that document's `subst` decides
the section composed, and its link title selects the target's presets
by complete comma-separated names. Their `subst`
pairs redirect the links the contribution writes, since those are the
target document's own. A `group` pair places a document where an
ordinary reference bundles it, so it places no contribution.

A directive a contribution carries composes as one its source writes
anywhere: beneath the heading holding it there, which is the
contribution heading for one in the target's own body and a carried
subsection's heading for one in a subsection. Its destination sections
follow that heading's content, ahead of the subsections that follow
it. A source link a contribution carries stands in every copy of that
contribution, so a composition is identified by its *placing*: the
directives whose compositions placed it, outermost first, its own last.

A deferred directive keeps its place and contributes no content: it
takes its destination section and contribution heading as an immediate
one does, and the contribution carries one generated line naming the
target by its heading text, the path the later run compiles and the
link title carrying its requested presets. That run reads the target as an entry,
so its body is
validated there, its immediate directives compose and its deferred
ones keep their own lines.

A composition whose target section holds its own directive, or one
on the placing that reached it, would compose that target again
within itself without end, so it is refused, naming the closing
directive and the chain. A target reached twice along distinct
placings is no cycle: each composes once.

Each contribution is bundle content, so its bytes count toward the
output budget as it is composed, and a multiplying composition fails
at the first emission crossing the budget rather than once it is
whole. Without a destination map a link's published destination is
not yet known, so that pass counts only the headings composition
generates, which every pass emits alike; with one, every byte emitted
counts.

Composition runs on the built groups ahead of the dispatch pass, which
reads what a destination section carries as the scope's own content:
a scope's dispatch-set sub-sections follow its destination sections, and
its child sections follow both.

Titles are matched exactly as their headings show them: no case
folding, Unicode normalisation or trimming joins two titles, so one
destination section holds only targets whose visible text is the same
string. Destination sections take the order their first directive is
written and contributions the order theirs are, so the source alone
decides the order and two runs over it compose alike. Parents carrying
one title keep a contribution each, told apart by the renderer's
ordinal as any repeated heading is.

Each composition failure names the directive that requested it, where
it is written. A target with no heading above it names no parent, an
authored child heading of the scope whose text equals a destination
section's would give the scope two sections of one name, and a
composed heading past the sixth level is beyond what Markdown emits,
so each is refused. A directive in a heading emitted as text alone has
no section to compose beneath, which the bundle refuses as it refuses
a dispatch there.
"""

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, replace
from html import escape

from markdown_it.token import Token

from prosiform.bundle import (
    ATX,
    HEADING_OPEN,
    MAX_LEVEL,
    Group,
    ancestry,
    carried_headings,
    emitted_text,
    escaped,
    region,
    rewrite,
    shown_text,
    single_line,
    source_fragments,
)
from prosiform.closure import (
    DECLARING,
    INLINE_MARK,
    UNSUBSTITUTED,
    Declarations,
    Reference,
    Substitution,
    deferred,
    directive,
    rebased,
    resolvable,
)
from prosiform.dispatch import region_of
from prosiform.limits import OUTPUT_BYTES, Limits
from prosiform.provenance import (
    CONTRIBUTION_HEADING,
    DESTINATION_SECTION,
    Ancestor,
    Carried,
    Contributing,
    Emitted,
    Generated,
    Instruction,
    Located,
    Origin,
    Part,
    Placing,
    Preamble,
    Range,
    Served,
    link_at,
)
from prosiform.rewrite import Definition
from prosiform.source import (
    ENCODING,
    HREF,
    LINK_OPEN,
    Source,
    events,
    inlines,
    level,
    lines,
    opening_text,
    section,
)
from prosiform.tags import read as read_tags

Composed = dict[Placing, Generated]
"""Each contribution's heading, by the placing of the composition it heads."""


class Parentless(Exception):
    """A directive whose target has no heading above it to name a parent by."""

    def __init__(self, path: str, line: int | None, destination: str) -> None:
        super().__init__(
            f"the directive {destination!r} in {path!r} names a section no "
            f"heading stands above"
        )
        self.path = path
        self.line = line
        self.destination = destination


class Overflowing(Exception):
    """A directive whose composed heading would stand beyond the sixth level."""

    def __init__(
        self, path: str, line: int | None, destination: str, heading: str, depth: int
    ) -> None:
        super().__init__(
            f"the directive {destination!r} in {path!r} composes the heading "
            f"{heading!r} at level {depth}"
        )
        self.path = path
        self.line = line
        self.destination = destination
        self.heading = heading
        self.level = depth


class Colliding(Exception):
    """A directive whose destination section an authored child of its scope names.

    The authored heading is named by its source and the line of the file
    it stands on.
    """

    def __init__(
        self,
        path: str,
        line: int | None,
        destination: str,
        title: str,
        authored: str,
    ) -> None:
        super().__init__(
            f"the directive {destination!r} in {path!r} places the section "
            f"{title!r}, which an authored heading of its scope names"
        )
        self.path = path
        self.line = line
        self.destination = destination
        self.title = title
        self.authored = authored


class Cycling(Exception):
    """A composition whose target holds a directive on the chain that reached it.

    The chain holds each directive whose composition placed the next,
    the closing one last.
    """

    def __init__(self, chain: tuple["Directive", ...]) -> None:
        closing = chain[-1]
        super().__init__(
            f"the directive {closing.written!r} in {closing.at[0]!r} composes a "
            f"section holding a directive on the chain that placed it"
        )
        self.chain = chain


@dataclass(frozen=True)
class Directive:
    """One composing link: the section it names and where it is written.

    The title is the target heading's visible text, which decides the
    destination section the directive shares with others in its scope.
    A deferred directive's target is composed by the run its
    contribution names rather than by this one.
    """

    target: Reference
    written: str
    line: int | None
    at: Located
    title: str
    deferred: bool = False
    link_title: str | None = None

    def overflowing(self, heading: str, depth: int) -> Overflowing:
        """The refusal of a heading this directive would compose past H6."""
        return Overflowing(self.at[0], self.line, self.written, heading, depth)


class Composing:
    """The bundle's groups rebuilt with the sections their directives compose.

    Without a destination map the composed regions carry the bytes
    their source wrote, as an unmapped group's do; with one, their
    links are rewritten through it, against the source they were
    written in.
    """

    def __init__(
        self,
        parsed: Mapping[str, Sequence[Token]],
        read: Mapping[str, Source],
        defined: Mapping[str, Mapping[str, Definition]],
        limits: Limits,
        assigned: Mapping[tuple[str, str | None], str] | None = None,
        dispatching: Mapping[tuple[str, int], Mapping[Served, str]] | None = None,
        declarations: Declarations = DECLARING,
        substitution: Substitution = UNSUBSTITUTED,
        composing: Contributing | None = None,
    ) -> None:
        self.parsed = parsed
        self.read = read
        self.conversions = {path: source.conversion for path, source in read.items()}
        self.defined = defined
        self.limits = limits
        self.assigned = assigned
        self.dispatching = dispatching
        self.declarations = declarations
        self.substitution = substitution
        self.composing = {} if composing is None else composing
        self.counted = 0
        self.placed: Composed = {}
        self.emitted: list[str] = []
        self.parts: list[Part] = []
        self.headings: list[Emitted] = []
        self.pending: dict[str, list[Directive]] = {}
        self.opened: dict[int, Directive] = {}
        self.level: int | None = None

    def directives(self, path: str, token: Token) -> Iterator[Directive]:
        """Every composing link one region writes, in written order."""
        tokens = self.parsed[path]
        for inline in inlines(tokens, [token]):
            if inline.map is None:
                continue
            line = self.read[path].line(inline.map[0] + 1)
            position = 0
            for children, at, child in events(inline.children or []):
                if child.type != LINK_OPEN:
                    continue
                here = position
                position += 1
                if not directive(opening_text(children, at)):
                    continue
                written = str(child.attrGet(HREF) or "")
                raw_title = child.attrGet("title")
                link_title = None if raw_title is None else str(raw_title)
                found = resolvable(
                    path,
                    written,
                    self.declarations,
                    self.substitution,
                    tags=read_tags(link_title),
                )
                if found is None or found.fragment is None:
                    continue
                named = self.parsed[found.path]
                chosen = section(named, found.fragment)
                if not chosen:
                    continue
                shows = shown_text(
                    found.path,
                    named,
                    self.declarations,
                    self.substitution,
                    conversions=self.conversions,
                )
                yield Directive(
                    found,
                    written,
                    line,
                    link_at(path, inline, inline.map[0], here),
                    single_line(shows[id(chosen[0])]),
                    deferred(opening_text(children, at)),
                    link_title,
                )

    def emit(self, text: str, generated: bool = False) -> None:
        """Emit one part's text, holding the output budget against it.

        Every pass emits a generated heading alike, so it counts in each;
        any other text counts once its links carry their destinations.
        """
        self.emitted.append(text)
        if generated or self.assigned is not None:
            self.counted += len(text.encode(ENCODING))
            self.limits.hold(OUTPUT_BYTES, self.counted)

    def heading(self, one: Generated) -> None:
        """Emit one generated heading of a composition."""
        self.emit(f"{ATX * one.level} {escaped(one.text)}", generated=True)
        self.parts.append(one)
        self.headings.append(one)

    def activation(self, one: Directive) -> None:
        """Emit the one line a deferred directive's contribution carries.

        The line names the target by its visible heading text and by the
        path a later run compiles it from, as a deferred link's
        destination names it, so that run composes the body this one
        withholds. Every pass emits it alike.
        """
        suffix = ""
        if one.link_title is not None:
            title = (
                escape(one.link_title, quote=True)
                .replace("\\", "&#92;")
                .replace("\n", "&#10;")
                .replace("\r", "&#13;")
                .replace("\t", "&#9;")
            )
            suffix = f' "{title}"'
        text = (
            f"[{INLINE_MARK} {escaped(one.title)}]"
            f"({rebased(one.target, one.written)}{suffix})"
        )
        self.emit(text, generated=True)
        self.parts.append(
            Instruction(
                text,
                activates=((one.target.path, one.target.fragment), one.target.tags),
            )
        )

    def contribute(
        self, one: Directive, depth: int, chain: tuple[Directive, ...]
    ) -> None:
        """Emit one directive's contribution at the depth its heading takes.

        The chain holds the directives whose compositions placed this
        one, outermost first. The directives the contribution carries
        compose beneath the heading holding each, as the scope's do.
        """
        path = one.target.path
        tokens = self.parsed[path]
        chosen = section(tokens, one.target.fragment or "") or ()
        placing = (*chain, one)
        opening = chosen[0]
        parents = ancestry(tokens)[id(opening)]
        if not parents:
            raise Parentless(one.at[0], one.line, one.written)
        shows = shown_text(
            path,
            tokens,
            self.declarations,
            self.substitution,
            conversions=self.conversions,
        )
        contribution = Generated(
            single_line(shows[id(parents[-1])]), depth, CONTRIBUTION_HEADING
        )
        if depth > MAX_LEVEL:
            raise one.overflowing(contribution.text, depth)
        placed = tuple(each.at for each in placing)
        self.placed.setdefault(placed, contribution)
        self.heading(contribution)
        if one.deferred:
            self.activation(one)
            return
        body = list(chosen[1:])
        by = depth - level(opening)
        source = self.read[path]
        defined = self.defined[path]
        removed = {at for held in defined.values() for at in range(*held.lines)}
        physical = lines(source.text)
        written = (
            list(physical)
            if self.assigned is None
            else rewrite(
                physical,
                tokens,
                body,
                dict(self.assigned),
                path,
                defined,
                self.declarations,
                self.dispatching,
                source.first_line,
                self.substitution,
                self.composing.get(placed, {}),
            )
        )
        named = source_fragments(tokens)
        pending: dict[str, list[Directive]] = {}
        holding = depth
        for token in body:
            carried = carried_headings(tokens, token)
            for held in carried:
                if level(held) + by > MAX_LEVEL:
                    raise one.overflowing(shows[id(held)], level(held) + by)
            if token.type == HEADING_OPEN:
                self.flush(pending, holding, placing)
                pending = {}
                holding = level(token) + by
            self.headings.extend(
                Carried(
                    emitted_text(held, shows[id(held)], by),
                    level(held) + by,
                    (
                        Origin(
                            path,
                            None if held.map is None else held.map[0] + 1,
                            level(held),
                            named[id(held)],
                            by,
                        ),
                    ),
                    composed=True,
                )
                for held in carried
            )
            lower, upper = token.map or (0, 0)
            self.parts.append(
                Range(
                    path,
                    (lower, upper),
                    tuple(at for at in range(lower, upper) if at in removed),
                    placed,
                )
            )
            self.emit(region(written, tokens, token, by, removed))
            for found in self.directives(path, token):
                pending.setdefault(found.title, []).append(found)
        self.flush(pending, holding, placing)

    def cycle(self, one: Directive, chain: tuple[Directive, ...]) -> None:
        """Refuse a directive whose target holds it or a directive on its chain.

        A deferred directive composes nothing in this run, so it closes
        no cycle.
        """
        if one.deferred:
            return
        tokens = self.parsed[one.target.path]
        chosen = section(tokens, one.target.fragment or "") or ()
        start = (chosen[0].map or (0, 0))[0]
        end = max((token.map or (0, 0))[1] for token in chosen)
        placing = (*chain, one)
        if any(
            each.at[0] == one.target.path and start <= each.at[1] < end
            for each in placing
        ):
            raise Cycling(placing)

    def flush(
        self,
        pending: Mapping[str, Sequence[Directive]],
        holding: int | None,
        chain: tuple[Directive, ...],
    ) -> None:
        """Emit the destination sections one closed section composes.

        The holding level is the level of the heading the directives
        stand beneath, and the chain is the directives whose
        compositions placed that heading, none for an authored one.
        """
        if holding is None:
            return
        for each in pending.values():
            for one in each:
                self.cycle(one, chain)
        depth = holding + 1
        for title, found in pending.items():
            if depth > MAX_LEVEL:
                raise found[0].overflowing(title, depth)
            destination = Generated(title, depth, DESTINATION_SECTION)
            self.opened[id(destination)] = found[0]
            self.heading(destination)
            for one in found:
                self.contribute(one, depth + 1, chain)

    def close(self) -> None:
        """Emit the destination sections the authored section just closed composes."""
        self.flush(self.pending, self.level, ())
        self.pending = {}

    def collide(self) -> None:
        """Refuse a destination section an authored child of its scope names.

        A destination section and the scope's child sections are siblings,
        and the children follow it until a heading above their level
        closes the scope.
        """
        for at, one in enumerate(self.headings):
            first = self.opened.get(id(one))
            if first is None:
                continue
            for later in self.headings[at + 1 :]:
                if later.level < one.level:
                    break
                if (
                    later.level == one.level
                    and isinstance(later, Carried | Ancestor)
                    and later.text == one.text
                ):
                    origin = later.origins[0]
                    authored = (
                        origin.path
                        if origin.line is None
                        else f"{origin.path}:{self.read[origin.path].line(origin.line)}"
                    )
                    raise Colliding(
                        first.at[0], first.line, first.written, one.text, authored
                    )

    def group(self, one: Group) -> Group:
        """One group with the sections its directives compose."""
        offset = 1 if one.wrapped else 0
        self.emitted = []
        for text in one.parts[:offset]:
            self.emit(text)
        self.opened = {}
        self.parts = []
        self.headings = list(one.record.headings[:offset])
        self.level = one.record.headings[0].level if one.wrapped else None
        at = offset
        for part, text in zip(one.record.parts, one.parts[offset:], strict=True):
            if isinstance(part, Ancestor | Generated):
                self.close()
                self.level = part.level
                self.headings.append(one.record.headings[at])
                at += 1
            elif isinstance(part, Range):
                tokens = self.parsed[part.path]
                token = region_of(tokens, part)
                held = len(carried_headings(tokens, token))
                if token.type == HEADING_OPEN:
                    self.close()
                    self.level = one.record.headings[at].level
                self.headings.extend(one.record.headings[at : at + held])
                at += held
                if not part.composed and not isinstance(part, Preamble):
                    for found in self.directives(part.path, token):
                        self.pending.setdefault(found.title, []).append(found)
            self.emit(text)
            self.parts.append(part)
        self.close()
        self.collide()
        return Group(
            tuple(self.emitted),
            replace(one.record, headings=tuple(self.headings), parts=tuple(self.parts)),
            wrapped=one.wrapped,
            level=one.level,
        )


def compositions(
    groups: Sequence[Group],
    parsed: Mapping[str, Sequence[Token]],
    read: Mapping[str, Source],
    defined: Mapping[str, Mapping[str, Definition]],
    limits: Limits,
    assigned: Mapping[tuple[str, str | None], str] | None = None,
    dispatching: Mapping[tuple[str, int], Mapping[Served, str]] | None = None,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    composing: Contributing | None = None,
) -> tuple[list[Group], Composed]:
    """Every group with the sections its directives compose, and each contribution.

    The contributions are the headings each composing link points at,
    held by the composition's placing, so the destinations they take
    are read once every heading of the bundle is known. A destination
    map comes with the composing links' destinations, which a
    contribution's own directives are rewritten through.
    """
    composer = Composing(
        parsed,
        read,
        defined,
        limits,
        assigned,
        dispatching,
        declarations,
        substitution,
        composing,
    )
    return [composer.group(one) for one in groups], composer.placed


def contributions(
    placed: Composed, headed: Sequence[Group], assigned: Sequence[str]
) -> Contributing:
    """The destination each composing link takes: its contribution heading's.

    The links are held by the placing of the region writing them, so a
    region's links are read together, each by its own position.
    """
    position = {
        id(heading): at
        for at, heading in enumerate(
            heading for one in headed for heading in one.record.headings
        )
    }
    found: Contributing = {}
    for placing, heading in placed.items():
        found.setdefault(placing[:-1], {})[placing[-1]] = assigned[
            position[id(heading)]
        ]
    return found
