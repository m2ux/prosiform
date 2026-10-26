"""How deep the dispatches a bundle starts run, and whether they return.

A dispatched target is compiled by a sub-agent, and its own content may
dispatch again, so dispatch nests: the session following the bundle hands
the target to a sub-agent, which compiles it and may hand a target of its
own to another. A *dispatch depth* is the number of dispatch hops along one
such chain, counted from the bundle being compiled: a dispatch the bundle
carries is the first hop, a dispatch the closure of that target carries is
the second, and so on.

The closure a target would have compiled as its own entry is what its
sub-agent reads, so the hops beyond the first are read from that closure,
under the rules any compilation follows: a link resolves from the file that
writes it within that file's root, a deferred link contributes nothing, and
a dispatched link is a hop. Which closure that is, is the caller's to
compute; this module follows the hops it is handed and reads nothing
itself. The analysis decides warnings and nothing else, so the bundle a run
publishes is the bundle it would publish without it.

A chain is deeper than the limit where it reaches a hop past it, and the
search for one stops there, so it is bounded however wide the dispatches
fan out. A chain returning to a target already on it — the bundle's own
entry among them — is a cycle, which is no depth: the sub-agents it starts
would dispatch one another without end. A target already on the chain is
not followed again, so neither search revisits a target along one chain
and both terminate on any graph of dispatches.
"""

from collections.abc import Callable, Collection, Iterator, Sequence
from dataclasses import dataclass

from prosiform.closure import Reference, identity
from prosiform.diagnostics import WARNING, Diagnostic, Location, RelatedLocation

DISPATCH_DEPTH = "W_DISPATCH_DEPTH"
DISPATCH_CYCLE = "W_DISPATCH_CYCLE"

CODES = (DISPATCH_DEPTH, DISPATCH_CYCLE)

LIMIT = 3

DEPTH_REMEDY = (
    "compile an intermediate target into the bundle that dispatches it, or "
    "dispatch its targets from an earlier hop"
)
CYCLE_REMEDY = "compile or cite one target of the cycle rather than dispatching it"


@dataclass(frozen=True)
class Hop:
    """One dispatched link: the target it names and where it is written."""

    target: Reference
    location: Location

    @property
    def name(self) -> str:
        """The target as the document and section it names."""
        return identity(self.target)


Onward = Callable[[Reference], Sequence[Hop]]


class Graph:
    """The dispatches each target's own closure carries, read once per target."""

    def __init__(self, onward: Onward) -> None:
        self.onward = onward
        self.read: dict[str, tuple[Hop, ...]] = {}

    def beyond(self, hop: Hop) -> tuple[Hop, ...]:
        """Each distinct dispatch the closure of one hop's target carries."""
        if hop.name not in self.read:
            distinct: dict[str, Hop] = {}
            for one in self.onward(hop.target):
                distinct.setdefault(one.name, one)
            self.read[hop.name] = tuple(distinct.values())
        return self.read[hop.name]


def deepest(graph: Graph, first: Hop, entries: Collection[str]) -> list[Hop] | None:
    """The first chain from one hop that reaches a hop past the limit.

    A chain is followed in the order each closure writes its dispatches,
    and only through targets not already on it, so a cycle adds no depth.
    """
    chain = [first]
    on = {*entries, first.name}
    pending: list[Iterator[Hop]] = [iter(graph.beyond(first))]
    while pending:
        if len(chain) > LIMIT:
            return chain
        following = next(pending[-1], None)
        if following is None:
            pending.pop()
            on.discard(chain.pop().name)
            continue
        if following.name in on:
            continue
        chain.append(following)
        on.add(following.name)
        pending.append(iter(graph.beyond(following)))
    return None


def returning(graph: Graph, first: Hop, entries: Collection[str]) -> list[Hop] | None:
    """The first chain from one hop whose last hop names a target already on it.

    The entries stand on every chain, so a dispatch naming the bundle's
    own entry closes a cycle. A target every chain through which was
    followed to its end without returning is not followed again.
    """
    if first.name in entries:
        return [first]
    chain = [first]
    on = {*entries, first.name}
    done: set[str] = set()
    pending: list[Iterator[Hop]] = [iter(graph.beyond(first))]
    while pending:
        following = next(pending[-1], None)
        if following is None:
            pending.pop()
            name = chain.pop().name
            on.discard(name)
            done.add(name)
            continue
        if following.name in on:
            return [*chain, following]
        if following.name in done:
            continue
        chain.append(following)
        on.add(following.name)
        pending.append(iter(graph.beyond(following)))
    return None


def reported(
    code: str, message: str, remedy: str, entry: str, chain: Sequence[Hop]
) -> Diagnostic:
    """One warning naming a chain: its first link, then every later hop."""
    first, *later = chain
    return Diagnostic(
        WARNING,
        message,
        code=code,
        reference=first.target.original,
        chain=(entry, *(hop.name for hop in chain)),
        remedy=remedy,
        location=first.location,
        related=tuple(
            RelatedLocation(
                hop.location.file,
                hop.location.line,
                hop.location.column,
                f"dispatches {hop.name!r}",
            )
            for hop in later
        ),
    )


def analysed(
    hops: Sequence[Hop], entries: Collection[str], onward: Onward
) -> list[Diagnostic]:
    """The warnings the dispatches one bundle carries raise.

    Each distinct target the bundle dispatches is followed from the first
    link naming it, and raises at most one warning of each code: one for
    the first chain from it reaching a hop past the limit, and one for the
    first chain from it returning to a target already on it. The warnings
    follow the order the bundle's dispatches were read in.
    """
    graph = Graph(onward)
    found: list[Diagnostic] = []
    distinct: dict[str, Hop] = {}
    for hop in hops:
        distinct.setdefault(hop.name, hop)
    for first in distinct.values():
        entry = first.target.chain[0] if first.target.chain else first.name
        written = first.target.original
        deep = deepest(graph, first, entries)
        if deep is not None:
            found.append(
                reported(
                    DISPATCH_DEPTH,
                    f"the dispatch {written!r} starts a chain reaching "
                    f"{len(deep)} dispatches, deeper than the {LIMIT} a chain "
                    f"is held to",
                    DEPTH_REMEDY,
                    entry,
                    deep,
                )
            )
        loop = returning(graph, first, entries)
        if loop is not None:
            found.append(
                reported(
                    DISPATCH_CYCLE,
                    f"the dispatch {written!r} starts a chain that dispatches "
                    f"{loop[-1].name!r} again, so its sub-agents would dispatch "
                    f"one another without end",
                    CYCLE_REMEDY,
                    entry,
                    loop,
                )
            )
    return found
