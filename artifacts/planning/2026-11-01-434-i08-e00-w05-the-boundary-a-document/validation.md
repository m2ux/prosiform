# Validation

Evidence for each check the [work item](w05.md) names, run in the unit's worktree at b3ba2629 with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 unit tests

`make test` passes. The six `test_closure.py` boundary tests pass: no local path gives the document's own directory, the boundary is the common directory of every named path, a `../` link widens it, withheld links and diagram clicks count, every derived-from path sits inside it, and a path above the working directory contributes nothing (AC9, AC17).

## T2 file roots

The three `test_file_roots.py` tests pass: `../rules.md` compiled and rewritten to `#rules` (AC2), a replaced directory a link resolved through fails `E_SOURCE_CHANGED`, and a root-relative entry fails `E_SOURCE_OUTSIDE_ROOT` naming the invocation working directory.

## T3 corpus

`make corpus`: 385 fixtures pass, 0 fail. `inclusion/a-target-above-the-writing-directory-is-compiled` (AC2) and `inclusion/a-silent-target-above-is-text` pass; `make conformance` maps both to *File-owned invocation conformance cases — Target declarations*.

## T4 boundary

`make boundary`: 59 documents under `example/work-planner/`, each boundary printed, 0 links outside their boundary (AC9, AC17).

## T5 full check

`make check` exits 0 at b3ba2629 before opening; the epic base held no newer commit before merging, CI on b3ba2629 passes, and #500 merged into `i08/e00/main` as 137a060b.
