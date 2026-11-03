"""Normalize each reference from the file that writes it, and classify it by its target.

URI components split before decoding. Local path segments decode once.
A link naming a Markdown document is a dependency when that document
declares `prosiform`, and a citation the bundle carries as authored when
it declares nothing. Canonical source identities are relative to the
invocation working directory, independent of the discovering parent, and
one above it keeps its leading parent segments.

Four operators open a link's text, their marks written together and
followed by a space; the deferral mark combines with the composition mark
alone. Each of the deferral, dispatch and parallel dispatch marks
withholds the same compilation from the bundle carrying the link: a
deferral states when the material is compiled, a dispatch that a
sub-agent follows it, and a parallel dispatch that a sub-agent follows it
together with the section's other parallel dispatches. A deferred link's
destination is the target's path, which no compiled link carries, so the
deferral is stated there; a dispatched link points at a bundle file or an
`In parallel` sub-section naming the bundle the run compiles for its
target, which states the dispatch. The composition mark places the
target's section beneath the section writing it, so the link points at
that placement. Every mark is therefore authoring syntax, and the bundle
drops it, a dispatch pointing at a bundle file keeping its own.

A composition directive is a link whose text opens with the composition
mark `↳` and a space, alone or written after the deferral mark as `¬↳`.
The mark requests placement and nothing else, so the meaning an author
gives the material stays with the link's text.

A link labelled with one Unicode arrow, once the operator marks and
blanks before it are set aside, is refused: an assigned scalar of the
four Arrows blocks, or a scalar of the Dingbats or Miscellaneous
Symbols and Arrows block whose character name holds the word `ARROW`.
Any other single scalar — a footnote mark, a superscript, a letter —
labels an ordinary link, and so do `⇉` and `↳` alone.

Symbols are written together, and the one blank stands between the
last of them and the link's text. A blank between two symbols states
no one operation and is refused. Nothing is trimmed or normalised to
make a label qualify."""

import posixpath
import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from enum import Enum
from types import MappingProxyType
from unicodedata import category, name
from urllib.parse import quote

from markdown_it.token import Token

from prosiform.profile import is_markdown
from prosiform.source import ANCHOR, ENCODING, external, regions, uses

DEFERRAL_MARK = "¬"
DISPATCH_MARK = "⇉"
PARALLEL_MARK = "⫽"
INLINE_MARK = "↳"

# The arrows that open an operator, which no arrow refusal reaches.
MARKS = (DISPATCH_MARK, INLINE_MARK)

# The blocks every assigned scalar of which is an arrow: Arrows and
# Supplemental Arrows-A, -B and -C.
ARROW_BLOCKS = (
    (0x2190, 0x21FF),
    (0x27F0, 0x27FF),
    (0x2900, 0x297F),
    (0x1F800, 0x1F8FF),
)

# The blocks holding arrows among other symbols, Dingbats and
# Miscellaneous Symbols and Arrows, where a scalar's name tells an arrow.
NAMED_ARROW_BLOCKS = ((0x2700, 0x27BF), (0x2B00, 0x2BFF))
ARROW_WORD = re.compile(r"\bARROWS?\b")
UNASSIGNED = "Cn"

SPACE = " "
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

DRIVE = re.compile(r"^[A-Za-z]:")
CONTROL = re.compile(r"[\x00-\x1f\x7f]")

PATH_PART = "path segment"
FRAGMENT_PART = "fragment"

OPERATORS = (DEFERRAL_MARK, DISPATCH_MARK, PARALLEL_MARK, INLINE_MARK)

# The operator groups one link may state, their marks written together.
# Only a composition can be deferred.
ADMITTED = (
    (DEFERRAL_MARK,),
    (DISPATCH_MARK,),
    (PARALLEL_MARK,),
    (INLINE_MARK,),
    (DEFERRAL_MARK, INLINE_MARK),
)


class Unresolvable(Exception):
    """A reference the sequence resolves to no document the run can open.

    The message is a clause about the reference rather than a sentence
    about it, so a caller naming the reference it read states the
    refusal in one line.
    """


