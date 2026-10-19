"""The bundle: one file group for each contributing source, under one entry line.

A group is a source document, headed by one generated H1 whose visible
text is the document's normalized root-relative path with the Markdown
extension removed. The path is escaped as literal heading text, so
punctuation in a filename names a file rather than opening a link, an
image, emphasis, code, raw HTML, an entity or a strikethrough, or closing
the heading that carries it. Two
documents sharing a basename in different directories carry their
directories in their headings and stay distinguishable; two whose paths
differ only by Markdown extension produce one heading text twice, which
the command refuses as an ambiguous file group.

A group is assembled from the maximal regions the run selected, in
source order, each carried as the bytes its source wrote. A whole
document selects every region it holds; a fragment selects the regions
of the section it names. What lies between two
regions is not source content: a blank line above the first region, the
blank line a removed reference definition was separated by, and the
spacing between any two blocks are the bundle's own, and the bundle
writes one blank line between regions wherever it joins them. Inside a
region nothing is touched, so an indented thematic break keeps its
indent, a delimiter keeps its trailing spaces and a code example keeps
its bytes.

The file heading absorbs the source's first heading when that heading is
the document's only H1 and its slug equals the final segment of the
path, because the file heading already names it. A group whose title is
absorbed keeps its source heading levels; every other group moves each
emitted heading down one level, the file heading taking the level that
makes room. A heading a retained container carries is shifted where it
sits, so the container keeps the structure it had. A shift that would
place any emitted heading beyond the sixth level is an overflow rather
than a heading, and the group refuses it.

A shift edits an ATX heading's number signs, which are the level the
author wrote. A Setext heading writes its level as an underline instead,
so a shifted group emits it as the ATX heading of the same level,
carrying the inline source its content lines hold joined into the one
line an ATX heading is, each line break reading as the space it already
read as. A group that shifts by nothing has no level to write, so the
heading stays the Setext heading its source wrote.

A destination is the fragment a renderer generates for a bundled
heading: the heading's slug, carrying the ordinal the renderer appends
where an earlier heading already took that slug. That is the rule the
source model applies over one document's headings, applied here over the
headings the bundle emits, so the entry line's link resolves in the
document a reader opens.
"""

import re
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import PurePosixPath

from markdown_it.token import Token

from prosiform.profile import SUFFIXES
from prosiform.source import (
    LINE_FEED,
    Selection,
    bare,
    headings,
    level,
    regions,
    slug,
    visible,
)

MAX_LEVEL = 6
SHIFT = 1

AMBIGUOUS_FILE_GROUP = "E_AMBIGUOUS_FILE_GROUP"
HEADING_DEPTH_OVERFLOW = "E_HEADING_DEPTH_OVERFLOW"

SEPARATOR = "\n\n"
TERMINATOR = "\n"

ATX = "#"
SPACE = " "
HEADING_OPEN = "heading_open"

ANCHOR = "#"

ENTRY_OPENING = "This bundle was built for "
ENTRY_CLOSING = "; everything else is material it references."
ENTRY_JOIN = ", "
ENTRY_LAST = " and "

OPENERS = "\\`*_[]<>&~!#"
OPENER = re.compile(f"([{re.escape(OPENERS)}])")

ATX_MARKER = re.compile(r"^([^#]*)(#{1,6})")
CONTAINER_PREFIX = re.compile(
    r"^(?:[ \t]*(?:>|[-*+](?=[ \t])|\d{1,9}[.)](?=[ \t])))*[ \t]*"
)
CLOSING_SEQUENCE = re.compile(r"(^|[ \t])(#+)([ \t]*)$")


class Overflow(Exception):
    """A heading the group's shift would place beyond the sixth level."""

    def __init__(self, heading: str, level: int) -> None:
        super().__init__(f"the heading {heading!r} would be emitted at level {level}")
        self.heading = heading
        self.level = level


@dataclass(frozen=True)
class Group:
    """One file group: the Markdown it emits and the headings it emits, in order."""

    text: str
    headings: tuple[str, ...]
    entries: tuple[int, ...]


