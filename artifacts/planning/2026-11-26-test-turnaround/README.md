# Test Turnaround

## Executive Summary

A change to the build costs more in tests and fixtures than in source. The checks run quickly: continuous integration finishes `make check` in about 95 seconds, the build's tests in 18 seconds and the harness tests in 14. The cost is the volume rewritten by hand on each change.

Two pieces of work reduce it, in this order.

1. **Accept mode.** The corpus runner writes a fixture's expected bundles from the build under test, so a change to bundle text or bundle names is reviewed as a diff, not typed.
2. **Overlap audit.** Each test in `test_cli.py` is listed beside the fixtures that already hold the same behaviour, and the user approves each removal before a test is deleted.

No issue is raised yet.

## Measurements

Taken on `main` at b0eb7a233.

| Measure | Value |
| --- | --- |
| Source, `src/prosiform` | 16,208 lines |
| Build tests, `src/tests` | 18,775 lines, 1,208 test functions |
| Harness tests, `checks/tests` | 328 test functions |
| Eval tests, `evals/diagram-following` | 352 test functions |
| Fixtures | 708, holding 614 expected bundles of 10,250 lines |
| `test_cli.py` | 5,779 lines, 342 test functions |

Lines changed across the 33 most recent merges into `main` that touch source:

| Area | Lines | Files |
| --- | --- | --- |
| Source | 12,346, of which 5,297 are one comment cleanup | 132 |
| Fixtures | 13,910 | 1,539 |
| Build tests | 4,169 | 102 |
| Documents | 1,068 | 202 |

- F33 changed 49 source lines and 1,291 fixture lines.
- F38 changed 15 source lines, 106 test lines and 120 fixture files, 96 of them one-line edits to a manifest's bundle list beside a renamed expected bundle.
- `test_cli.py` took 1,699 of the 4,424 test lines changed.

## Accept Mode

`python checks/corpus.py --accept` runs the corpus and, for each fixture whose run differs from its manifest in its bundles alone, writes what the run produced.

- **Written.** The files under `expected/`, and the manifest's `bundles` list where the names changed. A bundle the run no longer writes is removed.
- **Never written.** `exit_status`, `diagnostics`, `stdout_contains`, `clauses`, `description` and `awaiting`. These state the contract and stay authored.
- **Refused.** A fixture whose exit status or diagnostics differ, or whose run writes a different number of bundles than its manifest declares, is reported as failing and left untouched, so accepting cannot hide a behaviour change behind a bundle rewrite.
- **Local only.** Continuous integration never passes `--accept`. The check stays the comparison; accepting is an authoring aid whose output is a reviewed diff.
- **Manifest edits.** The `bundles` line is replaced in place so comments and layout survive.

`make corpus ARGS=--accept` reaches it. `checks/tests/test_corpus_run.py` holds its tests.

## Overlap Audit

The audit produces a table and removes nothing.

1. Run the build's tests under coverage with a context per test, and the corpus under subprocess coverage with a context per fixture. Coverage runs through `uv run --with`, outside the lockfile.
2. For each `test_cli.py` test, list the fixtures whose covered lines contain the test's.
3. Read each candidate pair and record whether the fixture asserts what the test asserts. Line containment shortlists; reading decides.
4. Hand the table to the user. A test is removed only where a named fixture holds its assertion and `make conformance` reports no clause newly uncovered.

## Later Candidates

Not planned here, recorded so they are not lost.

- Refusal and warning fixtures that also pin a full bundle.
- A rule in `AGENTS.md` stating which layer a new behaviour's test belongs to.
- A local target that reports every failing check in one run.
- The online half of `make links` moved off pull requests.

## Tasks

- [ ] Raise the issue for accept mode.
- [ ] Deliver accept mode with its harness tests and document it in `checks.md` and `fixtures/README.md`.
- [ ] Produce the overlap table for `test_cli.py`.
- [ ] User review of the table.

## Open Decisions

| Decision | State |
| --- | --- |
| Order of work | Decided by the user: accept mode, then the overlap audit. |
| Whether accept mode may write a manifest's `bundles` list | Decided by the user: names only. A run writing a different number of bundles than the manifest declares is refused. |
| Whether the two pieces are raised as one issue or two | Open. |
