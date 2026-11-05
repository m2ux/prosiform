# Project 18 alignment

## Work list

- [x] Read the complete board inventory and confirm scope.
- [x] Check issue bodies, sources, dependencies and delivery evidence; identify unevaluated conditions explicitly.
- [ ] Resolve the remaining content decisions (in progress).
- [x] Read back the approved changes, repeat affected checks and publish their evidence record.

## Scope

The user selected all open board work. The initial Project 18 inventory held 90 items, including 27 open issues: four initiatives, eleven epics and twelve task issues. The final complete [board readback](board-readback.json) holds 89 items and 25 open issues, with both approved retirements absent and every open issue grouped. View 4 has no filter. The issues belong to `m2ux/prosiform`; the workspace checkout's `origin` identifies that repository. The nested `.project/main` checkout's remote uses `m2ux/md-composer`, which GitHub redirects to `m2ux/prosiform`. Git reads in this review use the workspace project checkout and refreshed origin refs.

Open initiatives: I01 (#20), I10 (#464), I11 (#524), I12 (#526).

Closed issues are context only. The eleven closed epics linked by the open initiatives are not selected for body changes.

## Format review

All eleven open epics lack the Lane column in their task tables. Adding the column with empty cells preserves every task, dependency, join, coverage assignment and completion tick.

Eight existing task issues have findings about title shape, historical wording or internal references. These findings require inspection and a content decision before publication.

## Publication

The Lane column is saved and read back on #21, #22, #23, #187, #525, #527, #528, #529, #530, #531 and #579. I10 #464 records its completed E00 row from #403's current closed-as-completed state. These are twelve verified body corrections, with timestamps in [publication.json](publication.json).

The user approved reconciliation of I10 and #579 with delivered behavior. The [drafts](README.md#artifacts) preserve task IDs, carry the existing E04 lane assignments into the table, use the compiled form, separate W19's source, form and bundle criteria, and simplify W14's dependencies to W16 without changing their transitive reach. W14–W16's work items and the initiative's canonical drafts carry the same design.

The affected completed criteria pass the instruments in [verification.md](verification.md). The structural I11 and I12 dependency checks pass. I01 and I10 remain qualified by the findings in [source-review.md](source-review.md); historical closed-epic findings are separate from open-work corrections.

The approved bodies of #464 and #579, PR #651's test coverage and draft review PR #622's compiled-form overview are saved and read back. Their evidence links resolve to this record published on engineering.

The user approved retirement of #161. It is closed as not planned, with its historical body retained and a [retirement comment](https://github.com/m2ux/prosiform/issues/161#issuecomment-6654122521) naming the reason. #187 omits W03 and AC3 and preserves the remaining labels. A complete board read confirms #161 is absent; 26 open issues remain in the selected scope.

Twenty open items have their Initiative and Epic grouping saved and read back. Two initiative options and nine epic options cover the missing identities. Existing option IDs, colors, descriptions, statuses and priorities are preserved, as [grouping.json](grouping.json) records.

The user also approved retirement of #177 as superseded. It is closed as not planned with its body preserved and a [retirement comment](https://github.com/m2ux/prosiform/issues/177#issuecomment-6656075887) recording the decision. #187 omits W05, AC5 and AC6; all remaining IDs stand. The complete board read confirms its absence. The selected scope now has 25 open issues.

The evidence record starts at engineering commit `e79bdd9c5`, with publication receipts, grouping and retirement recorded incrementally. Alignment remains open for the decisions in [source-review.md](source-review.md). The user selected the current contract as the basis for I01's remaining refinement work, retaining its ledger, real-use evidence and freeze goals; the earlier root and dispatch metadata specifications supply historical background.

The saved source binding on #20 names design revision `6deca17d6b56c61f477c815da6eeecc3949d8ca1`, as merged main's profile link names it. #22 and its workspace-skill work item use the supported invocation guide and source declarations. Their acceptance criteria and completion states are preserved. The remaining exposure-set choice is pending before that goal's criteria and task coverage are changed.

The saved I10 follow-up criteria state the run-pf instruction before source content without claiming it is a bundle's first bytes. The instruction and absence of a generated dispatch protocol have separate criteria, AC17 and AC18. Three existing bundle-publication checks pass at merged main, and both criteria pass the initiative readiness gate against completed E06.

The saved I01 criteria and canonical initiative body state current grouping, selected presets, declaring entry invocation and compiled dispatch behavior. AC11's independent destination and casing conditions have AC16 and AC17, with E02's Coverage updated. All six affected criteria pass 649 existing merged-main tests and the initiative readiness gate; exposure-dependent criteria await the user choice.
