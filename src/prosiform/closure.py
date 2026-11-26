"""Resolve references, classify their targets, and select link operations.

Operator recognition uses `marks.opened`. The module also supplies
substitution mappings and preset-selection helpers.
"""

import posixpath
import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from enum import Enum
from types import MappingProxyType
from unicodedata import category, name
from urllib.parse import quote

from prosiform.marks import (
    BLANKS,
    DEFERRAL_MARK,
    DISPATCH_MARK,
    INLINE_MARK,
    OPERATORS,
    PARALLEL_MARK,
    SPACE,
    opened,
)
from prosiform.metadata import DEFAULT, Conversion, Preset
from prosiform.profile import is_markdown
from prosiform.source import ANCHOR, ENCODING, external
from prosiform.tags import PICK, picks

MARKS = (DISPATCH_MARK, INLINE_MARK)

ARROW_BLOCKS = (
    (0x2190, 0x21FF),
    (0x27F0, 0x27FF),
    (0x2900, 0x297F),
    (0x1F800, 0x1F8FF),
)

NAMED_ARROW_BLOCKS = ((0x2700, 0x27BF), (0x2B00, 0x2BFF))
ARROW_WORD = re.compile(r"\bARROWS?\b")
UNASSIGNED = "Cn"

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

ADMITTED = (
    (DEFERRAL_MARK,),
    (DISPATCH_MARK,),
    (PARALLEL_MARK,),
    (INLINE_MARK,),
    (DEFERRAL_MARK, INLINE_MARK),
)


class Unresolvable(Exception):
    """A reference `resolve` cannot interpret as a document the run can open.

    The message is a clause about the reference rather than a sentence
    about it, so a caller naming the reference it read states the
    refusal in one line.
    """


class Malformed(Unresolvable):
    """A reference whose form the profile's reference grammar does not admit."""


class OutsideRoot(Unresolvable):
    """A drive-qualified or absolute reference path refused by `resolve`."""


@dataclass(frozen=True)
class Reference:
    """One resolved reference and its occurrence context.

    `original` holds the authored destination, `path` its canonical path,
    `fragment` its section, and `external` its external-reference flag.
    `origin` holds the source position, `chain` the inclusion chain, and
    `walk` the authored access path. `redirected` records substitution,
    `title` the containing section's title, `tags` the requested preset
    names, and `composes` and `defers` the occurrence's operation flags.
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
    tags: frozenset[str] = frozenset()
    defers: bool = False


def matching_presets(
    conversion: Conversion, tags: frozenset[str]
) -> tuple[Preset, ...]:
    """The destination's matching named presets, in declaration order.

    Tags hold normalized complete names. An unmatched name adds nothing,
    and the reserved default token supplies no named selection. A stub
    the run's own names select matches whatever the tags name, since
    the run selects its entry's stubs wherever it bundles the entry.
    """
    return tuple(
        preset
        for preset in conversion.presets
        if preset.name.casefold() != DEFAULT
        and (
            preset.name.casefold() in tags
            or (preset.stub is not None and preset.name.casefold() in conversion.run)
        )
    )


@dataclass(frozen=True)
class BundleSelection:
    """One destination's canonical path, optional fragment and selected preset names."""

    path: str
    fragment: str | None = None
    presets: frozenset[str] = frozenset()


def bundle_selection(reference: Reference, conversion: Conversion) -> BundleSelection:
    """The effective bundle identity of a resolved reference at its destination."""
    return BundleSelection(
        reference.path,
        reference.fragment or None,
        frozenset(
            preset.name for preset in matching_presets(conversion, reference.tags)
        ),
    )


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


Served = tuple[str, tuple[str, str | None]]
"""A pair as the run's record names it: its declaring document and its key."""


@dataclass(frozen=True)
class Redirect:
    """One recorded substitution and its occurrence context.

    `resolved` holds the substituted identity, `would` the input identity,
    `source` the authored destination, and `origin` its optional source
    position. `pair` identifies the serving declaration and key;
    `declared` holds that pair's substitute identity.
    """

    resolved: str
    would: str
    source: str
    origin: str | None
    pair: Served
    declared: str


