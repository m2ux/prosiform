"""Normalize each reference from the file that writes it, within a source-owned root.

URI components split before decoding. Local path segments decode once.
Authored links that escape their source root remain citations; positional
references permit parent bootstrap. Canonical source identities are relative
to the invocation working directory, independent of the discovering parent.

Three operators open a link's text, each a mark followed by a space, and
one link states one of them. Each withholds the same compilation from the
bundle carrying the link: a deferral states when the material is
compiled, a dispatch that a sub-agent follows it, and a parallel dispatch
that a sub-agent follows it together with the section's other parallel
dispatches. A deferred link's destination is the target's path, which no
compiled link carries, so the deferral is stated there; a dispatched link
points at a sub-section naming the bundle the run compiles for its
target, which states the dispatch. Every mark is therefore authoring
syntax, and the bundle drops it."""

import posixpath
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from urllib.parse import quote

from prosiform.profile import is_markdown
from prosiform.source import ENCODING, external

DEFERRAL_MARK = "¬"
DISPATCH_MARK = "⇉"
PARALLEL_MARK = "⫽"

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

OPERATORS = (DEFERRAL_MARK, DISPATCH_MARK, PARALLEL_MARK)

# The operator groups one link may state. A deferral carries the dispatch
# that the run compiling the material later finds, and the marks of one
# group are written together.
ADMITTED = (
    (DEFERRAL_MARK,),
    (DISPATCH_MARK,),
    (PARALLEL_MARK,),
    (DEFERRAL_MARK, DISPATCH_MARK),
    (DEFERRAL_MARK, PARALLEL_MARK),
)


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


