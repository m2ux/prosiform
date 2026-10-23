"""Candidate validation: the completed bundle held to the provenance that built it.

The candidate is reparsed under the same declared grammar in a policy
context of its own. That context accepts what the bundle generates —
filename headings, shifted headings and the structural ancestors a later
epic adds — and it does not pass the candidate back through frontmatter
stripping, dependency discovery or generated-input rejection. The
producer's candidate therefore passes here while the same document
supplied to a later invocation is correctly refused as generated input;
the two are separate policies over one grammar rather than one policy
disagreeing with itself.

What the reparse supplies is the published bytes read as a reader reads
them. What the provenance supplies is the claim those bytes are held to:
which source region each part of the bundle carries, and which source
heading each emitted heading answers to. Every check below compares one
against the other, so an agreement means the candidate says what its
construction recorded rather than that it is internally consistent.

The invariants checked here are block boundary safety, target
integrity, exactly-once coverage,
absence of new links, absence of surviving definitions, reference
preservation, outline preservation, depth safety, group isolation, entry
line integrity, one intended destination per rewritten link, and the two
sides of region accounting: a candidate holding fewer regions than the
provenance claims has omitted one, and a candidate holding more carries
content no source range accounts for.

Block boundary safety is the first of them, because an absorbed region
is also a missing one: a candidate whose unterminated code example
swallowed the group written after it holds fewer regions than the
provenance claims, and reporting that as an omission would name the
count rather than the boundary that lost it. The check reads the line
each emitted part opens on from the assembly, and requires the reparse
to open a region of its own there. A part the reparse places inside the
one above it is a boundary the run refuses, and it is refused rather
than repaired: no fence is closed and no code example is rewritten on
the author's behalf, because a document the tool silently completed is
no longer the document the author wrote.

One invariant the contract names is not checked here, and is absent
rather than weakened. **Destination stability** is a property of the
construction rather than of the candidate. A reference is rewritten to
the destination its target was given, read from the map `cli` builds
over every group from the identity each emitted heading answers to, and
neither the position a link sits in nor the region a run consolidated it
into is part of that identity. A check comparing a link's destination
before and after consolidation would therefore compare one lookup of a
target with another lookup of the same target, and a check that cannot
fail reports a guarantee nobody has.

An unsafe boundary raises `Unsafe`, which names the source regions
either side of it and the container that absorbed one into the other.
Every other failure raises `Invalid`, which names the invariant and
what disagreed. Nothing is published while a check fails.
"""

from collections.abc import Collection, Iterator, Mapping, Sequence
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any

from markdown_it.common.normalize_url import normalizeLink
from markdown_it.token import Token

from prosiform.bundle import (
    MAX_LEVEL,
    Group,
    absorbed,
    ancestry,
    blank,
    carried_headings,
    entry_slot,
    heading_text,
    openings,
)
from prosiform.closure import Reference, bundled, deferring, rebased
from prosiform.profile import REFERENCES, parse
from prosiform.provenance import (
    Ancestor,
    Emitted,
    Generated,
    Part,
    Range,
    Record,
)
from prosiform.source import (
    HEADING_OPEN,
    HREF,
    IMAGE,
    LINK_OPEN,
    SRC,
    Source,
    bare,
    events,
    fragments,
    headings,
    inlines,
    level,
    lines,
    opening_text,
    regions,
    shown,
    visible,
)

ANCHOR = "#"
TITLE = "title"
PARAGRAPH_OPEN = "paragraph_open"
LINK_CLOSE = "link_close"
CODE_BLOCKS = ("fence", "code_block")

LINK = "link"

UNSAFE_BUNDLE_BOUNDARY = "E_UNSAFE_BUNDLE_BOUNDARY"

CODES = (UNSAFE_BUNDLE_BOUNDARY,)

ENTRY_LINE = "the entry line"

CONTAINERS = {
    "fence": "code example",
    "code_block": "indented code example",
    "bullet_list_open": "list",
    "ordered_list_open": "list",
    "blockquote_open": "quote",
    "html_block": "HTML block",
    "paragraph_open": "paragraph",
    "table_open": "table",
}

TARGET_INTEGRITY = "target integrity"
EXACTLY_ONCE = "exactly-once coverage"
NO_NEW_LINKS = "no new links"
NO_DEFINITION_LEAKAGE = "no definition leakage"
REFERENCE_PRESERVATION = "reference preservation"
OUTLINE_PRESERVATION = "outline preservation"
DEPTH_SAFETY = "depth safety"
GROUP_ISOLATION = "group isolation"
ENTRY_LINE_INTEGRITY = "entry line integrity"
ONE_DESTINATION = "one intended destination"
NO_OMISSIONS = "no accidental omissions"
NO_EXPANSION = "no accidental expansion"
PRESERVATION = "preservation"


