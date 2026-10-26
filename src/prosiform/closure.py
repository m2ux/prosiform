"""Normalize each reference from the file that writes it, within a source-owned root.

URI components split before decoding. Local path segments decode once.
Authored links that escape their source root remain citations; positional
references permit parent bootstrap. Canonical source identities are relative
to the invocation working directory, independent of the discovering parent.

Two operators open a link's text, and each withholds the compilation the
other withholds: one states when the material is compiled, the other who
compiles it. Only the dispatch states what its destination does not: a
withheld link's destination is the target's path, which no compiled link
carries, so the deferral is stated there and its mark is authoring
syntax. A dispatch has no such destination to tell a reader who compiles
the material, so its mark is content and the bundle publishes it."""

import posixpath
import re
from collections.abc import Sequence
from dataclasses import dataclass, replace
from urllib.parse import quote

from prosiform.profile import is_markdown
from prosiform.source import ENCODING

DEFERRAL_MARK = "¬"
DISPATCH_MARK = "»"

BLANKS = " \t"

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

OPERATORS = (DEFERRAL_MARK, DISPATCH_MARK)


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
    reference holds the working-directory-relative path it normalized
    to and the section it names, which is absent for a whole-document
    reference.

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
    walk: str | None = None


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


def normalized(base: str, segments: Sequence[str], allow_parent: bool = False) -> str:
    """Normalize segments, permitting leading parents for positional references."""
    walked = [part for part in base.split(SEPARATOR) if part]
    for part in segments:
        if part in ("", CURRENT):
            continue
        if part != PARENT:
            walked.append(part)
            continue
        if allow_parent and (not walked or walked[-1] == PARENT):
            walked.append(PARENT)
            continue
        if not walked:
            raise OutsideRoot(
                "normalizes above the allowed source root, which cannot contain "
                "the document it names"
            )
        walked.pop()
    return SEPARATOR.join(walked)


def operators(opening: str) -> tuple[str, ...]:
    """Each operator one link's text opens with, in the order it is written.

    An operator opens the text, so text one sits inside names a document
    the way any prose does. The blanks between two operators are the
    spacing an operator is written with, so text opening with one and
    then the other carries both.
    """
    found: list[str] = []
    at = 0
    while at < len(opening):
        while at < len(opening) and opening[at] in BLANKS:
            at += 1
        if at == len(opening) or opening[at] not in OPERATORS:
            break
        found.append(opening[at])
        at += 1
    return tuple(found)


def conflicting(opening: str) -> bool:
    """Whether a link's text opens with both operators.

    One compilation cannot wait for a later run and be dispatched by this
    one, so a link stating both states two contradictory things and the
    run says so rather than choosing.
    """
    return len(set(operators(opening))) > 1


def deferred(opening: str) -> bool:
    """Whether a link states that a later run compiles its material."""
    return DEFERRAL_MARK in operators(opening)


def dispatched(opening: str) -> bool:
    """Whether a link states that a sub-agent compiles its material.

    A dispatch and a deferral withhold the same compilation and differ in
    what they say about it, so everything a deferral withholds a dispatch
    withholds and the published mark is the only thing between them.
    """
    return DISPATCH_MARK in operators(opening)


def withholding(opening: str) -> bool:
    """Whether a link withholds its compilation from this run.

    The operators open the link text, which is ordinary text to the
    profile, so marking a link adds no construct the grammar has to
    recognize and a renderer knowing nothing of this tool shows the
    link.

    Which of the two marks reaches the bundle is a separate decision for
    each, read through `operators`: a dispatch states who compiles the
    material, which only the mark can tell a reader, while a deferral
    states when, which the destination already states.
    """
    return bool(operators(opening))


def unmarked(text: str) -> str:
    """One link's text as the bundle publishes it, with a deferral mark taken off.

    A deferral states when the material is compiled, and its destination
    states that already, so the mark that states it is authoring syntax
    rather than content. The mark goes with the blanks written around
    it, which are its spacing.

    Text opening with no deferral mark is the author's prose and is
    returned as written. A dispatch's mark states who compiles the
    material, which its destination does not, so it stays.

    The caller decides whether a link's destination states a deferral:
    a reference outside the root and one naming a resource carry their
    own text, mark included, because nothing rebased them.
    """
    at = 0
    while at < len(text) and text[at] in BLANKS:
        at += 1
    if at == len(text) or text[at] != DEFERRAL_MARK:
        return text
    at += 1
    while at < len(text) and text[at] in BLANKS:
        at += 1
    return text[at:]


