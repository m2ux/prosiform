"""The bundle: one file group for each contributing source.

A group is a source document unless its conversion metadata names the
merged group that `grouping` assembles. A file group is headed by one
generated H1. Its visible text is the document's title, where the
document carries one: its first heading, where that heading is its only
H1 and sits at the document level. A document carrying no title is
headed by its normalized path relative to the invocation working
directory with the Markdown extension removed, in title case: each word
of the path is capitalized and every separator the path carries is
kept, so the heading names the document the filesystem holds and
carries the one convention every generated heading takes. Either text
is escaped as literal heading text, so punctuation in a title or a
filename names itself rather than opening a link, an image, emphasis,
code, raw HTML, an entity or a strikethrough, or closing the heading
that carries it. Two documents whose file headings coincide are two
headings of one text, which take distinct destinations as any repeated
heading does: the renderer's slug, the later one carrying its ordinal.
A reader tells the two apart only by where each stands, so the run
warns of them.

A group is assembled from the maximal regions the run selected, in
source order, each carried as the bytes its source wrote. A whole
document selects every region it holds; a fragment selects the regions
of the section it names. A section whose eligible ancestors the run did
not select is placed in the outline its author gave it by emitting each
of those ancestors as a heading and nothing else: no body, no unselected
sibling and no other descendant. The ancestor's title is emitted as
literal text, so a link, an image or raw HTML inside it is the
characters its author typed rather than a live construct, and the
dependencies a run traverses are read from the regions it selected, so
nothing is required by an ancestor heading. Each ancestor is emitted
once however many selections stand beneath it, and an ancestor the
closure goes on to select is a selected region like any other, which is
the heading and the body that stand there in its place. What lies
between two
regions is not source content: a blank line above the first region, the
blank line a removed reference definition was separated by, and the
spacing between any two blocks are the bundle's own, and the bundle
writes one blank line between regions wherever it joins them. A group
is held as those parts rather than as the text they join into, so the
line each part opens on is a figure the assembly states and candidate
validation reads back to prove that no part landed inside the one above
it. Inside a
region nothing is touched but the lines a link-reference definition
occupies and the links the bundle rewrites, so an indented thematic
break keeps its indent, a delimiter keeps its trailing spaces and a
code example keeps every byte but a diagram's link destinations. A
terminator belongs to the line it terminates and is content as the rest
of the line is, so a region ends with the newline its source spelled on
the line that ends it, and every heading the bundle generates ends with
the newline the bundle generates.

Each resolved reference-style use in selected content is published
inline, and every original definition node is removed, the definitions
no use names included. A definition a container carries is dropped
where it sits, with the blank line the container separated it by, and
a definition at the document level lies between two regions and is
dropped by the slice that takes them.

The file heading absorbs the document's title, because it carries that
title's text. A group whose title is absorbed keeps its source heading
levels; every other group moves each
emitted heading down one level, the file heading taking the level that
makes room. A heading a retained container carries is shifted where it
sits, so the container keeps the structure it had. A shift that would
place any emitted heading beyond the sixth level is an overflow rather
than a heading, and the group refuses it.

A shift edits an ATX heading's number signs, which are the level the
author wrote. A Setext heading writes its level as an underline instead,
so a shifted group emits it as the ATX heading of the same level,
carrying the inline source its content lines hold joined into the one
line an ATX heading is, each line break reading as the space it already
read as. A group that shifts by nothing has no level to write, so the
heading stays the Setext heading its source wrote.

Each link in selected content that the bundle compiled is rewritten to
the destination of the target it resolved to, through the map the
bundle's own headings produce. A whole-document reference takes the
destination of that file's heading, except the parent — the first entry
document — whose whole-document reference takes the destination of its
first H2, wherever the bundle placed that heading. A fragment takes the
destination of the heading it named, and a fragment-only link resolves
inside its own source first and then takes that heading's destination. A destination
is scoped to the whole bundle, so a reference from one group to another
is spelled as one inside a group is. A mark goes with the rewrite,
because a reader of the bundle has no use for authoring syntax.

A Mermaid diagram's link destination is a link written inside a code
example, and the bundle rewrites it as it rewrites any other: the
destination's characters take the destination its target was given,
and every other byte of the fence is carried as written. The anchor is
spelled as the line's form spells it: a quoted destination opens it
with `#`, and a sequence diagram's menu entry with `#35;`, the entity
Mermaid renders as `#` where a bare one would open a comment. A diagram
link destination the bundle compiled nothing for, such as one outside
the root or one naming no Markdown document, keeps the text its author
wrote.

A destination is the fragment a renderer generates for a bundled
heading: the heading's slug, carrying the ordinal the renderer appends
where an earlier heading already took that slug. The ordinal is assigned
over every heading the bundle emits, in bundle order, a heading a
retained container carries included: the renderer indexes that heading
beside the rest and numbers the headings after it from a count that
holds it, so a map built from the document-level headings alone names
one heading and resolves to another.
"""

