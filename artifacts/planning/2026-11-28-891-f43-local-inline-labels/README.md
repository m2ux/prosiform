# F43: Local Inline Labels — November 2026

> Compiler hot-fix · Created 2026-11-28

## Executive Summary

F43 makes Mermaid node labels follow the existing publication rule for consumed inline operators. A node whose target is included in the same bundle has a plain label and local link. The workflow's graph-reading instructions govern following that link; an included phase stays in its caller's context.

Emission and candidate validation cover the same publication shape. Synthetic fixtures exercise quoted labels, metadata scalars, same-line click offsets, deferred inline content and real worker-file dispatches. Application sources and native trials are outside this unit.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Issue body](issue-body.md) | Scope and acceptance criteria |
| [Todos](todos.md) | Delivery sequence and verification hold |
| [Specimens](specimens/README.md) | Source, before/after bundles and receipts |
| [Released compiler corpus result](before-corpus.log) | Three reproductions fail; real dispatch passes |
| [Original candidate result](before-candidate.log) | Failing focused regressions before implementation |
| [Corrected focused corpus](focused-corpus.log) | Four synthetic fixtures pass |
| [Corrected candidate checks](focused-candidate.log) | Four focused candidate checks pass |
| [Final required checks](make-check.log) | Complete passing compiler checks at the declared 0.37.0 head |
| [Pre-version host checks](pre-version-check.log) | Runtime checks pass; final vocabulary guard identifies one description word |
| [Vocabulary correction](independence.log) | Corrected description passes independence |
| [Previous corpus](previous-corpus.log) | 708 passes and two expected output differences against tagged 0.36.0 |
| [Version validation](version-validation.log) | Installed wheel and lockfile report 0.37.0 |
| [Verification](verification.md) | Scope, attempts, version choice and final check results |
| [Agent review](agent-review.json) | Exact-head review with no findings |
| [Delivery readback](delivery-readback.json) | Ready PR, green CI, four checked criteria and In Review board status |
| [Sandbox attempt](sandbox-attempt.log) | Network-isolated wheel installation cannot resolve hatchling; 2101 tests pass before setup errors |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix | [#891](https://github.com/m2ux/prosiform/issues/891) |
| Pull request | [#892](https://github.com/m2ux/prosiform/pull/892) |

Branch f43-local-inline-labels targets main at 8cedda4cc06b0486168addc05f057161192a22a6. Required compiler checks pass at bb0c444c781816d777911f40d14945d737ac05d1; its exact-head review records no findings. The package declares 0.37.0; merge and release tags remain outstanding. The classifier's full suites and native trials remain held.

PR #892 is ready for review with green CI. Issue #891 remains open, all four criteria are checked, and Python board 18 records In Review. Merge and release tags are outstanding.
