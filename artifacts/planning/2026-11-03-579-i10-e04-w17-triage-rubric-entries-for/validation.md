# Validation — I10:E04 W17

Every check ran in the unit's worktree, at the task branch's head, with the build `make harness` uses; no paid agent session ran. The revision is the head the pull request carries when its Test Plan is recorded.

| Item | Value |
| --- | --- |
| Branch | `i10/e04/w17-triage-rubric-entries-for` |
| Tested revision | `e226cd60` |
| Command | `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` |

## Checks

### T1 The rubric decides every class the scorer gives

`make harness`, `test_runbook.py`: `test_the_rubric_decides_every_class_the_scorer_gives` reads the class names of the By Class table's rows and finds them equal to `score.Failure`'s values: `uncompiled`, `overcompiled` and `misordered_compile` present, `unbootstrapped` absent. On the epic base after it took `main` (`1678d4d3`), before this change, the test failed with `unbootstrapped` extra and the three run classes missing. Passed.

### T2 make check

The whole repository check, at the tested revision, exits 0; `make harness` runs 1461 tests. Passed.

## Findings

- **The epic base failed the rubric test once it took `main`.**
  Merging `main` into `i10/e04/main` brought `RUNBOOK.md` and its test beside W03's classes and W05's retirement, so the base's CI failed on T1 alone until this change merged.
