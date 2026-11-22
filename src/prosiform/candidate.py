"""Validate a completed bundle against its source and construction records.

`validate` checks provenance and reparses the candidate through
`profile.parse`. A failed boundary check raises `Unsafe`; other invariant
failures raise `Invalid`. The module publishes no output.
"""

import re
from collections.abc import Callable, Collection, Iterator, Mapping, Sequence
from dataclasses import dataclass, field, replace
from pathlib import PurePosixPath
from typing import Any
from urllib.parse import quote

from markdown_it.common.normalize_url import normalizeLink
from markdown_it.token import Token

from prosiform.bundle import (
    MAX_LEVEL,
    Group,
    absorbed,
    ancestry,
    blank,
    carried_headings,
    diagram_labels,
    document_title,
    emitted_visible,
    names_model,
    openings,
)
from prosiform.closure import (
    DECLARING,
    UNSUBSTITUTED,
    WORKING_FOLDER,
    BundleFolder,
    Declarations,
    Reference,
    Substitution,
    alternatives_of,
    briefing,
    bundled,
    carried_names,
    deferred_title,
    dispatched,
    filed,
    parallel,
    published_text,
    rebased,
    resolve,
    unmarked,
    withholding_target,
)
from prosiform.metadata import Conversion
from prosiform.profile import HTML_INLINE, REFERENCES, command_block, parse
from prosiform.provenance import (
    BRIEF_SECTION,
    CONTRIBUTION_HEADING,
    FILENAME_WRAPPER,
    GROUP_HEADING,
    PARALLEL_SECTION,
    PICK_SECTION,
    Ancestor,
    Carried,
    Contributing,
    Dispatching,
    Emitted,
    Generated,
    Instruction,
    Located,
    Part,
    Range,
    Record,
    Served,
    click_at,
    link_at,
)
from prosiform.provenance import (
    Placing as Chain,
)
from prosiform.source import (
    ANCHOR,
    FENCE,
    HEADING_OPEN,
    HREF,
    IMAGE,
    INLINE,
    LINE_FEED,
    LINK_OPEN,
    SRC,
    Source,
    bare,
    clicks,
    diagram_type,
    element_texts,
    events,
    fragments,
    headings,
    inlines,
    level,
    lines,
    opening_text,
    regions,
    runs,
    shown,
    visible,
    within,
)
from prosiform.tags import picks
from prosiform.tags import read as read_tags

TITLE = "title"
LINK_CLOSE = "link_close"
ESCAPED_BREAK = "\\\n"
CODE_BLOCKS = ("fence", "code_block")

LINK = "link"
CLICK = "click"
TOOLTIP = re.compile(r'"\s+"([^"]*)"')
"""The tooltip suffix span following a `source.Click` destination."""

UNSAFE_BUNDLE_BOUNDARY = "E_UNSAFE_BUNDLE_BOUNDARY"

CODES = (UNSAFE_BUNDLE_BOUNDARY,)

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

PARAGRAPH_OPEN = "paragraph_open"
BULLET_LIST_OPEN = "bullet_list_open"

TARGET_INTEGRITY = "target integrity"
EXACTLY_ONCE = "exactly-once coverage"
NO_NEW_LINKS = "no new links"
NO_DEFINITION_LEAKAGE = "no definition leakage"
REFERENCE_PRESERVATION = "reference preservation"
OUTLINE_PRESERVATION = "outline preservation"
DEPTH_SAFETY = "depth safety"
GROUP_ISOLATION = "group isolation"
ONE_DESTINATION = "one intended destination"
ONE_MEMBER = "one destination answers one member"
NO_OMISSIONS = "no accidental omissions"
NO_EXPANSION = "no accidental expansion"
PRESERVATION = "preservation"

OPENINGS = (FILENAME_WRAPPER, GROUP_HEADING)


class Invalid(Exception):
    """A candidate disagreeing with the provenance its construction recorded."""

    def __init__(self, invariant: str, detail: str) -> None:
        super().__init__(f"{invariant}: {detail}")
        self.invariant = invariant
        self.detail = detail


class Unsafe(Exception):
    """An unsafe emitted boundary, with the source path and adjacent parts.

    `container` names the construct absorbing the later part. `path` identifies
    the source whose earlier part opens it. `carried` and `absorbed` name the
    parts, and `at` locates the boundary in the candidate.
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
    """The comparable fields of a link, image or diagram use.

    `kind` classifies the use, `text` holds its opening text, `title` holds its
    title, and `destination` holds its normalized destination. Diagram field
    interpretation follows `source.Click`.
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