def heading_text(path: str) -> str:
    """One source's file heading: its root-relative path, the Markdown suffix gone.

    The suffix is classified case-insensitively, as the profile
    classifies one, and the rest of the path keeps the spelling the
    filesystem holds.
    """
    spelled = PurePosixPath(path)
    if spelled.suffix.lower() in SUFFIXES:
        return str(spelled.with_suffix(""))
    return path


def final_segment(title: str) -> str:
    """The last segment of a file heading's path, which a title can be absorbed by."""
    return PurePosixPath(title).name


def escaped(text: str) -> str:
    """One string as literal Markdown text, read as the characters it carries.

    A backslash precedes each character that can begin a construct the
    profile reads: an escape, a code span, emphasis, a link, an angle
    bracket, an entity, a strikethrough and an image marker. It also
    precedes the number sign, which ends one: a heading whose text runs
    to a space and a number sign carries a closing sequence, and a
    renderer takes that sequence off the heading rather than showing it.
    """
    return OPENER.sub(r"\\\1", text)


def entry_line(named: Sequence[tuple[str, str]]) -> str:
    """The bundle's opening line: each entry reference, linked to its destination.

    It states what the bundle was built for and nothing more. It carries
    no execution verb, because an entry reference names a document rather
    than a procedure the tool can recognize as one.
    """
    links = [f"[{escaped(text)}]({ANCHOR}{target})" for text, target in named]
    return f"{ENTRY_OPENING}{listed(links)}{ENTRY_CLOSING}"


def listed(items: Sequence[str]) -> str:
    """Several items as one phrase, the last joined by a word rather than a comma."""
    if len(items) == 1:
        return items[0]
    return f"{ENTRY_JOIN.join(items[:-1])}{ENTRY_LAST}{items[-1]}"


def is_atx(token: Token) -> bool:
    """Whether a heading is written with the heading syntax a shift edits."""
    return token.markup.startswith(ATX)


def shown_text(tokens: Sequence[Token]) -> dict[int, str]:
    """The visible text of each heading token, keyed by the token's identity."""
    return {id(opening): visible(inline) for opening, inline in headings(tokens)}


def absorbed(tokens: Sequence[Token], title: str) -> Token | None:
    """The source heading the file heading absorbs, where the source carries one.

    A title the path already names is absorbed: the document's first
    heading, where that heading is its only H1, sits at the document
    level, and slugs to the final segment of the file heading's path.
    """
    carried = list(headings(tokens))
    if not carried:
        return None
    opening, inline = carried[0]
    if level(opening) != 1 or sum(1 for one, _ in carried if level(one) == 1) != 1:
        return None
    if not any(token is opening for token in regions(tokens)):
        return None
    if slug(visible(inline)) != final_segment(title):
        return None
    return opening


def shifted(line: str, by: int) -> str:
    """One ATX heading's line, its level moved down by the group's shift.

    The level is written in the first number-sign run the line carries:
    what precedes it is the indent and the container markers the line
    opens with, and no container marker is a number sign.
    """
    return ATX_MARKER.sub(
        lambda written: written.group(1) + ATX * (len(written.group(2)) + by),
        line,
        count=1,
    )


def opening_markers(line: str) -> str:
    """The container markers and indent one line opens with, before its content."""
    written = CONTAINER_PREFIX.match(line)
    return "" if written is None else written.group(0)


def terminator(line: str) -> str:
    """The line ending one physical line carries, which may be nothing at all."""
    return line[len(bare(line)) :]


def literal_closing(text: str) -> str:
    """One heading's text with a trailing number-sign run kept as text.

    An ATX heading ends at a run of number signs a space precedes, and a
    renderer takes that run off the heading rather than showing it. A
    Setext heading has no closing sequence, so a run ending its text is
    text, and a backslash before the run keeps it the text it was.
    """
    return CLOSING_SEQUENCE.sub(r"\1\\\2\3", text)


