"""The complete preset names a decoded comma-separated list supplies.

A link's title, a diagram link's tooltip title and an entry's pick each
supply a decoded string. Tokens are complete names, trimmed and
case-folded, with empty tokens and repetition discarded. The set gives
their order no meaning. Matching names to a destination's declarations
and applying the implicit default belong to the consumer.

The pick token `?` is one of the tokens and names no preset: it leaves
the pick among a destination's alternatives to the agent that compiles
it, and no preset may be named for it, so it selects none.
"""

PICK = "?"


def read(text: str | None) -> frozenset[str]:
    """Normalize a list whose literal commas separate complete preset names."""
    if text is None:
        return frozenset()
    return frozenset(
        name.casefold() for part in text.split(",") if (name := part.strip())
    )


def picks(tags: frozenset[str]) -> bool:
    """Whether a list leaves the pick among alternatives to the agent."""
    return PICK in tags