def read(child: Token, compacted: bool) -> str:
    """The part of one inline event a reader reads, a compacted tag read as text."""
    return child.content if compacted and child.type == HTML_INLINE else shown(child)


def label(children: Sequence[Token], at: int, compacted: bool = False) -> str:
    """The visible text one link shows, read from the events between its ends."""
    closing = next(
        (
            after
            for after in range(at + 1, len(children))
            if children[after].type == LINK_CLOSE
        ),
        len(children),
    )
    return "".join(read(child, compacted) for child in children[at + 1 : closing])


def alternative(image: Token, compacted: bool = False) -> str:
    """The text one image's alternative content shows, its own uses aside.

    The alternative content is a run of inline events, and a use
    written there is compared as the use it is, so the text left to
    compare here is what surrounds it. A link's visible text is
    therefore read out of this run and read back on that link's own
    comparison, which is where a withholding mark the emission drops is
    accounted for.
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
            carried.append(read(child, compacted))
    return "".join(carried)


def uses(
    inline: Token, compacted: bool = False
) -> Iterator[tuple[Sequence[Token], int, Use]]:
    """Inline uses with their containing event run and position.

    Traversal follows `source.events`. A compacted command block's content
    uses `read` for text interpretation.
    """
    for children, at, child in events(inline.children or []):
        if child.type == LINK_OPEN:
            yield (
                children,
                at,
                Use(
                    LINK,
                    label(children, at, compacted),
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
                    alternative(child, compacted),
                    attribute(child, TITLE),
                    attribute(child, SRC),
                ),
            )


def carried(
    tokens: Sequence[Token], span: Token, compacted: Collection[int] = ()
) -> Iterator[tuple[Sequence[Token], int, Use]]:
    """Every comparable use in one region, in source order.

    Inline uses come from `uses`; diagram uses follow `source.Click` and the
    order `source.clicks` supplies. `compacted` names inline tokens by identity.
    """
    for token in within(tokens, [span]):
        if token.type == INLINE:
            yield from uses(token, id(token) in compacted)
        elif token.type == FENCE:
            for click in clicks(token):
                yield (
                    (),
                    0,
                    Use(CLICK, click.opening, click.title or "", click.destination),
                )


def positions(
    path: str, tokens: Sequence[Token], span: Token
) -> Iterator[Located | None]:
    """Where each use one region carries is written, in the order `carried` reads them.

    Inline identities use `provenance.link_at`; diagram identities use
    `provenance.click_at` on `source.Click`. Images have no composing identity.
    """
    for token in within(tokens, [span]):
        if token.type == INLINE:
            position = 0
            for _children, _at, use in uses(token):
                if use.kind != LINK or token.map is None:
                    yield None
                    continue
                yield link_at(path, token, token.map[0], position)
                position += 1
        elif token.type == FENCE:
            for click in clicks(token):
                yield click_at(path, click)


def intended(
    path: str,
    one: Use,
    at: int,
    children: Sequence[Token],
    targets: Mapping[tuple[str, str | None], str],
    declarations: Declarations = DECLARING,
    dispatched_to: Mapping[Served, str] | None = None,
    substitution: Substitution = UNSUBSTITUTED,
    contextual: bool = False,
    conversions: Mapping[str, Conversion] | None = None,
    folder: BundleFolder = WORKING_FOLDER,
) -> Use:
    """Compute the expected published fields of one source use.

    Resolve its target through `closure.bundled` or `closure.withholding_target`,
    applying the supplied maps. Deferred destinations use `closure.rebased`
    and `closure.deferred_title`. Visible text uses `closure.published_text`;
    diagram fields follow `source.Click`, with local label edits from
    `bundle.diagram_labels`. The supplied event run is the use's own, including
    uses inside image alternative content.
    """
    if one.kind == IMAGE:
        return one
    opening = one.text if one.kind == CLICK else opening_text(children, at)
    found = bundled(path, one.destination, opening, declarations, substitution)
    if contextual and found is not None:
        assigned = targets.get((found.path, found.fragment))
        if assigned is None:
            return one
        anchor = f"{ANCHOR}{assigned}"
        return Use(
            one.kind,
            one.text,
            one.title,
            anchor if one.kind == CLICK else normalizeLink(anchor),
        )
    if found is None:
        withheld = withholding_target(
            path,
            one.destination,
            opening,
            declarations,
            substitution,
            tags=read_tags(one.title),
        )
        if withheld is None:
            return one
        if dispatched(opening):
            served = {} if dispatched_to is None else dispatched_to
            given = served.get(
                ((withheld.path, withheld.fragment), withheld.tags, parallel(opening))
            )
            if given is None:
                raise Invalid(
                    TARGET_INTEGRITY,
                    f"the dispatch {one.destination!r} in {path!r} was assigned no "
                    f"destination",
                )
            return Use(
                one.kind,
                one.text
                if one.kind == CLICK and filed(given)
                else published_text(one.text, filed(given)),
                one.title,
                given if one.kind == CLICK else normalizeLink(given),
            )
        names = carried_names(withheld, conversions)
        if names:
            title = deferred_title(one.title, names) or ""
            one = Use(one.kind, one.text, title, one.destination)
        return withdrawn(one, rebased(withheld, one.destination, folder))
    assigned = targets.get((found.path, found.fragment))
    if assigned is None:
        raise Invalid(
            TARGET_INTEGRITY,
            f"the reference {one.destination!r} in {path!r} was assigned no "
            f"destination",
        )
    anchor = f"{ANCHOR}{assigned}"
    return Use(
        one.kind,
        one.text,
        one.title,
        anchor if one.kind == CLICK else normalizeLink(anchor),
    )


def withdrawn(one: Use, destination: str) -> Use:
    """One use with a supplied destination and `closure.unmarked` label.

    Its kind and title are carried into the result.
    """
    if one.kind == CLICK:
        return Use(one.kind, one.text, one.title, destination)
    return Use(one.kind, unmarked(one.text), one.title, normalizeLink(destination))


def carrying(
    tokens: Sequence[Token], span: Token, compacted: Collection[int] = ()
) -> set[int]:
    """The source lines excluded from the untouched-byte comparison.

    Collect inline-reference and command-block lines, and the
    diagram lines subject to `bundle.clicked` or `bundle.diagram_labels`.
    Include a following `bundle.names_model` line with its diagram use.
    """
    held: set[int] = set()
    for inline in inlines(tokens, [span]):
        if inline.map is not None and (
            id(inline) in compacted or any(True for _ in uses(inline))
        ):
            held.update(range(*inline.map))
    for fence in within(tokens, [span]):
        if fence.type != FENCE:
            continue
        content = lines(fence.content)
        first = 0 if fence.map is None else fence.map[0] + 2
        named = {click.node for click in clicks(fence)}
        for line, text in element_texts(fence.content, diagram_type(fence.content)):
            if text.node in named:
                held.add(first + line - 1)
        for click in clicks(fence):
            held.add(click.line - 1)
            beneath = click.line + 1 - first
            if beneath < len(content) and names_model(content[beneath], click):
                held.add(click.line)
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
    compacted: Collection[int] = (),
) -> list[str]:
    """Untouched non-heading content lines of one region, in order.

    Exclude the supplied removed lines, `carrying` lines and `bundle.blank`
    lines. Keep each remaining line's indentation and trailing spaces.
    """
    start, end = span.map or (0, 0)
    skipped = headed(tokens, span) | carrying(tokens, span, compacted) | set(removed)
    return [
        bare(physical[at])
        for at in range(start, end)
        if at not in skipped and not blank(physical[at])
    ]


def code(
    tokens: Sequence[Token],
    span: Token,
    local: Mapping[int, Collection[str]] | None = None,
) -> list[tuple[str, str, str]]:
    """Comparable code examples in one region.

    For diagrams, apply `bundle.diagram_labels` for the supplied local nodes,
    then `undestined` to isolate the code checked here from its link fields.
    """
    start, end = span.map or (0, 0)
    examples = []
    for token in tokens:
        if (
            token.type not in CODE_BLOCKS
            or token.map is None
            or not start <= token.map[0] < end
        ):
            continue
        nodes = () if local is None else local.get(id(token), ())
        if nodes:
            text, _ = diagram_labels(token, nodes)
            token = replace(token, content="".join(text), meta={})
        examples.append((token.type, token.info, undestined(token)))
    return examples


def undestined(example: Token) -> str:
    """A code example with the diagram fields checked by `references` excluded.

    `source.Click` supplies each destination offset and written extent;
    `TOOLTIP` locates a following tooltip. Remove spans last to first so
    offsets remain valid, and omit `bundle.names_model` lines.
    """
    held = lines(example.content)
    first = 0 if example.map is None else example.map[0] + 2
    for click in reversed(list(clicks(example))):
        at = click.line - first
        if at + 1 < len(held) and names_model(held[at + 1], click):
            del held[at + 1]
        line = held[at]
        rest = line[click.offset + len(click.written) :]
        tip = TOOLTIP.match(rest)
        if tip is not None:
            rest = rest[: tip.start(1) - 1].rstrip() + rest[tip.end() :]
        held[at] = line[: click.offset] + rest
    return "".join(held)


def prose(tokens: Sequence[Token], span: Token) -> list[Token]:
    """Inline tokens outside headings in a region, in source order.

    Heading text is checked by `outline`.
    """
    occupied = headed(tokens, span)
    return [
        inline
        for inline in inlines(tokens, [span])
        if inline.map is not None and inline.map[0] not in occupied
    ]


def parts(groups: Sequence[Group]) -> list[tuple[str, str]]:
    """Descriptions of emitted parts for a boundary error.

    Name each part from its `provenance.Record`; use its position when that
    record has no corresponding entry. `structure` checks the pairing itself.
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
            elif isinstance(part, Instruction):
                named.append((f"the {part.kind} {part.text!r} of {path!r}", path))
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
    """Require every emitted part to open its own candidate region.

    Use `bundle.openings` to locate each part in the reparse. An opening inside
    another block raises `Unsafe`; `structure` handles parts absent entirely.
    """
    named = parts(groups)
    started = {token.map[0] for token in spans if token.map is not None}
    for (carried, opening), opens, (what, _path) in zip(
        named[:-1], openings(groups)[1:], named[1:], strict=True
    ):
        if opens in started or opens >= len(physical):
            continue
        holding = container(spans, opens)
        kind = (
            "container"
            if holding is None
            else CONTAINERS.get(holding.type, holding.type)
        )
        raise Unsafe(carried, what, kind, opening, opens + 1)


