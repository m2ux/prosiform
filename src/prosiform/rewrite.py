"""Locate source-local reference spans and apply inline publication edits.

`definitions` captures authored definitions, `uses` locates reference spans,
and `rewritten` applies edits without re-rendering surrounding source text.
"""

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import accumulate, pairwise
from string import punctuation
from typing import Any

from markdown_it.common.utils import (
    UNESCAPE_ALL_RE,
    normalizeReference,
    replaceEntityPattern,
)
from markdown_it.rules_block.table import escapedSplit
from markdown_it.token import Token

from prosiform.closure import filed, published_text
from prosiform.marks import opened
from prosiform.profile import (
    COLUMN,
    COMMAND_CLOSE,
    COMMAND_OPEN,
    INLINE,
    MARKER,
    MARKER_LABELS,
    PARAGRAPH_OPEN,
    command_block,
    reader,
)
from prosiform.source import (
    HREF,
    LINE_FEED,
    LINK_CLOSE,
    LINK_OPEN,
    TEXT,
    events,
    opening_markers,
    opening_text,
)
from prosiform.tags import read as read_tags

BACKTICK = "`"
ESCAPE = "\\"
IMAGE = "!"
LABEL_OPEN = "["
LABEL_CLOSE = "]"
TARGET_OPEN = "("
TARGET_CLOSE = ")"
ANGLE_OPEN = "<"
ANGLE_CLOSE = ">"
COLON = ":"
PIPE = "|"

SPACE = " "
STRONG_OPEN = "strong_open"
STRONG_CLOSE = "strong_close"
STRONG = "**"

PARAGRAPH = (PARAGRAPH_OPEN, INLINE, "paragraph_close")
TEXT_LINE = "text"
ESCAPABLE = re.compile(r"[ \t]*(?:\d{1,9}(?=[.)]))?")
CONTINUING = re.compile(r"(?:[ \t]*>)*[ \t]*")


TITLE_CLOSERS = {'"': '"', "'": "'", TARGET_OPEN: TARGET_CLOSE}

LINK = "link"
RESOURCE = "resource"

AUTOLINK = re.compile(
    r"<(?:[A-Za-z][A-Za-z0-9+.\-]{1,31}:[^\x00-\x20<>]*"
    r"|[A-Za-z0-9.!#$%&'*+/=?^_`{|}~\-]+"
    r"@[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?)*)>"
)

MAP = "map"


class Unrewritable(Exception):
    """A use the run resolved and the emission cannot edit in place."""


@dataclass(frozen=True)
class Definition:
    """An authored link-reference definition.

    `destination` and `title` retain their written delimiters; `lines` holds
    the half-open content-line span occupied by the definition.
    """

    destination: str
    title: str
    lines: tuple[int, int]


@dataclass(frozen=True)
class Use:
    """The spans of one inline link or image.

    `kind` classifies the use; `opening` and `end` bound its written extent.
    `label` spans its visible content and `target` its destination syntax.
    `definition` holds a resolved reference definition, `autolink` identifies
    an angle-bracket use, and `title` spans an inline title with its delimiters,
    or is absent when the use has none.
    """

    kind: str
    opening: int
    label: tuple[int, int]
    target: tuple[int, int]
    end: int
    definition: Definition | None = None
    autolink: bool = False
    title: tuple[int, int] | None = None


@dataclass(frozen=True)
class Titled:
    """A destination and the preset `names` to add to its link title."""

    destination: str
    names: tuple[str, ...]


@dataclass(frozen=True)
class Followed:
    """A dispatch destination and its model annotations.

    `after` holds the Markdown suffix; `model` holds the name
    `bundle.model_comment` writes.
    """

    destination: str
    after: str
    model: str


TITLE_ESCAPED = frozenset('\\"()&' + "'")
"""The character escape set `title_names` uses for inserted preset names."""


