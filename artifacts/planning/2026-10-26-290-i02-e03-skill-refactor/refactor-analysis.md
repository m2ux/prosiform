# Work-planner refactor: what to move out of the ten modes, sorted by object

Scope: content moved out of the modes only. Protocols and artifacts appear only as places that content would go. All paths are relative to `example/work-planner/` at epic commit da6d0515 (dispatch marks since rewritten as `⇉`; Deliver step 8 since reworded), and `file:N` is a line in that file. Read-only analysis.

## 1. Object table

- **Ops today** lists the operations that already exist.
- **Ops to add or extend** lists new or extended operations the mode content needs (★ = new).
- **Op held in a protocol** lists operation-shaped content that sits inside a protocol today.
- **Mode lines out** is roughly how many mode lines would leave.

| Object | Artifact | Ops today | Mode locations (op or inline content) | Ops to add or extend | Op held in a protocol | Mode lines out |
|---|---|---|---|---|---|---|
| Tracker issue | issue.md | Read, Save, Select Tracker Number, Comment, Read Repository Issues, Confirm Auto-Close, Locate Initiative Issue | Read: almost every step. Save: about 25 sites. Select Number: propose:23, plan:25, plan:50 (applied twice). Inline capture of Development links: sync:33–34. Labels ensured before saving at propose:32, plan:48, advance:47–48. Standalone issue created with no body op at deliver:133, deliver:139. Priority label saved at advance:48, plan:52, plan:69. | Extend **Save Tracker Issue** to apply Ensure Repository Labels for any label it assigns (it now returns a missing-label result). ★**Check Issue Completion**: takes the kind, sends it to the epic.md or initiative.md check. | issue-closure.md step 3 holds the task/epic/initiative branching (should be ★Check Issue Completion). issue-closure.md:18 holds a "fresh destination file" rule belonging to Close Tracker Issue. | ~8 |
| Common issue body | issue-body.md | Validate, Apply Body Corrections, Repair Issue Format, Check Round of Edits | Validate → fix mechanically → ask → correct → save → re-validate loop written by hand at align:24–31, align:36–52, hoist:34–41, plan:55–58. sync:23–27 applies Repair then re-fetches and re-validates, which Repair step 4 already does. Open Questions resolved inline at sync:17–22, plan:31, plan:77–80. Criteria split and Coverage updated at plan:81–82. | Extend **Repair Issue Format** to accept the kind's validator (Validate Epic/Initiative/Proposal Body plus their extra inputs) and a set of bodies. ★**Resolve Open Questions**: ask the user, apply corrections, save, re-read; returns the questions still open. | none | ~30 |
| Initiative body | initiative-issue-body.md | Draft, Validate, Record Initiative Delivery, Read Requirement Sources | Record → verify → tick → save at align:88–95, sync:113–119. Sources named but Read Requirement Sources never applied (align:22, align:56–61). Temporary links replaced at plan:51–54. Misplaced Non-Goals moved in from an epic at align:39–40. | ★**Resolve Placeholder Links**: replaces temporary epic-row links with saved issue identities. Departure / Non-Goal rule (align:61) → Sources field. | none | ~15 |
| Epic body | epic-issue-body.md | Populate, Validate, Record Epic Delivery, Revise Epic Rows, Plan Gap Task, Reserve Task Rows, Release Task Rows | Record Epic Delivery: align:73, 114, 121; sync:55–92, sync:111; deliver:116. Unplaced task row placed inline at align:113–119, sync:76–83, plan:90–93. Absent or unlinked finding, refresh, repeat: align:81–87. Shared-reference row rewritten at align:47–50. Released rows saved at deliver:51–53. Corpus Audit unit rule at deliver:69–70. Hold invariants at deliver:66–67. | ★**Place Unplaced Task Row**: draft row → Revise Epic Rows → Save → Record Epic Delivery. Fold Save into Release Task Rows. deliver:66–67 invariants → Task Delivery field. deliver:69–70 rule → Corpus Audit field or delivery-plan Work Units. | issue-delivery.md:20 applies Populate Epic Issue Body for an unplaced task while the modes use Revise Epic Rows; the two should become one op. | ~30 |
| Task body | task-body.md | Record Task Delivery | sync:49–53: verify → record → save → comment "Delivered by #N" → close. | Record Task Delivery returns the comment file it calls for. | issue-delivery.md step 1 does the same sequence. | ~5 |
| Standalone body | standalone-body.md | Revise | deliver:133, deliver:139 save an issue with no populated body. | Apply Populate Standalone Body there. | none | ~2 |
| Acceptance criteria | acceptance-criteria.md | Verify Selected Criteria, Tick Verified Criteria | Verify → tick → save at align:77, align:91–95, sync:94–104, sync:115–119. Inline quality and source check at align:54–61. | ★**Record Verified Criteria**: verify, tick, save; returns verified ids and the refused or unverified ones. ★**Check Criteria Quality**: against Requirement Characteristics through Verifiable, plus Read Requirement Sources. | issue-delivery.md steps 1 and 4 hold the same verify/tick/save pairing. | ~22 |
| Epic (subject) | epic.md | Check Epic Prerequisites, Inspect Epic Delivery | Rule for matching pull requests to tasks inline at sync:45–47, reused at sync:60–63, sync:75. | ★**Match Delivery to Tasks**: one task, or tasks naming each other in Joins; unclear matches go to the user; returns confirmed matches. | none | ~6 |
| Board | board.md | Select, Locate, Create Proposals Board, Copy, Place Issue on Board, Read Board State, Read Board Configuration, Read Board Assignee, Update Item Status | Board found or created inline at propose:40–41 and sync:122–125, by different ops. Issue id read only to place it (propose:42). | ★**Ensure Project Board**: Select, then Copy with proposal provenance. Place Issue on Board takes the issue number. | none | ~6 |
| Board and delivery snapshot | delivery-evidence.md | Read Delivery Evidence | Same fetch block (board state, initiative PRs, issue links, configuration, assignee) at advance:22–26, deliver:22–27, standup:27–30, and in board-delivery Record Board Delivery step 1. sync:36–41 repeats Read Delivery Evidence step 3 (repair a PR title). sync:33–34 repeats its step 2. | ★**Read Board Delivery Evidence**: board-scoped twin of Read Delivery Evidence. | none | ~20 |
| Board queue | board-queue.md | Plan Board Queue | Missing-evidence loop at advance:30–35. Refresh and re-plan after writes at advance:46–51, advance:54–59. Status/assignee calls run inline with no op at advance:55. | ★**Apply Board Queue**, modelled on Record Board Delivery: plan → fetch unresolved → run calls → read back → re-plan until converged → return pending order/ask lines. | none | ~18 |
| Delivery plan | delivery-plan.md | Plan Available Work | Missing-issue loop at deliver:33–34, deliver:54. | Plan Available Work resolves its own missing issues. | none | ~3 |
| Standup report | standup-report.md | Compose Standup Report | Resolve-and-repeat loop at standup:33–37. | Compose Standup Report locates and reads unresolved initiatives itself. | none | ~4 |
| Pull request | pull-request.md | Publish Pull Request, Read Pull Request State, Merge Task Pull Requests, Link Pull Request to Issue, fetch ops | Draft review PR opened inline with no op at align:121–123, sync:64–66, sync:106. Base-alignment rules inline at align:104–112. Merge Task Pull Requests always followed by Task Merge (deliver:45–46, deliver:119–121). | ★**Align Pull Request Base**: retarget to the epic base or long-lived branch, Update Task Branch when not mergeable, report the rest. align:107–112 rules → Fields (Scope / Other Pull Requests). Inline review-PR sites follow the Review Pull Request protocol. | epic-integration.md:21 holds a head/target check; :30, :33 restate readiness and refusal rules (belong to Fetch Merge Readiness and Merge Delivery Pull Request). review-pull-request.md:22 holds a publication condition (belongs to State); :26 a body comparison Publish Pull Request already performs. | ~18 |
| Pull request body | pull-request-body.md | Populate Pull Request Body | Inline test-to-criterion check at deliver:101–102. | ★**Check Test Coverage**. | none | ~2 |
| Branches and worktrees | delivery-branches.md | Prepare Delivery Bases, Read Delivery Branches, Update Task Branch, Create Task Worktree | Prerequisites → prepare bases at align:99–102, deliver:29–30, plan:83–85. | none (see P2) | change-overview.md:15–19 holds a changed-head retry belonging inside Create Pull Request Worktree. | ~12 |
| Planning record | planning-record.md | Populate Planning Record, Publish Planning Record | Populate → Publish at deliver:60–61, 98–99, 143–144. Inline "Commit. Push." at plan:74–75 bypasses Publish. "Record/update the planning record" with no op link at plan:30, 42, 59, 73. | Fold Publish into Populate as an option. ★**Locate Planning Record** by reference. | change-overview.md:28–29 holds the folder identity and slug rule; :33 the Artifacts/Links row rule. | ~8 |
| Work item | work-item.md | Populate Work Item | Row's component and work-item file read inline at deliver:59, align:65. | ★**Read Work Item**: returns component and test row. | none | ~2 |
| Delivery brief | delivery-brief.md | Populate Delivery Brief | Brief read and reservation confirmed inline at deliver:89–93. | ★**Read Delivery Brief**. | none | ~3 |
| Plan change / change list | plan-change.md | Check Plan Change Autonomy, Record Plan Change | Check → automatic, record / held, settle or interview repeated at advance:38–41, hoist:23–29, hoist:37, sync:78–80, deliver:56, deliver:136/141. | ★**Settle Plan Change**: returns the applied option, held, or the user's answer, plus the updated list. | none | ~15 |
| Placement | placement.md | Find, Draft, Apply Issue Placement, Rewrite Orphan Issue, Subsume Orphan Work | hoist:21 orders options; hoist:32 chooses the disposition. | Ordering → Placement Record field. Disposition choice → Issue Placement protocol (P5). | none | ~3 |
| Dependency graph | dependency-graph.md | Check Dependencies and Numbering | Epic Priority map interview plus labels at plan:46–48, plan:68–69. | Check Dependencies and Numbering reads work-item files itself (align:65). | none | ~3 |
| Goal trace / review finding | goal-trace.md, review-finding.md | Review Initiative Goal, Report Review Finding | Review → report → apply → repeat at plan:35–43, plan:62–65, align:33–35. | none; guidelines keep this loop in Plan. | none | 0 |
| Repository labels | repository-labels.md | Ensure Repository Labels | advance:47, plan:48, propose:32 | Applied from Save Tracker Issue instead. | none | ~3 |
| Technical debt item | none today | none | Blocking / Trivial / Non-trivial classification inline at deliver:124–131. | ★`artifacts/technical-debt.md` with ★**Classify Technical Debt**, or a field under initiative-issue-body Deferred Debt. | none | ~7 |

