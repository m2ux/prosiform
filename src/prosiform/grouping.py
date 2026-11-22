"""Arrange selected document content into merged groups.

`prepared` records each member's selected content. `merged` combines those
members into a `bundle.Group` with its heading targets and provenance.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from pathlib import PurePosixPath

from markdown_it.token import Token

from prosiform.bundle import (
    ATX,
    MAX_LEVEL,
    Group,
    Overflow,
    Unplaced,
    absorbed,
    ancestry,
    carried_headings,
    document_title,
    emitted_text,
    escaped,
    line_of,
    placing_in,
    region,
    required,
    rewrite,
    shown_text,
    single_line,
    source_fragments,
)
from prosiform.closure import (
    DECLARING,
    UNSUBSTITUTED,
    WORKING_FOLDER,
    BundleFolder,
    Declarations,
    Substitution,
)
from prosiform.heading import WORD, title_cased, worded
from prosiform.metadata import Conversion
from prosiform.provenance import (
    GROUP_HEADING,
    MEMBER_OVERVIEW,
    OVERVIEW_SECTION,
    VARIANT_HEADING,
    Ancestor,
    Carried,
    Dispatching,
    Emitted,
    Generated,
    Located,
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
SLASH = "/"
MARKDOWN_SPACE = " \t"


def states(heading: str, word: str) -> bool:
    """Whether a group's heading already states one word of a member's stem.

    Compare `source.slug` values, accepting the member word alone or
    followed by a plural s as the group's name.
    """
    one, other = slug(heading), slug(word)
    return one in (other, f"{other}s")


def without_stated(heading: str, named: str) -> str:
    """One member's name, less a trailing word the group's heading states.

    The word goes with the separator joining it to the rest of the name,
    and a name of one word keeps it, so no name is left empty.
    """
    found = list(WORD.finditer(heading))
    if len(found) > 1 and states(named, found[-1].group()):
        return heading[: found[-2].end()]
    return heading


def member_headings(paths: Sequence[str], named: str) -> dict[str, str]:
    """The shortest displayed path name distinguishing each group member.

    Discard shared leading directories, then extend trailing path segments
    until the displayed names differ. `without_stated` removes the group's
    trailing word; retain complete names when removal leaves a collision.
    Spelling uses `heading.title_cased` and the fallback from `worded_names`.
    The mapping serves both overview subsections and variant headings.
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
            path: title_cased(SLASH.join(parts[-run:]))
            for path, parts in trimmed.items()
        }
        headings = {
            path: without_stated(heading, named) for path, heading in complete.items()
        }
        if len(set(headings.values())) == len(headings):
            return worded_names(headings)
    return worded_names(complete)


def worded_names(headings: Mapping[str, str]) -> dict[str, str]:
    """Member names, with `heading.title_cased` paths for unworded names."""
    return {
        path: heading if worded(heading) else title_cased(path)
        for path, heading in headings.items()
    }


@dataclass(frozen=True)
class Item:
    """A member item: `token` holds its region or heading; `ancestor` marks outline."""

    token: Token
    ancestor: bool


@dataclass
class Member:
    """The data one document contributes to a merged arrangement.

    `path` names its source; `tokens` and `written` hold parsed and rewritten
    content. `removed` identifies excluded lines. `text` maps heading identities
    to published text, `named` to source fragments, and `chains` to ancestors.
    `emitting` and `ancestors` identify selected and structural tokens. `title`
    holds its source title; `absorbing` holds the title named by its subsection.
    `first_line` locates content in its file; `items` holds its arranged items.
    """

    path: str
    tokens: Sequence[Token]
    written: Sequence[str]
    removed: set[int]
    text: dict[int, str]
    named: dict[int, str]
    chains: dict[int, tuple[Token, ...]]
    emitting: set[int]
    ancestors: set[int]
    title: Token | None
    absorbing: Token | None
    first_line: int = 1
    items: list[Item] = field(default_factory=list)

    def shift(self, at: int, content: Sequence[Item]) -> int:
        """The levels the member's content beneath its subsection moves by.

        The subsection naming the member sits at the level supplied. The
        shallowest heading the content carries takes the level directly
        beneath it, and every other heading keeps its distance from that
        one, so no level beneath the subsection stands empty. Content
        carrying no heading has no level to place.
        """
        levels = [level(one.token) for one in content if one.token.type == HEADING_OPEN]
        return at + 1 - min(levels) if levels else at - 1


