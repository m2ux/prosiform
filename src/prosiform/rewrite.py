"""Source-local reference interpretation: a definition environment and its edits.

A bundle is assembled from the physical lines its sources wrote. The
rewrite is an edit to spans of text rather than a re-rendering of the
content around it: everything outside the spans one use occupies — the
mark, the destination, and the label a reference-style use names — is
the bytes the source wrote.

A definition is a block and a use is a span, so a destination or title
the author spelled across more than one line is published into a span
that lies within one. The published text carries the line feeds the
author wrote, and the rewrite reports its result as one entry for each
line the source wrote, holding an inserted line feed inside the entry
for the line that gained it. A caller slicing by the source's line
count therefore slices the same lines whatever the spelling cost.

A span is located in the lines an inline token occupies, because that is
where the parser says inline content is. Every cell of a table row
occupies that row's line, so a cell's span is located in the stretch of
the line its column was split from. A code span is masked out
first, so a dependency written as an example inside backticks is text
the bundle carries as written, and a fenced block carries no inline
token at all.

The scan reads brackets the way the profile's parser reads them. A
closing bracket pairs with the nearest bracket still open, a link whose
own label holds a link is the literal text it is, and a bracketed
run is a reference-style use only where this source's own definition
environment holds its label. An image's alternative content is a run of
its own, so a link written there is the image's and leaves an enclosing
link the link it is. That environment is this source's and no
other's, so a literal `[runner]` here stays literal however another
source defines the same label.

An autolink is a use among them, written between angle brackets rather
than brackets: the scan reads one where it sits, so the reading and the
parser agree on how many uses a run carries and in what order. The
parser reads it beside an enclosing link rather than within it, so a
link whose label holds one is the link it is. Its
destination is its own text and carries a scheme or an authority, so the
bundle assigns it none and the emission edits no span of it — every byte
between the angle brackets, and the brackets themselves, are the bytes
the source wrote.

A resolved reference-style use is published inline. The label keeps the
bytes the author wrote, so the visible text, an image's alternative
content and the escaping the author chose are preserved by carrying
them rather than by re-rendering them, and the destination and title
come from the definition as it was authored. A link the bundle assigned
a destination is published with that destination in place of the
authored one; every other destination is emitted as authored.

The scan is cross-checked against the parser. The uses one inline token
carries are counted against the uses the parser read from the same
token, and a count that disagrees is content the run resolved and
cannot edit, which is an internal fault rather than a bundle.

A mark survives the rewrite where it states who compiles the material. A
dispatch pointing at a bundle file is the one thing in the bundle saying
the material belongs to another agent, so its label reaches the bundle
opening with the dispatch mark and one blank. A deferral states when, a
composition where, and a set's dispatch-set sub-section states who,
which each destination already says, so their marks and the blanks
following them are dropped from the label they open.
A link the bundle took no destination for opens with no operator, because
the run refuses an operator naming anything but a Markdown document or
section under the root, and it is published as its author wrote it.

A command block is published as its content. Its four wrapper tags go,
and a line left holding nothing but a tag and the container markers
opening it goes with them, so the block's first and last lines are its
first and last content. A strong emphasis enclosing a link's whole text
is unwrapped, and every character reference the parser decodes is
written as the character it names. A reference in a code span, a link's
target or an autolink is the parser's text rather than a reference, so
it stays as written. A line left opening with a character the parser
reads as a block of its own takes a backslash before it, so every line
stays the text of the block's paragraph. The edits reach no span a
link's own edits reach, because a tag stands outside every use, a
strong delimiter inside a label, and a decoded reference outside every
target.
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

from prosiform.closure import filed, opened, published_text
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
    """One link-reference definition: what it names, and where it is written.

    The destination and the title are the text the author wrote, angle
    brackets and quotation marks included, because a use published
    inline carries the destination its source spelled rather than one
    the parser normalized. The lines are the lines of this source's
    content the definition occupies, which are the lines the bundle
    does not emit.
    """

    destination: str
    title: str
    lines: tuple[int, int]


@dataclass(frozen=True)
class Use:
    """One link or image use, as the spans of text its emission edits.

    The label is the content between the brackets, which holds the mark
    where the author wrote one. The target is the span the destination
    is written at: for an inline use it is the authored destination, and
    for a reference-style use it is the `[label]` that follows the
    label, which is empty where the use is written as a shortcut. An
    autolink's destination is the text between its angle brackets, so
    its target is the empty span at its close and its emission edits
    nothing. It is a link the parser reads beside an enclosing link
    rather than within it, so the one that carries it stays the link it
    is, and the flag is what the scan reads that from.
    """

    kind: str
    opening: int
    label: tuple[int, int]
    target: tuple[int, int]
    end: int
    definition: Definition | None = None
    autolink: bool = False


def escaped(text: str, at: int) -> bool:
    """Whether the character at one position is escaped by a backslash run."""
    count = 0
    index = at - 1
    while index >= 0 and text[index] == ESCAPE:
        count += 1
        index -= 1
    return count % 2 == 1


def code_spans(text: str) -> list[tuple[int, int]]:
    """Each code span one run of inline text carries, as the extent it occupies.

    A code span opens at a backtick string and closes at the next
    backtick string of the same length, which is the profile's own rule.
    An opener that never closes is the literal backticks it is written
    as, and the scan carries on past it.
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


