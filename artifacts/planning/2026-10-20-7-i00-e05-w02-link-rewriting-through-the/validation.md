# Validation

What this row measured on its base, what it chose where the base left a choice, and what turned out to be stated wrongly.

## The Structural Problem and the Choice Made

A destination belongs to the bundle rather than to a group, so the map is known only once every group exists. Emission is line-based: a group is assembled from the physical lines its source wrote, and a link destination is an inline span inside one of those lines.

The groups are therefore built twice. The first pass learns the headings the bundle emits; `fragments` over that sequence is the destination map; the second pass builds the same groups again with the map in hand and rewrites each marked link as it slices the lines. The second pass emits the headings the first did, because a rewrite edits a link's destination and its mark and nothing a heading is slugged from — the one exception, a heading carrying a marked link, is held by deriving a group's heading text with the mark already dropped, so both passes see the text the bundle will emit.

The alternative was to rewrite the assembled bundle text. It was refused because the assembled text no longer says which bytes are a fenced example and which are inline content, and the contract turns on exactly that distinction.

A rewrite is located rather than re-rendered. `rewrite.py` scans the physical lines one inline token occupies, masks the code spans the profile reads, passes over an image, and edits two spans of one link: the mark and the destination. Everything else is the bytes the source wrote, including a title the link carries. The scan is cross-checked against the parser — the sites it finds are counted against the marked links the parser read from the same token — so a link the run resolved and the emission cannot edit is an internal fault rather than a bundle.

## The Invariant Validated in the Run

`resolving` reparses the completed candidate and compares the fragment a renderer generates for each heading it finds with the destination the map assigned that heading. Every rewritten link and every entry-line link names one of those destinations by construction, so an agreement is each of them resolving to exactly one heading of the bundle. A disagreement raises before anything is published.

## What Turned Out Wrong

| Stated | Measured |
| --- | --- |
| `fixtures/citation/an-unmarked-reference-above-the-root` has a marked link naming a target above the allowed root, and whether it rewrites is a contract question | Its link above the root is the *unmarked* one, which is emitted as authored and resolves to nothing; its marked link names `rules.md` inside the root and rewrites. The contract question does not arise. `fixtures/citation/marking-a-reference-above-the-root` is the fixture where a mark names a target above the root, and it already fails with `E_SOURCE_OUTSIDE_ROOT` |
| AC6 includes a grouped entry resolving to its overview subsection | Grouping arranges nothing in the build: `compose` emits one group per source and never reads the rules it validated. The overview subsection is `I00:E09:AC4`, and `I00:E09:AC6` carries the merged-heading references. AC6's own text names neither |
| `make check` is `lock-check lint format-check typecheck test corpus layout tables links vocabulary` | It also runs `harness`, the checks' own tests, between `test` and `corpus` |
| The catalogue carries 23 codes | 23 error codes and two warning codes, 25 in all. No code was added here |
| Each local Markdown link in selected content is rewritten (AC3, and the design's `Internal links`) | Only a marked one is. `Link classification and resource handling — Unmarked local Markdown links` states that an unmarked link is not rewritten even where the bundle carries its target, and D33 rests on it. The design's `Internal links` bullet is corrected to say so |

The measurements the brief got right: the destination map arrives after the groups are assembled at `cli.py:939`; emission is line-based; 130 fixtures, 127 passing, three awaiting; 17 expected bundles carry the mark, over 30 occurrences on 29 lines.

## The Marks, Decided One by One

28 of the 30 occurrences were links the rewrite reaches, and each lost its mark. The two that survive are in `traversal/a-marked-link-in-a-code-example`: one inside a code span and one inside a fenced block, which are text the bundle carries as written. Every one of the 17 bundles changed.

One of the 17, `ancestor-promotion/a-link-to-a-heading-only-ancestor`, awaits `I00:E09:W02`. Its expected bundle was edited by hand rather than regenerated, so it still declares the structural ancestor the build does not emit yet and still awaits that work.

## Held

- **A marked image is accepted.** `![¬ the architecture](plan.png)` reaches the bundle with its mark intact. `required` reads links and an image is not one, so `E_MARKED_RESOURCE` never fires, and D32's invariant that a mark never reaches a reader is broken by it. Declared as `rewriting/marking-an-image`, awaiting `I00:E10`, and raised as an issue.
- **A marked reference-style link cannot be rewritten.** The parser resolves one and the source carries no inline destination to edit, so the run raises an internal error rather than publishing a bundle naming a source path. The conversion to inline form is `I00:E05:W03`, and the finished behaviour is declared as `rewriting/a-marked-reference-style-link`, awaiting it.
- **A reference naming an absorbed title.** The map answers one, because a file heading that absorbed a source heading holds that heading's fragment in its place and a lookup without it would fault. That is `AC8`, which is `W04`'s, and nothing is ticked for it here.