class Redirects:
    """Collect a run's substitutions and served pairs through `record`."""

    def __init__(self) -> None:
        self._records: dict[tuple[Served, tuple[str, str | None]], Redirect] = {}
        self._served: set[tuple[Served, tuple[str, str | None]]] = set()

    def record(
        self,
        pair: Served,
        declared: Reference,
        substitute: Reference,
        found: Reference,
        origin: str | None = None,
    ) -> None:
        """Record a served pair and substitute, retaining the first occurrence.

        A pair and its declared target identify one record. Its first
        reference supplies the original destination and resolved substitute.
        A later occurrence may supply an origin where the first had none.
        """
        named = (pair, (declared.path, declared.fragment))
        self._served.add(named)
        earlier = self._records.get(named)
        if earlier is None:
            self._records[named] = Redirect(
                identity(substitute),
                identity(found),
                found.original,
                origin,
                pair,
                identity(declared),
            )
        elif earlier.origin is None and origin is not None:
            self._records[named] = replace(earlier, origin=origin)

    def served(self, pair: Served, declared: Reference) -> bool:
        """Whether a reference used this pair with its declared substitute."""
        return (pair, (declared.path, declared.fragment)) in self._served

    def targets(self) -> tuple[Redirect, ...]:
        """Each substitution the run performed, in the order it first reached one."""
        return tuple(self._records.values())


@dataclass(frozen=True)
class Substitution:
    """An immutable substitution mapping with a shared `Redirects` record.

    `documents` holds each document's pairs, and `contributions` each
    composed copy's pairs. `writer` names the current document and
    `selection` its optional composed-copy selection. `entry` names the
    run's entry and `stubs` its pairs. `composed` selects a copy;
    `redirect` owns lookup and occurrence preservation.
    """

    documents: Mapping[str, Mapping[tuple[str, str | None], Reference]] = (
        MappingProxyType({})
    )
    redirects: Redirects = field(default_factory=Redirects, compare=False, repr=False)
    writer: str | None = None
    contributions: Mapping[
        tuple[str, frozenset[str]], Mapping[tuple[str, str | None], Reference]
    ] = MappingProxyType({})
    selection: tuple[str, frozenset[str]] | None = None
    entry: str | None = None
    stubs: Mapping[tuple[str, str | None], Reference] = MappingProxyType({})

    def __post_init__(self) -> None:
        """Copy each pair mapping into read-only views."""
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
        object.__setattr__(
            self,
            "contributions",
            MappingProxyType(
                {
                    copy: MappingProxyType(dict(pairs))
                    for copy, pairs in self.contributions.items()
                }
            ),
        )
        object.__setattr__(self, "stubs", MappingProxyType(dict(self.stubs)))

    def stubbed(
        self, entry: str, stubs: Mapping[tuple[str, str | None], Reference]
    ) -> "Substitution":
        """This mapping with the run's entry and its stubs' pairs, one record shared."""
        return replace(self, entry=entry, stubs=stubs)

    def governed(
        self,
        documents: Mapping[str, Mapping[tuple[str, str | None], Reference]],
        contributions: Mapping[
            tuple[str, frozenset[str]], Mapping[tuple[str, str | None], Reference]
        ] = MappingProxyType({}),
    ) -> "Substitution":
        """This mapping with each group's and each copy's pairs, sharing its record."""
        return replace(self, documents=documents, contributions=contributions)

    def composed(self, document: str, tags: frozenset[str] | None) -> "Substitution":
        """The mapping in force for the links a composed copy of `document` writes.

        `tags` select the presets of the directive or dispatch placing the
        copy, and `None` names the document's own group.
        """
        return replace(self, selection=None if tags is None else (document, tags))

    def unrecorded(self) -> "Substitution":
        """This mapping, recording what it serves apart from the run's record.

        A caller reading what a link shows rather than bundling it asks
        through this, so what it resolves serves no key and states no
        substitution the run performed.
        """
        return replace(self, redirects=Redirects())

    def writing(self, document: str) -> "Substitution":
        """The mapping in force for the links one document writes."""
        return replace(self, writer=document)

    def redirect(self, found: Reference, origin: str | None = None) -> Reference:
        """Resolve a reference through the current writer's pairs and record it.

        The lookup uses the pairs selected by `composed` for this writer,
        otherwise its document pairs. External references and a mapping
        without a writer return their input. Lookup asks for the exact
        document and section before the document alone, asking the entry's
        stubs before the writer's pairs for each key. A stub naming the
        writer as a stand-in is excluded unless its key names the writer.

        The substitute supplies its path and access walk. Its fragment holds
        when present; otherwise the input fragment stays. Requested tags,
        authored destination and diagnostic context stay with the occurrence.
        `Redirects.record` owns the shared record's first-occurrence rule.
        """
        pairs = (
            self.contributions.get(self.selection, {})
            if self.selection is not None and self.selection[0] == self.writer
            else self.documents.get(self.writer or "", {})
        )
        if found.external or self.writer is None:
            return found
        stubs = {
            key: one
            for key, one in self.stubs.items()
            if one.path != self.writer or key[0] == self.writer
        }
        served = next(
            (
                (serving, key, held[key])
                for key in ((found.path, found.fragment), (found.path, None))
                for serving, held in ((self.entry, stubs), (self.writer, pairs))
                if serving is not None and key in held
            ),
            None,
        )
        if served is None:
            return found
        serving, key, named = served
        substituted = replace(
            found,
            path=named.path,
            fragment=found.fragment if named.fragment is None else named.fragment,
            walk=named.walk,
            redirected=True,
        )
        self.redirects.record((serving, key), named, substituted, found, origin)
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