def structure(
    spans: Sequence[Token], groups: Sequence[Group]
) -> list[tuple[Record, Part, Token]]:
    """Pair parsed candidate regions with each group's provenance parts.

    Check the wrapper separately and pair every remaining part in emission
    order. Raise `Invalid` for missing, extra or mismatched region kinds, so a
    heading-only ancestor cannot account for a selected region.
    """
    expected = sum((1 if one.wrapped else 0) + len(one.record.parts) for one in groups)
    if len(spans) != expected:
        short = len(spans) < expected
        raise Invalid(
            NO_OMISSIONS if short else NO_EXPANSION,
            f"the candidate holds {len(spans)} region(s) against the {expected} "
            f"the provenance accounts for",
        )
    paired: list[tuple[Record, Part, Token]] = []
    at = 0
    for one in groups:
        if one.wrapped:
            opening = spans[at]
            if opening.type != HEADING_OPEN or level(opening) != one.level:
                raise Invalid(
                    GROUP_ISOLATION,
                    f"the group for {one.record.path!r} opens on a {opening.type!r} "
                    f"rather than on its own heading at level {one.level}",
                )
            at += 1
        for part in one.record.parts:
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
            if isinstance(part, Instruction) and span.type != (
                BULLET_LIST_OPEN if part.listed else PARAGRAPH_OPEN
            ):
                raise Invalid(
                    NO_EXPANSION,
                    f"the {part.kind} {part.text!r} of {one.record.path!r} is "
                    f"emitted as a {span.type!r} rather than as a "
                    f"{'bulleted list' if part.listed else 'paragraph'}",
                )
            paired.append((one.record, part, span))
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


