# Sources, goals and unresolved decisions

## Goal trace

The existing initiative Overviews supply the goals for this alignment. This review does not introduce another initiative goal.

| Goal clause | Initiative criteria | Delivering epics | Evidence and finding |
| --- | --- | --- | --- |
| Reproducible findings from use | I01 AC1, AC2 | E00 | Ledger format is delivered; capture and run records remain open. |
| Design-first revisions and visible unsettled work | I01 AC3, AC4, AC8 | E01 | The row coverage exists; bootstrap guidance names the removed example tree. |
| Exposure before a tagged freeze | I01 AC5, AC6, AC7, AC9 | E00, E13 | The exposure goal includes example modes absent from current main. |
| Accounted-for carried debt | I01 AC10 | E03 | Superseded diagnostic and fault-option rows are retired by confirmed decisions. |
| Structural grouping and file-owned settings | I01 AC11, AC12, AC13 | E02, E06 | Closed delivery is recorded; current presets differ from the marked historical sources. |
| Dispatch declaration and repository branch shape | I01 AC14, AC15 | E09, E10 | Closed delivery is recorded; dispatch metadata is superseded by the guide, and configuration is absent from current code bases. |
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

- **I01 R1:** The entire v1 design at commit `3ff368936aa577ef57bd43b7a2fae63c264a99dc` was read from the project repository. It describes an explicit global source root, run-wide grouping and deferral emission that subsequent initiatives changed.
- **I01 R5:** Proposal #216 was read in full. Its goal requires Agent Skills metadata compatibility and its Non-Goals exclude source roots in metadata. The initiative also marks later file-owned-root requirements as a source, so their scopes and precedence need an explicit reconciliation.
- **I01 R6:** The file-owned invocation design on `engineering` was read in full. It specifies `prosiform.root`, direct group/depth fields and derived bundle filenames; current main's preset schema admits `group` and `subst` within presets.
- **I01 R7:** The dispatch record's README and design were read. They specify `»` and `prosiform.dispatch`; current code and documentation describe `⇉`, dispatch sets and one guide.
- **I11 R2:** Current main's `docs/versioning.md` was read in full. It specifies measured version selection, annotated tags and a persistent release branch merged back into main.
- **I10 and I12:** Neither initiative marks a requirement source. Their background references are not treated as requirements.

No unread marked source is claimed as checked. The source departures above remain unresolved; historical delivery is not a claim of current conformance.

## Ranked open findings

### I01 requirements — high

- **Resolved:** #161 required a diagnostic the current compiler does not define. Its AC1 starts “Each fault `E_INVALID_GROUP_RULE` names”. Current main at `ba93ca60860f0dc46722f27acd471740465279da` contains no such code in the compiler or diagnostic catalogue.
  **User decision, 2026-11-05:** Retire it as not planned, remove W03 and AC3 from #187, and remove its board entry. The issue's body is preserved and its retirement comment records the reason. [Readback evidence](retirement-161.json).
- **Resolved:** #177 AC1 required `--fault`, which the compiler retires. Its code-listing requirement is already stated in the current design as `-C`, `--codes`.
  **User decision, 2026-11-05:** Retire the superseded issue as not planned, remove W05, AC5 and AC6 from #187, and remove its board entry. Its historical body is preserved. [Readback evidence](retirement-177.json).
- **Problem:** #20 AC7 and #21's exposure-set criteria require the worked example's mode entries. #22 R2 points to `main/example/work-planner/bootstrap.md`, which the current main tree does not hold.
  **Proposed resolution:** Choose a current exposure set and an accessible bootstrap exemplar; retain the historical demonstration only as measured history.
- **Problem:** #20 AC13 and AC14 describe file-owned invocation and dispatch metadata that the current contract does not admit. The marked sources specify several different schema generations.
  **User decision, 2026-11-05:** The current contract governs the remaining refinement work. The ledger, real-use evidence and specification-freeze goals stand; earlier root and dispatch metadata specifications are historical background. Source and criterion reconciliation against that boundary is in progress.

### I10 integration — high

- **Resolved decision:** The user authorized reconciliation with the delivered guide and `compiled` form, preserving task IDs. The saved issue bodies, W14–W16, W19's coverage and the PR test table state that design. [Verification](verification.md) establishes the affected ticks.
- **Problem:** E04's base predates current main's guide and dispatch-set heading. Passing the old base's suite does not establish integration with main's later grammar and harness changes.
  **Proposed resolution:** W16 reads the current merged guide and validates the integrated base before its shakedown. No base merge or implementation repair is performed in this alignment.
- **Problem:** PR #651's Open Questions hold the expanded default workflow matrix. Its merged implementation admits edge workflows through the existing `compiled` form; the planning record also carries the earlier decision to keep the baseline and edge workflow selections separate.
  **Proposed resolution:** Reconcile the runbook's workflow selections and the runner's default inventory before another paid run or declaring the combined baseline current.

### Criteria — medium

- **Problem:** I01 AC11 joins member headings, destination identity and casing. I11 AC2 joins the tag pair, an open pull request and passing checks. I12 AC2 joins template section order and successful compilation. These are independently falsifiable conditions.
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

The I10 reconciliation and retirements of #161 and #177 are approved and applied. The current contract is the confirmed basis for I01. Remaining questions cover its exposure set, criterion boundaries and splits, component declarations and branch configuration. Each is asked separately.
