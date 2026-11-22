"""Configure Markdown parsing and report unsupported selected constructs.

`parser` configures the dialect, `parse` produces tokens, and `refusals`
checks a caller's token selection. Diagram fields follow `source.Click`.
"""

import re
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from functools import cache
from pathlib import PurePosixPath
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.parser_inline import ParserInline
from markdown_it.rules_inline.state_inline import StateInline
from markdown_it.token import Token
from markdown_it.utils import EnvType

from prosiform import PROFILE
from prosiform.limits import NESTING
from prosiform.marks import marked
from prosiform.source import FENCE, external, linking
from prosiform.tags import read as read_tags

PRESET = "commonmark"
ENABLED = ("table", "strikethrough")
HEADROOM = 20

SUFFIXES = (".md", ".markdown")

TEXT = "text"
INLINE = "inline"
HEADING_OPEN = "heading_open"
LIST_ITEM_OPEN = "list_item_open"
PARAGRAPH_OPEN = "paragraph_open"
ROW_OPEN = "tr_open"
CELL_OPENS = ("th_open", "td_open")
LINK_OPEN = "link_open"
LINK_CLOSE = "link_close"
HTML_BLOCK = "html_block"
HTML_INLINE = "html_inline"

COMMAND_OPEN = ("<big>", "<pre>")
COMMAND_CLOSE = ("</pre>", "</big>")

HREF = "href"
TITLE = "title"
LABEL_OPEN = "["

REFERENCES = "references"

TASK_MARKERS = ("[x]", "[X]")
MARKER_LENGTH = 3
MARKER_LABELS = ("x", "X")
MARKER = "marker"
MARKER_CHILDREN = 3
COLUMN = "column"

UNESCAPED = r"(?<!\\)"
WIKI_LINK = re.compile(rf"{UNESCAPED}(!?)\[\[[^\[\]\n]+\]\]")
FOOTNOTE = re.compile(rf"{UNESCAPED}\[\^[^\[\]\s][^\[\]\n]*\]")
HEADING_ATTRIBUTE = re.compile(rf"{UNESCAPED}\{{#[^{{}}\s]+\}}\s*$")

LINK_REMEDY = "write the dependency as a Markdown link"

RAW_HTML = "E_RAW_HTML"
UNSUPPORTED_CONSTRUCT = "E_UNSUPPORTED_CONSTRUCT"
PARSER_REFERENCE_LIMIT = "E_PARSER_REFERENCE_LIMIT"

CODES = (RAW_HTML, UNSUPPORTED_CONSTRUCT, PARSER_REFERENCE_LIMIT)

NESTING_CEILING = "maxNesting"


@dataclass(frozen=True)
class Refusal:
    """One unsupported construct's diagnostic fields.

    `code`, `message` and `remedy` describe the refusal; `line` and
    `reference` locate it. `earlier` locates a related earlier construct.
    """

    code: str
    message: str
    remedy: str
    line: int | None = None
    reference: str | None = None
    earlier: int | None = None
    """The line of an earlier construct the refusal names beside its own."""


class Suppressed(Exception):
    """A reference lookup declined by `Watched.skipToken`.

    `line` locates the abandoned inline content, and `reference` names
    the destination `referenced` recovered, where available.
    """

    def __init__(self, line: int | None, reference: str | None = None) -> None:
        named = f"the lookup of {reference!r}" if reference else "a reference lookup"
        super().__init__(
            f"the parser reached its own nesting ceiling and abandoned {named}, "
            f"so a reference this source carries is read as literal text and "
            f"names a document the run cannot reach"
        )
        self.line = line
        self.reference = reference

    @property
    def remedy(self) -> str:
        """The remedy a declined lookup leads to, naming the nesting it sits in."""
        return "write the reference outside the nesting that surrounds it"


