"""The `skill-markdown-v1` profile: the parser it configures and what it refuses.

The profile is CommonMark with pipe tables and double-tilde strikethrough
enabled, source task-list markers preserved as the text the source wrote,
typographic substitution off, and raw HTML recognized so a run can refuse
it. Every one of those is a property of the configuration below rather
than of a plugin: the parser's `commonmark` preset supplies the core and
holds the typographer off, `table` and `strikethrough` are core rules
enabled by name, and leaving the task-list plugin out is what keeps a
marker the three characters the source spelled.

A reference definition can otherwise turn `[x]` at the head of a list item
into a link, which would make a task marker a dependency. The parse
recognizes those positions and returns the marker to the literal text it
is, so the token stream every later stage reads carries no such link.

A construct the profile does not support is not simply left unparsed. One
that names a dependency or a section fails the run, because publishing it
as literal text would drop that name without reporting it. Recognition is
therefore deliberately narrow, and the two conditions below are what draw
the line between a construct and prose that resembles one.

- The spelling occurs in text the parser left as text, so a code span, a
  code block, a link destination and raw HTML carry none of it.
- The spelling occurs unescaped in the source the parser read, so a
  deliberately escaped `\\[\\[page\\]\\]` is the literal text it asks to be.

Recognition covers the constructs spelled in Markdown's own link and
heading syntax: a wiki link, its transclusion form, a footnote reference,
and a heading-attribute suffix at the end of a heading. A directive
written in a templating language the profile does not read is ordinary
prose, and so is a brace block anywhere but the end of a heading.
"""

import re
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from functools import cache
from pathlib import PurePosixPath

from markdown_it import MarkdownIt
from markdown_it.token import Token

from prosiform import PROFILE
from prosiform.limits import NESTING

PRESET = "commonmark"
ENABLED = ("table", "strikethrough")
HEADROOM = 20

SUFFIXES = (".md", ".markdown")

TEXT = "text"
INLINE = "inline"
HEADING_OPEN = "heading_open"
LIST_ITEM_OPEN = "list_item_open"
PARAGRAPH_OPEN = "paragraph_open"
LINK_OPEN = "link_open"
LINK_CLOSE = "link_close"
HTML_BLOCK = "html_block"
HTML_INLINE = "html_inline"

TASK_MARKERS = ("[x]", "[X]")
MARKER_LENGTH = 3
MARKER_LABELS = ("x", "X")
MARKER_CHILDREN = 3

UNESCAPED = r"(?<!\\)"
WIKI_LINK = re.compile(rf"{UNESCAPED}(!?)\[\[[^\[\]\n]+\]\]")
FOOTNOTE = re.compile(rf"{UNESCAPED}\[\^[^\[\]\s][^\[\]\n]*\]")
HEADING_ATTRIBUTE = re.compile(rf"{UNESCAPED}\{{#[^{{}}\s]+\}}\s*$")

LINK_REMEDY = "write the dependency as a Markdown link"

RAW_HTML = "E_RAW_HTML"
UNSUPPORTED_CONSTRUCT = "E_UNSUPPORTED_CONSTRUCT"


@dataclass(frozen=True)
class Refusal:
    """One construct in selected content the profile refuses, and where it sits.

    The profile names the defect it refuses, so the refusal carries the
    code the contract declares for it: raw HTML and a recognized
    unsupported construct are two clauses with two remedies.
    """

    code: str
    message: str
    remedy: str
    line: int | None = None
    reference: str | None = None


@cache
def parser(budget: int) -> MarkdownIt:
    """The parser the profile configures: CommonMark and its two extensions.

    The parser carries a nesting ceiling of its own, and reaching it
    makes it read the rest of a construct as text rather than refuse
    it. The ceiling therefore sits above the nesting budget the run
    declares, far enough that the inline structure of an ordinary
    document is unaffected, so a source nested deeper than the budget
    is counted past the boundary and refused rather than quietly read
    as something else.
    """
    return MarkdownIt(PRESET, {"maxNesting": budget + HEADROOM}).enable(list(ENABLED))


def parse(text: str, budget: int = NESTING.default) -> list[Token]:
    """One source, parsed under the profile, its task markers left as text."""
    tokens = parser(budget).parse(text)
    for inline in item_openings(tokens):
        if linked_marker(inline):
            unlink_marker(inline)
    return tokens


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
    """Return a linked task marker to the literal text the source wrote."""
    children = inline.children or []
    marker = Token(TEXT, "", 0, content=inline.content[:MARKER_LENGTH])
    inline.children = [marker, *children[MARKER_CHILDREN:]]


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
    """Raw HTML, which the bundle carries no form of."""
    return Refusal(
        code=RAW_HTML,
        message=(
            f"the raw HTML {spelling!r} is outside the {PROFILE} profile, which "
            f"refuses it rather than copying it into the bundle"
        ),
        remedy="write the content as Markdown",
        line=at,
    )


def inline_refusals(inline: Token, heading: bool) -> Iterator[Refusal]:
    """Every construct one inline token carries that the profile refuses."""
    at = line(inline)
    markup = next(
        (child for child in inline.children or [] if child.type == HTML_INLINE), None
    )
    if markup is not None:
        yield html_refusal(markup.content, at)

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


def refusals(tokens: Sequence[Token]) -> Iterator[Refusal]:
    """Every construct the profile refuses, in the order the source carries them."""
    heading = False
    for token in tokens:
        if token.nesting == 1:
            heading = token.type == HEADING_OPEN
        if token.type == HTML_BLOCK:
            opening = next(iter(token.content.strip().splitlines()), token.content)
            yield html_refusal(opening, line(token))
        elif token.type == INLINE:
            yield from inline_refusals(token, heading)
