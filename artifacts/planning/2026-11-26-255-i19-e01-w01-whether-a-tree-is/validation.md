# W01 Validation

Each check the pull request's Test Plan records, run at `775b1bb4546af40963530a5bbb57ca5a7231ded7` on `i19/e01/w01-whether-tree-is-sound`, the task's commits merged with `i19/e01/main` at `b2b2a965fc2ee3befc18b1abc80fe7b2d741459b`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`.

## T1 check-all over two failing checks

`checks/tests/test_check_all.py::test_check_all_names_every_failing_check` runs `make check-all` over a makefile that includes the repository's `Makefile` and sets `CHECKS` to three stand-in checks, the first and third failing. All three ran, the run exited nonzero, and it printed `check-all: failed: alpha gamma`. Observes AC1 and the task's AC3 and AC4.

## T2 check-all over a passing set

`test_check_all_passes_a_tree_where_every_check_passes` runs the same makefile with no failing check: all three ran and the run exited 0 with `check-all: every check passed`. Observes the task's AC5 with T5.

## T3 check stops at its first failure

`test_check_stops_at_the_first_failing_check` runs `make check` over the same failing set: only the first check ran and the run exited nonzero, so `make check` keeps its meaning.

## T4 runner's three states

In `checks/tests/test_runner.py`:

- `test_a_run_whose_output_moved_is_told_from_one_that_failed_in_itself` runs two fixtures declaring the same bundle. One run writes other bytes and reaches `State.MOVED`, reported as `output moved`. The other exits 4 with `E_UNEXPECTED_INTERNAL_ERROR` and reaches `State.FAILED_IN_ITSELF`, reported as `run failed in itself`. Neither passed. Observes AC2 and the task's AC6.
- `test_a_run_meeting_its_manifest_is_met` and `test_a_declared_internal_error_meets_its_manifest` reach `State.MET`, the second for a fixture declaring the internal error as its outcome.
- `test_a_run_ended_by_a_signal_failed_in_itself`, `test_a_run_that_does_not_complete_is_reported` and `test_a_malformed_fixture_is_refused_without_invoking_the_build` reach `State.FAILED_IN_ITSELF`.

`make harness`: 1169 passed.

## T5 the repository's checks

`make check` exited 0: 2330 build tests and 1169 harness tests passed, and the corpus check reported `708 fixture(s), 708 pass, 0 fail, 0 awaited, 0 unexpected pass`. The link check resolved every reference in 445 documents, run with network. The table check found 21 commands, `make check-all` among them, each declared and named by a table.

`make check-all` over the same tree exited 0 and printed `check-all: every check passed`.