class Watched(ParserInline):
    """An inline parser recording active content and declined label scans.

    `parse` maintains the content stack and `skipToken` detects a declined
    lookup, with its outermost content and abandoned span.
    """

    def __init__(self) -> None:
        super().__init__()
        self.reading: list[str] = []
        self.declined: str | None = None
        self.abandoned: str | None = None

    def parse(
        self, src: str, md: MarkdownIt, env: EnvType, tokens: list[Token]
    ) -> list[Token]:
        """One run of inline content, recorded while the parser reads it."""
        self.reading.append(src)
        try:
            return super().parse(src, md, env, tokens)
        finally:
            self.reading.pop()

    def skipToken(self, state: StateInline) -> None:  # noqa: N802
        """Record the first uncached label scan at the parser's nesting ceiling.

        The outermost inline content locates the refusal; the abandoned span
        allows `referenced` to recover its destination. Watching the scan is
        necessary because literal text alone does not reveal a declined lookup.
        """
        ceiling = state.level >= state.md.options[NESTING_CEILING]
        if ceiling and state.pos not in state.cache and self.declined is None:
            self.declined = self.reading[0]
            self.abandoned = state.src[state.pos : state.posMax]
        super().skipToken(state)


@cache
def watch(budget: int) -> Watched:
    """The watched inline parser one configuration of the profile reads with."""
    return Watched()


@cache
def parser(budget: int) -> MarkdownIt:
    """Configure CommonMark with tables and double-tilde strikethrough.

    Typographic substitution is disabled by the preset. Task-list syntax
    has no plugin and raw HTML remains visible to `refusals`. The parser's
    nesting ceiling is `HEADROOM` above the declared block-nesting budget,
    so source nesting can be counted before refusal; `Watched.skipToken`
    detects an inline reference lookup the parser declines at its ceiling.
    """
    configured = MarkdownIt(PRESET, {NESTING_CEILING: budget + HEADROOM})
    configured.inline = watch(budget)
    return configured.enable(list(ENABLED))


@cache
def reader() -> MarkdownIt:
    """The profile's parser with no watch over it, which reads one abandoned span.

    A span is read after the parse that abandoned it has finished, and
    the watch belongs to that parse, so the span is read with a parser
    of its own: a second run through the watched one would answer for
    the span rather than for the source.
    """
    return MarkdownIt(PRESET).enable(list(ENABLED))


def referenced(span: str, env: dict[str, Any]) -> str | None:
    """The destination the construct holding one abandoned span names.

    The scan stops inside a label the parser had opened, so the span is
    a construct again once that bracket is restored, and the definition
    environment the source filled is what a reference-style spelling
    resolves against. A span whose construct does not complete names no
    destination, and the lookup is reported against its source alone.
    """
    for token in reader().parse(LABEL_OPEN + span, dict(env)):
        opening = next(iter(token.children or []), None)
        if opening is None:
            continue
        if opening.type != LINK_OPEN:
            return None
        return str(opening.attrGet(HREF) or "") or None
    return None


def parse(
    text: str,
    budget: int = NESTING.default,
    env: dict[str, Any] | None = None,
) -> list[Token]:
    """Parse source text and fill `env` with its reference definitions.

    A declined lookup recorded by `Watched.skipToken` raises `Suppressed`.
    `linked_marker` and `unlink_marker` preserve task markers as literal
    text, and `cells` supplies table-column metadata for each cell token.
    """
    watched = watch(budget)
    watched.declined = None
    watched.abandoned = None
    environment: dict[str, Any] = {} if env is None else env
    tokens = parser(budget).parse(text, environment)
    if watched.declined is not None:
        raise Suppressed(
            declined_line(tokens, watched.declined),
            referenced(watched.abandoned or "", environment),
        )
    for inline in item_openings(tokens):
        if linked_marker(inline):
            unlink_marker(inline)
    for inline, column in cells(tokens):
        inline.meta[COLUMN] = column
    return tokens


