"""The link one command-line entry publishes, read as an authored link is read.

An agent compiles a link it meets in a bundle by running `pf` on the
link as the bundle publishes it: a Markdown link, a Mermaid `click`
line or a class diagram `link` line. Each is read by the reader that
reads it in a source, so its destination and its title tags arrive as
they would from an authored link, a Markdown escape decoded and a
tooltip's opening marks set aside.

Operator marks direct the agent reading the bundle, which has acted on
them before it runs `pf`, and the run that compiled the link's source
checked them. The entry therefore reads no operator: the marks opening
a link's text or a tooltip are never read, whatever they combine to.

Any other text is a plain path, the bootstrap entry a document names
to start its own run, which carries no title.
"""

import re
from dataclasses import dataclass

from prosiform.marks import tooltip
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

MARKDOWN_LINK = re.compile(r"\s*\[.*\]\(.*\)\s*", re.DOTALL)


@dataclass(frozen=True)
class Link:
    """The destination one published link names and the tags its title states."""

    destination: str
    tags: frozenset[str]


class NotOneLink(ValueError):
    """A text written as a link that does not read as exactly one link."""


def markdown_link(text: str) -> Link | None:
    """The one Markdown link a text holds and nothing else, where it holds one.

    A text nested past the parser's ceiling reads as no link.
    """
    try:
        tokens = parse(text)
    except Suppressed:
        return None
    inline = [token for token in tokens if token.type == "inline"]
    if len(inline) != 1 or len(tokens) != 3:
        return None
    children = inline[0].children or []
    if not children or children[0].type != LINK_OPEN or children[-1].type != LINK_CLOSE:
        return None
    found = [use for use in uses(tokens, tokens) if not use.resource]
    if len(found) != 1 or sum(child.type == LINK_OPEN for child in children) != 1:
        return None
    return Link(found[0].destination, found[0].tags)


def diagram_link(text: str) -> Link | None:
    """The one `click` or class diagram `link` statement a line holds."""
    found = linked(text, CLASS_DIAGRAM)
    if len(found) != 1:
        return None
    destination, _, _, _, written, _, _ = found[0]
    return Link(destination, read_tags(tooltip(written).title))


def published(text: str) -> Link | None:
    """The link one entry argument publishes, or none for a plain path.

    A text written as a Markdown link or a diagram link line that does
    not read as exactly one is refused, since no plain path is spelled
    that way.
    """
    if MARKDOWN_LINK.fullmatch(text):
        link = markdown_link(text)
        if link is None:
            raise NotOneLink("is written as a Markdown link but is not one link")
        return link
    if QUOTE in text and (CLICK_STATEMENT.match(text) or CLASS_STATEMENT.match(text)):
        link = diagram_link(text)
        if link is None:
            raise NotOneLink(
                "is written as a diagram link line but names not one destination"
            )
        return link
    return None