@dataclass(frozen=True)
class Pairing:
    """One mapping entry as its caller read it, and which kind of entry it states.

    A folder pairing names a folder on both sides, so its key is a path
    and its substitute is a folder; a document pairing names a reference
    on each side. Each reference carries the spelling its caller wrote,
    separator included, because that is what a diagnostic about the entry
    names.
    """

    original: Reference
    alternative: Reference
    folder: bool


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
    the source position it stands at, absent where the reference is a
    command-line entry and stands in no source.
    """

    resolved: str
    would: str
    source: str
    origin: str | None


class Redirects:
    """Every substitution one run performed, and every key a reference named.

    A mapping is a value the run cannot rewrite, and the record of what a
    run did with it belongs to the run: each stage that resolves a
    reference again writes the same record, so the mapping holds one and
    the run reads it after traversal rather than inferring it from the
    bundle.

    A record is kept under the key that served the reference and the
    document it substituted, so a key naming one target states one
    substitution however many references named it — a document key
    serving the document and one of its sections included — and a folder
    key states one per document it answered, because each remainder is a
    target of its own. The first reference to reach one keeps the
    position and destination the record carries. A key is marked served
    by any reference that named it, whether or not the record it wrote
    was the first. The position is the caller's to supply, because the
    lookup knows a reference was redirected and only the traversal knows
    where the link that wrote it stands; a record re-reached by a caller
    that knows no position keeps the one already recorded.
    """

    def __init__(self) -> None:
        self._records: dict[tuple[tuple[str, str | None], str], Redirect] = {}
        self._served: set[tuple[str, str | None]] = set()

    def record(
        self,
        key: tuple[str, str | None],
        substitute: Reference,
        found: Reference,
        origin: str | None = None,
    ) -> None:
        """Note one redirect: its key, target and the position it was written at."""
        self._served.add(key)
        named = (key, substitute.path)
        earlier = self._records.get(named)
        if earlier is None:
            self._records[named] = Redirect(
                identity(substitute), identity(found), found.original, origin
            )
        elif earlier.origin is None and origin is not None:
            self._records[named] = replace(earlier, origin=origin)

    def served(self, key: tuple[str, str | None]) -> bool:
        """Whether any reference of the run named this key."""
        return key in self._served

    def targets(self) -> tuple[Redirect, ...]:
        """Each substitution the run performed, in the order it first reached one."""
        return tuple(self._records.values())


@dataclass(frozen=True)
class Substitution:
    """The mapping from an authored identity to the reference the run reads instead.

    A key is the identity a reference normalized to, so two spellings of
    one path name one key. One lookup answers: the exact document and
    section first, then the document alone, then the longest folder key
    holding the path, so a key carrying a fragment redirects that section,
    a key naming the whole document covers it and every fragment of it,
    and a key naming a folder redirects every document under that folder.

    A folder key is a path rather than an identity, because it answers for
    a path and not for one document: its substitute is a folder, and the
    remainder a reference carries past the key is what the substitute
    folder takes. A document key answers before any folder key, and of two
    folder keys holding one path the longer answers, so the narrowest
    statement a caller wrote is the one that holds.

    A lookup returns the substitute's reference whole — its path, its
    section and its authored access walk — while the text the reference
    was written as stays the author's, because that is what a diagnostic
    about the link names.

    The keys are held behind a read-only view, so a mapping is a value:
    the same pairs name the same substitution however many stages read
    it. What a run did with it is kept beside it, in `redirects`, because
    that is where a reference is known to have been redirected and which
    key served it. A key's authored spelling is kept for the warning that
    states a key no reference named, and a mapping given none writes the
    key's identity back, which is the spelling the caller wrote.
    """

    keys: Mapping[tuple[str, str | None], Reference]
    spellings: Mapping[tuple[str, str | None], str] = MappingProxyType({})
    folders: Mapping[str, Reference] = MappingProxyType({})
    redirects: Redirects = field(default_factory=Redirects, compare=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "keys", MappingProxyType(dict(self.keys)))
        object.__setattr__(self, "spellings", MappingProxyType(dict(self.spellings)))
        object.__setattr__(self, "folders", MappingProxyType(dict(self.folders)))

    def __len__(self) -> int:
        """How many keys the mapping holds, of either kind."""
        return len(self.keys) + len(self.folders)

    def __bool__(self) -> bool:
        """Whether the mapping redirects anything at all."""
        return bool(self.keys) or bool(self.folders)

    def unserved(self) -> tuple[str, ...]:
        """Every key no reference named, as its caller wrote it, in the order given."""
        keys: tuple[tuple[str, str | None], ...] = (
            *self.keys,
            *((folder, None) for folder in self.folders),
        )
        return tuple(
            self.spelling(key) for key in keys if not self.redirects.served(key)
        )

    def spelling(self, key: tuple[str, str | None]) -> str:
        """One key as the caller wrote it, where the mapping was given its spelling."""
        written = self.spellings.get(key)
        if written is not None:
            return written
        path, fragment = key
        return path if fragment is None else f"{path}{FRAGMENT}{fragment}"

    def substitute(self, found: Reference) -> Reference:
        """One resolved reference as the reference the mapping names instead.

        A reference the mapping does not name, and one naming something
        other than a local document, is returned as it resolved.

        The lookup answers the exact document and section first, then
        the document alone, then the longest folder key holding the path.
        A key the second lookup finds names a document rather than a
        section, so it covers every fragment of that document: the
        substitute's path is taken and the section stays the one the
        reference named. A key the first lookup finds states the section
        the run reads instead, so its section is the substitute's whole.
        A folder key names no section and takes none: the substitute's
        folder joined with the remainder the reference carries past the
        key is the path, and the section is the reference's.

        What is taken is the substitute's path and its authored access
        walk, and what stays is the text the reference was written as,
        because that is what a diagnostic about the link names.
        """
        named = self.key(found)
        if named is None:
            return found
        return Reference(
            found.original,
            named.path,
            found.fragment if named.fragment is None else named.fragment,
            walk=named.walk,
        )

    def redirect(self, found: Reference, origin: str | None = None) -> Reference:
        """One resolved reference as the reference the mapping names, recording it.

        The record is the run's and not the mapping's: every stage that
        resolves the same link again records the same substitution, and
        the first reference to reach one keeps the record, so a warning
        naming a substitution names where the run first met it.

        The origin is the position the caller read the link at, absent for
        a reference the command line names, which stands in no source. A
        stage that resolves the same link again records the same key and
        adds no position of its own, so which caller answers does not
        change what the record states.
        """
        named = self.substitute(found)
        if named is not found:
            self.redirects.record(self.served_key(found), named, found, origin)
        return named

    def served_key(self, found: Reference) -> tuple[str, str | None]:
        """The key one reference's identity names, which is what a record is kept under.

        The answer follows the lookup's precedence, so a key carrying a
        section is marked served by the reference that named that section
        rather than by every reference to its document, and a folder key is
        marked served by the first reference it answered.
        """
        answering = self.answering(found)
        return (found.path, None) if answering is None else answering[0]

    def answering(
        self, found: Reference
    ) -> tuple[tuple[str, str | None], Reference] | None:
        """The key that answers one reference and the substitute it names.

        One answer is what the lookup and the record both read, so a
        caller asking what a reference names and a caller asking which key
        served it cannot disagree about which of two keys holds.

        The exact document and section answers first, then the document
        alone, then the longest folder key holding the path. The exact
        answer is asked for even where the section is absent, because a key
        naming a document and a key naming that document's section are two
        keys and the section one states which.
        """
        if found.external or not (self.keys or self.folders):
            return None
        exact = self.keys.get((found.path, found.fragment))
        if exact is not None:
            return ((found.path, found.fragment), exact)
        whole = self.keys.get((found.path, None))
        if whole is not None:
            return ((found.path, None), whole)
        folder = self.folder(found.path)
        if folder is None:
            return None
        substitute = self.folders[folder]
        remainder = found.path[len(folder) :].lstrip(SEPARATOR)
        return (
            (folder, None),
            Reference(
                substitute.original,
                posixpath.join(substitute.path, remainder),
                walk=posixpath.join(substitute.walk or substitute.path, remainder),
            ),
        )

    def key(self, found: Reference) -> Reference | None:
        """The substitute one resolved reference's identity names, or nothing.

        A caller for which "the mapping named this" and "the mapping did
        not" are different outcomes asks this rather than comparing what
        `substitute` returned, so no case turns on two references being
        the same object.
        """
        answering = self.answering(found)
        return None if answering is None else answering[1]

    def folder(self, path: str) -> str | None:
        """The longest folder key one path sits under, or nothing.

        A folder key holds a path that continues it past a separator, so
        a key `rules` holds `rules/red.md` and not `ruleset.md`: the
        separator is what states that the key names a folder rather than a
        document whose name happens to be a prefix.
        """
        holding = [key for key in self.folders if path.startswith(f"{key}{SEPARATOR}")]
        if not holding:
            return None
        return max(holding, key=len)


UNSUBSTITUTED = Substitution({})
"""The mapping a run given no `-m` carries, which redirects nothing."""


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

    An operator is a run of operator marks followed by a space, and it
    opens the text, so text a mark sits inside, or opens with no space
    after it, names a document the way any prose does. One link states
    both a deferral and a dispatch by writing the two marks adjacent, as
    `¬⇉ target`, and the blanks before the run are its spacing.
    """
    at = 0
    while at < len(opening) and opening[at] in BLANKS:
        at += 1
    end = at
    while end < len(opening) and opening[end] in OPERATORS:
        end += 1
    if end == at or opening[end : end + 1] != SPACE:
        return ()
    return tuple(opening[at:end])