class Invalid(Exception):
    """A candidate disagreeing with the provenance its construction recorded."""

    def __init__(self, invariant: str, detail: str) -> None:
        super().__init__(f"{invariant}: {detail}")
        self.invariant = invariant
        self.detail = detail


class Unsafe(Exception):
    """A bundle boundary placing one emitted part inside a container of the part above.

    The two parts are named as the source regions they carry, because a
    boundary is a defect of the documents being bundled together rather
    than of a position in the output, and the container is named as the
    construct a reader of the bundle would find the later part inside.
    The path carried is the source whose region opens the container,
    which is the document an author closes the construct in, rather
    than the source of the content that landed inside it.
    """

    def __init__(
        self, carried: str, absorbed: str, container: str, path: str | None, at: int
    ) -> None:
        super().__init__(
            f"{absorbed} is placed inside the {container} that {carried} opens, "
            f"at line {at} of the bundle"
        )
        self.carried = carried
        self.absorbed = absorbed
        self.container = container
        self.path = path
        self.at = at
        self.code = UNSAFE_BUNDLE_BOUNDARY
        self.remedy = (
            f"end the {container} in the source before the content that follows "
            f"it, or select content that does not end inside one"
        )


class Use:
    """One link or image use, as the parts of it the bundle promises to carry.

    The destination is the one the parser resolved, so a reference-style
    use in a source and the inline use the bundle publishes for it arrive
    in the same shape and are compared as the same thing.
    """

    def __init__(self, kind: str, text: str, title: str, destination: str) -> None:
        self.kind = kind
        self.text = text
        self.title = title
        self.destination = destination

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Use) and self.parts() == other.parts()

    def __hash__(self) -> int:
        return hash(self.parts())

    def __repr__(self) -> str:
        return f"Use{self.parts()!r}"

    def parts(self) -> tuple[str, str, str, str]:
        """The use as the four things a comparison reads."""
        return (self.kind, self.text, self.title, self.destination)


def attribute(token: Token, name: str) -> str:
    """One attribute of a token, as the text it carries or nothing at all."""
    value = token.attrGet(name)
    return "" if value is None else str(value)


def label(children: Sequence[Token], at: int) -> str:
    """The visible text one link shows, read from the events between its ends."""
    closing = next(
        (
            after
            for after in range(at + 1, len(children))
            if children[after].type == LINK_CLOSE
        ),
        len(children),
    )
    return "".join(shown(child) for child in children[at + 1 : closing])


def alternative(image: Token) -> str:
    """The text one image's alternative content shows, its own uses aside.

    The alternative content is a run of inline events, and a use
    written there is compared as the use it is, so the text left to
    compare here is what surrounds it. A link's visible text is
    therefore read out of this run and read back on that link's own
    comparison, which is where a mark the rewrite drops is accounted
    for.
    """
    children = image.children or []
    carried = []
    inside = False
    for child in children:
        if child.type == LINK_OPEN:
            inside = True
        elif child.type == LINK_CLOSE:
            inside = False
        elif not inside:
            carried.append(shown(child))
    return "".join(carried)


def uses(inline: Token) -> Iterator[tuple[Sequence[Token], int, Use]]:
    """Every link and image use one inline token carries, with its position.

    Each use arrives with the run that carries it and its position in
    that run, which is where a mark is read from, so a use written
    inside an image's alternative content is compared on the run it
    was written in. Both sides of every comparison read the run the
    same way.
    """
    for children, at, child in events(inline.children or []):
        if child.type == LINK_OPEN:
            yield (
                children,
                at,
                Use(
                    LINK,
                    label(children, at),
                    attribute(child, TITLE),
                    attribute(child, HREF),
                ),
            )
        else:
            yield (
                children,
                at,
                Use(
                    IMAGE,
                    alternative(child),
                    attribute(child, TITLE),
                    attribute(child, SRC),
                ),
            )