import re
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import PurePosixPath

from markdown_it.token import Token

from prosiform.closure import (
    bundled,
    dispatched,
    rebased,
    unmarked,
    withholding_target,
)
from prosiform.profile import SUFFIXES
from prosiform.provenance import (
    FILENAME_WRAPPER,
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
from prosiform.rewrite import Definition, destinations, rewritten
from prosiform.source import (
    ANCHOR,
    FENCE,
    HREF,
    LINE_FEED,
    LINK_OPEN,
    TEXT,
    Click,
    Selection,
    bare,
    clicks,
    headings,
    inlines,
    level,
    lines,
    opening_markers,
    regions,
    shown,
    slug,
    visible,
    within,
)

MAX_LEVEL = 6
SHIFT = 1

HEADING_DEPTH_OVERFLOW = "E_HEADING_DEPTH_OVERFLOW"

CODES = (HEADING_DEPTH_OVERFLOW,)

TERMINATOR = "\n"
SEPARATOR = TERMINATOR
CARRIAGE_RETURN = "\r"
ENDINGS = (f"{CARRIAGE_RETURN}{TERMINATOR}", TERMINATOR, CARRIAGE_RETURN)

ATX = "#"
SPACE = " "
HEADING_OPEN = "heading_open"

OPENERS = "\\`*_[]<>&~!#"
OPENER = re.compile(f"([{re.escape(OPENERS)}])")

WORD = re.compile(r"[^-_/\s]+")

ATX_MARKER = re.compile(r"^([^#]*)(#{1,6})")
CLOSING_SEQUENCE = re.compile(r"(^|[ \t])(#+)([ \t]*)$")


class Overflow(Exception):
    """A heading the group's shift would place beyond the sixth level."""

    def __init__(self, heading: str, level: int, path: str) -> None:
        super().__init__(f"the heading {heading!r} would be emitted at level {level}")
        self.heading = heading
        self.level = level
        self.path = path


def ending(run: str) -> str:
    """The line ending one run of newline characters opens with.

    A run empty of them ends no line, so the newline the bundle
    generates stands in its place.
    """
    for spelling in ENDINGS:
        if run.startswith(spelling):
            return spelling
    return TERMINATOR


def terminated(part: str) -> str:
    """One emitted part with the newline that ends it.

    A region carries the spelling its source wrote on the line that ends
    it, and a part the bundle generates ends with the newline the bundle
    generates.
    """
    return part if part.endswith(ENDINGS) else part + TERMINATOR


def joined(parts: Sequence[str]) -> str:
    """Several emitted parts, one blank line apart, each ending its own line.

    The blank line between two parts is the bundle's own and is spelled
    with the newline the bundle generates, which is why one terminated
    part followed by that newline opens the next part two lines below.
    """
    return SEPARATOR.join(terminated(part) for part in parts)


@dataclass(frozen=True)
class Group:
    """One file group: the Markdown it emits, and the record of where it came from.

    The group is held as the parts it emits — its file heading, then one
    part for each selected source region — rather than as the Markdown
    those parts join into, because the separation between two of them is
    the bundle's own and the bundle states it in one place. A group the
    parent's own title opens has no file heading ahead of those regions.
    The text the group publishes is those parts with one blank line
    between each.

    The headings the group emits and the source fragment each answers to
    are read from that record, so the group states them once. The first
    is the file heading, which answers to the whole document and so to
    no fragment of it. A file heading that absorbed a source heading
    answers to that heading's fragment as well, which is held apart
    because the heading itself is not emitted.

    The order is the path of the first document the group carries in
    placement order, which is where the bundle places the group.
    """

    parts: tuple[str, ...]
    record: Record
    order: str
    wrapped: bool = True

    @property
    def text(self) -> str:
        """The Markdown the group publishes: its parts, one blank line apart."""
        return joined(self.parts)

    @property
    def headings(self) -> tuple[str, ...]:
        """The visible text of each heading the group emits, in bundle order."""
        return tuple(one.text for one in self.record.headings)

    @property
    def targets(self) -> tuple[tuple[Target, ...], ...]:
        """The targets each emitted heading resolves, in bundle order."""
        return tuple(one.answers for one in self.record.headings)


def title_cased(text: str) -> str:
    """One generated heading in title case: each word capitalized, the rest as written.

    A word runs between the separators a name carries, and only its
    first letter is touched, so a nested name keeps its separators and
    a hyphenated name keeps its hyphens. The convention changes
    letters, not structure.
    """
    return WORD.sub(lambda word: word.group()[:1].upper() + word.group()[1:], text)


def heading_text(path: str) -> str:
    """One untitled source's file heading: its path in title case, the suffix gone.

    The path is the one the run read the source by, relative to the
    invocation working directory.

    The suffix is classified case-insensitively, as the profile
    classifies one, and the path the heading spells is the path the
    filesystem holds with each of its words capitalized, so one
    convention covers this heading and every other the bundle
    generates.
    """
    spelled = PurePosixPath(path)
    if spelled.suffix.lower() in SUFFIXES:
        return title_cased(str(spelled.with_suffix("")))
    return title_cased(path)


def escaped(text: str) -> str:
    """One string as literal Markdown text, read as the characters it carries.

    A backslash precedes each character that can begin a construct the
    profile reads: an escape, a code span, emphasis, a link, an angle
    bracket, an entity, a strikethrough and an image marker. It also
    precedes the number sign, which ends one: a heading whose text runs
    to a space and a number sign carries a closing sequence, and a
    renderer takes that sequence off the heading rather than showing it.
    """
    return OPENER.sub(r"\\\1", text)


def is_atx(token: Token) -> bool:
    """Whether a heading is written with the heading syntax a shift edits."""
    return token.markup.startswith(ATX)


def emitted_visible(path: str, inline: Token, root: str = "") -> str:
    """The text one inline token shows once the bundle has rewritten its links.

    A heading can carry a link, and one the run withholds a compilation
    of publishes without its deferral or dispatch mark. What the heading shows is
    therefore what the renderer slugs, so the destination the heading
    takes names the heading a reader finds.

    A link the bundle took no destination for shows the text its author
    wrote. That covers a markup or resource reference under the root and
    a reference leaving the root.
    """
    children = inline.children or []
    carried: list[str] = []
    for at, child in enumerate(children):
        before = children[at - 1] if at else None
        if child.type == TEXT and before is not None and before.type == LINK_OPEN:
            target = withholding_target(
                path, str(before.attrGet(HREF) or ""), child.content, root
            )
            carried.append(
                unmarked(child.content) if target is not None else child.content
            )
            continue
        carried.append(shown(child))
    return "".join(carried)


def shown_text(path: str, tokens: Sequence[Token], root: str = "") -> dict[int, str]:
    """The visible text of each heading token, keyed by the token's identity.

    The text is the one the bundle emits for that heading, which is the
    text its author wrote with a withholding mark taken off, so the
    destination the heading takes names what a reader finds.
    """
    return {
        id(opening): emitted_visible(path, inline, root)
        for opening, inline in headings(tokens)
    }


def source_fragments(tokens: Sequence[Token]) -> dict[int, str]:
    """The source fragment each heading token answers to, keyed by its identity.

    A source fragment is the slug of the text the author wrote, which is
    what a reference into that document resolved against. It is read
    from the authored text and not from the published one, because a
    reference naming this heading carries the fragment the author's text
    produces: a heading whose withholding mark is dropped on emission is
    still reached by the fragment its source spelling slugs to.
    """
    return {id(opening): slug(visible(inline)) for opening, inline in headings(tokens)}


def rewrite(
    physical: Sequence[str],
    tokens: Sequence[Token],
    selected: Sequence[Token],
    assigned: dict[tuple[str, str | None], str],
    path: str,
    defined: Mapping[str, Definition],
    root: str = "",
    dispatching: Mapping[tuple[str, int], Mapping[Target, str]] | None = None,
) -> list[str]:
    """The source's physical lines, as the bundle publishes the selected content.

    A rewrite edits the lines one inline token occupies and reports one
    entry for each of them, so the lines the group then slices are the
    lines the source wrote, one for one, and a token map taken from the
    parse names the same content after the rewrite as before it. A
    definition the author spelled across more than one line is published
    with the line feeds it carries, and the entry for the line that
    gained one holds it.

    Content the run did not select is left alone: no reference in it was
    resolved, so no destination was assigned to one, and a definition it
    names is removed with the rest rather than published around it.

    A source declaring no definition carries no reference-style use, so
    a token holding no link is the text its source wrote.

    A diagram's link destination is replaced in the one line it is
    written on, so the line count holds there too. Several destinations
    on one line are replaced in written order.

    A dispatched link takes the destination of the sub-section its
    region carries for its target, which the dispatch map holds by the
    region's first line.
    """
    written = list(physical)
    served = {} if dispatching is None else dispatching
    for region in selected:
        here = served.get((path, (region.map or (0, 0))[0]), {})
        for inline in inlines(tokens, [region]):
            found = destinations(inline)
            if inline.map is None or (not found and not defined):
                continue
            start, end = inline.map
            targets = [
                target(path, one, opening, assigned, root, dispatched_to=here)
                for one, opening in found
            ]
            written[start:end] = rewritten(written[start:end], inline, targets, defined)
    for fence in within(tokens, selected):
        if fence.type != FENCE:
            continue
        held = lines(fence.content)
        first = 0 if fence.map is None else fence.map[0] + 1
        for click in clicks(fence):
            given = target(path, click.destination, "", assigned, root, click.anchor)
            if given is not None:
                at = click.line - 1
                written[at] = clicked(written[at], held[at - first], click, given)
    return written


def clicked(physical: str, held: str, click: Click, given: str) -> str:
    """One physical line with one diagram link destination replaced.

    The fence holds the line without the container markers and indent
    the document line opens with, so the line the fence holds is the
    trailing text of the physical one. The destination is located from
    the end of the line, which both carry alike, its terminator aside:
    a CRLF the document wrote reaches the fence as a line feed.
    """
    after = len(bare(held)) - click.offset - len(click.written)
    end = len(bare(physical)) - after
    return f"{physical[: end - len(click.written)]}{given}{physical[end:]}"


def target(
    path: str,
    destination: str,
    opening: str,
    assigned: Mapping[tuple[str, str | None], str],
    root: str = "",
    anchor: str = ANCHOR,
    dispatched_to: Mapping[Target, str] | None = None,
) -> str | None:
    """The destination the bundle gave one link, or nothing where it gave none.

    A link the bundle compiled resolves to an identity the map holds,
    because the closure selected what the link named and the group
    emitting it recorded the target it answers to. Its destination is
    that heading's slug behind the anchor spelling the link's form
    writes, `#` wherever the link is not a sequence diagram's menu entry.

    A deferred link under the allowed source root takes its target's
    path from the invocation working directory, so the run that
    compiles it later, from that directory, follows it as written. A
    dispatched one takes the destination of the dispatch sub-section
    its region carries for its target. Neither is rewritten to the
    destination of the target's own heading, even where another
    reference carried its target into the bundle: what one author
    withheld cannot be changed by another author's reference.

    A link resolving outside the allowed source root, and one naming no
    Markdown document, is text the bundle carries and takes no
    destination, whether or not its author marked it.
    """
    found = bundled(path, destination, opening, root)
    if found is not None:
        return f"{anchor}{assigned[(found.path, found.fragment)]}"
    deferred = withholding_target(path, destination, opening, root)
    if deferred is None:
        return None
    if dispatched(opening):
        held = {} if dispatched_to is None else dispatched_to
        return f"{anchor}{held[(deferred.path, deferred.fragment)]}"
    return rebased(deferred, destination)


def carries_title(tokens: Sequence[Token]) -> bool:
    """Whether the document carries an H1 at its own level."""
    return any(
        level(opening) == 1 and any(token is opening for token in regions(tokens))
        for opening, _inline in headings(tokens)
    )


def document_title(tokens: Sequence[Token]) -> Token | None:
    """The document's title: its first heading, where that is its only H1.

    The title sits at the document level, so an H1 a container carries
    titles nothing, and a document carrying a second H1 or opening on a
    deeper heading has no single heading that names it.
    """
    carried = list(headings(tokens))
    if not carried:
        return None
    opening, _inline = carried[0]
    if level(opening) != 1 or sum(1 for one, _ in carried if level(one) == 1) != 1:
        return None
    if not any(token is opening for token in regions(tokens)):
        return None
    return opening


def file_heading(path: str, tokens: Sequence[Token], root: str = "") -> str:
    """The text one document's file group is headed by.

    It is the document's title where the document carries one, as the
    group shows it on one line, and the path the run read the document
    by where it carries none.
    """
    titled = document_title(tokens)
    if titled is None:
        return heading_text(path)
    return single_line(shown_text(path, tokens, root)[id(titled)])


def absorbed(tokens: Sequence[Token], name: str) -> Token | None:
    """The document's title, where it slugs to what a name slugs to.

    Both sides are slugged, so the capitalization and spacing a
    filesystem carries decide nothing and a document at `My Note.md`
    titled `My Note` is named by `my-note` as one at `my-note.md` is.
    """
    opening = document_title(tokens)
    if opening is None:
        return None
    inline = next(one for heading, one in headings(tokens) if heading is opening)
    if slug(visible(inline)) != slug(name):
        return None
    return opening


def shifted(line: str, by: int) -> str:
    """One ATX heading's line, its level moved down by the group's shift.

    The level is written in the first number-sign run the line carries:
    what precedes it is the indent and the container markers the line
    opens with, and no container marker is a number sign.
    """
    return ATX_MARKER.sub(
        lambda written: written.group(1) + ATX * (len(written.group(2)) + by),
        line,
        count=1,
    )


def terminator(line: str) -> str:
    """The line ending one physical line carries, which may be nothing at all."""
    return line[len(bare(line)) :]


def literal_closing(text: str) -> str:
    """One heading's text with a trailing number-sign run kept as text.

    An ATX heading ends at a run of number signs a space precedes, and a
    renderer takes that run off the heading rather than showing it. A
    Setext heading has no closing sequence, so a run ending its text is
    text, and a backslash before the run keeps it the text it was.
    """
    return CLOSING_SEQUENCE.sub(r"\1\\\2\3", text)


def converted(carried: Sequence[str], depth: int) -> str:
    """One Setext heading as the ATX heading of the same level and text.

    A Setext heading writes its level as an underline rather than as a
    prefix, so it is rewritten rather than edited. Its content lines
    carry the inline source the author wrote, and they join into the
    one line an ATX heading is, separated by the space a reader already
    reads in place of each line break. The rewritten line opens with
    the markers the heading opened with, so the container that holds
    the heading holds it still, and a number-sign run ending its text
    is escaped, because an ATX heading ends at one.
    """
    written = [
        bare(line)[len(opening_markers(line)) :].strip() for line in carried[:-1]
    ]
    text = literal_closing(SPACE.join(written))
    return f"{opening_markers(carried[0])}{ATX * depth} {text}"


def carried_headings(tokens: Sequence[Token], token: Token) -> list[Token]:
    """Every heading one region holds, the region's own heading included."""
    start, end = token.map or (0, 0)
    return [
        opening
        for opening, _ in headings(tokens)
        if opening.map is not None and start <= opening.map[0] < end
    ]


def ancestry(tokens: Sequence[Token]) -> dict[int, tuple[Token, ...]]:
    """The chain of eligible ancestor headings above each region, by its identity.

    Only a heading the document carries at its own level roots a
    section, so the chain is read from the document-level regions
    alone: each heading closes every open heading of its level or
    deeper and then stands open itself, and what is open above a region
    is the chain that placed it. A heading a container carries roots
    nothing, and the region holding that container is where the
    document puts its content.

    The chain is the document's own structure rather than the run's, so
    a region is placed the same way whether it was selected on its own
    or inside a larger region that consolidated it.
    """
    chain: list[Token] = []
    found: dict[int, tuple[Token, ...]] = {}
    for token in regions(tokens):
        if token.type != HEADING_OPEN:
            found[id(token)] = tuple(chain)
            continue
        depth = level(token)
        while chain and level(chain[-1]) >= depth:
            chain.pop()
        found[id(token)] = tuple(chain)
        chain.append(token)
    return found


def required(tokens: Sequence[Token], emitting: Collection[int]) -> set[int]:
    """Each ancestor heading the emitted regions need and the run did not select.

    An ancestor the run selected is emitted as the content it is, so it
    is no structural ancestor, and an ancestor several selections share
    is one identity in a set and so is emitted once.
    """
    above = ancestry(tokens)
    needed = {
        id(one)
        for token in regions(tokens)
        if id(token) in emitting
        for one in above[id(token)]
    }
    return needed - set(emitting)


def single_line(text: str) -> str:
    """One heading's title on the one line an ATX heading is.

    A Setext heading carries its title on as many lines as its author
    wrote, and each line break reads as the space it already read as.
    """
    return SPACE.join(part.strip() for part in text.split(LINE_FEED))


def blank(line: str) -> bool:
    """Whether one line carries nothing but the markers the container opens it with."""
    return not bare(line)[len(opening_markers(line)) :].strip()


def region(
    physical: Sequence[str],
    tokens: Sequence[Token],
    token: Token,
    by: int,
    removed: Collection[int] = (),
) -> str:
    """One region as the lines its source occupies, each heading it holds shifted.

    A heading a container carries is shifted where it sits, so the
    container keeps the structure it had, and everything that is not a
    heading is carried as the bytes its source wrote. The headings are
    rewritten last to first, because a Setext heading becomes one line
    where its source wrote several and an earlier heading's lines would
    otherwise move out from under it.

    A line a definition occupies is dropped, and so is the blank line
    a container separated the definition from the content above it by:
    a definition is not content, and the spacing around it is the
    bundle's own wherever it joins what remains. A line marked for
    removal is held as the absence it is rather than as an index, so a
    heading rewritten above it moves it without losing it.

    The region ends at the last line that remains and carries the
    newline that line was terminated with, because a terminator belongs
    to the line it terminates and is content like the rest of it. A last
    line carrying none is ended with the newline the bundle generates,
    there being no spelling to carry.
    """
    start, end = token.map or (0, 0)
    carried: list[str | None] = [
        None if at in removed else line
        for at, line in enumerate(physical[start:end], start=start)
    ]
    dropped = len(carried) - len([line for line in carried if line is not None])
    if by:
        for opening in reversed(carried_headings(tokens, token)):
            at, closing = opening.map or (0, 0)
            if is_atx(opening):
                written = carried[at - start]
                carried[at - start] = None if written is None else shifted(written, by)
            else:
                carried[at - start : closing - start] = [
                    converted(physical[at:closing], level(opening) + by)
                    + terminator(physical[closing - 1])
                ]
    kept = [line for line in carried if line is not None]
    while dropped and kept and blank(kept[-1]):
        kept.pop()
    written = "".join(kept)
    content = written.rstrip(f"{CARRIAGE_RETURN}{TERMINATOR}")
    return content + ending(written[len(content) :])


def emitted_text(token: Token, text: str, by: int) -> str:
    """The visible text the group emits for one heading.

    A Setext heading the group converts carries on one line what its
    source wrote on several, so each line break between them reads as
    the space it already read as.
    """
    if by and not is_atx(token):
        return SPACE.join(part.strip() for part in text.split(LINE_FEED))
    return text


def group(
    path: str,
    tokens: Sequence[Token],
    physical: Sequence[str],
    defined: Mapping[str, Definition] | None = None,
    selected: Selection | None = None,
    assigned: dict[tuple[str, str | None], str] | None = None,
    root: str = "",
    situate: bool = False,
    dispatching: Mapping[tuple[str, int], Mapping[Target, str]] | None = None,
) -> Group:
    """One file group: its generated heading, then the regions the run selected.

    The parent keeps its H1 and the content above its first H2 at the
    levels the author wrote, and a whole-document reference to it
    resolves to that first H2.

    A selection of None is the whole document. A selection of sections
    emits the regions it names and nothing else.

    The file heading carries the document's title where the document
    has one, and the path the run read it by where it has none. A title
    is absorbed only where the group emits it, because the absorption is
    the file heading standing in for a heading the group carries. A
    group that emits none therefore shifts, and a reference to an
    absorbed title resolves to the file heading's own destination. The
    file heading names that title either way, so a selection
    beneath an unemitted one is placed by the file heading and the
    title is no structural ancestor: a second heading carrying the
    document's own name is one a reader cannot tell from the first.

    A destination map rewrites each link the selected content carries
    that the bundle compiled. The map is built from the headings every
    group emits, so it is known only once every group exists: a group
    built without one reports the headings that produce it, and the
    same group built with it carries the links pointing at them. The
    headings a group reports are the same either way, because the
    rewrite edits a destination and a mark and nothing a heading is
    slugged from.

    An eligible ancestor of a selected region that the run did not
    select is emitted above it as a heading alone, carrying the title
    its author wrote as literal text and nothing else. The ancestors
    and the selected regions are emitted in one walk of the document,
    so both stand in the source order their author wrote, and an
    ancestor shared by two selections is emitted once.

    The definition environment is this source's own, which is what its
    reference-style uses resolve against and which no other source
    reaches. Every line a definition occupies is dropped from the
    content the group emits, the lines of a definition no use names
    included, so the bundle carries the uses and none of the
    declarations behind them.
    """
    situate = situate and carries_title(tokens) and selected is None
    text = shown_text(path, tokens, root)
    titled = document_title(tokens)
    title = file_heading(path, tokens, root)
    environment: Mapping[str, Definition] = {} if defined is None else defined
    removed = {
        at for one in environment.values() for at in range(one.lines[0], one.lines[1])
    }
    emitting = (
        {id(token) for token in regions(tokens)}
        if selected is None
        else {id(token) for token in selected.regions}
    )
    absorbing = (
        None
        if situate
        else titled
        if titled is not None and id(titled) in emitting
        else None
    )
    by = 0 if situate or absorbing is not None else SHIFT
    emitted = [] if situate else [f"{ATX} {escaped(title)}"]
    named = source_fragments(tokens)
    emitting_headings: list[Emitted] = []
    recorded: list[Part] = []
    if not situate:
        resolving: list[Target] = [(path, None)]
        if absorbing is not None:
            resolving.append((path, named[id(absorbing)]))
        wrapper = Generated(title, 1, FILENAME_WRAPPER, tuple(resolving))
        emitting_headings.append(wrapper)
    chosen = [token for token in regions(tokens) if id(token) in emitting]
    needed = required(tokens, emitting) - (set() if titled is None else {id(titled)})
    written = (
        list(physical)
        if assigned is None
        else rewrite(
            physical, tokens, chosen, assigned, path, environment, root, dispatching
        )
    )
    for token in regions(tokens):
        if id(token) in needed:
            depth = level(token) + by
            shows = single_line(text[id(token)])
            ancestor = Ancestor(
                shows,
                depth,
                (
                    Origin(
                        path,
                        None if token.map is None else token.map[0] + 1,
                        level(token),
                        named[id(token)],
                        by,
                    ),
                ),
            )
            emitting_headings.append(ancestor)
            recorded.append(ancestor)
            emitted.append(f"{ATX * depth} {escaped(shows)}")
            continue
        if id(token) not in emitting:
            continue
        if token is absorbing:
            continue
        carried = carried_headings(tokens, token)
        for opening in carried:
            depth = level(opening) + by
            if depth > MAX_LEVEL:
                raise Overflow(text[id(opening)], depth, path)
        emitting_headings.extend(
            Carried(
                emitted_text(one, text[id(one)], by),
                level(one) + by,
                (
                    Origin(
                        path,
                        None if one.map is None else one.map[0] + 1,
                        level(one),
                        named[id(one)],
                        by,
                    ),
                ),
                ((path, named[id(one)]),),
            )
            for one in carried
        )
        start, end = token.map or (0, 0)
        recorded.append(
            Range(
                path,
                (start, end),
                tuple(at for at in range(start, end) if at in removed),
            )
        )
        emitted.append(region(written, tokens, token, by, removed))
    if situate:
        roots = {
            token.map[0] + 1
            for token in regions(tokens)
            if token.type == HEADING_OPEN
            and level(token) == 2
            and token.map is not None
        }
        at = next(
            (
                index
                for index, heading in enumerate(emitting_headings)
                if isinstance(heading, Carried)
                and any(
                    origin.path == path and origin.line in roots
                    for origin in heading.origins
                )
            ),
            None,
        )
        if at is None:
            at = next(
                (
                    index
                    for index, heading in enumerate(emitting_headings)
                    if isinstance(heading, Carried)
                    and any(origin.path == path for origin in heading.origins)
                ),
                None,
            )
        if at is not None:
            heading = emitting_headings[at]
            emitting_headings[at] = replace(
                heading, answers=(*heading.answers, (path, None))
            )
    return Group(
        tuple(emitted),
        Record(path, None, tuple(emitting_headings), tuple(recorded)),
        path,
        wrapped=not situate,
    )


def assemble(groups: Sequence[Group]) -> str:
    """The document: every group's parts in bundle order.

    One blank line between two maximal emitted regions is the separation
    the contract requires, and it is written here and nowhere else, so
    the geometry `openings` reads back is the geometry this writes. The
    document opens on the first part of the first group, and each part
    ends with the newline that ends its own last line, so the document
    closes with the one its final part carries.
    """
    return joined([part for one in groups for part in one.parts])


def openings(groups: Sequence[Group]) -> list[int]:
    """The line of the document each emitted part opens on, in order.

    The first part opens the document, and every later part opens one
    blank line below the last line of the part above it.
    """
    at = 0
    found: list[int] = []
    for one in groups:
        for part in one.parts:
            found.append(at)
            at += len(lines(part)) + 1
    return found
