# Change List

The plan changes the W07 delivery session applied and held.

## Applied

- **Dispatch mark against a directive's label folded in.** (User, 2026-11-02.) `[⇉→]`, `[⫽→]` and `[¬⇉→]` are refused with `E_UNSUPPORTED_CONSTRUCT`, naming the link: a dispatch sends material to a sub-agent and a directive places it inline.
  - Design `aa97db93` amends *Operators that combine* (the rule's home), *Operator marks* and the Composition fixture list.
  - The I09 record's Decisions carry it.
  - The docs reference page and the glossary state it.
  - The README pin moves to `aa97db93`.
- **Delivery recorded.** W07's row links its pull request, `AC14` is ticked on [#460](https://github.com/m2ux/prosiform/issues/460) on merge, and review pull request [#556](https://github.com/m2ux/prosiform/pull/556) carries the change. These record the delivery and do not change the plan.

## Held

None.

## Notes

- **No routing change.** Every composition failure is raised while the entry and its dispatched bundles compile, before `publication` makes the output folder or writes a bundle; the fixtures pin that.
- **Fixture whose meaning changed.** `operator-marks-are-no-directive-label` uses `[⇉step]` where it used `[⇉→]`.
- **No arising issues.**