def title_names(names: Sequence[str]) -> str:
    """Join names into a comma-separated title list with literal text escaping.

    Prefix title delimiters, backslashes and ampersands with a backslash so
    the parser reads each inserted name as its original text.
    """
    return ", ".join(
        "".join(ESCAPE + char if char in TITLE_ESCAPED else char for char in name)
        for name in names
    )


def gained(title: str, names: Sequence[str]) -> str:
    """One authored title, delimiters included, with the names written before its close.

    Names follow the authored tags after a comma; a title holding nothing
    takes them alone.
    """
    inner = title[1:-1]
    separator = ", " if inner else ""
    return f"{title[:-1]}{separator}{title_names(names)}{title[-1]}"


def escaped(text: str, at: int) -> bool:
    """Whether the character at one position is escaped by a backslash run."""
    count = 0
    index = at - 1
    while index >= 0 and text[index] == ESCAPE:
        count += 1
        index -= 1
    return count % 2 == 1


def code_spans(text: str) -> list[tuple[int, int]]:
    """The source extents of code spans in inline text.

    Pair each opening backtick run with the next run of the same length.
    An unmatched opening is literal text and leaves later scanning available.
    """
    found: list[tuple[int, int]] = []
    at = 0
    while at < len(text):
        if text[at] != BACKTICK or escaped(text, at):
            at += 1
            continue
        opening = at
        while at < len(text) and text[at] == BACKTICK:
            at += 1
        width = at - opening
        scan = at
        while scan < len(text):
            if text[scan] != BACKTICK:
                scan += 1
                continue
            closing = scan
            while scan < len(text) and text[scan] == BACKTICK:
                scan += 1
            if scan - closing == width:
                found.append((opening, scan))
                at = scan
                break
        else:
            continue
    return found


def cell(row: str, column: int) -> tuple[int, int]:
    """The extent one table cell's inline content is read from in its row's line.

    The row is split by the parser's own table splitter, after the
    container markers and blanks the line opens with, and an empty cell
    before a leading pipe or after a trailing one is dropped, as the
    parser's table rule drops it. The splitter takes the backslash from
    each escaped pipe, so a cell spans one source character more than it
    holds for every pipe it holds. A column the row writes no cell for
    is the empty extent at the row's end.
    """
    opening = len(opening_markers(row))
    closing = len(row.rstrip())
    stretches: list[tuple[int, int]] = []
    at = opening
    for held in escapedSplit(row[opening:closing]):
        width = len(held) + held.count(PIPE)
        stretches.append((at, at + width))
        at += width + 1
    if stretches and stretches[0][0] == stretches[0][1]:
        stretches.pop(0)
    if stretches and stretches[-1][0] == stretches[-1][1]:
        stretches.pop()
    return stretches[column] if column < len(stretches) else (closing, closing)


def masked(spans: Sequence[tuple[int, int]], at: int) -> bool:
    """Whether one position sits inside a span the scan passes over."""
    return any(start <= at < end for start, end in spans)


def target_end(text: str, at: int) -> int | None:
    """Where the destination opening at one position ends, or nothing where it does not.

    A destination is written between angle brackets or as a run carrying
    balanced parentheses, and it ends at the first whitespace a title
    could follow, at the parenthesis closing the link, or at the closing
    angle bracket.
    """
    if at < len(text) and text[at] == ANGLE_OPEN:
        for index in range(at + 1, len(text)):
            if text[index] == ANGLE_CLOSE and not escaped(text, index):
                return index + 1
        return None
    depth = 0
    for index in range(at, len(text)):
        if escaped(text, index):
            continue
        if text[index].isspace():
            return index
        if text[index] == TARGET_OPEN:
            depth += 1
        elif text[index] == TARGET_CLOSE:
            if depth == 0:
                return index
            depth -= 1
    return None


