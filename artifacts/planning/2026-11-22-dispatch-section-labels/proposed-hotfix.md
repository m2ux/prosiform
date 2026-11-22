## Overview

Generated dispatch sections should read as local navigation, with the dispatch mark identifying the bundle hand-off inside. This retrospective hot-fix records the implemented compiler candidate: plain generated headings and graph labels whose mark follows their compiled destination. The correction is delivered on main; fresh checks at the exact merge revision verify all eight criteria.

Target: `main`

## Problem

- **A local section looks like a dispatch.**
  The [released brief rules](https://github.com/m2ux/prosiform/blob/bf42862ef3757c8f62b0b8522481d27c4518dd0d/docs/dispatch.md#briefs) generate a marked section heading and a marked hand-off link beneath it. A graph node keeps the mark when its click opens that local section, giving two different operations the same visual cue.
- **A direct bundle click is a hand-off.**
  Removing the mark from every graph label would hide the distinction between navigating to local instructions and opening a dispatch bundle.

## Proposal

- **Name generated sections plainly.**
  Named brief sections and Dispatch Pick sections have plain headings. Their contained hand-off links retain their dispatch marks.
- **Render graph labels by destination.**
  Remove the dispatch mark exactly when the compiled click targets a local section. Preserve the mark on direct bundle destinations.
- **Validate the permitted edits.**
  Rewrite local anchors consistently, preserve source content outside the permitted display edits, and reject collisions with plain generated headings. Align the design, documentation and corpus expectations.

## Acceptance Criteria

- [x] **AC1.** Generated named-brief and Dispatch Pick headings have plain names, as compiler unit and corpus tests show.
- [x] **AC2.** Contained bundle hand-off links retain their dispatch marks, as compiler unit and corpus tests show.
- [x] **AC3.** A dispatched graph label loses its dispatch mark if and only if its compiled click targets a local section, as a mixed local/direct corpus fixture shows.
- [x] **AC4.** Geometry, quoted text, Markdown strings, metadata, class labels and shared statement lines preserve content outside the permitted label and destination edits, as focused regression tests show.
- [x] **AC5.** Every rewritten local reference reaches the corresponding plain section heading, as compiler and corpus tests show.
- [x] **AC6.** A generated plain heading that collides with an authored heading is refused, as a compiler regression test shows.
- [x] **AC7.** The canonical design, shipped documentation and corpus expectations agree on the display rule, as document review and repository guards show.
- [x] **AC8.** The delivering revision passes `make check`.

## References

- **R1.** [Released dispatch behavior](https://github.com/m2ux/prosiform/blob/bf42862ef3757c8f62b0b8522481d27c4518dd0d/docs/dispatch.md) — The pf 0.33.0 baseline for briefs and dispatch picks.
- **R2.** [Implemented F34 Revision](https://github.com/m2ux/prosiform/commit/1ea933b7b213e2032f700b5bb18d5dd10b02b731) — The retrospectively registered implementation, based on main at bf42862ef.
- **R3.** [Retrospective Validation](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-22-dispatch-section-labels/validation.md) — Full `make check` passes: 2,303 compiler tests, 1,153 harness tests and 708 corpus fixtures, including 13 focused display regressions. Paired bundles preserve hand-off targets and model selections. This is compiler validation, not fresh native agent performance evidence. The merged-revision verification below confirms AC1–AC8.
- **R4.** [Merged Revision Verification](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-22-dispatch-section-labels/validation.md#merged-revision) — AC1–AC8 verified by fresh full checks at e2dde5e569800e5584797bb194bb989f8fb2843b; exact log and criterion mapping.
