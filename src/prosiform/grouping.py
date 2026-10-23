"""The merged group: one part of the source tree arranged by heading rather than file.

Each contributing document declares its group name and source heading
level in conversion metadata. Members of the same group merge at that
level beneath its title-cased name. A document without conversion
settings keeps its individual file group.

A merged group emits its slug as an H1, a subsection naming each member
and holding what that member carries above the grouping depth, and then
one H2 for each distinct source heading text at that depth. A member's
heading at the grouping depth is replaced by the merged one and its
content moves to sit beneath it, so the level a heading is emitted at is
the level its author wrote under a shift the arrangement supplies rather
than a single shift for the whole group.

A merged heading keeps its source text. Where that text occurs once in
the group it is emitted alone, and where several documents contribute it
the text is emitted once and each document's content hangs beneath it
under a variant heading naming the document. The name a variant heading
carries is the shortest run of that document's root-relative path which
distinguishes it from the others, in title case, measured after the
leading segments they all share are dropped, because those are the
context the group heading already states.

Every section with more than one contributing document splits into
variants, whether those contributions hold body text, subheadings or
only the section heading. A sole contributor keeps its own arrangement.
Each member's name is measured once against the whole group and serves
both its overview subsection and every variant, following the same
qualification and group-word removal in both places.

A member's subsection is named by the shortest run of that document's
root-relative path which distinguishes it from the group's other
members, in title case, measured after the leading segments they all
share are dropped. A trailing word the group's heading states is
omitted where qualification still distinguishes the displayed names. It
carries the member's content above the grouping depth. That heading
absorbs the member's own H1 where their slugs agree, as a file heading
absorbs the title it carries, and it is where a whole-document reference
to the member resolves. A member whose H1 the heading absorbs takes a
subsection, as does one the arrangement emits nothing else from, so the
group names every member it merges; such a subsection is the heading
alone. A member whose content all sits at the grouping depth is named by
the merged sections it contributes to, and a reference to it resolves to
the first heading the group emits from it that no other member shares:
the variant heading naming the document where its contribution carries a
heading text another member contributes too, and the merged heading
itself where that text occurs once in the group. No two members of one
group therefore reach one destination.

The subsections sit beneath an `Overview` section where the group also
emits merged sections, so a member's preamble is read as that member's
rather than as one more of the group's own sections. Where the group
emits no merged section they are its whole structure and sit directly
beneath its heading.

Grouping is decided before ancestry. Conversion metadata fixes each document's
membership, its grouping depth and the shift each of its contributions
takes, and the chain of eligible ancestors is then read inside that
arrangement: above the grouping depth the group's own structure supplies
the chain, so only a heading at or below that depth is ever emitted as a
structural ancestor.
"""

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from pathlib import PurePosixPath

from markdown_it.token import Token

from prosiform.bundle import (
    ATX,
    MAX_LEVEL,
    SPACE,
    Group,
    Overflow,
    absorbed,
    ancestry,
    carried_headings,
    emitted_text,
    escaped,
    region,
    required,
    rewrite,
    shown_text,
    single_line,
    source_fragments,
)
from prosiform.provenance import (
    GROUP_HEADING,
    MEMBER_OVERVIEW,
    OVERVIEW_SECTION,
    VARIANT_HEADING,
    Ancestor,
    Carried,
    Emitted,
    Generated,
    Origin,
    Part,
    Range,
    Record,
    Target,
)
from prosiform.rewrite import Definition
from prosiform.source import HEADING_OPEN, Selection, level, regions, slug

OVERVIEW = "Overview"
GROUP_AT = 0
GROUP_LEVEL = 1
SECTION_LEVEL = 2
MEMBER_LEVEL = 3

WORDS = re.compile(r"[-_\s]+")


def words(text: str) -> list[str]:
    """One name as the words it is written from, a hyphen reading as a space."""
    return [word for word in WORDS.split(text) if word]


def titled(text: str) -> str:
    """One name in title case, each word keeping the spelling its source gave it."""
    return SPACE.join(word[:1].upper() + word[1:] for word in words(text))