def title_end(text: str, at: int) -> int | None:
    """Where the title opening at one position ends, or nothing where it does not."""
    closing = TITLE_CLOSERS[text[at]]
    for index in range(at + 1, len(text)):
        if text[index] == closing and not escaped(text, index):
            return index + 1
    return None


def skipped(text: str, at: int) -> int:
    """The first position at or after one position that is not whitespace."""
    while at < len(text) and text[at].isspace():
        at += 1
    return at


def inline_target(
    text: str, at: int
) -> tuple[tuple[int, int], tuple[int, int] | None, int] | None:
    """The destination and title spans and the end of the inline target at one position.

    The target runs from the parenthesis to the one closing it, holding
    a destination, an optional title, and the whitespace between them.
    The title span holds its delimiters, and a target writing no title
    has none. A run the grammar does not admit is no inline target, and
    the brackets before it are read as a reference-style use or as the
    literal text they are.
    """
    opening = skipped(text, at + 1)
    ending = target_end(text, opening)
    if ending is None:
        return None
    scan = skipped(text, ending)
    title: tuple[int, int] | None = None
    if scan < len(text) and text[scan] in TITLE_CLOSERS and scan > ending:
        closing = title_end(text, scan)
        if closing is None:
            return None
        title = (scan, closing)
        scan = skipped(text, closing)
    if scan >= len(text) or text[scan] != TARGET_CLOSE:
        return None
    return (opening, ending), title, scan + 1


def autolink_end(text: str, at: int, spans: Sequence[tuple[int, int]]) -> int | None:
    """Where the autolink at one position closes, or nothing where it opens none.

    An autolink is an absolute URI — a scheme, a colon, and no further
    whitespace or angle bracket — or an email address, each written
    between angle brackets as CommonMark spells it. A bracketed run
    spelling neither is the literal text the author wrote, so raw HTML
    opens no use here. A code span is read before an autolink is, so a
    run of backticks the brackets enclose leaves them the text they are.
    """
    found = AUTOLINK.match(text, at)
    if found is None:
        return None
    if any(masked(spans, index) for index in range(at, found.end())):
        return None
    return found.end()


def label_close(text: str, at: int, spans: Sequence[tuple[int, int]]) -> int | None:
    """Where the reference label opening at one position closes.

    A link label holds no unescaped bracket of its own, so the label
    ends at the first closing bracket the scan reads as one.
    """
    for index in range(at + 1, len(text)):
        if escaped(text, index) or masked(spans, index):
            continue
        if text[index] in (LABEL_OPEN, LABEL_CLOSE):
            return index if text[index] == LABEL_CLOSE else None
    return None


def formed(
    text: str,
    spans: Sequence[tuple[int, int]],
    opening: int,
    closing: int,
    image: bool,
    defined: Mapping[str, Definition],
) -> Use | None:
    """The use one matched bracket pair spells, or nothing where it spells none.

    A pair followed by an inline target is an inline use. A pair
    followed by a label this source defines, or whose own text this
    source defines, is a reference-style use. Everything else is literal
    text. `published` supplies the reference-style publication target.
    """
    kind = RESOURCE if image else LINK
    label = (opening + 1, closing)
    after = closing + 1
    if after < len(text) and text[after] == TARGET_OPEN:
        found = inline_target(text, after)
        if found is not None:
            return Use(kind, opening, label, found[0], found[2], title=found[1])
    if after < len(text) and text[after] == LABEL_OPEN:
        ending = label_close(text, after, spans)
        if ending is not None:
            spelled = text[after + 1 : ending]
            named = spelled if spelled.strip() else text[label[0] : label[1]]
            held = defined.get(normalizeReference(named))
            if held is not None:
                return Use(kind, opening, label, (after, ending + 1), ending + 1, held)
            return None
    held = defined.get(normalizeReference(text[label[0] : label[1]]))
    if held is None:
        return None
    return Use(kind, opening, label, (after, after), after, held)


