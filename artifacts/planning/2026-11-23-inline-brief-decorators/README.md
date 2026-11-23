# Inline Brief Decorators

> Prosiform Python · Created 2026-11-23

## Executive Summary

An inline call and a dispatched call use the same declared brief and the same generated call section. Their execution links select different destinations: a local section for inline execution and a separate bundle for a sub-agent. Plain links include their material without a brief decorator.

The goal is consistent authoring without manual Contract copies or wrapper prose. This record plans the compiler change against released pf 0.34.0; it does not implement it or authorize the next classifier board task.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Proposed hotfix](proposed-hotfix.md) | Problem, confirmed behavior and verifiable acceptance criteria |
| [Implementation plan](plan.md) | Compiler boundaries, sequence, invariants and regression matrix |
| [Released behavior specimen](specimen/result.json) | Actual outputs from five local pf 0.34.0 comparisons |
| [Specimen method](specimen-method.py) | Exact local comparison program |
| [Format check](format-check.txt) | Work Planner hotfix-body validation |
| [Publication](publication.json) | Saved issue equality, format result and Ready board readback |

## Progress

- [x] Confirm inline, dispatch and plain-link behavior with the user.
- [x] Verify released behavior and current compiler ownership.
- [x] Publish the validated issue and planning record; F36 is Ready on Project 18.
- [ ] Implement the planned compiler change after explicit continuation.

## Links

| Resource | Link |
| --- | --- |
| Source baseline | [pf 0.34.0 main](https://github.com/m2ux/prosiform/commit/61ddc5aa1) |
| Theme board | [Prosiform Python, Project 18](https://github.com/users/m2ux/projects/18) |
| Planned hotfix | [F36: Inline Briefs](https://github.com/m2ux/prosiform/issues/845) |
