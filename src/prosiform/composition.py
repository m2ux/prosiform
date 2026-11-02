"""Composition: the links that request it, and the sections they place.

A composition directive is a link whose label, read as plain text with
its entities decoded, is exactly one Unicode scalar above U+007F that
shows something: a whitespace, control or format scalar shows nothing,
so a reader could not see the placement it would request. The label
requests placement and nothing else, so every qualifying scalar means
the same and the meaning an author gives one stays with the author.

Deferral is read before recognition and apart from it: the deferral
mark and the blanks after it are set aside, so a deferred link is a
deferred directive where what remains qualifies and an ordinary
deferral where it does not. Every other operator opens a link that is
no directive, and the marks that open an operator or a convention are
no directive's label. Nothing is trimmed or normalised to make a label
qualify.

An immediate directive naming a section of a document the bundle
compiles *composes* it. The section containing the directive is its
*scope*, at the heading the bundle emits for it. When the scope's own
content ends, each title its directives' targets carry takes a
*destination section* one level below the scope, in the order its
first directive is written, so directives in one scope naming sections
of one title share one destination and sibling scopes each carry their
own. Beneath it, each directive takes a *contribution*: a heading one
level further down naming the target's immediate parent, then the
target's body and subsections as the regions its source wrote, each
heading moved so the target's own level becomes the contribution
heading's. The directive's link points at its contribution heading.

A contribution is its source's content: its regions are rewritten
against the document that wrote them, so its links resolve from that
document's directory, its fragments against that document's headings
and its reference-style uses against that document's definitions,
whatever the writing document defines. Every directive contributes, a
repeated one and one naming a section another directive or an
ordinary link names included, each in the scope that writes it.

Composition runs on the built groups ahead of the dispatch pass, which
reads what a destination section carries as the scope's own content:
a scope's dispatch sub-sections follow its destination sections, and
its child sections follow both.

A target with no heading above it names no parent and is refused, and
a composed heading past the sixth level is the overflow it is.
"""

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, replace
from unicodedata import category

from markdown_it.token import Token

from prosiform.bundle import (
    ATX,
    HEADING_OPEN,
    MAX_LEVEL,
    Group,
    Overflow,
    ancestry,
    carried_headings,
    emitted_text,
    escaped,
    region,
    rewrite,
    shown_text,
    single_line,
    source_fragments,
)
from prosiform.closure import (
    DECLARING,
    DEFERRAL_MARK,
    DISPATCH_MARK,
    PARALLEL_MARK,
    UNSUBSTITUTED,
    Declarations,
    Reference,
    Substitution,
    bundled,
    operators,
    unmarked,
)
from prosiform.dispatch import region_of
from prosiform.provenance import (
    CONTRIBUTION_HEADING,
    DESTINATION_SECTION,
    Ancestor,
    Carried,
    Emitted,
    Generated,
    Located,
    Origin,
    Part,
    Range,
    Served,
)
from prosiform.rewrite import Definition
from prosiform.source import (
    HREF,
    LINK_OPEN,
    Source,
    events,
    inlines,
    level,
    lines,
    opening_text,
    plain_label,
    section,
)

INLINE_MARK = "↳"

# The marks that open an operator or a convention, which no label
# requests placement with.
MARKS = (DEFERRAL_MARK, DISPATCH_MARK, PARALLEL_MARK, INLINE_MARK)

ASCII_CEILING = 0x7F

# The general categories of a scalar that shows nothing: a control and a
# format character. Whitespace is read from the scalar's own property.
UNSHOWN = ("Cc", "Cf")


def directive(label: str | None) -> bool:
    """Whether a link with this plain-text label is a composition directive.

    The label is absent where the link's text is not plain text, which
    no directive's is. A label opening with the deferral mark alone is
    read without it; one opening with any other operator states how its
    material is compiled and requests no placement.
    """
    if label is None:
        return False
    found = operators(label)
    if found and found != (DEFERRAL_MARK,):
        return False
    requested = unmarked(label) if found else label
    return (
        len(requested) == 1
        and ord(requested) > ASCII_CEILING
        and requested not in MARKS
        and not requested.isspace()
        and category(requested) not in UNSHOWN
    )


