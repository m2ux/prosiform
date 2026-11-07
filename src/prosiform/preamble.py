"""Source preambles carried beside a fragment selection, grouped by parent folder."""

from collections.abc import Mapping, Sequence
from pathlib import PurePosixPath

from markdown_it.token import Token

from prosiform.bundle import (
    Group,
    carried_headings,
    emitted_text,
    region,
)
from prosiform.closure import (
    DECLARING,
    UNSUBSTITUTED,
    Declarations,
    Substitution,
    inside,
)
from prosiform.grouping import Assembly, Member, generated_part, origin_of, prepared
from prosiform.heading import title_cased
from prosiform.metadata import Conversion
from prosiform.provenance import (
    GROUP_HEADING,
    PREAMBLE_HEADING,
    Carried,
    Preamble,
    PreambleRecord,
)
from prosiform.rewrite import Definition, rewritten
from prosiform.source import (
    HEADING_OPEN,
    Selection,
    Source,
    inlines,
    level,
    lines,
    regions,
)

PREAMBLE_DEPTH = 2


def selected(tokens: Sequence[Token]) -> Selection | None:
    """The H1 title and content up to the first H2, where a document has a title."""
    spans = list(regions(tokens))
    title = next(
        (token for token in spans if token.type == HEADING_OPEN and level(token) == 1),
        None,
    )
    if title is None:
        return None
    held = []
    for token in spans:
        if token is title:
            held.append(token)
        elif held and token.type == HEADING_OPEN and level(token) <= PREAMBLE_DEPTH:
            break
        elif held:
            held.append(token)
    return Selection(tuple(held))


def destination(
    path: str,
    written: str,
    targets: Mapping[tuple[str, str | None], str],
    substitution: Substitution,
) -> str | None:
    """A bundled target's fragment, or nothing where this selection carries none."""
    found = inside(path, written, substitution.unrecorded().writing(path))
    if found.external or (found.path, found.fragment) not in targets:
        return None
    return f"#{targets[(found.path, found.fragment)]}"


def rewritten_preamble(
    member: Member,
    targets: Mapping[tuple[str, str | None], str],
    substitution: Substitution,
    definitions: Mapping[str, Definition],
) -> list[str]:
    """The preamble's lines, with links to carried targets pointed at their headings."""
    if not targets:
        return list(member.written)
    written = list(member.written)
    for item in member.items:
        for inline in inlines(member.tokens, [item.token]):
            if inline.map is None:
                continue
            start, end = inline.map
            targets_here = []
            for child in inline.children or []:
                if child.type != "link_open":
                    continue
                targets_here.append(
                    destination(
                        member.path,
                        str(child.attrGet("href") or ""),
                        targets,
                        substitution,
                    )
                )
            if targets_here:
                written[start:end] = rewritten(
                    written[start:end], inline, targets_here, definitions
                )
    return written


def grouped(
    paths: Sequence[str],
    parsed: Mapping[str, Sequence[Token]],
    read: Mapping[str, Source],
    defined: Mapping[str, Mapping[str, Definition]],
    selections: Mapping[str, Selection | None],
    targets: Mapping[tuple[str, str | None], str] | None,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    *,
    conversions: Mapping[str, Conversion],
) -> Group | None:
    """One H2 folder group holding each partial member's preamble at H3."""
    members = []
    for path in paths:
        choice = selected(parsed[path]) if selections[path] is not None else None
        if choice is None:
            continue
        member = prepared(
            path,
            parsed[path],
            lines(read[path].text),
            defined[path],
            choice,
            None,
            PREAMBLE_DEPTH,
            declarations,
            substitution=substitution,
            conversions=conversions,
        )
        if targets is not None:
            member.written = rewritten_preamble(
                member, targets, substitution, defined[path]
            )
        members.append(member)
    if not members:
        return None
    folder = str(PurePosixPath(members[0].path).parent)
    into = Assembly()
    heading, record = generated_part(
        title_cased(PurePosixPath(folder).name),
        2,
        GROUP_HEADING,
        (),
        members[0].path,
    )
    into.emitted.append(heading)
    into.heading(record)
    for member in members:
        name = title_cased(PurePosixPath(member.path).stem)
        heading, record = generated_part(
            name,
            3,
            PREAMBLE_HEADING,
            ((member.path, None),),
            member.path,
        )
        into.part(heading, record, [record])
        for item in member.items:
            if item.ancestor or item.token is member.absorbing:
                continue
            start, end = item.token.map or (0, 0)
            carried = carried_headings(member.tokens, item.token)
            into.part(
                region(
                    member.written,
                    member.tokens,
                    item.token,
                    member.shift(2),
                    member.removed,
                ),
                Preamble(
                    member.path,
                    (start, end),
                    tuple(at for at in range(start, end) if at in member.removed),
                ),
                [
                    Carried(
                        emitted_text(one, member.text[id(one)], member.shift(2)),
                        level(one) + member.shift(2),
                        (origin_of(member, one, member.shift(2)),),
                        ((member.path, member.named[id(one)]),),
                    )
                    for one in carried
                ],
            )
    return Group(
        tuple(into.emitted),
        PreambleRecord(folder, 2, tuple(into.headings), tuple(into.parts)),
        level=2,
    )