def absorbing(record: Record, path: str, tokens: Sequence[Token]) -> set[int]:
    """The source-title line represented by a group's wrapper or member heading.

    Title recognition uses `bundle.document_title`; merged member-title
    matching uses `bundle.absorbed` against the path stem.
    """
    found = (
        document_title(tokens)
        if record.merged is None
        else absorbed(tokens, PurePosixPath(path).stem)
    )
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


def placement(record: Record, parsed: Mapping[str, Sequence[Token]]) -> None:
    """Check each recorded part against its source's ancestor chain.

    For a file group, each required ancestor must precede the part it places.
    For merged groups, match against the complete set of recorded origins.
    Composed ranges are excluded from source-chain placement. Each structural
    ancestor must place a later part; otherwise raise `Invalid`.
    """
    answered: dict[str, set[int | None]] = {}
    for each in record.placed():
        for origin in each.origins:
            answered.setdefault(origin.path, set()).add(origin.line)
    needed: dict[str, set[int]] = {}
    for path in record.paths():
        tokens = parsed[path]
        chains = above(tokens)
        emitted_at: set[int | None] = set(absorbing(record, path, tokens))
        if record.merged is not None:
            emitted_at |= answered.get(path, set())
        for one in record.parts:
            if sourced(one) != path or (isinstance(one, Range) and one.composed):
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
        if record.preamble:
            continue
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
    """Reject live links and images in a structural ancestor's inline content.

    `structure` checks the region's kind and any additional regions.
    """
    found = [use for inline in inlines(tokens, [span]) for _, _at, use in uses(inline)]
    if found:
        raise Invalid(
            NO_NEW_LINKS,
            f"the structural ancestor {one.text!r} of {one.origins[0].path!r} "
            f"publishes the use(s) {found!r}",
        )


