"""Title case: the one spelling every heading the bundle generates carries.

A name is read as words and the separators between them. A separator is
a hyphen, an underscore, a slash or whitespace, and a word is a run of
anything else. Title case capitalizes the first letter of each word and
keeps every separator where the name wrote it, so a hyphenated name
keeps its hyphens and a nested path keeps its slashes. The convention
changes letters, not structure.

A name made of separators alone carries no word, so its title case names
nothing a reader can tell from another such name.
"""

import re

WORD = re.compile(r"[^-_/\s]+")


def title_cased(text: str) -> str:
    """One generated heading in title case: each word capitalized, the rest kept."""
    return WORD.sub(lambda word: word.group()[:1].upper() + word.group()[1:], text)


def worded(text: str) -> bool:
    """Whether a name carries a word for its title case to name."""
    return WORD.search(text) is not None
