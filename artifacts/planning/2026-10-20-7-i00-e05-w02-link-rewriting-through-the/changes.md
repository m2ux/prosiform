# Changes

Every change this row applied under its allowance, and every change it held.

## Applied — Contract Change

| Change | Where | Why the implementation needed it |
| --- | --- | --- |
| The order several entries are named in | `design.md`, `Bundle destinations — Entry line`, a new `Order` bullet | The design stated the line and not its order, so a second implementation reading it would name entries in command-line order and reach other bytes. The order is bundle order, which is what the two determinism fixtures already pin |
| The separator the mark carries | `design.md`, `Link classification and resource handling — The mark` | `[¬ the rules]` rewritten by the stated rule alone carries a leading space into the published text. The spaces or tabs between the mark and the text go with the mark; a line break does not, because dropping one would join two lines the source kept apart |
| What `Internal links` rewrites | `design.md`, `Bundle destinations — Internal links` | The bullet said each cross-file and fragment-only link is rewritten, which contradicts `Unmarked local Markdown links` in the same document and the decision resting on it. It now says a marked link, and names the classification rules that place the rest |

## Applied — Folded Work

| Change | Why it belongs here |
| --- | --- |
| The destination a file heading holds for the source heading it absorbed | A lookup without it faults on a reference the run already resolved, so the map answers one. It is `AC8`'s behaviour and `W04`'s row, and nothing is ticked for it here |
| A heading carrying a marked link | The rewrite drops the mark from a heading's own text, so the slug the renderer generates comes from the text the bundle emits. Leaving it would have put a destination in the map that names no heading of the published document, which the run now refuses |

## Held — Reported, Not Applied

| Held | Why |
| --- | --- |
| Refusing a marked image with `E_MARKED_RESOURCE` | `required` reads links and an image is not one. The fix changes what the traversal classifies rather than what the rewrite emits, which is another row's surface. Declared as a fixture awaiting `I00:E11` and raised as [#87](https://github.com/m2ux/prosiform/issues/87), placed as `I00:E11:W08`.|
| Converting a marked reference-style link to inline form | `I00:E05:W03` delivers the conversion. Until it lands the run raises an internal error rather than publishing a bundle naming a source path. Declared as a fixture awaiting that row |
| Recording in `design.md` which part of the entry line landed in which row | `w02.md` proposed it. The design states the system as it is, and a delivery order is not part of the system; it is recorded here instead |

## Applied — Task Creation

`I00:E11:W08` and the criterion it covers, `AC9`, were added to [#39](https://github.com/m2ux/prosiform/issues/39) as the placement of [#87](https://github.com/m2ux/prosiform/issues/87). The epic's reference list gains `R8` naming the gap. Nothing was renumbered: the list already carries two entries labelled `R6`, and a number a pull request names is preserved.

No row was created in `I00:E05`, none migrated, nothing re-prioritised, and nothing outside the allowance was needed.
