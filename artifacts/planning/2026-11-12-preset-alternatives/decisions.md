# Decisions

## Confirmed

Settled in the design interview (user, 2026-11-12). Each names the options set aside.

1. **A pick reaches its target alone.** The picked alternative's `subst` routes the target's links to that kind's material. Set aside: forwarding a pick to linked documents through a title tag; applying it to every document of the run.
2. **The marker is a `?` title tag on a deferred link.** Set aside: a new operator mark in the link text.
3. **The target declares its alternatives** with `choice: <when to pick it>`, and exactly one is in force wherever it compiles. Set aside: offering every named preset; listing the alternatives in each link's title.
4. **The listing is pf's answer to `?`**: exit 2, each alternative with its choice line, and the same answer for a missing or wrong pick. Set aside: a listing flag; writing the list into the published link.
5. **`?` is accepted on deferred links only** (`¬`, `¬↳`). Set aside: compiling every alternative of a dispatch up front; publishing a dispatch for the agent to compile and hand on.
6. **An alternative's `subst` pairs route quietly**: no `W_SUBST_USED`, and `W_SUBST_UNUSED` only for a pair no link of its document names. Set aside: relaxing both warnings for every pair; keeping them.
7. **Delivery is a new initiative** planned through work-planner. Set aside: one hot-fix pull request; a record with nothing raised.
8. **work-kind is the motivating case.** work-planner is pre-migration, so a work-kind-shaped fixture proves the pattern.
9. **The exactly-one failure has its own code**, `E_ALTERNATIVE_UNRESOLVED`, with exit 2, so a harness matches the pick step by code. Set aside: reusing `E_INVALID_USAGE`, as group and `subst` conflicts do.

## Defaults Taken

Details settled without a question; each can be reopened.

- `choice` holds a non-empty one-line string, and a `choice` in `default` is refused.
- A preset named `?` is refused.
- Exactly one alternative is counted on the union of presets every reference reaching the document selects in one bundle.
- `?` selects no preset, in a title or in `--presets`; the listing is the exactly-one failure.
- The run publishing a deferral refuses a link to alternatives that names none, names two, or names one beside `?`, since the later run would fail.
- A diagram link selects no preset, so a document with alternatives reached through diagram links alone fails the exactly-one rule.

## Open Questions

None.
