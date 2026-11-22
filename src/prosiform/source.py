"""Model source content, headings, selections and reference occurrences.

`content` reads the document body and metadata, `index` records its
headings, and `section` selects its regions. `uses` enumerates references;
`Click` describes diagram-link fields and `linking` caches their read.
"""

import hashlib
import json
import re
from bisect import bisect_right
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from itertools import pairwise

from markdown_it.token import Token
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError
from ruamel.yaml.nodes import MappingNode
from ruamel.yaml.tokens import (
    AliasToken,
    FlowMappingEndToken,
    FlowMappingStartToken,
    FlowSequenceEndToken,
    FlowSequenceStartToken,
    ScalarToken,
    ValueToken,
)

from prosiform.limits import FILE_BYTES, NESTING
from prosiform.metadata import (
    INVALID_CONVERSION_METADATA,
    INVALID_FRONTMATTER,
    Conversion,
)
from prosiform.metadata import decode as decode_metadata
from prosiform.tags import read as read_tags

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
FENCE = "fence"
DIAGRAM = "mermaid"
QUOTED = (
    r'"(?P<destination>[^"]*)"(?:\s+"(?P<tooltip>[^"]*)")?'
    r"(?:\s+(?:_self|_blank|_parent|_top))?\s*;?\s*"
)
CLICK_LINE = re.compile(
    rf'\s*click\s+(?P<node>[^\s"]+)\s+(?:href\s+)?{QUOTED}', re.IGNORECASE
)
GANTT_CLICK = re.compile(r'\s*click\s+[^\s"]+\s+href\s+"[^"]*"\s*', re.IGNORECASE)
CLASS_LINK = re.compile(rf'\s*link\s+(?P<node>[^\s"]+)\s+{QUOTED}', re.IGNORECASE)
CLICK_STATEMENT = re.compile(r"\s*click\s", re.IGNORECASE)
CLASS_STATEMENT = re.compile(r"\s*(?:link|callback)\s", re.IGNORECASE)
QUOTE = '"'
MENU_ENTRY = re.compile(r"\s*link\s+[^:]+:", re.IGNORECASE)
MENU = re.compile(r"\s*links\s+[^:]+:", re.IGNORECASE)
ENTRY_SEPARATOR = "@"
ANCHOR = "#"
ENTITY_ANCHOR = "#35;"
ENTITY = re.compile(r"#[A-Za-z0-9_]+;")
STATEMENT_END = ";"
JSON_SPACE = " \t\r\n"
JSON_STRING = re.compile(r'"(?:[^"\\]|\\.)*"')
JSON_OPEN = "{["
JSON_CLOSE = "}]"
JSON_MEMBER_END = ",}"
FRONT_MATTER = re.compile(
    r"^([^\S\n\r]*)-{3}\s*[\n\r](.*?)[\n\r]\1-{3}\s*[\n\r]+", re.DOTALL
)
DIRECTIVE = re.compile(
    r"%{2}{\s*(?:(\w+)\s*:|(\w+))\s*(?:(\w+)|((?:(?!}%{2}).|\r?\n)*))?\s*(?:}%{2})?",
    re.IGNORECASE,
)
COMMENT = re.compile(r"\s*%%.*\n")
CLASS_DIAGRAM = "classDiagram"
FLOWCHARTS = ("flowchart", "graph")
SHAPES = {
    "(((": (")))",),
    "((": ("))",),
    "([": ("])",),
    "(-": ("-)",),
    "[[": ("]]",),
    "[(": (")]",),
    "[/": ("/]", "\\]"),
    "[\\": ("\\]", "/]"),
    "{{": ("}}",),
    "@{": ("}",),
    "[": ("]",),
    "(": (")",),
    "{": ("}",),
    ">": ("]",),
}
NODE_SHAPE = re.compile(
    r"(?<!\w)(?<!\w-)(?P<node>\w+(?:-\w+)*)(?P<open>"
    + "|".join(re.escape(opener) for opener in SHAPES)
    + ")"
)
METADATA_SHAPE = "@{"
LABEL = "label"
EDGE_TEXT = "|"
EDGE = ("-", "=")
EDGE_ENDS = "ox"
MARKDOWN_STRING = "`"
CLASS_LABEL = re.compile(r'\s*class\s+(?P<node>[^\s"\[]+)\["(?P<label>[^"]*)"\]')
SEQUENCE_DIAGRAM = "sequenceDiagram"
KANBAN = "kanban"
GANTT = "gantt"
DIAGRAM_TYPES = (CLASS_DIAGRAM, SEQUENCE_DIAGRAM, KANBAN, GANTT)
TEXT_LABELS = (
    SEQUENCE_DIAGRAM,
    "pie",
    "timeline",
    "journey",
    "gantt",
    "quadrantChart",
    "gitGraph",
    "xychart",
    "sankey",
    "packet",
    "radar",
    "treemap",
    "C4",
)
INITIALIZING = ("init", "initialize")
CONFIG = "config"
TICKET_BASE_URL = "ticketBaseUrl"
TICKET_PLACEHOLDER = "#TICKET#"
TICKET = "ticket"
NODE_METADATA = re.compile(r"@(\{.*\})\s*$")
HTML_ANCHOR = re.compile(
    r"<a\s[^>]*?\bhref\s*=\s*(?:\"(?P<double>[^\"]*)\"|'(?P<single>[^']*)'|(?P<bare>[^\s>]+))",
    re.IGNORECASE,
)
COMMENT_LINE = re.compile(r"\s*%%")
KANBAN_TICKET = "Kanban ticket's link"
LABEL_ANCHOR = "HTML anchor in a label"
AUTHORITY = "//"
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]+:")
DIAGRAM_READ = "diagram links"
TEXT = "text"
CODE_INLINE = "code_inline"
LINK_OPEN = "link_open"
LINK_CLOSE = "link_close"
AUTOLINK = "autolink"
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

    def line(self, at: int | None) -> int | None:
        """The line of the original file one line of this content occupies."""
        return None if at is None else at + self.first_line - 1


