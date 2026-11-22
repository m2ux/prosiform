# Dispatch Sections and Graph Labels

## Executive Summary

Dispatch sections have plain names and retain marked hand-off links inside. A diagram dispatch label loses its mark precisely when the compiled destination is local; direct bundle links retain it.

The isolated implementation is dispatch-section-labels, based on main at bf42862ef3757c8f62b0b8522481d27c4518dd0d (0.33.0). Registration as proposed hot-fix F34 is held for the operator under Work Planner's Plan Change rule; implementation and review preparation are authorized by the requested compiler change.

## Tasks

- [x] Implement the heading and conditional label rule with focused regressions.
- [ ] **In progress:** Align contract/fixtures and complete compiler checks.
- [ ] Publish the compiler change and review evidence.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [proposed-hotfix.md](proposed-hotfix.md) | Concrete issue draft for a possible F34 registration; not published to the tracker. |
| [validation.md](validation.md) | Compiler checks and review boundary. |

## Links

- [Canonical dispatch contract](../2026-10-17-prosiform-v1/design.md#link-classification-and-resource-handling)