def alternative(one: Use, found: Sequence[Use]) -> bool:
    """Whether one use is written inside an image's alternative content.

    An image's alternative content is a run of its own, so a use the
    scan has already read as lying within an image's label belongs to
    that run rather than to the label of anything enclosing the image.
    """
    return any(
        each.kind == RESOURCE
        and each.label[0] <= one.opening
        and one.end <= each.label[1]
        for each in found
    )


def uses(
    text: str, defined: Mapping[str, Definition], marker: bool = False
) -> list[Use]:
    """Locate link and image spans in one inline text run, in written order.

    Use `code_spans` to mask examples, `autolink_end` for angle-bracket uses,
    and `formed` for bracket pairs. Escaped brackets are literal text. Pair
    each closing bracket with its nearest open bracket; a link enclosing
    another link is literal unless `alternative` places that use inside an
    image's alternative content. Pass over each completed use whole.
    The supplied marker flag identifies a task opening recognized by
    `profile.linked_marker`.
    """
    spans = code_spans(text)
    stack: list[tuple[int, bool]] = []
    found: list[Use] = []
    at = 0
    while at < len(text):
        if escaped(text, at) or masked(spans, at):
            at += 1
            continue
        if text[at] == ANGLE_OPEN:
            closing = autolink_end(text, at, spans)
            if closing is not None:
                label = (at + 1, closing - 1)
                found.append(
                    Use(
                        LINK,
                        at,
                        label,
                        (closing, closing),
                        closing,
                        autolink=True,
                    )
                )
                at = closing
                continue
        if text[at] == LABEL_OPEN:
            image = at > 0 and text[at - 1] == IMAGE and not escaped(text, at - 1)
            stack.append((at, image))
            at += 1
            continue
        if text[at] == LABEL_CLOSE and stack:
            opening, image = stack.pop()
            one = formed(text, spans, opening, at, image, defined)
            if one is None:
                at += 1
                continue
            if one.kind == LINK and any(
                each.kind == LINK
                and not each.autolink
                and each.opening > opening
                and not alternative(each, found)
                for each in found
            ):
                at += 1
                continue
            found.append(one)
            at = one.end
            continue
        at += 1
    found.sort(key=lambda one: one.opening)
    if marker and found:
        first = found[0]
        if text[first.label[0] : first.label[1]] in MARKER_LABELS:
            return found[1:]
    return found


def destinations(inline: Token) -> list[tuple[str, str, frozenset[str]]]:
    """Each inline link's destination, opening text and requested preset tags.

    Read links through `source.events`, their text through `source.opening_text`,
    and their tags through `tags.read`, retaining event order.
    """
    return [
        (
            str(child.attrGet(HREF) or ""),
            opening_text(children, at),
            read_tags(str(child.attrGet("title") or "")),
        )
        for children, at, child in events(inline.children or [])
        if child.type == LINK_OPEN
    ]


def carried(children: Sequence[Token] | None) -> int:
    """How many link and image uses one run of inline events carries."""
    return sum(1 for _ in events(children or []))


def authored(written: str) -> tuple[str, str]:
    """One definition's destination and title, as the source spelled them."""
    closing = next(
        (
            at
            for at in range(len(written))
            if written[at] == LABEL_CLOSE and not escaped(written, at)
        ),
        None,
    )
    if closing is None or COLON not in written[closing:]:
        raise Unrewritable(f"the definition {written!r} names no destination")
    opening = skipped(written, written.index(COLON, closing) + 1)
    ending = target_end(written, opening)
    if ending is None:
        ending = len(written)
    return written[opening:ending], written[ending:].strip()


def definitions(
    references: Mapping[str, Mapping[str, Any]], physical: Sequence[str]
) -> dict[str, Definition]:
    """Authored definitions keyed by the parser's reference labels.

    Labels come from the supplied `profile.REFERENCES` environment. Remove each
    line's `source.opening_markers` before `authored` captures its destination
    and title; retain the definition's content-line span.
    """
    found: dict[str, Definition] = {}
    for label, held in references.items():
        start, end = held[MAP]
        written = "".join(
            line[len(opening_markers(line)) :] for line in physical[start:end]
        )
        destination, title = authored(written)
        found[label] = Definition(destination, title, (start, end))
    return found