@dataclass(frozen=True)
class Capture:
    """One source read's identity and evidence.

    `identity` is its canonical path, `digest` its content hash, `chain`
    the dependency chain, and `walk` its lexical path. `directories` records
    directory identities; `file_identity` and `size` record the opened file.
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


def frontmatter(text: str) -> tuple[tuple[int, int], int] | None:
    """Where one document's frontmatter payload sits, or nothing where none opens.

    Exactly one byte-order mark is passed over, and a second is content.
    The opener is the first physical line where that line is the three
    characters of `OPENER`; the block closes at the next physical line
    equal to one of `CLOSERS`. The answer is the payload's half-open
    byte span in the text's encoding, delimiters excluded, and the index
    of the closer among the physical lines after the mark. An opener no
    later line closes is `Unterminated`.
    """
    body = text.removeprefix(MARK)
    physical = lines(body)
    if not physical or bare(physical[0]) != OPENER:
        return None
    start = len((text[: len(text) - len(body)] + physical[0]).encode(ENCODING))
    end = start
    for index, line in enumerate(physical[1:], start=1):
        if bare(line) in CLOSERS:
            return (start, end), index
        end += len(line.encode(ENCODING))
    raise Unterminated(1)


def closes_head(index: int, line: bytes) -> bool:
    """Whether a byte line completes the head needed by `frontmatter`.

    Delimiter recognition follows `frontmatter`. Invalid UTF-8 also stops
    the probe, so `decode` can report the captured text's encoding error.
    """
    try:
        text = line.decode(ENCODING)
    except UnicodeDecodeError:
        return True
    if index == 0:
        return bare(text.removeprefix(MARK)) != OPENER
    return bare(text) in CLOSERS


def declaration(
    text: str,
    *,
    file: str = "",
    max_bytes: int = FILE_BYTES.default,
    max_depth: int = NESTING.default,
) -> Conversion:
    """Decode conversion settings from a captured document head.

    `frontmatter` supplies the payload span and `metadata.decode` validates
    it within `max_bytes` and `max_depth`, using `file` in diagnostics.
    """
    found = frontmatter(text)
    return decode_metadata(
        text.encode(ENCODING),
        file=file,
        span=None if found is None else found[0],
        max_bytes=max_bytes,
        max_depth=max_depth,
    )


def content(
    text: str,
    *,
    file: str = "",
    max_bytes: int = FILE_BYTES.default,
    max_depth: int = NESTING.default,
) -> Source:
    """Return the body, original starting line and conversion settings.

    One leading byte-order mark is removed. Where `frontmatter` finds a
    block, its delimiters, payload and closing line terminator are removed
    together. `metadata.decode` validates the payload within the given bounds.
    """
    raw = text.encode(ENCODING)
    body = text.removeprefix(MARK)
    found = frontmatter(text)
    conversion = decode_metadata(
        raw,
        file=file,
        span=None if found is None else found[0],
        max_bytes=max_bytes,
        max_depth=max_depth,
    )
    if found is None:
        return Source(body, conversion=conversion)
    _span, closer = found
    return Source("".join(lines(body)[closer + 1 :]), closer + 2, conversion)


def visible(inline: Token) -> str:
    """The text an inline token shows, which is what its fragment comes from."""
    return "".join(shown(child) for child in inline.children or [])


def shown(child: Token) -> str:
    """Return the visible characters one inline event contributes.

    Text and code supply their content, and a soft or hard break supplies
    a line feed. Formatting events, HTML and images contribute no text.
    """
    if child.type in (TEXT, CODE_INLINE):
        return child.content
    if child.type in BREAKS:
        return LINE_FEED
    return ""


def slug(text: str) -> str:
    """Derive a heading slug by lowercasing, discarding punctuation and controls,
    then replacing each remaining space with a hyphen.
    """
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


def runs(tokens: Sequence[Token]) -> dict[int, Sequence[Token]]:
    """Map each `regions` opening's identity to its run of tokens.

    Each run ends where the next region opens. `within` selects tokens
    when a caller holds the whole document rather than these indexed runs.
    """
    opening = {id(token) for token in regions(tokens)}
    opened = [at for at, token in enumerate(tokens) if id(token) in opening]
    return {
        id(tokens[start]): tokens[start:end]
        for start, end in pairwise([*opened, len(tokens)])
    }


def opens(tokens: Sequence[Token], opening: Token) -> int | None:
    """Where one token opens a region of this document, by position in its run.

    Tokens are compared by identity. Two headings carrying one text and
    one level are equal as values, so a comparison by value would place
    the first of them wherever the second occurs.
    """
    return next((at for at, token in enumerate(tokens) if token is opening), None)


def section(tokens: Sequence[Token], fragment: str) -> tuple[Token, ...] | None:
    """Return the document regions selected by a source fragment.

    The fragment must match exactly one heading produced by `index`.
    Multiple matches raise `Ambiguous` before section eligibility is tested;
    no match returns None. A match outside `regions` raises `Nested`.
    The selected run ends at the next document-level heading of equal or
    higher level, or at the end of the document.
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
    """One reference occurrence and its source context.

    `destination` is the parsed target; `opening` is its opening text;
    `name` identifies the use in diagnostics, and `line` locates it.
    `resource` identifies a resource occurrence. `title` and `heading`
    record its containing section's text and line. `label` holds its plain
    label where available, and `tags` holds its selected preset names.
    """

    destination: str
    opening: str
    name: str
    line: int | None
    resource: bool
    title: str | None = None
    label: str | None = None
    heading: int | None = None
    tags: frozenset[str] = frozenset()


