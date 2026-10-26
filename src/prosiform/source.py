"""One source document: the content it carries, and the headings that name it.

A file holds two things the author did not write as instructions: a
leading byte-order mark, which is a text-file convention, and a leading
frontmatter block, which is metadata for whatever reads the file. Neither
is content, and both would otherwise be published as body. The scan below
removes them before anything parses the document.

The scan recognizes delimiters by exact physical-line comparison and
decodes the enclosed YAML into immutable conversion settings. An indented
delimiter, a delimiter
carrying a trailing space, a TOML `+++` fence, JSON metadata, and a `---`
under a blank line are each a line the comparison rejects, so each is
body the bundle carries. A document meaning to open on a horizontal rule
spells it another way, `***` among them; the leading `---` is reserved.

A removal moves every line after it, so the content is returned with the
line it began on. A location at line `n` of the content sits at line
`n + first_line - 1` of the file, and that expression is the only place
the shift is applied. A byte-order mark sits at the head of line 1, which
stays line 1, so the mark shifts no coordinate; the block does.

A heading is the only thing that names a section, so the index below is
what a fragment resolves against. A heading's visible text is derived
from the parser's own events rather than from the bytes that produced
them: text and code content, the label a link shows and the character
an entity decodes to are text a reader reads, a line break is the line
break it is, and a formatting delimiter, a raw HTML tag and an image
each direct what is read without being read. The derivation therefore
reads the event stream and nothing else, which is why a heading written
three ways with one appearance indexes once.

A heading's fragment is the slug its own visible text produces: the text
lowered, the characters the renderer discards removed, and each
remaining space a hyphen. Nothing numbers two headings of one source
apart, so a fragment names a heading by what its author wrote and not by
how many similar headings precede it. A fragment no heading's text
produces names nothing; a fragment two headings' text produces names
neither, which is the refusal `Ambiguous` raises, and the author
disambiguates by retitling.

The renderer's own ordinal belongs to a bundle destination rather than to
a source fragment, because the tool assigns it over a document it
generated in one pass. `fragments` below is that rule, applied to the
sequence of headings a bundle emits.

Every heading the profile recognizes is indexed, a container-nested one
included: eligibility to be selected is a later decision, and a heading
a container carries is one a renderer reading the bundle indexes beside
the rest.

A source is also recorded as the file it was read from: the canonical
path that read arrived at, and a hash of the bytes it held. The pair is
a record of a read, which a later read of the same source can be
compared against.

A reference use is read from the same events. What a document requires
is written in the marks its author wrote, and either a link or an image
can carry one, so the model reports each link and each image a given
run of regions carries: where it points, the literal text its content
opens on, the line of its block, and whether it names a resource
whatever it points at. An image names one, because a picture is carried
as the text its author wrote rather than bundled, and the mark a caller
finds on one is therefore a request the bundle cannot meet. An apparent
link inside a code span or a code block is example content the parser
produces no use for, so none reaches a caller asking what this content
references.

That later decision is the section below. A document is a run of
maximal regions, each a block the document itself carries, and a
container is one region whatever it holds. Only a heading that is such
a region roots a section: it is the heading a reader finds at the
document's own level, and the blocks following it belong to it until
the document returns to that level or above. A heading a container
carries is therefore neither a root nor a boundary — it sits inside one
region, so the region it sits in is what the document holds there — and
a fragment naming one names a section the model does not have.

The content above a document's first eligible heading is the document's
own, so a selection naming the whole document carries it. A link is read
for the target it names and the position the source wrote it at, and the
section it sits in enters neither: a reference names the same target
wherever its author put it.

The document also counts what a budget is declared over: the container
blocks it nests at its deepest point, which is what a nesting budget
bounds, and the link and image occurrences a run of regions carries,
each counted once where the source wrote it.
"""

import hashlib
import re
from collections.abc import Iterator, Sequence
from dataclasses import dataclass

from markdown_it.token import Token

from prosiform.limits import FILE_BYTES, NESTING
from prosiform.metadata import (
    INVALID_CONVERSION_METADATA,
    INVALID_FRONTMATTER,
    Conversion,
)
from prosiform.metadata import decode as decode_metadata

