# Change List

The plan changes the W08 delivery session applied and held.

## Applied

- **Debt fixed: a dispatch inside an inline-only contribution.**
  The W03 session found that a dispatch link inside a contribution pointed at the sub-section in its target's own file group, which W08 removes. Without a fix, the run refused the dispatch with `E_UNSUPPORTED_CONSTRUCT`. Now, when no group carries the region a contribution copies, the first contribution emits the dispatch sub-section one level below the composed section holding the link. Fixture: `a-dispatch-in-an-inline-only-contribution-takes-its-own-sub-section`.
- **Delivery recorded.** [#569](https://github.com/m2ux/prosiform/pull/569) merged into `i09/e04/main` at `32568729`. W08's row links it and is marked Done, `AC17` is ticked on [#460](https://github.com/m2ux/prosiform/issues/460), and review pull request [#556](https://github.com/m2ux/prosiform/pull/556) carries the change under Section Composition. These record the delivery and do not change the plan.

## Held

None.

## Notes

- **W05 retires the interim directive rule.**
  Composition does not yet place a directive inside a contribution, so placement reads one as an ordinary inclusion and keeps a group for its target (`placement` in `src/prosiform/cli.py`, the `inside` branch, and two `test_cli.py` cases). When W05 composes such directives, it removes that branch and the two tests, so the target becomes inline-only.
- **The design names no rule for a dispatch inside a contribution.**
  The build places its sub-section beneath the contribution, following the general *Dispatch sub-sections* rule. W10's composition page should say so.
- **W02 fixtures still link their targets whole.**
  They pass unchanged, and each keeps the file group its whole-document link includes.