def states(heading: str, word: str) -> bool:
    """Whether a group's heading already states one word of a member's stem.

    A group name can state a kind shared by its members, so
    `modes` states `Mode`. Both sides are slugged, so the capitalization
    a filesystem carries decides nothing, and the plural the group
    is named with is the one spelling a slug does not reconcile.
    """
    one, other = slug(heading), slug(word)
    return one in (other, f"{other}s")


def member_headings(paths: Sequence[str], named: str) -> dict[str, str]:
    """The final displayed name distinguishing each member of a merged group.

    Shared leading directories are omitted. Trailing path segments are
    added until the title-cased names, with the group's trailing word
    removed, distinguish the members. Where every segment is needed and
    removing that word still joins names, the complete names retain it.
    Overview subsections and variants use this same group-wide mapping.
    """
    spelled = {path: list(PurePosixPath(path).parts) for path in paths}
    shortest = min(len(one) for one in spelled.values())
    shared = 0
    while (
        shared < shortest - 1
        and len({tuple(one[: shared + 1]) for one in spelled.values()}) == 1
    ):
        shared += 1
    trimmed = {
        path: [*one[shared:-1], PurePosixPath(one[-1]).stem]
        for path, one in spelled.items()
    }
    longest = max(len(one) for one in trimmed.values())
    complete: dict[str, str] = {}
    for run in range(1, longest + 1):
        complete = {
            path: titled(SPACE.join(parts[-run:])) for path, parts in trimmed.items()
        }
        headings = {}
        for path, heading in complete.items():
            parts = heading.split(SPACE)
            if len(parts) > 1 and states(named, parts[-1]):
                parts = parts[:-1]
            headings[path] = SPACE.join(parts)
        if len(set(headings.values())) == len(headings):
            return headings
    return complete


@dataclass(frozen=True)
class Item:
    """One thing a member contributes: a selected region, or an ancestor heading."""

    token: Token
    ancestor: bool


@dataclass
class Member:
    """One document conversion metadata groups, read as the arrangement needs it."""

    path: str
    tokens: Sequence[Token]
    written: Sequence[str]
    removed: set[int]
    text: dict[int, str]
    named: dict[int, str]
    chains: dict[int, tuple[Token, ...]]
    emitting: set[int]
    ancestors: set[int]
    targets: tuple[Target, ...]
    title: Token | None
    absorbing: Token | None
    items: list[Item] = field(default_factory=list)

    def shift(self, at: int) -> int:
        """The levels the member's content above the grouping depth moves by.

        The subsection naming the member sits at the level supplied, so
        a title that heading absorbs leaves the member's own H1
        unemitted and its sections one level below the subsection; a
        title it does not absorb is emitted beneath the subsection and
        takes the level that makes room.
        """
        return at - 1 if self.absorbing is not None else at


def prepared(
    path: str,
    tokens: Sequence[Token],
    physical: Sequence[str],
    defined: Mapping[str, Definition],
    selected: Selection | None,
    assigned: dict[tuple[str, str | None], str] | None,
    depth: int,
    root: str = "",
) -> Member:
    """One member of a merged group, with what it contributes already decided.

    The regions the run selected and the eligible ancestors they need
    are read here, as they are for a file group. The title the member's
    overview subsection names is absorbed where the member's own H1
    carries it, and is no structural ancestor either way, because the
    subsection stands in its place.
    """
    removed = {
        at for one in defined.values() for at in range(one.lines[0], one.lines[1])
    }
    emitting = (
        {id(token) for token in regions(tokens)}
        if selected is None
        else {id(token) for token in selected.regions}
    )
    text = shown_text(tokens)
    named = source_fragments(tokens)
    titled_token = absorbed(tokens, PurePosixPath(path).stem)
    absorbing = (
        titled_token
        if titled_token is not None
        and depth > level(titled_token)
        and id(titled_token) in emitting
        else None
    )
    needed = required(tokens, emitting) - (
        set() if titled_token is None else {id(titled_token)}
    )
    chosen = [token for token in regions(tokens) if id(token) in emitting]
    written = (
        list(physical)
        if assigned is None
        else rewrite(physical, tokens, chosen, assigned, path, defined, root)
    )
    targets: tuple[Target, ...] = (
        ((path, None),)
        if selected is None
        else tuple((path, named[id(token)]) for token in selected.named)
    )
    member = Member(
        path,
        tokens,
        written,
        removed,
        text,
        named,
        ancestry(tokens),
        emitting,
        needed,
        targets,
        titled_token,
        absorbing,
    )
    member.items = [
        Item(token, id(token) in needed)
        for token in regions(tokens)
        if (id(token) in emitting or id(token) in needed) and token is not absorbing
    ]
    return member