def spaced(opening: str) -> bool:
    """Whether a link's text states two operator groups separated by a blank.

    The marks of a compound operator are written together, so a blank
    between two of them states two operators rather than one, and the
    author who meant `¬⇉ target` wrote something else.
    """
    at = 0
    while at < len(opening) and opening[at] in BLANKS:
        at += 1
    end = at
    while end < len(opening) and opening[end] in OPERATORS:
        end += 1
    if end == at or opening[end : end + 1] != SPACE:
        return False
    after = end
    while after < len(opening) and opening[after] in BLANKS:
        after += 1
    return opening[after : after + 1] in OPERATORS


def conflicting(opening: str) -> bool:
    """Whether a link's text states operators the run cannot carry out together.

    A deferral says when the material is compiled and a dispatch says who
    compiles it, so the two are written together as `¬⇉` or `¬⫽` and
    state one compilation: the material is deferred, and the run that
    later compiles it finds a dispatch. Two dispatch marks state two ways
    for one sub-agent to run, which is why the refusal outlives the
    deferral.
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

    No mark reaches the bundle: a deferral's destination states when
    the material is compiled, and a dispatch's sub-section states who
    compiles it.
    """
    return deferred(opening) or dispatched(opening)


def unmarked(text: str) -> str:
    """One link's text as the bundle publishes it, with its operator's marks taken off.

    A deferral states when the material is compiled, and its destination
    states that already; a dispatch states who compiles it, and the
    sub-section its link points at states that. Every mark is authoring
    syntax rather than content, so they go with the blanks that are their
    spacing. The marks of a compound operator go together, because a mark
    with no space after it is the author's text and ends the run.

    Text opening with no operator is the author's prose and is returned
    as written.

    The caller applies it where the bundle gave the link a destination
    of its own, which is where that destination states the withholding.
    """
    at = 0
    while at < len(text) and text[at] in BLANKS:
        at += 1
    end = at
    while end < len(text) and text[end] in OPERATORS:
        end += 1
    if end == at or text[end : end + 1] != SPACE:
        return text
    while end < len(text) and text[end] in BLANKS:
        end += 1
    return text[end:]


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