## 2. Existing artifacts departing from the canonical structure

All 30 artifacts have the right section order (Operations, Fields, Commands), and every `###` operation has its opening line and **Inputs:** line. Departures are in content:

- `placement.md#apply-issue-placement`: changes several objects in one operation (populates epic and initiative bodies, saves several issues, runs Check Dependencies and Numbering). A protocol, not an operation of one shape.
- `placement.md#subsume-orphan-work`: edits the destination issue and closes the source issue; spans two objects.
- `pull-request.md#merge-task-pull-requests`: updates the epic base and task branch (delivery-branches) as well as merging; spans two objects.
- `delivery-evidence.md#read-delivery-evidence` step 3: a read renames a pull request through Publish Pull Request; the write belongs to the caller.
- `dependency-graph.md#check-dependencies-and-numbering`: settles plan changes and writes the planning record.
- `goal-trace.md#review-initiative-goal` step 7: records the trace table in the planning record.
- `board-delivery.md#record-board-delivery`: runs assignee calls against the issue, not the board item (the rest is acceptable).
- Operations handing the user a decision or saving the result (`epic-issue-body.md#plan-gap-task`, `issue-body.md#repair-issue-format`): not forbidden for a single object, but they set the precedent for ★Resolve Open Questions and ★Settle Plan Change.
- `issue.md#close-tracker-issue` step 2: restates the Auto-Close Setting rule inline; its home is the Auto-Close Setting field.
- `board.md` Select Project Board and Locate Project Board run the same two commands; Locate is reached only from propose:40 and has no caller once ★Ensure Project Board exists.

