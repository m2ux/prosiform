# Epic

An epic's prerequisite evidence, task delivery findings, integration readiness and completion state.

## Prerequisites

Read these files first.

- [Initiative Issue Body](initiative-issue-body.md)
- [Issue](issue.md)
- [Pull Request](pull-request.md)
- [Pull Request Body](pull-request-body.md)
- [Delivery Branches](delivery-branches.md)

## Operations

### Check Epic Prerequisites

The evidence required before starting an epic's work.

**Inputs:** Current initiative and epic bodies, and current issue and base-merge records for every prerequisite named by their rows.

1. Identify each prerequisite named by the supplied initiative and task rows.
2. Apply the initiative's [whole-epic dependency rule](initiative-issue-body.md#work-breakdown); task-level references retain which output is consumed.
3. Confirm each prerequisite epic is closed as completed and every one of its bases has merged. A dependency on one task of another epic waits for that entire epic's delivery. Missing records leave the prerequisite unconfirmed.
4. Return the [Prerequisite Evidence](#prerequisite-evidence), identifying each confirmed prerequisite and missing condition. Only a confirmed result permits an unstarted epic to be marked Ready, its bases to be created or its task to be dispatched.

### Inspect Epic Delivery

The delivery findings for one epic from supplied evidence.

**Inputs:** Epic JSON, current pull request records and complete issue-link snapshot.

1. Run [Match Pull Requests](#match-pull-requests) with the epic JSON, pull request records as `--prs` and link snapshot as `--links`.
2. Return the [Delivery Findings](#delivery-findings); missing linked pull requests are missing evidence for the caller to supply.

### Check Epic Readiness

The epic's eligibility for integration from current delivery and criterion evidence.

**Inputs:** Current epic JSON, pull request records, complete issue-link snapshot and criterion verification evidence for the current delivery revisions.

1. Run [Inspect Epic Delivery](#inspect-epic-delivery) with the supplied epic JSON, pull request records and complete issue-link snapshot.
2. Confirm every task is delivered, every epic criterion is verified and ticked, and no open question or unresolved delivery discrepancy remains. An unmerged epic base awaiting integration is expected at this stage. Missing or stale verification leaves readiness unconfirmed.
3. Return the integration readiness in [Delivery State](#delivery-state), with the evidence revisions and each blocker. Readiness establishes the epic's content conditions; the caller supplies pull-request review, target and head-check evidence for the merge.

### Check Epic Completion

The epic's normal delivery result before tracker closure.

**Inputs:** Current epic JSON, pull request records, complete issue-link snapshot, current criterion verification evidence, complete expected base list and each base's merge evidence.

1. Run [Check Epic Readiness](#check-epic-readiness) with the current epic, pull request records, issue-link snapshot and criterion verification evidence.
2. Reconcile the expected bases with the task delivery targets.
3. Confirm every base has merged into its corresponding long-lived branch. An unknown or incomplete base list, or missing merge evidence, leaves completion unconfirmed even when every task is delivered and every criterion is ticked.
4. Return the completion result in [Delivery State](#delivery-state), identifying remaining blockers. Passing normal delivery checks supplies the caller's closure evidence; the tracker issue's current Development-link gate still governs the write.

### Integrate Epic Delivery

Coordinates current branch, epic and pull-request evidence for one epic-base integration.

**Inputs:** Epic identity and body, review identity, base worktree and target, current delivery records, complete issue-link snapshot, criterion verification evidence, and the architecture overview published for the review pull request.

1. Prepare the evidence.
   - Confirm the repository prerequisite in [Close Tracker Issue](issue.md#close-tracker-issue).
   - Run [Maintain Review Pull Request](pull-request-body.md#maintain-review-pull-request) with the actual task merges.
   - Confirm the supplied overview is the one published for the review pull request at its current head, meeting [Review Evidence](#review-evidence). Return a missing or stale overview as a finding for the caller to resolve before integration continues.
   - Read the pull request through [Read Pull Request State](pull-request.md#read-pull-request-state).
   - Require the user to have marked the draft ready.
   - Leave a draft waiting for that decision.
   - Confirm its head is the epic base and its target is the corresponding long-lived branch.
2. Run [Update Epic Base](delivery-branches.md#update-epic-base).
   - Obtain current criterion verification for the updated result.
   - Refresh the delivery records.
   - Call [Check Epic Readiness](#check-epic-readiness) with the current epic, delivery records, complete issue-link snapshot and that verification evidence.
   - When the branch content changes, before checking merge readiness:
     - Repeat Maintain Review Pull Request with the current task merges.
     - Return the changed head as a stale-overview finding, and resume with the overview the caller republishes for it.
   - Follow [Fetch Merge Readiness](pull-request.md#fetch-merge-readiness) for the exact current head and target. A conflict, failed or pending check, unmet epic condition or incomplete evidence leaves integration blocked.
3. Pass the confirmed epic readiness, verified head, target requirements, repository prerequisite and passing evidence to [Merge Delivery Pull Request](pull-request.md#merge-delivery-pull-request) with delivery kind epic, without asking for further confirmation.
   - Return its handoff when a human reviewer must merge. A changed head requires fresh verification; a merge refusal returns to the readiness checks, and a repeated refusal is reported without retrying.
4. Run [Read Pull Request State](pull-request.md#read-pull-request-state) to confirm the merged state, verified head, target and merge commit.
   - Return the result or blocker. Draft and blocked pull requests remain open.

## Fields

### Review Evidence

An epic base integrates with an architecture overview published for its review pull request at the head under review. An absent overview, or one published for an earlier head, is stale, and a stale overview leaves integration unresolved until the caller republishes it.

### Prerequisite Evidence

Each prerequisite has its issue identity and completion state, expected delivery bases and their merge evidence. The result identifies confirmed and missing conditions for the candidate epic.

### Delivery State

The epic is identified by its repository and issue number. Its state contains task delivery findings, criterion verification and ticks, open questions, expected delivery bases and their merges, and the revisions supporting the evidence. Integration readiness and completion are separate results, each with its unresolved conditions. An epic may be ready to integrate while one or more bases await merging.

### Delivery Findings

| Line | What it names |
| --- | --- |
| Conflict | Tasks that share a pull request and do not name each other in Joins. A row linked to a pull request whose title names another epic. |
| Unmatched | A merged pull request that names the epic and that no row links. |
| In flight | An open pull request that names the epic and that no row links. A pull request whose head is an epic base is not a task match. |
| Draft | An epic base a merged task targets that has no pull request merging it, while a task is undelivered or a criterion is unticked. |
| Unmerged | An epic base its pull requests target that has not merged into its long-lived branch, once every task is delivered and every criterion is ticked. A draft pull request is named draft. |
| References | A review pull request whose cited pull requests differ from the task pull requests merged into its base. |
| Uncited | A linked pull request whose task has its own issue and does not link it, or a review pull request that does not link the epic's issue. |
| Note | A row that links its task issue. |
| Unplaced | A task issue of this epic whose id is not a row. |
| Open questions | The epic's Open Questions section remains. |
| Ready to verify | A criterion whose delivering rows are all delivered. |
| Ticked early | A criterion ticked while a delivering row is not delivered. |
| Disagreement | A linked pull request's test plan against the Coverage of the rows it delivers. |

An unmet row links a merged pull request while a covered criterion remains unticked. A linked pull request naming another epic is a conflict and delivers its linked task once merged. A missing linked pull request leaves the supplied evidence incomplete.

A coverage disagreement identifies the pull request and row, a criterion absent from either the test plan or row Coverage, an empty Test cell, or prose assigning the criterion to another task. Recording links, verified criteria and Done continues despite that finding.

## Commands

### Match Pull Requests

Reports an epic's delivery state against the pull requests that name it.

**Inputs:** Epic JSON, pull request records and complete issue-link snapshot.

- Results follow [Delivery Findings](#delivery-findings).

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py '<epic-json-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json
```