def published(
    held: Definition, destination: str | None, names: Sequence[str] = ()
) -> str:
    """The inline target for a reference definition and an optional destination.

    Use the supplied destination when present, otherwise the definition's
    authored destination. Carry its authored title, extending it through
    `gained` when names are supplied, or construct a new title through
    `title_names` when absent.
    """
    target = held.destination if destination is None else destination
    title = held.title
    if names:
        title = gained(title, names) if title else f'"{title_names(names)}"'
    shown = f"{SPACE}{title}" if title else ""
    return f"{TARGET_OPEN}{target}{shown}{TARGET_CLOSE}"


def edits(
    one: Use, destination: str | Titled | Followed | None, label: str, text: str = ""
) -> list[tuple[int, int, str]]:
    """The replacement spans for one use and its supplied publication data.

    `published` supplies reference-style targets. Inline targets receive their
    destination and any `Titled` names through `gained` or `title_names`.
    `closure.published_text` supplies the label prefix to edit. A `Followed`
    suffix joins an edit already ending at the use's end, or occupies its own
    empty span there. Keep these spans disjoint so nested uses remain editable.
    """
    names: tuple[str, ...] = ()
    found: list[tuple[int, int, str]] = []
    after = ""
    if isinstance(destination, Titled):
        names = destination.names
        destination = destination.destination
    if isinstance(destination, Followed):
        after = destination.after
        destination = destination.destination
    if one.definition is not None:
        found.append((*one.target, published(one.definition, destination, names)))
    elif destination is not None:
        if names and one.title is None:
            found.append((*one.target, f'{destination} "{title_names(names)}"'))
        else:
            found.append((*one.target, destination))
        if names and one.title is not None:
            start, end = one.title
            titled = gained(text[start:end], names)
            found.append((start, end, titled))
    shown = None if destination is None else published_text(label, filed(destination))
    if shown is not None and shown != label:
        lead = opened(label)
        assert lead is not None
        prefix = shown[: len(shown) - (len(label) - lead.after)]
        found.append((one.label[0], one.label[0] + lead.after, prefix))
    if after:
        ending = next((at for at, edit in enumerate(found) if edit[1] == one.end), None)
        if ending is None:
            found.append((one.end, one.end, after))
        else:
            start, end, written = found[ending]
            found[ending] = (start, end, written + after)
    return found


def continuing_markers(line: str) -> str:
    """The quote markers and indent a later line of one paragraph opens with.

    A list marker opens no later line of a paragraph: one that would
    open an item interrupts the paragraph, and any other is its text.
    """
    written = CONTINUING.match(line)
    assert written is not None
    return written.group(0)


def wrapper(text: str) -> list[tuple[int, int, str]]:
    """The spans a command block's four tags occupy, each edited to nothing.

    The opening tags stand first in the block and the closing tags last.
    Where nothing but blanks follows the opening tags on their line, the
    deletion runs on through the line feed and the quote markers and indent
    opening the next line, so that line's content takes the first line's
    place beside any marker the first line opened with. Where nothing but
    quote markers and indent precede the closing tags on their line, the
    deletion runs back to the line feed ending the line before, so the
    content above ends the block.
    """
    opening = "".join(COMMAND_OPEN)
    closing = "".join(COMMAND_CLOSE)
    start = text.index(opening)
    end = start + len(opening)
    feed = text.find(LINE_FEED, end)
    if feed != -1 and not text[end:feed].strip():
        end = feed + 1 + len(continuing_markers(text[feed + 1 :]))
    close = text.rindex(closing)
    after = close + len(closing)
    line = text.rfind(LINE_FEED, 0, close)
    if line >= end and len(continuing_markers(text[line + 1 :])) >= close - line - 1:
        close = line
    return [(start, end, ""), (close, after, "")]


