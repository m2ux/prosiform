"""Construct file groups, rewrite selected source lines, and assemble bundle text.

Each group carries its emitted parts and provenance together. `group` builds
a file group; `grouping.merged` supplies merged groups. `assemble` joins the
groups into the candidate that `candidate.validate` checks before publication.
"""

import json
import re
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import PurePosixPath

from markdown_it.token import Token

from prosiform.closure import (
    DECLARING,
    UNSUBSTITUTED,
    WORKING_FOLDER,
    Briefs,
    BundleFolder,
    BundleSelection,
    Declarations,
    Levels,
    Reference,
    Substitution,
    Unmapped,
    Unresolvable,
    briefing,
    bundle_selection,
    bundled,
    carried_names,
    directive,
    dispatched,
    filed,
    model_of,
    parallel,
    picking,
    published_text,
    rebased,
    resolvable,
    unmarked,
    withholding_target,
)
from prosiform.heading import title_cased
from prosiform.metadata import Conversion
from prosiform.profile import SUFFIXES, command_block
from prosiform.provenance import (
    FILENAME_WRAPPER,
    Ancestor,
    Carried,
    Dispatching,
    Emitted,
    Generated,
    Instruction,
    Located,
    Origin,
    Part,
    Placing,
    Range,
    Record,
    Served,
    Target,
    click_at,
    link_at,
)
from prosiform.rewrite import Definition, Followed, Titled, destinations, rewritten
from prosiform.source import (
    ANCHOR,
    FENCE,
    HREF,
    LINE_FEED,
    LINK_CLOSE,
    LINK_OPEN,
    QUOTE,
    TEXT,
    Click,
    Selection,
    bare,
    clicks,
    diagram_type,
    element_texts,
    events,
    headings,
    inlines,
    label_span,
    level,
    lines,
    opening_markers,
    opening_text,
    regions,
    shown,
    slug,
    visible,
    within,
)
from prosiform.tags import read as read_tags

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

RUN_PF = "Run `pf`, then follow the guidance it prints."
MODEL_LEAD = "on"
MODEL_COMMENT = "%%"
"""What opens the Mermaid comment line naming a diagram dispatch's model."""
"""What stands between a published dispatch and the model its sub-agent starts on."""

OPENERS = "\\`*_[]<>&~!#"
OPENER = re.compile(f"([{re.escape(OPENERS)}])")

ATX_MARKER = re.compile(r"^([^#]*)(#{1,6})")
TOOLTIP = re.compile(r'"\s+"[^"]*"')
"""The tooltip suffix span following a `source.Click` destination."""
CLOSING_SEQUENCE = re.compile(r"(^|[ \t])(#+)([ \t]*)$")


class Overflow(Exception):
    """A heading the group's shift would place beyond the sixth level."""

    def __init__(self, heading: str, level: int, path: str) -> None:
        super().__init__(f"the heading {heading!r} would be emitted at level {level}")
        self.heading = heading
        self.level = level
        self.path = path


class Unplaced(Exception):
    """A heading directive that cannot be placed, with its source location.

    `path` and `line` locate the heading; `destination` and `opening` identify
    its link, and `composing` distinguishes composition from dispatch.
    """

    def __init__(
        self,
        path: str,
        line: int | None,
        destination: str,
        opening: str,
        composing: bool,
    ) -> None:
        super().__init__(
            f"the link {opening!r} in {path!r} names {destination!r} and no "
            f"section holds it"
        )
        self.path = path
        self.line = line
        self.destination = destination
        self.opening = opening
        self.composing = composing


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
    """Emitted group data and its provenance.

    `parts` holds the Markdown parts; `record` holds their source and heading
    records. `wrapped` identifies a group with a generated opening, and `level`
    is the opening heading's level.
    """

    parts: tuple[str, ...]
    record: Record
    wrapped: bool = True
    level: int = 1

    @property
    def filed(self) -> bool:
        """Whether the group carries the file heading the bundle writes for it."""
        return any(
            isinstance(one, Generated) and one.kind == FILENAME_WRAPPER
            for one in self.record.headings
        )

    @property
    def text(self) -> str:
        """The group's Markdown, with the separation `joined` supplies."""
        return joined(self.parts)

    @property
    def headings(self) -> tuple[str, ...]:
        """The visible text of each heading the group emits, in bundle order."""
        return tuple(one.text for one in self.record.headings)

    @property
    def targets(self) -> tuple[tuple[Target, ...], ...]:
        """The targets each emitted heading resolves, in bundle order."""
        return tuple(one.answers for one in self.record.headings)


