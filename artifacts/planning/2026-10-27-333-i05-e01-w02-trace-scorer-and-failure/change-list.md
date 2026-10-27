# W02 Change List

Plan changes arising in delivery. Allowance: none, so every non-trivial change is held for the planner.

## Applied

| Change | Reason |
| --- | --- |
| *Invented state* also covers a diagram state no walk reaches from the state before it, which includes any state entered after a terminal one. | Needed for the classes to cover every failing trace: a step back or past the end is neither a drawn successor nor further along a walk, and naming a step the diagram gives no route to is the nearest of the six. Flagged for the planner's review. |
| *Loop miscount* is the departure at a decision on how often `trace.log` holds a line; *wrong branch* is the departure at any other decision. | Fixes the precedence the work item leaves to the plan: at the loop's decision, the other edge is the loop taken more or fewer times. |
| `checks.md`, `src/README.md` and the Makefile's harness comment name the scorer. | In scope: they describe what `make harness` holds. |

## Held

None.
