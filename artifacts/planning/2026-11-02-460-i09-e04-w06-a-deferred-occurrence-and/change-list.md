# Change List

The plan changes the W06 delivery session applied and held.

## Applied

- **Operator syntax folded in as debt.** (User, 2026-11-02.) Operator symbols are written together, with the one blank before the link's text.
  - Design `3ed0bf02` amends *The deferral mark*, *Operators that combine* (the rule's home), *Recognition*, *Operator marks* and the Dispatch and Composition fixture lists.
  - The I09 record's Decisions carry it.
  - The W01 work item, the docs reference page and the glossary are corrected.
  - #556's Changes gain the syntax, the eligible target and deferred composition.
  - The README pin moves to `3ed0bf02`.
- **Delivery recorded.** [#576](https://github.com/m2ux/prosiform/pull/576) merged into `i09/e04/main` at `1a80f346`. W06's row links it and is marked Done, `AC11` to `AC13` are ticked on [#460](https://github.com/m2ux/prosiform/issues/460), and review pull request [#556](https://github.com/m2ux/prosiform/pull/556) carries the change. These record the delivery and do not change the plan.

## Held

None.

## Notes

- **Fixtures whose meaning changed.**
  - `a-deferred-glyph-label-is-a-deferred-directive` is renamed `a-glyph-written-against-the-deferral-mark-is-a-deferred-directive` and uses `[¬→]`.
  - `a-dispatched-glyph-is-a-dispatch`, `[⇉ →]` as a dispatch, is now `a-blank-between-the-dispatch-mark-and-a-glyph-is-refused`.
  - `operator-marks-are-no-directive-label` uses `[⇉→]` where it used `[¬→]`.
  - The new fixture `a-blank-between-the-deferral-mark-and-a-glyph-is-refused` refuses `[¬ →]`.
- **Gapped dispatch marks.** `[⇉ ⫽ x]` and `[⇉ ¬ x]` were read as a dispatch whose text opened with a mark; now they are refused. No fixture held the earlier reading.
- **Delivered records left as they ran.** The W00 and W01 validation records state what passed at their revisions, so they keep the earlier syntax.
- **Activation is a run of its own.** Per the pinned *Activation* clause, the deferred line's destination is an entry reference, and the run it names publishes the composed body as its own bundle.
- **No arising issues.**