def arrow(scalar: str) -> bool:
    """Whether one scalar is a Unicode arrow.

    Every assigned scalar in Arrows or Supplemental Arrows-A, -B and -C
    is an arrow. In Dingbats and Miscellaneous Symbols and Arrows, its
    Unicode name must contain the word ARROW or ARROWS.
    """
    at = ord(scalar)
    if any(low <= at <= high for low, high in ARROW_BLOCKS):
        return category(scalar) != UNASSIGNED
    return (
        any(low <= at <= high for low, high in NAMED_ARROW_BLOCKS)
        and ARROW_WORD.search(name(scalar, "")) is not None
    )


def operators(opening: str) -> tuple[str, ...]:
    """Return the marks `marks.opened` recognizes, in written order."""
    found = opened(opening)
    return () if found is None else tuple(found.marks)


def gapped(opening: str) -> bool:
    """Whether a `marks.opened` operator is followed by another mark after spacing."""
    found = opened(opening)
    return found is not None and opening[found.after : found.after + 1] in OPERATORS


def arrowed(label: str) -> bool:
    """Whether a link's plain-text label is one arrow beside its marks.

    Leading operator marks and their blanks are excluded. The dispatch
    and composition marks alone are exempt; `arrow` classifies the
    remaining scalar.
    """
    rest = (
        label.lstrip(BLANKS + "".join(OPERATORS))
        if label.startswith(OPERATORS)
        else label
    )
    return len(rest) == 1 and rest not in MARKS and arrow(rest)


def deferring_dispatch(opening: str) -> bool:
    """Whether recognized operators combine deferral with either dispatch mark."""
    found = operators(opening)
    return DEFERRAL_MARK in found and (DISPATCH_MARK in found or PARALLEL_MARK in found)


def contradicting(opening: str) -> bool:
    """Whether recognized operators combine composition with either dispatch mark."""
    found = operators(opening)
    return INLINE_MARK in found and (DISPATCH_MARK in found or PARALLEL_MARK in found)


def conflicting(opening: str) -> bool:
    """Whether the recognized marks form a combination outside `ADMITTED`."""
    found = operators(opening)
    if not found:
        return False
    return found not in ADMITTED


def deferred(opening: str) -> bool:
    """Whether a link states that a later run bundles its material."""
    return DEFERRAL_MARK in operators(opening)


def bundled_pick(opening: str, tags: frozenset[str]) -> bool:
    """Whether `tags.picks` applies outside `deferred` and `picking` links."""
    return picks(tags) and not deferred(opening) and not picking(opening, tags)


