---
prosiform:
  root: ".."
  group: "protocols"
  group-depth: 1
---
# Change Overview

The published architecture overview, planning record and pull request link that explain one pull request's change.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md).

## Procedure

1. **Prepare the evidence.**
   Apply [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state) with the supplied repository and pull request number for its identity, title, base and head.
   - Apply [Create Pull Request Worktree](../artifacts/delivery-branches.md#create-pull-request-worktree) with the repository, its checkout, the pull request number and that head.
   - Return a changed-head finding to the caller.
   - Apply [Measure Repository Change](../artifacts/repository-graph.md#measure-repository-change) with the returned worktree, its head and the pull request's base.
   - Return a freshness blocker to the caller before writing the overview.
2. **Locate the record.**
   Apply [Locate Planning Record](../artifacts/planning-record.md#locate-planning-record) with the pull request number.
   - **Record found.**
     - Take the returned folder path and its record identity.
   - **No record.**
     - Take a new overview record's identity and folder path, meeting [Layout](../artifacts/planning-record.md#layout), from the pull request's number and title.
   - Apply [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record) with that record identity and folder path.
3. **Write the overview.**
   Apply [Populate Architecture Overview](../artifacts/architecture-overview.md#populate-architecture-overview) with the measured structure and flows, the head from step 1, pinned code permalinks and an overview path in the record's folder.
4. **Register the overview.**
   Apply [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record) with the record identity, folder path, the returned overview file and the pull request link, meeting [Artifacts](../artifacts/planning-record.md#artifacts), and a commit message file naming that folder, asking it to publish.
   - Return a publication discrepancy to the caller.
5. **Link the pull request.**
   Apply [Link Architecture Overview](../artifacts/pull-request-body.md#link-architecture-overview) with the current body, the published overview URL and an output body path.
   - Apply [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request) with the repository, pull request number and returned body file.
   - Return the pull request, record folder, published overview, diagrams and References row to the caller.