class Malformed(Unresolvable):
    """A reference whose form the profile's reference grammar does not admit."""


class OutsideRoot(Unresolvable):
    """A reference whose path names a place above or outside the working directory."""


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

    A reference the substitution mapping redirected states that it is
    one: its pair named the substitute, so a substitute naming no
    document is refused rather than read as a link to nothing.

    A reference a source carries holds the title of the section it is
    written in, which selects the presets of the document it reaches.
    One in a preamble, and one written on the command line, holds none.

    A reference a composition directive writes, naming a section, states
    that it composes: it places that section beneath the directive's
    scope, and is no inclusion of the document it names.
    """

    original: str
    path: str
    fragment: str | None = None
    external: bool = False
    origin: str | None = None
    chain: tuple[str, ...] = ()
    walk: str | None = None
    redirected: bool = False
    title: str | None = None
    composes: bool = False


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
class Redirect:
    """One substitution a run performed, as the warning stating it reports.

    `resolved` is the substitute the served key names, which is the target
    one record serves however many references that key served. `would` is
    the identity the first reference to reach it was written to name,
    `source` the destination that reference was written as, and `origin`
    the source position it stands at, absent where no caller that reached
    it knew one.
    """

    resolved: str
    would: str
    source: str
    origin: str | None


Served = tuple[str, tuple[str, str | None]]
"""A pair as the run's record names it: its declaring document and its key."""


class Redirects:
    """Every substitution one run performed, and every pair a reference named.

    A mapping is a value the run cannot rewrite, and the record of what a
    run did with it belongs to the run: each stage that resolves a
    reference again writes the same record, so the mapping holds one and
    the run reads it after traversal rather than inferring it from the
    bundle.

    A record is kept under the pair that served the reference and the
    document it substituted, so a pair naming one target states one
    substitution however many references named it — a document key
    serving the document and one of its sections included. A pair is its
    declaring document and its key, so two documents declaring one key
    state two pairs, each recorded and served by the links its own
    document writes. The first reference to reach one keeps the position
    and destination the record carries. A pair is marked served by any
    reference that named it, whether or not the record it wrote was the
    first. The position is the caller's to supply, because the lookup
    knows a reference was redirected and only the traversal knows where
    the link that wrote it stands; a record re-reached by a caller that
    knows no position keeps the one already recorded.
    """

    def __init__(self) -> None:
        self._records: dict[tuple[Served, str], Redirect] = {}
        self._served: set[Served] = set()

    def record(
        self,
        pair: Served,
        substitute: Reference,
        found: Reference,
        origin: str | None = None,
    ) -> None:
        """Note one redirect: its pair, target and the position it was written at."""
        self._served.add(pair)
        named = (pair, substitute.path)
        earlier = self._records.get(named)
        if earlier is None:
            self._records[named] = Redirect(
                identity(substitute), identity(found), found.original, origin
            )
        elif earlier.origin is None and origin is not None:
            self._records[named] = replace(earlier, origin=origin)

    def served(self, pair: Served) -> bool:
        """Whether any reference of the run named this pair."""
        return pair in self._served

    def targets(self) -> tuple[Redirect, ...]:
        """Each substitution the run performed, in the order it first reached one."""
        return tuple(self._records.values())