def anchored(member: Member, token: Token, depth: int) -> Token | None:
    """The heading at or above the grouping depth that places one item.

    The chain its author wrote above the item, with the item itself
    where that is a heading, is read down to the last heading no deeper
    than the grouping depth. A heading at exactly that depth is the
    merged section the item belongs to; anything shallower leaves the
    item above the grouping depth, which is what the overview carries.
    """
    chain = [*member.chains[id(token)]]
    if token.type == HEADING_OPEN:
        chain.append(token)
    shallow = [one for one in chain if level(one) <= depth]
    return shallow[-1] if shallow else None


def origin_of(member: Member, token: Token, by: int) -> Origin:
    """The identity one source heading carries into the record."""
    return Origin(
        member.path,
        None if token.map is None else token.map[0] + 1,
        level(token),
        member.named[id(token)],
        by,
    )


def carried_part(
    member: Member, token: Token, by: int
) -> tuple[str, Range, list[Carried]]:
    """One selected region as the group emits it, with the record it answers to."""
    held = carried_headings(member.tokens, token)
    for opening in held:
        if level(opening) + by > MAX_LEVEL:
            raise Overflow(member.text[id(opening)], level(opening) + by, member.path)
    start, end = token.map or (0, 0)
    recorded = Range(
        member.path,
        (start, end),
        tuple(at for at in range(start, end) if at in member.removed),
    )
    headings = [
        Carried(
            emitted_text(one, member.text[id(one)], by),
            level(one) + by,
            (origin_of(member, one, by),),
            ((member.path, member.named[id(one)]),),
        )
        for one in held
    ]
    return (
        region(member.written, member.tokens, token, by, member.removed),
        recorded,
        headings,
    )


def ancestor_part(member: Member, token: Token, by: int) -> tuple[str, Ancestor]:
    """One eligible ancestor the run did not select, emitted as a heading alone."""
    depth = level(token) + by
    if depth > MAX_LEVEL:
        raise Overflow(member.text[id(token)], depth, member.path)
    shows = single_line(member.text[id(token)])
    recorded = Ancestor(shows, depth, (origin_of(member, token, by),))
    return f"{ATX * depth} {escaped(shows)}", recorded


def generated_part(
    text: str, depth: int, kind: str, answers: Sequence[Target]
) -> tuple[str, Generated]:
    """One heading the arrangement writes itself, as the part it is emitted as."""
    recorded = Generated(text, depth, kind, tuple(answers))
    return f"{ATX * depth} {escaped(text)}", recorded


class Assembly:
    """The parts, headings and targets one merged group accumulates as it is built."""

    def __init__(self) -> None:
        self.emitted: list[str] = []
        self.parts: list[Part] = []
        self.headings: list[Emitted] = []

    def heading(self, one: Emitted) -> None:
        """Record one emitted heading."""
        self.headings.append(one)

    def answer(self, at: int, target: Target) -> None:
        """Record one more target the heading at a position is where it resolves."""
        one = self.headings[at]
        self.headings[at] = replace(one, answers=(*one.answers, target))

    def part(self, text: str, recorded: Part, headings: Sequence[Emitted] = ()) -> None:
        """Record one emitted part and every heading it carries."""
        self.emitted.append(text)
        self.parts.append(recorded)
        for one in headings:
            self.heading(one)

    def region(self, member: Member, token: Token, by: int) -> None:
        """Record one of a member's items, as the kind of part it is."""
        if id(token) in member.ancestors:
            text, ancestor = ancestor_part(member, token, by)
            self.part(text, ancestor, [ancestor])
            return
        text, recorded, headings = carried_part(member, token, by)
        self.part(text, recorded, headings)


def under(member: Member, anchor: Token, depth: int) -> list[Item]:
    """Every item of one member the named merged section holds, in source order."""
    return [
        one
        for one in member.items
        if anchored(member, one.token, depth) is anchor and one.token is not anchor
    ]


