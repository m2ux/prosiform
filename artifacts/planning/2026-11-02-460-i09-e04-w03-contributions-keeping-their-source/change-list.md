# Change List

The plan changes the W03 delivery session applied and held.

## Applied

- **Delivery recorded.** [#567](https://github.com/m2ux/prosiform/pull/567) merged into `i09/e04/main` at `64f85304`. W03's row links it and is marked Done, `AC5` and `AC6` are ticked on [#460](https://github.com/m2ux/prosiform/issues/460), and review pull request [#556](https://github.com/m2ux/prosiform/pull/556) carries the change under Section Composition. These record the delivery and do not change the plan.

## Held

None.

## Notes

- **No code change was needed.**
  W02's rewrite already resolves each composed region against its source and keys each contribution by its directive's position. W03 states both rules in the composition module and pins them with fixtures.
- **A dispatch inside a contribution points at its source's sub-section.**
  The contribution's dispatch link points at the dispatch sub-section in the target's own file group, as W02's dispatch pass states. W08 drops the file group of a document reached only by directives, which removes that sub-section, so W08 must give such a dispatch a sub-section of its own.