def declined_line(tokens: Sequence[Token], content: str) -> int | None:
    """The source line of the inline content one declined lookup sits in."""
    return next(
        (
            line(token)
            for token in tokens
            if token.type == INLINE and token.content == content
        ),
        None,
    )


def is_markdown(name: str) -> bool:
    """Whether a document name carries a suffix the profile classifies as Markdown.

    The suffix decides classification case-insensitively; the name itself
    keeps the spelling and case the filesystem holds.
    """
    return PurePosixPath(name).suffix.lower() in SUFFIXES


def item_openings(tokens: Sequence[Token]) -> Iterator[Token]:
    """The inline token opening each list item's first paragraph.

    A task marker occupies the head of that paragraph and nowhere else, so
    this is the only position at which a link can be one.
    """
    item = False
    paragraph = False
    for token in tokens:
        if token.type == LIST_ITEM_OPEN:
            item = True
        elif token.type == PARAGRAPH_OPEN:
            paragraph = item
            item = False
        elif token.type == INLINE:
            if paragraph:
                yield token
            paragraph = False
        else:
            item = False
            paragraph = False


def cells(tokens: Sequence[Token]) -> Iterator[tuple[Token, int]]:
    """The inline token of each table cell, with the column it stands in.

    Every cell of one row shares that row's line, so the column is what
    says which stretch of the line a cell's inline content was read from.
    """
    column = 0
    cell = False
    for token in tokens:
        if token.type == ROW_OPEN:
            column = 0
        elif token.type in CELL_OPENS:
            cell = True
        elif token.type == INLINE and cell:
            yield token, column
            column += 1
            cell = False


def linked_marker(inline: Token) -> bool:
    """Whether a definition has turned this item's task marker into a link."""
    children = inline.children or []
    if len(children) < MARKER_CHILDREN:
        return False
    if inline.content[:MARKER_LENGTH] not in TASK_MARKERS:
        return False
    following = inline.content[MARKER_LENGTH : MARKER_LENGTH + 1]
    if following and not following.isspace():
        return False
    return (
        children[0].type == LINK_OPEN
        and children[1].content in MARKER_LABELS
        and children[2].type == LINK_CLOSE
    )


def unlink_marker(inline: Token) -> None:
    """Return a linked task marker to the literal text the source wrote.

    The token records that it carries one, because the marker is the
    one bracket pair a definition does not make a link of and a scan
    over the source text has no list structure to read that from.
    """
    children = inline.children or []
    marker = Token(TEXT, "", 0, content=inline.content[:MARKER_LENGTH])
    inline.children = [marker, *children[MARKER_CHILDREN:]]
    inline.meta[MARKER] = True


def line(token: Token) -> int | None:
    """The one-based source line a token opens on, where the parser records one."""
    return None if token.map is None else token.map[0] + 1


def literal(inline: Token) -> str:
    """The text of one inline token that the parser left as text."""
    children = inline.children or []
    return "".join(child.content for child in children if child.type == TEXT)


def recognized(pattern: re.Pattern[str], inline: Token) -> re.Match[str] | None:
    """One construct's spelling, where the inline token carries it as literal text.

    The spelling has to survive both readings: the text the parser left as
    text, which holds no code span and no markup, and the unescaped source
    the parser read, which holds no construct an author escaped.
    """
    found = pattern.search(literal(inline))
    if found is None or pattern.search(inline.content) is None:
        return None
    return found


def html_refusal(spelling: str, at: int | None) -> Refusal:
    """Build the raw-HTML refusal for `spelling` at source line `at`."""
    return Refusal(
        code=RAW_HTML,
        message=(
            f"the raw HTML {spelling!r} is outside the {PROFILE} profile, which "
            f"refuses it rather than copying it into the bundle"
        ),
        remedy="write the content as Markdown",
        line=at,
    )


