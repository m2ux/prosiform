# Change List — W20 State the Publication and Title-Dispatch Refusals in the Design

> Delivery record · 2026-11-01

The plan changes this session applied, the ones it held, and the technical debt it classified.

## Applied

| Change | Kind | Why | Where |
| --- | --- | --- | --- |
| The Publication clause refuses a non-folder, non-link at the run folder's path with `E_PUBLICATION_FAILED` and leaves it in place | Design | AC31; the build, `docs/bundles.md` and the corpus already state it | engineering `f028ee97` |
| The Dispatch sub-sections clause refuses a dispatch in a heading emitted as text alone with `E_UNSUPPORTED_CONSTRUCT` | Design | AC31; the build, `docs/dispatch.md` and the corpus already state it | engineering `f028ee97` |

No task, epic or criterion was created, closed or renumbered.

## Held

| Held | Why |
| --- | --- |
| Moving the README's Design link on `i07/e00` to `f028ee97`, and so the pull request and merge | The commit also carries six I08 declaration commits (`771f8c1b`–`ca8e1c97`) the I07 build does not implement; at that pin `make vocabulary` and `make conformance` fail. See [Validation](validation.md). With the pin unmoved the branch carries no change, so no pull request was opened, #482 stays open and `AC31` stays unticked |

## Debt

None classified. The design history on `engineering` holds I07 and I08 statements in one line, so no I07 pin can name a design carrying the W20 clauses without I08's; that is a planning decision held above, not debt.