def opening_text(children: Sequence[Token], at: int) -> str:
    """Return the text event immediately following a link opening, or empty text.

    A code span, formatting delimiter or image at that position contributes
    no opening text.
    """
    following = children[at + 1] if at + 1 < len(children) else None
    if following is None or following.type != TEXT:
        return ""
    return following.content


def plain_label(children: Sequence[Token], at: int) -> str | None:
    """Return a link's complete label when it contains text events alone.

    An autolink, an incomplete link or a label containing any other event
    returns None. Entity and escape decoding belongs to `profile.parse`.
    """
    opening = children[at]
    if opening.markup == AUTOLINK:
        return None
    held: list[str] = []
    for child in children[at + 1 :]:
        if child.type == LINK_CLOSE:
            return "".join(held)
        if child.type != TEXT:
            return None
        held.append(child.content)
    return None


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
        line = token.map[0]
        for start, end in spans:
            if start <= line < end:
                yield token
                break


def inlines(tokens: Sequence[Token], selected: Sequence[Token]) -> Iterator[Token]:
    """Each inline token the given regions of one document carry, in source order."""
    return (token for token in within(tokens, selected) if token.type == INLINE)


@dataclass(frozen=True)
class Click:
    """One diagram-link destination and its source fields.

    `destination` is the decoded target; `written` is its source spelling,
    `line` its source-content line and `offset` its first character in the
    fence line. `anchor` is the fragment marker's spelling for that form.
    `node` identifies the linked element. `opening` is that element's text,
    which supplies its operator marks; an element with no text has an empty
    opening. `title` is the quoted tooltip, which supplies preset tags,
    or None where absent. A sequence menu has no element text or tooltip.
    `name` is the diagnostic name: keyword and node, or empty for a menu.
    """

    destination: str
    line: int
    offset: int
    anchor: str
    written: str
    node: str = ""
    opening: str = ""
    title: str | None = None
    name: str = ""


