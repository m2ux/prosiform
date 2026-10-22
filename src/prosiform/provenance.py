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
itself — the filename wrapper, and the group, overview and variant
headings a grouping rule produces — which carries no source range and so
can never stand in for selected body content a group failed to emit. A
*structural ancestor* names a heading the bundle emits to place a
selected section in the outline its author gave it: it answers to a
source heading, as a carried heading does, and carries no source range,
as a generated heading does, which is why it is neither of them.

A heading the bundle emits is exactly one of the three, and the record
keeps them in emission order. A heading that answers to a source heading
holds that heading's identity: the path, the line, the level its author
wrote, the fragment a reference into that document resolved against, and
the number of levels the arrangement moves it by. A merged heading
several documents contribute one text to holds one identity for each of
them, because it stands in the outline of every document it was drawn
from.

What a heading resolves is recorded beside it rather than derived from
it. A target is a document and a fragment of it, or a document alone,
and the headings that answer one are the filename wrapper, a carried
heading, a variant heading and the subsection naming a member. A
structural ancestor answers none: a displayed title is not the section it
names, and a reference naming that section expands the closure to select
it, so the heading emitted for it is a carried one.

The emitted parts of a group are recorded in one sequence as well: the
group's own heading, then one part for each selected source range, each
structural ancestor and each heading the arrangement generates, in the
order the group emits them. A part is therefore accounted for by one of
the three and never by none, so a candidate holding a region more or a
region less than the sequence names is a disagreement a count reports.

The record travels with the group it describes. A record held in a
structure beside the groups can be paired with the wrong group; one the
group carries cannot be, and the group's emitted headings are read from
it rather than written twice.
"""

from dataclasses import dataclass, field

FILENAME_WRAPPER = "filename wrapper"
GROUP_HEADING = "group heading"
OVERVIEW_SECTION = "overview section"
MEMBER_OVERVIEW = "member overview"
VARIANT_HEADING = "variant heading"
STRUCTURAL_ANCESTOR = "structural ancestor"

Target = tuple[str, str | None]


@dataclass(frozen=True)
class Origin:
    """The source heading one emitted heading answers to.

    The level is the level the author wrote and the shift is the number
    of levels the arrangement moves it by, so the two together are the
    level the bundle emits it at. The fragment is the slug that author's
    text produces, which is what a reference into the document resolved
    against.
    """

    path: str
    line: int | None
    level: int
    fragment: str
    shift: int


@dataclass(frozen=True)
class Carried:
    """One source heading the bundle emits, and the headings it came from.

    A heading one document contributes holds one origin. A merged
    heading several documents contribute one text to holds one origin
    for each of them, and is emitted once for all of them.
    """

    text: str
    level: int
    origins: tuple[Origin, ...]
    answers: tuple[Target, ...] = ()


@dataclass(frozen=True)
class Generated:
    """One heading the bundle wrote itself, which answers to no source heading.

    A filename wrapper that absorbed a source heading answers to that
    heading's fragment as well as to the document, because a reference
    naming the absorbed title resolves to the wrapper's own destination.
    The subsection naming a member answers the same way under a
    grouping rule, and a variant heading answers to the heading of the document
    it names. The heading is still generated structure: what it answers
    names what resolves to it, not a region of body content it carries.
    """

    text: str
    level: int
    kind: str
    answers: tuple[Target, ...] = ()


@dataclass(frozen=True)
class Ancestor:
    """One heading the bundle emits for an unselected ancestor of selected content.

    The text is the title its author wrote, as a reader reads it, and
    the group emits it as literal text: an ancestor heading is
    structure, so it carries no live link, image or HTML and no
    reference is traversed from it. The origins are the source headings
    the text came from, which is what the reconstructed outline is held
    to, and a merged group draws one from each document that wrote the
    text at the grouping depth.

    It is not a target, and it answers nothing. A reference naming that
    section expands the closure to select it, and the heading the group
    then emits for it is a carried one.
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


Part = Range | Ancestor | Generated


@dataclass(frozen=True)
class Record:
    """One group's provenance: what it carried, and what it generated.

    The path is the group's identity: a source document for a file
    group, and the directory slug for a merged one. The depth is the
    source heading level a grouping rule merges its members at, and is
    nothing for a file group, so the record states which of the two
    arrangements produced it.

    The parts are what the group emits below its own heading, in
    emission order: a range for each selected source region, an
    ancestor for each heading the group emits to place one of them, and
    a generated heading for each one the arrangement adds.
    """

    path: str
    merged: int | None
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
        the source level their author wrote under the shift the
        arrangement gives them, so the checks over that placement read
        them together.
        """
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
