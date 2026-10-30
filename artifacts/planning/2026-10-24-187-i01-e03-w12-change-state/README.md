# W12: Change State — October 2026

> Plan · Created 2026-10-24

## Executive Summary

`main` stayed red through six commits, and each commit reported a different failing target. The `links` failure was present at every one and was reached by none after the second. The pull request that broke it was never checked, because the workflow triggers on a branch naming pattern rather than on a pull request.

This record carries the planning for [W12](w12.md) under [E03 Carried Debt](https://github.com/m2ux/prosiform/issues/187). The work is raised as [#255](https://github.com/m2ux/prosiform/issues/255) and is kept open with the epic row linking it.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W12](w12.md) | The work item: problem, proposal and breakdown |

## Evidence

Read from the repository at `4c612b9`, the merge that restored `main`.

| Commit | Reported failing target | Actually failing |
| --- | --- | --- |
| `3d549a26` | `links` | `links` |
| `52851dd` | `corpus` | `corpus`, `links` |
| `c74d927` | `corpus` | `corpus`, `links` |
| `ee0aac0` | `corpus` | `corpus`, `links` |
| `16306e4` | `corpus` | `corpus`, `links` |
| `15c7805` | `test` | `test`, `harness`, `corpus`, `smoke`, `links` |

The first and last rows are measured: `make -k check` at `52851dd` reports `corpus` and `links`, and at `15c7805` reports `test`, `harness`, `corpus`, `smoke` and `links`. The middle three rows carry the `links` failure forward on the evidence that no commit between `3d549a26` and `52851dd` touched the worked examples, which is where both broken links sit; they were not each re-run.

`make -k check` reports five failing targets at `15c7805` where `make check` names one, and exits 0 with none on the restored tree.

| Merged pull request | Branch | CI ran |
| --- | --- | --- |
| #236, #235, #244, #212 | outside the naming pattern | no |
| The rest, 25 of 30 | `i01/e0*` | yes |

## Links

| Resource | Link |
| --- | --- |
| Issue | [#255](https://github.com/m2ux/prosiform/issues/255) |
| Epic | [E03 Carried Debt](https://github.com/m2ux/prosiform/issues/187) |
| Initiative | [Field Refinement](https://github.com/m2ux/prosiform/issues/20) |
| Retrospective | [Session retrospective](../../2026-10-24-session-retrospective/README.md) |
