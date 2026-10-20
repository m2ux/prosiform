"""Where the bundle's content came from: source ranges and generated structure.

A reparse that agrees with itself establishes that the candidate parses.
What it cannot establish is that a region came from the source it claims,
or that a region the run selected is missing, because the candidate
carries no record of either. This module is that record, written while
the bundle is constructed and read while it is validated.

Three kinds of record are kept, and they are kept apart. A *range* names
a selected source region by the lines of its source's content it
occupies, which is an identity two regions carrying the same prose do not
share: a sentence repeated in two sections is two ranges, so repeated
identical prose is not duplication and a count of occurrences is not a
coverage test. A *generated* record names a heading the bundle wrote
itself — the filename wrapper — which carries no source range and so can
never stand in for selected body content a group failed to emit. A
*structural ancestor* names a heading the bundle emits to place a
selected section in the outline its author gave it: it answers to a
source heading, as a carried heading does, and carries no source range,
as a generated heading does, which is why it is neither of them.

A heading the bundle emits is exactly one of the three, and the record
keeps them in emission order. A heading that answers to a source heading
holds that heading's identity: the path, the line, the level its author
wrote and the fragment a reference into that document resolved against.
That is what a destination is held to, so a destination reaching a
heading whose slug merely coincides is a disagreement rather than a
match. A structural ancestor holds the same identity and is still not a
destination any reference is assigned, because a displayed title is not
the section it names.

The emitted parts of a group are recorded in one sequence as well: the
file heading, then one part for each selected source range and one for
each structural ancestor, in the order the group emits them. A part is
therefore accounted for by a range or by an ancestor and never by
neither, so a candidate holding a region more or a region less than the
sequence names is a disagreement a count reports.

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


@dataclass(frozen=True)
class Ancestor:
    """One heading the bundle emits for an unselected ancestor of selected content.

    The text is the title its author wrote, as a reader reads it, and
    the group emits it as literal text: an ancestor heading is
    structure, so it carries no live link, image or HTML and no
    reference is traversed from it. The level is the source level under
    the group's shift, and the origin is the source heading the text
    came from, which is what the reconstructed outline is held to.

    It is not a target. A reference naming that section expands the
    closure to select it, and the heading the group then emits for it
    is a carried one, so no destination is ever assigned to the
    ancestor record.
    """

    text: str
    level: int
    origin: Origin

    @property
    def kind(self) -> str:
        """What this heading is, named as the record's own vocabulary names it."""
        return STRUCTURAL_ANCESTOR


Emitted = Carried | Generated | Ancestor
Sourced = Carried | Ancestor


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


Part = Range | Ancestor


@dataclass(frozen=True)
class Record:
    """One group's provenance: what it carried, and what it generated.

    The shift is the number of levels the group moved its source
    headings down by, which is zero where the file heading absorbed the
    document's title.

    The parts are what the group emits below its file heading, in
    emission order: a range for each selected source region and an
    ancestor for each heading the group emits to place one of them.
    """

    path: str
    shift: int
    headings: tuple[Emitted, ...]
    parts: tuple[Part, ...]

    @property
    def ranges(self) -> tuple[Range, ...]:
        """Every selected source region the group carries, in emission order."""
        return tuple(one for one in self.parts if isinstance(one, Range))

    def carried(self) -> list[Carried]:
        """Every source heading the group emits, in emission order."""
        return [one for one in self.headings if isinstance(one, Carried)]

    def placed(self) -> list[Sourced]:
        """Every heading the group emits that answers to a source heading.

        A carried heading and a structural ancestor are both placed by
        the source level their author wrote under the group's shift, so
        the checks over that placement read them together.
        """
        return [one for one in self.headings if isinstance(one, Carried | Ancestor)]

    def ancestors(self) -> list[Ancestor]:
        """Every structural ancestor the group emits, in emission order."""
        return [one for one in self.headings if isinstance(one, Ancestor)]
