"""Whether the target a run-set link names holds only calls to run concurrently.

A link whose text opens with the run-set operator states that the calls the
section it names holds run concurrently. The target is compiled into the
bundle like any link's, because the agent reads the calls, so what the
operator adds is a claim about the target's shape, and this module reads
whether the target bears it out.

A *run-set* is a section, or a whole document, whose content below its
heading is one bulleted list and nothing else. The list may nest, every
list it holds is bulleted, and every item carries in its own text at least
one link to a Markdown document or section under the root: each item is a
call. A paragraph, a numbered list, a code block, a table, a further
heading or an item linking nothing is material a reader cannot run as a
call, so a target holding one warns, and the bundle is published as it
would be without the check.

The target is read from the source the run already parsed, as the regions
the traversal selected for it, so the check reads nothing itself and
decides warnings alone.
"""

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from markdown_it.token import Token

from prosiform.closure import Reference, identity
from prosiform.diagnostics import WARNING, Diagnostic, Location, RelatedLocation
from prosiform.source import opens

RUN_SET_SHAPE = "W_RUN_SET_SHAPE"

CODES = (RUN_SET_SHAPE,)

REMEDY = (
    "link a section that holds only a bulleted list of calls, or remove the "
    "run-set mark"
)

HEADING_OPEN = "heading_open"
BULLET_LIST_OPEN = "bullet_list_open"
LIST_ITEM_OPEN = "list_item_open"
LIST_ITEM_CLOSE = "list_item_close"
INLINE = "inline"
LINK_OPEN = "link_open"
HREF = "href"

LISTED = frozenset(
    {
        BULLET_LIST_OPEN,
        "bullet_list_close",
        LIST_ITEM_OPEN,
        LIST_ITEM_CLOSE,
        "paragraph_open",
        "paragraph_close",
        INLINE,
    }
)

NAMED = {
    "paragraph_open": "a paragraph",
    "ordered_list_open": "a numbered list",
    BULLET_LIST_OPEN: "a further bulleted list",
    "fence": "a code block",
    "code_block": "a code block",
    "table_open": "a table",
    HEADING_OPEN: "a heading",
    "blockquote_open": "a block quote",
    "hr": "a thematic break",
    "html_block": "raw HTML",
}

UNLINKED = "a list item that links no Markdown document or section under the root"
EMPTY = "no bulleted list"

Calls = Callable[[str], bool]


@dataclass(frozen=True)
class RunSet:
    """One run-set link: the target it names and where it is written."""

    target: Reference
    opening: str
    location: Location

    @property
    def name(self) -> str:
        """The target as the document and section it names."""
        return identity(self.target)


@dataclass(frozen=True)
class Stray:
    """The first thing a target holds that a run-set does not.

    The line is the line of the target's content the construct opens on,
    and is absent where the target holds nothing to point at.
    """

    held: str
    line: int | None


def stray(
    tokens: Sequence[Token], selected: Sequence[Token], calls: Calls
) -> Stray | None:
    """The first construct that keeps one target from being a run-set.

    The selected regions are the target's: the whole document, or the
    section a fragment roots with its subsections. A heading opening them
    is the target's own and is passed over. A link is a call where the
    target's document resolves it to a Markdown document or section under
    the root, which `calls` answers for each destination.
    """
    spans = list(selected)
    if spans and spans[0].type == HEADING_OPEN:
        spans = spans[1:]
    if not spans:
        return Stray(EMPTY, None)
    listed, *rest = spans
    if listed.type != BULLET_LIST_OPEN:
        return Stray(named(listed), line(listed))
    if rest:
        return Stray(named(rest[0]), line(rest[0]))
    return unlisted(tokens, listed, calls)


def unlisted(tokens: Sequence[Token], listed: Token, calls: Calls) -> Stray | None:
    """The first construct inside one bulleted list that is not a call.

    Each item stands open until it closes, so the text an item carries
    is the text read while it is the innermost item open, and a nested
    item's links are its own.
    """
    start = opens(tokens, listed) or 0
    open_items: list[tuple[Token, bool]] = []
    depth = 0
    for token in tokens[start:]:
        if token.type not in LISTED:
            return Stray(named(token), line(token))
        if token.type == LIST_ITEM_OPEN:
            open_items.append((token, False))
        elif token.type == LIST_ITEM_CLOSE:
            item, linked = open_items.pop()
            if not linked:
                return Stray(UNLINKED, line(item))
        elif token.type == INLINE and open_items and linking(token, calls):
            open_items[-1] = (open_items[-1][0], True)
        depth += token.nesting
        if depth == 0:
            break
    return None


def linking(inline: Token, calls: Calls) -> bool:
    """Whether one run of text carries a link that is a call."""
    return any(
        child.type == LINK_OPEN and calls(str(child.attrGet(HREF) or ""))
        for child in inline.children or []
    )


def named(token: Token) -> str:
    """One construct as a reader names it."""
    return NAMED.get(token.type, f"a {token.type.removesuffix('_open')} block")


def line(token: Token) -> int | None:
    """The line of the target's content one construct opens on."""
    return None if token.map is None else token.map[0] + 1


def misshapen(link: RunSet, found: Stray, at: int | None) -> Diagnostic:
    """One warning naming a run-set link whose target is no run-set.

    The place the stray construct is written, where it has one, is
    carried as a related location in the target's document.
    """
    return Diagnostic(
        WARNING,
        f"the run-set link {link.opening!r} names {link.name!r}, which is no "
        f"run-set: it holds {found.held}, where a run-set holds only one "
        f"bulleted list of calls",
        code=RUN_SET_SHAPE,
        reference=link.target.original,
        resolved=link.name,
        chain=link.target.chain,
        remedy=REMEDY,
        location=link.location,
        related=None
        if at is None
        else (RelatedLocation(link.target.path, at, 1, f"holds {found.held}"),),
    )
