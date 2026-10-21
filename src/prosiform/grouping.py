"""The merged group: one part of the source tree arranged by heading rather than file.

A grouping rule names a directory slug and a source heading level, and
every document under any directory of that slug is merged at that level,
beneath one heading carrying the slug in title case. A document no rule
names keeps its own file group, so one bundle can carry both
arrangements.

A merged group emits its slug as an H1, an `Overview` section holding
what its members carry above the grouping depth, and then one H2 for each
distinct source heading text at that depth. A member's heading at the
grouping depth is replaced by the merged one and its content moves to sit
beneath it, so the level a heading is emitted at is the level its author
wrote under a shift the arrangement supplies rather than a single shift
for the whole group.

A merged heading keeps its source text. Where that text occurs once in
the group it is emitted alone, and where several documents contribute it
the text is emitted once and each document's content hangs beneath it
under a variant heading naming the document. The name a variant heading
carries is the shortest run of that document's root-relative path which
distinguishes it from the others, in title case, measured after the
leading segments they all share are dropped, because those are the
context the group heading already states.

Two rules decide where a document's name goes, and they are applied in
that order. A merged section carrying body text above its first
subheading, in more than one document, is the document's section rather
than a container of named items, so it splits into variants by document
throughout. A section no such body splits is arranged by name, and the
names inside it that two or more documents contribute take variants of
their own.

The `Overview` section carries each member's content above the grouping
depth under a subsection named by that document's stem in title case,
less a trailing word the group's own heading already states. That heading
absorbs the member's own H1 where their slugs agree, as a file heading
absorbs the title it carries, and it is where a whole-document reference
to the member resolves. A member with nothing above the grouping depth
gets no subsection, and a reference to it resolves to its first
contribution instead; a member contributing nothing resolves to the
group's own heading, which carries it as it carries every member.

Grouping is decided before ancestry. The rules fix each document's
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

    A directory slug names a kind and its members are of that kind, so
    `modes` states `Mode`. Both sides are slugged, so the capitalization
    a filesystem carries decides nothing, and the plural the directory
    is named with is the one spelling a slug does not reconcile.
    """
    one, other = slug(heading), slug(word)
    return one in (other, f"{other}s")


def member_heading(path: str, named: str) -> str:
    """One member's overview subsection heading: its stem, in title case.

    A trailing word the group's own heading already states is dropped,
    because the subsection sits beneath that heading and a reader has
    read it there.
    """
    spelled = words(PurePosixPath(path).stem)
    if len(spelled) > 1 and states(named, spelled[-1]):
        spelled = spelled[:-1]
    return SPACE.join(word[:1].upper() + word[1:] for word in spelled)


def qualifiers(paths: Sequence[str]) -> dict[str, str]:
    """The name each document takes as a variant heading, by its path.

    The name is the shortest run of the path's trailing segments that
    tells the documents apart, measured after the leading segments they
    all share are dropped and with the Markdown suffix gone from the
    last of them. One segment distinguishes documents in one directory;
    documents of the same name in different directories take as many as
    their paths need.
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
    for run in range(1, longest + 1):
        taken = {path: tuple(one[-run:]) for path, one in trimmed.items()}
        if len(set(taken.values())) == len(taken):
            return {
                path: SPACE.join(titled(part) for part in each)
                for path, each in taken.items()
            }
    return {
        path: SPACE.join(titled(part) for part in each)
        for path, each in trimmed.items()
    }


@dataclass(frozen=True)
class Item:
    """One thing a member contributes: a selected region, or an ancestor heading."""

    token: Token
    ancestor: bool


@dataclass
class Member:
    """One document a grouping rule merges, read as the arrangement needs it."""

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

    @property
    def shift(self) -> int:
        """The levels the member's content above the grouping depth moves by.

        The subsection the overview carries it under sits at the third
        level, so a title that heading absorbs leaves the member's own
        H1 unemitted and its sections one level below the subsection;
        a title it does not absorb is emitted beneath the subsection
        and takes the level that makes room.
        """
        return MEMBER_LEVEL - 1 if self.absorbing is not None else MEMBER_LEVEL


def prepared(
    path: str,
    tokens: Sequence[Token],
    physical: Sequence[str],
    defined: Mapping[str, Definition],
    selected: Selection | None,
    assigned: dict[tuple[str, str | None], str] | None,
    depth: int,
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
        else rewrite(physical, tokens, chosen, assigned, path, defined)
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


def naming(member: Member, token: Token, depth: int) -> Token | None:
    """The heading just inside a merged section that holds one of its items."""
    chain = [*member.chains[id(token)]]
    if token.type == HEADING_OPEN:
        chain.append(token)
    inside = [one for one in chain if depth < level(one) <= depth + 1]
    return inside[-1] if inside else None


def merged(
    named: str,
    depth: int,
    members: Sequence[Member],
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
    overview(into, named, depth, members)
    sections(into, depth, members)
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


def contributed(into: "Assembly", member: Member) -> None:
    """Where a reference to one member resolves, the overview naming it nowhere.

    A member carrying nothing above the grouping depth is given no
    overview subsection, so the destinations that subsection holds —
    the document itself, and the title its own heading carries — are
    answered by the first heading the group emits from it. A member the
    arrangement emits no heading of its own for is answered by the
    group's own heading, which carries every member. Each of the two
    destinations is therefore one the bundle has, whatever the member
    contributes, so a reference the closure resolved into a merged group
    is rewritten rather than left for the entry line to read as one it
    never assigned.
    """
    answered = {target for one in into.headings for target in one.answers}
    wanted: list[Target] = [(member.path, None)]
    if member.absorbing is not None:
        wanted.append((member.path, member.named[id(member.absorbing)]))
    found = next(
        (
            at
            for at, one in enumerate(into.headings)
            if isinstance(one, Carried)
            and any(origin.path == member.path for origin in one.origins)
        ),
        GROUP_AT,
    )
    for target in wanted:
        if target not in answered:
            into.answer(found, target)


def overview(into: Assembly, named: str, depth: int, members: Sequence[Member]) -> None:
    """The group's `Overview` section: what each member carries above the depth."""
    above = {
        member.path: [
            one
            for one in member.items
            if (found := anchored(member, one.token, depth)) is None
            or level(found) < depth
        ]
        for member in members
    }
    if not any(above.values()):
        return
    text, recorded = generated_part(OVERVIEW, SECTION_LEVEL, OVERVIEW_SECTION, ())
    into.part(text, recorded, [recorded])
    for member in members:
        if not above[member.path]:
            continue
        answers: list[Target] = [(member.path, None)]
        if member.absorbing is not None:
            answers.append((member.path, member.named[id(member.absorbing)]))
        text, recorded = generated_part(
            member_heading(member.path, named), MEMBER_LEVEL, MEMBER_OVERVIEW, answers
        )
        into.part(text, recorded, [recorded])
        for one in above[member.path]:
            into.region(member, one.token, member.shift)


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