def prepared(
    path: str,
    tokens: Sequence[Token],
    physical: Sequence[str],
    defined: Mapping[str, Definition],
    selected: Selection | None,
    assigned: dict[tuple[str, str | None], str] | None,
    depth: int,
    declarations: Declarations = DECLARING,
    keep_title: bool = False,
    dispatching: Dispatching | None = None,
    first_line: int = 1,
    substitution: Substitution = UNSUBSTITUTED,
    composing: Mapping[Located, str] | None = None,
    *,
    conversions: Mapping[str, Conversion],
    folder: BundleFolder = WORKING_FOLDER,
) -> Member:
    """Prepare one merged member's selected items, headings and source records.

    Use `bundle.required` for ancestors and `bundle.rewrite` for selected link
    edits. `bundle.absorbed` identifies a title the member subsection names;
    `keep_title` preserves the parent's title. `first_line` locates link errors
    in the original file.
    """
    removed = {
        at for one in defined.values() for at in range(one.lines[0], one.lines[1])
    }
    emitting = (
        {id(token) for token in regions(tokens)}
        if selected is None
        else {id(token) for token in selected.regions}
    )
    text = shown_text(path, tokens, declarations, substitution, conversions=conversions)
    named = source_fragments(tokens)
    titled_token = absorbed(tokens, PurePosixPath(path).stem)
    absorbing = (
        None
        if keep_title
        else titled_token
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
        else rewrite(
            physical,
            tokens,
            chosen,
            assigned,
            path,
            defined,
            declarations,
            dispatching,
            first_line,
            substitution,
            composing,
            conversions=conversions,
            folder=folder,
        )
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
        titled_token,
        absorbing,
        first_line,
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
    held = placing_in(member.tokens, token)
    if held is not None:
        raise Unplaced(member.path, line_of(token, member.first_line), *held)
    depth = level(token) + by
    if depth > MAX_LEVEL:
        raise Overflow(member.text[id(token)], depth, member.path)
    shows = single_line(member.text[id(token)])
    recorded = Ancestor(shows, depth, (origin_of(member, token, by),))
    return f"{ATX * depth} {escaped(shows)}", recorded


def generated_part(
    text: str, depth: int, kind: str, answers: Sequence[Target], path: str
) -> tuple[str, Generated]:
    """One heading the arrangement writes itself, as the part it is emitted as.

    The caller supplies the depth; a value above `bundle.MAX_LEVEL`
    raises `Overflow` against `path`. The returned `Generated` records
    the text, depth, kind and answers supplied by the caller.
    """
    if depth > MAX_LEVEL:
        raise Overflow(text, depth, path)
    recorded = Generated(text, depth, kind, tuple(answers))
    return f"{ATX * depth} {escaped(text)}", recorded


class Assembly:
    """Accumulate emitted text, provenance parts and heading records.

    `offset` sets the section and member heading levels relative to the group's
    top-level arrangement.
    """

    def __init__(self, offset: int = 0) -> None:
        self.section_level = SECTION_LEVEL + offset
        self.member_level = MEMBER_LEVEL + offset
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


def above_depth(member: Member, depth: int) -> list[Item]:
    """The items of one member that sit above the grouping depth, in source order."""
    return [
        one
        for one in member.items
        if (found := anchored(member, one.token, depth)) is None or level(found) < depth
    ]


def beneath(member: Member, token: Token, items: Sequence[Item]) -> list[Item]:
    """The items one heading of a member holds, in source order."""
    return [
        one
        for one in items
        if any(held is token for held in member.chains[id(one.token)])
    ]


def merged_only(member: Member, token: Token, depth: int) -> bool:
    """Whether a heading above the grouping depth holds only what the merge carries.

    Its section holds a selected item at the grouping depth and no
    content above that depth but headings.
    """
    held = [one for one in beneath(member, token, member.items) if not one.ancestor]
    at_depth = [
        (found := anchored(member, one.token, depth)) is not None
        and level(found) == depth
        for one in held
    ]
    return any(at_depth) and all(
        merged or one.token.type == HEADING_OPEN
        for one, merged in zip(held, at_depth, strict=True)
    )


def overview_content(member: Member, depth: int) -> list[Item]:
    """Selected items above grouping depth that the overview carries.

    Exclude structural ancestors and headings recognized by `merged_only`.
    """
    return [
        one
        for one in above_depth(member, depth)
        if not one.ancestor
        and (
            one.token.type != HEADING_OPEN or not merged_only(member, one.token, depth)
        )
    ]


def outlined(member: Member, depth: int) -> list[Token]:
    """Each selected heading above the grouping depth the overview leaves out."""
    content = overview_content(member, depth)
    return [
        one.token
        for one in above_depth(member, depth)
        if not one.ancestor
        and one.token.type == HEADING_OPEN
        and all(kept is not one for kept in content)
    ]


def relocated(into: "Assembly", member: Member, depth: int) -> None:
    """Where a reference to a heading the overview leaves out resolves.

    Such a heading is answered by the first heading the group emits that
    answers a heading of its section, so the reference reaches the
    merged section carrying what it selected. Its section holds a
    selected section at the grouping depth, which the merged heading or
    the variant naming the member answers, so that heading exists.
    """
    for token in outlined(member, depth):
        held = {
            (member.path, member.named[id(one.token)])
            for one in beneath(member, token, member.items)
            if one.token.type == HEADING_OPEN
        }
        found = next(
            at for at, one in enumerate(into.headings) if held & set(one.answers)
        )
        into.answer(found, (member.path, member.named[id(token)]))


def situated(member: Member, depth: int) -> bool:
    """Whether the parent's own H1 can open the group."""
    return any(
        one.token.type == HEADING_OPEN and level(one.token) == 1
        for one in above_depth(member, depth)
    )


def situate(into: Assembly, member: Member, depth: int) -> None:
    """The parent's title and preamble, at the levels the author wrote."""
    for one in above_depth(member, depth):
        into.region(member, one.token, 0)


def arranged(
    depth: int,
    parent: Member | None,
    pooled: Sequence[tuple[str, list[tuple[Member, Token]]]],
) -> list[tuple[str, list[tuple[Member, Token]]]]:
    """Parent sections in parent order, then sections another member adds."""
    if parent is None:
        return list(pooled)
    order: list[str] = []
    for one in parent.items:
        anchor = anchored(parent, one.token, depth)
        if anchor is None or level(anchor) != depth:
            continue
        text = single_line(parent.text[id(anchor)])
        if text not in order:
            order.append(text)
    by = dict(pooled)
    leading = [(text, by[text]) for text in order if text in by]
    seen = set(order)
    return leading + [(text, contrib) for text, contrib in pooled if text not in seen]


def direct(into: Assembly, member: Member) -> None:
    """Assign the parent's whole-document target to its selected title heading.

    Use `bundle.document_title` to identify the title. Leave the target alone
    when that title is absent from the emitted headings.
    """
    title = document_title(member.tokens)
    if title is None:
        return
    target: Target = (member.path, member.named[id(title)])
    for at, heading in enumerate(into.headings):
        if target in heading.answers:
            into.answer(at, (member.path, None))
            return


def merged(
    named: str,
    depth: int,
    members: Sequence[Member],
    parent: str | None = None,
    at: int = GROUP_LEVEL,
) -> Group:
    """Assemble prepared members into one named group at the supplied level.

    Members must arrive in placement order. `situated` decides whether the
    parent title opens the group, `arranged` orders its sections, and `overview`
    and `sections` emit them. `direct`, `contributed` and `relocated` record the
    targets answered by the resulting headings.
    """
    into = Assembly(at - GROUP_LEVEL)
    parent_member = next((one for one in members if one.path == parent), None)
    kept = False
    if parent_member is not None and situated(parent_member, depth):
        situate(into, parent_member, depth)
        kept = True
    else:
        title = title_cased(named).strip(MARKDOWN_SPACE)
        text, recorded = generated_part(title, at, GROUP_HEADING, (), members[0].path)
        into.emitted.append(text)
        into.heading(recorded)
    pooled = contributions(depth, members)
    headings = member_headings([m.path for m in members], named)
    order = arranged(depth, parent_member, pooled)
    if not kept:
        overview(into, headings, depth, members, bool(pooled), parent)
    sections(into, depth, order, headings, parent)
    if kept:
        others = [one for one in members if one is not parent_member]
        overview(into, headings, depth, others, bool(pooled), parent)
    if parent_member is not None:
        direct(into, parent_member)
    for member in members:
        contributed(into, member)
        if not kept or member is not parent_member:
            relocated(into, member, depth)
    return Group(
        tuple(into.emitted),
        Record(named, depth, tuple(into.headings), tuple(into.parts)),
        wrapped=not kept,
        level=at,
    )


def names_one(one: Emitted, path: str) -> bool:
    """Whether a heading's origins or target answers identify only one member.

    Inspect origins for `provenance.Carried` and answers for
    `provenance.Generated`; a structural ancestor names no target.
    """
    if isinstance(one, Generated):
        return bool(one.answers) and all(target[0] == path for target in one.answers)
    if isinstance(one, Carried):
        return bool(one.origins) and all(origin.path == path for origin in one.origins)
    return False


def contributed(into: "Assembly", member: Member) -> None:
    """Assign a whole-document target for a member lacking a subsection.

    Choose the first contributed heading `names_one` identifies as unique to
    the member, otherwise its first contributed heading, otherwise the group's
    opening. A target already answered by another heading is left alone.
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
    parent: str | None = None,
) -> None:
    """Emit member subsections, optionally beneath an Overview heading.

    `overview_content` supplies each member's content. A member takes a
    subsection when it carries that content, absorbs a selected title, or
    has no selected items. `member_headings` supplies the names. Emit the Overview
    heading only when merged sections and nonempty overview content coexist.
    """
    above = {member.path: overview_content(member, depth) for member in members}
    named_here = {
        member.path: bool(above[member.path])
        or not [one for one in member.items if not one.ancestor]
        or member.absorbing is not None
        for member in members
    }
    if not any(named_here.values()):
        return
    wrapped = pooled and any(
        above[member.path] for member in members if named_here[member.path]
    )
    at = into.member_level if wrapped else into.section_level
    if wrapped:
        text, recorded = generated_part(
            OVERVIEW, into.section_level, OVERVIEW_SECTION, (), members[0].path
        )
        into.part(text, recorded, [recorded])
    for member in members:
        if not named_here[member.path]:
            continue
        content = above[member.path]
        if (
            not content
            and member.absorbing is not None
            and id(member.absorbing) not in member.emitting
            and any(not one.ancestor for one in member.items)
        ):
            continue
        answers: list[Target] = []
        if member.path != parent:
            answers.append((member.path, None))
        if member.absorbing is not None:
            answers.append((member.path, member.named[id(member.absorbing)]))
        text, recorded = generated_part(
            headings[member.path], at, MEMBER_OVERVIEW, answers, member.path
        )
        into.part(text, recorded, [recorded])
        by = member.shift(at, content)
        for one in content:
            into.region(member, one.token, by)


def contributions(
    depth: int, members: Sequence[Member]
) -> list[tuple[str, list[tuple[Member, Token]]]]:
    """Distinct section texts and their contributing members, in first-use order.

    Read members in their supplied placement order and headings in source order.
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
    parent: str | None = None,
) -> None:
    """One merged heading for each distinct heading text at the grouping depth."""
    for text, contributing in pooled:
        section(into, depth, text, contributing, headings, parent)


def section(
    into: Assembly,
    depth: int,
    text: str,
    contributing: Sequence[tuple[Member, Token]],
    headings: Mapping[str, str],
    parent: str | None = None,
) -> None:
    """One merged section: its heading, then the content its members contribute.

    The parent's contribution leads a section several members share.
    A reference to a contributor's heading resolves to the variant
    heading naming that document where the section splits into variants,
    and to the merged heading where one document contributes it.
    """
    if parent is not None:
        contributing = tuple(
            sorted(contributing, key=lambda pair: pair[0].path != parent)
        )
    by = into.section_level - depth
    variants = len(contributing) > 1
    answers = tuple(
        (member.path, member.named[id(anchor)])
        for member, anchor in contributing
        if id(anchor) in member.emitting
    )
    merged_heading(
        into, text, into.section_level, contributing, by, () if variants else answers
    )
    if variants:
        for member, anchor in contributing:
            heading, recorded = generated_part(
                headings[member.path],
                into.member_level,
                VARIANT_HEADING,
                [(member.path, member.named[id(anchor)])]
                if id(anchor) in member.emitting
                else [],
                member.path,
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
