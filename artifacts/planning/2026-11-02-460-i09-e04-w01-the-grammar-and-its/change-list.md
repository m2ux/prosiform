# Change List

The plan changes the W01 delivery session applied and held.

## Applied

- **Folded work: the preamble refusal.**
  W01 refuses a directive written in a preamble with `E_UNSUPPORTED_CONSTRUCT`, one case of W04's *A missing containing heading* (AC8). Recognition alone changes no output, so the lexical fixtures AC1 and AC2 name need a behaviour that answers it; the refusal is that behaviour and is permanent. W04 keeps the other scopeless case, a heading the bundle emits as text alone, and the rest of AC8.

- **Delivery recorded.** [#562](https://github.com/m2ux/prosiform/pull/562) merged into `i09/e04/main` at `4f13b24d`; W01's row links it and is Done, `AC1` and `AC2` are ticked on [#460](https://github.com/m2ux/prosiform/issues/460), and review pull request [#556](https://github.com/m2ux/prosiform/pull/556) carries the change under Directive Recognition. These record delivery rather than change the plan.

## Held

None. Validation found no deferred debt, and no issue arose during delivery.

## Notes

- **Composition stays with W02.** A directive inside a section bundles as the ordinary reference it is until W02 places it, so no fixture yet shows a placed contribution.
- **A no-break space qualifies.** The clause trims and normalises nothing, so a label of one no-break space is a directive; a unit test pins it.