def picking(opening: str, tags: frozenset[str]) -> bool:
    """Whether a link is a `⇉` dispatch leaving its pick to the dispatching agent."""
    return picks(tags) and dispatched(opening) and not parallel(opening)


def alternatives_of(
    reference: Reference, conversion: Conversion
) -> tuple[tuple[Reference, Preset], ...]:
    """Each alternative a picking dispatch publishes a bundle for, in declaration order.

    Each is the dispatch's reference with the alternative standing in its
    tags where the pick token stands, beside the fixed tags, so each
    bundle selects that alternative and the ordinary presets the link
    names.
    """
    fixed = reference.tags - {PICK}
    return tuple(
        (replace(reference, tags=fixed | {one.name.casefold()}), one)
        for one in conversion.alternatives
    )


class Briefs(Exception):
    """Two presets one dispatch selects, each naming a different brief."""

    def __init__(self, first: Preset, later: Preset) -> None:
        super().__init__(
            f"prosiform.{first.name}.brief and prosiform.{later.name}.brief name "
            f"{first.brief!r} and {later.brief!r}"
        )
        self.first = first
        self.later = later


def brief_of(tags: frozenset[str], conversion: Conversion) -> str | None:
    """The fragment naming the section a dispatch selecting `tags` carries as its brief.

    A named preset the tags select layers over `default`, so its brief
    holds over `default`'s. Two selected presets naming different briefs
    leave nothing saying which is carried, so they raise `Briefs`. A
    dispatch whose presets in force name none carries no brief.
    """
    found: Preset | None = None
    for preset in matching_presets(conversion, tags):
        if preset.brief is None:
            continue
        if found is not None and found.brief != preset.brief:
            raise Briefs(found, preset)
        found = found or preset
    if found is not None:
        return found.brief
    return conversion.default.brief


class Levels(Exception):
    """Two presets one reference selects, each stating a different level or model.

    `level` names the level two `levels` maps give different models, and
    is absent where the two presets state different `level`s.
    """

    def __init__(self, first: Preset, later: Preset, level: str | None) -> None:
        field = "level" if level is None else f"levels.{level}"
        stated = (
            (first.level, later.level)
            if level is None
            else (dict(first.levels)[level], dict(later.levels)[level])
        )
        super().__init__(
            f"prosiform.{first.name}.{field} and prosiform.{later.name}.{field} "
            f"state {stated[0]!r} and {stated[1]!r}"
        )
        self.first = first
        self.later = later


class Unmapped(Exception):
    """A level the run's level map names no model for."""

    def __init__(self, level: str) -> None:
        super().__init__(level)
        self.level = level


def level_of(tags: frozenset[str], conversion: Conversion) -> str | None:
    """The capability level a reference selecting `tags` puts in force.

    A named preset the tags select layers over `default`, so its level
    holds over `default`'s. Two selected presets stating different
    levels raise `Levels`. A document whose presets in force state none
    has no level.
    """
    found: Preset | None = None
    for preset in matching_presets(conversion, tags):
        if preset.level is None:
            continue
        if found is not None and found.level != preset.level:
            raise Levels(found, preset, None)
        found = found or preset
    if found is not None:
        return found.level
    return conversion.default.level


def level_map(
    tags: frozenset[str], conversion: Conversion
) -> tuple[tuple[str, str], ...]:
    """The level map a run entering a document with `tags` resolves every dispatch by.

    Each named preset the tags select layers its `levels` over
    `default`'s, level by level, and two selected presets giving one
    level different models raise `Levels`.
    """
    held = dict(conversion.default.levels)
    stated: dict[str, Preset] = {}
    for preset in matching_presets(conversion, tags):
        for level, model in preset.levels:
            earlier = stated.get(level)
            if earlier is not None and dict(earlier.levels)[level] != model:
                raise Levels(earlier, preset, level)
            stated.setdefault(level, preset)
            held[level] = model
    return tuple(held.items())


def model_of(target: Reference, conversion: Conversion) -> str | None:
    """Look up the model for the target's `level_of` selection.

    A target with no selected level yields none. A selected level absent
    from the conversion's model map raises `Unmapped`.
    """
    level = level_of(target.tags - {PICK}, conversion)
    if level is None:
        return None
    model = dict(conversion.models).get(level)
    if model is None:
        raise Unmapped(level)
    return model