def converted(carried: Sequence[str], depth: int) -> str:
    """One Setext heading as the ATX heading of the same level and text.

    A Setext heading writes its level as an underline rather than as a
    prefix, so it is rewritten rather than edited. Its content lines
    carry the inline source the author wrote, and they join into the
    one line an ATX heading is, separated by the space a reader already
    reads in place of each line break. The rewritten line opens with
    the markers the heading opened with, so the container that holds
    the heading holds it still, and a number-sign run ending its text
    is escaped, because an ATX heading ends at one.
    """
    written = [
        bare(line)[len(opening_markers(line)) :].strip() for line in carried[:-1]
    ]
    text = literal_closing(SPACE.join(written))
    return f"{opening_markers(carried[0])}{ATX * depth} {text}"


def carried_headings(tokens: Sequence[Token], token: Token) -> list[Token]:
    """Every heading one region holds, the region's own heading included."""
    start, end = token.map or (0, 0)
    return [
        opening
        for opening, _ in headings(tokens)
        if opening.map is not None and start <= opening.map[0] < end
    ]


def region(
    physical: Sequence[str], tokens: Sequence[Token], token: Token, by: int
) -> str:
    """One region as the lines its source occupies, each heading it holds shifted.

    A heading a container carries is shifted where it sits, so the
    container keeps the structure it had, and everything that is not a
    heading is carried as the bytes its source wrote. The headings are
    rewritten last to first, because a Setext heading becomes one line
    where its source wrote several and an earlier heading's lines would
    otherwise move out from under it.
    """
    start, end = token.map or (0, 0)
    carried = list(physical[start:end])
    if not by:
        return "".join(carried).rstrip("\r\n")
    for opening in reversed(carried_headings(tokens, token)):
        at, closing = opening.map or (0, 0)
        if is_atx(opening):
            carried[at - start] = shifted(carried[at - start], by)
        else:
            written = converted(physical[at:closing], level(opening) + by)
            carried[at - start : closing - start] = [
                written + terminator(physical[closing - 1])
            ]
    return "".join(carried).rstrip("\r\n")


def emitted_text(token: Token, text: str, by: int) -> str:
    """The visible text the group emits for one heading.

    A Setext heading the group converts carries on one line what its
    source wrote on several, so each line break between them reads as
    the space it already read as.
    """
    if by and not is_atx(token):
        return SPACE.join(part.strip() for part in text.split(LINE_FEED))
    return text


def group(
    path: str,
    tokens: Sequence[Token],
    physical: Sequence[str],
    selected: Selection | None = None,
) -> Group:
    """One file group: its generated heading, then the regions the run selected.

    A selection of None is the whole document, which the file heading
    itself is the entry to. A selection of sections emits the regions it
    names and nothing else, and each heading an entry reference resolved
    to is the entry to the destination that heading takes.

    A title is absorbed only where the group emits it, because the
    absorption is the file heading standing in for a heading the group
    carries. A group that emits none therefore shifts, and a reference
    to an absorbed title resolves to the file heading's own destination.
    """
    title = heading_text(path)
    emitting = (
        {id(token) for token in regions(tokens)}
        if selected is None
        else {id(token) for token in selected.regions}
    )
    naming: set[int] = (
        set() if selected is None else {id(token) for token in selected.named}
    )
    absorbing = absorbed(tokens, title)
    if absorbing is not None and id(absorbing) not in emitting:
        absorbing = None
    by = 0 if absorbing is not None else SHIFT
    emitted = [f"{ATX} {escaped(title)}"]
    shown = [title]
    entries = [0] if selected is None else []
    text = shown_text(tokens)
    for token in regions(tokens):
        if id(token) not in emitting:
            continue
        if token is absorbing:
            if id(token) in naming:
                entries.append(0)
            continue
        for opening in carried_headings(tokens, token):
            depth = level(opening) + by
            if depth > MAX_LEVEL:
                raise Overflow(text[id(opening)], depth)
        if token.type == HEADING_OPEN:
            if id(token) in naming:
                entries.append(len(shown))
            shown.append(emitted_text(token, text[id(token)], by))
        emitted.append(region(physical, tokens, token, by))
    return Group(SEPARATOR.join(emitted), tuple(shown), tuple(entries))


def assemble(line: str, groups: Sequence[Group]) -> str:
    """The bundle: its entry line, then each group, terminated by one newline."""
    return SEPARATOR.join([line, *(one.text for one in groups)]) + TERMINATOR