def intended(
    path: str,
    one: Use,
    at: int,
    children: Sequence[Token],
    targets: Mapping[tuple[str, str | None], str],
    root: str = "",
) -> Use:
    """The use the bundle must publish for one use its source wrote.

    A link the bundle compiled carries the destination it assigned the
    target that link resolved to, and shows the text its author wrote.
    Every other use is published as its author wrote it, a
    reference-style use at the inline form the definition it names
    gives it.

    A deferred link under the allowed source root carries its target's
    path from that root, so what it shows is its author's text and
    where it points is the destination the bundle rebased. A deferral
    resolving nowhere the bundle is responsible for is published as
    authored like any other mention.

    Whether the bundle compiled the link is read from the text the
    link's content opens with, as discovery and emission read it, so a
    deferral the parser places inside a formatting event is the same
    deferral to all three.

    The run passed in is the one that carries the use, which is an
    image's alternative content where the use was written there, so
    the opening is read from the event the author wrote it on.
    """
    if one.kind != LINK:
        return one
    opening = opening_text(children, at)
    found = bundled(path, one.destination, opening, root)
    if found is None:
        deferred = deferring(path, one.destination, opening, root)
        if deferred is None:
            return one
        return Use(
            one.kind,
            one.text,
            one.title,
            normalizeLink(rebased(deferred, one.destination)),
        )
    assigned = targets.get((found.path, found.fragment))
    if assigned is None:
        raise Invalid(
            TARGET_INTEGRITY,
            f"the reference {one.destination!r} in {path!r} was assigned no "
            f"destination",
        )
    return Use(
        one.kind,
        one.text,
        one.title,
        normalizeLink(f"{ANCHOR}{assigned}"),
    )


def carrying(tokens: Sequence[Token], span: Token) -> set[int]:
    """Each line one region's use-bearing inline tokens occupy.

    A line the bundle edits is a heading's line or a line of an inline
    token carrying a link or an image: reference-use conversion and
    destination rewriting reach nowhere else. Every other line of a
    selected region is bytes the bundle carries as its source wrote
    them, which is what the preservation comparison holds it to.
    """
    held: set[int] = set()
    for inline in inlines(tokens, [span]):
        if inline.map is not None and any(True for _ in uses(inline)):
            held.update(range(*inline.map))
    return held


def headed(tokens: Sequence[Token], span: Token) -> set[int]:
    """Each line the headings one region carries occupy."""
    return {
        at
        for opening in carried_headings(tokens, span)
        if opening.map is not None
        for at in range(*opening.map)
    }


def body(
    physical: Sequence[str],
    tokens: Sequence[Token],
    span: Token,
    removed: Collection[int] = (),
) -> list[str]:
    """One region's untouched non-heading lines, in order and without blanks.

    A blank line is the bundle's own wherever it joins what it emits —
    above a region, where a removed definition stood, and at a region's
    end — so the comparison runs over the lines that carry content, and
    a line carrying nothing but the markers its container opens it with
    is one of those blanks. The bytes of each line compared are the
    bytes its source wrote, trailing spaces and indentation included.
    """
    start, end = span.map or (0, 0)
    skipped = headed(tokens, span) | carrying(tokens, span) | set(removed)
    return [
        bare(physical[at])
        for at in range(start, end)
        if at not in skipped and not blank(physical[at])
    ]


def code(tokens: Sequence[Token], span: Token) -> list[tuple[str, str, str]]:
    """Each code example one region holds, as the parser read it.

    A code block's content carries the blank lines inside it, which the
    line comparison passes over, so the example is compared whole.
    """
    start, end = span.map or (0, 0)
    return [
        (token.type, token.info, token.content)
        for token in tokens
        if token.type in CODE_BLOCKS
        and token.map is not None
        and start <= token.map[0] < end
    ]


def prose(tokens: Sequence[Token], span: Token) -> list[Token]:
    """Each inline token one region carries outside a heading, in source order.

    A heading's inline content is compared where the outline is, because
    a converted Setext heading carries on one line what its source wrote
    on several and the line break reads as the space it already read as.
    """
    occupied = headed(tokens, span)
    return [
        inline
        for inline in inlines(tokens, [span])
        if inline.map is not None and inline.map[0] not in occupied
    ]


def parts(groups: Sequence[Group]) -> list[tuple[str, str]]:
    """What each emitted part of the bundle carries, in bundle order.

    A group writes its own heading and then one part for each part the
    provenance records, so a part after the first is named by that
    record: a selected range names the document and the lines it was
    taken from, a structural ancestor names the heading it emits, and a
    generated heading names what the arrangement produced it as. A
    boundary then names two pieces of source rather than two offsets
    into the output. A part the provenance records nothing for is named
    by its position, because the count is the structural pairing's to
    report and a boundary still has to say which part it concerns.
    """
    named: list[tuple[str, str]] = []
    for one in groups:
        path = one.record.path
        offset = 1 if one.wrapped else 0
        if one.wrapped:
            named.append((f"the heading for {path!r}", path))
        for at in range(offset, len(one.parts)):
            if at - offset >= len(one.record.parts):
                named.append((f"the region at position {at} of {path!r}", path))
                continue
            part = one.record.parts[at - offset]
            if isinstance(part, Range):
                named.append(
                    (
                        f"the region at lines {part.lines} of {part.path!r}",
                        part.path,
                    )
                )
            elif isinstance(part, Ancestor):
                held = part.origins[0].path
                named.append(
                    (f"the structural ancestor {part.text!r} of {held!r}", held)
                )
            else:
                named.append((f"the {part.kind} {part.text!r} of {path!r}", path))
    return named


