# Change List

The plan changes the W15 delivery session applied and held.

## Applied

- **Design — one group pair.** `design.md` on `engineering` at `c1c68415` replaces *`group` is refused* with *`group` holds one pair*, states `E_GROUP_CONFLICT`, and rewrites the example, the field table, the Grouping clause, *An entry is one string key with an integer value*, *`default` always applies*, *Selected presets union*, *What a selection governs*, *A document in several groups*, the metadata failure table and the rejected-metadata row. The README design pin on the branch moves to it.
- **Review pull request [#508](https://github.com/m2ux/prosiform/pull/508).** The Changes bullets naming `group-depth`, a list of pairs or one group named twice are reworded for one `group` pair and `E_GROUP_CONFLICT`, and R12 cites [#518](https://github.com/m2ux/prosiform/pull/518).

W15's row links [#518](https://github.com/m2ux/prosiform/pull/518), which records delivery rather than changing the plan.

## Held

- **Epic integration of I08:E01.** Every row is Done and every criterion ticked after #518, so the epic is ready for [Epic Integration](https://github.com/m2ux/prosiform/pull/508): agent review, review pull request #508 ready, In Review on the board, and the merge into `main`. The brief forbids this session merging an epic base into `main`, so integration is left to the caller.

Validation found no deferred debt, and no issue arose during delivery.

## Notes

- **Fixtures whose meaning depended on one link placing a document in two divisions.** `a-title-matching-two-keywords-selects-both` and `default-applies-in-every-section` are rewritten to show selection with one pair; `a-dependencys-preset-comes-from-itself` and `an-entry-name-reads-its-documents-presets` are re-recorded with the selected pair holding over `default`'s; `a-document-joins-two-divisions` is removed.
- **sync.py reports #510 and #511 naming criteria their rows do not cover** (AC12 on #510; AC14 and AC15 on #511). The brief leaves them alone.
- **Merged** as `923affc3` into `i08/e01/main`, CI green on head `ad7623ff`; `AC12` and W15 Done ticked on #436.
