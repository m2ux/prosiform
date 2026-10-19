"""One source document's content, and the transport metadata carried ahead of it.

A file holds two things the author did not write as instructions: a
leading byte-order mark, which is a text-file convention, and a leading
frontmatter block, which is metadata for whatever reads the file. Neither
is content, and both would otherwise be published as body. The scan below
removes them before anything parses the document.

The scan is deterministic and reads nothing it removes. It parses no
YAML, interprets no metadata and executes nothing: it compares two
physical lines against two literals, and the narrowness of that
comparison is the whole of the policy. An indented delimiter, a delimiter
carrying a trailing space, a TOML `+++` fence, JSON metadata, and a `---`
under a blank line are each a line the comparison rejects, so each is
body the bundle carries. A document meaning to open on a horizontal rule
spells it another way, `***` among them; the leading `---` is reserved.

A removal moves every line after it, so the content is returned with the
line it began on. A location at line `n` of the content sits at line
`n + first_line - 1` of the file, and that expression is the only place
the shift is applied. A byte-order mark sits at the head of line 1, which
stays line 1, so the mark shifts no coordinate; the block does.
"""

import re
from dataclasses import dataclass

ENCODING = "utf-8"
MARK = "﻿"

OPENER = "---"
CLOSERS = ("---", "...")

LINE_FEED = "\n"
CARRIAGE_RETURN = "\r"

PHYSICAL_LINE = re.compile(r"[^\n]*\n|[^\n]+")

UNTERMINATED_FRONTMATTER = "E_UNTERMINATED_FRONTMATTER"


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

    def line(self, at: int | None) -> int | None:
        """The line of the original file one line of this content occupies."""
        return None if at is None else at + self.first_line - 1


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


def decode(data: bytes) -> str:
    """One source's bytes as text, which they are only if they are valid UTF-8.

    The strict error handler is the one that raises. Substituting a
    replacement character would put a byte the author never wrote into
    content the tool promises to preserve, and then report success.
    """
    return data.decode(ENCODING)


def content(text: str) -> Source:
    """One source's content, its leading transport metadata removed.

    Exactly one byte-order mark is removed, and a second is content. The
    frontmatter opener is the first physical line where that line is the
    three characters of `OPENER`; the block closes at the next physical
    line equal to one of `CLOSERS`, and the opener, the metadata, the
    closer and the closer's terminator go together.
    """
    body = text.removeprefix(MARK)
    physical = lines(body)
    if not physical or bare(physical[0]) != OPENER:
        return Source(body)
    for index, line in enumerate(physical[1:], start=1):
        if bare(line) in CLOSERS:
            return Source("".join(physical[index + 1 :]), index + 2)
    raise Unterminated(1)