ENCODING = "utf-8"
MARK = "﻿"
DIGEST = "sha256"
TOP_LEVEL = 1

OPENER = "---"
CLOSERS = ("---", "...")

LINE_FEED = "\n"
CARRIAGE_RETURN = "\r"

PHYSICAL_LINE = re.compile(r"[^\n]*\n|[^\n]+")
CONTAINER_PREFIX = re.compile(
    r"^(?:[ \t]*(?:>|[-*+](?=[ \t])|\d{1,9}[.)](?=[ \t])))*[ \t]*"
)

UNTERMINATED_FRONTMATTER = "E_UNTERMINATED_FRONTMATTER"
NESTED_SECTION_TARGET = "E_NESTED_SECTION_TARGET"
AMBIGUOUS_SOURCE_HEADING = "E_AMBIGUOUS_SOURCE_HEADING"

CODES = (
    INVALID_FRONTMATTER,
    INVALID_CONVERSION_METADATA,
    UNTERMINATED_FRONTMATTER,
    NESTED_SECTION_TARGET,
    AMBIGUOUS_SOURCE_HEADING,
)

HEADING_OPEN = "heading_open"
INLINE = "inline"
TEXT = "text"
CODE_INLINE = "code_inline"
LINK_OPEN = "link_open"
IMAGE = "image"
REFERENCE_USES = (LINK_OPEN, IMAGE)
CONTAINER_OPEN = ("blockquote_open", "list_item_open")
CONTAINER_CLOSE = ("blockquote_close", "list_item_close")
HREF = "href"
SRC = "src"
BREAKS = ("softbreak", "hardbreak")

SLUG_DISCARDED = re.compile("[\u0000-\u001f!-,./:-@[-^`{-~]")
SLUG_SPACE = " "
SLUG_HYPHEN = "-"
ORDINAL = "-"


class Nested(Exception):
    """A fragment naming a heading a container carries, which roots no section."""

    def __init__(self, fragment: str) -> None:
        super().__init__(
            f"the fragment {fragment!r} names a heading a container carries"
        )
        self.fragment = fragment


class Ambiguous(Exception):
    """A fragment two headings of one source produce, which names neither."""

    def __init__(self, fragment: str, lines: Sequence[int | None]) -> None:
        super().__init__(
            f"the fragment {fragment!r} names {len(lines)} headings of one document"
        )
        self.fragment = fragment
        self.lines = tuple(lines)


class Unterminated(Exception):
    """A recognized frontmatter opener the document never closes."""

    def __init__(self, at: int) -> None:
        super().__init__(f"the frontmatter opener at line {at} has no closing line")
        self.line = at


@dataclass(frozen=True)
class Source:
    """One document's content, and where that content begins in its file."""

    text: str
    first_line: int = 1
    conversion: Conversion = Conversion()
    root: str = ""
    display: str = ""
    identity: str = ""

    def line(self, at: int | None) -> int | None:
        """The line of the original file one line of this content occupies."""
        return None if at is None else at + self.first_line - 1


@dataclass(frozen=True)
class Capture:
    """What one source was at the moment the run read it.

    The identity is the canonical filesystem path that read arrived at
    and the digest is taken over the bytes the file held, so comparing
    a later read against both answers whether a document is still the
    one the run read. It records a read rather than holding a file
    still: a source can be written again after any comparison, and a
    digest taken over one file says nothing about the others.
    """

    identity: str
    digest: str
    chain: tuple[str, ...]
    walk: str
    directories: tuple[tuple[str, int, int], ...]
    file_identity: tuple[int, int]
    size: int


def hashed(data: bytes) -> str:
    """One source's content hash, taken over the bytes its file held."""
    return hashlib.new(DIGEST, data).hexdigest()


def lines(text: str) -> list[str]:
    """Each physical line of the text, its terminator included.

    A line ends at a line feed, which a carriage return may precede, and
    at nothing else. `str.splitlines` also ends one at a form feed, a line
    separator and four further characters Unicode calls line breaks, none
    of which ends a line in CommonMark.
    """
    return PHYSICAL_LINE.findall(text)