@dataclass(frozen=True)
class Substitution:
    """The `subst` pairs each document's presets put in force for its own links.

    `documents` holds the pairs each document's governing presets state,
    by the path of the document that writes the links they redirect. A
    key is the identity a reference normalized to, so two spellings of
    one path name one key. One lookup answers: the exact document and
    section first, then the document alone, so a key carrying a fragment
    redirects that section and a key naming the whole document covers it
    and every fragment of it.

    A link is resolved through the mapping in force for the document that
    wrote it, which `writing` reads, so a pair reaches the links its
    declaring document writes and no other document's. A mapping naming
    no `writer` redirects nothing.

    A lookup returns the substitute's reference whole — its path, its
    section and its authored access walk — while the text the reference
    was written as stays the author's, because that is what a diagnostic
    about the link names.

    The pairs are held behind a read-only view, so a mapping is a value:
    the same pairs name the same substitution however many stages read
    it. What a run did with it is kept beside it, in `redirects`, because
    that is where a reference is known to have been redirected and which
    pair served it. Every mapping read from one run shares that run's
    record.
    """

    documents: Mapping[str, Mapping[tuple[str, str | None], Reference]] = (
        MappingProxyType({})
    )
    redirects: Redirects = field(default_factory=Redirects, compare=False, repr=False)
    writer: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "documents",
            MappingProxyType(
                {
                    path: MappingProxyType(dict(pairs))
                    for path, pairs in self.documents.items()
                }
            ),
        )

    def governed(
        self, documents: Mapping[str, Mapping[tuple[str, str | None], Reference]]
    ) -> "Substitution":
        """This mapping with each document's governing pairs, sharing its record."""
        return replace(self, documents=documents)

    def unrecorded(self) -> "Substitution":
        """This mapping, recording what it serves apart from the run's record.

        A caller reading what a link shows rather than compiling it asks
        through this, so what it resolves serves no key and states no
        substitution the run performed.
        """
        return replace(self, redirects=Redirects())

    def writing(self, document: str) -> "Substitution":
        """The mapping in force for the links one document writes."""
        return replace(self, writer=document)

    def redirect(self, found: Reference, origin: str | None = None) -> Reference:
        """One resolved reference as the reference the writer's pairs name, recorded.

        A reference no pair names, and one naming something other than a
        local document, is returned as it resolved.

        The lookup answers the exact document and section first, then
        the document alone. A key the second lookup finds names a
        document rather than a section, so it covers every fragment of
        that document: the substitute's path is taken and the section
        stays the one the reference named. A key the first lookup finds
        states the section the run reads instead, so its section is the
        substitute's whole.

        The record is the run's and not the mapping's, kept under the
        writer and the key that served the reference: every stage that
        resolves the same link again records the same substitution, and
        the first reference to reach one keeps the record, so a warning
        naming a substitution names where the run first met it. The
        origin is the position the caller read the link at; a stage that
        resolves the same link again adds no position of its own, so
        which caller answers does not change what the record states.
        """
        pairs = self.documents.get(self.writer or "", {})
        if found.external or not pairs:
            return found
        key: tuple[str, str | None] = (found.path, found.fragment)
        named = pairs.get(key)
        if named is None:
            key = (found.path, None)
            named = pairs.get(key)
        if named is None or self.writer is None:
            return found
        substituted = Reference(
            found.original,
            named.path,
            found.fragment if named.fragment is None else named.fragment,
            walk=named.walk,
            redirected=True,
        )
        self.redirects.record((self.writer, key), substituted, found, origin)
        return substituted


UNSUBSTITUTED = Substitution()
"""The mapping that redirects nothing: no document states a pair."""


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
    """Normalize segments, keeping the leading parents of a path above the root."""
    walked = [part for part in base.split(SEPARATOR) if part]
    for part in segments:
        if part in ("", CURRENT):
            continue
        if part != PARENT:
            walked.append(part)
        elif not walked or walked[-1] == PARENT:
            walked.append(PARENT)
        else:
            walked.pop()
    return SEPARATOR.join(walked)


@dataclass(frozen=True)
class Opened:
    """The operator marks one link's text opens with, and where its text begins.

    The marks are followed by a blank, and the text after the blanks
    begins at `after`.
    """

    marks: str
    after: int


def arrow(scalar: str) -> bool:
    """Whether one scalar is a Unicode arrow.

    Every assigned scalar of an Arrows block is one, and a scalar of a
    block mixing arrows with other symbols is one where its character
    name says so.
    """
    at = ord(scalar)
    if any(low <= at <= high for low, high in ARROW_BLOCKS):
        return category(scalar) != UNASSIGNED
    return (
        any(low <= at <= high for low, high in NAMED_ARROW_BLOCKS)
        and ARROW_WORD.search(name(scalar, "")) is not None
    )


