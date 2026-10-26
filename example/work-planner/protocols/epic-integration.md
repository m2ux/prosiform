---
prosiform:
  root: ".."
  group: "protocols"
  group-depth: 1
---
# Epic Integration

One epic base merged into its long-lived branch, on current branch, epic and pull-request evidence.

## Procedure

1. **Prepare the review.**
   - Apply [Confirm Repository Auto-Close](../artifacts/issue.md#confirm-repository-auto-close) for the repository.
   - Follow [Review Pull Request](review-pull-request.md) with the actual task merges, the epic's issue and that confirmed setting.
   - Follow [Change Overview](change-overview.md) with the review pull request identity.
   - Read the pull request through [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state).
   - When it is a draft, put the ready mark [State](../artifacts/pull-request.md#state) leaves to the user as an [interview](../rules.md), naming the epic standing in review on its board.
   - Return a draft still awaiting that decision to the caller, open.
2. **Refresh the evidence.**
   - Apply [Update Epic Base](../artifacts/delivery-branches.md#update-epic-base) with the project checkout and the epic base.
     - Return a conflict or failure to the caller.
   - Apply [Read Delivery Evidence](../artifacts/delivery-evidence.md#read-delivery-evidence) with the repository, initiative prefix and current epic JSON.
   - Apply [Record Verified Criteria](../artifacts/acceptance-criteria.md#record-verified-criteria) for the epic, with its criterion ids, current issue JSON and body, the delivery findings, pull request records and complete issue-link snapshot Read Delivery Evidence returned, the updated epic base as delivery revision, the named instruments, the project checkout and an output body file.
   - When Update Epic Base merged new content into the base:
     - Repeat Review Pull Request with the current task merges.
     - Repeat Change Overview with the same pull request identity and updated head.
3. **Check readiness.**
   - Apply [Check Epic Readiness](../artifacts/epic.md#check-epic-readiness) with the current epic JSON, pull request records, complete issue-link snapshot and the verification evidence Record Verified Criteria returned.
   - Apply [Fetch Merge Readiness](../artifacts/pull-request.md#fetch-merge-readiness) with the review pull request identity, delivery kind epic, the epic base, the long-lived branch [Epic Bases](../artifacts/delivery-branches.md#epic-bases) names for it as target, and output paths.
   - Return to the caller each blocker the two report, leaving the pull request open.
4. **Merge or hand off.**
   Pass the confirmed epic readiness, the verified head and target requirements Fetch Merge Readiness returned, the repository setting and the passing evidence to [Merge Delivery Pull Request](../artifacts/pull-request.md#merge-delivery-pull-request) with delivery kind epic, without asking for further confirmation.
   - Return its handoff to the caller when a human reviewer must merge.
   - On a refusal, repeat steps 2 and 3 once with refreshed inputs, then this step. Return a second refusal to the caller.
5. **Confirm the result.**
   Apply [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state) for the merged pull request.
   - Return its merged state, head, target and merge commit to the caller.