def keyed(member: Member, anchor: Token, depth: int) -> bool:
    """Whether one member writes body text above the first subheading of a section."""
    for one in under(member, anchor, depth):
        if one.token.type == HEADING_OPEN:
            return False
        return True
    return False


def sections(into: Assembly, depth: int, members: Sequence[Member]) -> None:
    """One H2 for each distinct source heading text at the grouping depth."""
    for text, contributing in contributions(depth, members):
        split = sum(keyed(member, anchor, depth) for member, anchor in contributing) > 1
        variants = split and len(contributing) > 1
        section(into, depth, text, contributing, variants)


def section(
    into: Assembly,
    depth: int,
    text: str,
    contributing: Sequence[tuple[Member, Token]],
    variants: bool,
) -> None:
    """One merged section: its heading, then the content its members contribute."""
    by = SECTION_LEVEL - depth
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
        qualified = qualifiers([member.path for member, _ in contributing])
        for member, anchor in contributing:
            heading, recorded = generated_part(
                qualified[member.path],
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
    names(into, depth, contributing, by)


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


def names(
    into: Assembly,
    depth: int,
    contributing: Sequence[tuple[Member, Token]],
    by: int,
) -> None:
    """The names inside one merged section, each emitted once for every document."""
    for member, anchor in contributing:
        for one in under(member, anchor, depth):
            if naming(member, one.token, depth) is None:
                into.region(member, one.token, by)
    found: dict[str, list[tuple[Member, Token]]] = {}
    for member, anchor in contributing:
        seen: list[Token] = []
        for one in under(member, anchor, depth):
            held = naming(member, one.token, depth)
            if held is None or held in seen:
                continue
            seen.append(held)
            found.setdefault(single_line(member.text[id(held)]), []).append(
                (member, held)
            )
    for text, carrying in found.items():
        name(into, depth, text, carrying, by)


def name(
    into: Assembly,
    depth: int,
    text: str,
    carrying: Sequence[tuple[Member, Token]],
    by: int,
) -> None:
    """One name inside a merged section, bare or carrying a variant per document."""
    at = depth + 1 + by
    if len(carrying) == 1:
        member, held = carrying[0]
        for one in held_items(member, held, depth):
            into.region(member, one.token, by)
        return
    merged_heading(into, text, at, carrying, by, ())
    qualified = qualifiers([member.path for member, _ in carrying])
    for member, held in carrying:
        heading, recorded = generated_part(
            qualified[member.path],
            at + 1,
            VARIANT_HEADING,
            [(member.path, member.named[id(held)])]
            if id(held) in member.emitting
            else [],
        )
        into.part(heading, recorded, [recorded])
        for one in held_items(member, held, depth):
            if one.token is held:
                continue
            into.region(member, one.token, by + 1)


def held_items(member: Member, held: Token, depth: int) -> list[Item]:
    """Every item of one member that sits under one name of a merged section."""
    anchor = anchored(member, held, depth)
    return [
        one
        for one in member.items
        if anchored(member, one.token, depth) is anchor
        and naming(member, one.token, depth) is held
    ]
