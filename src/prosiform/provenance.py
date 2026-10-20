"""Where the bundle's content came from: source ranges and generated structure.

A reparse that agrees with itself establishes that the candidate parses.
What it cannot establish is that a region came from the source it claims,
or that a region the run selected is missing, because the candidate
carries no record of either. This module is that record, written while
the bundle is constructed and read while it is validated.

Two kinds of record are kept, and they are kept apart. A *range* names a
selected source region by the lines of its source's content it occupies,
which is an identity two regions carrying the same prose do not share: a
sentence repeated in two sections is two ranges, so repeated identical
prose is not duplication and a count of occurrences is not a coverage
test. A *generated* record names a heading the bundle wrote itself — a
filename wrapper, and the structural ancestors a later epic adds — which
carries no source range and so can never stand in for selected body
content a group failed to emit.

A heading the bundle emits is one or the other, never both, and the
record keeps them in emission order. A carried heading holds the source
heading it answers to: the path, the line, the level its author wrote and
the fragment a reference into that document resolved against. That is
what a destination is held to, so a destination reaching a heading whose
slug merely coincides is a disagreement rather than a match.

The record travels with the group it describes. A record held in a
structure beside the groups can be paired with the wrong group; one the
group carries cannot be, and the group's emitted headings are read from
it rather than written twice.
"""

from dataclasses import dataclass

FILENAME_WRAPPER = "filename wrapper"
STRUCTURAL_ANCESTOR = "structural ancestor"


@dataclass(frozen=True)
class Origin:
    """The source heading one emitted heading answers to.

    The level is the level the author wrote, which the group's shift is
    applied to, and the fragment is the slug that author's text
    produces, which is what a reference into the document resolved
    against.
    """

    path: str
    line: int | None
    level: int
    fragment: str


@dataclass(frozen=True)
class Carried:
    """One source heading the bundle emits, and the heading it came from."""

    text: str
    level: int
    origin: Origin


@dataclass(frozen=True)
class Generated:
    """One heading the bundle wrote itself, which answers to no source heading.

    A filename wrapper that absorbed a source heading names that
    heading's fragment, because a reference naming the absorbed title
    resolves to the wrapper's own destination. The wrapper is still
    generated structure: the fragment names what resolves to it, not a
    region of body content it carries.
    """

    text: str
    level: int
    kind: str
    absorbed: str | None = None


Emitted = Carried | Generated


@dataclass(frozen=True)
class Range:
    """One selected source region, as the lines of its source's content it holds.

    The bounds are half-open and in the coordinates of the source's
    content, which is the text the parse read. The removed lines are the
    lines a link-reference definition occupies inside the range, which
    the group drops, so the content the range stands for is the rest.
    """

    path: str
    lines: tuple[int, int]
    removed: tuple[int, ...]

    def kept(self) -> list[int]:
        """Each line of the source the bundle carries, in source order."""
        return [at for at in range(*self.lines) if at not in self.removed]


@dataclass(frozen=True)
class Record:
    """One group's provenance: what it carried, and what it generated.

    The shift is the number of levels the group moved its source
    headings down by, which is zero where the file heading absorbed the
    document's title.
    """

    path: str
    shift: int
    headings: tuple[Emitted, ...]
    ranges: tuple[Range, ...]

    def carried(self) -> list[Carried]:
        """Every source heading the group emits, in emission order."""
        return [one for one in self.headings if isinstance(one, Carried)]
