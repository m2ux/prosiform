# Sources, goals and unresolved decisions

## Goal trace

The existing initiative Overviews supply the goals for this alignment. This review does not introduce another initiative goal.

| Goal clause | Initiative criteria | Delivering epics | Evidence and finding |
| --- | --- | --- | --- |
| Reproducible findings from use | I01 AC1, AC2 | E00 | Ledger format is delivered; capture and run records remain open. |
| Design-first revisions and visible unsettled work | I01 AC3, AC4, AC8 | E01 | The row coverage exists; workspace-skill guidance cites the pinned current invocation guide. |
| Exposure before a tagged freeze | I01 AC5, AC6, AC7, AC9 | E00, E13 | The user will deploy an example skill in prosiform-skills; deployment and its declaration are deferred, and workspace skills remain required. |
| Accounted-for carried debt | I01 AC10 | E03 | Superseded diagnostic and fault-option rows are retired by confirmed decisions. |
| Structural grouping and file-owned settings | I01 AC11, AC12, AC13, AC16, AC17 | E02, E06 | Atomic current-contract criteria pass 649 existing merged-main tests and the initiative readiness gate. |
| Dispatch declaration and repository branch shape | I01 AC14, AC15 | E09, E10 | Compiled dispatch targets pass merged-main verification; branch configuration is absent from current code bases. |
| A baseline that distinguishes forms | I10 AC1, AC2, AC9, AC11, AC12 | E00 | The epic is closed as completed. The initiative criteria are ready to verify, not automatically ticked. |
| Checks describing their execution and revisions | I10 AC3, AC4, AC5, AC7 | E01 | Closed delivery and ticked initiative criteria. |
| Settings isolation | I10 AC6, AC8 | E02 | Closed delivery and ticked initiative criteria. |
| References reaching the named grouped document | I10 AC10 | E03 | Closed delivery and ticked initiative criterion. |
| Measured composition and dispatch edges | I10 AC13 | E04 | Live records and shakedown remain open; completed structural criteria have passing verification. |
| Feature proof and runbook-governed measurements | I10 AC14, AC15 | E00, E04, E05 | Feature proof is delivered. The edge measurement still prevents AC15 from being complete. |
| One guide before the marks it explains | I10 AC16, AC17 | E06 | The approved AC16 describes current merged guide wording and passes its existing tests. |
| A named MVP release | I11 AC1, AC2 | E00 | Versioning source was read; no release work is recorded as delivered. |
| A checked pattern catalogue | I12 AC1, AC2, AC3, AC4, AC5, AC6 | E00–E04 | Every criterion has epic coverage. Template compliance and compilation in AC2 need distinct conditions. |

## Marked requirement sources

- **I01 R1:** The full current contract at `6deca17d6b56c61f477c815da6eeecc3949d8ca1` was read. Main revision `ba93ca60860f0dc46722f27acd471740465279da` names that exact design revision in its README profile link. The saved initiative binds I01 to that contract.
- **I01 R5, historical background:** Proposal #216 was read in full. It describes the first metadata design, including Agent Skills compatibility. It is not a requirement source for remaining refinement work.
- **I01 R6, historical background:** The file-owned invocation design was read in full. It describes historical `prosiform.root` and direct group/depth fields; current presets admit `group` and `subst`.
- **I01 R7, historical background:** The dispatch record's README and design were read. They describe historical `»` and `prosiform.dispatch`; current dispatch and guide requirements come from R1.
- **I11 R2:** Current main's `docs/versioning.md` was read in full. It specifies measured version selection, annotated tags and a persistent release branch merged back into main.
- **I10 and I12:** Neither initiative marks a requirement source. Their background references are not treated as requirements.

Every currently marked source has been read. The current-contract binding and its grouping, presets, invocation and dispatch criteria are reconciled. The exposure source set is confirmed; the external example's deployment and declaration remain pending. Historical delivery is not a claim of current conformance.

## Ranked open findings

### I01 requirements — high

- **Resolved:** #161 required a diagnostic the current compiler does not define. Its AC1 starts “Each fault `E_INVALID_GROUP_RULE` names”. Current main at `ba93ca60860f0dc46722f27acd471740465279da` contains no such code in the compiler or diagnostic catalogue.
  **User decision, 2026-11-05:** Retire it as not planned, remove W03 and AC3 from #187, and remove its board entry. The issue's body is preserved and its retirement comment records the reason. [Readback evidence](retirement-161.json).
- **Resolved:** #177 AC1 required `--fault`, which the compiler retires. Its code-listing requirement is already stated in the current design as `-C`, `--codes`.
  **User decision, 2026-11-05:** Retire the superseded issue as not planned, remove W05, AC5 and AC6 from #187, and remove its board entry. Its historical body is preserved. [Readback evidence](retirement-177.json).
- **Confirmed exposure source set:** The user will deploy an example skill in `prosiform-skills`; deployment is deferred. I01 requires that example and workspace skills before the freeze. The example's exact source identity, entry points and invocation await deployment. #21 AC6 is unticked because its delivered local-example declaration does not establish the external source. The declaration follow-up remains a gap-task decision. [Decision and evidence](external-example.md).
- **Resolved decision:** The current contract governs I01's remaining refinement work. The ledger, real-use evidence and specification-freeze goals stand; earlier root and dispatch metadata specifications are historical background. AC11–AC14, AC16 and AC17 state current grouping, presets, invocation and compiled dispatch behavior. Their ticks have passing merged-main [verification](verification.md) and initiative readiness evidence.

### I10 integration — high

