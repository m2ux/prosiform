# Changes

The plan changes this delivery session applied, and what it held for the user. The allowance it ran under covers task creation, epic creation, migration, re-prioritisation and folded work; a new initiative is outside it.

## Applied

| Kind | Subject | Option applied |
| --- | --- | --- |
| Task creation | [#189 \[I01:E03:W08\]](https://github.com/m2ux/prosiform/issues/189) Corpus Runner: One Fixture Run by Its Identity | Raised as a task issue and placed as row W08 on [#187 \[I01:E03\]](https://github.com/m2ux/prosiform/issues/187), the carried-debt epic. |
| Folded work | [#187 \[I01:E03\]](https://github.com/m2ux/prosiform/issues/187) | AC9 added, stating the verdict the runner gives for one fixture asked for by its identity, which W08's row covers. |
| Re-prioritisation | [#189](https://github.com/m2ux/prosiform/issues/189) on the Bundling board | Added at Backlog, where every other row of that epic stands. |
| Re-prioritisation | [#39 \[I00:E11\]](https://github.com/m2ux/prosiform/issues/39) on the Bundling board | Moved to In Review, its rows and criteria all complete and its review pull request a draft awaiting the user's mark. |
| Folded work | [#39 \[I00:E11\]](https://github.com/m2ux/prosiform/issues/39), row W15 | The row links the commit that delivered it rather than its task issue, so the delivery record resolves and a sync no longer reads the row as undelivered. |

## Held

Nothing was held. No change this session met required a new initiative, and no option it took was outside the allowance.

## Classified and not raised

- **A file heading's fragment drops the path separator.**
  Without a grouping rule, `docs/alpha.md` is headed `# docs/alpha` and slugs to `docsalpha`, which `doc/salpha.md` would slug to as well. The run was performed: the second document takes `docsalpha-1` and each reference reaches the document it named, which is the renderer's own ordinal rule and what the design's *Residual ambiguity* clause states for anything still coinciding. No defect, so no issue.

## Deferred debt, classified

Classified by what fixing each makes true, as the session's own reading.

- **Blocking — fixed here.**
  The design's Grouping clause stated that a member contributing nothing to a group resolves to the group's own heading. W29 ends that behaviour, so the sentence would have read as current fact about a build that no longer does it. The clause is restated on the `engineering` branch with this delivery.

- **Trivial — fixed here.**
  Row W15 on [#39](https://github.com/m2ux/prosiform/issues/39) linked its task issue rather than the commit that delivered it, so each sync of the epic read the row as undelivered and offered to untick the criterion it covers. One link, no work item.

- **Non-trivial — deferred.**
  The corpus runner takes no fixture to run, which no run of the tool shows and which blocked none of this unit's criteria. It is [#189](https://github.com/m2ux/prosiform/issues/189) on the carried-debt epic, where the line this epic's scope was drawn on puts it.
