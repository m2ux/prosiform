## Overview

What `I00:E11:AC5` required, the fixture that states it, and the two runs that show the fixture decides between a build reporting the outcome and one that does not.

## The Rule Under Test

The corpus could not hold a fixture for an allowed source root naming no directory. `missing_files` reported `invocation.root` as a missing path whenever it was not a directory, so the one shape of fixture that states the outcome was the one shape the validator refused, and the fixture was rejected before any build was invoked.

A manifest declaring `E_ROOT_NOT_FOUND` has declared that the run cannot find its root, because that code is the contract's name for exactly that outcome. `absent_root()` reads it, `missing_files` leaves such a fixture's root alone, and `present_files` refuses one that carries the directory anyway. The declaration is the diagnostic, so no field beside `invocation.root` repeats it and the two cannot disagree.

Three harness tests hold the rule, all under `make harness`:

| Test | Holds |
| --- | --- |
| `test_a_fixture_declaring_an_absent_root_is_decided_from_its_manifest` | A fixture declaring the outcome and carrying no source tree validates, and its run is decided from the manifest. |
| `test_a_fixture_declaring_an_absent_root_it_holds_is_refused` | A fixture declaring the outcome while holding the directory is refused, and the build is never invoked. |
| `test_a_fixture_naming_a_root_it_does_not_hold_is_refused` | Every other fixture is still held to a root that is a directory it carries. |

`make harness` reports 383 passed against the base's 379: these three, and the schema check the corpus test runs over the one new fixture.

## The Build That Reports It

`fixtures/cli/an-allowed-source-root-naming-no-directory/` declares exit status 1, empty standard output and one `E_ROOT_NOT_FOUND` error. It carries `expected/stdout.md` and no `source/`.

```text
cli/an-allowed-source-root-naming-no-directory: pass
corpus check: 204 fixture(s), 202 pass, 0 fail, 2 awaited, 0 unexpected pass
```

The corpus grew by one fixture and the awaited count is unchanged, so nothing else moved.

## The Build That Does Not

The same corpus was run against a build whose root check was removed — the six lines of `cli.py` that raise `E_ROOT_NOT_FOUND` deleted, nothing else touched — and then restored.

```text
cli/an-allowed-source-root-naming-no-directory: fail
  expected.exit_status: expected 1, the run exited 4
  expected.diagnostics: the run emits 1 diagnostic where 1 diagnostic is expected
    position 1: error E_ROOT_NOT_FOUND expected, error E_UNEXPECTED_INTERNAL_ERROR produced
corpus check: 204 fixture(s), 201 pass, 1 fail, 2 awaited, 0 unexpected pass
```

One fixture of 204 told the two builds apart, and it is this one. That is the criterion: the outcome is stated by the corpus rather than by one build's own tests, so every implementation of the contract is held to the same code and the same status.

The mutant is also what the outcome costs when it is unreported. With no root check the run reaches directory enumeration on a path that is not there and ends in an unexpected internal error at exit status 4 — a fault in the tool, reported for a command line the caller wrote.

## The Gate

Measured on `i00/e11/w04-a-fixture-declaring-an` at its delivered head.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | Success: no issues found in 44 source files |
| `make test` | 603 passed |
| `make harness` | 383 passed |
| `make corpus` | 204 fixture(s), 202 pass, 0 fail, 2 awaited, 0 unexpected pass |
| `make smoke` | Installs and bundles from an environment outside the repository |
| `make layout` | 3 tree(s) present |
| `make tables` | 14 command(s) and 7 declaration(s) |
| `make links` | Every reference in 12 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |
| `make invocation` | 27 statement(s) of the documented invocation |

## The Review

- **The build is untouched.** The change is confined to `checks/manifests.py`, `checks/tests/test_runner.py`, `checks/README.md`, `fixtures/README.md`, `fixtures/manifest.schema.json` and the new fixture. Nothing under `src/` moved, so the fixture states what the build already does rather than following a change to it.
- **The schema's shape is unchanged.** Only the `root` description was rewritten, so no manifest validates differently against the document itself and the catalogue test is untouched.
- **No other fixture changed verdict.** Each of the other 203 was read by the validator and run, before and after, with the same result.
- **The contradiction is refused in both directions.** A fixture declaring the outcome while holding the directory, and a fixture declaring any other outcome over an absent root, are each reported and each stop the run before the build is invoked, held by a test apiece.

## Limitations

The rule is keyed on a code rather than on a field of its own, so a second outcome that also implies an absent root would need the predicate widened. The contract declares one, and widening it is a line in `absent_root()`.

The mutant run measured a build with the check removed. It did not measure a build that reports the outcome under another code, which the fixture would also fail on the diagnostic comparison and which the catalogue makes unreachable.
