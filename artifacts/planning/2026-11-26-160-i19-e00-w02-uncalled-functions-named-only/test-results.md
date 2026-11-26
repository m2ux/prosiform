# Test Results

Validation observed at `i19/e00/w02-uncalled-functions` head 5a9e5ae5c, based on `i19/e00/main` at 3c400526d.

## Reachability

- **T1, AC1.** `make reachability` over the repository reads 570 definitions and exits 0. Nine are reached from outside the package, each with its reason:
  - `cli.main`, the console script `pf` declared in `src/pyproject.toml`;
  - `candidate.Use.__eq__`, `__hash__`, `__repr__`, `cli.BudgetEntries.__call__`, `cli.Once.__call__` and `closure.Substitution.__post_init__`, methods Python calls by name;
  - `metadata._MarkedScanner.scan_flow_scalar_non_spaces` and `profile.Watched.skipToken`, framework hooks on the written list.
- **No dead code today.** The run found no definition without a caller or a reason, so nothing was removed. The R1 audit's `delivery` wrapper is no longer in the package.
- **T1, harness.** `checks/tests/test_reachability.py` holds the reading against small packages written for it:
  - `test_a_function_named_only_by_itself_is_not_reached` fails a recursive function nothing else names.
  - `test_a_method_named_as_an_attribute_is_reached` and `test_an_import_alias_reaches_the_function_it_imports` reach a definition through an `Attribute` and through an alias.
  - `test_a_nested_function_is_part_of_the_function_holding_it` reads one definition from a function holding another.
  - `test_a_method_the_language_calls_is_reached`, `test_a_declared_entry_point_is_reached` and `test_a_listed_framework_hook_is_reached` reach a dunder method, a `[project.scripts]` entry and a listed hook.
  - `test_a_listed_definition_the_package_names_fails` and `test_a_listed_definition_the_package_lacks_fails` fail a list entry the package does not need.

## Limitations

- **A name reaches every definition carrying it.** Names are compared rather than calls resolved, as the issue's Proposal sets out. `cli.Parser.error`, the hook `argparse` calls on a usage failure, reads as reached because `cli` binds a local `error` in `except OSError as error`; listing it would fail the check as an entry the package already names. A definition sharing its name with any variable the package uses passes the same way.

## Suites

- **T2.** `make check`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`, exits 0: lint, format (520 files), types (110 source files), reachability (570 definitions), 2,125 build tests, 1,206 harness tests, 708 corpus fixtures (708 pass), smoke, layout, tables (24 commands), links (445 documents), vocabulary, invocation, conformance and independence.
