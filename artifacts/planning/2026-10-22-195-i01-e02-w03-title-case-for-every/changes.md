# Change list

Every plan change this delivery session applied, and every one it held.

## Applied

| Kind | Subject | Change |
| --- | --- | --- |
| Epic creation | [#206](https://github.com/m2ux/prosiform/issues/206) · [I01:E05] Deferred Debt | The initiative's final epic, raised because its delivery deferred its first item and no epic of the initiative held that debt. [#187 \[I01:E03\]](https://github.com/m2ux/prosiform/issues/187) carries what the prototype initiative deferred, which is other debt |
| Task creation | [#207](https://github.com/m2ux/prosiform/issues/207) · [I01:E05:W01] | Generated-input detection under title-cased headings, placed as the first row of the new epic and depending on [E02](https://github.com/m2ux/prosiform/issues/195) |
| Folded work | [#20](https://github.com/m2ux/prosiform/issues/20) | The E05 row and criterion AC11, so the new epic's clear-up is covered by the initiative that carries it |
| Re-prioritisation | [#206](https://github.com/m2ux/prosiform/issues/206), [#207](https://github.com/m2ux/prosiform/issues/207) | Placed on the theme board at Backlog, with `priority: 4`, `tech-debt` and `theme:bundling` |

## Held

None.

## Debt this unit's validation found

| Item | Classification | Where it is fixed |
| --- | --- | --- |
| A bundle of a source root whose paths the filesystem spells in lower case opens on a title-cased file heading naming no path under that root, so offering it back as a source is not refused | Non-trivial — it blocks neither criterion this unit delivers, and deciding what the detection signal becomes warrants a work item of its own | [#207](https://github.com/m2ux/prosiform/issues/207), row W01 of [#206](https://github.com/m2ux/prosiform/issues/206) |

The epic in hand keeps the scope it was planned with: W03 delivered AC4 and AC5, and the deferred item sits in the initiative's clear-up epic rather than as a further row of the Merged Groups epic.

## Observed and not raised

The casing a word takes is written in `src/prosiform/bundle.py` as `title_cased` and spelled again inline in `titled` and `member_heading` in `src/prosiform/grouping.py`. The two sessions extending that file were running when this unit implemented, so no edit was made there; the duplication is two lines and warrants no work item of its own. It is recorded here for whoever next opens that file.
