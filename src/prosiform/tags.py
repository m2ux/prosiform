"""The complete preset names a decoded comma-separated list supplies.

A Markdown link title and a command argument each supply a decoded string.
Tokens are complete names, trimmed and case-folded, with empty tokens and
repetition discarded. The set gives their order no meaning. Matching names
to a destination's declarations and applying the implicit default belong
to the consumer.
"""


def read(text: str | None) -> frozenset[str]:
    """Normalize a list whose literal commas separate complete preset names."""
    if text is None:
        return frozenset()
    return frozenset(
        name.casefold() for part in text.split(",") if (name := part.strip())
    )