def briefing(target: Reference, conversion: Conversion) -> Reference | None:
    """Build the composing reference for the section `brief_of` selects.

    The reference keeps the target's context and tags except the pick
    token, names the decoded brief fragment, and sets the composition
    flag. A target with no brief yields none.
    """
    brief = brief_of(target.tags, conversion)
    if brief is None:
        return None
    return replace(
        target,
        original=f"{target.walk or target.path}{brief}",
        fragment=admissible(decoded(brief[1:], FRAGMENT_PART), FRAGMENT_PART),
        tags=target.tags - {PICK},
        composes=True,
        defers=False,
    )


def dispatched(opening: str) -> bool:
    """Whether recognized operators include either dispatch mark."""
    found = operators(opening)
    return DISPATCH_MARK in found or PARALLEL_MARK in found


def parallel(opening: str) -> bool:
    """Whether a link states that its dispatch runs beside its section's others."""
    return PARALLEL_MARK in operators(opening)


def withholding(opening: str) -> bool:
    """Whether `deferred` or `dispatched` recognizes the link's operation."""
    return deferred(opening) or dispatched(opening)


def unmarked(text: str) -> str:
    """Return link text after the operator recognized by `marks.opened`.

    Text with no recognized operator is returned as written.
    `published_text` owns publication of a dispatch mark.
    """
    found = opened(text)
    return text if found is None else text[found.after :]


def filed(destination: str) -> bool:
    """Whether a destination the bundle gave a dispatch names a file beside it."""
    return not destination.startswith(ANCHOR)


def published_text(text: str, file: bool) -> str:
    """Return the link label for its published destination.

    A recognized dispatch or parallel mark becomes a dispatch mark and
    one space when `file` is true. Other recognized marks and their
    spacing are removed. Text without an operator stays as written.
    `marks.opened` owns recognition of the opening.
    """
    found = opened(text)
    if found is None:
        return text
    rest = text[found.after :]
    if file and found.marks in (DISPATCH_MARK, PARALLEL_MARK):
        return f"{DISPATCH_MARK}{SPACE}{rest}"
    return rest


def directive(opening: str) -> bool:
    """Whether recognized operators include the composition mark."""
    return INLINE_MARK in operators(opening)


def resolve(
    text: str, base: str = "", *, tags: frozenset[str] = frozenset()
) -> Reference:
    """Resolve a destination against `base`, retaining its authored access walk.

    `components` splits the URI before `segment` decodes local path parts;
    `normalized` supplies the path identity. Drive-qualified and absolute
    paths raise `OutsideRoot`; a local query or backslash raises `Malformed`.
    `source.external` owns external-path classification. A nonempty
    fragment passes through `decoded` and `admissible`.
    """
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
        return Reference(text, path, walk=walk, tags=tags)
    return Reference(
        text,
        path,
        admissible(decoded(written.fragment, FRAGMENT_PART), FRAGMENT_PART),
        walk=walk,
        tags=tags,
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
    """Cache the answers supplied by a caller's declaration probe."""

    def __init__(self, probe: Callable[[Reference], Probed]) -> None:
        self._probe = probe
        self._answers: dict[str, Probed] = {}

    def answer(self, found: Reference) -> Probed:
        """Probe a canonical path once, using its first reference's context.

        Later references to that path reuse the cached answer.
        """
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
    *,
    tags: frozenset[str] = frozenset(),
) -> Reference:
    """Resolve a link against its writing document, then apply substitution.

    `resolve` owns path grammar and normalization. A fragment-only link
    uses `document` as its path and access walk; other local links retain
    the writing directory in their access walk. External references return
    directly. The writer's `Substitution.redirect` receives `origin`.
    """
    base = posixpath.dirname(document)
    found = resolve(text, base, tags=tags)
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
    *,
    tags: frozenset[str] = frozenset(),
) -> Reference | None:
    """Return the `resolvable` target unless `withholding` excludes this run."""
    if withholding(opening):
        return None
    return resolvable(
        document, text, declarations, substitution, origin, reached, tags=tags
    )