def opened(text: str) -> Opened | None:
    """The operator marks one link's text opens with, where it states any.

    Symbols are written together and one blank separates the last of
    them from the link's text, so an operator is a run of marks followed
    by a blank, the blanks before the run being its spacing. A mark
    followed directly by text is the author's text, and opens nothing.
    """
    at = 0
    while at < len(text) and text[at] in BLANKS:
        at += 1
    end = at
    while end < len(text) and text[end] in OPERATORS:
        end += 1
    if end == at or text[end : end + 1] != SPACE:
        return None
    after = end
    while after < len(text) and text[after] in BLANKS:
        after += 1
    return Opened(text[at:end], after)


def operators(opening: str) -> tuple[str, ...]:
    """Each operator one link's text opens with, in the order it is written.

    One link states a deferred composition by writing the two marks
    together, as `¬↳ target`.
    """
    found = opened(opening)
    return () if found is None else tuple(found.marks)


def gapped(opening: str) -> bool:
    """Whether a link's text writes a blank between two of its operator marks.

    The marks of a compound operator are written together, so a blank
    between two symbols states no one operation: `¬ ⇉ target` and
    `¬ ↳ target` are each refused.
    """
    found = opened(opening)
    return found is not None and opening[found.after : found.after + 1] in OPERATORS


def arrowed(label: str) -> bool:
    """Whether a link's plain-text label is one Unicode arrow beside its operator marks.

    The marks, and the blanks after them, written before the arrow are set
    aside, and the operator marks `⇉` and `↳` are no arrow. Composition has one mark, so
    a link labelled with any other arrow is refused. The label is the
    link's whole plain text, with its entities decoded.
    """
    rest = (
        label.lstrip(BLANKS + "".join(OPERATORS))
        if label.startswith(OPERATORS)
        else label
    )
    return len(rest) == 1 and rest not in MARKS and arrow(rest)


def deferring_dispatch(opening: str) -> bool:
    """Whether a link's text writes the deferral mark against a dispatch mark.

    A dispatch is compiled up front into a bundle of its own, so a
    deferred dispatch states a dispatch no bundle publishes.
    """
    found = operators(opening)
    return DEFERRAL_MARK in found and (DISPATCH_MARK in found or PARALLEL_MARK in found)


def contradicting(opening: str) -> bool:
    """Whether a link's text writes a dispatch mark against the composition mark.

    A dispatch sends its material to a sub-agent and a composition
    places it inline beneath the section writing it, so the two marks
    state contradicting operations, as `⇉↳` and `⫽↳` do.
    """
    found = operators(opening)
    return INLINE_MARK in found and (DISPATCH_MARK in found or PARALLEL_MARK in found)


def conflicting(opening: str) -> bool:
    """Whether a link's text states operators the run cannot carry out together.

    Two dispatch marks state two ways for one sub-agent to run, which is
    why the run refuses the link rather than choosing.
    """
    found = operators(opening)
    if not found:
        return False
    return found not in ADMITTED


def deferred(opening: str) -> bool:
    """Whether a link states that a later run compiles its material."""
    return DEFERRAL_MARK in operators(opening)


def dispatched(opening: str) -> bool:
    """Whether a link states that a sub-agent follows its material.

    A dispatch and a deferral withhold the same compilation from the
    bundle carrying the link: a deferral leaves it to a later run, and a
    dispatch has the run compile it as a bundle of its own. A parallel
    dispatch is a dispatch, whose sub-agent runs beside the others its
    section names.
    """
    found = operators(opening)
    return DISPATCH_MARK in found or PARALLEL_MARK in found


def parallel(opening: str) -> bool:
    """Whether a link states that its dispatch runs beside its section's others."""
    return PARALLEL_MARK in operators(opening)


def withholding(opening: str) -> bool:
    """Whether a link withholds its compilation from this run.

    The operators open the link text, which is ordinary text to the
    profile, so marking a link adds no construct the grammar has to
    recognize and a renderer knowing nothing of this tool shows the
    link.

    A deferral's destination states when the material is compiled, and
    a dispatch's file or `In parallel` sub-section states who compiles
    it.
    """
    return deferred(opening) or dispatched(opening)


