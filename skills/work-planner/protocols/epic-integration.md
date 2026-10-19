# Epic Integration

One epic base merged into its long-lived branch, on current branch, epic and pull-request evidence.

## Prerequisites

Read these files first.

- [Issue](../artifacts/issue.md)
- [Review Pull Request](review-pull-request.md)
- [Understand Mode](../modes/understand-mode.md)
- [Pull Request](../artifacts/pull-request.md)
- [Delivery Branches](../artifacts/delivery-branches.md)
- [Epic](../artifacts/epic.md)

## Procedure

1. **Prepare the evidence.**
   - Confirm the repository prerequisite in [Close Tracker Issue](../artifacts/issue.md#close-tracker-issue).
   - Follow [Review Pull Request](review-pull-request.md) with the actual task merges.
   - Run [Understand Mode](../modes/understand-mode.md) with the review pull request identity.
   - Resume with its published overview so the complete review body cites the task merges and carries that overview.
   - Read the pull request through [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state).
   - Require the user to have marked the draft ready.
   - Leave a draft waiting for that decision.
   - Confirm its head is the epic base and its target is the corresponding long-lived branch.
2. **Refresh and validate.**
   Run [Update Epic Base](../artifacts/delivery-branches.md#update-epic-base).
   - Obtain current criterion verification for the updated result.
   - Refresh the delivery records.
   - Call [Check Epic Readiness](../artifacts/epic.md#check-epic-readiness) with the current epic, delivery records, complete issue-link snapshot and that verification evidence.
   - When the branch content changes, before checking merge readiness:
     - Repeat Review Pull Request with the current task merges.
     - Repeat Understand Mode with the same pull request identity and updated head.
   - Follow [Fetch Merge Readiness](../artifacts/pull-request.md#fetch-merge-readiness) for the exact current head and target. A conflict, failed or pending check, unmet epic condition or incomplete evidence leaves integration blocked.
3. **Merge or hand off.**
   Pass the confirmed epic readiness, verified head, target requirements, repository prerequisite and passing evidence to [Merge Delivery Pull Request](../artifacts/pull-request.md#merge-delivery-pull-request) with delivery kind epic, without asking for further confirmation.
   - Return its handoff when a human reviewer must merge. A changed head requires fresh verification; a merge refusal returns to the readiness checks, and a repeated refusal is reported without retrying.
4. **Confirm the result.**
   Run [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state) to confirm the merged state, verified head, target and merge commit.
   - Return the result or blocker. Draft and blocked pull requests remain open.

## Effects

- **A ready epic base reaches its long-lived branch.**
  The merge runs on a head verified after the last branch change, with the review body and its overview current for that head.
- **A reviewer meets an explained change.**
  The review pull request carries an architecture overview written at the head under review.
- **An unready base stays open with its condition named.**
  A draft the user has not marked ready, a conflict, a failed or pending check, an unmet epic condition or incomplete evidence each leave the pull request open.
- **A human approval requirement is handed back, not worked around.**
  Where the target requires a reviewer, integration returns that handoff rather than attempting the merge.
