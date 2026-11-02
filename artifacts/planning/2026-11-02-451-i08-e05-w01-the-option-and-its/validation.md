# Validation

Evidence for each check the work items name, run in the task worktree with `PROSIFORM_BUILD` naming the worktree's own build.

## Tested revisions

- **Design:** engineering `a7069f30`, which the README badge pins.
- **Task branch:** `i08/e05/w01-the-option-and-its` at `cac9aaaa`.

## Unit tests

`src/tests` under `make test`: 1573 passed.

- **A named entry sets its budget.** `test_a_budget_entry_sets_the_budget_it_names` sets each of the eight by name and finds the other seven at their defaults; `test_budget_entries_naming_several_budgets_set_each` sets three at once, in both the spaced and the joined spelling.
- **A crossing names the budget.** `test_a_crossed_budget_fails_the_run_and_names_the_budget` crosses seven budgets by name, and each diagnostic names the budget and the remedy `--budget <name>`.
- **Each refused entry is invalid usage.** `test_a_budget_entry_the_grammar_does_not_admit_is_invalid_usage` covers an unknown name, no `=`, an empty name, an empty value, zero, a budget named twice and `nesting=1`: exit status `2`, `E_INVALID_USAGE`, no bundle, each message naming the fault. `test_an_unknown_budget_name_is_reported_with_every_name_admitted` finds all eight names in the message.

## Corpus

`make corpus`: 427 fixtures, 427 pass, 0 fail.

- **AC1.** `fixtures/limits/a-named-budget-bounds-the-run` passes `--budget files=1` over two sources and fails with `E_RESOURCE_LIMIT`, the message reading `reached 2` and `files budget of 1`. `fixtures/dispatch/a-dispatched-target-crossing-the-file-budget` holds `files=3` and `fixtures/limits/a-file-count-budget-crossed` holds `files=2` the same way.
- **AC2.** `fixtures/cli/an-unknown-budget-name-is-invalid-usage` (`key=1`, naming `'key'` and the eight), `fixtures/cli/a-malformed-budget-entry-is-invalid-usage` (`files`, no `=`), `fixtures/cli/a-budget-entry-naming-no-budget-is-invalid-usage` (`=1`), `fixtures/limits/a-zero-override-is-refused` (`files=0`) and `fixtures/limits/a-negative-override-is-refused` (`files=-1`) each exit `2` with `E_INVALID_USAGE`.
- **AC4.** The 21 fixtures that passed a letter pass its name, and no `expected` block changed: `git diff 220a19cf cac9aaaa -- fixtures` touches their `arguments` lines alone, beside the two refused-override fixtures' `clauses`, which name `Resource limits — Malformed entry`, and one `description` that named `-F 1`.
- **AC5.** `fixtures/cli/a-budget-named-twice-is-refused` (`files=1`, `files=2`) exits `2` with `E_INVALID_USAGE`, naming `files budget is named twice`.
- **AC8.** `fixtures/cli/a-nesting-budget-below-two-is-refused` (`nesting=1`) exits `2` with `E_INVALID_USAGE`, naming `nesting budget of 1 is below 2`.

## Invocation

`make invocation`, observing AC7: 29 statements hold. The option table names one budget row, `--budget NAME=VALUE`, reproducing the help word for word; the budgets table names `files`, `file-bytes`, `input-bytes`, `output-bytes`, `targets`, `links`, `nesting` and `depth`, each matching the help's `budgets:` line. `checks/tests/test_invocation.py` under `make harness` (1157 passed) drifts a budget's default and drops a budget row, and each fails the comparison.

## Conformance

`make conformance`: 332 clauses, 0 declarations naming no clause. `Resource limits — Unknown name`, `— Malformed entry`, `— Name given twice` and `— Nesting floor` are each covered, and `CLI contract — --budget NAME=VALUE` is covered by `fixtures/limits/a-named-budget-bounds-the-run`. `make independence` holds.

## Repository check

`make check` exits 0 at `cac9aaaa`: lock, lint, format, typecheck, steps, authoring, boundary, test, harness, corpus, smoke, layout, tables, links, vocabulary, invocation, conformance, independence and mock scenarios.
