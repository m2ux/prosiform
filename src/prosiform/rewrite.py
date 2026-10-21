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
where the parser says inline content is. A code span is masked out
first, so a dependency written as an example inside backticks is text
the bundle carries as written, and a fenced block carries no inline
token at all.

The scan reads brackets the way the profile's parser reads them. A
closing bracket pairs with the nearest bracket still open, a link whose
label already holds a link is the literal text it is, and a bracketed
run is a reference-style use only where this source's own definition
environment holds its label. That environment is this source's and no
other's, so a literal `[runner]` here stays literal however another
source defines the same label.

A resolved reference-style use is published inline. The label keeps the
bytes the author wrote, so the visible text, an image's alternative
content and the escaping the author chose are preserved by carrying
them rather than by re-rendering them, and the destination and title
come from the definition as it was authored. A compiled link takes the
destination the bundle assigned its target in place of the authored
one; every other destination is emitted as authored.

The scan is cross-checked against the parser. The uses one inline token
carries are counted against the uses the parser read from the same
token, and a count that disagrees is content the run resolved and
cannot edit, which is an internal fault rather than a bundle.

A mark survives the rewrite. The mark defers a compilation, so a link
carrying one is a link the bundle compiles none of, and its label is the
author's text like any other label: every byte of it reaches the bundle,
because an agent reading the bundle is what reads the mark next.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import accumulate, pairwise
from typing import Any

from markdown_it.common.utils import normalizeReference
from markdown_it.token import Token

from prosiform.profile import MARKER, MARKER_LABELS
from prosiform.source import (
    HREF,
    LINK_OPEN,
    opening_markers,
    opening_text,
)
from prosiform.source import (
    IMAGE as IMAGE_TOKEN,
)

ANCHOR = "#"
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

SPACE = " "

TITLE_CLOSERS = {'"': '"', "'": "'", TARGET_OPEN: TARGET_CLOSE}

LINK = "link"
RESOURCE = "resource"

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
    label, which is empty where the use is written as a shortcut.
    """

    kind: str
    opening: int
    label: tuple[int, int]
    target: tuple[int, int]
    end: int
    definition: Definition | None = None


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


def uses(
    text: str, defined: Mapping[str, Definition], marker: bool = False
) -> list[Use]:
    """Every link and image use one run of inline text carries, in written order.

    The scan reads brackets as the parser reads them: a closing bracket
    pairs with the nearest bracket still open, a bracket an author
    escaped or wrote inside a code span is text, and a link whose label
    already holds a link is text as well, because a link holds no link.
    A pair the scan reads as a use is passed over whole, so a bracket
    inside a destination or a title opens nothing.

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
                each.kind == LINK and each.opening > opening for each in found
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


def destinations(inline: Token) -> list[tuple[str, str]]:
    """Each link one inline token carries, as its destination and its opening.

    The opening is the literal text the link's content begins with,
    which is what a deferral is written in, so a caller classifying the
    link reads both halves of the question from one pass over the
    token.
    """
    children = inline.children or []
    return [
        (str(child.attrGet(HREF) or ""), opening_text(children, at))
        for at, child in enumerate(children)
        if child.type == LINK_OPEN
    ]


def carried(children: Sequence[Token] | None) -> int:
    """How many link and image uses one run of inline events carries.

    An image's alternative content is a run of its own, and a link
    written inside one is a use the emission edits where it sits.
    """
    total = 0
    for child in children or []:
        if child.type == LINK_OPEN:
            total += 1
        elif child.type == IMAGE_TOKEN:
            total += 1 + carried(child.children)
    return total


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


def edits(one: Use, destination: str | None) -> list[tuple[int, int, str]]:
    """The spans one use's emission replaces, and what it writes at each.

    A use's label is the author's and stays as written, so the span a
    use edits is its destination alone and no two spans one text
    produces overlap. A use the bundle assigned no destination is
    published with the bytes its author wrote.
    """
    found: list[tuple[int, int, str]] = []
    target = None if destination is None else f"{ANCHOR}{destination}"
    if one.definition is not None:
        found.append((*one.target, published(one.definition, target)))
    elif target is not None:
        found.append((*one.target, target))
    return found


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
    supplied none. The spans are edited last to first, so an earlier
    edit does not move the span the next one names.

    The result holds one entry for each line given, so the published
    text of a source line is found where that line was. A replacement
    carrying a line feed — a definition the author spelled across more
    than one line — makes its entry longer rather than making another
    entry, and a line boundary the replacement swallowed lands at the
    end of it.
    """
    text = "".join(physical)
    found = uses(text, defined, bool(inline.meta.get(MARKER)))
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
    written = text
    bounds = list(accumulate(len(line) for line in physical))
    applied = [edit for one in found for edit in edits(one, targets.get(id(one)))]
    for start, end, replacement in sorted(applied, reverse=True):
        written = f"{written[:start]}{replacement}{written[end:]}"
        bounds = [moved(at, start, end, len(replacement)) for at in bounds]
    return [written[opening:closing] for opening, closing in pairwise([0, *bounds])]