def heading_text(path: str) -> str:
    """A path-derived file heading without its Markdown suffix.

    `path` is relative to the invocation working directory. Suffix recognition
    uses `profile.SUFFIXES`; spelling follows `heading.title_cased`.
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


def started_on(model: str | None, *, visible: bool = False) -> str:
    """The text a published dispatch line or link carries after its link.

    It names the model the dispatch's sub-agent starts on, and is empty
    where its target has no level. It is written as Markdown, or, where
    `visible`, as the text a reader reads.
    """
    if model is None:
        return ""
    return f" {MODEL_LEAD} {model if visible else escaped(model)}"


def is_atx(token: Token) -> bool:
    """Whether a heading is written with the heading syntax a shift edits."""
    return token.markup.startswith(ATX)


def pointing(
    target: Reference,
    opening: str,
    dispatched_to: Mapping[Served, str] | None,
    alone: bool = False,
    lifted: bool = False,
) -> bool:
    """Whether a withheld link points at a bundle file the dispatch map names.

    A link carrying the pick token points at its dispatch-pick
    sub-section. Any other dispatched link does where the map gives its
    target a file, and a link the map says nothing of points at a file
    for a `⇉` link and at its set's sub-section for a `⫽` one, so a
    sub-section a brief lifts it into is one the map names. Where there
    is no map, `lifted` states that the link carries a brief, which
    points it at the sub-section it is lifted into, a `⇉` link carrying
    none points at a file, and `alone` states that a `⫽` link's set holds
    one target, which is published as a dispatch to its file.
    """
    if picking(opening, target.tags):
        return False
    together = parallel(opening)
    if dispatched_to is None:
        return not lifted and (alone or not together)
    given = dispatched_to.get(((target.path, target.fragment), target.tags, together))
    if given is None:
        return not together
    return filed(given)


def sole_set(
    path: str,
    tokens: Sequence[Token],
    heading: Token,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    *,
    conversions: Mapping[str, Conversion],
) -> bool:
    """Whether a heading's own section names one distinct parallel target.

    Only content before the next document-level heading belongs to that set.
    Target resolution uses `closure.withholding_target`; effective identity
    follows `closure.bundle_selection`.
    """
    targets: set[BundleSelection] = set()
    counting = False
    for region in regions(tokens):
        if region.type == HEADING_OPEN:
            if counting:
                break
            counting = region is heading
        if not counting:
            continue
        for inline in inlines(tokens, [region]):
            for children, at, child in events(inline.children or []):
                if child.type != LINK_OPEN:
                    continue
                opening = opening_text(children, at)
                if not parallel(opening):
                    continue
                found = withholding_target(
                    path,
                    str(child.attrGet(HREF) or ""),
                    opening,
                    declarations,
                    substitution,
                    tags=read_tags(str(child.attrGet("title") or "")),
                )
                if found is not None:
                    # An unselected heading can name an uncaptured target.
                    # Its labels establish no published single-selection set.
                    if found.path not in conversions:
                        return False
                    targets.add(bundle_selection(found, conversions[found.path]))
    return len(targets) == 1


def briefs(target: Reference, conversions: Mapping[str, Conversion] | None) -> bool:
    """Whether the target's presets select a brief through `closure.briefing`.

    An invalid brief selection returns false here; traversal reports its error.
    """
    if conversions is None or target.path not in conversions:
        return False
    try:
        return briefing(target, conversions[target.path]) is not None
    except (Briefs, Unresolvable):
        return False


def emitted_visible(
    path: str,
    inline: Token,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    dispatched_to: Mapping[Served, str] | None = None,
    alone: bool = False,
    conversions: Mapping[str, Conversion] | None = None,
) -> str:
    """The visible text one inline token publishes after link rewriting.

    For each resolved use, apply `closure.published_text` and the model suffix
    from `started_on`. `pointing` determines whether a dispatch names a file,
    using `sole_set` or the supplied dispatch map. `briefs` supplies the brief
    classification when conversions are available.

    The lookup uses unrecorded substitutions because it can inspect unselected
    headings; selected reference rewriting records uses at their positions.
    """
    substitution = substitution.unrecorded()
    children = inline.children or []
    carried: list[str] = []
    following = ""
    for at, child in enumerate(children):
        before = children[at - 1] if at else None
        if child.type == LINK_CLOSE and following:
            carried.extend((shown(child), following))
            following = ""
            continue
        if child.type == TEXT and before is not None and before.type == LINK_OPEN:
            target = withholding_target(
                path,
                str(before.attrGet(HREF) or ""),
                child.content,
                declarations,
                substitution,
                tags=read_tags(str(before.attrGet("title") or "")),
            )
            if target is not None:
                file = pointing(
                    target,
                    child.content,
                    dispatched_to,
                    alone,
                    briefs(target, conversions),
                )
                shown_label = published_text(child.content, file)
                model = None
                if (
                    file
                    and dispatched(child.content)
                    and conversions is not None
                    and target.path in conversions
                ):
                    try:
                        model = model_of(target, conversions[target.path])
                    except (Levels, Unmapped):
                        pass
                following = started_on(model, visible=True)
            elif directive(child.content):
                shown_label = unmarked(child.content)
            else:
                shown_label = child.content
            carried.append(shown_label)
            continue
        carried.append(shown(child))
    return "".join(carried)


def shown_text(
    path: str,
    tokens: Sequence[Token],
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    *,
    conversions: Mapping[str, Conversion],
) -> dict[int, str]:
    """Each heading's `emitted_visible` text, keyed by its token identity.

    `sole_set` supplies the section-local parallel selection for each heading.
    """
    return {
        id(opening): emitted_visible(
            path,
            inline,
            declarations,
            substitution,
            alone=sole_set(
                path,
                tokens,
                opening,
                declarations,
                substitution,
                conversions=conversions,
            ),
            conversions=conversions,
        )
        for opening, inline in headings(tokens)
    }


def source_fragments(tokens: Sequence[Token]) -> dict[int, str]:
    """Each heading's authored `source.slug`, keyed by its token identity.

    The authored text is required here because `emitted_visible` can change the
    text the bundle publishes without changing the source target's identity.
    """
    return {id(opening): slug(visible(inline)) for opening, inline in headings(tokens)}


def rewrite(
    physical: Sequence[str],
    tokens: Sequence[Token],
    selected: Sequence[Token],
    assigned: dict[tuple[str, str | None], str],
    path: str,
    defined: Mapping[str, Definition],
    declarations: Declarations = DECLARING,
    dispatching: Dispatching | None = None,
    first_line: int = 1,
    substitution: Substitution = UNSUBSTITUTED,
    composing: Mapping[Located, str] | None = None,
    placing: Placing = (),
    *,
    conversions: Mapping[str, Conversion] | None = None,
    folder: BundleFolder = WORKING_FOLDER,
) -> list[str]:
    """The source's physical lines after rewriting selected references.

    Inline edits use `rewrite.rewritten`; diagram uses follow `source.Click`,
    with destination edits from `clicked` and label edits from `diagram_labels`.
    Unselected content is left alone. Each result entry corresponds to its
    original physical line, including when the replacement contains line feeds.

    Dispatch destinations come from the region's dispatch map; a missing entry
    raises `Unplaced`. Composition destinations come from the link-position map,
    and `unplaced` checks an emitted heading whose contribution is absent.
    Deferred destinations use `closure.rebased` and titles use
    `closure.deferred_title`.
    """
    written = list(physical)
    served = {} if dispatching is None else dispatching
    contributing = {} if composing is None else composing
    titles = {id(inline) for _, inline in headings(tokens)}
    for region in selected:
        here = served.get((path, (region.map or (0, 0))[0], placing), {})
        for inline in inlines(tokens, [region]):
            found = destinations(inline)
            if inline.map is None or (
                not found and not defined and not command_block(inline.children or [])
            ):
                continue
            start, end = inline.map
            if composing is not None and id(inline) in titles:
                unplaced(
                    path,
                    inline,
                    start,
                    contributing,
                    declarations,
                    first_line,
                    substitution,
                )
            targets = [
                f"{ANCHOR}{contributing[link_at(path, inline, start, at)]}"
                if link_at(path, inline, start, at) in contributing
                else target(
                    path,
                    one,
                    opening,
                    assigned,
                    declarations,
                    dispatched_to=here,
                    line=start + first_line,
                    substitution=substitution,
                    tags=tags,
                    conversions=conversions,
                    folder=folder,
                )
                for at, (one, opening, tags) in enumerate(found)
            ]
            written[start:end] = rewritten(written[start:end], inline, targets, defined)
    for region in selected:
        here = served.get((path, (region.map or (0, 0))[0], placing), {})
        for fence in within(tokens, [region]):
            if fence.type != FENCE:
                continue
            held = lines(fence.content)
            first = 0 if fence.map is None else fence.map[0] + 1
            prepared: list[tuple[Click, str | Titled | Followed]] = []
            local: set[str] = set()
            for click in clicks(fence):
                located = click_at(path, click)
                given = (
                    f"{click.anchor}{contributing[located]}"
                    if located in contributing
                    else target(
                        path,
                        click.destination,
                        click.opening,
                        assigned,
                        declarations,
                        click.anchor,
                        dispatched_to=here,
                        line=click.line - 1 + first_line,
                        substitution=substitution,
                        tags=read_tags(click.title),
                        conversions=conversions,
                        folder=folder,
                    )
                )
                if given is not None:
                    prepared.append((click, given))
                    if (
                        dispatched(click.opening)
                        and isinstance(given, str)
                        and not filed(given)
                    ):
                        local.add(click.node)
            changed, edits = diagram_labels(fence, local)
            for line in edits:
                physical = written[first + line]
                prefix = physical[: len(bare(physical)) - len(bare(held[line]))]
                written[first + line] = (
                    prefix + bare(changed[line]) + terminator(physical)
                )
            held = changed
            for click, given in prepared:
                at = click.line - 1
                shift = sum(
                    len(replacement) - len(original)
                    for offset, original, replacement in edits.get(at - first, [])
                    if offset + len(original) <= click.offset
                )
                adjusted = replace(click, offset=click.offset + shift)
                written[at] = clicked(written[at], held[at - first], adjusted, given)
    return written


def diagram_labels(
    fence: Token, local: Collection[str]
) -> tuple[list[str], dict[int, list[tuple[int, str, str]]]]:
    """Unmark diagram labels whose nodes navigate to local dispatch sections.

    Labels come from `source.element_texts`; `source.Click` owns diagram-use
    interpretation. `source.label_span` supplies each edit's original offset
    and spelling, and `closure.unmarked` supplies its text. Metadata label
    values use a quoted JSON scalar,
    which YAML reads as the same string. Other source bytes and content
    line counts are preserved, so click offsets shift by edits before them.
    """
    held = lines(fence.content)
    edits: dict[int, list[tuple[int, str, str]]] = {}
    for line, label in element_texts(fence.content, diagram_type(fence.content)):
        if label.node not in local or not dispatched(label.text):
            continue
        offset, original = label_span(label)
        text = unmarked(label.text)
        replacement = json.dumps(text, ensure_ascii=False) if label.scalar else text
        edits.setdefault(line, []).append((offset, original, replacement))
    for line, changes in edits.items():
        text = bare(held[line])
        for offset, original, replacement in sorted(changes, reverse=True):
            assert text[offset : offset + len(original)] == original
            text = text[:offset] + replacement + text[offset + len(original) :]
        held[line] = text + terminator(held[line])
    return held, edits


def unplaced(
    path: str,
    inline: Token,
    start: int,
    contributing: Mapping[Located, str],
    declarations: Declarations,
    first_line: int,
    substitution: Substitution,
) -> None:
    """Reject a heading directive that has no recorded contribution.

    Identify directives through `closure.directive` and link positions
    through `provenance.link_at`. Reject a target accepted by
    `closure.resolvable` when its position has no contribution.
    """
    position = 0
    for children, at, child in events(inline.children or []):
        if child.type != LINK_OPEN:
            continue
        here = position
        position += 1
        opening = opening_text(children, at)
        if link_at(path, inline, start, here) in contributing:
            continue
        if not directive(opening_text(children, at)):
            continue
        destination = str(child.attrGet(HREF) or "")
        found = resolvable(path, destination, declarations, substitution)
        if found is None or found.fragment is None:
            continue
        raise Unplaced(path, start + first_line, destination, opening, composing=True)


def model_comment(node: str, model: str) -> str:
    """A Mermaid comment naming the node and its dispatch model.

    The model occupies its own comment line because `source.Click` has no
    model field in the diagram-link syntax.
    """
    return f"{MODEL_COMMENT} {node} {MODEL_LEAD} {model}"


def names_model(line: str, click: Click) -> bool:
    """Whether one fence line is the comment `model_comment` writes for a click."""
    return line.strip().startswith(f"{MODEL_COMMENT} {click.node} {MODEL_LEAD} ")


def clicked(
    physical: str, held: str, click: Click, given: str | Titled | Followed
) -> str:
    """One physical source line with a `source.Click` destination replaced.

    Locate the destination from the line's end: the parsed fence omits
    container markers and normalizes its line endings. For `rewrite.Titled`,
    extend the existing tooltip with `rewrite.gained`, or append a new tooltip.
    For `rewrite.Followed`, append the line `model_comment` supplies beneath it.
    """
    after = len(bare(held)) - click.offset - len(click.written)
    end = len(bare(physical)) - after
    rest = physical[end:]
    if isinstance(given, Titled):
        names = ", ".join(given.names)
        tip = TOOLTIP.match(rest)
        if tip is None:
            rest = f'{QUOTE} "{names}"{rest[len(QUOTE) :]}'
        else:
            close = tip.end() - 1
            separator = ", " if click.title else ""
            rest = f"{rest[:close]}{separator}{names}{rest[close:]}"
        given = given.destination
    if isinstance(given, Followed):
        # The comment opens with the markers and indent the link's line
        # opens with, so it stays inside the fence and its container.
        line = bare(physical)
        lead = line[: len(line) - len(bare(held).lstrip())]
        terminator = physical[len(line) :]
        rest = f"{rest}{lead}{model_comment(click.node, given.model)}{terminator}"
        given = given.destination
    return f"{physical[: end - len(click.written)]}{given}{rest}"


def target(
    path: str,
    destination: str,
    opening: str,
    assigned: Mapping[tuple[str, str | None], str],
    declarations: Declarations = DECLARING,
    anchor: str = ANCHOR,
    dispatched_to: Mapping[Served, str] | None = None,
    line: int | None = None,
    substitution: Substitution = UNSUBSTITUTED,
    *,
    tags: frozenset[str] = frozenset(),
    conversions: Mapping[str, Conversion] | None = None,
    folder: BundleFolder = WORKING_FOLDER,
) -> str | Titled | Followed | None:
    """The published destination for a source use, or none for an uncompiled use.

    Resolve the use through `closure.bundled` or `closure.withholding_target`.
    A selected target takes its
    assigned anchor; diagram anchor spelling comes from `source.Click`.
    Deferred paths and title extensions use `closure.rebased` and
    `closure.deferred_title`. Dispatch destinations come from the region's
    dispatch map, with `closure.model_of` supplying their model suffix.
    A resolved dispatch missing from that map raises `Unplaced`.
    """
    found = bundled(path, destination, opening, declarations, substitution)
    if found is not None:
        return f"{anchor}{assigned[(found.path, found.fragment)]}"
    withheld = withholding_target(
        path, destination, opening, declarations, substitution, tags=tags
    )
    if withheld is None:
        return None
    if dispatched(opening):
        held = {} if dispatched_to is None else dispatched_to
        served = ((withheld.path, withheld.fragment), withheld.tags, parallel(opening))
        if served not in held:
            raise Unplaced(path, line, destination, opening, composing=False)
        model = (
            model_of(withheld, conversions[withheld.path])
            if filed(held[served])
            and conversions is not None
            and withheld.path in conversions
            else None
        )
        if model is None:
            return held[served]
        return Followed(held[served], started_on(model), model)
    names = carried_names(withheld, conversions)
    published = rebased(withheld, destination, folder)
    return Titled(published, names) if names else published


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


def file_heading(
    path: str,
    tokens: Sequence[Token],
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    *,
    conversions: Mapping[str, Conversion],
) -> str:
    """The file heading from `document_title`, or `heading_text` when absent.

    An authored title uses `emitted_visible` and `single_line` for publication.
    """
    titled = document_title(tokens)
    if titled is None:
        return heading_text(path)
    return single_line(
        shown_text(path, tokens, declarations, substitution, conversions=conversions)[
            id(titled)
        ]
    )


def absorbed(tokens: Sequence[Token], name: str) -> Token | None:
    """The document's title, where it slugs to what a name slugs to.

    Recognize the title through `document_title` and compare its
    `source.slug` with the supplied name's slug.
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
    """One Setext heading emitted at the supplied ATX depth.

    Join its content lines with spaces, preserve the opening container markers,
    and protect its closing text with `literal_closing`.
    """
    written = [
        bare(line)[len(opening_markers(line)) :].strip() for line in carried[:-1]
    ]
    text = literal_closing(SPACE.join(written))
    return f"{opening_markers(carried[0])}{ATX * depth} {text}"


