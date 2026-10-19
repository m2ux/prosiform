"""A reference's path identity: the document it names and the section inside it.

A link string is not a path. Percent escapes, an encoded delimiter, a
query and a relative segment each change which file a reference names, so
two references are the same dependency, or a reference is one the profile
resolves at all, only after the sequence below has run over both. Every
later stage compares what this module returned rather than the text an
author wrote, because a comparison of the written text answers a
different question.

The sequence is the design's, step for step, and its order is the whole
of its correctness.

- **The components split before anything is decoded.** The fragment opens
  at the first number sign and the query at the first question mark
  before it, read in the authored text, so `notes%23draft.md` names one
  filename carrying a number sign rather than a document and a section.
- **A scheme or an authority ends the sequence.** Such a reference is not
  a local document. It is classified and returned, never opened, fetched
  or interpreted, and which scheme it carries decides nothing.
- **A query is refused**, an explicitly empty one included. A local
  Markdown document is a file, and a file takes no query.
- **Each path segment and the fragment decode exactly once**, as UTF-8,
  with every escape required to be a percent and two hexadecimal digits.
  A segment decodes alone, so an escape can never produce a delimiter:
  a decoded separator is a character in a name no root holds, which the
  next step refuses, rather than a separator the normalization would act
  on.
- **A NUL, a control character and a separator are refused**, whether the
  separator was decoded from an escape or written as a backslash. Local
  paths are spelled with forward slashes.
- **`.` and `..` normalize against the base** the reference is written
  relative to, and a path that walks above that base names a document the
  allowed root cannot contain.
- **An absent fragment and an empty one are one whole-document
  reference**, and a fragment that is present is looked up as the exact
  text it decoded to.

A drive letter is read before a scheme, because `C:` is spelled as both.
A drive path names a local document the root cannot contain, and reading
it as a scheme would emit it as authored.

The module reaches no filesystem, holds no parser and writes no
diagnostic. It says what a reference names and what kind of refusal a
reference that names nothing resolvable is; the command says which code
and which exit status that refusal returns.
"""

import re
from collections.abc import Sequence
from dataclasses import dataclass

from prosiform.source import ENCODING

FRAGMENT = "#"
QUERY = "?"
SEPARATOR = "/"
BACKSLASH = "\\"
CURRENT = "."
PARENT = ".."

ESCAPE = "%"
DIGITS = 2
HEXADECIMAL = "0123456789abcdefABCDEF"
BASE = 16

AUTHORITY = "//"
DRIVE = re.compile(r"^[A-Za-z]:")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]+:")
CONTROL = re.compile(r"[\x00-\x1f\x7f]")

PATH_PART = "path segment"
FRAGMENT_PART = "fragment"


class Unresolvable(Exception):
    """A reference the sequence resolves to no document under the root.

    The message is a clause about the reference rather than a sentence
    about it, so a caller naming the reference it read states the
    refusal in one line.
    """


class Malformed(Unresolvable):
    """A reference whose form the profile's reference grammar does not admit."""


class OutsideRoot(Unresolvable):
    """A reference naming a local document the allowed source root cannot hold."""


@dataclass(frozen=True)
class Reference:
    """What one reference names, once the sequence has run over it.

    An external reference carries a scheme or an authority, names no
    local document, and holds the text it was authored as. Every other
    reference holds the root-relative path it normalized to and the
    section it names, which is absent for a whole-document reference.
    """

    original: str
    path: str
    fragment: str | None = None
    external: bool = False


@dataclass(frozen=True)
class Components:
    """One reference's parts, split in the authored text before any decoding."""

    path: str
    query: str | None
    fragment: str | None


def components(text: str) -> Components:
    """One reference split into its path, its query and its fragment.

    A delimiter is the first one written, and an escape is still an
    escape here, so an encoded number sign and an encoded question mark
    are characters of the path rather than the delimiters they spell.
    """
    head, marked, fragment = text.partition(FRAGMENT)
    path, asked, query = head.partition(QUERY)
    return Components(path, query if asked else None, fragment if marked else None)


def external(path: str) -> bool:
    """Whether a reference carries a scheme or an authority."""
    return path.startswith(AUTHORITY) or SCHEME.match(path) is not None


