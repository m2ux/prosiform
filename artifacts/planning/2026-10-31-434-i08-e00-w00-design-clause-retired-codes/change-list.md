# Change List — W00 Design Clause, Retired Codes and Pin

> Plan changes · Created 2026-10-31

## Applied

- **Folded work, I08:E00 W00.** The row's scope is narrowed to the clause the build already supports. The seven amendments planned for one pin are returned to the epics that implement each: the budget collapse to `I08:E05`, the `-f` withdrawal to `I08:E03`, the `-x` withdrawal to `I08:E04`, the `-m` retirement and preset-only substitution to `I08:E06`, exclusion to `I08:E02`, and presets to `I08:E01`. Each lands in the pull request that makes it true. (User, 2026-10-31.)

## Held

Nothing.

## Reported, not changed

- **Record registration, I08:E07.** The epic record's Artifacts table registers `w12.md` twice, as W10 ("The fourth refused shape") and as W12 ("A folder key's absent substitute"). The epic's two rows state the opposite: W10 is the folder key's absent substitute and unused report, and W12 is the value naming no Markdown document. Two rows therefore link one work item, and neither carries the other's. The rows are delivered, so their ids are fixed by the pull requests naming them; the correction is to the record's table.
- **The pin join, I08:E07.** The design declares `W_MOCK_SUBSTITUTED` and `W_MOCK_UNUSED`, whose schema landed at `12803a9e` on `i05/e09/main` and has never reached `main`. Any pin naming an `engineering` revision carrying those statements fails `test_a_catalogue_is_the_codes_the_design_declares`. `i05/e09/main` is `I08:E07`'s base, so the merge that closes the gap belongs to that epic rather than to this row.