def line_of(token: Token, first_line: int = 1) -> int:
    """The line of the file one token opens on."""
    return first_line if token.map is None else token.map[0] + first_line


def placing_in(tokens: Sequence[Token], token: Token) -> tuple[str, str, bool] | None:
    """A heading's dispatch or composition link, with its classification.

    Read the authored inline tokens because a literal heading copy has no live
    link. Operator recognition uses `closure.dispatched` and `closure.directive`.
    """
    if token.type != HEADING_OPEN:
        return None
    for opening, inline in headings(tokens):
        if opening is not token:
            continue
        for children, at, child in events(inline.children or []):
            if child.type != LINK_OPEN:
                continue
            destination = str(child.attrGet(HREF) or "")
            opened = opening_text(children, at)
            if directive(opening_text(children, at)):
                return destination, opened, True
            if dispatched(opened):
                return destination, opened, False
    return None


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

    `source.regions` supplies the eligible regions. Each heading closes
    every open heading of its level or deeper and then stands open
    itself; the headings open above a region form its ancestor chain.

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
    declarations: Declarations = DECLARING,
    situate: bool = False,
    dispatching: Dispatching | None = None,
    first_line: int = 1,
    substitution: Substitution = UNSUBSTITUTED,
    composing: Mapping[Located, str] | None = None,
    *,
    conversions: Mapping[str, Conversion],
    folder: BundleFolder = WORKING_FOLDER,
) -> Group:
    """Build one file group and its provenance from a source selection.

    `selected=None` contributes every document-level region. `file_heading`
    names the group; an emitted `document_title` is absorbed when it supplies
    that heading. The parent's situated title opens its own content directly.
    Other content shifts down one level, with overflow reported as `Overflow`.

    `required` identifies unselected ancestor headings. Emit those as literal
    headings alongside selected regions, walking the source once to preserve
    order. `region` supplies each selected part, with reference-definition lines
    from `rewrite.definitions` excluded. `rewrite` supplies link edits when the
    destination map is available; heading records supply the targets needed to
    build that map. `first_line` locates errors in the original file. A title
    emitted literally has no live directive destination and raises `Unplaced`.
    """
    situate = situate and carries_title(tokens) and selected is None
    text = shown_text(path, tokens, declarations, substitution, conversions=conversions)
    titled = document_title(tokens)
    title = file_heading(
        path, tokens, declarations, substitution, conversions=conversions
    )
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
    if absorbing is None and not situate and titled is not None:
        held = placing_in(tokens, titled)
        if held is not None:
            raise Unplaced(path, line_of(titled, first_line), *held)
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
            physical,
            tokens,
            chosen,
            assigned,
            path,
            environment,
            declarations,
            dispatching,
            first_line,
            substitution,
            composing,
            conversions=conversions,
            folder=folder,
        )
    )
    for token in regions(tokens):
        if id(token) in needed:
            held = placing_in(tokens, token)
            if held is not None:
                raise Unplaced(path, line_of(token, first_line), *held)
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
        opening = (
            titled
            if titled is not None
            else next(
                token
                for token in regions(tokens)
                if token.type == HEADING_OPEN and level(token) == 1
            )
        )
        target: Target = (path, named[id(opening)])
        at = next(
            index
            for index, heading in enumerate(emitting_headings)
            if target in heading.answers
        )
        heading = emitting_headings[at]
        emitting_headings[at] = replace(
            heading, answers=(*heading.answers, (path, None))
        )
    return Group(
        tuple(emitted),
        Record(path, None, tuple(emitting_headings), tuple(recorded)),
        wrapped=not situate,
    )