## 3. Existing protocols carrying artifact-specific content

| Protocol | Inline content | Where it belongs |
|---|---|---|
| change-overview | :15–19 retry on a changed head; :22–25 stale index or changed revision | Retry loops inside Create Pull Request Worktree and Measure Repository Change |
| change-overview | :28–29 overview folder identity (PR number plus slug); :33 one Artifacts row, PR under Links | ★planning-record Locate Planning Record; Layout / Artifacts fields |
| epic-integration | :21 head is the epic base, target is long-lived | pull-request Fields (State/Scope) checked inside Fetch Merge Readiness |
| epic-integration | :24–25 "obtain verification, refresh records" with no op | ★Record Verified Criteria; Read Delivery Evidence |
| epic-integration | :30, :33 blocking conditions and refusal handling | Fetch Merge Readiness; Merge Delivery Pull Request |
| issue-closure | :18 fresh destination file; :19–29 branching by kind | Close Tracker Issue; ★Check Issue Completion |
| issue-delivery | :20 Populate Epic Issue Body for an unplaced task; :23–24 restates the Disagreement rule from epic.md | ★Place Unplaced Task Row; link to Delivery Findings |
| review-pull-request | :22 when to publish, and "epic stays open / user marks ready"; :26 body comparison | pull-request State field; already done inside Publish Pull Request |
| task-merge | :26 "Refresh the evidence" with no op | Read Delivery Evidence |