def container(spans: Sequence[Token], at: int) -> Token | None:
    """The document-level block of the candidate that holds one line below its own.

    A region opening on the line is no container of it, so the search
    is for a block the line falls strictly inside: that block is what a
    reader of the bundle finds the content at that line within.
    """
    return next(
        (
            token
            for token in spans
            if token.map is not None and token.map[0] < at < token.map[1]
        ),
        None,
    )


def boundaries(
    physical: Sequence[str], spans: Sequence[Token], groups: Sequence[Group]
) -> None:
    """Hold each emitted part to opening a region of the candidate's own.

    The assembly writes one blank line between parts, and a blank line
    separates most blocks. It does not end an unterminated code
    example, and it does not separate two lists that share a marker or
    a list from an indented block below it, so a part can land inside
    the part above it without producing invalid Markdown. The reparse
    is what reveals it: a part whose opening line begins no
    document-level region of the candidate was absorbed by the part
    that holds it.

    A part the candidate has no line for at all is an omission rather
    than a boundary, and the structural pairing names it as one.
    """
    named = parts(groups)
    started = {token.map[0] for token in spans if token.map is not None}
    slot = entry_slot(groups)
    span = spans[slot] if spans else None
    entry_lines = (
        span.map[1] - span.map[0] if span is not None and span.map is not None else 1
    )
    for at, (opens, (what, path)) in enumerate(
        zip(openings(groups, entry_lines), named, strict=True)
    ):
        if opens in started or opens >= len(physical):
            continue
        holding = container(spans, opens)
        carried, opening = named[at - 1] if at else (ENTRY_LINE, path)
        kind = (
            "container"
            if holding is None
            else CONTAINERS.get(holding.type, holding.type)
        )
        raise Unsafe(carried, what, kind, opening, opens + 1)


def structure(
    spans: Sequence[Token], groups: Sequence[Group]
) -> list[tuple[Record, Part, Token]]:
    """Pair each region the candidate holds with the provenance that claims it.

    The bundle is its entry line, then for each group the filename
    heading and one region for each part the group records: a selected
    source range, or a structural ancestor. A group the parent's title
    opens records that title among its parts and has no filename heading
    ahead of them. A candidate holding fewer
    regions than the provenance claims has dropped one; a candidate
    holding more carries content no part accounts for. The filename
    wrapper is paired separately from the parts, so it cannot stand in
    for a missing selected region, and an ancestor is paired as the
    ancestor it is, so a heading-only part cannot stand in for a
    selected one either.
    """
    expected = 1 + sum(
        (1 if one.wrapped else 0) + len(one.record.parts) for one in groups
    )
    if len(spans) != expected:
        short = len(spans) < expected
        raise Invalid(
            NO_OMISSIONS if short else NO_EXPANSION,
            f"the candidate holds {len(spans)} region(s) against the {expected} "
            f"the provenance accounts for",
        )
    slot = entry_slot(groups)
    if slot >= len(spans) or spans[slot].type != PARAGRAPH_OPEN:
        found = spans[slot].type if slot < len(spans) else "nothing"
        raise Invalid(
            ENTRY_LINE_INTEGRITY,
            f"the entry paragraph is a {found!r} rather than a paragraph",
        )
    paired: list[tuple[Record, Part, Token]] = []
    at = 0 if any(one.entry_at is not None for one in groups) else 1
    for one in groups:
        if one.wrapped:
            opening = spans[at]
            if opening.type != HEADING_OPEN or level(opening) != 1:
                raise Invalid(
                    GROUP_ISOLATION,
                    f"the group for {one.record.path!r} opens on a {opening.type!r} "
                    f"rather than on its own heading",
                )
            at += 1
        for index, part in enumerate(one.record.parts):
            if one.entry_at is not None and index == one.entry_at:
                at += 1
            span = spans[at]
            if isinstance(part, Ancestor | Generated) and (
                span.type != HEADING_OPEN or level(span) != part.level
            ):
                raise Invalid(
                    NO_EXPANSION,
                    f"the {part.kind} {part.text!r} of {one.record.path!r} "
                    f"is emitted as a {span.type!r} rather than as a heading at "
                    f"level {part.level}",
                )
            paired.append((one.record, part, span))
            at += 1
        if one.entry_at is not None and one.entry_at == len(one.record.parts):
            at += 1
    return paired


