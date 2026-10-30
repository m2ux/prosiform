# W02 Change List

Plan changes arising in delivery. Allowance: none, so every non-trivial change is held for the planner.

## Applied

| Change | Reason |
| --- | --- |
| A seventh class, *invalid transition*: a state the diagram holds that no edge leads to from the state before it — a step back, a state after a terminal one, or an immediate repeat. *Invented state* is only a name the diagram does not hold, and *skipped state* excludes the predecessor itself, so a repeat on a cycle is an invalid transition. | Planner decision on PR #336, approved by the user: the six classes left a step the diagram gives no route to without a home. Epic #333's AC4 names the seventh class. |
| *Loop miscount* is the departure at a decision on how often `trace.log` holds a line; *wrong branch* is the departure at any other decision. | Fixes the precedence the work item leaves to the plan: at the loop's decision, the other edge is the loop taken more or fewer times. |
| `checks.md`, `src/README.md` and the Makefile's harness comment name the scorer. | In scope: they describe what `make harness` holds. |

## Held

None.