def unmarked(text: str) -> str:
    """One link's text as the bundle publishes it, with its operator's marks taken off.

    Every mark is authoring syntax rather than content, so they go with
    the blanks that are their spacing.

    Text opening with no operator is the author's prose and is returned
    as written.

    The caller applies it where the bundle gave the link a destination
    of its own, which is where that destination states the withholding;
    `published_text` decides the dispatches that keep their mark.
    """
    found = opened(text)
    return text if found is None else text[found.after :]


def filed(destination: str) -> bool:
    """Whether a destination the bundle gave a dispatch names a file beside it."""
    return not destination.startswith(ANCHOR)


def published_text(text: str, file: bool) -> str:
    """One link's text as the bundle publishes it, given whether it points at a file.

    A dispatch pointing at a bundle file keeps its mark, written as the
    dispatch mark and the one blank after it: that mark is what tells an
    agent the file is handed to a sub-agent. A `⫽` link whose set holds
    one target points at the file too, so it publishes as that dispatch.
    Every other operator's marks go, with the blanks that are their
    spacing, because the destination states what they stated: a path for
    a deferral, the contribution heading for a composition and the
    `In parallel` sub-section for a set.
    """
    found = opened(text)
    if found is None:
        return text
    rest = text[found.after :]
    if file and found.marks in (DISPATCH_MARK, PARALLEL_MARK):
        return f"{DISPATCH_MARK}{SPACE}{rest}"
    return rest


def directive(opening: str) -> bool:
    """Whether a link opening with this text is a composition directive.

    The composition mark requests placement and nothing else; every
    other operator states how its material is compiled.
    """
    return INLINE_MARK in operators(opening)


def resolve(text: str, base: str = "") -> Reference:
    """Decode a reference and normalize its path, retaining the authored access walk."""
    written = components(text)
    if DRIVE.match(written.path) is not None:
        raise OutsideRoot(
            f"names the drive path {written.path!r}, which no path under the "
            f"invocation working directory spells"
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
            f"names the root-relative path {written.path!r}, which no path under "
            f"the invocation working directory spells"
        )
    if BACKSLASH in written.path:
        raise Malformed(
            f"spells {written.path!r} with a backslash, which separates no local "
            f"path the profile reads"
        )
    parts = [segment(part) for part in written.path.split(SEPARATOR)]
    path = normalized(base, parts)
    walk = "/".join(parts) if written.path else None
    if written.fragment is None or not written.fragment:
        return Reference(text, path, walk=walk)
    return Reference(
        text,
        path,
        admissible(decoded(written.fragment, FRAGMENT_PART), FRAGMENT_PART),
        walk=walk,
    )


class Probed(Enum):
    """What a probe found at the path one reference names.

    A document that declares and one that declares nothing both exist;
    a path naming no document is a third answer, because a link to
    nothing and a link to a silent document are text for one reason and
    refused for different ones.
    """

    DECLARING = "declaring"
    SILENT = "silent"
    ABSENT = "absent"


class Declarations:
    """Whether each document a link names declares `prosiform`, asked once per path.

    A declaration lives in the target, so the answer comes from a read
    this module cannot make: the caller supplies the probe that makes
    it. The record keeps each answer under the path it was asked of, so
    a second link to one target costs no read, and every stage that
    classifies a link reads the answer discovery read.

    The probe is handed the occurrence that first asked — the reference
    with the position it is written at and the chain that reached it —
    so a refusal the read meets names the link that asked for it.
    """

    def __init__(self, probe: Callable[[Reference], Probed]) -> None:
        self._probe = probe
        self._answers: dict[str, Probed] = {}

    def answer(self, found: Reference) -> Probed:
        """What the path one reference names holds, probed the first time."""
        answer = self._answers.get(found.path)
        if answer is None:
            answer = self._answers[found.path] = self._probe(found)
        return answer

    def declares(self, found: Reference) -> bool:
        """Whether the document one reference names exists and declares."""
        return self.answer(found) is Probed.DECLARING


