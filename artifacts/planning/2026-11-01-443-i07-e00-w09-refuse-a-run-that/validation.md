# Validation — W09

> Evidence · Created 2026-11-01

## What was observed before the fix

Each case was written as a test and run on `i07/e00/w09-refuse-a-run-that` at `5bffb717`, before any source edit.

### AC21 — a set split across two messages passes

`dispatched` counted the members with `together` false and passed a set holding exactly one. `together` says only that a start shares a message with the start above it, which may be a start the scenario does not expect, so two records passed though each set reached two messages:

| Record | Members' `together` | Openers counted | Verdict before |
| --- | --- | --- | --- |
| opener, an unrelated start opening a second message, second member beside it | false, true | 1 | passed |
| an unrelated start, opener beside it, second member opening a second message | true, false | 1 | passed |

```text
FAILED evals/diagram-following/test_score.py::test_a_set_split_across_two_messages_is_sequential_set
E   AssertionError: second message opened by another start
E   assert (True, None) == (False, <Failure.SEQUENTIAL_SET: 'sequential_set'>)
```

### AC19 — a budget-stopped run of errored sessions reports completed

`outcome` returned `completed` whenever a session of the matrix was not started, so a run its budget stopped after three sessions that all reported the agent's limit tabulated as a completed run of `errored` failures. The test that shipped beside it, `test_a_run_the_budget_stopped_part_way_is_not_refused`, asserted that defect; it is replaced by the AC19 case.

```text
FAILED evals/diagram-following/test_run.py::test_a_run_the_budget_stopped_whose_sessions_all_errored_is_refused
E   AssertionError: assert 'completed' == 'refused'
```

### AC20 — a run that measured nothing writes a baseline

`main` refused `--write-baseline` only for a run whose state was `refused`. A completed run with no session record wrote a baseline of zero cells over the committed one:

```text
FAILED evals/diagram-following/test_report.py::test_a_run_that_measured_no_cell_writes_no_baseline
E   Failed: DID NOT RAISE CorpusError
```

## Failing case, before and after

Each repair was reverted alone, with the new tests in place, and the eval suite run:

| Repair reverted | Result |
| --- | --- |
| `score.py` (set check) | `test_a_set_split_across_two_messages_is_sequential_set` fails |
| `run.py` (refusal) | `test_a_run_the_budget_stopped_whose_sessions_all_errored_is_refused` fails |
| `report.py` (baseline write) | `test_a_run_that_measured_no_cell_writes_no_baseline` and `test_a_refused_run_writes_no_baseline` fail |

With every repair restored, all three pass, and the neighbouring cases hold: a set started in one message beside an unrelated start passes, a run with a genuine mix of errors and states stays completed, and a whole-matrix refusal keeps the agent's reason.

## Test runs

| Run | Where | Result |
| --- | --- | --- |
| The three new cases at `5bffb717`, before any source edit | worktree | 3 failed, as recorded above |
| Each repair reverted alone | worktree | its case fails, as tabled above |
| `pytest evals/diagram-following` after the repairs | worktree | all passed |
| `make check` at `1530aa80` | worktree | exit 0 |
| `make check` at `6015a8cc`, after merging `origin/i07/e00/main` | worktree | exit 0, see below |

### make check

Run as `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `6015a8cc`:

```text
206 files already formatted
Success: no issues found in 83 source files
step check: every procedure in 59 document(s) under example/work-planner/ writes its steps as sub-sections
authoring check: 0 finding(s)
1420 passed
1061 passed
corpus check: 374 fixture(s), 374 pass, 0 fail, 0 awaited, 0 unexpected pass
link check: every reference in 237 document(s) resolved
EXIT 0
```

## What was not proved here

- **The eval's own paid runs.** `make eval-diagrams` starts agent sessions against a real CLI and is not run by `make check`. Each case drives the runner through the stub agent, or the scorer and report over records laid out by hand, which is where each defect sat.