def inside(
    document: str,
    text: str,
    root: str = "",
    substitution: Substitution = UNSUBSTITUTED,
    origin: str | None = None,
) -> Reference:
    """Resolve a link from the file that carries it, within the source root.

    A link is the path a reader of its file follows, so it resolves from
    that file's directory. The root bounds the result: a path landing
    outside it names nothing the root can contain, so it is a citation
    rather than a dependency. A fragment with no path names a section
    of the document that carries it.

    The mapping is consulted on the identity the reference normalized
    to, which is the authored identity and never the substitute's: it
    decides what an identity names, and the root decides what the run
    does with that identity. A reference the root admits is redirected
    to the substitute, and so is one the root refuses — a citation can
    name a stand-in, which is what makes a tree under test reachable
    from outside its own root. A reference no key names is returned as
    it resolved, or refused as `OutsideRoot` where the root does not
    hold it.

    The substitute is exempt from the writing source's root and is
    never held to it. It is opened through the bounded no-follow walk
    from the invocation working directory, which is the same access a
    positional entry takes, so a redirected citation is no wider a
    grant than an entry reference already is. Holding the substitute to
    the writing source's root, or reading the mapping after the check
    had refused the authored path, would refuse every substitute kept
    beside the tree under test.

    A remote reference is returned before the mapping is consulted: a
    key is the identity a reference normalized to, and a reference
    carrying a scheme or an authority names no local path identity for
    one to match. That is a decision rather than an omission, and the
    one exception the reach of the mapping has.

    The origin is where the link that wrote this reference stands, which
    the caller that read it supplies so the substitution can be reported
    at the first link that redirected it. Every stage that resolves the
    same link again passes nothing and records nothing new.
    """
    base = posixpath.dirname(document)
    found = resolve(text, base, allow_parent=True)
    if found.external:
        return found
    if not components(text).path:
        return substitution.redirect(
            replace(found, path=document, walk=document), origin
        )
    resolved = replace(found, walk=posixpath.join(base, found.walk or found.path))
    if substitution.key(resolved) is not None:
        return substitution.redirect(resolved, origin)
    if not covers(root, found.path):
        raise OutsideRoot(
            "normalizes above the allowed source root, which cannot contain "
            "the document it names"
        )
    return resolved


def bundled(
    document: str,
    text: str,
    opening: str,
    root: str = "",
    substitution: Substitution = UNSUBSTITUTED,
    origin: str | None = None,
) -> Reference | None:
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
    return resolvable(document, text, root, substitution, origin)


def withholding_target(
    document: str,
    text: str,
    opening: str,
    root: str = "",
    substitution: Substitution = UNSUBSTITUTED,
    origin: str | None = None,
) -> Reference | None:
    """The target one withheld link names, where the run is responsible for it.

    Withholding withholds a compilation position would have granted, so
    what it withholds is a reference under the allowed source root
    naming a Markdown document, and that is the reference answered
    here. The run stays responsible for it: the target is required to
    exist, and the destination the bundle publishes names it from the
    root.

    An operator on anything else states a compilation no run performs:
    a reference leaving the root, one naming no Markdown document and
    one whose form the grammar does not admit withhold nothing, so each
    is answered here as no withheld target and the run refuses the link
    that carries it.

    This and `bundled` are the two halves of one rule, read from one
    resolution: a reference under the root naming a Markdown document is
    compiled by this run or withheld from it, and the operator is the
    whole of the difference.
    """
    if not withholding(opening):
        return None
    return resolvable(document, text, root, substitution, origin)


def resolvable(
    document: str,
    text: str,
    root: str = "",
    substitution: Substitution = UNSUBSTITUTED,
    origin: str | None = None,
) -> Reference | None:
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
        found = inside(document, text, root, substitution, origin)
    except Unresolvable:
        return None
    if found.external or not is_markdown(found.path):
        return None
    return found


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