def resolve(text: str, base: str = "", *, allow_parent: bool = False) -> Reference:
    """Decode a reference and normalize its path, retaining the authored access walk."""
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
    parts = [segment(part) for part in written.path.split(SEPARATOR)]
    path = normalized(base, parts, allow_parent)
    walk = "/".join(parts) if written.path else None
    if written.fragment is None or not written.fragment:
        return Reference(text, path, walk=walk)
    return Reference(
        text,
        path,
        admissible(decoded(written.fragment, FRAGMENT_PART), FRAGMENT_PART),
        walk=walk,
    )


def covers(root: str, path: str) -> bool:
    """Whether one working-directory-relative path sits inside the source root."""
    anchor = "/anchor/cwd"
    held = posixpath.normpath(posixpath.join(anchor, root or CURRENT))
    named = posixpath.normpath(posixpath.join(anchor, path))
    return posixpath.commonpath((held, named)) == held


def inside(document: str, text: str, root: str = "") -> Reference:
    """Resolve a link from the file that carries it, within the source root.

    A link is the path a reader of its file follows, so it resolves from
    that file's directory. The root bounds the result: a path landing
    outside it names nothing the root can contain. A fragment with no
    path names a section of the document that carries it.
    """
    base = posixpath.dirname(document)
    found = resolve(text, base, allow_parent=True)
    if found.external:
        return found
    if not components(text).path:
        return replace(found, path=document, walk=document)
    if not covers(root, found.path):
        raise OutsideRoot(
            "normalizes above the allowed source root, which cannot contain "
            "the document it names"
        )
    return replace(found, walk=posixpath.join(base, found.walk or found.path))


def bundled(document: str, text: str, opening: str, root: str = "") -> Reference | None:
    """The reference one link in a document names where the bundle compiles it.

    A dependency carries no scheme and no authority, normalizes under
    the allowed source root, names a file the profile reads as Markdown,
    and is not withheld. Everything else is text the bundle carries as
    its author wrote it: a reference leaving the root cites material
    rather than requiring it, and a reference naming no Markdown
    document names nothing the bundle can carry.

    The opening is the literal text the link's content begins with,
    which is where an operator is written. A withheld link is no
    dependency: this run does not compile it, and the bundle carries it
    for a run that will. Withholding is read from the link rather than
    from its target, so a document another source carried into the
    bundle leaves a link withholding it alone.

    Discovery, emission and candidate validation each ask this
    question, and each asks it of the document the link was written in,
    so the answer is a property of the reference rather than of the
    stage that read it. A reference whose form the grammar does not
    admit is answered here as no dependency; the command resolves such
    a reference again where it names a Markdown document, and reports
    the refusal it is.
    """
    if withholding(opening):
        return None
    return resolvable(document, text, root)


def withholding_target(
    document: str, text: str, opening: str, root: str = ""
) -> Reference | None:
    """The target one withheld link names, where the run is responsible for it.

    Withholding withholds a compilation position would have granted, so
    what it withholds is a reference under the allowed source root
    naming a Markdown document, and that is the reference answered
    here. The run stays responsible for it: the target is required to
    exist, and the destination the bundle publishes names it from the
    root.

    An operator on anything else changes nothing that was going to
    happen to it. A reference leaving the root, one naming no Markdown
    document and one whose form the grammar does not admit are text
    whether their author marked them or not, so each is answered here
    as no withheld target.

    This and `bundled` are the two halves of one rule, read from one
    resolution: a reference under the root naming a Markdown document is
    compiled by this run or withheld from it, and the operator is the
    whole of the difference.
    """
    if not withholding(opening):
        return None
    return resolvable(document, text, root)


def resolvable(document: str, text: str, root: str = "") -> Reference | None:
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
        found = inside(document, text, root)
    except Unresolvable:
        return None
    if found.external or not is_markdown(found.path):
        return None
    return found


def rebased(found: Reference, text: str) -> str:
    """URI-escape a withheld target's canonical working-directory-relative path.

    A deferral and a dispatch publish the same destination: the path the
    run that compiles the material follows from the root the bundle
    names, with the fragment the link resolved retained.
    """
    path = SEPARATOR.join(quote(part, safe="") for part in found.path.split(SEPARATOR))
    fragment = components(text).fragment
    if fragment is None:
        return path
    return f"{path}{FRAGMENT}{fragment}"