def bare(physical: str) -> str:
    """One physical line without the LF or CRLF that terminates it."""
    stripped = physical.removesuffix(LINE_FEED)
    return stripped.removesuffix(CARRIAGE_RETURN)


def opening_markers(line: str) -> str:
    """The container markers and indent one line opens with, before its content."""
    written = CONTAINER_PREFIX.match(line)
    return "" if written is None else written.group(0)


def decode(data: bytes) -> str:
    """One source's bytes as text, which they are only if they are valid UTF-8.

    The strict error handler is the one that raises. Substituting a
    replacement character would put a byte the author never wrote into
    content the tool promises to preserve, and then report success.
    """
    return data.decode(ENCODING)


def content(
    text: str,
    *,
    file: str = "",
    max_bytes: int = FILE_BYTES.default,
    max_depth: int = NESTING.default,
) -> Source:
    """One source's content, its leading transport metadata removed.

    Exactly one byte-order mark is removed, and a second is content. The
    frontmatter opener is the first physical line where that line is the
    three characters of `OPENER`; the block closes at the next physical
    line equal to one of `CLOSERS`, and the opener, the metadata, the
    closer and the closer's terminator go together.
    """
    raw = text.encode(ENCODING)
    body = text.removeprefix(MARK)
    physical = lines(body)
    if not physical or bare(physical[0]) != OPENER:
        conversion = decode_metadata(
            raw, file=file, span=None, max_bytes=max_bytes, max_depth=max_depth
        )
        return Source(body, conversion=conversion)
    start = len((text[: len(text) - len(body)] + physical[0]).encode(ENCODING))
    end = start
    for index, line in enumerate(physical[1:], start=1):
        if bare(line) in CLOSERS:
            conversion = decode_metadata(
                raw,
                file=file,
                span=(start, end),
                max_bytes=max_bytes,
                max_depth=max_depth,
            )
            return Source("".join(physical[index + 1 :]), index + 2, conversion)
        end += len(line.encode(ENCODING))
    raise Unterminated(1)


def visible(inline: Token) -> str:
    """The text an inline token shows, which is what its fragment comes from."""
    return "".join(shown(child) for child in inline.children or [])


def shown(child: Token) -> str:
    """The part of one inline event a reader reads.

    Text and code content are read as the characters they carry, an
    entity having already been decoded into the text that holds it. A
    line break is the character that breaks the line, which the slug
    then discards as the control character it is. Everything else
    directs what is read without being read: an emphasis, link or
    strikethrough delimiter, a raw HTML tag, and an image, whose
    alternative text describes a picture to a reader who cannot see it
    rather than appearing beside one who can.
    """
    if child.type in (TEXT, CODE_INLINE):
        return child.content
    if child.type in BREAKS:
        return LINE_FEED
    return ""


def slug(text: str) -> str:
    """The fragment a renderer generates for a heading carrying this text."""
    return SLUG_DISCARDED.sub("", text.lower()).replace(SLUG_SPACE, SLUG_HYPHEN)


def fragments(shown_texts: Sequence[str]) -> list[str]:
    """The fragment a renderer generates for each heading of one sequence.

    The first heading to carry a slug takes it, and a later one takes
    the slug and an ordinal, counting from one. An ordinal something
    already carries is passed over, so a heading whose own text spells
    one keeps it and the heading that would have been numbered into it
    takes the next free ordinal instead. Two headings therefore never
    share a fragment.

    This is the renderer's own rule, reproduced so a destination and the
    document it names agree. The sequence it runs over is the headings
    the bundle emits, in bundle order, and the counts it keeps belong to
    one run over one sequence, so a sequence begun again is numbered
    from the start.
    """
    counted: dict[str, int] = {}
    taken: set[str] = set()
    assigned = []
    for text in shown_texts:
        name = slug(text)
        if name not in taken:
            counted[name] = 0
        else:
            ordinal = counted.get(name, 0) + 1
            while f"{name}{ORDINAL}{ordinal}" in taken:
                ordinal += 1
            counted[name] = ordinal
            name = f"{name}{ORDINAL}{ordinal}"
        taken.add(name)
        assigned.append(name)
    return assigned


def level(opening: Token) -> int:
    """The level a heading token opens at, whatever syntax it is written in."""
    return int(opening.tag[1:])


