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

A reference is a dependency when it resolves to a Markdown file under
the allowed source root, and text the bundle carries unchanged when it
resolves outside it. Where the target sits is what decides, and the root
is the lever the author holds: material a document must carry sits under
it, material it only names sits outside. One mark overrides that in a
single direction: a link whose text opens with it is deferred, so this
run does not compile what position would have carried, and the bundle
holds the link for a run that will. The run stays responsible for a
reference under the root either way: a deferred one names a target that
must exist, and the destination the bundle publishes for it names that
target from the root, so the later run needs nothing else. The module
says what a reference names, whether the bundle compiles what it names
and what a deferred link is published with; it is the command that
opens a dependency and leaves a mention alone.

A link inside a source is written relative to the document carrying
it, and a fragment alone names a section of that same document. Both
bases come from the document the link was written in rather than from
the one that discovered it, so a document names the same dependency
however the run reached it.

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
from dataclasses import dataclass, replace
from urllib.parse import quote

from prosiform.profile import is_markdown
from prosiform.source import ENCODING

MARK = "¬"

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

    A reference a source carries also holds the location it is written
    at, which a diagnostic about it names, because the document that
    refuses it is not the document it was written in. A command-line
    reference is written on the command line and holds none.

    It holds the inclusion chain as well: the identities followed from
    an entry reference to this one, this one last. How a reference was
    reached is a fact about the occurrence rather than about what it
    names, which is why it sits here beside the location rather than in
    a record kept in step with the references it describes. An entry
    reference stands at the head of its own chain.
    """

    original: str
    path: str
    fragment: str | None = None
    external: bool = False
    origin: str | None = None
    chain: tuple[str, ...] = ()


def identity(reference: Reference, base: str = "") -> str:
    """One reference as the document and the section it names, in one string.

    This is the name a chain hop is written as and the name two
    spellings of one dependency share. A fragment-only reference names
    a section of the document it is written against, which the base
    supplies, so the hop names a document wherever the reference was
    written.
    """
    path = reference.path or base
    if reference.fragment is None:
        return path
    return f"{path}{FRAGMENT}{reference.fragment}"


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


def marked(opening: str) -> bool:
    """Whether a link's author deferred it, by opening its text with the mark.

    The mark opens the link text, so text the mark sits inside names a
    document the way any prose does. It is ordinary text to the
    profile, which is why it adds no construct the grammar has to
    recognize and a renderer knowing nothing of this tool shows the
    link. It is content as well as instruction: the bundle publishes it
    where the author wrote it, because an agent reading the bundle is
    what reads it next.
    """
    return opening.startswith(MARK)


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


def inside(document: str, text: str) -> Reference:
    """One reference a source carries, as the document and the section it names.

    A link is written relative to the document carrying it, so its base
    is that document's own directory and never the directory of
    whichever document discovered the link. A fragment alone names a
    section of the document it is written in, which the directory
    cannot say, so the document itself is the path such a reference
    normalizes to.
    """
    found = resolve(text, document.rpartition(SEPARATOR)[0])
    if components(text).path:
        return found
    return replace(found, path=document)


def bundled(document: str, text: str, opening: str) -> Reference | None:
    """The reference one link in a document names where the bundle compiles it.

    A dependency carries no scheme and no authority, normalizes under
    the allowed source root, names a file the profile reads as Markdown,
    and is not deferred. Everything else is text the bundle carries as
    its author wrote it: a reference leaving the root cites material
    rather than requiring it, and a reference naming no Markdown
    document names nothing the bundle can carry.

    The opening is the literal text the link's content begins with,
    which is where a deferral is written. A marked link is no
    dependency: this run does not compile it, and the bundle carries it
    for a run that will. Deferral is read from the link rather than
    from its target, so a document another source carried into the
    bundle leaves a link deferring it alone.

    Discovery, emission and candidate validation each ask this
    question, and each asks it of the document the link was written in,
    so the answer is a property of the reference rather than of the
    stage that read it. A reference whose form the grammar does not
    admit is answered here as no dependency; the command resolves such
    a reference again where it names a Markdown document, and reports
    the refusal it is.
    """
    if marked(opening):
        return None
    return resolvable(document, text)


def deferring(document: str, text: str, opening: str) -> Reference | None:
    """The target one deferred link names, where the run is responsible for it.

    A deferral withholds a compilation position would have granted, so
    what it withholds is a reference under the allowed source root
    naming a Markdown document, and that is the reference answered
    here. The run stays responsible for it: the target is required to
    exist, and the destination the bundle publishes names it from the
    root.

    A mark on anything else changes nothing that was going to happen to
    it. A reference leaving the root, one naming no Markdown document
    and one whose form the grammar does not admit are text whether
    their author marked them or not, so each is answered here as no
    deferred target.

    This and `bundled` are the two halves of one rule, read from one
    resolution: a reference under the root naming a Markdown document
    is compiled by this run or deferred to a later one, and the mark is
    the whole of the difference.
    """
    if not marked(opening):
        return None
    return resolvable(document, text)


def resolvable(document: str, text: str) -> Reference | None:
    """The target one link names, where it resolves under the root to a document.

    Such a reference carries no scheme and no authority, normalizes
    under the allowed source root, and names a file the profile reads
    as Markdown. Everything else is text the bundle carries as its
    author wrote it: a reference leaving the root cites material rather
    than requiring it, and a reference naming no Markdown document
    names nothing the bundle can carry.

    What a reference names is a property of the reference, so this
    answers that question alone and leaves which run compiles it to the
    caller reading the mark.
    """
    try:
        found = inside(document, text)
    except Unresolvable:
        return None
    if found.external or not is_markdown(found.path):
        return None
    return found


def rebased(found: Reference, text: str) -> str:
    """One deferred link's destination: its target's path from the allowed source root.

    The path is the one the reference normalized to, which is the
    spelling the bundle's file headings carry, so a run holding nothing
    but the root follows the link the bundle hands it. The authored
    spelling cannot serve: it is written relative to the source
    document carrying the link, and the bundle records no such
    directory for a reference it did not compile.

    Each segment is escaped as it is written, so a path the resolution
    sequence decodes once is the path the filesystem carries. A name
    holding a number sign reaches the later run as that name rather
    than as a document and a section of one.

    The fragment is the author's own, carried after the path as they
    spelled it, because the run that compiles the link looks it up in
    the target document's index and this run changes no lookup.
    """
    path = SEPARATOR.join(quote(part, safe="") for part in found.path.split(SEPARATOR))
    fragment = components(text).fragment
    if fragment is None:
        return path
    return f"{path}{FRAGMENT}{fragment}"