DECLARING = Declarations(lambda _found: Probed.DECLARING)
"""The record a caller holding no probe reads, answering every target as declaring."""


def inside(
    document: str,
    text: str,
    substitution: Substitution = UNSUBSTITUTED,
    origin: str | None = None,
) -> Reference:
    """Resolve a link from the file that carries it, held to the path grammar.

    A link is the path a reader of its file follows, so it resolves from
    that file's directory. A fragment with no path names a section of
    the document that carries it. Where the result sits decides nothing
    about whether the run compiles it; the target's declaration does,
    and `resolvable` asks it. A path normalizing above the invocation
    working directory keeps its leading parent segments, so its target
    is asked like any other and opened through the bounded no-follow
    walk from the working directory, the access a positional entry
    takes.

    The grammar still bounds the path: a drive path and a root-relative
    path name nothing the run can open, so each is refused as
    `OutsideRoot`.

    The mapping is consulted on the identity the reference normalized
    to, which is the authored identity and never the substitute's, so
    a substitute is returned wherever it sits and opened through that
    same walk. The mapping read is the one in force for `document`, the
    file that wrote the link.

    A remote reference is returned before the mapping is consulted: a
    key is the identity a reference normalized to, and a reference
    carrying a scheme or an authority names no local path identity for
    one to match.

    The origin is where the link that wrote this reference stands, which
    the caller that read it supplies so the substitution can be reported
    at the first link that redirected it. Every stage that resolves the
    same link again passes nothing and records nothing new.
    """
    base = posixpath.dirname(document)
    found = resolve(text, base)
    if found.external:
        return found
    substitution = substitution.writing(document)
    if not components(text).path:
        return substitution.redirect(
            replace(found, path=document, walk=document), origin
        )
    return substitution.redirect(
        replace(found, walk=posixpath.join(base, found.walk or found.path)), origin
    )


def bundled(
    document: str,
    text: str,
    opening: str,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    origin: str | None = None,
    reached: Sequence[str] = (),
) -> Reference | None:
    """The reference one link in a document names where the bundle compiles it.

    A dependency is a reference `resolvable` answers that is not
    withheld. Everything else is text the bundle carries as its author
    wrote it.

    The opening is the literal text the link's content begins with,
    which is where an operator is written. A withheld link is no
    dependency: this run does not compile it, and the bundle carries it
    for a run that will. Withholding is read from the link rather than
    from its target, so a document another source carried into the
    bundle leaves a link withholding it alone.

    Discovery, emission and candidate validation each ask this
    question, of the document the link was written in and of the one
    record of declarations, so the answer is a property of the reference
    rather than of the stage that read it. A reference whose form the
    grammar does not admit is answered here as no dependency; the
    command resolves such a reference again where it names a Markdown
    document, and reports the refusal it is.
    """
    if withholding(opening):
        return None
    return resolvable(document, text, declarations, substitution, origin, reached)


def withholding_target(
    document: str,
    text: str,
    opening: str,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    origin: str | None = None,
    reached: Sequence[str] = (),
) -> Reference | None:
    """The target one withheld link names, where the run is responsible for it.

    Withholding withholds a compilation the declaration would have
    granted, so what it withholds is a reference `resolvable` answers,
    and that is the reference answered here. The run stays responsible
    for it: the target is required to exist, and the destination the
    bundle publishes names it from the working directory.

    An operator on anything else states a compilation no run performs:
    a reference naming no Markdown document, one whose target declares
    nothing and one whose form the grammar does not admit withhold
    nothing, so each is answered here as no withheld target and the run
    refuses the link that carries it.

    This and `bundled` are the two halves of one rule, read from one
    resolution: a reference naming a declaring Markdown document is
    compiled by this run or withheld from it, and the operator is the
    whole of the difference.
    """
    if not withholding(opening):
        return None
    return resolvable(document, text, declarations, substitution, origin, reached)


