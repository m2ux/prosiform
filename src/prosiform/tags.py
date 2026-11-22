"""Read preset-name lists with `read` and identify agent picks with `picks`."""

PICK = "?"


def read(text: str | None) -> frozenset[str]:
    """Normalize a decoded list of complete preset names.

    Literal commas separate names; whitespace is trimmed, case is folded,
    and empty names and repetitions are discarded. The resulting set has
    no selection order.
    """
    if text is None:
        return frozenset()
    return frozenset(
        name.casefold() for part in text.split(",") if (name := part.strip())
    )


def picks(tags: frozenset[str]) -> bool:
    """Whether a normalized list contains the agent-pick token `PICK`.

    The token requests a choice among alternatives rather than a named preset.
    """
    return PICK in tags
