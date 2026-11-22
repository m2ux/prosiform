"""Read one published link from a command-line entry argument.

`markdown_link` uses `source.uses`, `diagram_link` uses the reader
behind `source.Click`, and `published` distinguishes links from paths.
"""

import re
from dataclasses import dataclass

from prosiform.profile import Suppressed, parse
from prosiform.source import (
    CLASS_DIAGRAM,
    CLASS_STATEMENT,
    CLICK_STATEMENT,
    LINK_CLOSE,
    LINK_OPEN,
    QUOTE,
    linked,
    uses,
)
from prosiform.tags import read as read_tags

MARKDOWN_LINK = re.compile(r"\[.*\]\(", re.DOTALL)


@dataclass(frozen=True)
class Link:
    """The destination one published link names and the tags its title states."""

    destination: str
    tags: frozenset[str]


class NotOneLink(ValueError):
    """A text written as a link that does not read as exactly one link."""


def markdown_link(text: str) -> Link | None:
    """Read exactly one standalone Markdown link, or return none.

    The parse must hold one paragraph containing that link alone.
    `profile.parse` owns parsing and suppression; `source.uses` supplies
    the destination and preset tags.
    """
    try:
        tokens = parse(text.strip())
    except Suppressed:
        return None
    inline = [token for token in tokens if token.type == "inline"]
    if len(inline) != 1 or len(tokens) != 3 or tokens[0].type != "paragraph_open":
        return None
    children = inline[0].children or []
    if not children or children[0].type != LINK_OPEN or children[-1].type != LINK_CLOSE:
        return None
    found = [use for use in uses(tokens, tokens) if not use.resource]
    if len(found) != 1:
        return None
    return Link(found[0].destination, found[0].tags)


def diagram_link(text: str) -> Link | None:
    """Read one diagram statement using the reader behind `source.Click`.

    Exactly one result from `source.linked` supplies the destination;
    `tags.read` supplies the preset names from its title.
    """
    found = linked(text, CLASS_DIAGRAM)
    if len(found) != 1:
        return None
    destination, _, _, _, written, _, _ = found[0]
    return Link(destination, read_tags(written))


def published(text: str) -> Link | None:
    """Read an entry argument as one published link or return none for a path.

    Markdown-link syntax must satisfy `markdown_link`; a quoted diagram
    statement must satisfy `diagram_link`. A recognized form yielding no
    single link raises `NotOneLink`.
    """
    if MARKDOWN_LINK.search(text):
        link = markdown_link(text)
        if link is None:
            raise NotOneLink("holds a Markdown link but is not one link alone")
        return link
    if QUOTE in text and (CLICK_STATEMENT.match(text) or CLASS_STATEMENT.match(text)):
        link = diagram_link(text)
        if link is None:
            raise NotOneLink(
                "is written as a diagram link line but names not one destination"
            )
        return link
    return None