def command_block(children: Sequence[Token]) -> bool:
    """Whether a paragraph opens with `COMMAND_OPEN` and closes with `COMMAND_CLOSE`.

    The exact inline HTML tags delimit the command block; its enclosed
    content may contain ordinary inline events.
    """
    tags = [child.content if child.type == HTML_INLINE else None for child in children]
    return (
        len(tags) >= len(COMMAND_OPEN) + len(COMMAND_CLOSE)
        and tuple(tags[: len(COMMAND_OPEN)]) == COMMAND_OPEN
        and tuple(tags[-len(COMMAND_CLOSE) :]) == COMMAND_CLOSE
    )


def inline_refusals(inline: Token, heading: bool, paragraph: bool) -> Iterator[Refusal]:
    """Yield unsupported constructs in one inline token.

    `command_block` identifies the outer tags exempted from raw-HTML refusal.
    Local-link title tags recognized by `marked_tag`, wiki links, footnote
    references and heading attributes produce located refusals. `recognized`
    limits syntax detection to unescaped literal text.
    """
    at = line(inline)
    children = inline.children or []
    if paragraph and command_block(children):
        children = children[len(COMMAND_OPEN) : -len(COMMAND_CLOSE)]
    markup = next((child for child in children if child.type == HTML_INLINE), None)
    if markup is not None:
        yield html_refusal(markup.content, at)

    for child in children:
        title = child.attrGet(TITLE) if child.type == LINK_OPEN else None
        if not title or external(str(child.attrGet(HREF) or "")):
            continue
        tag = marked_tag(read_tags(str(title)))
        if tag is not None:
            yield Refusal(
                code=UNSUPPORTED_CONSTRUCT,
                message=(
                    f"the link to {child.attrGet(HREF)!r} carries the title tag "
                    f"{tag!r}, which states operator marks, and a title names "
                    f"presets alone"
                ),
                remedy="write the marks at the start of the link's text, and keep "
                "the title for preset tags",
                line=at,
                reference=str(child.attrGet(HREF)),
            )

    found = recognized(WIKI_LINK, inline)
    if found is not None:
        spelling = found.group()
        construct = "transclusion directive" if found.group(1) else "wiki link"
        yield Refusal(
            code=UNSUPPORTED_CONSTRUCT,
            message=(
                f"the {construct} {spelling!r} names a document the {PROFILE} "
                f"profile does not resolve"
            ),
            remedy=LINK_REMEDY,
            line=at,
            reference=spelling,
        )

    found = recognized(FOOTNOTE, inline)
    if found is not None:
        yield Refusal(
            code=UNSUPPORTED_CONSTRUCT,
            message=(
                f"the footnote reference {found.group()!r} names a target the "
                f"{PROFILE} profile does not carry"
            ),
            remedy="write the note where it is referred to",
            line=at,
            reference=found.group(),
        )

    if not heading:
        return
    found = recognized(HEADING_ATTRIBUTE, inline)
    if found is not None:
        yield Refusal(
            code=UNSUPPORTED_CONSTRUCT,
            message=(
                f"the heading attribute {found.group().strip()!r} names the section "
                f"the heading opens, which the {PROFILE} profile names by its "
                f"heading text alone"
            ),
            remedy="retitle the heading rather than naming it a second time",
            line=at,
            reference=found.group().strip(),
        )


def local_markdown(destination: str) -> bool:
    """Whether the path before a destination's query or fragment is Markdown.

    `source.external` classifies remote paths and `is_markdown` tests suffixes.
    """
    path = destination.partition("#")[0].partition("?")[0]
    return not external(path) and is_markdown(path)


def marked_tag(tags: frozenset[str]) -> str | None:
    """Return the first tag in code point order that `marks.marked` recognizes."""
    return next((one for one in sorted(tags) if marked(one)), None)


