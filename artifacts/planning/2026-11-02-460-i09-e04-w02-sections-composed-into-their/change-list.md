# Change List

The plan changes the W02 delivery session applied and held.

## Applied

- **Folded work: the parentless refusal.**
  W02 refuses a directive whose target has no heading above it with `E_UNSUPPORTED_CONSTRUCT`, naming the link. This is one case of W04's *A missing containing heading, a missing source or parent section* (AC8). A contribution heading has to name a parent, so composition needs this refusal for every target. W04 keeps the rest of AC8.
- **Debt fixed: invisible labels.**
  The design's *Recognition* clause (engineering `ee8df501`), the predicate, the glossary, W01's unit test and a new fixture now treat a whitespace, control or format scalar as no directive. W01 had pinned a no-break space as a directive.

## Held

- **The README design pin stays at `99bec9f7`.**
  Engineering's design gained I08:E06's `subst` clauses (`187478e4`) before the Recognition amendment. Those clauses rename `W_MOCK_*` to `W_SUBST_*`, and `i09/e04/main` does not yet carry that code. Pinning `ee8df501` fails the harness's catalogue check, and no engineering revision carries only the amendment. The pin can move to `ee8df501` or later once I08:E06 is in the base that pins it, which is the next design-clause row or integration on `main`. Until then the build is stricter than the pinned clause in one case: it reads an invisible scalar as no directive.

## Notes

- **The target keeps its own group.**
  Until W08, a target reached only through directives is still bundled in its own file group. Each W02 fixture also links its targets whole, so the expected bundles already meet *Inline-only targets*.
- **Diagnostics left to W04.**
  A composed heading past H6 is refused with `E_HEADING_DEPTH_OVERFLOW`, but the diagnostic names the target document rather than the directive. An authored child heading equal to a destination section is not refused yet. Both belong to W04's AC8.
- **Nested directives, deferred directives and whole-document targets compose nothing yet.**
  A directive inside a contribution, a deferred directive, and a directive naming a whole document each still bundle as the ordinary or deferred link they are. These belong to W05 and W06.
