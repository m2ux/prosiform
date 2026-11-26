# Test Results

Validation observed at `i19/e01/w07-fixture-run-by-identity` head 183c95f46, based on `i19/e01/main` at b0eb7a233.

## Selection

- **T1, AC15.** `checks/tests/test_corpus_run.py` holds the request in the corpus harness:
  - `test_an_identity_selects_the_fixture_carrying_it` selects `family/moved` and `beside` from a corpus holding a family, in path order.
  - `test_an_identity_no_fixture_carries_is_refused` raises `UnknownFixture` naming `family/absent` and `family`, the family directory.
  - `test_a_named_fixture_reports_its_verdict_under_its_identity` prints `family/met: pass` and a count of one fixture.
  - `test_a_named_fixture_is_decided_as_the_corpus_run_decides_it` exits 1 for `family/moved` and prints exactly the lines the whole run prints for that fixture, the byte difference among them.
  - `test_a_request_naming_no_fixture_runs_nothing` exits 1 for `family`, prints nothing to standard output and names the identity on standard error.
  - `test_a_request_both_reporting_and_running_is_refused` refuses `--awaiting` beside an identity.
- **Real corpus.** `corpus.py identity/whole-document identity/path-needing-escaping` against the worktree's `pf` prints both as `pass` and `2 fixture(s), 2 pass`; `corpus.py identity/whole extraction` exits 1 naming both.

## Suites

- **T2.** `make check`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`, exits 0: lint, format, types, 2,330 build tests, 1,162 harness tests, 708 corpus fixtures (708 pass), links, conformance and independence.
