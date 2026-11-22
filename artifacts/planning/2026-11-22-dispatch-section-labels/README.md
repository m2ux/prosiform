# Dispatch Sections and Graph Labels

## Executive Summary

Dispatch sections have plain names and retain marked hand-off links inside. A diagram dispatch label loses its mark precisely when the compiled destination is local; direct bundle links retain it.

The isolated delivery branch is f34-dispatch-display, based on main at bf42862ef3757c8f62b0b8522481d27c4518dd0d (0.33.0). The operator requested retrospective registration on 2026-11-22. [F34, issue #839](https://github.com/m2ux/prosiform/issues/839) targets main and stands In Progress on Python board 18. Its saved body passes Work Planner format checks. The delivering PR has merged; issue delivery synchronization remains separate.

## Tasks

- [x] Implement the heading and conditional label rule with focused regressions.
- [x] Align contract/fixtures and complete compiler checks.
- [x] Register retrospective hot-fix F34, issue #839, and verify In Progress on board 18.
- [x] Revalidate the exact standalone PR head and prepare retrospective publication.
- [x] Register the draft delivering PR and its verified Development link.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [proposed-hotfix.md](proposed-hotfix.md) | Saved body of registered F34, issue #839; compiler delivery remains open. |
| [validation.md](validation.md) | Compiler checks and review boundary. |

## Links

- [Canonical dispatch contract](../2026-10-17-prosiform-v1/design.md#link-classification-and-resource-handling)

## Local Candidate

Compiler commit 1ea933b7b213e2032f700b5bb18d5dd10b02b731 passes a fresh full make check on f34-dispatch-display, based on main. The operator explicitly requests retrospective Prosiform PR publication. The source, public contract and validation record are published. [PR #841](https://github.com/m2ux/prosiform/pull/841) targets main and is linked to #839 through Development. CI passes at the recorded head. GitHub confirms merge e2dde5e569800e5584797bb194bb989f8fb2843b at 2026-11-22T09:42:27Z; the [readback](merge-readback.json) records it. No issue closure is asserted by this publication receipt.
