# Project 18 alignment

## Work list

- [x] Read the complete board inventory and confirm scope.
- [x] Check issue bodies, sources, dependencies and delivery evidence; identify unevaluated conditions explicitly.
- [ ] Publish mechanical corrections and resolve content decisions.
- [ ] Read back published changes, repeat affected checks and publish this record.

## Scope

The user selected all open board work. Project 18 holds 90 items, including 27 open issues: four initiatives, eleven epics and twelve task issues. View 4 has no filter. The issues belong to `m2ux/prosiform`; the workspace checkout's `origin` identifies that repository. The nested `.project/main` checkout's remote uses `m2ux/md-composer`, which GitHub redirects to `m2ux/prosiform`. Git reads in this review use the workspace project checkout and refreshed origin refs.

Open initiatives: I01 (#20), I10 (#464), I11 (#524), I12 (#526).

Closed issues are context only. The eleven closed epics linked by the open initiatives are not selected for body changes.

## Format review

All eleven open epics lack the Lane column in their task tables. Adding the column with empty cells preserves every task, dependency, join, coverage assignment and completion tick.

Eight existing task issues have findings about title shape, historical wording or internal references. These findings require inspection and a content decision before publication.

## Publication

The Lane column is saved and read back on #21, #22, #23, #187, #525, #527, #528, #529, #530, #531 and #579. I10 #464 records its completed E00 row from #403's current closed-as-completed state. These are twelve verified body corrections, with timestamps in [publication.json](publication.json).

The user approved reconciliation of I10 and #579 with delivered behavior. The [drafts](README.md#artifacts) preserve task IDs, carry the existing E04 lane assignments into the table, use the compiled form, separate W19's source, form and bundle criteria, and simplify W14's dependencies to W16 without changing their transitive reach. W14–W16's work items and the initiative's canonical drafts carry the same design.

The affected completed criteria pass the instruments in [verification.md](verification.md). The structural I11 and I12 dependency checks pass. I01 and I10 remain qualified by the findings in [source-review.md](source-review.md); historical closed-epic findings are separate from open-work corrections.

The approved I10 bodies and PR updates await publication after this record reaches the engineering branch. Board statuses and priorities are preserved.