@dataclass(frozen=True)
class ElementText:
    """One diagram element's label and its position in a statement.

    `node` identifies the element, `text` holds its decoded label, and
    `offset` and `written` locate its source span. `scalar` identifies a
    span containing metadata for `label_span` to read.
    """

    node: str
    text: str
    offset: int
    written: str
    scalar: bool = False


@dataclass(frozen=True)
class Unfollowed:
    """One rendered link outside the supported diagram-link forms.

    `form` names its kind, `destination` is its rendered URL, and `line`
    locates its source content.
    """

    form: str
    destination: str
    line: int


@dataclass(frozen=True)
class Diagram:
    """The links and malformed constructs found in one diagram.

    `clicks` holds `Click` records in source order; `broken` and `listed`
    hold malformed-menu lines. `unfollowed` holds `Unfollowed` records;
    `unparsed` holds unsupported Gantt clicks. `repeated` pairs the first
    and each subsequent link to one element.
    """

    clicks: tuple[Click, ...] = ()
    broken: tuple[int, ...] = ()
    listed: tuple[int, ...] = ()
    unfollowed: tuple[Unfollowed, ...] = ()
    unparsed: tuple[Click, ...] = ()
    repeated: tuple[tuple[Click, Click], ...] = ()


class BrokenMenu(Exception):
    """A `links` object one of whose values is no string."""


class ListedMenu(Exception):
    """A `links` value that is a non-empty array."""


def diagram(fence: Token) -> bool:
    """Whether one fence holds a Mermaid diagram, as its info string opens."""
    return fence.info.split(maxsplit=1)[:1] == [DIAGRAM]


def diagram_type(content: str) -> str:
    """Return the declared type where it has a distinct link grammar.

    `diagram_opening` supplies the declaration text; types outside
    `DIAGRAM_TYPES` return an empty string.
    """
    opening = diagram_opening(content)
    return next((one for one in DIAGRAM_TYPES if opening.startswith(one)), "")


def draws_anchors(content: str) -> bool:
    """Whether one diagram draws an HTML anchor its label text writes.

    A diagram whose labels Mermaid draws as HTML draws an anchor written
    in one. A sequence, pie, timeline, journey, Gantt, quadrant, Git,
    XY, Sankey, packet, radar, treemap or C4 diagram draws its label
    text as SVG text, so an anchor written there shows as the characters
    it is written in. Every other diagram is held to draw one.
    """
    return not diagram_opening(content).startswith(TEXT_LABELS)


def diagram_opening(content: str) -> str:
    """One diagram's text from the word that declares its type.

    Mermaid sets aside a leading front matter block, every directive and
    every comment line before reading that word.
    """
    text = FRONT_MATTER.sub("", content, count=1)
    return COMMENT.sub(LINE_FEED, DIRECTIVE.sub("", text)).lstrip()


def clicks(fence: Token) -> tuple[Click, ...]:
    """Return the `Click` records from the fence read cached by `linking`."""
    return linking(fence).clicks


def linking(fence: Token) -> Diagram:
    """What one fence's diagram links to, read once for the fence.

    The read is kept on the fence's token, so discovery, the budget, the
    refusals, emission and candidate validation each take the read the
    first of them made rather than reading the diagram again.
    """
    held = fence.meta.get(DIAGRAM_READ)
    if not isinstance(held, Diagram):
        held = read_diagram(fence)
        fence.meta[DIAGRAM_READ] = held
    return held


def read_diagram(fence: Token) -> Diagram:
    """Build a diagram's `Click` records and collect malformed constructs.

    `linked` reads destinations, `element_texts` supplies labels, and
    `rendered` finds other rendered links. Each `#35;` in a sequence-menu
    destination decodes to `#`. A node takes the last label `element_texts`
    yields for it. Gantt forms outside `GANTT_CLICK` are recorded as
    unparsed; subsequent links to one element are paired with its first.
    Broken and listed menus are recorded at their source-content lines.
    """
    if fence.map is None or not diagram(fence):
        return Diagram()
    form = diagram_type(fence.content)
    base = ticket_base(fence.content) if form == KANBAN else None
    anchors = draws_anchors(fence.content)
    texts = {one.node: one.text for _, one in element_texts(fence.content, form)}
    first = fence.map[0] + 2
    found: list[Click] = []
    broken: list[int] = []
    listed: list[int] = []
    unfollowed: list[Unfollowed] = []
    unparsed: list[Click] = []
    linked_at: dict[str, Click] = {}
    repeated: list[tuple[Click, Click]] = []
    for at, physical in enumerate(lines(fence.content)):
        line = bare(physical)
        unfollowed.extend(rendered(line, form, base, anchors, first + at))
        try:
            named = linked(line, form)
        except BrokenMenu:
            broken.append(first + at)
            continue
        except ListedMenu:
            listed.append(first + at)
            continue
        for written, offset, anchor, node, tip, name, gantt_form in named:
            destination = (
                written.replace(ENTITY_ANCHOR, ANCHOR)
                if anchor == ENTITY_ANCHOR
                else written
            )
            click = Click(
                destination,
                first + at,
                offset,
                anchor,
                written,
                node,
                texts.get(node, ""),
                tip,
                name,
            )
            if form == GANTT and not gantt_form:
                unparsed.append(click)
                continue
            found.append(click)
            if node:
                earlier = linked_at.setdefault(node, click)
                if earlier is not click:
                    repeated.append((earlier, click))
    return Diagram(
        tuple(found),
        tuple(broken),
        tuple(listed),
        tuple(unfollowed),
        tuple(unparsed),
        tuple(repeated),
    )


