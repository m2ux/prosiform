# Validation

Every check ran on branch `i08/e04/w01-the-parser-and-the` at revision `62b5d9a1`, through `make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`. Exit status `0`.

## Unit tests

`make test`: 1572 passed.

- `src/tests/test_cli.py`: `test_the_internal_fault_names_the_run_and_publishes_nothing` sets `PROSIFORM_FAULT=internal` and observes status `4` and `E_UNEXPECTED_INTERNAL_ERROR`; `test_a_run_asking_for_no_fault_meets_none` removes the variable and observes status `0`, no diagnostic, and the source unchanged (AC1).
- `test_a_fault_the_contract_does_not_declare_is_a_usage_failure`, over `other` and the empty string, observes status `2`, one `E_INVALID_USAGE` naming the value and the three faults, no bundle, and the source unchanged (AC6).
- `test_the_source_changed_fault_fails_the_run_and_publishes_nothing` and the three tests in `src/tests/test_derived_output.py` reach `source-changed` and `cleanup-refused` through the variable.

## Harness

`make harness`: 1150 passed.

- `checks/tests/test_runner.py`: `test_the_run_receives_the_fault_the_manifest_names_through_its_environment` observes the child reading `source-changed` from `PROSIFORM_FAULT` and an argument list ending `-d json guide.md`; `test_a_run_meeting_no_fault_carries_no_variable` sets the variable in the corpus's own environment and observes it absent in the child (AC2).
- `checks/tests/test_manifest_schema.py`: `unrecognized` validates as a fault, and `""`, `source_changed`, `SOURCE-CHANGED` and `other` still fail (AC4).

## Corpus

`make corpus`: 422 fixtures, 422 pass, 0 fail.

- `diagnostics/a-run-that-fails-in-itself`: pass (AC1, AC5).
- `cli/an-unknown-fault-is-invalid-usage`: pass, status `2`, `E_INVALID_USAGE` naming `unrecognized` and the three faults (AC6).
- `source-consistency/a-source-that-changes-during-compilation` and `publication/an-earlier-set-the-run-cannot-remove-warns`: pass (AC5).
- No fixture's `arguments` names `-x`; each fault reaches the build through the environment the runner sets (AC2).

## Invocation

`make invocation`: 28 statements held to the build's help. `pf -h` names no `-x`, the option table has no row for it, and the two-way comparison passes (AC3).

## Inspection

- `fixtures/README.md` states `fault` as a manifest field asked for "by the means the contract declares", linking the design's Conformance faults section, and names no flag. `checks/runner.py` translates the field into `PROSIFORM_FAULT` in `environment()` (AC4).
- `grep` over the worktree finds no `-x` option, `options.fault` or `-x NAME` outside history.

## Unchanged fixtures

`git diff origin/i08/e04/main -- fixtures/source-consistency fixtures/diagnostics/a-run-that-fails-in-itself fixtures/publication/an-earlier-set-the-run-cannot-remove-warns` is empty (AC5).

## Conformance

`make conformance`: `Conformance faults — Unknown value` lists `cli/an-unknown-fault-is-invalid-usage`; every declared clause resolves against the pinned design.
