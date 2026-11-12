# Review Fixes

Two findings from the agent reviews of the epic's review pull requests, each fixed on the epic base the review read: [#717](https://github.com/m2ux/prosiform/issues/717) on `i15/e00/main` for [#713](https://github.com/m2ux/prosiform/pull/713), and [#718](https://github.com/m2ux/prosiform/issues/718) on `i15/e00/engineering` for [#711](https://github.com/m2ux/prosiform/pull/711).

## F717 Routing Pair Order

Revision tested: `a2c5ae8df` on `i15/e00/f717-routing-pair-order`, based on `i15/e00/main` at `eead56b50`. Every check ran from the unit checkout with `PROSIFORM_BUILD` naming that checkout's build: `uv run --project <unit-checkout>/src --frozen pf`.

The design's substitution mapping makes a pair an alternative states a routing pair and flags every other pair a reference uses. `governing` keeps the ordinary preset's entry for a key an alternative states identically, so the pair warns `W_SUBST_USED` whichever preset the document declares first.

- `test_a_pair_an_ordinary_preset_shares_warns_in_either_order`, parametrized over both declaration orders: both pass; with `cli.py` reverted, the alternative-first case fails with no warning, reproducing #717.
- Inclusion fixtures `a-shared-pair-warns-with-the-alternative-first` and `a-shared-pair-warns-with-the-ordinary-preset-first`: each exits 0 with one `W_SUBST_USED` for `body.md` at `work-kind.md:11:1`.
- `make check`: exit 0. `make test` 2014 passed, `make harness` 1006 passed; `corpus check: 567 fixture(s), 567 pass, 0 fail, 0 awaited, 0 unexpected pass`; lint, format, typecheck, lock, smoke, layout, tables, links, vocabulary, invocation, conformance and independence each passed.

## F718 Metadata Failures Wording

Revision tested: `c5700040f` on `i15/e00/f718-metadata-failures-wording`, based on `i15/e00/engineering` at `59382d3a2`.

The Metadata failures paragraph reads "Every metadata failure, exit 1 or 2, fails check mode, publishes no bundle and preserves an existing output file", so the sentence names both exit classes rather than the two exit-2 exceptions alone.

- `python3 checks/links.py --online` on the design, run from the main checkout: `link check: every reference in 1 document(s) resolved`.
- A read of the section: each exit class is stated once, and the heading and every clause name are unchanged, so the pins at `c04f5d8e6` on `i15/e00/main` stay valid.