def diagram_refusals(fence: Token) -> Iterator[Refusal]:
    """Yield refusals from the diagram read returned by `source.linking`.

    Diagram-link fields follow `source.Click`. A tooltip tag recognized by
    `marked_tag`, a repeated element link, or a malformed menu is refused.
    Unfollowed rendered links and unparsed Gantt clicks are refused when
    `local_markdown` identifies a local Markdown destination.
    """
    read = linking(fence)
    for click in read.clicks:
        tag = marked_tag(read_tags(click.title))
        if tag is None:
            continue
        yield Refusal(
            code=UNSUPPORTED_CONSTRUCT,
            message=(
                f"the diagram's {click.name!r} carries the tooltip tag "
                f"{tag!r}, which states operator marks, and a tooltip "
                f"is the link's title, which names presets alone"
            ),
            remedy="write the marks at the start of the text of the element the "
            "link names, as Plan[⇉ Plan], and keep the tooltip for preset tags",
            line=click.line,
            reference=click.name,
        )
    for earlier, click in read.repeated:
        yield Refusal(
            code=UNSUPPORTED_CONSTRUCT,
            message=(
                f"the diagram's {click.name!r} links the element {click.node!r}, "
                f"which {earlier.name!r} already links, and Mermaid keeps one "
                f"link for each element, so a reader of the rendered diagram "
                f"reaches only the last"
            ),
            remedy="keep one click or link line for each element, and draw "
            "each further link on an element of its own",
            line=click.line,
            reference=click.name,
            earlier=earlier.line,
        )
    for at in read.listed:
        yield Refusal(
            code=UNSUPPORTED_CONSTRUCT,
            message=(
                f"the sequence diagram's links line holds an array, which Mermaid "
                f"renders as a menu whose entries are named by their positions, so "
                f"the {PROFILE} profile cannot carry it"
            ),
            remedy="write the links value as an object naming each entry",
            line=at,
        )
    for at in read.broken:
        yield Refusal(
            code=UNSUPPORTED_CONSTRUCT,
            message=(
                f"the sequence diagram's links line holds a value that is not a "
                f"string, which Mermaid renders as a link opening nothing, so the "
                f"{PROFILE} profile cannot carry it"
            ),
            remedy="write each value of the links object as a string",
            line=at,
        )
    for link in read.unfollowed:
        if not local_markdown(link.destination):
            continue
        yield Refusal(
            code=UNSUPPORTED_CONSTRUCT,
            message=(
                f"the diagram's {link.form} names the local Markdown document "
                f"{link.destination!r}, which Mermaid renders as a link the "
                f"{PROFILE} profile does not follow, so the bundle would carry "
                f"a link to a document it does not hold"
            ),
            remedy="write the link as a click line naming the document",
            line=link.line,
            reference=link.destination,
        )
    for click in read.unparsed:
        if not local_markdown(click.destination):
            continue
        yield Refusal(
            code=UNSUPPORTED_CONSTRUCT,
            message=(
                f"the Gantt chart's {click.name!r} names {click.destination!r} in "
                f"a form Mermaid's gantt grammar does not parse, which reads "
                f"href and the destination alone, so Mermaid draws no chart and "
                f"the click opens nothing"
            ),
            remedy='write the click as click <task> href "<destination>" alone '
            "on its line, with no tooltip, link target or semicolon: a Gantt "
            "task's click states no operator and selects no preset",
            line=click.line,
            reference=click.destination,
        )


def refusals(tokens: Iterable[Token]) -> Iterator[Refusal]:
    """Yield refusals in token order for the caller's selected content.

    Block HTML is refused through `html_refusal`, fences are checked by
    `diagram_refusals`, and inline content by `inline_refusals`. The caller
    supplies the token scope to check.
    """
    heading = paragraph = False
    for token in tokens:
        if token.nesting == 1:
            heading = token.type == HEADING_OPEN
            paragraph = token.type == PARAGRAPH_OPEN
        if token.type == HTML_BLOCK:
            opening = next(iter(token.content.strip().splitlines()), token.content)
            yield html_refusal(opening, line(token))
        elif token.type == FENCE:
            yield from diagram_refusals(token)
        elif token.type == INLINE:
            yield from inline_refusals(token, heading, paragraph)
