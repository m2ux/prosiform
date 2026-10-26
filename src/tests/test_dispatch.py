"""Assert the dispatch analysis follows chains as deep as the limit and no further.

Each graph here is a mapping from a target to the targets its closure
dispatches, standing in for the closures a run would traverse, so a case
states the shape of the dispatches and the warnings that shape raises.
"""

from collections.abc import Mapping, Sequence

from prosiform.closure import Reference
from prosiform.diagnostics import Location
from prosiform.dispatch import DISPATCH_CYCLE, DISPATCH_DEPTH, Hop, Onward, analysed


def hop(name: str, written: str) -> Hop:
    """One dispatch of a document, written in another."""
    return Hop(Reference(name, name, chain=("entry.md", name)), Location(written, 1, 1))


def graph(edges: Mapping[str, Sequence[str]]) -> Onward:
    """The dispatches each target's closure carries, under the edges given."""

    def onward(target: Reference) -> Sequence[Hop]:
        return [hop(name, target.path) for name in edges.get(target.path, ())]

    return onward


def codes(edges: Mapping[str, Sequence[str]]) -> list[str]:
    """The codes the analysis raises for the entry's dispatches."""
    first = [hop(name, "entry.md") for name in edges.get("entry.md", ())]
    found = analysed(first, {"entry.md"}, graph(edges))
    return [one.code for one in found]


def test_a_chain_of_exactly_the_limit_raises_nothing() -> None:
    assert codes({"entry.md": ["a"], "a": ["b"], "b": ["c"]}) == []


def test_a_cycle_longer_than_the_limit_is_deep_and_a_cycle() -> None:
    edges = {"entry.md": ["a"], "a": ["b"], "b": ["c"], "c": ["d"], "d": ["a"]}
    assert codes(edges) == [DISPATCH_DEPTH, DISPATCH_CYCLE]


def test_a_cycle_within_the_limit_is_a_cycle_alone() -> None:
    assert codes({"entry.md": ["a"], "a": ["entry.md"]}) == [DISPATCH_CYCLE]


def test_a_dense_graph_terminates() -> None:
    names = [f"n{at}" for at in range(40)]
    edges = {name: list(names) for name in names}
    edges["entry.md"] = names
    found = codes(edges)
    assert found.count(DISPATCH_DEPTH) == len(names)
    assert found.count(DISPATCH_CYCLE) == len(names)


def test_two_links_dispatching_one_target_warn_once() -> None:
    edges = {"a": ["b"], "b": ["c"], "c": ["d"]}
    first = [hop("a", "entry.md"), hop("a", "entry.md")]
    found = analysed(first, {"entry.md"}, graph(edges))
    assert [one.code for one in found] == [DISPATCH_DEPTH]
