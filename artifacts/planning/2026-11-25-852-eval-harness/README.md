# Eval Harness

## Executive Summary

`make eval-harness` passes: the walk reads each deferred line from the form's root, the brief tests find a brief's sub-section by the dispatch's plain name, and the guide tests hold a bare `pf` run to the build's own guide text. Three merged changes had left 39 tests failing on `main`, none of which `make check` runs.

[Issue #852](https://github.com/m2ux/prosiform/issues/852) holds the work. It is delivered on `852-eval-harness`, cut from `main` at 6f103e34d, with one commit per cause, at head e298a4604b00c4dbcfe620666139ac5c11d39979. [test-results.md](test-results.md) records the validation and the change each cluster started failing at.

Delivery found a live defect from the same cause: a live session cannot bundle a deferred line its bundle set carries. At the user's direction it is raised as [F40, issue #853](https://github.com/m2ux/prosiform/issues/853), stating the defect and the outcome and leaving the approach open, and this delivery does not change the runner, the instruction or the harnesses.

## Commits

| Commit | Cluster | Holds |
| --- | --- | --- |
| 99199a9ee | Deferred-line walks | `rooted` in `workflow.py` reads a bundle's `↳` lines from the form's root wherever the walk reads a bundle, and the tests reading a bundle's text directly read it the same way. |
| ee03dd60d | Brief sections | The brief tests select the sub-section headed by the dispatch's text and hold the dispatch line inside it to its mark. |
| e298a4604 | Guide opening | The guide tests compare a bare run's output with `prosiform.cli.GUIDE`. |

## Tasks

- [x] Reproduce the 39 failures on `main`.
- [x] Name the change each cluster started failing at.
- [x] Repair each cluster in its own commit.
- [x] Run `make eval-harness` and `make check`.
- [x] Raise the live-session defect as F40, issue #853.
- [x] Open the pull request to `main` and link it to #852 through Development.
- [ ] Review, merge, confirm `make eval-harness` on `main`, and close #852.

## Open Decisions

| Decision | State |
| --- | --- |
| Whether the eval harness runs in CI | Decided by the user: it stays a manual target, outside CI. |

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [issue.md](issue.md) | Body of issue #852, with its acceptance criteria. |
| [pull-request.md](pull-request.md) | Body of the delivering pull request. |
| [test-results.md](test-results.md) | The validation at the head and the failing clusters. |
| [hotfix-live-deferrals.md](hotfix-live-deferrals.md) | Body of F40, issue #853. |
