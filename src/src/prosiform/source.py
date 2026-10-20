"""One source document: the content it carries, and the headings that name it.

A file holds two things the author did not write as instructions: a
leading byte-order mark, which is a text-file convention, and a leading
frontmatter block, which is metadata for whatever reads the file. Neither
is content, and both would otherwise be published as body. The scan below
removes them before anything parses the document.

The scan is deterministic and reads nothing it removes. It parses no
YAML, interprets no metadata and executes nothing: it compares two
physical lines against two literals, and the narrowness of that
comparison is the whole of the policy. An indented delimiter, a delimiter
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

The fragment is the one a renderer generates: the visible text lowered,
the characters the renderer discards removed, and each remaining space
a hyphen. Where a slug is already taken the renderer numbers the
heading apart, counting from one and passing over every ordinal
something already carries, so a heading whose own text spells an
ordinal takes that ordinal from the heading that would otherwise have
been numbered into it. The count is kept per complete source document,
so a heading's fragment follows from the document that carries it
rather than from anything bundled beside it.

Every heading the profile recognizes is indexed, a container-nested one
included: eligibility to be selected is a later decision, and a heading
left out of the index would change the fragment of every heading after
it that shares its slug.

A link is read from the same events. What a document requires is
written in its links, so the model reports each link a given run of
regions carries: where it points, the literal text its content opens
on, and the line of its block. A link inside a code span or a code
block is an example rather than a link and the parser produces none,
and an image is a reference to a resource rather than to a document,
so neither reaches a caller asking what this content links to.

That later decision is the section below. A document is a run of
maximal regions, each a block the document itself carries, and a
container is one region whatever it holds. Only a heading that is such
a region roots a section: it is the heading a reader finds at the
document's own level, and the blocks following it belong to it until
the document returns to that level or above. A heading a container
carries is therefore neither a root nor a boundary — it sits inside one
region, so the region it sits in is what the document holds there — and
a fragment naming one names a section the model does not have.
"""

import re
from collections.abc import Iterator, Sequence
from dataclasses import dataclass

from markdown_it.token import Token

ENCODING = "utf-8"
MARK = "﻿"

OPENER = "---"
CLOSERS = ("---", "...")

LINE_FEED = "\n"
CARRIAGE_RETURN = "\r"

PHYSICAL_LINE = re.compile(r"[^\n]*\n|[^\n]+")

UNTERMINATED_FRONTMATTER = "E_UNTERMINATED_FRONTMATTER"
NESTED_SECTION_TARGET = "E_NESTED_SECTION_TARGET"

HEADING_OPEN = "heading_open"
INLINE = "inline"
TEXT = "text"
CODE_INLINE = "code_inline"
LINK_OPEN = "link_open"
HREF = "href"
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

    def line(self, at: int | None) -> int | None:
        """The line of the original file one line of this content occupies."""
        return None if at is None else at + self.first_line - 1


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


def decode(data: bytes) -> str:
    """One source's bytes as text, which they are only if they are valid UTF-8.

    The strict error handler is the one that raises. Substituting a
    replacement character would put a byte the author never wrote into
    content the tool promises to preserve, and then report success.
    """
    return data.decode(ENCODING)


def content(text: str) -> Source:
    """One source's content, its leading transport metadata removed.

    Exactly one byte-order mark is removed, and a second is content. The
    frontmatter opener is the first physical line where that line is the
    three characters of `OPENER`; the block closes at the next physical
    line equal to one of `CLOSERS`, and the opener, the metadata, the
    closer and the closer's terminator go together.
    """
    body = text.removeprefix(MARK)
    physical = lines(body)
    if not physical or bare(physical[0]) != OPENER:
        return Source(body)
    for index, line in enumerate(physical[1:], start=1):
        if bare(line) in CLOSERS:
            return Source("".join(physical[index + 1 :]), index + 2)
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
    """The fragment of each heading, in the order a renderer reads them.

    The first heading to carry a slug takes it, and a later one takes
    the slug and an ordinal, counting from one. An ordinal something
    already carries is passed over, so a heading whose own text spells
    one keeps it and the heading that would have been numbered into it
    takes the next free ordinal instead. Two headings therefore never
    share a fragment.

    This is the renderer's own rule, and the counts it keeps belong to
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
    """One source heading: its level, the text it shows and the fragment it takes."""

    level: int
    text: str
    fragment: str
    line: int | None


def index(tokens: Sequence[Token]) -> tuple[Heading, ...]:
    """Every heading one complete source document carries, in source order."""
    carried = list(headings(tokens))
    shown_texts = [visible(inline) for _, inline in carried]
    return tuple(
        Heading(
            level=level(opening),
            text=text,
            fragment=fragment,
            line=None if opening.map is None else opening.map[0] + 1,
        )
        for (opening, _), text, fragment in zip(
            carried, shown_texts, fragments(shown_texts), strict=True
        )
    )


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
    reported as the reference to nothing it is. A fragment naming a
    container-nested heading names a heading the document carries and a
    section it does not, which is the refusal `Nested` raises.
    """
    carried = [opening for opening, _ in headings(tokens)]
    named = index(tokens)
    at = next(
        (one for one, each in enumerate(named) if each.fragment == fragment), None
    )
    if at is None:
        return None
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
class Link:
    """One link a source carries, read from the events the parser produced.

    The destination is the one the parser resolved, so a reference-style
    use and an inline one arrive the same way and a Markdown escape has
    already been read. The opening is the literal text the link's
    content begins with, which is where a dependency's mark is written:
    a link whose content opens on a code span, an emphasis or an image
    begins with no text and opens with nothing.
    """

    destination: str
    opening: str
    line: int | None


def opening_text(children: Sequence[Token], at: int) -> str:
    """The literal text the link opened at one position begins with."""
    following = children[at + 1] if at + 1 < len(children) else None
    if following is None or following.type != TEXT:
        return ""
    return following.content


def inlines(tokens: Sequence[Token], selected: Sequence[Token]) -> Iterator[Token]:
    """Each inline token the given regions of one document carry, in source order."""
    spans = [token.map for token in selected if token.map is not None]
    for token in tokens:
        if token.type != INLINE or token.map is None:
            continue
        if any(start <= token.map[0] < end for start, end in spans):
            yield token


def links(tokens: Sequence[Token], selected: Sequence[Token]) -> Iterator[Link]:
    """Every link the given regions of one source carry, in source order.

    A link is what the parser read as one, so an apparent link inside a
    code span or a code block is text the document carries and is not
    one of these, and an image names a resource rather than a document
    and is not one either. The line is the line of this content the
    link's own block opens on, which is as near the link as the parser
    records a position.
    """
    for token in inlines(tokens, selected):
        children = token.children or []
        for at, child in enumerate(children):
            if child.type != LINK_OPEN:
                continue
            destination = child.attrGet(HREF)
            yield Link(
                "" if destination is None else str(destination),
                opening_text(children, at),
                None if token.map is None else token.map[0] + 1,
            )


@dataclass(frozen=True)
class Selection:
    """What one source contributes to the bundle, and what named it.

    The regions are the document-level blocks the run selected, in
    source order. The named headings are the ones an entry reference
    resolved to, which is what the entry line links and what the bundle
    keeps identifiable.
    """

    regions: tuple[Token, ...]
    named: tuple[Token, ...]
