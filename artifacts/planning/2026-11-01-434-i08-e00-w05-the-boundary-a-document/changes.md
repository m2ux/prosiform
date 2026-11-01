# Plan Changes

- **Design decision, applied** — A positional entry above the working directory keeps bounded bootstrap capture. The epic plan's `a-w05.md` proposed refusing it with `E_SOURCE_OUTSIDE_ROOT`; the pinned design's *Bounded bootstrap capture* and resolution table authorize it and `confinement/a-parent-segment-above-the-root` holds it, so `fixtures/confinement/an-entry-above-the-working-directory` is not added.
- **Design decision, applied** — The boundary is a function (`closure.boundary`) rather than a `Source` field: no stage of the run reads it, and `Capture.directories` already records every directory a link's walk crosses for the recheck.
- **Observation, held** — Corpus manifest descriptions and fixture prose still say "allowed source root" (about 25 files). [W07](https://github.com/m2ux/prosiform/issues/434) rewrites the corpus families and is the place for it.