def unwrapped(
    text: str, one: Use, children: Sequence[Token], at: int
) -> list[tuple[int, int, str]]:
    """The spans of a strong emphasis enclosing one link's whole text, if it has one.

    The parser says where the emphasis opens and closes: it encloses the
    whole text when, empty text aside, it opens on the event after the
    link opens and closes on the event before the link closes, and the
    label opens and closes with its asterisks.
    """
    closing = next(
        (
            after
            for after in range(at + 1, len(children))
            if children[after].type == LINK_CLOSE
        ),
        len(children),
    )
    inside = [
        child
        for child in children[at + 1 : closing]
        if child.type != TEXT or child.content
    ]
    start, end = one.label
    if (
        len(inside) < 2
        or (inside[0].type, inside[-1].type) != (STRONG_OPEN, STRONG_CLOSE)
        or not text.startswith(STRONG, start)
        or not text.endswith(STRONG, start, end)
    ):
        return []
    depth = 0
    for child in inside[:-1]:
        depth += {STRONG_OPEN: 1, STRONG_CLOSE: -1}.get(child.type, 0)
        if depth == 0:
            return []
    return [(start, start + len(STRONG), ""), (end - len(STRONG), end, "")]


def references(text: str, found: Sequence[Use]) -> list[tuple[int, int, str]]:
    """Each character reference the parser decodes, as its span and its character.

    The scan is the parser's own unescaping pattern, so a backslash
    escape is read where it stands and the reference it escapes stays
    text, and a reference naming no character is the text it is.
    """
    spans = code_spans(text) + [
        (one.opening, one.end) if one.autolink else (one.label[1], one.end)
        for one in found
    ]
    held: list[tuple[int, int, str]] = []
    for written in UNESCAPE_ALL_RE.finditer(text):
        name = written.group(2)
        if name is None or masked(spans, written.start()):
            continue
        character = replaceEntityPattern(written.group(), name)
        if character != written.group():
            held.append((written.start(), written.end(), character))
    return held


def compacted(
    text: str, inline: Token, found: Sequence[Use]
) -> list[tuple[int, int, str]]:
    """The edits that publish one command block as its content."""
    applied = wrapper(text) + references(text, found)
    for one, (children, at, _child) in zip(
        found, events(inline.children or []), strict=True
    ):
        if one.kind == LINK and not one.autolink:
            applied.extend(unwrapped(text, one, children, at))
    return applied


def opens_block(content: str, first: bool) -> bool:
    """Whether one line of a paragraph is read as anything but that paragraph's text.

    The first line opens the paragraph and is read on its own; a later
    line continues it and is read beneath a line of text, where a block
    that cannot interrupt a paragraph is text as well.
    """
    read = content if first else f"{TEXT_LINE}{LINE_FEED}{content}"
    return tuple(token.type for token in reader().parse(read)) != PARAGRAPH


def kept_as_text(written: str, starts: Sequence[int]) -> list[int]:
    """Where a compacted command block's lines take a backslash to stay its text.

    Each start is where one line's content opens, past its container
    markers. The tags a compaction drops and the references it decodes
    can leave a line opening with a character the parser reads as a
    block of its own, such as `>` opening a quote, `#` a heading or
    `1.` a list. A backslash before that character, or before the
    delimiter after a list number, is the Markdown escaping that keeps
    the line its paragraph's text.
    """
    found: list[int] = []
    first = True
    for start in sorted(set(starts)):
        feed = written.find(LINE_FEED, start)
        content = written[start : len(written) if feed == -1 else feed]
        if not content.strip():
            continue
        if opens_block(content, first):
            at = ESCAPABLE.match(content)
            assert at is not None
            if content[at.end() : at.end() + 1] in tuple(punctuation):
                found.append(start + at.end())
        first = False
    return found