- **Resolved decision:** The user authorized reconciliation with the delivered guide and `compiled` form, preserving task IDs. The saved issue bodies, W14–W16, W19's coverage and the PR test table state that design. [Verification](verification.md) establishes the affected ticks.
- **Problem:** E04's base predates current main's guide and dispatch-set heading. Passing the old base's suite does not establish integration with main's later grammar and harness changes.
  **Proposed resolution:** W16 reads the current merged guide and validates the integrated base before its shakedown. No base merge or implementation repair is performed in this alignment.
- **Problem:** At merged main `ba93ca60860f0dc46722f27acd471740465279da`, the guide in `src/prosiform/cli.py` names `⫽ <that section's title> dispatch set`, while `src/prosiform/dispatch.py` declares `⫽ Dispatch Set`. The existing guide tests assert its printed text and do not compare the two.
  **Proposed resolution:** The integration review needs a corrected guide and a check comparing its stated dispatch-set form with emitted bundles. Passing the printed-text checks alone does not settle this finding.
- **Problem:** PR #651's Open Questions hold the expanded default workflow matrix. Its merged implementation admits edge workflows through the existing `compiled` form; the planning record also carries the earlier decision to keep the baseline and edge workflow selections separate.
  **Proposed resolution:** Reconcile the runbook's workflow selections and the runner's default inventory before another paid run or declaring the combined baseline current.

### Criteria — medium

- **Resolved for I01:** AC11 states member headings, with distinct destinations in AC16 and derived heading casing in AC17. E02's Coverage includes all three; existing tests verify each condition.
- **Problem:** I11 AC2 joins the tag pair, an open pull request and passing checks. I12 AC2 joins template section order and successful compilation. These are independently falsifiable conditions.
  **Proposed resolution:** Split the conditions, preserve their existing labels where referenced, and update Coverage after confirmation.
- **Problem:** #187 AC13 combines CI triggering, collection of failed checks and crash-versus-drift verdicts. #255's CI conditions overlap the delivered #454 work. #243's AC2 says `--only` restricts a rewrite while its scope says triage reports and restatement is separate.
  **Proposed resolution:** Reconcile current delivery and separate verdict, execution and restatement requirements before planning implementation.

### Planning components and dependencies — medium

- **Problem:** I01's revision and freeze work items omit Component declarations; several issue-backed rows have no task file located in their registered records. The ledger work items use directory-level or branchless components. Contention cannot be fully measured from these declarations.
  **Proposed resolution:** Draft exact file components for each open row and account for each resulting join candidate before delivery. The [check evidence](checks.md) identifies every location not checked.
- **Problem:** The graph proposes E00 W03 and W04 as a ledger join candidate; its directory-level declaration is insufficient to choose that join.
  **Proposed resolution:** Choose the actual file components before joining or recording why they remain split.
- **Problem:** I10 has redundant edges in completed historical rows and backward task-number references. Closed epics remain outside the requested body-edit scope. E04 W14's redundant direct inputs are removed in the approved draft because W16 reaches them all.
  **Resolution for E04:** The user selected reconciliation preserving task IDs, so its current IDs stand. Closed-epic numbering remains historical context. Other undelivered-row renumbering requires a confirmed map.
- **Existing I12 decision:** All ten index-component contention pairs are printed in the graph report. The foundation's four pairs are ordered by row dependencies. The six family pairs have a recorded user decision for disjoint index sections and shared priority; this alignment changes no priority.

### Issue wording and references — low

- **Problem:** #160, #162, #185 and #186 lack the required title separator. #160 names an internal task in Problem and carries historical narration.
  **Proposed titles:** “Uncalled Functions: A Check Names Every Definition Without a Caller”; “Tracker Coverage: The Repository Run Resolves a Tracker Reference”; “Contract Vocabulary: Build Words Stay Outside Corpus Declarations”; “Corpus Vocabulary: Avoided Terms Carry the Glossary's Reason”.
- **Problem:** #187 References link same-board issues #39 and #454; #255 References link same-board issue #243.
  **Proposed resolution:** Put provenance in the planning record and cite that record from References; preserve the current ownership in the task tables.
- **False positives:** #158's W23 validation link and #162's W16 record are planning artifacts. PRs #184, #188, #190 and #244 are not board issues. Their evidence links do not violate same-board membership rules and are retained.

### Branch and board configuration — medium

- **Problem:** `config/branches` at refreshed `origin/workspace` declares `engineering`, `main` and `workspace`, but is absent from `origin/main`, `origin/i01/e00/main` and `origin/i10/e04/main`. The delivery scripts explicitly leave route, base-integration and review-link checks unevaluated.
  **Proposed resolution:** Establish the declaration at the revisions the delivery checks evaluate before preparing missing bases. No branch is created, retargeted or merged using an inferred declaration.
- **Resolved:** Twenty open items needed Initiative and Epic custom-field values after #161's retirement. Two initiative options and nine epic options cover I11, I12 and I10 E04. Existing IDs, colors, descriptions and assigned status and priority values were preserved; each saved grouping was read back. [Readback evidence](grouping.json).
- **I11 constraint:** The accepted release design explicitly names a `release/vX.Y.Z` branch and a user-owned merge into main. Its relationship to generic epic-base routing remains a recorded branch-shape decision; this alignment does not silently rewrite that release procedure.

## Interview queue

The I10 reconciliation and retirements of #161 and #177 are approved and applied. The current contract is the confirmed basis for I01. Its exposure set requires the forthcoming example in `prosiform-skills` and real workspace skills; deployment is deferred. Remaining questions cover the declaration gap task, criterion boundaries and splits, component declarations and branch configuration. The user also defers I10 E04 W14–W16 into the new I14 Evaluation Refinement initiative, preserving I13 Production Build.