def element_texts(content: str, form: str) -> Iterator[tuple[int, ElementText]]:
    """Each flowchart or class label, its content line and its source span.

    Labels are yielded in written order. Shape text is read by shape_text;
    class declarations expose the text inside their label quotes.
    """
    if form != CLASS_DIAGRAM and not diagram_opening(content).startswith(FLOWCHARTS):
        return
    for line, physical in enumerate(lines(content)):
        if COMMENT_LINE.match(physical):
            continue
        for statement, start in statements(bare(physical)):
            if form == CLASS_DIAGRAM:
                found = CLASS_LABEL.match(statement)
                if found is not None:
                    text = found.group("label")
                    yield (
                        line,
                        ElementText(
                            found.group("node"),
                            text,
                            start + found.start("label"),
                            text,
                        ),
                    )
            elif not CLICK_STATEMENT.match(statement):
                for one in shaped(statement):
                    yield (
                        line,
                        ElementText(
                            one.node,
                            one.text,
                            start + one.offset,
                            one.written,
                            one.scalar,
                        ),
                    )


def shaped(statement: str) -> Iterator[ElementText]:
    """Each flowchart shape's node, text and source span within one statement.

    Quoted strings and edge text outside shapes carry no node. An edge
    ending in a circle or cross addresses the following node name.
    """
    at = 0
    while at < len(statement):
        character = statement[at]
        if character in (QUOTE, EDGE_TEXT):
            close = statement.find(character, at + 1)
            at = len(statement) if close < 0 else close + 1
            continue
        found = NODE_SHAPE.match(statement, at)
        if found is None:
            at += 1
            continue
        node = found.group("node")
        if node[0] in EDGE_ENDS and len(node) > 1 and statement[:at].endswith(EDGE):
            node = node[1:]
        text, at = shape_text(statement, found.end(), found.group("open"))
        if text is not None:
            scalar = found.group("open") == METADATA_SHAPE
            offset = (
                found.end() - 1 if scalar else statement.index(text, found.end(), at)
            )
            written = statement[offset:at] if scalar else text
            yield ElementText(node, text, offset, written, scalar)


def label_span(label: ElementText) -> tuple[int, str]:
    """The label value's offset and spelling inside one element's statement.

    Metadata keys are resolved by YAML composition. The corresponding
    top-level value token locates the scalar or alias as it is written,
    excluding an anchor or tag that belongs to that value.
    """
    if not label.scalar:
        return label.offset, label.written
    parser = YAML(typ="safe", pure=True)
    mapping = parser.compose(label.written)
    assert isinstance(mapping, MappingNode)
    entry = next(i for i, (key, _) in enumerate(mapping.value) if key.value == LABEL)
    depth, value = 0, -1
    taking = False
    for token in parser.scan(label.written):
        if isinstance(token, (FlowMappingStartToken, FlowSequenceStartToken)):
            depth += 1
        elif isinstance(token, (FlowMappingEndToken, FlowSequenceEndToken)):
            depth -= 1
        elif depth == 1 and isinstance(token, ValueToken):
            value += 1
            taking = value == entry
        elif taking and isinstance(token, (ScalarToken, AliasToken)):
            assert token.start_mark is not None and token.end_mark is not None
            start, end = token.start_mark.index, token.end_mark.index
            return label.offset + start, label.written[start:end]
    raise AssertionError("a metadata label has a scalar or alias value token")


