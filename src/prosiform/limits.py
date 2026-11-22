"""Declare resource budgets and report crossings through `Limits.hold`.

`Budget` records each budget's command-line name, default, counting
description and minimum. `in_force` supplies a complete configuration.
"""

from collections.abc import Mapping
from dataclasses import dataclass

RESOURCE_LIMIT = "E_RESOURCE_LIMIT"

CODES = (RESOURCE_LIMIT,)

SCALAR_DIGITS = 65_536
"""The most characters one quadratically-canonicalised scalar may carry.

A source at the byte budget of a megabyte holds a million digits, and a
base-prefixed integer of that length takes minutes to canonicalise. This
ceiling holds the work one such scalar may ask for to a figure whose cost
stays well inside the second, whatever size the source holding it is.
"""


@dataclass(frozen=True)
class Budget:
    """One budget's declaration.

    `name` identifies its option, `default` is its default ceiling,
    `counted` names the measured quantity, and `least` is its minimum.
    """

    name: str
    default: int
    counted: str
    least: int = 1


FILES = Budget("files", 256, "distinct source documents opened")
FILE_BYTES = Budget("file-bytes", 1_048_576, "raw bytes in one source")
INPUT_BYTES = Budget(
    "input-bytes", 16_777_216, "raw source bytes, counted once per source"
)
OUTPUT_BYTES = Budget("output-bytes", 262_144, "bytes of the complete bundle")
TARGETS = Budget("targets", 4_096, "distinct document and section targets discovered")
LINKS = Budget(
    "links", 32_768, "authored link and image occurrences in selected content"
)
NESTING = Budget(
    "nesting",
    64,
    "levels of container nesting and, independently, "
    "YAML collection nesting in one source",
    least=2,
)
EXPANSION_DEPTH = Budget("depth", 8, "link hops from the nearest entry reference")

BUDGETS = (
    FILES,
    FILE_BYTES,
    INPUT_BYTES,
    OUTPUT_BYTES,
    TARGETS,
    LINKS,
    NESTING,
    EXPANSION_DEPTH,
)

NAMED = {budget.name: budget for budget in BUDGETS}
"""Each budget under the name a command line sets it by."""


class Crossed(Exception):
    """A budget crossing with its budget, configured limit and observed count.

    The exception message identifies the boundary, the measured quantity
    and the count; `remedy` supplies the author's next action.
    """

    def __init__(self, budget: Budget, limit: int, counted: int) -> None:
        super().__init__(
            f"the run reached {counted} {budget.counted}, which crosses the "
            f"{budget.name} budget of {limit}"
        )
        self.budget = budget
        self.limit = limit
        self.counted = counted

    @property
    def remedy(self) -> str:
        """The one remedy every crossing leads to, naming the entry that raises it."""
        return f"restructure the sources, or raise --budget {self.budget.name}"


@dataclass(frozen=True)
class Limits:
    """The `declared` budget ceilings, with access and enforcement methods."""

    declared: Mapping[Budget, int]

    def hold(self, budget: Budget, counted: int) -> None:
        """Raise `Crossed` when `counted` exceeds this run's ceiling for `budget`.

        A crossing refuses the run rather than truncating its input or output.
        """
        limit = self.declared[budget]
        if counted > limit:
            raise Crossed(budget, limit, counted)

    def of(self, budget: Budget) -> int:
        """The number one budget stands at for this run."""
        return self.declared[budget]


def in_force(named: Mapping[Budget, int]) -> Limits:
    """Every budget in force: each figure `named` holds, the rest at default.

    The result holds one entry per declared budget, so a run naming no
    budget stands at every default and no stage reads a budget it lacks.
    """
    return Limits({budget: named.get(budget, budget.default) for budget in BUDGETS})