def withholding_target(
    document: str,
    text: str,
    opening: str,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    origin: str | None = None,
    reached: Sequence[str] = (),
    *,
    tags: frozenset[str] = frozenset(),
) -> Reference | None:
    """Return the `resolvable` target when `withholding` excludes this run."""
    if not withholding(opening):
        return None
    return resolvable(
        document, text, declarations, substitution, origin, reached, tags=tags
    )


def resolvable(
    document: str,
    text: str,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    origin: str | None = None,
    reached: Sequence[str] = (),
    *,
    tags: frozenset[str] = frozenset(),
) -> Reference | None:
    """Return a `named` reference whose target `Declarations.declares` accepts.

    The probe receives the reference's occurrence context. The returned
    target carries no origin or inclusion chain.
    """
    found = named(document, text, substitution, origin, reached, tags=tags)
    if found is None or not declarations.declares(found):
        return None
    return replace(found, origin=None, chain=())


def named(
    document: str,
    text: str,
    substitution: Substitution = UNSUBSTITUTED,
    origin: str | None = None,
    reached: Sequence[str] = (),
    *,
    tags: frozenset[str] = frozenset(),
) -> Reference | None:
    """Return a local Markdown reference with its origin and extended chain.

    `inside` resolves and substitutes the destination, `source.external`
    classifies external paths, and `profile.is_markdown` decides suffixes.
    An unresolvable reference or one failing classification yields none.
    """
    try:
        found = inside(document, text, substitution, origin, tags=tags)
    except Unresolvable:
        return None
    if found.external or not is_markdown(found.path):
        return None
    return replace(found, origin=origin, chain=(*reached, identity(found)))


@dataclass(frozen=True)
class BundleFolder:
    """The absolute POSIX paths of the working directory and bundle folder.

    `root` holds the working directory and `folder` the bundle's folder,
    for the relative paths `published` and `rooted` calculate.
    """

    root: str
    folder: str

    def published(self, path: str) -> str:
        """One canonical source path as the path from the bundle's folder to it."""
        return posixpath.relpath(posixpath.join(self.root, path), self.folder)

    def rooted(self, path: str) -> str:
        """One path from the bundle's folder as the canonical source path it names."""
        return posixpath.relpath(
            posixpath.normpath(posixpath.join(self.folder, path)), self.root
        )


WORKING_FOLDER = BundleFolder(SEPARATOR, SEPARATOR)
"""A bundle folder that is the invocation working directory itself."""


def rebased(found: Reference, text: str, folder: BundleFolder = WORKING_FOLDER) -> str:
    """URI-escape a deferred target's path from its bundle folder.

    `BundleFolder.published` supplies the relative path, whose segments
    are escaped independently. A resolved fragment is retained; when it
    is absent, `components` supplies the authored fragment, including an
    empty one.
    """
    relative = folder.published(found.path)
    path = SEPARATOR.join(quote(part, safe="") for part in relative.split(SEPARATOR))
    if found.fragment is not None:
        return f"{path}{FRAGMENT}{found.fragment}"
    fragment = components(text).fragment
    if fragment is None:
        return path
    return f"{path}{FRAGMENT}{fragment}"


def carried_names(
    found: Reference, conversions: Mapping[str, Conversion] | None
) -> tuple[str, ...]:
    """The run's names a deferral publishes beside its own title tags.

    `metadata.Conversion.carried` supplies the target's names. Exclude
    those the reference's tags name, and return the remainder in code
    point order. A target with no captured conversion supplies none.
    """
    conversion = None if conversions is None else conversions.get(found.path)
    if conversion is None:
        return ()
    return tuple(sorted(conversion.carried() - found.tags))


def deferred_title(title: str | None, names: Sequence[str]) -> str | None:
    """The title a deferral publishes: its author's, then the run's names it carries.

    The names join the authored tags as further comma-separated names,
    so the run bundling the deferral reads both from one title.
    """
    if not names:
        return title
    joined = ", ".join(names)
    return f"{title}, {joined}" if title else joined