def coverage(groups: Sequence[Group]) -> None:
    """Require each selected source range to occur once within its group.

    Compare source coordinates, rather than prose strings, and reject
    overlapping ranges. Exclude composed ranges from this count.
    """
    carried: dict[tuple[int, str], list[tuple[int, int]]] = {}
    for at, one in enumerate(groups):
        for each in one.record.ranges:
            if each.composed:
                continue
            carried.setdefault((at, each.path), []).append(each.lines)
    for (_, path), held in carried.items():
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
    """Require candidate heading count, visible text and level to match records.

    `placement` checks source ancestry; `levels` checks recorded source levels.
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
    """Check recorded heading levels, depth, group isolation and source order.

    Each recorded level must equal its origin's level plus shift, stay within
    `bundle.MAX_LEVEL`, and sit below its generated group opening. Check source
    order for file groups; merged and composed headings use `placement` for
    their arrangement. Validate these records before parsing the candidate,
    because excess heading depth parses as text.
    """
    opening = next(
        (
            heading.level
            for heading in record.headings
            if isinstance(heading, Generated) and heading.kind in OPENINGS
        ),
        None,
    )
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
        if opening is not None and one.level <= opening:
            raise Invalid(
                GROUP_ISOLATION,
                f"the heading {one.text!r} of {record.path!r} is emitted at the "
                f"level its group's own heading holds",
            )
        if record.merged is not None or (isinstance(one, Carried) and one.composed):
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
    """Map assigned fragments to the emitted headings they actually reach.

    Recompute candidate fragments through `source.fragments` and reject a
    sequence differing from the assigned fragment sequence.
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


def one_member(groups: Sequence[Group]) -> None:
    """Hold each merged group's emitted heading to answering one member.

    Reject a heading whose target answers name more than one source path.
    `grouping.contributed` and `grouping.overview` assign whole-document
    targets during construction.
    """
    for group in groups:
        record = group.record
        if record.merged is None:
            continue
        for one in record.headings:
            members = sorted({path for path, _ in one.answers})
            if len(members) > 1:
                raise Invalid(
                    ONE_MEMBER,
                    f"the heading {one.text!r} of the group {record.path!r} answers "
                    f"the targets of {members[0]!r} and {members[1]!r}",
                )


