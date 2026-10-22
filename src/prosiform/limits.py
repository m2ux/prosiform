"""The declared resource budgets, and what a run reports when it crosses one.

A compilation that is not bounded is discovered by exhausting memory rather
than by a diagnostic, so the profile declares eight budgets and a run fails
at the first boundary it crosses. A budget fails rather than truncates:
nothing is dropped to fit, no bundle is published, and the figure the run
reports is what tells an author whether to restructure the sources or to
raise the number.

Each budget names the option that overrides it, the default it stands at,
and the rule by which its figure is counted. The counting rule is the whole
of a budget's meaning — a byte budget summed once per source identity and
one summed per reference are different budgets — so it is written beside
the number rather than left to whichever stage happens to count.

One code names every crossing. Whichever budget it was, the remedy is the
same shape, and the message says which boundary the run crossed and what
it had counted when it crossed it, which is what distinguishes one
crossing from another. `E_PARSER_REFERENCE_LIMIT` is a different thing
entirely: an internal parser limit suppressing a reference lookup, which
is a defect in indexing rather than a budget an author chose.

Overrides are positive decimal integers. Zero is refused and does not mean
unlimited, because a budget of nothing is a run that cannot open its first
source, and a caller who wants a larger number says so.
"""

from collections.abc import Mapping
from dataclasses import dataclass

RESOURCE_LIMIT = "E_RESOURCE_LIMIT"

CODES = (RESOURCE_LIMIT,)


@dataclass(frozen=True)
class Budget:
    """One declared budget: the option that sets it, its default, and its rule."""

    option: str
    dest: str
    default: int
    counted: str


FILES = Budget("-F", "max_files", 256, "distinct source documents opened")
FILE_BYTES = Budget("-B", "max_file_bytes", 1_048_576, "raw bytes in one source")
INPUT_BYTES = Budget(
    "-I", "max_input_bytes", 16_777_216, "raw source bytes, counted once per source"
)
OUTPUT_BYTES = Budget("-O", "max_output_bytes", 262_144, "bytes of the complete bundle")
TARGETS = Budget(
    "-T", "max_targets", 4_096, "distinct document and section targets discovered"
)
LINKS = Budget(
    "-L",
    "max_links",
    32_768,
    "authored link and image occurrences in selected content",
)
NESTING = Budget("-N", "max_nesting", 64, "levels of container nesting in one source")
EXPANSION_DEPTH = Budget(
    "-E", "max_expansion_depth", 8, "link hops from the nearest entry reference"
)

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


class Crossed(Exception):
    """One budget a run crossed, named with the figure it had counted.

    The message is the whole diagnostic a caller reads: which boundary
    the run crossed, what the budget counts, and the figure that crossed
    it. One code covers every budget, so the message is what says which.
    """

    def __init__(self, budget: Budget, limit: int, counted: int) -> None:
        super().__init__(
            f"the run reached {counted} {budget.counted}, which crosses the "
            f"{budget.option} budget of {limit}"
        )
        self.budget = budget
        self.limit = limit
        self.counted = counted

    @property
    def remedy(self) -> str:
        """The one remedy every crossing leads to, naming the option."""
        return f"restructure the sources, or raise {self.budget.option}"


@dataclass(frozen=True)
class Limits:
    """The budget in force for each declared limit, and the holding of it."""

    declared: Mapping[Budget, int]

    def hold(self, budget: Budget, counted: int) -> None:
        """Hold one budget against the figure counted so far."""
        limit = self.declared[budget]
        if counted > limit:
            raise Crossed(budget, limit, counted)

    def of(self, budget: Budget) -> int:
        """The number one budget stands at for this run."""
        return self.declared[budget]
