# Change List — W00 Design Clause, Retired Codes and Pin

> Plan changes · Created 2026-10-31

## Applied

Nothing. No plan change arose that this run's allowance covers.

## Held

- **Task creation, I08:E00.** The row cannot be delivered as planned. Retiring the eight budget letters and `-f` in the design before the build implements either leaves `make conformance` failing on 33 fixtures across twelve families, and the pinned contract would describe a build that does not exist. The recommended option is to split this row: keep the declaration clause, the `root` refusal and the code retirements here, and return the budget, `-f`, `-x` and `-m` retirements to the epics that implement each (`I08:E05` budgets, `I08:E03` remove-the-referrer, `I08:E04` faults, `I08:E06` preset-only substitution), so each retirement lands in the pull request that makes it true.

## Reported, not changed

- **Record registration, I08:E07.** The epic record's Artifacts table registers `w12.md` twice, as W10 ("The fourth refused shape") and as W12 ("A folder key's absent substitute"). The epic's two rows state the opposite: W10 is the folder key's absent substitute and unused report, and W12 is the value naming no Markdown document. Two rows therefore link one work item, and neither carries the other's. The rows are delivered, so their ids are fixed by the pull requests naming them; the correction is to the record's table and is left for the user to decide, since it reaches a planning record this row does not own.