def above(tokens: Sequence[Token]) -> dict[int, tuple[int, ...]]:
    """The source line of each eligible ancestor above each region, by that region.

    A region is keyed by the source line it opens on, and its chain is
    the lines of the headings open above it, outermost first. The chain
    is the source document's own outline, which is what a reconstructed
    one is compared against.
    """
    chains = ancestry(tokens)
    return {
        token.map[0] + 1: tuple(
            one.map[0] + 1 for one in chains[id(token)] if one.map is not None
        )
        for token in regions(tokens)
        if token.map is not None
    }


def absorbing(
    record: Record, path: str, tokens: Sequence[Token], display: str | None = None
) -> set[int]:
    """The source line of the heading the group names in one source's place.

    A file group's heading names the document's title, and a merged
    group's member subsection names its member's, whether the group
    emitted that title's section or not: a section beneath it is placed
    by that heading and the title is no structural ancestor. The line
    is what the outline check reads it as emitted at.
    """
    named = (
        heading_text(path if display is None else display)
        if record.merged is None
        else PurePosixPath(path).stem
    )
    found = absorbed(tokens, named)
    if found is None or found.map is None:
        return set()
    return {found.map[0] + 1}


def sourced(one: Part) -> str | None:
    """The source one emitted part carries content or structure from."""
    if isinstance(one, Range):
        return one.path
    if isinstance(one, Ancestor):
        return one.origins[0].path
    return None


def placement(
    record: Record,
    parsed: Mapping[str, Sequence[Token]],
    read: Mapping[str, Source] | None = None,
) -> None:
    """Hold one group's parts to the outline their source gave them.

    Each part the group emits is placed by the chain of eligible
    ancestor headings the source wrote above it, and every heading of
    that chain is emitted before it: as the heading that absorbed the
    source's title, as a selected region of its own, or as a structural
    ancestor. A chain member the group emits nowhere is an outline the
    candidate reconstructs differently from the one its author wrote.

    A merged group arranges its members by their conversion settings rather
    than by any one source's order, and a heading several documents
    contribute one text to is emitted once for all of them, so the
    chain is read against every source line the group's headings
    answer to rather than against the parts emitted before each one.
    A file group emits its parts in its source's own order, so the
    chain there is held to what stands above the part as well.

    The converse is held here as well. A structural ancestor is the
    only unselected source-derived content a group emits, so each of
    them places a part that follows it; one placing nothing is content
    the group emitted for no outline.
    """
    answered: dict[str, set[int | None]] = {}
    for each in record.placed():
        for origin in each.origins:
            answered.setdefault(origin.path, set()).add(origin.line)
    needed: dict[str, set[int]] = {}
    for path in record.paths():
        tokens = parsed[path]
        chains = above(tokens)
        emitted_at: set[int | None] = set(
            absorbing(
                record,
                path,
                tokens,
                (read[path].display or path) if read is not None else None,
            )
        )
        if record.merged is not None:
            emitted_at |= answered.get(path, set())
        for one in record.parts:
            if sourced(one) != path:
                continue
            at = (
                one.lines[0] + 1
                if isinstance(one, Range)
                else one.origins[0].line
                if isinstance(one, Ancestor)
                else None
            )
            chain = chains.get(at or 0, ())
            needed.setdefault(path, set()).update(chain)
            for line in chain:
                if line not in emitted_at:
                    raise Invalid(
                        OUTLINE_PRESERVATION,
                        f"the part at line {at} of {path!r} is emitted below "
                        f"none of the heading its source wrote at line {line}",
                    )
            emitted_at.add(at)
    for one in record.ancestors():
        for origin in one.origins:
            if origin.line not in needed.get(origin.path, set()):
                raise Invalid(
                    NO_EXPANSION,
                    f"the structural ancestor {one.text!r} of {origin.path!r} "
                    f"places no part the group emits",
                )


def structural(
    record: Record, one: Ancestor, span: Token, tokens: Sequence[Token]
) -> None:
    """Hold one structural ancestor's emitted part to carrying nothing live.

    The part is one region of the candidate, so a body, a sibling or a
    descendant emitted with it would be a region of its own and the
    structural pairing reports it, as it reports a part that is no
    heading. What is left to read is the title: it carries no live link
    and no live image, because the group emitted it as the literal text
    its author typed.
    """
    found = [use for inline in inlines(tokens, [span]) for _, _at, use in uses(inline)]
    if found:
        raise Invalid(
            NO_NEW_LINKS,
            f"the structural ancestor {one.text!r} of {one.origins[0].path!r} "
            f"publishes the use(s) {found!r}",
        )


