# Change List

The plan changes the W00 delivery session applied and held.

## Applied

None. W00 linked [#539](https://github.com/m2ux/prosiform/pull/539), ticked Done and `AC7` on [#458](https://github.com/m2ux/prosiform/issues/458), which records delivery rather than changing the plan, and the draft review pull request [#541](https://github.com/m2ux/prosiform/pull/541) was opened and linked to #458.

## Held

None. Validation found no deferred debt, and no issue arose during delivery.

## Notes

- **Nesting is settled in the design.** The design states where a nested group stands: inside the division of the document whose reference placed its first member, after that division's own content, one level deeper per enclosing division. A document with no pair keeps its file group at the top level, so bundles declaring no pair keep their arrangement. W02's plan reads the level from this clause rather than settling it.
- **An entry's pair still applies.** The invocation bundles each entry, so an entry's pair places the entry's own sections and *The parent arrangement* stands unchanged.
- **The pin carries the concurrent clause.** The pinned revision `febd4a6d` sits after I08:E04's PROSIFORM_FAULT clause on `engineering`, so this base pins a design holding both.
