## Overview

This retrospective hotfix records the implemented narrow pruning rule: empty, unreferenced generated wrappers are omitted with a warning. Authored sections and referenced document identities retain their structure and destinations. The implementation and validation precede this delivery record; review and merge remain open.

Target: `main`

## Problem

- **Generated wrappers can carry no information.**
  Grouped fragment selections can leave empty parent-folder and document-title scaffolding beside the useful selected sections.
- **An empty heading can be an address.**
  A grouped member can retain its document identity while its useful content sits under pooled sections. Removing that heading would break valid whole-document references.

## Proposal

- **Prune empty generated wrappers.**
  After composition and brief placement, omit unreferenced generated group, overview and preamble wrappers whose subtrees hold no body or retained structure. Preserve authored headings, required ancestors, addressed identities and dispatch/composition sections.
- **Warn for each omission.**
  Emit W_EMPTY_SECTION in bundle order, naming the heading and group and locating a contributing source title where available. Successful compilation exits zero.
- **Preserve reference identity.**
  Protect each pass's referenced headings and assign anchors over the retained outline. Included links retain their intended destinations; genuinely missing targets remain subject to normal resolution refusal.
- **Align the delivered contract and evidence.**
  The design, documentation, warning catalogue and corpus describe this boundary. The existing fixture sources retain their bytes; one expected empty generated heading is omitted with its expected warning. The standalone PR targets main independently of the separately tracked F34 display fix.

## Acceptance Criteria

- [ ] **AC1.** Empty unreferenced generated group, overview and preamble wrappers are omitted, as focused and corpus regressions show.
- [ ] **AC2.** Each omitted wrapper emits W_EMPTY_SECTION with its heading and source location where known, as diagnostic regressions show.
- [ ] **AC3.** Body content, meaningful descendants, code examples and containers retain their outline, as focused and existing compiler tests show.
- [ ] **AC4.** Retained links reach their intended destinations after heading ordinals are assigned, as candidate validation and corpus tests show.
- [ ] **AC5.** Authored empty anchors and referenced generated document identities remain addressable through inline, reference-style and diagram links, as focused regressions show.
- [ ] **AC6.** Dispatch positions and composition identities remain valid after pruning, as position-map, dispatch and composition regressions show.
- [ ] **AC7.** The design, documentation, warning catalogue and corpus agree on the narrow pruning rule, as repository guards show.
- [ ] **AC8.** The standalone delivering revision passes make check.

## References

- **R1.** [Released Hierarchy Rules](https://github.com/m2ux/prosiform/blob/bf42862ef3757c8f62b0b8522481d27c4518dd0d/docs/hierarchy.md) — the grouping and preamble behavior the defect affects.
- **R2.** [F34: Dispatch Display](https://github.com/m2ux/prosiform/issues/839) — the separately tracked display correction; this hotfix owns wrapper pruning and warnings.
- **R3.** [Retrospective F35 Validation](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-22-840-f35-empty-sections/README.md) — the implemented standalone revision, scope decision and compiler evidence. Criteria remain unticked pending delivery verification.
