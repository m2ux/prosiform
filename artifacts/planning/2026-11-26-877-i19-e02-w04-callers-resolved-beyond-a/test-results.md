# Test Results

Validation observed at `i19/e02/w04-callers-beyond-shared-name` head 41d747589, based on `i19/e02/main` at 6eb02cb5c.

## Reachability

- **T1, AC4.** `checks/tests/test_reachability.py` writes small packages in which a method `Box.error` shares its name with a binding, and the check fails it in each:
  - `test_a_binding_sharing_a_definitions_name_does_not_reach_it`, one case each for a local variable, a parameter, an exception name (`except OSError as error`, then loaded), a loop target, a comprehension target, a lambda parameter, a keyword argument's name and a module variable.
  - `test_a_variable_of_an_enclosing_function_shadows_the_name_inside_it` resolves a load in a nested lambda to the enclosing function's variable.
- **The rule still reaches what it should.**
  - `test_a_name_a_function_loads_without_binding_reaches_the_definition` reaches a module function loaded inside a comprehension.
  - `test_a_class_attribute_does_not_shadow_a_name_its_methods_load` keeps a class body's names out of its methods, as Python resolves them.
  - `test_a_decorator_reaches_the_function_it_names` and `test_a_name_declared_global_resolves_in_the_module` reach through a decorator and a `global` declaration.
- **The repository.** `make reachability` reads 567 definitions and exits 0. The stricter rule failed three on first reading:
  - `cli.Parser.error`, which `argparse` calls on an argument it cannot parse, joins `EXTERNAL_CALLERS` with that reason.
  - `closure.boundary`, with its helper `closure.climb`, had no caller but `src/tests/test_closure.py`; both are removed with their tests.
  - `provenance.Range.kept` had no caller but one test in `src/tests/test_candidate.py`, which now reads `Range.removed`; it is removed.

## Suites

- **T2.** `make check`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`, exits 0: lint, format (522 files), types (112 source files), reachability (567 definitions), 2,116 build tests, 1,247 harness tests, 708 corpus fixtures (708 pass), smoke, layout, tables, links (445 documents), vocabulary, invocation, conformance and independence.
