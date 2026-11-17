"""The operator marks a link opens with, read from its text.

Four operators open a link's text, their marks written together and
followed by a space. A mark followed directly by text is the author's
text and opens nothing. What each operator states is the closure
module's to say.

A diagram link's text is the text of the diagram element its `click`
or class diagram `link` line names, so the marks opening that text
state the diagram link's operator as they state a Markdown link's.
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


def marked(text: str) -> bool:
    """Whether one text states operator marks: marks alone, or marks opening it."""
    held = text.strip(BLANKS)
    if held and all(one in OPERATORS or one in BLANKS for one in held):
        return True
    return opened(text) is not None