def coverage(groups: Sequence[Group]) -> None:
    """Hold each selected source region to being carried once and only once.

    A region is named by the lines of its source's content it occupies,
    which two regions carrying the same prose do not share, so repeated
    identical prose in different source regions is not duplication and
    counting occurrences of a string decides nothing here.

    The ranges are read by source rather than by group, because a
    declared group arranges one document's regions among another's and
    two regions of one source overlap wherever they are emitted.
    """
    carried: dict[str, list[tuple[int, int]]] = {}
    for one in groups:
        for each in one.record.ranges:
            carried.setdefault(each.path, []).append(each.lines)
    for path, held in carried.items():
        last = 0
        for span in sorted(held):
            if held.count(span) > 1:
                raise Invalid(
                    EXACTLY_ONCE,
                    f"the region at lines {span} of {path!r} is carried more than once",
                )
            if span[0] < last:
                raise Invalid(
                    EXACTLY_ONCE,
                    f"the region at lines {span} of {path!r} overlaps the "
                    f"region before it",
                )
            last = span[1]


def emitted(groups: Sequence[Group]) -> list[tuple[Record, Emitted]]:
    """Every heading the bundle emits, in bundle order, with the group's record."""
    return [(one.record, each) for one in groups for each in one.record.headings]


def outline(tokens: Sequence[Token], groups: Sequence[Group]) -> None:
    """Hold the candidate's headings to the provenance of each one.

    A carried heading sits at the level its author wrote plus its
    group's shift, and the carried headings of one group follow their
    source's own order, so the chain above each of them is the chain
    its source gave it. A heading the shift would place beyond the
    sixth level is an overflow the group refuses, and the record is
    held to that here as well, so a group that stopped refusing one is
    caught by the provenance rather than by the parse that would read
    the result as text.

    What this reads is the candidate against the record. The chain a
    structural ancestor supplies is read from the source outline
    instead, by `placement`, because the record alone cannot say which
    ancestors a source gave a heading.
    """
    found = list(headings(tokens))
    expected = emitted(groups)
    if len(found) != len(expected):
        raise Invalid(
            ONE_DESTINATION,
            f"the candidate carries {len(found)} heading(s) against the "
            f"{len(expected)} the provenance records",
        )
    for (opening, inline), (_, one) in zip(found, expected, strict=True):
        if visible(inline) != one.text:
            raise Invalid(
                OUTLINE_PRESERVATION,
                f"the candidate shows {visible(inline)!r} where the provenance "
                f"records {one.text!r}",
            )
        if level(opening) != one.level:
            raise Invalid(
                OUTLINE_PRESERVATION,
                f"the heading {one.text!r} is emitted at level {level(opening)} "
                f"against the level {one.level} the provenance records",
            )


def levels(record: Record) -> None:
    """Hold one group's placed headings to their source levels and source order.

    A structural ancestor is placed by the level its author wrote under
    the shift its arrangement gives it, as a carried heading is, so both
    are held here: an ancestor emitted at another level would
    reconstruct an outline its source never wrote.

    A file group emits its headings in its source's order, so that
    order is held here too. A merged group's order is the grouping
    rules', which place one document's name beside another's, and the
    outline each part keeps is held by `placement` instead.

    The record is held to the levels and the order its sources wrote
    before the candidate is read, because a level beyond the sixth is
    no heading to a parser: a candidate the record claims an H7 of
    carries a paragraph there, and reading the candidate first would
    report the missing heading rather than the depth that lost it.
    """
    at = 0
    for one in record.placed():
        for origin in one.origins:
            if one.level != origin.level + origin.shift:
                raise Invalid(
                    OUTLINE_PRESERVATION,
                    f"the heading {one.text!r} of {origin.path!r} is emitted at "
                    f"level {one.level} where its source level {origin.level} "
                    f"under the shift of {origin.shift} it is arranged by places "
                    f"it at {origin.level + origin.shift}",
                )
        if one.level > MAX_LEVEL:
            raise Invalid(
                DEPTH_SAFETY,
                f"the heading {one.text!r} of {record.path!r} is emitted at level "
                f"{one.level}, which is beyond H{MAX_LEVEL}",
            )
        if one.level == 1 and any(
            isinstance(heading, Generated) and heading.level == 1
            for heading in record.headings
        ):
            raise Invalid(
                GROUP_ISOLATION,
                f"the heading {one.text!r} of {record.path!r} is emitted at the "
                f"level its group's own heading holds",
            )
        if record.merged is not None:
            continue
        line = one.origins[0].line
        if line is not None and line < at:
            raise Invalid(
                OUTLINE_PRESERVATION,
                f"the heading {one.text!r} of {record.path!r} is emitted before a "
                f"heading its source wrote above it",
            )
        at = at if line is None else line