def merged(
    named: str,
    depth: int,
    members: Sequence[Member],
    displays: Mapping[str, str] | None = None,
) -> Group:
    """One merged group: its slug, the overview, and one section for each name.

    The members are in root-relative path order, which is the order
    every arrangement below reads them in, so one selection always
    bundles to the same bytes.
    """
    into = Assembly()
    title = titled(named)
    into.emitted.append(f"{ATX * GROUP_LEVEL} {escaped(title)}")
    into.heading(Generated(title, GROUP_LEVEL, GROUP_HEADING))
    pooled = contributions(depth, members)
    displays = {m.path: m.path for m in members} if displays is None else displays
    names = member_headings([displays[m.path] for m in members], named)
    headings = {m.path: names[displays[m.path]] for m in members}
    overview(into, headings, depth, members, bool(pooled))
    sections(into, depth, pooled, headings)
    for member in members:
        contributed(into, member)
    reached: dict[Target, int] = {}
    for at, one in enumerate(into.headings):
        for target in one.answers:
            reached.setdefault(target, at)
    entries = tuple(
        reached[target]
        for member in members
        for target in member.targets
        if target in reached
    )
    return Group(
        tuple(into.emitted),
        entries,
        Record(named, depth, tuple(into.headings), tuple(into.parts)),
        min(member.path for member in members),
    )


def names_one(one: Emitted, path: str) -> bool:
    """Whether one emitted heading names that member and no other.

    A carried heading answers to one source heading per contributing
    document, so a merged heading several documents write names none of
    them alone and a heading one document writes names that one. A
    generated heading carries no source heading, and the targets it
    answers are what it names: a variant heading answers one document's
    heading, and the group's own heading answers nothing. A structural
    ancestor answers nothing by construction and is no destination.
    """
    if isinstance(one, Generated):
        return bool(one.answers) and all(target[0] == path for target in one.answers)
    if isinstance(one, Carried):
        return bool(one.origins) and all(origin.path == path for origin in one.origins)
    return False


def contributed(into: "Assembly", member: Member) -> None:
    """Where a whole-document reference resolves for a member with no subsection.

    A member whose content all sits at the grouping depth is named by
    the merged sections it contributes to, so the document itself is
    answered by the first heading the group emits from it that no other
    member shares: the variant heading naming the document where its
    contribution carries a heading text another member contributes too,
    and the merged heading itself where that text occurs once in the
    group. Two members contributing one heading text therefore reach
    two destinations.

    Where the group emits no heading naming the member alone, the first
    heading it emits from the member answers, and the group's own
    heading where it emits none carrying it. That destination is
    therefore one the bundle has, whatever the member contributes, so a
    reference the closure resolved into a merged group is rewritten
    rather than left for the entry line to read as one it never
    assigned.
    """
    answered = {target for one in into.headings for target in one.answers}
    whole: Target = (member.path, None)
    if whole in answered:
        return
    alone = next(
        (at for at, one in enumerate(into.headings) if names_one(one, member.path)),
        None,
    )
    found = (
        alone
        if alone is not None
        else next(
            (
                at
                for at, one in enumerate(into.headings)
                if isinstance(one, Carried)
                and any(origin.path == member.path for origin in one.origins)
            ),
            GROUP_AT,
        )
    )
    into.answer(found, whole)