def leakage(environment: Mapping[str, Any]) -> None:
    """Hold the candidate to carrying no surviving link-reference definition.

    Inspect the `profile.REFERENCES` environment from the candidate parse
    and reject any declared label. `bundle.group` excludes definition
    source lines during construction.
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
    """One side of a region comparison.

    `tokens` holds the parsed source, `physical` its source lines, and `span`
    the region being compared. `compacted` holds command-block inline token
    identities for this side.
    """

    tokens: Sequence[Token]
    physical: Sequence[str]
    span: Token
    compacted: frozenset[int] = field(default_factory=frozenset)


def compaction(source: Side, published: Side) -> tuple[Side, Side]:
    """Pair command-block tokens on both sides of a region comparison.

    Recognize source blocks through `profile.command_block`, then mark their
    corresponding published inline tokens by position. `preserved` checks the
    inline counts before comparing their content.
    """
    pairs = [
        (one, each)
        for one, each in zip(
            prose(source.tokens, source.span),
            prose(published.tokens, published.span),
            strict=False,
        )
        if command_block(one.children or [])
    ]
    return (
        replace(source, compacted=frozenset(id(one) for one, _ in pairs)),
        replace(published, compacted=frozenset(id(each) for _, each in pairs)),
    )


def content(written: str) -> str:
    """What a command block's source shows, as its compacted form shows it.

    The line breaks inside the wrapper tags are not read, and a
    backslash ending a line reads as the line break a backslash makes.
    """
    return written.strip(LINE_FEED).replace(ESCAPED_BREAK, LINE_FEED)


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
    declarations: Declarations = DECLARING,
    dispatched_to: Mapping[Served, str] | None = None,
    substitution: Substitution = UNSUBSTITUTED,
    composing: Mapping[Located, str] | None = None,
    contextual: bool = False,
    conversions: Mapping[str, Conversion] | None = None,
    folder: BundleFolder = WORKING_FOLDER,
) -> None:
    """Compare a region's published uses with their expected source uses.

    `intended` supplies expected link fields; `withdrawn` supplies composing
    uses whose destinations come from the composition map. Reject differences
    in count or any compared field. Diagram fields follow `source.Click`.
    """
    contributing = {} if composing is None else composing
    expected: list[Use] = []
    for (children, at, one), written in zip(
        carried(source.tokens, source.span, source.compacted),
        positions(path, source.tokens, source.span),
        strict=True,
    ):
        anchor = None if written is None else contributing.get(written)
        expected.append(
            intended(
                path,
                one,
                at,
                children,
                targets,
                declarations,
                dispatched_to,
                substitution,
                contextual,
                conversions,
                folder,
            )
            if anchor is None
            else withdrawn(one, f"{ANCHOR}{anchor}")
        )
    found = [
        one
        for _, _at, one in carried(
            published.tokens, published.span, published.compacted
        )
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
    path: str,
    removed: Collection[int],
    source: Side,
    published: Side,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    dispatched_to: Mapping[Served, str] | None = None,
    conversions: Mapping[str, Conversion] | None = None,
) -> None:
    """Compare a region's untouched lines, code examples and visible prose.

    `body` and `code` supply the byte and example comparisons. For inline
    content, compare `bundle.emitted_visible` with the candidate's `read` text,
    using `content` for compacted command blocks. Raise `Invalid` on a
    difference in counts or content.
    """
    wrote = body(source.physical, source.tokens, source.span, removed, source.compacted)
    carries = body(
        published.physical,
        published.tokens,
        published.span,
        compacted=published.compacted,
    )
    if wrote != carries:
        raise Invalid(
            PRESERVATION,
            f"the region at lines {source.span.map} of {path!r} wrote {wrote!r} "
            f"and the candidate carries {carries!r}",
        )
    local: dict[int, set[str]] = {}
    for fence in within(source.tokens, [source.span]):
        if fence.type != FENCE:
            continue
        for click in clicks(fence):
            if not dispatched(click.opening):
                continue
            expected = intended(
                path,
                Use(CLICK, click.opening, click.title or "", click.destination),
                0,
                (),
                {},
                declarations,
                dispatched_to,
                substitution,
                conversions=conversions,
            )
            if not filed(expected.destination):
                local.setdefault(id(fence), set()).add(click.node)
    examples = code(source.tokens, source.span, local)
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
        shown = emitted_visible(
            path,
            one,
            declarations,
            substitution,
            dispatched_to,
            conversions=conversions,
        )
        compacted = id(each) in published.compacted
        if compacted:
            shown = content(shown)
        shows_here = "".join(read(child, compacted) for child in each.children or [])
        if shown != shows_here:
            raise Invalid(
                PRESERVATION,
                f"the region at lines {source.span.map} of {path!r} shows "
                f"{shown!r} and the candidate shows {shows_here!r}",
            )


def dispatches(
    reached: Mapping[str, tuple[Record, Emitted]],
    dispatching: Dispatching,
    bundle_file: Callable[[Reference], str],
    conversions: Mapping[str, Conversion],
) -> None:
    """Check dispatch destinations against their recorded heading or file kind.

    Local destinations must reach the generated dispatch kind selected by
    the supplied dispatch and conversion context. File destinations are
    classified by `closure.filed`.
    """
    for (path, _line, _placing), served in dispatching.items():
        for (target, tags, together), destination in served.items():
            reference = Reference(target[0], target[0], target[1], tags=tags)
            briefed = briefing(reference, conversions[target[0]]) is not None
            kinds = (
                (PICK_SECTION,)
                if picks(tags) and not together
                else (PARALLEL_SECTION, BRIEF_SECTION)
                if together and briefed
                else (PARALLEL_SECTION,)
                if together
                else (BRIEF_SECTION,)
            )
            kind = kinds[0]
            if filed(destination):
                if kind == PICK_SECTION:
                    raise Invalid(
                        TARGET_INTEGRITY,
                        f"the dispatch of {target!r} with tags {sorted(tags)!r} "
                        f"in {path!r} carries the pick token and points at the "
                        f"file {destination!r}",
                    )
                expected = quote(bundle_file(reference), safe="")
                if destination != expected:
                    raise Invalid(
                        TARGET_INTEGRITY,
                        f"the dispatch of {target!r} with tags {sorted(tags)!r} "
                        f"in {path!r} points at {destination!r}, whose bundle "
                        f"selection differs from {expected!r}",
                    )
                continue
            found = reached.get(destination.removeprefix(ANCHOR))
            if found is None or not (
                isinstance(found[1], Generated) and found[1].kind in kinds
            ):
                raise Invalid(
                    TARGET_INTEGRITY,
                    f"the destination {destination!r} a dispatch of {target!r} in "
                    f"{path!r} was given reaches no {kind}",
                )


def parallel_sets(
    tokens: Sequence[Token],
    assigned: Sequence[str],
    dispatching: Dispatching,
    bundle_file: Callable[[Reference], str],
    read: Mapping[str, Source],
    paired: Sequence[tuple[Record, Part, Token]],
) -> None:
    """Require each generated dispatch section to list its recorded files.

    Read the section's own dispatch lines through its closing heading, passing
    over nested dispatch sections and including lifted member subsections.
    Compare the resulting sequence with the supplied dispatch records.
    """
    lines = {
        id(span)
        for _record, part, span in paired
        if isinstance(part, Instruction) and part.activates is None
    }
    nested = {
        id(span): part.kind
        for _record, part, span in paired
        if isinstance(part, Generated)
        and part.kind in (PARALLEL_SECTION, PICK_SECTION, BRIEF_SECTION)
    }
    openings = dict(
        zip(assigned, (one for one, _inline in headings(tokens)), strict=True)
    )
    spans = list(regions(tokens))
    positions = {id(span): at for at, span in enumerate(spans)}

    def own(opening: Token) -> tuple[list[str], list[Token]]:
        found: list[str] = []
        members: list[Token] = []
        skipping: int | None = None
        for span in spans[positions[id(opening)] + 1 :]:
            if span.type == HEADING_OPEN:
                if level(span) <= level(opening):
                    break
                if skipping is not None and level(span) <= skipping:
                    skipping = None
                if skipping is None and id(span) in nested:
                    skipping = level(span)
                    if (
                        nested[id(opening)] == PARALLEL_SECTION
                        and nested[id(span)] == BRIEF_SECTION
                        and level(span) == level(opening) + 1
                    ):
                        members.append(span)
                continue
            if skipping is not None or id(span) not in lines:
                continue
            found.extend(
                one.destination
                for _children, _at, one in carried(tokens, span)
                if one.kind == LINK
            )
        return found, members

    expected: dict[str, set[str]] = {}
    for served in dispatching.values():
        for (target, tags, together), destination in served.items():
            if filed(destination):
                continue
            reference = Reference(target[0], target[0], target[1], tags=tags)
            listed = (
                [reference]
                if together or not picks(tags)
                else [
                    one
                    for one, _alternative in alternatives_of(
                        reference, read[target[0]].conversion
                    )
                ]
            )
            expected.setdefault(destination, set()).update(
                quote(bundle_file(one), safe="") for one in listed
            )
    for destination, files in expected.items():
        found, members = own(openings[destination.removeprefix(ANCHOR)])
        for member in members:
            found.extend(own(member)[0])
        if len(found) != len(files) or set(found) != files:
            raise Invalid(
                TARGET_INTEGRITY,
                f"the dispatch set {destination!r} lists {found!r} against "
                f"its effective bundle files {sorted(files)!r}",
            )


def contributions(
    reached: Mapping[str, tuple[Record, Emitted]],
    composing: Contributing,
) -> None:
    """Hold each composing link's destination to a contribution heading.

    A contribution heading answers to no source target, so what a
    composing link's destination is held to is the kind of heading it
    reaches.
    """
    for (path, line, _column, _at), destination in (
        each for links in composing.values() for each in links.items()
    ):
        found = reached.get(destination)
        if found is None or not (
            isinstance(found[1], Generated) and found[1].kind == CONTRIBUTION_HEADING
        ):
            raise Invalid(
                TARGET_INTEGRITY,
                f"the destination {destination!r} a directive at line {line + 1} "
                f"of {path!r} was given reaches no contribution heading",
            )


def activation(
    part: Instruction,
    span: Token,
    tokens: Sequence[Token],
    folder: BundleFolder = WORKING_FOLDER,
) -> None:
    """Check the sole link of a deferred contribution against its record.

    Read its target through `closure.resolve` and `closure.BundleFolder.rooted`,
    and its requested tags through `tags.read`, then compare with
    `provenance.Instruction.activates`.
    """
    found = [use for inline in inlines(tokens, [span]) for _c, _a, use in uses(inline)]
    resolved = [resolve(use.destination) for use in found]
    selections = [
        ((folder.rooted(one.path), one.fragment), read_tags(use.title))
        for one, use in zip(resolved, found, strict=True)
    ]
    if selections != [part.activates]:
        raise Invalid(
            TARGET_INTEGRITY,
            f"the line {part.text!r} a deferred directive's contribution carries "
            f"does not preserve its one requested selection {part.activates!r}",
        )


def validate(
    bundled: str,
    groups: Sequence[Group],
    assigned: Sequence[str],
    targets: Mapping[tuple[str, str | None], str],
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
    budget: int,
    dispatching: Dispatching | None = None,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    composing: Contributing | None = None,
    *,
    bundle_file: Callable[[Reference], str],
    within: Mapping[Chain, Mapping[tuple[str, str | None], str]] | None = None,
    folder: BundleFolder = WORKING_FOLDER,
) -> None:
    """Validate provenance and the completed candidate against their sources.

    Run the record checks first, then reparse through `profile.parse`
    and run the boundary, structure, reference and preservation
    checks. `within` supplies each composition copy's target map and
    `closure.Substitution.composed` its substitutions. `folder` is the
    publication folder used by `closure.rebased`. A failure raises before the
    caller can publish the candidate.
    """
    coverage(groups)
    for one in groups:
        if one.record.path not in read:
            continue
        levels(one.record)
        placement(one.record, parsed)
    environment: dict[str, Any] = {}
    tokens = parse(bundled, budget, environment)
    physical = lines(bundled)
    spans = list(regions(tokens))
    boundaries(physical, spans, groups)
    paired = structure(spans, groups)
    leakage(environment)
    outline(tokens, groups)
    served = {} if dispatching is None else dispatching
    emitted = runs(tokens)
    sourced = {path: runs(one) for path, one in parsed.items()}
    reached = named(tokens, groups, assigned)
    integrity(reached, targets)
    one_member(groups)
    dispatches(
        reached,
        served,
        bundle_file,
        {path: one.conversion for path, one in read.items()},
    )
    parallel_sets(tokens, assigned, served, bundle_file, read, paired)
    contributing = {} if composing is None else composing
    owned = {} if within is None else within
    contributions(reached, contributing)
    for record, part, span in paired:
        if isinstance(part, Ancestor):
            structural(record, part, span, tokens)
            continue
        if isinstance(part, Instruction):
            if part.activates is not None:
                activation(part, span, tokens, folder)
            continue
        if isinstance(part, Generated):
            continue
        carried = part
        wrote = located(parsed[carried.path], carried.lines)
        source = Side(
            sourced[carried.path][id(wrote)],
            lines(read[carried.path].text),
            wrote,
        )
        source, published = compaction(source, Side(emitted[id(span)], physical, span))
        reading = substitution.composed(carried.path, carried.selecting)
        references(
            carried.path,
            source,
            published,
            {**targets, **owned.get(carried.placing, {})},
            declarations,
            served.get((carried.path, carried.lines[0], carried.placing), {}),
            reading,
            contributing.get(carried.placing, {}),
            record.preamble,
            {path: one.conversion for path, one in read.items()},
            folder,
        )
        preserved(
            carried.path,
            carried.removed,
            source,
            published,
            declarations,
            reading,
            served.get((carried.path, carried.lines[0], carried.placing), {}),
            {path: one.conversion for path, one in read.items()},
        )