def instruction_group(next_heading: str | None = None) -> Group:
    """The group every bundle opens with: the `§ Instructions` heading and the line.

    It answers to no source document, so its record names a path no source
    holds and carries no selected range. The heading is generated structure,
    and the line is an instruction beneath it. `next_heading` is the title of
    the first heading the bundle carries, which the line names so a reader
    holding the line has somewhere to go.
    """
    line = RUN_PF
    if next_heading is not None:
        line = f"{RUN_PF} Follow [{next_heading}](#{slug(next_heading)}) next."
    heading = Generated(INSTRUCTIONS, 1, FILENAME_WRAPPER)
    record = Record(INSTRUCTIONS, None, (heading,), (Instruction(line),))
    return Group((f"# {INSTRUCTIONS}", line), record)


def assemble(groups: Sequence[Group]) -> str:
    """Join every group's parts using `joined` for their separation."""
    return joined([part for one in groups for part in one.parts])


INSTRUCTIONS = "\u00a7 Instructions"
"""The opening heading text used by `instruction_group`."""


def opened(groups: Sequence[Group]) -> list[Group]:
    """Prepend the group `instruction_group` supplies to the content groups.

    Pass the first published heading to that constructor as the next destination.
    """
    next_heading = None
    for one in groups:
        for heading in one.headings:
            if heading and not heading.startswith("\u2afd"):
                next_heading = heading
                break
        if next_heading is not None:
            break
    return [instruction_group(next_heading), *groups]


def openings(groups: Sequence[Group]) -> list[int]:
    """The opening line of each emitted part under `joined` separation."""
    at = 0
    found: list[int] = []
    for one in groups:
        for part in one.parts:
            found.append(at)
            at += len(lines(part)) + 1
    return found
