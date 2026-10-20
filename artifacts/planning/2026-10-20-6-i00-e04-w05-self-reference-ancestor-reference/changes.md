# Change List — I00:E04:W05 and W06

> Applied 2026-10-20 under the session's change allowance. Creating a new initiative sits outside it; nothing here needed one.

## Applied

| Kind | Issue or row | What was applied |
| --- | --- | --- |
| Folded work | [`decisions.md`](../2026-10-17-prosiform-v1/decisions.md) D42 | A marked direct self-reference carries `E_SELF_REFERENCE`. The contract declared the failure and named no code, so AC4 was undeliverable as written. Found by measuring the build rather than by reading the plan |
| Folded work | [`design.md`](../2026-10-17-prosiform-v1/design.md) Self-reference and ancestor-reference behavior | The Direct self-reference clause names `E_SELF_REFERENCE`, and says that the refusal is of a marked link, an unmarked one being a mention the bundle emits as authored |
| Folded work | [`design.md`](../2026-10-17-prosiform-v1/design.md) Link classification and resource handling | A clause declaring `E_MARKED_RESOURCE`, per D40 |
| Folded work | [`design.md`](../2026-10-17-prosiform-v1/design.md) Resource limits | A clause declaring `E_RESOURCE_LIMIT` and what its message names, per D41 |
| Folded work | [`design.md`](../2026-10-17-prosiform-v1/design.md) CLI contract | One sentence saying each budget adds an option, pointing at the table that declares them. The options stay declared in one place |
| Trivial debt, fixed | `fixtures/README.md` | The prose named two fixtures carrying `awaiting` and the corpus carried three, none of them one of the two named. It names the three the corpus holds and the work each waits on |
| Delivery record | [#6](https://github.com/m2ux/prosiform/issues/6) rows W05 and W06 | Both rows link the pull request, AC4, AC7, AC11, AC13 and AC17 are ticked, and Done is ticked on both after the merge |

## Held

| Kind | Issue or row | What is recommended |
| --- | --- | --- |
| — | — | Nothing is held. No finding needed an initiative, and no debt was classified non-trivial, so [#39](https://github.com/m2ux/prosiform/issues/39) takes no new row |

## Markers

| Marker | Fixture | Disposition |
| --- | --- | --- |
| — | — | None added. This unit's twenty-three fixtures all hold against the build it delivers |
| — | — | None lifted. The three the base carried — `I00:E09:W02`, `I00:E05:W03` and `I00:E08` — are untouched, and the README now names them |

## What the Brief Got Wrong

| Statement | What was found |
| --- | --- |
| "You add two new error codes" and "the catalogue stands at 21 and must end at 23" | Three codes. AC4's failing half had no code either, which the design's own text shows and the build confirmed. The error catalogue held twenty rather than twenty-one and ends at twenty-three, the two catalogues holding twenty-five between them |
| "The same may be true of parts of AC4 and AC13" — that they need no code | The ancestor half of AC4 holds on the base. The self-reference half and AC13 both need the ownership model, which is one implementation serving both |
