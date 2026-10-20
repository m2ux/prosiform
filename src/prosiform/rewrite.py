"""Rewriting a marked link to the destination the bundle assigned its target.

A bundle is assembled from the physical lines its sources wrote, and a
link destination sits inside one of those lines. The rewrite is
therefore an edit to a span of text rather than a re-rendering of the
content around it: everything outside the two spans one link occupies —
the mark and the destination — is the bytes the source wrote.

A span is located in the lines an inline token occupies, because that is
where the parser says inline content is. A code span is masked out
first, so a dependency written as an example inside backticks is text
the bundle carries as written, and a fenced block carries no inline
token at all. An image is passed over: a reference to a resource is
emitted as authored and rewritten by nothing, and the exclamation mark
is what tells one from a link.

The scan is cross-checked against the parser. Each inline token's sites
are counted against the marked links the parser read from the same
token, and a count that disagrees is a link the run resolved and cannot
rewrite, which is an internal fault rather than a bundle. A reference
style use is the case that reaches it today: the parser resolves one and
the source carries no inline destination to edit, so the conversion to
inline form has to land before the rewrite can.

The mark is authoring syntax. A rewritten link carries the text that
followed the mark, and the space an author separated the two by goes
with it, so `[¬ the rules]` and `[¬the rules]` both carry `the rules`.
A line break is not that separator: it is content the author wrote, and
dropping it would join two lines the source kept apart.
"""

from collections.abc import Sequence
from dataclasses import dataclass

from markdown_it.token import Token

from prosiform.closure import MARK, marked
from prosiform.source import LINK_OPEN, opening_text

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

SEPARATOR = " \t"


class Unrewritable(Exception):
    """A marked link the run resolved and the emission cannot edit in place."""


@dataclass(frozen=True)
class Site:
    """Where one marked link's two editable spans sit in the text holding it.

    The label span is the link's text, between its brackets, and the
    target span is the destination, which a title may follow inside the
    same parentheses and is left where it is.
    """

    label: tuple[int, int]
    target: tuple[int, int]


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


def label_end(text: str, at: int, spans: Sequence[tuple[int, int]]) -> int | None:
    """Where the label opened at one position closes, or nothing where it does not.

    A label carries balanced brackets, and a bracket an author escaped
    or wrote inside a code span is text rather than one of them.
    """
    depth = 0
    for index in range(at, len(text)):
        if escaped(text, index) or masked(spans, index):
            continue
        if text[index] == LABEL_OPEN:
            depth += 1
        elif text[index] == LABEL_CLOSE:
            depth -= 1
            if depth == 0:
                return index
    return None


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


def sites(text: str) -> list[Site]:
    """Each marked inline link one run of inline text carries, in written order.

    A link is read where the profile reads one: outside a code span, not
    opened by an escaped bracket, and not an image, which the
    exclamation mark ahead of the bracket spells.
    """
    spans = code_spans(text)
    found: list[Site] = []
    at = 0
    while at < len(text):
        if (
            text[at] != LABEL_OPEN
            or escaped(text, at)
            or masked(spans, at)
            or (at and text[at - 1] == IMAGE and not escaped(text, at - 1))
        ):
            at += 1
            continue
        closing = label_end(text, at, spans)
        if closing is None or not text[at + 1 :].startswith(MARK):
            at += 1
            continue
        if closing + 1 >= len(text) or text[closing + 1] != TARGET_OPEN:
            at += 1
            continue
        opening = closing + 2
        while opening < len(text) and text[opening].isspace():
            opening += 1
        ending = target_end(text, opening)
        if ending is None:
            at += 1
            continue
        found.append(Site((at + 1, closing), (opening, ending)))
        at = ending
    return found


def unmarked(label: str) -> str:
    """One marked link's text, the mark and the space separating it gone."""
    if not label.startswith(MARK):
        return label
    return label[len(MARK) :].lstrip(SEPARATOR)


def destinations(inline: Token) -> list[str]:
    """The destination of each marked link one inline token carries, in order."""
    children = inline.children or []
    return [
        str(child.attrGet("href") or "")
        for at, child in enumerate(children)
        if child.type == LINK_OPEN and marked(opening_text(children, at))
    ]


def rewritten(text: str, assigned: Sequence[str]) -> str:
    """One run of inline text, each marked link it carries pointing at its destination.

    The spans are edited last to first, so an earlier edit does not move
    the span the next one names.
    """
    found = sites(text)
    if len(found) != len(assigned):
        raise Unrewritable(
            f"{len(assigned)} marked link(s) resolved against {len(found)} the "
            f"emission can edit in place"
        )
    written = text
    for site, target in reversed(list(zip(found, assigned, strict=True))):
        start, end = site.target
        written = f"{written[:start]}{ANCHOR}{target}{written[end:]}"
        start, end = site.label
        written = f"{written[:start]}{unmarked(written[start:end])}{written[end:]}"
    return written