def headings(tokens: Sequence[Token]) -> Iterator[tuple[Token, Token]]:
    """Every heading the source carries, each with the inline token holding its text."""
    for index, token in enumerate(tokens[:-1]):
        if token.type == HEADING_OPEN and tokens[index + 1].type == INLINE:
            yield token, tokens[index + 1]


@dataclass(frozen=True)
class Heading:
    """One source heading: its level, the text it shows and that text's slug."""

    level: int
    text: str
    fragment: str
    line: int | None


def headed(opening: Token, inline: Token) -> Heading:
    """One heading, read from the token opening it and the text it shows."""
    return Heading(
        level=level(opening),
        text=visible(inline),
        fragment=slug(visible(inline)),
        line=None if opening.map is None else opening.map[0] + 1,
    )


def index(tokens: Sequence[Token]) -> tuple[Heading, ...]:
    """Every heading one complete source document carries, in source order."""
    return tuple(headed(opening, inline) for opening, inline in headings(tokens))


def regions(tokens: Sequence[Token]) -> Iterator[Token]:
    """The token opening each maximal region of the document.

    A region is a block at the document level: a container is one region
    whatever it holds, and a token inside one opens no region of its own.
    """
    depth = 0
    for token in tokens:
        if depth == 0 and token.nesting >= 0 and token.map is not None:
            yield token
        depth += token.nesting


def opens(tokens: Sequence[Token], opening: Token) -> int | None:
    """Where one token opens a region of this document, by position in its run.

    Tokens are compared by identity. Two headings carrying one text and
    one level are equal as values, so a comparison by value would place
    the first of them wherever the second occurs.
    """
    return next((at for at, token in enumerate(tokens) if token is opening), None)


def section(tokens: Sequence[Token], fragment: str) -> tuple[Token, ...] | None:
    """The document-level regions one fragment selects.

    The fragment names a heading of this document's index, and the
    section it roots runs from that heading to the next document-level
    heading of equal or higher level, or to the end of the document
    where the document holds no such heading. A deeper document-level
    heading and its content belong to the section, and a heading a
    container carries neither roots nor ends one.

    A fragment naming no heading of this document selects nothing and is
    reported as the reference to nothing it is. A fragment two headings
    produce names neither, and is refused as the ambiguity it is before
    anything asks what either heading roots: the run cannot say which
    heading was meant, so it cannot say that the one that was meant
    roots no section. A fragment naming one heading a container carries
    names a heading the document carries and a section it does not,
    which is the refusal `Nested` raises.
    """
    carried = [opening for opening, _ in headings(tokens)]
    named = index(tokens)
    found = [one for one, each in enumerate(named) if each.fragment == fragment]
    if len(found) > 1:
        raise Ambiguous(fragment, [named[one].line for one in found])
    if not found:
        return None
    at = found[0]
    spans = list(regions(tokens))
    start = opens(spans, carried[at])
    if start is None:
        raise Nested(fragment)
    depth = named[at].level
    end = len(spans)
    for following in range(start + 1, len(spans)):
        token = spans[following]
        if token.type == HEADING_OPEN and level(token) <= depth:
            end = following
            break
    return tuple(spans[start:end])


@dataclass(frozen=True)
class Use:
    """One reference use a source carries, read from the parser's events.

    The destination is the one the parser resolved, so a reference-style
    use and an inline one arrive the same way and a Markdown escape has
    already been read. The opening is the literal text the use's content
    begins with, which is where a dependency's mark is written: content
    opening on a code span, an emphasis or an image begins with no text
    and opens with nothing.

    A resource is a reference the bundle carries as the text its author
    wrote rather than opening it, which an image is whatever file it
    points at: the alternative content of an image describes a picture,
    and no picture is a document the bundle can carry.
    """

    destination: str
    opening: str
    line: int | None
    resource: bool


def opening_text(children: Sequence[Token], at: int) -> str:
    """The literal text the link opened at one position begins with."""
    following = children[at + 1] if at + 1 < len(children) else None
    if following is None or following.type != TEXT:
        return ""
    return following.content


