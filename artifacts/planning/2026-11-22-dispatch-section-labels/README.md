# Dispatch Sections and Graph Labels

## Executive Summary

Dispatch sections have plain names and retain marked hand-off links inside. A diagram dispatch label loses its mark precisely when the compiled destination is local; direct bundle links retain it.

The isolated implementation is dispatch-section-labels, based on main at bf42862ef3757c8f62b0b8522481d27c4518dd0d (0.33.0). The operator requested retrospective registration on 2026-11-22. [F34, issue #839](https://github.com/m2ux/prosiform/issues/839) targets main and stands In Progress on Python board 18. Its saved body passes Work Planner format checks; review and upstream delivery remain open.

## Tasks

- [x] Implement the heading and conditional label rule with focused regressions.
- [x] Align contract/fixtures and complete compiler checks.
- [x] Register retrospective hot-fix F34, issue #839, and verify In Progress on board 18.
- [ ] Compiler/design publication is held for explicit authorization; local review evidence is complete.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [proposed-hotfix.md](proposed-hotfix.md) | Saved body of registered F34, issue #839; compiler delivery remains open. |
| [validation.md](validation.md) | Compiler checks and review boundary. |

## Links

- [Canonical dispatch contract](../2026-10-17-prosiform-v1/design.md#link-classification-and-resource-handling)

## Local Candidate

Compiler commit 1ea933b7b213e2032f700b5bb18d5dd10b02b731 passes full make check. Its public branch and this engineering record remain unpublished: automatic approval review rejected the public engineering push because the destination and payload were not explicitly authorized. The installed released compiler remains unchanged.
