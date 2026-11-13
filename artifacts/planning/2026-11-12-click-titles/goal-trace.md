# Goal Trace

## Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| A click's quoted tooltip is read as its link's title | AC1 | E00 | E00 AC2, AC3, AC5 | Goal; Defaults Taken 1, 2 and 4 |
| `"⇉"` bundles as a dispatch and `"¬"` as a deferral | AC1 | E00 | E00 AC2, AC4, AC5 | Goal; Defaults Taken 3 and 5 |
| Both `click N href "d" "t"` and `click N "d" "t"` are covered | AC1 | E00 | E00 AC2 | Goal |
| Diagram links documentation states it | AC2 | E00 | E00 AC1, AC6 | Goal; Defaults Taken 6 |
| `pf` takes a published link as written, with `--pick` | AC4 | E01 | E01 AC1 to AC7 | #747; Link Invocation 1 to 3 |
| A release follows under the project's tagging | AC3 | E02 | E02 AC1, AC2, AC3 | Confirmed 3 |

The marked sources are the record's [decisions](decisions.md) and [Cutting a release](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/versioning.md#cutting-a-release).

## Gaps

Ranked; the flagged ones most threaten the goal.

1. **Resolved: the tooltip carries operator and tags.** The goal reads the tooltip "as a link title", but a Markdown link's operator sits in its text, not its title; Defaults Taken 1 reads both from the tooltip, confirmed by the user.
2. **Flagged: the build alone turns the corpus red.** The retired fixture fails once the build reads tooltips; Defaults Taken 8 joins the build and fixture rows.
3. **Resolved.** The release cannot sit inside the feature epic, whose merge it waits on; Defaults Taken 7 gives it its own epic.
4. **Noted: existing descriptive tooltips.** A tooltip of plain words is read as tags; unknown tags are ignored, so the bytes of every existing click fixture stand, except on a document declaring alternatives, which a diagram link alone could not reach before either.

## Outside Threats

- **Readers of the changed surface.** `bundle.py`'s destination rewriting, candidate validation and the link budget each read `clicks`; W01 routes all of them through one split.
- **Fail-closed paths.** An operator on a click naming no declaring document is refused as on a link, so a tooltip mark never ships as a silent ordinary link.
- **Instrument independence.** The corpus fixtures, not the unit tests, carry AC1, and the previous contract tag's corpus chooses the release number.
- **Ground shift.** I15's E00 and E01, which edited `docs/references.md`, `docs/glossary.md` and `docs/selection.md`, have merged to `main`; its open E02 and I16 change the eval, whose harness E01 W03 also changes, so whichever lands second merges the other's `evals/diagram-following` invocations.

## Checks

- Format: the initiative and both epic drafts report nothing to fix, apply or decide.
- Dependencies: no problems, no open candidate unit, no cross-epic contention; longest chain four steps, E00 W00 through E00 W03 to E01 W01. The check proposes E00 2, E01 1, applied as the epics' priority labels.
- Dependencies after the Link Invocation hoist, 2026-11-13: no problems; longest chain four steps, E01 W00 through E01 W04 to E02 W01; E00 and E01 `priority: 2`, E02 `priority: 1`.
- Dependencies at alignment, 2026-11-13, with E01's work items from its task records: no problems; longest chains five steps, each through E00 W00, E01 W04 and E02 W01; contending pairs E00 W00 and E01 W00 on the v1 design, E00 W01 and E01 W01 on `source.py` and `test_cli.py`, E00 W03 and E01 W04 on `references.md`, `glossary.md` and `selection.md`, each ordered by a dependency edge.
- Dependencies after the alignment decisions, 2026-11-13, with E02 W00 added: one problem, the initiative's E02 row naming E00 and E01 while E02 W00 needs neither; longest chains unchanged at five steps.
- Dependencies after the initiative's E02 row named no epic, 2026-11-13: no problems; longest chains five steps, each through E00 W00, E01 W04 and E02 W01.
