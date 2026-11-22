"""Records linking emitted bundle parts and headings to their source data.

Constructors retain source coordinates, generated structure and target
answers. `Record` exposes those records to emission and validation callers.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field

from markdown_it.token import Token

from prosiform.profile import COLUMN
from prosiform.source import Click

FILENAME_WRAPPER = "filename wrapper"
GROUP_HEADING = "group heading"
OVERVIEW_SECTION = "overview section"
MEMBER_OVERVIEW = "member overview"
PREAMBLE_HEADING = "preamble subsection"
VARIANT_HEADING = "variant heading"
STRUCTURAL_ANCESTOR = "structural ancestor"
INSTRUCTION = "instruction"
PARALLEL_SECTION = "dispatch-set sub-section"
PICK_SECTION = "dispatch-pick sub-section"
BRIEF_SECTION = "dispatch-brief sub-section"
DESTINATION_SECTION = "destination section"
CONTRIBUTION_HEADING = "contribution heading"

COMPOSED_HEADINGS = (DESTINATION_SECTION, CONTRIBUTION_HEADING)

Target = tuple[str, str | None]

Served = tuple[Target, frozenset[str], bool]
"""A dispatched occurrence's destination, requested tags and parallel operator."""

Located = tuple[str, int, int, int]
"""A link identity: source path, content line, column and occurrence position.

`link_at` constructs inline identities; `click_at` constructs diagram
identities from `source.Click`.
"""


def link_at(path: str, inline: Token, start: int, position: int) -> Located:
    """One link's identity, from the inline block it is written in."""
    return (path, start, inline.meta.get(COLUMN, 0), position)


def click_at(path: str, click: Click) -> Located:
    """One `source.Click` identity from its path, content line and offset."""
    return (path, click.line - 1, 0, click.offset)


Placing = tuple[Located, ...]
"""A region's composing-link identities in outermost-first order."""

Contributing = dict[Placing, dict[Located, str]]
"""Each composing link's destination, by the placing of the region it is in."""

Region = tuple[str, int, Placing]
"""One copy of a source region: its document, the first line of content it
opens on, and the placing of the composition that placed the copy, none for
an authored region."""

Dispatching = Mapping[Region, Mapping[Served, str]]
"""The destination each copy of a region gives the dispatched links it writes."""


@dataclass(frozen=True)
class Origin:
    """The source coordinates and shift of an emitted heading.

    `path` names its document; `line` locates its source heading when present.
    `level` is its source level, `fragment` its source fragment, and `shift`
    its arranged level offset.
    """

    path: str
    line: int | None
    level: int
    fragment: str
    shift: int


@dataclass(frozen=True)
class Carried:
    """A carried heading and the source headings recorded for it.

    `text` and `level` describe the emitted heading; `origins` holds its source
    coordinates. `answers` holds its target identities, and `composed` identifies
    a heading inside a composition copy.
    """

    text: str
    level: int
    origins: tuple[Origin, ...]
    answers: tuple[Target, ...] = ()
    composed: bool = False


@dataclass(frozen=True)
class Generated:
    """A generated heading's text, level, kind and target answers."""

    text: str
    level: int
    kind: str
    answers: tuple[Target, ...] = ()


@dataclass(frozen=True)
class Ancestor:
    """An ancestor heading's text, level and source origins.

    `answers` holds the empty target tuple; `kind` identifies its record type.
    """

    text: str
    level: int
    origins: tuple[Origin, ...]
    answers: tuple[Target, ...] = field(default=(), init=False)

    @property
    def kind(self) -> str:
        """What this heading is, named as the record's own vocabulary names it."""
        return STRUCTURAL_ANCESTOR


Emitted = Carried | Generated | Ancestor
Sourced = Carried | Ancestor


@dataclass(frozen=True)
class Range:
    """A recorded source region and its composition context.

    `path` names the document; `lines` holds its half-open content-line bounds,
    and `removed` its excluded line indices. `placing` identifies the directive
    chain. `selecting` holds its preset tags, or is absent for a group's own
    selection.
    """

    path: str
    lines: tuple[int, int]
    removed: tuple[int, ...]
    placing: Placing = ()
    selecting: frozenset[str] | None = None

    @property
    def composed(self) -> bool:
        """Whether a directive's composition placed this range."""
        return bool(self.placing)

    def kept(self) -> list[int]:
        """Each line of the source the bundle carries, in source order."""
        return [at for at in range(*self.lines) if at not in self.removed]


@dataclass(frozen=True)
class Instruction:
    """Generated block data with no source range.

    `text` holds the block; `listed` identifies a dispatch-list entry.
    `activates` holds a deferred composition target and tags when present.
    """

    text: str
    listed: bool = False
    activates: tuple[Target, frozenset[str]] | None = None

    @property
    def kind(self) -> str:
        """What this part is, named as the record's own vocabulary names it."""
        return INSTRUCTION


@dataclass(frozen=True)
class Preamble(Range):
    """A source preamble grouped beside a partial section selection."""


Part = Range | Ancestor | Generated | Instruction


@dataclass(frozen=True)
class Record:
    """One group's identity, arrangement and emitted provenance.

    `path` names the source or declared group. `merged` holds its grouping
    depth, or is absent for a file group. `headings` and `parts` hold their
    records in emission order.
    """

    path: str
    merged: int | None
    headings: tuple[Emitted, ...]
    parts: tuple[Part, ...]

    @property
    def preamble(self) -> bool:
        """Whether this group arranges source context beside partial selections."""
        return False

    @property
    def ranges(self) -> tuple[Range, ...]:
        """Every selected source region the group carries, in emission order."""
        return tuple(one for one in self.parts if isinstance(one, Range))

    def carried(self) -> list[Carried]:
        """Every source heading the group emits, in emission order."""
        return [one for one in self.headings if isinstance(one, Carried)]

    def placed(self) -> list[Sourced]:
        """Carried and ancestor heading records, in emission order."""
        return [one for one in self.headings if isinstance(one, Carried | Ancestor)]

    def ancestors(self) -> list[Ancestor]:
        """Every structural ancestor the group emits, in emission order."""
        return [one for one in self.headings if isinstance(one, Ancestor)]

    def paths(self) -> list[str]:
        """Every source the group carries content or structure from, in order."""
        found: list[str] = []
        for one in self.parts:
            held = (
                one.path
                if isinstance(one, Range)
                else one.origins[0].path
                if isinstance(one, Ancestor)
                else None
            )
            if held is not None and held not in found:
                found.append(held)
        for each in self.placed():
            for origin in each.origins:
                if origin.path not in found:
                    found.append(origin.path)
        return found


@dataclass(frozen=True)
class PreambleRecord(Record):
    """The provenance of preambles arranged beneath their parent folder."""

    @property
    def preamble(self) -> bool:
        return True
