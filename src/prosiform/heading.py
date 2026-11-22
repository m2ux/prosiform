"""Spell generated headings with `title_cased` and detect names with `worded`."""

import re

WORD = re.compile(r"[^-_/\s]+")


def title_cased(text: str) -> str:
    """Capitalize each word's first character while preserving its remaining text.

    Hyphens, underscores, slashes and whitespace separate words and keep
    their original spelling and position.
    """
    return WORD.sub(lambda word: word.group()[:1].upper() + word.group()[1:], text)


def worded(text: str) -> bool:
    """Whether a name carries a word for its title case to name."""
    return WORD.search(text) is not None