## 4. Protocol candidates (each purely operations applied and protocols followed)

- **P1 Unit Hold** (deliver:58–67): Read Work Item → Populate Planning Record (publish) → Reserve Task Rows → Save Tracker Issue → Update Item Status for each task, then the epic. Inputs: unit line, epic JSON, board identity. Returns held unit and record folder. ~9 lines out. High confidence.
- **P2 Delivery Base Preparation** (align:99–112, plan:83–85, deliver:29–31): Check Epic Prerequisites → Prepare Delivery Bases → Read Initiative Pull Requests → Read Delivery Branches → ★Align Pull Request Base. Returns bases created, PRs retargeted, conflicts. ~20 lines out across three modes. High confidence.
- **P3 Delivery Recording** (sync:42–104, align:70–97): per epic, Read Delivery Evidence → ★Match Delivery to Tasks → follow Issue Delivery for each merged match → Record Epic Delivery → route findings (Review Pull Request; ★Place Unplaced Task Row; ★Resolve Open Questions; Plan Gap Task → ★Record Verified Criteria; Link Pull Request to Issue); then Record Initiative Delivery → ★Record Verified Criteria for the initiative. Removes Sync's direct use of Verify, Record Task Delivery, Tick and Save, which Issue Delivery owns (a Layers breach). ~75 lines out. Medium confidence: Align asks the user where Sync applies its allowance, so it needs an allowance input.
- **P4 Epic Closure** (sync:105–112, plus task-merge.md step 4): Review Pull Request (unmerged base with no review) → Epic Integration → Read Delivery Evidence → Record Epic Delivery → Issue Closure → Record Initiative Delivery. ~8 lines out. High confidence.
- **P5 Issue Placement** (hoist:31–33, plus `placement.md#apply-issue-placement` and Subsume Orphan Work): apply destination body ops → Save Tracker Issue → Check Dependencies and Numbering → Rewrite Orphan Issue, or Subsume (through Close Transferred Work). Fixes the artifact departure in section 2. Medium confidence.
- **P6 Initiative Publication** (plan:49–59): Select Tracker Number → Save initiative → Save epics in dependency order with priority labels → ★Resolve Placeholder Links → Save → Repair Issue Format with each kind validator → Populate Planning Record. ~10 lines out. Medium: one site, long, several objects.
- **P7 Task Pull Request Opening** (deliver:113–117): Confirm Repository Auto-Close → Publish Pull Request → Record Epic Delivery → Save. Medium-low: one site.
- **Fold the merge into Task Merge** (deliver:45–46, deliver:119–121): Task Merge starts from a `merge` line and applies Merge Task Pull Requests first. Medium: widens the situation the protocol is named for.
- **Not a protocol candidate:** the arising-issue hoist (deliver:132–141) follows Hoist Mode; a protocol calling a mode is an up-the-stack call. It should become one mode subsection used by both debt steps and the arising-issue step.

