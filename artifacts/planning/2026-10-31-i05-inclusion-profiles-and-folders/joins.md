# Joins and Ordering

Which rows share a pull request, which epic edges order the work, and how the epics are sequenced. The dependency checker derives the candidates from each work item's declared component; this record states the disposition of each.

## Within an epic

Rows of one epic extending one component are candidates to share a pull request. Each candidate unit is named below on one line with why its rows stay split.

- **E02:W01, E02:W02, E02:W03, E02:W05** stay split by rule: together they cover seven criteria, above the bound of six for one pull request.
- **E03:W01, E03:W02** stay split: W02 derives the run name through the parser W01 lands, and each row carries its own criterion and fixture family.
- **E06:W01, E06:W07** stay split: W07 compiles an entry as named through the preset channel W01 installs, and each row carries its own criterion and fixture family.
- **E06:W02, E06:W06, E06:W08** stay split: the declared-file path basis, a pair's reach and the folder refusal are three behaviours with their own criteria and fixtures, and one change to `closure.py` each keeps every refusal reviewable alone.

## Across epics

| Edge | Consumes |
| --- | --- |
| E01:W01 → E00:W00 | The preset key rule amends the design after E00's clause and pin. |
| E01:W04 → E00:W03 | Selection reads the classification that asks the target rather than a root. |
| E02:W01 → E00:W03 | The filter seam narrows the region set classification settles. |
| E02:W06 → E01:W03 | A preset carrying `include` and `exclude` reads the entry shapes that row lands. |
| E03:W01, E04:W01, E05:W01 → E00:W00 | Each option change amends the design after E00's clause and pin. |
| E06:W01 → E00:W00, E01:W09 | The preset read follows E00's clause, and reads `subst` in the colon-pair shape W09 lands. |
| E08:W00 → E00:W06, E02:W06, E06:W03 | The example tree is rewritten once the rootless tree, the preset carrying the filters and the corpus stating `subst` have landed. |

## Order and bases

- **Each epic cuts its base, `i08/eNN/main`, from `main` after the previous epic's review pull request merges.** The design pins then chain, and no epic base carries another's frontmatter edits.
- **Priority follows the task graph.** E00 8, E01 7, E02 through E06 5, and E08 1 as the migration that waits on the rest.
- **Every design clause row extends one file.** Each W00 amends `design.md` after the previous epic's pin moved, so the clause rows serialise across epics.
