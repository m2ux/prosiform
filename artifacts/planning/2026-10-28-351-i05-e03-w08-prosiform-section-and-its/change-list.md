# I05:E03:W08 Change List

The plan changes this delivery session made, and those it held.

## Applied

- **Folded work, I05:E03 W08.** `## Dispatch` is present whenever the bundle uses either operator, because a parallel dispatch is dispatch done together and the Parallel dispatch protocol links Dispatch; `## Parallel dispatch` is present only when the bundle uses `⫽`; a bundle using neither has no Prosiform section. AC16 on #351 is reworded to state it, and the design's The Prosiform section clause and the epic design record state it.
- **Folded work, I05:E03 W08.** Wherever pf emits `## Dispatch` or `## Parallel dispatch`, an authored heading of that text in the bundle is refused with `E_HEADING_COLLISION`, as `Prosiform` and `Dispatch in parallel` are. The design's Generated heading collisions clause states it.
- **Folded work, I05:E03 W08.** The section's levels are fixed at `#` and `##`, so each protocol is the same bytes in every bundle (AC17). It is the bundle's first heading: ahead of a file heading, and, for an entry or titled entry member opening on content above its title, after that content and ahead of the dispatch sub-section the content takes.
- **Folded work, I05:E03 W08.** The parallel protocol link sits in the set's instruction paragraph, ahead of its list: "Dispatch these bundles together, each to a sub-agent, as [Parallel dispatch](#parallel-dispatch) states:".
- **Folded work, I05:E03 W08.** The section is emitted by the sub-section placement in `src/prosiform/dispatch.py`, beside the instruction texts it serves; `src/prosiform/bundle.py` gains `Group.filed`, which the coincident-heading warning reads once a wrapped first group carries its file heading as a part. The work item keeps `bundle.py` as its declared component.
- **Folded work, I05:E03 W08.** Candidate validation holds each link an instruction carries to a Prosiform protocol heading (`target integrity`).
- **Folded work, I05:E03 W08.** The glossary defines `Prosiform section`, which the design marks as a contract term, so `make vocabulary` holds; W09's documentation sweep keeps the rest of the docs.
- **Folded work, I05:E03 W08.** A `fixtures/prosiform` family of eight fixtures, and a `Prosiform section` adversarial clause in the design naming it. Design pinned at `429eaf81`.

## Held

None.

## Deferred debt and arising issues

- **Deferred debt.** None.
- **Arising.** None. The example corpus's `bootstrap.md` symbol rows for `⇉` and `⫽`, and the run-set wording in `guidelines.md` and `rules.md`, are W09's planned documentation sweep.
