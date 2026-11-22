## Overview

Generated dispatch sections identify local navigation with plain names. Dispatch marks remain on hand-off links and on diagram labels that open bundle files, so the compiled graph distinguishes navigation from delegation.

Target: `main`

## Problem

- **A local section looks like another dispatch.** A briefed dispatch generates a heading such as `⇉ Investigate` and a marked hand-off link beneath it. Its graph node keeps the same mark even though its click opens that local section.
- **The destination determines the operation.** A direct bundle click remains a hand-off; its label must retain the dispatch mark.

## Proposal

- **Name generated sections plainly.** Named brief sections and Dispatch Pick sections carry plain headings, with the marked bundle hand-off links inside.
- **Publish graph labels by destination.** Remove the mark from a node or class label exactly when its dispatch click compiles to a local section. Preserve direct-bundle labels.
- **Preserve integrity checks.** Rewrite matching anchors and compare the allowed label edits during candidate validation. Plain heading collisions remain errors.

## Acceptance Criteria

- [ ] **AC1.** Generated brief and pick sections have plain headings and marked contained hand-off links, as compiler unit and corpus tests show.
- [ ] **AC2.** Diagram labels lose their dispatch mark if and only if the compiled dispatch target is local, as a mixed local/direct acceptance fixture shows.
- [ ] **AC3.** Class labels, geometry, quoted text, Markdown strings, metadata and shared statement lines preserve their destinations and other content, as focused regression tests show.
- [ ] **AC4.** Plain generated heading collisions are refused and rewritten references reach the plain section names, as compiler tests show.
- [ ] **AC5.** The design, shipped documentation and corpus expectations state this behavior, as make check verifies.
- [ ] **AC6.** The classifier's 52 harness/seam selections compile with the candidate compiler and preserve dispatch model/target maps, as source-bound integration evidence shows.

## References

- **R1.** [Released dispatch behavior](https://github.com/m2ux/prosiform/blob/bf42862ef3757c8f62b0b8522481d27c4518dd0d/docs/dispatch.md#briefs) — baseline heading and dispatch-brief rules.
