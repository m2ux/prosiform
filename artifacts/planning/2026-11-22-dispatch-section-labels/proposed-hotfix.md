## Overview

Generated dispatch sections should read as local navigation, with the dispatch mark identifying the bundle hand-off inside. This retrospective hot-fix records the implemented compiler candidate: plain generated headings and graph labels whose mark follows their compiled destination. The candidate passes local checks; review and upstream delivery remain open.

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

- [ ] **AC1.** Generated named-brief and Dispatch Pick headings have plain names, as compiler unit and corpus tests show.
- [ ] **AC2.** Contained bundle hand-off links retain their dispatch marks, as compiler unit and corpus tests show.
- [ ] **AC3.** A dispatched graph label loses its dispatch mark if and only if its compiled click targets a local section, as a mixed local/direct corpus fixture shows.
- [ ] **AC4.** Geometry, quoted text, Markdown strings, metadata, class labels and shared statement lines preserve content outside the permitted label and destination edits, as focused regression tests show.
- [ ] **AC5.** Every rewritten local reference reaches the corresponding plain section heading, as compiler and corpus tests show.
- [ ] **AC6.** A generated plain heading that collides with an authored heading is refused, as a compiler regression test shows.
- [ ] **AC7.** The canonical design, shipped documentation and corpus expectations agree on the display rule, as document review and repository guards show.
- [ ] **AC8.** The delivering revision passes `make check`.

## References

- **R1.** [Released dispatch behavior](https://github.com/m2ux/prosiform/blob/bf42862ef3757c8f62b0b8522481d27c4518dd0d/docs/dispatch.md) — The pf 0.33.0 baseline for briefs and dispatch picks.
- **R2.** Local implementation commit `1ea933b7b213e2032f700b5bb18d5dd10b02b731`, based on `bf42862ef3757c8f62b0b8522481d27c4518dd0d` — Unpublished compiler candidate; no delivering pull request exists yet.
- **R3.** Local validation at that candidate — Full `make check` passes: 2,303 compiler tests, 1,153 harness tests and 708 corpus fixtures, including 13 focused display regressions. Paired bundles preserve hand-off targets and model selections. This is compiler validation, not fresh native agent performance evidence. Criteria remain unticked pending delivery verification.