def shape_text(statement: str, start: int, opener: str) -> tuple[str | None, int]:
    """The text one shape writes from its opening, and where the shape ends.

    A metadata shape writes the `label` its mapping holds, and none where
    it holds no label.
    """
    closers = SHAPES[opener]
    if opener == METADATA_SHAPE:
        close = statement.find(closers[0], start)
        end = len(statement) if close < 0 else close + 1
        label = yaml_mapping(statement[start - 1 : end]).get(LABEL)
        return (None if label is None else str(label)), end
    text_end = start
    if statement.startswith(QUOTE, start):
        close = statement.find(QUOTE, start + 1)
        text_end = len(statement) if close < 0 else close + 1
    found = [
        (at, at + len(closer))
        for closer in closers
        if (at := statement.find(closer, text_end)) >= 0
    ]
    close, end = min(found) if found else (len(statement), len(statement))
    text = statement[start:close]
    if text.startswith(QUOTE):
        text = text.strip().removeprefix(QUOTE).removesuffix(QUOTE)
        if len(text) > 1 and text[0] == text[-1] == MARKDOWN_STRING:
            text = text[1:-1]
    return text, end


def rendered(
    line: str, form: str, base: str | None, anchors: bool, at: int
) -> Iterator[Unfollowed]:
    """Each link one diagram line renders that no diagram link line writes.

    A comment line renders nothing. A line writing a ticket in a Kanban
    diagram whose ticket base URL is `base` renders the link Mermaid
    builds from them. In a diagram that draws anchors, each HTML anchor
    a statement of the line writes renders its `href`, except in a
    `click` statement or a class diagram's `link` or `callback`
    statement: the only text those carry is a destination and a tooltip,
    and Mermaid shows a tooltip on hover as a box that takes no pointer,
    so an anchor there opens nothing.
    """
    if COMMENT_LINE.match(line):
        return
    if base:
        ticket = ticket_of(line)
        if ticket:
            destination = base.replace(TICKET_PLACEHOLDER, ticket, 1)
            yield Unfollowed(KANBAN_TICKET, destination, at)
    if not anchors:
        return
    for statement, _start in statements(line):
        if CLICK_STATEMENT.match(statement) or (
            form == CLASS_DIAGRAM and CLASS_STATEMENT.match(statement)
        ):
            continue
        for anchor in HTML_ANCHOR.finditer(statement):
            destination = next(g for g in anchor.groups() if g is not None)
            yield Unfollowed(LABEL_ANCHOR, destination, at)


def statements(line: str) -> list[tuple[str, int]]:
    """Each statement one diagram line holds, with where it starts in the line.

    Mermaid ends a statement at a `;` outside a double-quoted string, so
    a `;` a destination or a label quotes is the statement's own text.
    """
    found = []
    start = 0
    quoted = False
    for at, character in enumerate(line):
        if character == QUOTE:
            quoted = not quoted
        elif character == STATEMENT_END and not quoted:
            found.append((line[start:at], start))
            start = at + 1
    found.append((line[start:], start))
    return found


def yaml_mapping(text: str) -> dict[object, object]:
    """One YAML text as the mapping it holds, or an empty one where it holds none."""
    try:
        loaded = YAML(typ="safe", pure=True).load(text)
    except YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def ticket_base(content: str) -> str | None:
    """The `ticketBaseUrl` one Kanban diagram's own configuration sets.

    Mermaid reads it from the front matter's `config` mapping, and an
    `init` directive's configuration replaces it, so the last
    directive setting it decides.
    """
    base: object = None
    matter = FRONT_MATTER.match(content)
    if matter is not None:
        base = configured(yaml_mapping(matter.group(2)).get(CONFIG))
    for directive in DIRECTIVE.finditer(content):
        kind = directive.group(1) or directive.group(2) or ""
        if kind.lower() not in INITIALIZING or directive.group(4) is None:
            continue
        set_here = configured(yaml_mapping(directive.group(4)))
        if set_here is not None:
            base = set_here
    return base if isinstance(base, str) else None


def configured(configuration: object) -> object:
    """The `ticketBaseUrl` one Mermaid configuration mapping sets, if any."""
    if not isinstance(configuration, dict):
        return None
    kanban = configuration.get(KANBAN)
    return kanban.get(TICKET_BASE_URL) if isinstance(kanban, dict) else None


def ticket_of(line: str) -> str | None:
    """The ticket one Kanban node line's metadata names, if it names one."""
    metadata = NODE_METADATA.search(line)
    if metadata is None:
        return None
    ticket = yaml_mapping(metadata.group(1)).get(TICKET)
    return None if ticket is None or ticket == "" else str(ticket)