## 5. What each mode keeps

| Mode | Procedure lines now | Lines out | Lines left | Role afterwards |
|---|---|---|---|---|
| Advance | 49 | ~22 | ~27 | Orchestration only: select, follow Sync, Read Board Delivery Evidence, Apply Board Queue, Settle Plan Change on order/ask lines, report |
| Align | 119 | ~65 | ~54 | Orchestration, except scope rules at align:14–23 (legitimate scope selection) |
| Deliver (main) | 69 | ~25 | ~44 | Orchestration: confirmation interview, follow P1 Unit Hold, dispatch |
| Deliver (Run Delivery Session) | 62 | ~22 | ~40 | Orchestration, except sub-agent grouping at deliver:104–111 (mode-level dispatch, stays) |
| Hoist | 33 | ~12 | ~21 | Orchestration only |
| Plan | 82 | ~30 | ~52 | Orchestration; review loop stays, as the guidelines ask |
| Propose | 34 | ~6 | ~28 | Orchestration; interview and evidence steps stay |
| Revise | 32 | ~6 | ~26 | Orchestration; checklist at revise:28–33 restates guidelines and could link them |
| Standup | 32 | ~7 | ~25 | Orchestration only |
| Sync | 122 | ~90 | ~32 | Orchestration only: select → follow P3 → follow P4 → board → follow Understand Mode → report. sync:130 overview ownership rule moves to architecture-overview Fields. |
| Understand | 8 | 0 | 8 | Already orchestration only |

## 6. Highest-value migrations

1. **P3 Delivery Recording**, with ★Match Delivery to Tasks and ★Place Unplaced Task Row: ~75 lines out of Sync and Align; ends Sync's direct use of operations Issue Delivery owns.
2. **★Record Verified Criteria** (acceptance-criteria): five copies of verify → tick → save in Align and Sync, plus the matching steps in Issue Delivery.
3. **★Settle Plan Change** (plan-change): six copies across Advance, Hoist, Sync and Deliver.
4. **★Read Board Delivery Evidence** plus **★Apply Board Queue**: removes the copied fetch block from Advance, Deliver, Standup (and Record Board Delivery), and Advance's three hand-written re-plan loops, including the inline call execution at advance:55.
5. **P2 Delivery Base Preparation** plus **★Align Pull Request Base**: three modes; base rules move out of align:104–112 into pull-request Fields.
6. **Route inline review-PR openings through Review Pull Request**: align:121–123, sync:64–66, sync:106 open a draft review PR with no operation.
7. **P1 Unit Hold** and **P4 Epic Closure**: two multi-object sequences, the second shared with Task Merge step 4.
8. **Extend Repair Issue Format** to take each kind's validator and a set of bodies: replaces hand-written validate/correct/save loops in Align 3–6, Hoist 6, Plan 6, and the redundant re-validate in Sync 1.

Small, high-confidence fixes:
- plan:74–75 "Commit. Push." should apply Publish Planning Record.
- plan:90–93 repeats Sync's own handling of an unplaced task.
- sync:36–41 repeats Read Delivery Evidence step 3.
- align:22 and align:56–61 should apply Read Requirement Sources.
- propose:40–41 should use the same Select → Copy path as sync:122–125.