def named(
    tokens: Sequence[Token], groups: Sequence[Group], assigned: Sequence[str]
) -> dict[str, tuple[Record, Emitted]]:
    """The heading each destination reaches, as the renderer reading the bundle does.

    The fragment the declared renderer generates for each heading of the
    candidate is derived from the candidate itself, so a destination the
    map assigned reaches the heading a reader following it reaches, or
    the bundle is not published.
    """
    generated = fragments([visible(inline) for _, inline in headings(tokens)])
    if generated != list(assigned):
        raise Invalid(
            ONE_DESTINATION,
            f"the candidate generates {generated} against the {list(assigned)} "
            f"the destination map names",
        )
    return dict(zip(assigned, emitted(groups), strict=True))


def integrity(
    reached: Mapping[str, tuple[Record, Emitted]],
    targets: Mapping[tuple[str, str | None], str],
) -> None:
    """Hold each assigned destination to the source identity it was assigned for.

    A destination is a slug, and two unrelated headings can produce one,
    so agreement between a link and a heading's text is not target
    integrity. What is checked is the provenance of the heading the
    destination reaches: each emitted heading records the targets it is
    where they resolve, and a destination reaching a heading that
    records another target was assigned to something else.
    """
    for named_target, destination in targets.items():
        found = reached.get(destination)
        if found is None:
            raise Invalid(
                TARGET_INTEGRITY,
                f"the destination {destination!r} assigned to {named_target[0]!r} "
                f"reaches no heading of the candidate",
            )
        record, one = found
        if named_target not in one.answers:
            raise Invalid(
                TARGET_INTEGRITY,
                f"the destination {destination!r} assigned to the target "
                f"{named_target!r} reaches {one.text!r} of {record.path!r}",
            )


def entry(
    spans: Sequence[Token],
    tokens: Sequence[Token],
    referrer: Reference | None,
    requested: Collection[Reference],
    targets: Mapping[tuple[str, str | None], str],
    groups: Sequence[Group],
) -> None:
    """Hold the entry line to naming every entry reference and no other.

    Each entry reference is resolved to the destination its target was
    assigned, and the links the published entry line carries are read
    back from the candidate. The two sets are the same set, or the line
    names something the caller did not ask for, or leaves out something
    the caller did.
    """
    expected = set()
    for one in requested:
        path = one.path or (referrer.path if referrer is not None else "")
        assigned = targets.get((path, one.fragment))
        if assigned is None:
            raise Invalid(
                ENTRY_LINE_INTEGRITY,
                f"the entry reference {one.original!r} names a target no "
                f"destination was assigned to",
            )
        expected.add(normalizeLink(f"{ANCHOR}{assigned}"))
    carried = {
        use.destination
        for inline in inlines(tokens, [spans[entry_slot(groups)]])
        for _, _at, use in uses(inline)
    }
    if carried != expected:
        raise Invalid(
            ENTRY_LINE_INTEGRITY,
            f"the entry line links {sorted(carried)} against the "
            f"{sorted(expected)} the entry references were assigned",
        )


def leakage(environment: Mapping[str, Any]) -> None:
    """Hold the candidate to carrying no surviving link-reference definition.

    A definition node that survived emission would resolve a label the
    bundle carries as literal text, so the candidate's own definition
    environment is empty. A literal example of a definition is inside a
    code block and declares nothing, which is why it is unchanged.
    """
    declared = environment.get(REFERENCES, {})
    if declared:
        raise Invalid(
            NO_DEFINITION_LEAKAGE,
            f"the candidate declares the link-reference definition(s) "
            f"{sorted(declared)}",
        )


@dataclass(frozen=True)
class Side:
    """One side of a region comparison: its tokens, its lines and the region."""

    tokens: Sequence[Token]
    physical: Sequence[str]
    span: Token


def located(tokens: Sequence[Token], at: tuple[int, int]) -> Token:
    """The region of one source occupying the lines a provenance range names."""
    found = next(
        (token for token in regions(tokens) if token.map == list(at)),
        None,
    )
    if found is None:
        raise Invalid(
            NO_OMISSIONS,
            f"no region of the source occupies the lines {at} the provenance names",
        )
    return found


