"""Assert the dispatch analysis follows chains as deep as the limit and refuses a cycle.

Each graph here is a mapping from a target to the targets its bundle
dispatches, standing in for the bundles a run compiles, so a case states
the shape of the dispatches and what that shape raises.
"""

from collections.abc import Mapping, Sequence

import pytest

from prosiform.closure import Reference
from prosiform.diagnostics import ERROR, Location
from prosiform.dispatch import (
    DISPATCH_CYCLE,
    DISPATCH_DEPTH,
    Hop,
    Onward,
    Refused,
    analysed,
    cycle,
)


def hop(name: str, written: str) -> Hop:
    """One dispatch of a document, written in another."""
    return Hop(Reference(name, name, chain=("entry.md", name)), Location(written, 1, 1))


def graph(edges: Mapping[str, Sequence[str]]) -> Onward:
    """The dispatches each target's bundle carries, under the edges given."""

    def onward(target: Reference) -> Sequence[Hop]:
        return [hop(name, target.path) for name in edges.get(target.path, ())]

    return onward


def first(edges: Mapping[str, Sequence[str]]) -> list[Hop]:
    """The entry's own dispatches."""
    return [hop(name, "entry.md") for name in edges.get("entry.md", ())]


def codes(edges: Mapping[str, Sequence[str]]) -> list[str]:
    """The warning codes the analysis raises for the entry's dispatches."""
    found = analysed(first(edges), {"entry.md"}, graph(edges))
    return [one.code for one in found]


def refused(edges: Mapping[str, Sequence[str]]) -> list[str] | None:
    """The chain the cycle refusal names, or nothing where none is refused."""
    try:
        cycle(first(edges), {"entry.md"}, graph(edges))
    except Refused as refusal:
        assert refusal.diagnostic.code == DISPATCH_CYCLE
        assert refusal.diagnostic.severity == ERROR
        return list(refusal.diagnostic.chain or ())
    return None


def test_a_chain_of_exactly_the_limit_raises_nothing() -> None:
    edges = {"entry.md": ["a"], "a": ["b"], "b": ["c"]}
    assert codes(edges) == []
    assert refused(edges) is None


def test_a_chain_past_the_limit_warns() -> None:
    assert codes({"entry.md": ["a"], "a": ["b"], "b": ["c"], "c": ["d"]}) == [
        DISPATCH_DEPTH
    ]


def test_a_cycle_longer_than_the_limit_is_refused() -> None:
    edges = {"entry.md": ["a"], "a": ["b"], "b": ["c"], "c": ["d"], "d": ["a"]}
    assert refused(edges) == ["entry.md", "a", "b", "c", "d", "a"]


def test_a_dispatch_of_the_entry_is_refused() -> None:
    assert refused({"entry.md": ["a"], "a": ["entry.md"]}) == [
        "entry.md",
        "a",
        "entry.md",
    ]


def test_a_target_dispatching_itself_is_refused() -> None:
    assert refused({"entry.md": ["a"], "a": ["a"]}) == ["entry.md", "a", "a"]


@pytest.mark.parametrize("size", [40])
def test_a_dense_graph_terminates(size: int) -> None:
    names = [f"n{at}" for at in range(size)]
    edges = {name: list(names) for name in names}
    edges["entry.md"] = names
    assert codes(edges).count(DISPATCH_DEPTH) == size
    assert refused(edges) == ["entry.md", "n0", "n0"]


def test_a_dense_acyclic_graph_terminates() -> None:
    names = [f"n{at:02}" for at in range(40)]
    edges = {name: names[at + 1 :] for at, name in enumerate(names)}
    edges["entry.md"] = names
    assert refused(edges) is None
