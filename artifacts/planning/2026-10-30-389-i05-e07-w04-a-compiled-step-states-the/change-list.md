# I05:E07:W04 Change List

The plan changes this delivery session met, and what it did with each.

## Applied

- **Task creation — `I05:E07:W04`, with AC5.** The row the delivery was raised as, reading `A compiled step states its dispatch by its operators` and covering one new criterion: a compiled form's step states its dispatch by the operator its links carry and by nothing beside it. Added to the epic's Work Breakdown with its link to pull request 416, and AC5 to the epic's criteria, ticked on the merged evidence.

## Held

- **The fixture corpus states the dispatch in prose before the operator.** 33 fixture sources write `Hand the … to a sub-agent: [⇉ plan](plan.md).`, and 16 expected bundles carry that sentence as published output. `pf` compiles the mark and carries the prose beside it, so the build accepts the duplicate this row removes from the eval. **Recommended:** raise a corpus row that rewrites the 33 sources and regenerates the 16 bundles, and decide whether `pf` should refuse a dispatch step restating its operator — a new diagnostic and a change to `invocation.md`. Held because it reaches past the eval into the compiler's contract, and `invocation.md` states no such refusal today.

## Design readings recorded by this unit

Each is a reading the unit took while implementing. None changes the plan.

- **The operator states the dispatch; a protocol states its meaning.** The division is what the row rests on, and it is why the authored form keeps its prose: it has no operator and no protocol.
- **`together` and the re-dispatch continuation are protocol text, not step text.** Both are stated by `Parallel dispatch` and `Dispatch` respectively, so a step repeating either is the same duplicate as a step naming a sub-agent.
- **The guard is the eval's, not `pf`'s.** `pf` carries a sentence beside a dispatched link untouched, so the corpus cannot be held to this rule by the build until a diagnostic exists.