def resolvable(
    document: str,
    text: str,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    origin: str | None = None,
    reached: Sequence[str] = (),
) -> Reference | None:
    """The target one link names, where it is a document that declares `prosiform`.

    Such a reference carries no scheme and no authority, resolves to a
    file the profile reads as Markdown, and names a document whose
    frontmatter declares. Everything else is text the bundle carries as
    its author wrote it: a reference naming no Markdown document names
    nothing the bundle can carry, and one whose target declares nothing
    cites material rather than requiring it.

    The declaration is asked of the record after every other test, so a
    citation that is no Markdown document is never opened. The record is
    handed the occurrence — the origin and the chain `reached` extended
    by this reference — so a refusal its probe meets names the link.

    What a reference names is a property of the reference, so this
    answers that question alone and leaves which run compiles it to the
    caller reading the mark.
    """
    found = named(document, text, substitution, origin, reached)
    if found is None or not declarations.declares(found):
        return None
    return replace(found, origin=None, chain=())


def named(
    document: str,
    text: str,
    substitution: Substitution = UNSUBSTITUTED,
    origin: str | None = None,
    reached: Sequence[str] = (),
) -> Reference | None:
    """The local Markdown path one link names, as the occurrence written there.

    A reference carrying a scheme or an authority, one naming no
    Markdown document and one whose form the grammar does not admit
    name no path a probe can ask, and each is answered as none. What
    is returned carries the origin and the chain `reached` extended by
    this reference, which is what a probe or a refusal names.
    """
    try:
        found = inside(document, text, substitution, origin)
    except Unresolvable:
        return None
    if found.external or not is_markdown(found.path):
        return None
    return replace(found, origin=origin, chain=(*reached, identity(found)))


def boundary(document: str, tokens: Sequence[Token]) -> str:
    """The deepest directory holding every local Markdown path a document's links name.

    Each link resolves from the document's directory, as a reader of the
    file follows it, and a fragment-only link names the document itself.
    The boundary is read from every link the document writes rather than
    from a selected region, because the links are a property of the
    document and one file has one boundary. It is derived from the links,
    so it holds every one of them and refuses none. A document naming no
    local Markdown path has its own directory.

    The working-directory-relative directory is returned, empty for the
    working directory itself, and one above it is spelled with leading
    parent segments. A link the path grammar refuses, one naming no
    Markdown document and an image name no path and contribute nothing.

    A directory reached by climbing further than another holds it, so
    where the paths climb different distances the boundary is the
    directory the furthest climb reaches.
    """
    directories = [
        posixpath.dirname(found.path)
        for use in uses(tokens, tuple(regions(tokens)))
        if not use.resource and (found := named(document, use.destination)) is not None
    ]
    if not directories:
        return posixpath.dirname(document)
    climbs = {climb(directory) for directory in directories}
    if len(climbs) > 1:
        return SEPARATOR.join([PARENT] * max(climbs))
    return posixpath.commonpath(directories)


def climb(path: str) -> int:
    """How many leading parent segments a normalized path opens with."""
    parts = path.split(SEPARATOR)
    count = 0
    while count < len(parts) and parts[count] == PARENT:
        count += 1
    return count


def rebased(found: Reference, text: str) -> str:
    """URI-escape a deferred target's canonical working-directory-relative path.

    A deferral publishes the path the run that compiles the material
    follows from the working directory the bundle was compiled in, with
    the fragment the link resolved to retained. The path is the
    target's, so a target the substitution mapping redirected publishes
    the substitute's path, and so is the fragment: a section key
    redirects the section together with the document, while a document
    key keeps the section the reference named. A target resolving to no
    section publishes the fragment its author wrote, which an empty one
    spells as the bare delimiter.
    """
    path = SEPARATOR.join(quote(part, safe="") for part in found.path.split(SEPARATOR))
    if found.fragment is not None:
        return f"{path}{FRAGMENT}{found.fragment}"
    fragment = components(text).fragment
    if fragment is None:
        return path
    return f"{path}{FRAGMENT}{fragment}"
