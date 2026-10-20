# Change List — I00:E04:W04

> Applied 2026-10-20 under the session's change allowance. Creating a new initiative sits outside it; nothing here needed one.

## Applied

| Kind | Issue or row | What was applied |
| --- | --- | --- |
| Task creation | [#6](https://github.com/m2ux/prosiform/issues/6) row W07 | `W07 — Ancestor promotion over structural ancestors`, depending on [E09:W02](https://github.com/m2ux/prosiform/issues/60), with its work item at [i00-e04/w07.md](../2026-10-17-prosiform-v1/i00-e04/w07.md) |
| Migration | [#6](https://github.com/m2ux/prosiform/issues/6) rows W04 and W07 | AC10 moved off W04's Coverage onto W07's. W04 covers AC3 and AC9, which it delivered; AC10 waits on the row that can reach the state it turns on |
| Delivery record | [#6](https://github.com/m2ux/prosiform/issues/6) row W04 | The row links [#81](https://github.com/m2ux/prosiform/pull/81), AC3 and AC9 are ticked, and Done is ticked after the merge |
| Blocking debt, fixed | [#81](https://github.com/m2ux/prosiform/pull/81) | A run could write its bundle over a source it reached as a dependency. The output check moves to the completed closure |
| Trivial debt, fixed | [#81](https://github.com/m2ux/prosiform/pull/81) | `cli.sources()` resolved a source path, which crosses a symbolic link the read refuses. It locates a source under the canonicalized root instead, and `distinct()` goes with the pre-traversal check it existed for |
| Trivial debt, fixed | `design.md`, Heading-only structural ancestors | The example bundle headed its group `# guide.md`, which the File-scoped hierarchy rule removes the suffix from, and ran its regions together, which the Block boundaries rule separates by a blank line. It is the example [W07](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1/i00-e04/w07.md) builds to |
| Record correction | [#81](https://github.com/m2ux/prosiform/pull/81) | The merged body named AC10 under its coverage, which `sync.py` reported as a disagreement with the row. It names the row AC10 moved to |

## Held

| Kind | Issue or row | What is recommended |
| --- | --- | --- |
| — | — | Nothing is held. No finding needed an initiative, and no debt was classified non-trivial, so [#39](https://github.com/m2ux/prosiform/issues/39) takes no new row |

## Markers

| Marker | Fixture | Disposition |
| --- | --- | --- |
| `awaiting = "I00:E09:W02"` | `ancestor-promotion/a-link-to-a-heading-only-ancestor` | Added. The corpus stands at three awaited |
| — | — | None lifted. The two the base carried, `I00:E08` and `I00:E05:W03`, are untouched |
