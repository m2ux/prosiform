"""Recognise the links that request composition.

A composition directive is a link whose label, read as plain text with
its entities decoded, is exactly one Unicode scalar above U+007F. The
label requests placement and nothing else, so every qualifying scalar
means the same and the meaning an author gives one stays with the
author.

Deferral is read before recognition and apart from it: the deferral
mark and the blanks after it are set aside, so a deferred link is a
deferred directive where what remains qualifies and an ordinary
deferral where it does not. Every other operator opens a link that is
no directive, and the marks that open an operator or a convention are
no directive's label. Nothing is trimmed or normalised to make a label
qualify.
"""

from prosiform.closure import (
    DEFERRAL_MARK,
    DISPATCH_MARK,
    PARALLEL_MARK,
    operators,
    unmarked,
)

INLINE_MARK = "↳"

# The marks that open an operator or a convention, which no label
# requests placement with.
MARKS = (DEFERRAL_MARK, DISPATCH_MARK, PARALLEL_MARK, INLINE_MARK)

ASCII_CEILING = 0x7F


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
    )
