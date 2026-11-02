# Change List

The plan changes the W12 delivery session applied and held.

## Applied

- **Design amended for all three criteria.** (User, 2026-11-02, I09 Decisions.) Design `4958ad38` defines an *arrow* once in *Recognition* (the four Arrows blocks, and Dingbats or Miscellaneous Symbols and Arrows scalars named `ARROW`), narrows *Operator marks* to `⇉` and `↳`, adds *Composing its own document* with `W_COMPOSE_SELF`, and adds `## Run pf first` with the line referring to it to *The Prosiform section*; *Clean Markdown*, the exit-status codes and both fixture lists follow. The README pin moves to `4958ad38`; the glossary defines *arrow*.
- **First-run wording carries the command.** (Coordinator, relaying the user, mid-session.) The `Run pf first` sub-section states ``Run `pf` first, with no arguments, and follow the guide it prints.``, the runnable command in a code span; no frontmatter or blockquote carrier.
- **W12 work item written.** `e04/w12.md` and the I09 README's work-item table carry it.
- **Delivery recorded.** [#580](https://github.com/m2ux/prosiform/pull/580) merged into `i09/e04/main` at `304fa79c`. W12's row links it and is marked Done, `AC22` to `AC24` are ticked on [#460](https://github.com/m2ux/prosiform/issues/460), and review pull request [#556](https://github.com/m2ux/prosiform/pull/556) carries the change and its reference. These record the delivery and do not change the plan.

## Held

None.

## Notes

- **Fixtures whose meaning changed.** `a-supplementary-scalar-label-is-a-directive` (`𝔸`) became `a-supplementary-arrow-label-is-a-directive` (`🡒`); `invisible-scalar-labels-are-ordinary-links` became `non-arrow-labels-are-ordinary-links`; `an-entity-decoding-to-one-scalar-is-a-directive` was renamed for its arrow; `a-deferred-dispatch-in-a-dispatched-bundle` now expects the first-run section. Unit cases `[é]`, `[𝔸]`, `[&#x1D538;]`, `[¬𝔸]`, `[⇉𝔸]` moved accordingly.
- **No arising issues, no deferred debt.**