def references(
    path: str,
    source: Side,
    published: Side,
    targets: Mapping[tuple[str, str | None], str],
    root: str = "",
) -> None:
    """Hold one region's link and image uses to the uses its source wrote.

    A use count that grew is text the author wrote as literal brackets
    read as a reference, and a use that differs in what it shows, in
    its title or in where it points is a reference the bundle did not
    preserve.
    """
    expected = [
        intended(path, one, at, children, targets, root)
        for inline in inlines(source.tokens, [source.span])
        for children, at, one in uses(inline)
    ]
    found = [
        one
        for inline in inlines(published.tokens, [published.span])
        for _, _at, one in uses(inline)
    ]
    if len(found) != len(expected):
        raise Invalid(
            NO_NEW_LINKS,
            f"the region at lines {source.span.map} of {path!r} carries "
            f"{len(expected)} use(s) and the candidate publishes {len(found)}",
        )
    for one, each in zip(expected, found, strict=True):
        if one != each:
            raise Invalid(
                REFERENCE_PRESERVATION,
                f"the region at lines {source.span.map} of {path!r} wrote {one!r} "
                f"and the candidate publishes {each!r}",
            )


def preserved(
    path: str, removed: Collection[int], source: Side, published: Side
) -> None:
    """Hold one region's untouched bytes and code examples to its source.

    The lines the bundle does not edit are compared as the bytes they
    are, the code examples as the parser read them, and the text each
    inline token shows as a reader reads it, the mark a rewrite drops
    taken off the source side where the link carrying it is one the
    bundle compiled. Together they are the content of the region:
    nothing in it is reformatted or repaired.
    """
    wrote = body(source.physical, source.tokens, source.span, removed)
    carries = body(published.physical, published.tokens, published.span)
    if wrote != carries:
        raise Invalid(
            PRESERVATION,
            f"the region at lines {source.span.map} of {path!r} wrote {wrote!r} "
            f"and the candidate carries {carries!r}",
        )
    examples = code(source.tokens, source.span)
    published_examples = code(published.tokens, published.span)
    if examples != published_examples:
        raise Invalid(
            PRESERVATION,
            f"the region at lines {source.span.map} of {path!r} wrote the code "
            f"example(s) {examples!r} and the candidate carries "
            f"{published_examples!r}",
        )
    written = prose(source.tokens, source.span)
    shows = prose(published.tokens, published.span)
    if len(written) != len(shows):
        raise Invalid(
            PRESERVATION,
            f"the region at lines {source.span.map} of {path!r} wrote "
            f"{len(written)} block(s) of inline content and the candidate carries "
            f"{len(shows)}",
        )
    for one, each in zip(written, shows, strict=True):
        if visible(one) != visible(each):
            raise Invalid(
                PRESERVATION,
                f"the region at lines {source.span.map} of {path!r} shows "
                f"{visible(one)!r} and the candidate shows "
                f"{visible(each)!r}",
            )


def validate(
    bundled: str,
    groups: Sequence[Group],
    assigned: Sequence[str],
    targets: Mapping[tuple[str, str | None], str],
    referrer: Reference | None,
    requested: Collection[Reference],
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
    budget: int,
) -> None:
    """Hold the completed candidate to the provenance its construction recorded.

    The record is held to itself first — each selected region carried
    once, each heading at the level and in the order its source wrote —
    and the candidate is then reparsed in candidate mode and held to
    the record, the boundaries between its parts first. A failure
    raises before anything is published, so a candidate that disagrees
    with its source provenance publishes nothing.
    """
    coverage(groups)
    for one in groups:
        levels(one.record)
        placement(one.record, parsed, read)
    environment: dict[str, Any] = {}
    tokens = parse(bundled, budget, environment)
    physical = lines(bundled)
    spans = list(regions(tokens))
    boundaries(physical, spans, groups)
    paired = structure(spans, groups)
    leakage(environment)
    outline(tokens, groups)
    integrity(named(tokens, groups, assigned), targets)
    entry(spans, tokens, referrer, requested, targets, groups)
    for record, part, span in paired:
        if isinstance(part, Ancestor):
            structural(record, part, span, tokens)
            continue
        if isinstance(part, Generated):
            continue
        carried = part
        source = Side(
            parsed[carried.path],
            lines(read[carried.path].text),
            located(parsed[carried.path], carried.lines),
        )
        published = Side(tokens, physical, span)
        references(carried.path, source, published, targets, read[carried.path].root)
        preserved(carried.path, carried.removed, source, published)