Composed = dict[Located, Generated]
"""Each composing link's contribution heading, by the link's position."""


class Parentless(Exception):
    """A directive whose target has no heading above it to name a parent by."""

    def __init__(self, path: str, line: int | None, destination: str) -> None:
        super().__init__(
            f"the directive {destination!r} in {path!r} names a section no "
            f"heading stands above"
        )
        self.path = path
        self.line = line
        self.destination = destination


@dataclass(frozen=True)
class Directive:
    """One composing link: the section it names and where it is written.

    The title is the target heading's visible text, which decides the
    destination section the directive shares with others in its scope.
    """

    target: Reference
    written: str
    line: int | None
    at: Located
    title: str


class Composing:
    """The bundle's groups rebuilt with the sections their directives compose.

    Without a destination map the composed regions carry the bytes
    their source wrote, as an unmapped group's do; with one, their
    links are rewritten through it, against the source they were
    written in.
    """

    def __init__(
        self,
        parsed: Mapping[str, Sequence[Token]],
        read: Mapping[str, Source],
        defined: Mapping[str, Mapping[str, Definition]],
        assigned: Mapping[tuple[str, str | None], str] | None = None,
        dispatching: Mapping[tuple[str, int], Mapping[Served, str]] | None = None,
        declarations: Declarations = DECLARING,
        substitution: Substitution = UNSUBSTITUTED,
    ) -> None:
        self.parsed = parsed
        self.read = read
        self.defined = defined
        self.assigned = assigned
        self.dispatching = dispatching
        self.declarations = declarations
        self.substitution = substitution
        self.placed: Composed = {}
        self.emitted: list[str] = []
        self.parts: list[Part] = []
        self.headings: list[Emitted] = []
        self.pending: dict[str, list[Directive]] = {}
        self.level: int | None = None

    def directives(self, path: str, token: Token) -> Iterator[Directive]:
        """Every composing link one region writes, in written order."""
        tokens = self.parsed[path]
        for inline in inlines(tokens, [token]):
            if inline.map is None:
                continue
            line = self.read[path].line(inline.map[0] + 1)
            position = 0
            for children, at, child in events(inline.children or []):
                if child.type != LINK_OPEN:
                    continue
                here = position
                position += 1
                if not directive(plain_label(children, at)):
                    continue
                written = str(child.attrGet(HREF) or "")
                found = bundled(
                    path,
                    written,
                    opening_text(children, at),
                    self.declarations,
                    self.substitution,
                )
                if found is None or found.fragment is None:
                    continue
                named = self.parsed[found.path]
                chosen = section(named, found.fragment)
                if not chosen:
                    continue
                shows = shown_text(
                    found.path, named, self.declarations, self.substitution
                )
                yield Directive(
                    found,
                    written,
                    line,
                    (path, inline.map[0], here),
                    single_line(shows[id(chosen[0])]),
                )

    def heading(self, one: Generated) -> None:
        """Emit one generated heading of a composition."""
        self.emitted.append(f"{ATX * one.level} {escaped(one.text)}")
        self.parts.append(one)
        self.headings.append(one)

    def contribute(self, one: Directive, depth: int) -> None:
        """Emit one directive's contribution at the depth its heading takes."""
        path = one.target.path
        tokens = self.parsed[path]
        chosen = section(tokens, one.target.fragment or "") or ()
        opening = chosen[0]
        chain = ancestry(tokens)[id(opening)]
        if not chain:
            raise Parentless(one.at[0], one.line, one.written)
        shows = shown_text(path, tokens, self.declarations, self.substitution)
        contribution = Generated(
            single_line(shows[id(chain[-1])]), depth, CONTRIBUTION_HEADING
        )
        if depth > MAX_LEVEL:
            raise Overflow(contribution.text, depth, path)
        self.placed.setdefault(one.at, contribution)
        self.heading(contribution)
        body = list(chosen[1:])
        by = depth - level(opening)
        source = self.read[path]
        defined = self.defined[path]
        removed = {at for held in defined.values() for at in range(*held.lines)}
        physical = lines(source.text)
        written = (
            list(physical)
            if self.assigned is None
            else rewrite(
                physical,
                tokens,
                body,
                dict(self.assigned),
                path,
                defined,
                self.declarations,
                self.dispatching,
                source.first_line,
                self.substitution,
            )
        )
        named = source_fragments(tokens)
        for token in body:
            carried = carried_headings(tokens, token)
            for held in carried:
                if level(held) + by > MAX_LEVEL:
                    raise Overflow(shows[id(held)], level(held) + by, path)
            self.headings.extend(
                Carried(
                    emitted_text(held, shows[id(held)], by),
                    level(held) + by,
                    (
                        Origin(
                            path,
                            None if held.map is None else held.map[0] + 1,
                            level(held),
                            named[id(held)],
                            by,
                        ),
                    ),
                    composed=True,
                )
                for held in carried
            )
            start, end = token.map or (0, 0)
            self.parts.append(
                Range(
                    path,
                    (start, end),
                    tuple(at for at in range(start, end) if at in removed),
                    composed=True,
                )
            )
            self.emitted.append(region(written, tokens, token, by, removed))

    def flush(self) -> None:
        """Emit the destination sections the section just closed composes."""
        if self.level is None or not self.pending:
            self.pending = {}
            return
        depth = self.level + 1
        for title, found in self.pending.items():
            if depth > MAX_LEVEL:
                raise Overflow(title, depth, found[0].target.path)
            self.heading(Generated(title, depth, DESTINATION_SECTION))
            for one in found:
                self.contribute(one, depth + 1)
        self.pending = {}

    def group(self, one: Group) -> Group:
        """One group with the sections its directives compose."""
        offset = 1 if one.wrapped else 0
        self.emitted = list(one.parts[:offset])
        self.parts = []
        self.headings = list(one.record.headings[:offset])
        self.level = one.record.headings[0].level if one.wrapped else None
        at = offset
        for part, text in zip(one.record.parts, one.parts[offset:], strict=True):
            if isinstance(part, Ancestor | Generated):
                self.flush()
                self.level = part.level
                self.headings.append(one.record.headings[at])
                at += 1
            elif isinstance(part, Range):
                tokens = self.parsed[part.path]
                token = region_of(tokens, part)
                held = len(carried_headings(tokens, token))
                if token.type == HEADING_OPEN:
                    self.flush()
                    self.level = one.record.headings[at].level
                self.headings.extend(one.record.headings[at : at + held])
                at += held
                if not part.composed:
                    for found in self.directives(part.path, token):
                        self.pending.setdefault(found.title, []).append(found)
            self.emitted.append(text)
            self.parts.append(part)
        self.flush()
        return Group(
            tuple(self.emitted),
            replace(one.record, headings=tuple(self.headings), parts=tuple(self.parts)),
            wrapped=one.wrapped,
            level=one.level,
        )


def compositions(
    groups: Sequence[Group],
    parsed: Mapping[str, Sequence[Token]],
    read: Mapping[str, Source],
    defined: Mapping[str, Mapping[str, Definition]],
    assigned: Mapping[tuple[str, str | None], str] | None = None,
    dispatching: Mapping[tuple[str, int], Mapping[Served, str]] | None = None,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> tuple[list[Group], Composed]:
    """Every group with the sections its directives compose, and each contribution.

    The contributions are the headings each composing link points at,
    held by the link's position, so the destinations they take are read
    once every heading of the bundle is known.
    """
    composing = Composing(
        parsed, read, defined, assigned, dispatching, declarations, substitution
    )
    return [composing.group(one) for one in groups], composing.placed


def contributions(
    placed: Composed, headed: Sequence[Group], assigned: Sequence[str]
) -> dict[Located, str]:
    """The destination each composing link takes: its contribution heading's."""
    position = {
        id(heading): at
        for at, heading in enumerate(
            heading for one in headed for heading in one.record.headings
        )
    }
    return {link: assigned[position[id(heading)]] for link, heading in placed.items()}