def inline_target(text: str, at: int) -> tuple[tuple[int, int], int] | None:
    """The destination span and the end of the inline target opening at one position.

    The target runs from the parenthesis to the one closing it, holding
    a destination, an optional title, and the whitespace between them.
    A run the grammar does not admit is no inline target, and the
    brackets before it are read as a reference-style use or as the
    literal text they are.
    """
    opening = skipped(text, at + 1)
    ending = target_end(text, opening)
    if ending is None:
        return None
    scan = skipped(text, ending)
    if scan < len(text) and text[scan] in TITLE_CLOSERS and scan > ending:
        closing = title_end(text, scan)
        if closing is None:
            return None
        scan = skipped(text, closing)
    if scan >= len(text) or text[scan] != TARGET_CLOSE:
        return None
    return (opening, ending), scan + 1


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
    source defines, is a reference-style use the emission publishes
    inline. Everything else is the literal text the author wrote.
    """
    kind = RESOURCE if image else LINK
    label = (opening + 1, closing)
    after = closing + 1
    if after < len(text) and text[after] == TARGET_OPEN:
        found = inline_target(text, after)
        if found is not None:
            return Use(kind, opening, label, found[0], found[1])
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
    """Every link and image use one run of inline text carries, in written order.

    An autolink is one of them. It opens at an unescaped angle bracket
    outside a code span and closes at the next one, carrying an
    absolute URI or an email address as CommonMark spells them, and a
    bracketed run spelling neither is the text it is. The scan reads it
    where it sits, among the bracketed uses in written order, and
    passes over it whole. The parser reads it beside an enclosing link
    rather than within it, so a link whose label holds one is the link
    it is.

    The scan reads brackets as the parser reads them: a closing bracket
    pairs with the nearest bracket still open, a bracket an author
    escaped or wrote inside a code span is text, and a link whose own
    label holds a link is text as well, because a link holds no link.
    A link an image inside that label carries belongs to the image's
    alternative content, which is a run of its own, so it leaves the
    enclosing link the link it is. A pair the scan reads as a use is
    passed over whole, so a bracket inside a destination or a title
    opens nothing.

    A task marker the profile returned to literal text is the one
    bracket pair a definition cannot make a link of, and it opens the
    inline content that carries it.
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
    """Each inline link's destination, opening and requested preset tags.

    The opening is the literal text the link's content begins with,
    which is what a deferral is written in, so a caller classifying the
    link reads both halves of the question from one pass over the
    token.

    The order is written order, which is the order the emission reads
    its spans in, and an image's alternative content is a run of its
    own, so a link written inside one takes the destination assigned
    to the span that spells it and carries the opening of the run it
    was written in.
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
    """Every link-reference definition one source carries, by the label it answers to.

    The label is normalized as the profile normalizes one, so a use
    naming it in another case or spacing resolves against it. The lines
    are the lines of this source's content the definition occupies, and
    a definition a container carries is read without the markers the
    container opens its lines with.
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


def published(held: Definition, destination: str | None) -> str:
    """The inline target a reference-style use is published with.

    The destination is the one the bundle assigned the use's target
    where the bundle compiled that use, and the one its definition was
    authored with where it did not. The title is the definition's own, carried as
    the author spelled it, so a title the author broke across two lines
    reaches the bundle broken in the same place: the title is the
    author's text and the conversion moves it rather than reflowing it.
    """
    target = held.destination if destination is None else destination
    title = f"{SPACE}{held.title}" if held.title else ""
    return f"{TARGET_OPEN}{target}{title}{TARGET_CLOSE}"


def edits(one: Use, destination: str | None, label: str) -> list[tuple[int, int, str]]:
    """The spans one use's emission replaces, and what it writes at each.

    A use's label is the author's, so the span a use edits is its
    destination alone and no two spans one text produces overlap. A use
    the bundle assigned no destination is published with the bytes its
    author wrote.

    The one exception is a withheld link's mark, which is authoring
    syntax rather than content: the bundle took a destination for that
    link, and the destination states the withholding, so the mark and
    the blanks following it go, or become the dispatch mark and one
    blank for a dispatch pointing at a bundle file. The edit reaches the
    prefix of the label, which no nested use opens on, so it still
    overlaps nothing.

    The destination arrives whole. Where a link points is the bundle's
    question, and this writes the answer, so a fragment of the bundle
    and a path from the invocation working directory are published the
    same way.
    """
    found: list[tuple[int, int, str]] = []
    if one.definition is not None:
        found.append((*one.target, published(one.definition, destination)))
    elif destination is not None:
        found.append((*one.target, destination))
    shown = None if destination is None else published_text(label, filed(destination))
    if shown is not None and shown != label:
        lead = opened(label)
        assert lead is not None
        prefix = shown[: len(shown) - (len(label) - lead.after)]
        found.append((one.label[0], one.label[0] + lead.after, prefix))
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
    assigned: Sequence[str | None],
    defined: Mapping[str, Definition],
) -> list[str]:
    """The lines one run of inline text occupies, as the bundle publishes them.

    Each resolved reference-style use is published inline, and each
    link the bundle compiled points at the destination it assigned that
    link's target. One destination is supplied for each link the token
    carries, in written order, and a link the bundle did not compile is
    supplied none. A table cell's uses are read from its own stretch of
    the row's line, so each cell of one row is rewritten by its own call
    and the others' links are text to it. A command block's content is
    published as well as its links. The spans are edited last to first,
    so an earlier edit does not move the span the next one names.

    The result holds one entry for each line given, so the published
    text of a source line is found where that line was. A replacement
    carrying a line feed — a definition the author spelled across more
    than one line — makes its entry longer rather than making another
    entry, and a line boundary the replacement swallowed lands at the
    end of it.
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
        for edit in edits(one, targets.get(id(one)), labels.get(id(one), ""))
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
