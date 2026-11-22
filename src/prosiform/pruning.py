"""Prune unreferenced empty generated wrappers from the completed bundle outline."""

from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass, replace

from markdown_it.token import Token

from prosiform.bundle import Group, carried_headings
from prosiform.provenance import (
    GROUP_HEADING,
    MEMBER_OVERVIEW,
    OVERVIEW_SECTION,
    PREAMBLE_HEADING,
    Ancestor,
    Emitted,
    Generated,
    Range,
    Record,
)
from prosiform.source import HEADING_OPEN, regions


@dataclass(frozen=True)
class Removed:
    """One omitted section heading and the group that supplied it."""

    record: Record
    heading: Emitted


@dataclass(frozen=True)
class Block:
    """One emitted part, its heading positions and whether it contributes body."""

    group: int
    part: int
    first: int
    count: int
    heading: Emitted | None
    body: bool


def blocks(
    groups: Sequence[Group], parsed: Mapping[str, Sequence[Token]]
) -> list[Block]:
    """Classify each part using its source region and recorded headings."""
    indexed = {
        path: {tuple(token.map or (0, 0)): token for token in regions(tokens)}
        for path, tokens in parsed.items()
    }
    found = []
    first = 0
    for group_at, group in enumerate(groups):
        offset = int(group.wrapped)
        local = offset
        if group.wrapped:
            found.append(Block(group_at, 0, first, 1, group.record.headings[0], False))
            first += 1
        for at, (part, text) in enumerate(
            zip(group.record.parts, group.parts[offset:], strict=True), offset
        ):
            count = 0
            heading = None
            if isinstance(part, Generated | Ancestor):
                count = 1
                heading = group.record.headings[local]
            elif isinstance(part, Range):
                token = indexed[part.path][part.lines]
                count = len(carried_headings(parsed[part.path], token))
                if token.type == HEADING_OPEN:
                    heading = group.record.headings[local]
            found.append(
                Block(
                    group_at,
                    at,
                    first,
                    count,
                    heading,
                    heading is None and bool(text.strip()),
                )
            )
            local += count
            first += count
        assert local == len(group.record.headings)
    return found


def prune(
    groups: Sequence[Group],
    parsed: Mapping[str, Sequence[Token]],
    protected: Collection[int],
) -> tuple[list[Group], list[Removed], dict[int, int]]:
    """Remove empty, unreferenced generated group, overview and preamble wrappers.

    Authored headings, document identities and dispatch/composition sections
    remain. Referenced generated headings remain, as do their ancestors.
    A wrapper enclosing body content or retained structure remains at its
    existing level. Containers and code examples are content. Pruning
    follows composition and brief placement and precedes anchor assignment;
    its position map includes every retained heading, including headings
    carried inside containers. Source ranges are preserved in full.
    """
    flattened = blocks(groups, parsed)
    active: list[tuple[int, int]] = []
    occupied: set[int] = set()
    for block in flattened:
        if block.heading is not None:
            while active and active[-1][1] >= block.heading.level:
                active.pop()
            active.append((block.first, block.heading.level))
            if (
                not isinstance(block.heading, Generated)
                or block.heading.kind
                not in (
                    GROUP_HEADING,
                    MEMBER_OVERVIEW,
                    OVERVIEW_SECTION,
                    PREAMBLE_HEADING,
                )
                or id(block.heading) in protected
            ):
                occupied.update(at for at, _level in active)
        elif block.body:
            occupied.update(at for at, _level in active)
    kept: dict[int, list[int]] = {}
    headings: dict[int, list[Emitted]] = {}
    positions: dict[int, int] = {}
    removed = []
    all_headings = [heading for group in groups for heading in group.record.headings]
    for block in flattened:
        if block.heading is not None and block.first not in occupied:
            removed.append(Removed(groups[block.group].record, block.heading))
            continue
        kept.setdefault(block.group, []).append(block.part)
        for at in range(block.first, block.first + block.count):
            positions[at] = len(positions)
            headings.setdefault(block.group, []).append(all_headings[at])
    rebuilt = []
    for at, group in enumerate(groups):
        retained = kept.get(at, [])
        if not retained:
            continue
        offset = int(group.wrapped)
        rebuilt.append(
            replace(
                group,
                parts=tuple(group.parts[i] for i in retained),
                record=replace(
                    group.record,
                    headings=tuple(headings.get(at, [])),
                    parts=tuple(
                        group.record.parts[i - offset] for i in retained if i >= offset
                    ),
                ),
                wrapped=group.wrapped and 0 in retained,
            )
        )
    return rebuilt, removed, positions
