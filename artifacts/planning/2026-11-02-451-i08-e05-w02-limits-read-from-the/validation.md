# Validation

Evidence for each check the work item names, run in the task worktree with `PROSIFORM_BUILD` naming the worktree's own build.

## Tested revisions

- **Task branch:** `i08/e05/w02-limits-read-from-the` at `79c29079`, cut from `i08/e05/main` at `6d9652b4`.

## Unit tests

`src/tests/test_limits.py`, observing AC3: 11 passed.

- **An unnamed budget stands at its default.** `test_a_run_naming_no_budget_holds_every_budget_at_its_default` reads the budgets in force from no entries and finds each of the eight at its declared default.
- **A named budget leaves the rest at default.** `test_a_named_budget_holds_its_figure_and_the_rest_their_defaults` names each of the eight in turn and finds that figure for it and the default for the other seven.
- **One entry per `Budget`.** Both tests above find the `Limits` in force holding exactly the keys of `BUDGETS`; `test_each_budget_is_declared_once_under_its_own_name` finds each budget declared once and `NAMED` resolving each name to its own budget.
- **The figure in force is the one held.** `test_a_figure_past_the_budget_in_force_is_crossed` holds a budget at a named figure, admits that figure and raises `Crossed` one past it.

`src/tests` under `make test`: 1584 passed, `test_cli.py` among them, its `test_a_budget_entry_sets_the_budget_it_names` reading the same defaults through the parser.

## Repository check

`make check` exits 0 at `79c29079`: lock, lint, format, typecheck, steps, authoring, boundary, test (1584 passed), harness (1157 passed), corpus (427 fixtures, 427 pass), smoke, layout, tables, links, vocabulary, invocation, conformance, independence and mock scenarios.

## Merge

Continuous integration passed on `79c29079`, and [#554](https://github.com/m2ux/prosiform/pull/554) merged into `i08/e05/main` as `92d2f50f`.