def alternative_text(image: Token) -> str:
    """The literal text one image's alternative content begins with.

    An image's alternative content is a run of its own, so its opening
    is the first event of that run rather than the event following the
    image, which is the text beside the picture.
    """
    children = image.children or []
    first = children[0] if children else None
    if first is None or first.type != TEXT:
        return ""
    return first.content


def within(tokens: Sequence[Token], selected: Sequence[Token]) -> Iterator[Token]:
    """Each token the given regions of one document carry, in source order.

    A token belongs to a region when the line it opens on falls inside
    that region's span, so a container's own opening and everything it
    holds arrive together and a check reading this run sees the same
    structure the whole document would show it, narrowed to what the
    run selected. A token the parser records no position for opens
    nothing and belongs to no region.
    """
    spans = [token.map for token in selected if token.map is not None]
    for token in tokens:
        if token.map is None:
            continue
        if any(start <= token.map[0] < end for start, end in spans):
            yield token


def inlines(tokens: Sequence[Token], selected: Sequence[Token]) -> Iterator[Token]:
    """Each inline token the given regions of one document carry, in source order."""
    return (token for token in within(tokens, selected) if token.type == INLINE)


def uses(tokens: Sequence[Token], selected: Sequence[Token]) -> Iterator[Use]:
    """Every reference use the given regions of one source carry, in source order.

    A use is what the parser read as one, so an apparent link inside a
    code span or a code block is text the document carries and is none
    of these. A link names whatever its destination resolves to and an
    image names a resource, and each carries the opening its own
    content begins with, so a mark is read from the use that was
    written. The line is the line of this content the use's own block
    opens on, which is as near the use as the parser records a
    position.
    """
    for token in inlines(tokens, selected):
        line = None if token.map is None else token.map[0] + 1
        for children, at, child in events(token.children or []):
            if child.type == LINK_OPEN:
                destination = child.attrGet(HREF)
                yield Use(
                    "" if destination is None else str(destination),
                    opening_text(children, at),
                    line,
                    resource=False,
                )
            else:
                destination = child.attrGet(SRC)
                yield Use(
                    "" if destination is None else str(destination),
                    alternative_text(child),
                    line,
                    resource=True,
                )


def events(
    children: Sequence[Token],
) -> Iterator[tuple[Sequence[Token], int, Token]]:
    """Each reference use one run of inline events carries, in written order.

    A use arrives with the run that carries it and its position in that
    run, because what a use opens with is the event following it.

    An image's alternative content is a run of its own, so the walk
    descends into it where the image sits and a use written there is
    read where a use written beside the image is. This is the one walk
    over a run of inline events, so discovery, the budget, the
    emission and the candidate comparison each read the same uses in
    the same order.
    """
    for at, child in enumerate(children):
        if child.type in REFERENCE_USES:
            yield children, at, child
        if child.type == IMAGE:
            yield from events(child.children or [])


def occurrences(tokens: Sequence[Token], selected: Sequence[Token]) -> int:
    """How many link and image uses the given regions of one source carry.

    A budget over references is declared over what an author wrote, so
    the count is of occurrences in the source rather than of the
    documents they reach: one document named five times is five
    occurrences, and an image is one of them because opening a resource
    costs what opening a document costs. A use written inside an
    image's alternative content is one the author wrote, so it is
    counted where it sits.
    """
    return sum(
        1 for token in inlines(tokens, selected) for _ in events(token.children or [])
    )


def nesting(tokens: Sequence[Token]) -> int:
    """The deepest run of container blocks one complete source nests.

    A container block is a block quote or a list item, which is what
    CommonMark calls one: a list is how its items are grouped rather
    than a level of its own, so three nested bullets nest three deep.
    The count is over the complete opened source, because a parser
    indexes the whole document however narrow the requested section is.
    """
    depth = 0
    deepest = 0
    for token in tokens:
        if token.type in CONTAINER_OPEN:
            depth += 1
            deepest = max(deepest, depth)
        elif token.type in CONTAINER_CLOSE:
            depth -= 1
    return deepest


@dataclass(frozen=True)
class Selection:
    """What one source contributes to the bundle.

    The regions are the document-level blocks the run selected, in
    source order.
    """

    regions: tuple[Token, ...]
