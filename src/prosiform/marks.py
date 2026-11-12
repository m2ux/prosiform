"""The operator marks a link opens with, read from its text or a diagram link's tooltip.

Four operators open a link's text, their marks written together and
followed by a space. A mark followed directly by text is the author's
text and opens nothing. What each operator states is the closure
module's to say.

A Mermaid `click` line and a class diagram `link` line may carry a
quoted tooltip after their destination, which states the diagram
link's operator and title. Marks opening the tooltip, followed by a
blank or by the tooltip's end, are its operator, so a tooltip may be
all marks: the node it is drawn on names the link to its reader. The
rest of the tooltip, or the whole of it where no mark opens it, is the
link's title, read as a Markdown link's title is.
"""

from dataclasses import dataclass

DEFERRAL_MARK = "¬"
DISPATCH_MARK = "⇉"
PARALLEL_MARK = "⫽"
INLINE_MARK = "↳"

OPERATORS = (DEFERRAL_MARK, DISPATCH_MARK, PARALLEL_MARK, INLINE_MARK)

SPACE = " "
BLANKS = " \t"


@dataclass(frozen=True)
class Opened:
    """The operator marks one link's text opens with, and where its text begins.

    The marks are followed by a blank, and the text after the blanks
    begins at `after`.
    """

    marks: str
    after: int


def opened(text: str) -> Opened | None:
    """The operator marks one link's text opens with, where it states any.

    Symbols are written together and one blank separates the last of
    them from the link's text, so an operator is a run of marks followed
    by a blank, the blanks before the run being its spacing. A mark
    followed directly by text is the author's text, and opens nothing.
    """
    at = 0
    while at < len(text) and text[at] in BLANKS:
        at += 1
    end = at
    while end < len(text) and text[end] in OPERATORS:
        end += 1
    if end == at or text[end : end + 1] != SPACE:
        return None
    after = end
    while after < len(text) and text[after] in BLANKS:
        after += 1
    return Opened(text[at:end], after)


@dataclass(frozen=True)
class Tooltip:
    """What one diagram link's tooltip states: its opening and its title.

    The opening is the text the operator readers read, as they read the
    text a Markdown link opens with: the tooltip itself where marks open
    it, a blank closing it where the marks end the tooltip, and nothing
    where no mark opens it. The title is what the tooltip leaves once
    the marks and the blanks after them are set aside, read as a link's
    title; a diagram link carrying no tooltip has none.
    """

    opening: str = ""
    title: str | None = None


def tooltip(written: str | None) -> Tooltip:
    """The opening and title one diagram link's tooltip states."""
    if written is None:
        return Tooltip()
    closed = written if opened(written) is not None else written + SPACE
    found = opened(closed)
    if found is None:
        return Tooltip("", written)
    return Tooltip(closed, closed[found.after :])
