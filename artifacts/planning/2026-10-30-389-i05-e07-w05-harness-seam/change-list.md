# I05:E07:W05 Change List

The plan changes this delivery session met, and what it did with each.

## Applied

- **Task creation — `I05:E07:W05`.** The row this delivery was raised as, reading `A harness drives any agent CLI` and covering one new criterion: a run drives the agent CLI its harness names, reading that CLI's own stream for its sub-agent starts, returns, result and tokens. Added to the epic's Work Breakdown with its link to pull request 418.
- **Re-prioritisation — the run's budget.** `--budget-usd` and `--session-budget-usd` become `--budget-tokens` and `--session-budget-tokens`, the Makefile's `EVAL_BUDGET_USD` becomes `EVAL_BUDGET_TOKENS`, and the report's token column becomes one count while its cost column reads `—` where a harness reports none. Taken as folded work, since the row cannot be held to one measure across two CLIs without it.

## Held

- **No criterion for the second harness's parity.** W05's criterion says a run drives the CLI its harness names; it says nothing about whether a Cursor pass rate is comparable with a Claude one, and the two differ in isolation, model and session cap. **Recommended:** raise a corpus-and-comparison row that states what makes two harnesses' pass rates comparable and refuses a report that compares them without it. Held because it needs a measurement neither harness has yet made.
- **The stub prints one stream's shape.** `stub_agent.py` emits Claude's blocks, so the Cursor path is held only by `test_harness.py` against captured shapes. **Recommended:** give the stub a second emitter and run one stubbed Cursor matrix in `make harness`, so the whole loop is covered for both. Held as work beyond this row's criterion.

## Design readings recorded by this unit

None changes the plan.

- **The budget is tokens because that is what both CLIs report.** Cost is a figure a harness records where it has one, not the measure a run is held to.
- **Isolation is a harness's to declare.** A CLI that cannot confine a session as another does states the difference, and the comparison states it beside the number.
