## Overview

Compiled Mermaid nodes should describe the work at their published destination. When an inline target is already included in the current bundle, its node label must lose the consumed inline operator, just as a Markdown inline link does. The remaining local link is followed under the workflow's graph-reading rules.

Target: `main`

## Problem

- pf 0.36.0 retains `↳` on Mermaid labels whose targets have already become local sections. Its guide interprets that operator as an instruction to bundle the destination, so an agent can try to compile an emitted bundle rather than follow the included graph.
- Markdown publication already removes the consumed operator. Mermaid publication handles local dispatch labels but omits inline labels, including candidate comparison.

## Proposal

- **Publish labels for their resolved destinations.**
  Apply the existing consumed-operator rule to Mermaid nodes targeting included local sections in emission and candidate validation.
- **Preserve real dispatch instructions.**
  Keep dispatch operators on links to worker bundle files; leave unrecognised literal text intact.
- **Exercise public synthetic examples.**
  Cover ordinary and metadata labels, same-line click offsets, candidate validation and existing dispatch behavior without application fixtures.
- **Declare Python build 0.37.0.**
  The user requests a version bump. Changed emitted bytes move the pre-1.0 contract minor under the repository's versioning rules; run the previous tagged corpus against this build and retain the differences.

## Acceptance Criteria

- [ ] **AC1.** Mermaid inline nodes targeting included local sections publish plain labels and valid anchors, including metadata labels and click offsets, verified by focused source regressions and generic corpus fixtures.
- [ ] **AC2.** Candidate validation accepts the correctly published local labels and rejects incorrect label changes, while real worker-bundle dispatch labels retain their operators, verified by candidate and dispatch regressions.
- [ ] **AC3.** The change has a current exact-head review and passes the repository's required compiler checks, with results linked from its delivering pull request.
- [ ] **AC4.** The package and lockfile declare 0.37.0, its installed command reports that version, and a previous-tag corpus comparison records the version choice, verified by lock, installation and corpus checks.

## References

- **R1.** [Prosiform composition](https://github.com/m2ux/prosiform/blob/main/docs/composition.md) — Inline composition and publication semantics.