def external(path: str) -> bool:
    """Whether a reference carries a scheme or an authority."""
    return path.startswith(AUTHORITY) or SCHEME.match(path) is not None


def linked(
    line: str, form: str
) -> list[tuple[str, int, str, str, str | None, str, bool]]:
    """Return one line's destinations in written order, with their source fields.

    Keywords match case-insensitively. A quoted destination follows
    `click <node>`, with optional `href`, or a class diagram's `link <class>`.
    It may be followed by a quoted tooltip and a link target. Callback
    and `call` forms supply no destination. `statements` separates the
    statements read from a line.

    In sequence diagrams, `link <actor>: <label> @ <destination>` supplies
    the trimmed text after its first `@`, and `links <actor>: {…}` supplies
    the menu destinations `entries` reads.
    Each result carries its offset, fragment-marker spelling, node, tooltip,
    diagnostic name and whether the full line matches `GANTT_CLICK`.
    The assembled diagram-link fields are described by `Click`.
    """
    found = []
    for statement, start in statements(line):
        quoted = CLICK_LINE.fullmatch(statement)
        if quoted is None and form == CLASS_DIAGRAM:
            quoted = CLASS_LINK.fullmatch(statement)
        if quoted is not None:
            offset = start + quoted.start("destination")
            found.append(
                (
                    quoted.group("destination"),
                    offset,
                    ANCHOR,
                    quoted.group("node"),
                    quoted.group("tooltip"),
                    f"{statement.split(maxsplit=1)[0]} {quoted.group('node')}",
                    GANTT_CLICK.fullmatch(line) is not None,
                )
            )
    if found or form != SEQUENCE_DIAGRAM:
        return found
    entry = MENU_ENTRY.match(line)
    if entry is not None:
        end = statement_end(line, entry.end())
        at = line.find(ENTRY_SEPARATOR, entry.end(), end)
        if at < 0:
            return []
        start, stop = trimmed(line, at + 1, end)
        if start == stop:
            return []
        return [(line[start:stop], start, ENTITY_ANCHOR, "", None, "", False)]
    menu = MENU.match(line)
    if menu is None:
        return []
    start, stop = trimmed(line, menu.end(), statement_end(line, menu.end()))
    return [
        (value, offset, ENTITY_ANCHOR, "", None, "", False)
        for value, offset in entries(line, start, stop)
    ]


def statement_end(line: str, at: int) -> int:
    """Where a sequence statement's text begun at `at` ends.

    Mermaid's sequence lexer ends the text at a `;`, which closes the
    statement, or a `#`, which opens a comment. Mermaid first replaces
    every entity, `#<word>;`, with a placeholder, so neither the `#` nor
    the `;` of an entity ends anything.
    """
    while at < len(line):
        if line[at] == ANCHOR:
            entity = ENTITY.match(line, at)
            if entity is None:
                return at
            at = entity.end()
        elif line[at] == STATEMENT_END:
            return at
        else:
            at += 1
    return len(line)


def trimmed(line: str, start: int, end: int) -> tuple[int, int]:
    """The span `start` to `end` of a line with its surrounding whitespace left out."""
    text = line[start:end]
    begin = start + len(text) - len(text.lstrip())
    return begin, max(begin, start + len(text.rstrip()))


def entries(line: str, start: int, end: int) -> list[tuple[str, int]]:
    """Each destination the JSON object one line holds names, with its offset.

    The object spans `start` to `end` of the line, and a span holding
    anything else names nothing. It is read as `JSON.parse` reads it: a
    key written twice keeps its last value, so an earlier value names
    nothing, and a value that is no string is a broken menu, which
    `BrokenMenu` raises. A non-empty array in the object's place is a
    listed menu, which `ListedMenu` raises. A string value whose written
    text differs from the string it decodes to, such as one holding an
    escape, is left out, because the characters a rewrite replaces are
    the destination's own.
    """
    try:
        members = decoded(line[start:end])
    except ValueError:
        return []
    if isinstance(members, list) and members:
        raise ListedMenu
    if not isinstance(members, tuple):
        return []
    last = {key: at for at, (key, _value) in enumerate(members)}
    found = []
    for at, ((key, value), (begin, past)) in enumerate(
        zip(members, spans(line, start), strict=True)
    ):
        if last[key] != at:
            continue
        if not isinstance(value, str):
            raise BrokenMenu
        if line[begin + 1 : past - 1] == value:
            found.append((value, begin + 1))
    return found


def refused_constant(name: str) -> object:
    """Refuse a constant `JSON.parse` does not read, such as `NaN`."""
    raise ValueError(name)