def overview(
    into: Assembly,
    headings: Mapping[str, str],
    depth: int,
    members: Sequence[Member],
    pooled: bool,
) -> None:
    """The subsection each member is named by, and the `Overview` carrying them.

    A member takes a subsection where it carries selected content above
    the grouping depth, where its own H1 is absorbed into that heading,
    and where the arrangement emits nothing else from it at all, so
    every member the group merges is named by a heading the bundle
    carries. A member whose selected content all sits at the grouping
    depth takes none: the merged sections it contributes to name it.

    The heading naming a member carries the run of its path that tells
    it apart from the group's other members, measured against every
    member the group merges rather than those taking a subsection, so
    one answer to what a member is called serves the whole group.

    The subsections sit beneath an `Overview` section where the group
    also emits merged sections, so a member's preamble is read as that
    member's rather than as one more of the group's own sections. Where
    the group emits no merged section the subsections are its whole
    structure, and they sit directly beneath its heading.
    """
    above = {
        member.path: [
            one
            for one in member.items
            if (found := anchored(member, one.token, depth)) is None
            or level(found) < depth
        ]
        for member in members
    }
    named_here = {
        member.path: bool(above[member.path])
        or not member.items
        or member.absorbing is not None
        for member in members
    }
    if not any(named_here.values()):
        return
    at = MEMBER_LEVEL if pooled else SECTION_LEVEL
    if pooled:
        text, recorded = generated_part(OVERVIEW, SECTION_LEVEL, OVERVIEW_SECTION, ())
        into.part(text, recorded, [recorded])
    for member in members:
        if not named_here[member.path]:
            continue
        answers: list[Target] = [(member.path, None)]
        if member.absorbing is not None:
            answers.append((member.path, member.named[id(member.absorbing)]))
        text, recorded = generated_part(
            headings[member.path], at, MEMBER_OVERVIEW, answers
        )
        into.part(text, recorded, [recorded])
        for one in above[member.path]:
            into.region(member, one.token, member.shift(at))


def contributions(
    depth: int, members: Sequence[Member]
) -> list[tuple[str, list[tuple[Member, Token]]]]:
    """Each distinct heading text at the grouping depth, with what contributes it.

    The order is first appearance across the members in path order, so
    a name enters the group where the first document carrying it puts
    it.
    """
    found: dict[str, list[tuple[Member, Token]]] = {}
    for member in members:
        seen: list[Token] = []
        for one in member.items:
            anchor = anchored(member, one.token, depth)
            if anchor is None or level(anchor) != depth or anchor in seen:
                continue
            seen.append(anchor)
            found.setdefault(single_line(member.text[id(anchor)]), []).append(
                (member, anchor)
            )
    return list(found.items())


def sections(
    into: Assembly,
    depth: int,
    pooled: Sequence[tuple[str, list[tuple[Member, Token]]]],
    headings: Mapping[str, str],
) -> None:
    """One H2 for each distinct source heading text at the grouping depth."""
    for text, contributing in pooled:
        section(into, depth, text, contributing, headings)


def section(
    into: Assembly,
    depth: int,
    text: str,
    contributing: Sequence[tuple[Member, Token]],
    headings: Mapping[str, str],
) -> None:
    """One merged section: its heading, then the content its members contribute."""
    by = SECTION_LEVEL - depth
    variants = len(contributing) > 1
    answers = (
        ()
        if variants
        else tuple(
            (member.path, member.named[id(anchor)])
            for member, anchor in contributing
            if id(anchor) in member.emitting
        )
    )
    merged_heading(into, text, SECTION_LEVEL, contributing, by, answers)
    if variants:
        for member, anchor in contributing:
            heading, recorded = generated_part(
                headings[member.path],
                MEMBER_LEVEL,
                VARIANT_HEADING,
                [(member.path, member.named[id(anchor)])]
                if id(anchor) in member.emitting
                else [],
            )
            into.part(heading, recorded, [recorded])
            for one in under(member, anchor, depth):
                into.region(member, one.token, by + 1)
        return
    for member, anchor in contributing:
        for one in under(member, anchor, depth):
            into.region(member, one.token, by)


def merged_heading(
    into: Assembly,
    text: str,
    at: int,
    contributing: Sequence[tuple[Member, Token]],
    by: int,
    answers: Sequence[Target],
) -> None:
    """One heading several documents contribute one text to, emitted once.

    Where a member selected the heading, the bytes its source wrote are
    what the group publishes, so the text keeps the inline content its
    author gave it. Where every member reached it as an ancestor alone,
    it is emitted as the literal title it is.
    """
    origins = [origin_of(member, anchor, by) for member, anchor in contributing]
    selecting = [
        (member, anchor)
        for member, anchor in contributing
        if id(anchor) in member.emitting
    ]
    if not selecting:
        if at > MAX_LEVEL:
            raise Overflow(text, at, contributing[0][0].path)
        alone = Ancestor(text, at, tuple(origins))
        into.part(f"{ATX * at} {escaped(text)}", alone, [alone])
        return
    member, anchor = selecting[0]
    published, recorded, _ = carried_part(member, anchor, by)
    into.part(published, recorded, [Carried(text, at, tuple(origins), tuple(answers))])