def decoded(text: str, part: str) -> str:
    """One reference part decoded exactly once, as UTF-8 and no further.

    Every escape is a percent and two hexadecimal digits, and the bytes
    those escapes and the literal characters make up are decoded
    together, so a multi-byte character spelled across two escapes
    arrives as the one character it is. A sequence that is not UTF-8,
    an over-long form among them, is refused rather than replaced.
    """
    written = bytearray()
    index = 0
    while index < len(text):
        character = text[index]
        if character != ESCAPE:
            written.extend(character.encode(ENCODING))
            index += 1
            continue
        escape = text[index + 1 : index + 1 + DIGITS]
        if len(escape) < DIGITS or any(digit not in HEXADECIMAL for digit in escape):
            raise Malformed(
                f"carries the escape {text[index : index + 1 + DIGITS]!r} in its "
                f"{part}, which is no percent and two hexadecimal digits"
            )
        written.append(int(escape, BASE))
        index += 1 + DIGITS
    try:
        return written.decode(ENCODING)
    except UnicodeDecodeError as undecodable:
        raise Malformed(
            f"carries an escape sequence in its {part} that is not valid "
            f"{ENCODING.upper()}: byte {undecodable.start}, {undecodable.reason}"
        ) from undecodable


def admissible(text: str, part: str) -> str:
    """One decoded part, held to the characters a local path identity carries."""
    found = CONTROL.search(text)
    if found is not None:
        raise Malformed(
            f"carries the control character {found.group()!r} in its {part}, which "
            f"no document name the bundle opens holds"
        )
    return text


def segment(written: str) -> str:
    """One authored path segment as the filename character it names.

    A separator the decoding produced is a character of a name rather
    than a separator, and no root holds a name carrying one, so the
    escape that spelled it is refused here rather than widening the
    path by one level.
    """
    decoding = admissible(decoded(written, PATH_PART), PATH_PART)
    if SEPARATOR in decoding or BACKSLASH in decoding:
        raise Malformed(
            f"carries the escape {written!r}, which decodes to a path separator "
            f"inside one segment of its path"
        )
    return decoding


def normalized(base: str, segments: Sequence[str]) -> str:
    """One reference's path, normalized against the directory it is written in.

    A `.` names the directory it sits in and a `..` names the one above,
    so the walk below holds the segments a path arrives at. An internal
    `..` the base absorbs is ordinary; one that walks above the base
    names a document outside the allowed source root.
    """
    walked = [part for part in base.split(SEPARATOR) if part]
    for part in segments:
        if part in ("", CURRENT):
            continue
        if part != PARENT:
            walked.append(part)
            continue
        if not walked:
            raise OutsideRoot(
                "normalizes above the allowed source root, which cannot contain "
                "the document it names"
            )
        walked.pop()
    return SEPARATOR.join(walked)


def resolve(text: str, base: str = "") -> Reference:
    """One reference as the document and the section it names.

    The base is the root-relative directory the reference is written
    relative to: the allowed source root itself for a command-line
    reference, and the referring document's own directory for a link
    inside a source.
    """
    written = components(text)
    if DRIVE.match(written.path) is not None:
        raise OutsideRoot(
            f"names the drive path {written.path!r}, which the allowed source "
            f"root cannot contain"
        )
    if external(written.path):
        return Reference(text, "", None, external=True)
    if written.query is not None:
        raise Malformed(
            f"carries the query {written.query!r}, which a local Markdown "
            f"document reference does not admit"
        )
    if written.path.startswith(SEPARATOR):
        raise OutsideRoot(
            f"names the root-relative path {written.path!r}, which the allowed "
            f"source root cannot contain"
        )
    if BACKSLASH in written.path:
        raise Malformed(
            f"spells {written.path!r} with a backslash, which separates no local "
            f"path the profile reads"
        )
    path = normalized(base, [segment(part) for part in written.path.split(SEPARATOR)])
    if written.fragment is None or not written.fragment:
        return Reference(text, path)
    return Reference(
        text,
        path,
        admissible(decoded(written.fragment, FRAGMENT_PART), FRAGMENT_PART),
    )
