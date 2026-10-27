"""The `skill-markdown-v3` profile: the parser it configures and what it refuses.

The profile is CommonMark with pipe tables and double-tilde strikethrough
enabled, source task-list markers preserved as the text the source wrote,
typographic substitution off, and raw HTML recognized so a run can refuse
it. Every one of those is a property of the configuration below rather
than of a plugin: the parser's `commonmark` preset supplies the core and
holds the typographer off, `table` and `strikethrough` are core rules
enabled by name, and leaving the task-list plugin out is what keeps a
marker the three characters the source spelled.

A link the parser produces is a use, and a code span or a code block
carries none, with one exception the source model reads: a diagram link
line in a fence whose info string opens with `mermaid` — a `click` line,
a class diagram's `link` line, or a sequence diagram's `link` or `links`
participant menu, its keywords in any letter case — names a destination
a reader of the rendered diagram follows, so each such destination is a
use although the parser reads the fence as text.

A reference definition can otherwise turn `[x]` at the head of a list item
into a link, which would make a task marker a dependency. The parse
recognizes those positions and returns the marker to the literal text it
is, so the token stream every later stage reads carries no such link.

The parser holds a nesting ceiling of its own, and a label scan that
reaches it is abandoned at the end of the paragraph rather than resolved:
the reference that label opens is read as literal text and its lookup
never happens. The profile watches that scan, so a lookup the ceiling
declined is reported rather than published as a bundle missing whatever
the reference named. The watch keeps the span the scan stopped in, which
runs from inside the label the parser had opened to the end of that
inline content, and reading it names the reference the lookup would have
made.

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

A Mermaid sequence diagram's `links` line whose JSON object holds a value
that is no string names a link Mermaid renders opening nothing, so it is
refused as an unsupported construct naming its line rather than bundled
around the gap.
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
from prosiform.source import FENCE, linking

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

HREF = "href"
LABEL_OPEN = "["

REFERENCES = "references"

TASK_MARKERS = ("[x]", "[X]")
MARKER_LENGTH = 3
MARKER_LABELS = ("x", "X")
MARKER = "marker"
MARKER_CHILDREN = 3

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


class Suppressed(Exception):
    """One reference lookup the parser's nesting ceiling declined to make.

    The lookup never happened, so what the reference named is unknown
    and no bundle can be published from the parse that abandoned it.
    The line is the source line of the content the scan was reading,
    where the parser records one, and the reference is the destination
    the abandoned construct spells, where the span the scan stopped in
    completes one.
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
    """The inline parser, watched for a reference lookup its ceiling declines.

    A label scan reaching the ceiling is abandoned to the end of the
    paragraph, which is the one event that tells a declined lookup from
    the literal bracketed text it leaves behind: a scan over the source
    sees the same brackets either way. The scan is watched rather than
    the result compared against a second parse, because an event stream
    that omits a suppressed reference agrees with another one that omits
    it too.

    The watch records the outermost content being parsed, which is the
    inline token the declined lookup sits in, so the parse the caller
    reads locates it by that content. It records the span the scan
    stopped in beside it, which is what names the reference the lookup
    would have made.
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
        """One token of a label scan, noting a scan the ceiling abandons."""
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
    """The parser the profile configures: CommonMark and its two extensions.

    The parser carries a nesting ceiling of its own, and reaching it
    makes it read the rest of a construct as text rather than refuse
    it. The ceiling therefore sits above the nesting budget the run
    declares, far enough that the inline structure of an ordinary
    document is unaffected, so a source nested deeper than the budget
    is counted past the boundary and refused rather than quietly read
    as something else.

    The ceiling is reachable all the same, because inline nesting is
    counted into it and no budget is declared over that, so the parser
    reads with the watch that reports a lookup the ceiling declines.
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
    """One source, parsed under the profile, its task markers left as text.

    The environment the parse fills holds the link-reference definitions
    the source declared, which is the definition environment its own
    reference-style uses resolve against. A caller that reads them
    supplies the mapping the parse writes them into.

    A parse whose nesting ceiling declined a reference lookup raises
    rather than returning tokens, so every caller reads a token stream
    the parser resolved in full. The raise carries the reference that
    lookup would have made, where the span the scan abandoned spells
    one.
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


def menu_refusals(fence: Token) -> Iterator[Refusal]:
    """Each `links` line one diagram carries holding a value that is no string."""
    for at in linking(fence).broken:
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


def refusals(tokens: Iterable[Token]) -> Iterator[Refusal]:
    """Every construct the profile refuses, in the order the run carries them.

    The tokens are whatever run a caller holds them to, and the caller
    decides which: the profile says what it refuses, and the scope of
    the refusal is a question about the bundling rather than about the
    construct. A run narrowed to the regions one source contributes
    therefore reports what that content carries and nothing else.
    """
    heading = False
    for token in tokens:
        if token.nesting == 1:
            heading = token.type == HEADING_OPEN
        if token.type == HTML_BLOCK:
            opening = next(iter(token.content.strip().splitlines()), token.content)
            yield html_refusal(opening, line(token))
        elif token.type == FENCE:
            yield from menu_refusals(token)
        elif token.type == INLINE:
            yield from inline_refusals(token, heading)
