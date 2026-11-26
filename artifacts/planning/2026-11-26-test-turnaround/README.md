# Test Turnaround

> Epic plan. Created 2026-11-26.

## Executive Summary

A change to the build costs more in tests and fixtures than in source. The checks run quickly: continuous integration finishes `make check` in about 95 seconds, the build's tests in 18 seconds and the harness tests in 14. The cost is the volume rewritten by hand on each change.

[Epic I19 E01, issue #858](https://github.com/m2ux/prosiform/issues/858) holds the work. It gathers the four turnaround rows the repository checks epic carried, and adds the reading of the command-line tests against the corpus and the removal of each test the user approves.

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

## Restatement

`checks/restate.py` runs the corpus and, for each fixture whose run differs from its manifest in its bundles alone, names what it would write. With `--write` it writes it.

- **Written.** The files under `expected/`, and the manifest's `bundles` entry where the names changed.
- **Never written.** `exit_status`, `diagnostics`, `stdout_contains`, `clauses`, `description` and `awaiting`. These state the contract and stay authored.
- **Refused.** A fixture whose run failed in itself, whose exit status or diagnostics differ, or whose run writes a different number of bundles than its manifest declares is named and left untouched.
- **Local only.** Continuous integration compares and never restates.

## Overlap Audit

The audit produces a table and removes nothing.

1. Run the build's tests under coverage with a context per test, and the corpus under subprocess coverage with a context per fixture. Coverage runs through `uv run --with`, outside the lockfile.
2. For each `test_cli.py` test, list the fixtures whose covered lines contain the test's.
3. Read each candidate pair and record whether the fixture asserts what the test asserts. Line containment shortlists; reading decides.
4. Hand the table to the user. A test is removed only where a named fixture holds its assertion and `make conformance` reports no clause newly uncovered.

## Later Candidates

Not planned here, recorded so they are not lost.

- Refusal and warning fixtures that also pin a full bundle.
- The online half of `make links` moved off pull requests.

## Tasks

- [x] Raise the epic and move the turnaround rows into it.
- [x] Place the epic on the board at Backlog.
- [ ] W01: `make check-all` and the three-state verdict.
- [ ] W02: drift triage.
- [ ] W03 and W04, one pull request: restatement and its refusals.
- [ ] W05: the overlap table, then the user's review of it.
- [ ] W06: the approved removals and the layer rule.

## Decisions

| Decision | State |
| --- | --- |
| Order of work | Decided by the user: restatement, then the overlap audit. |
| Whether restatement may write a manifest's `bundles` entry | Decided by the user: names only. A run writing a different number of bundles than the manifest declares is refused. |
| Shape of the epic | Decided by the user: a new epic under I19, with the rows W12 to W15 of E00 moved into it and the overlap audit added. |
| What restatement writes | The expected bundles and the `bundles` entry. The earlier work item replaced the whole `[expected]` block, which also holds the exit status and diagnostics. |
| Restatement and its refusals | One pull request. The two rows change the same three files, and a restatement without its refusals is not safe to merge. |
| Lanes | None, as the initiative's existing epic uses none. |
| Epic priority | Decided by the user: 1, ahead of E00 at 2. |

## Row Moves

| E00 row | E01 row | E00 criteria | E01 criteria |
| --- | --- | --- | --- |
| W12 | W01 | AC20, AC21 | AC1, AC2 |
| W13 | W02 | AC14, AC15, AC16 | AC3, AC4, AC5 |
| W14 | W03 | AC17, AC18, AC19 | AC6, AC7, AC8 |
| W15 | W04 | AC22 | AC9, AC10, AC11 |
| W08 | W07 | AC9 | AC15 |

## I19 Review

Each remaining row of E00 read against `main` at b0eb7a233 on 2026-11-26.

| Row | Finding | Action |
| --- | --- | --- |
| W01, #158 | The indented-block reading is as the issue states it. Fencing the block is a workaround. | Kept. |
| W02, #160 | No check names an uncalled definition. The delivery wrapper its second criterion decides is absent from `src/prosiform`. | That criterion, E00 AC23, and the two bullets about the wrapper removed. |
| W04, #162 | An online link run resolves three issues and the project board, which the eval runbook cites. | Row ticked, issue closed with the run as evidence. |
| W06, #185 and W07, #186 | The design still states `crate`, one fixture still states `branches`, and the independence check reads neither rule. | Kept. |
| W08, #189 | The corpus runner takes `--awaiting` alone. | Moved to E01 as W07. |
| W09, #191 | No check reads a tag. The versioning policy is on `main`. | The bullet placing the policy in a planning record removed. |
| W10, #193 | The checks read tracked files, which the shared reading's own docstring states as its rule. | Kept. |

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [epic-e01.md](epic-e01.md) | Body of the epic, issue #858. |
| [epic-e00.md](epic-e00.md) | Body of the repository checks epic, issue #187, without the moved rows. |
| [initiative.md](initiative.md) | Body of the initiative, issue #770, with the new epic's row and criterion. |
| [w03.md](w03.md) | Work item: restatement that writes only the bundles. |
| [w04.md](w04.md) | Work item: restatement refuses what a reader decides. |
| [w05.md](w05.md) | Work item: command-line tests read against the corpus. |
| [w06.md](w06.md) | Work item: approved command-line tests removed. |

## Links

| Resource | URL |
| --- | --- |
| Epic I19 E01 | https://github.com/m2ux/prosiform/issues/858 |
| Epic I19 E00 | https://github.com/m2ux/prosiform/issues/187 |
| Initiative I19 | https://github.com/m2ux/prosiform/issues/770 |
| Task W01 | https://github.com/m2ux/prosiform/issues/255 |
| Task W02 | https://github.com/m2ux/prosiform/issues/243 |
| Board | https://github.com/users/m2ux/projects/18 |