def paragraph_of(written: str, starts: Sequence[int]) -> str:
    """One compacted command block as its paragraph's lines, past their markers.

    Each start is where one line's content opens, so the lines read
    together are what the block's container holds, and a line the
    compaction emptied holds nothing of it.
    """
    held = []
    for start in sorted(set(starts)):
        feed = written.find(LINE_FEED, start)
        content = written[start : len(written) if feed == -1 else feed]
        if content.strip():
            held.append(content)
    return LINE_FEED.join(held)


def moved(at: int, start: int, end: int, width: int) -> int:
    """One offset into a text, as one edit to that text leaves it.

    An offset the edited span precedes moves by what the replacement
    added or took away. One inside the span lands at the end of the
    replacement, because the text it stood between is gone, and one
    before the span does not move at all.
    """
    if at <= start:
        return at
    if at >= end:
        return at + width - (end - start)
    return start + width


def rewritten(
    physical: Sequence[str],
    inline: Token,
    assigned: Sequence[str | Titled | Followed | None],
    defined: Mapping[str, Definition],
) -> list[str]:
    """Apply publication edits to one inline token's original physical lines.

    Supply one destination per parsed link in written order; none leaves its
    destination authored. `cell` limits a table token to its own row extent.
    `uses` locates spans, `edits` supplies reference replacements, and
    `compacted` supplies command-block edits. Apply them last to first so
    earlier spans keep their coordinates.

    The result has one entry per original physical line. Inserted line feeds
    remain inside the entry receiving them; a line boundary swallowed by an
    edit maps to that replacement's end.
    """
    text = "".join(physical)
    column = inline.meta.get(COLUMN)
    scanned = text
    if column is not None:
        start, end = cell(text, column)
        scanned = f"{SPACE * start}{text[start:end]}{SPACE * (len(text) - end)}"
    found = uses(scanned, defined, bool(inline.meta.get(MARKER)))
    if len(found) != carried(inline.children):
        raise Unrewritable(
            f"the parser read {carried(inline.children)} use(s) against the "
            f"{len(found)} the emission can edit in place"
        )
    links = [one for one in found if one.kind == LINK]
    if len(links) != len(assigned):
        raise Unrewritable(
            f"the run resolved {len(assigned)} link(s) against {len(links)} the "
            f"emission can edit in place"
        )
    targets = dict(zip((id(one) for one in links), assigned, strict=True))
    labels = {id(one): text[one.label[0] : one.label[1]] for one in links}
    written = text
    bounds = list(accumulate(len(line) for line in physical))
    applied = [
        edit
        for one in found
        for edit in edits(one, targets.get(id(one)), labels.get(id(one), ""), text)
    ]
    starts: list[int] = []
    if command_block(inline.children or []):
        applied.extend(compacted(text, inline, found))
        starts = [len(opening_markers(physical[0]))] + [
            opening + len(continuing_markers(line))
            for opening, line in zip(bounds, physical[1:], strict=False)
        ]
    for start, end, replacement in sorted(applied, reverse=True):
        written = f"{written[:start]}{replacement}{written[end:]}"
        bounds = [moved(at, start, end, len(replacement)) for at in bounds]
        starts = [moved(at, start, end, len(replacement)) for at in starts]
    for at in sorted(kept_as_text(written, starts), reverse=True):
        written = f"{written[:at]}{ESCAPE}{written[at:]}"
        bounds = [moved(one, at, at, len(ESCAPE)) for one in bounds]
        starts = [moved(one, at, at, len(ESCAPE)) for one in starts]
    if starts and opens_block(paragraph_of(written, starts), True):
        raise Unrewritable(
            f"the command block {text!r} is read as more than its one paragraph "
            f"once compacted"
        )
    return [written[opening:closing] for opening, closing in pairwise([0, *bounds])]
