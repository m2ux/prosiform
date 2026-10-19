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

A group is assembled from the maximal regions the parse found, in source
order, each carried as the bytes its source wrote. What lies between two
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
makes room. A shift that would place a heading beyond the sixth level is
an overflow rather than a heading, and the group refuses it.

A destination is the fragment a renderer generates for a bundled
heading: the heading's slug, carrying the ordinal the renderer appends
where an earlier heading already took that slug. That is the rule the
source model applies over one document's headings, applied here over the
headings the bundle emits, so the entry line's link resolves in the
document a reader opens.
"""

import re
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import PurePosixPath

from markdown_it.token import Token

from prosiform.profile import SUFFIXES
from prosiform.source import headings, level, slug, visible

MAX_LEVEL = 6
SHIFT = 1

AMBIGUOUS_FILE_GROUP = "E_AMBIGUOUS_FILE_GROUP"
HEADING_DEPTH_OVERFLOW = "E_HEADING_DEPTH_OVERFLOW"

SEPARATOR = "\n\n"
TERMINATOR = "\n"

ATX = "#"
HEADING_OPEN = "heading_open"

ANCHOR = "#"

ENTRY_OPENING = "This bundle was built for "
ENTRY_CLOSING = "; everything else is material it references."
ENTRY_JOIN = ", "
ENTRY_LAST = " and "

OPENERS = "\\`*_[]<>&~!#"
OPENER = re.compile(f"([{re.escape(OPENERS)}])")

ATX_PREFIX = re.compile(r"^( {0,3})(#{1,6})")


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
    """One ATX heading's first line, its level moved down by the group's shift."""
    return ATX_PREFIX.sub(
        lambda written: written.group(1) + ATX * (len(written.group(2)) + by),
        line,
        count=1,
    )


def region(physical: Sequence[str], token: Token, by: int) -> str:
    """One region as the lines its source occupies, its heading level shifted."""
    start, end = token.map or (0, 0)
    carried = list(physical[start:end])
    if by and token.type == HEADING_OPEN and is_atx(token):
        carried[0] = shifted(carried[0], by)
    return "".join(carried).rstrip("\r\n")


def group(path: str, tokens: Sequence[Token], physical: Sequence[str]) -> Group:
    """One file group: its generated heading, then the regions its source emits."""
    title = heading_text(path)
    absorbing = absorbed(tokens, title)
    by = 0 if absorbing is not None else SHIFT
    emitted = [f"{ATX} {escaped(title)}"]
    shown = [title]
    text = shown_text(tokens)
    for token in regions(tokens):
        if token is absorbing:
            continue
        if token.type == HEADING_OPEN:
            depth = level(token) + by
            if depth > MAX_LEVEL:
                raise Overflow(text[id(token)], depth)
            shown.append(text[id(token)])
        emitted.append(region(physical, token, by))
    return Group(SEPARATOR.join(emitted), tuple(shown))


def assemble(line: str, groups: Sequence[Group]) -> str:
    """The bundle: its entry line, then each group, terminated by one newline."""
    return SEPARATOR.join([line, *(one.text for one in groups)]) + TERMINATOR