MENU_DECODER = json.JSONDecoder(
    object_pairs_hook=tuple, parse_constant=refused_constant
)


def decoded(text: str) -> object:
    """One `links` object's text decoded, each object as its members in order."""
    return MENU_DECODER.decode(text)


def spans(line: str, start: int) -> Iterator[tuple[int, int]]:
    """Where each member's value sits in the JSON object opening at `start`.

    The object has already decoded, so the walk reads its text lexically:
    a key is a string, and a value runs to the `,` or `}` outside every
    string and every nested value.
    """
    at = skipped(line, start + 1)
    while line[at] != JSON_MEMBER_END[1]:
        key = JSON_STRING.match(line, at)
        assert key is not None
        at = skipped(line, skipped(line, key.end()) + 1)
        past = value_end(line, at)
        yield at, past
        at = skipped(line, past)
        if line[at] == JSON_MEMBER_END[0]:
            at = skipped(line, at + 1)


def value_end(line: str, at: int) -> int:
    """Where the JSON value opening at `at` of one line ends."""
    depth = 0
    while at < len(line):
        if line[at] == '"':
            string = JSON_STRING.match(line, at)
            assert string is not None
            at = string.end()
            if depth == 0:
                return at
            continue
        if depth == 0 and (line[at] in JSON_MEMBER_END or line[at] in JSON_SPACE):
            return at
        if line[at] in JSON_OPEN:
            depth += 1
        elif line[at] in JSON_CLOSE:
            depth -= 1
            if depth == 0:
                return at + 1
        at += 1
    return at


def skipped(line: str, at: int) -> int:
    """The first position from `at` past the JSON whitespace one line holds there."""
    while at < len(line) and line[at] in JSON_SPACE:
        at += 1
    return at


def uses(tokens: Sequence[Token], selected: Sequence[Token]) -> Iterator[Use]:
    """Yield reference occurrences in selected regions, in source order.

    `events` supplies inline uses, `opening_text` and `alternative_text`
    read their openings, and `plain_label` reads labels. Images are resources.
    Local link titles supply names through `tags.read`; images and external
    links have no tags. `sections` supplies the containing section from the
    whole document. Diagram references use `Click` fields from `clicks`.
    Inline uses are located at their containing block's opening line.
    """
    held = sections(tokens)
    starts = [line for line, _ in held]

    def holding(line: int | None) -> tuple[int, str] | tuple[None, None]:
        at = 0 if line is None else bisect_right(starts, line)
        return held[at - 1] if at else (None, None)

    for token in within(tokens, selected):
        if token.type == FENCE:
            for click in clicks(token):
                heading, title = holding(click.line)
                yield Use(
                    click.destination,
                    click.opening,
                    click.name,
                    click.line,
                    False,
                    title,
                    heading=heading,
                    tags=frozenset()
                    if external(click.destination)
                    else read_tags(click.title),
                )
            continue
        if token.type != INLINE:
            continue
        line = None if token.map is None else token.map[0] + 1
        heading, title = holding(line)
        for children, at, child in events(token.children or []):
            if child.type == LINK_OPEN:
                found = child.attrGet(HREF)
                destination = "" if found is None else str(found)
                attribute = child.attrGet("title")
                opening = opening_text(children, at)
                yield Use(
                    destination,
                    opening,
                    opening,
                    line,
                    False,
                    title,
                    plain_label(children, at),
                    heading,
                    read_tags(None if attribute is None else str(attribute))
                    if not external(destination)
                    else frozenset(),
                )
            else:
                image_destination = child.attrGet(SRC)
                alternative = alternative_text(child)
                yield Use(
                    "" if image_destination is None else str(image_destination),
                    alternative,
                    alternative,
                    line,
                    True,
                    title,
                    heading=heading,
                )


def sections(tokens: Sequence[Token]) -> list[tuple[int, str]]:
    """The line and text of each heading rooting a section, in source order.

    A section is rooted by a document-level heading, so a heading a
    container carries roots none and titles nothing beneath it.
    """
    rooting = {id(token) for token in regions(tokens)}
    return [
        (opening.map[0] + 1, visible(inline))
        for opening, inline in headings(tokens)
        if id(opening) in rooting and opening.map is not None
    ]


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
    """Count the occurrences `uses` yields for the selected regions.

    The count is per written occurrence rather than per target identity,
    so repeated references each contribute to the budget.
    """
    return sum(1 for _ in uses(tokens, selected))


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
    """The document-level `regions` selected from one source, in source order."""

    regions: tuple[Token, ...]
