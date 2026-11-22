"""Recognize operator marks in link text through `opened` and `marked`."""

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
    """One recognized opening: its `marks` and the text offset `after` them."""

    marks: str
    after: int


def opened(text: str) -> Opened | None:
    """The operator marks one link's text opens with, where it states any.

    Symbols are written together and an ASCII space follows the last
    one. Leading spaces and tabs, and spaces and tabs after that required
    space, are padding. A mark followed directly by text or a tab opens
    nothing.
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
