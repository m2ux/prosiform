## Overview

`make eval-harness` fails on `main`. The suite is the eval's own apparatus and `make check` never runs it, so the failures reach no pull request's CI. This issue asks for the suite to pass on `main`, so a change to the eval can be held to it.

## Problem

- **The suite is red on `main`.**
  At 684437c06 it reports 819 passed and 39 failed. The bundler vocabulary branch reports the same count, and the same tests once their names are read in the new vocabulary.
- **The failures cluster in the bundle-set walks.**
  Most are the corpus tests that bundle a workflow's bundle-set form and walk its deferred lines, dispatches and picks. Several report `E_TARGET_NOT_FOUND` for an entry reference that climbs from the test's output folder back to the workflow's sources, where the test expects a destination relative to those sources.
- **A red suite cannot serve as an instrument.**
  F39's criterion on the eval's names named this suite as its proof and was reworded to a search and the passing tests.

## Proposal

- **Find the change that broke each cluster.**
  Run the suite at each release tag back from `main` to the last one that passes, and name the feature each cluster started failing at.
- **Repair the test or the eval, whichever is stale.**
  Where the build's behaviour is the contract's, the test's expectation or the eval's walk follows it; where it is not, the build is the defect and takes a hot-fix of its own.
- **Keep it green.**
  Decide whether the suite runs in CI on changes under `evals/`, so it cannot go red unseen.

## Acceptance Criteria

- [ ] **AC1.** `make eval-harness` passes on `main`, as its output shows.
- [x] **AC2.** Each failing cluster names the change it started failing at, as the planning record shows.

## References

- **R1.** [F39 test results](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-850-f39-bundler-vocabulary/test-results.md#eval-harness) — The counts observed on `main` at 684437c06 and on the bundler vocabulary branch.
- **R2.** [Failing clusters](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-852-eval-harness/test-results.md#failing-clusters) — Each cluster, the merge it started failing at, and its cause.
