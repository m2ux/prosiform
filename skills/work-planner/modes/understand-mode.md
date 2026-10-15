# Understand Mode

Explains the named pull request's changes through a measured architecture overview and publishes that overview for its reviewer.

## Prerequisites

Read these files first.

- [Pull Request](../artifacts/pull-request.md)
- [Delivery Branches](../artifacts/delivery-branches.md)
- [Repository Graph](../artifacts/repository-graph.md)
- [Planning Record](../artifacts/planning-record.md)
- [Architecture Overview](../artifacts/architecture-overview.md)
- [Pull Request Body](../artifacts/pull-request-body.md)

## Procedure

The main path meets [Outcomes](#outcomes).

1. **Select the change.**
   - Require the pull request number or URL.
   - Ask and stop when none is supplied. Do not infer it from the current branch.
   - For several supplied pull requests, complete one overview per pull request. An initiative has no overview of its own.
   - Read the pull request identity, title, base and verified head through [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state).
2. **Prepare the evidence.**
   - Call [Create Pull Request Worktree](../artifacts/delivery-branches.md#create-pull-request-worktree) with the repository checkout, pull request number, verified head and worktree path.
   - On a changed-head finding:
     - Repeat Read Pull Request State for the same pull request.
     - Repeat Create Pull Request Worktree using its new verified head.
   - Continue to measurement only when the worktree matches that head.
   - Obtain its changed paths through [Read Pull Request State](../artifacts/pull-request.md#read-pull-request-state).
   - Call [Measure Repository Change](../artifacts/repository-graph.md#measure-repository-change) with that worktree, head and base.
   - On stale index evidence, repeat Measure Repository Change after its index update.
   - On a changed revision:
     - Repeat Read Pull Request State.
     - Rebuild the worktree evidence.
   - Return any unresolved freshness blocker before writing the overview.
3. **Write the overview.**
   - Locate any existing overview record for this pull request number before creating a record.
   - Reuse its folder identity when one exists; otherwise choose a planning-folder identity whose reference is the pull request number and whose slug comes from its title.
   - Call [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record) to prepare that folder.
   - Run [Populate Architecture Overview](../artifacts/architecture-overview.md#populate-architecture-overview) with the measured structure and flows, verified head, pinned code links and overview path. A repeat replaces its overview while preserving the record's other content.
4. **Register the overview.**
   Call [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record) with the record identity, folder, overview file and pull request link. The overview is its one Artifacts row and the pull request is under Links.
5. **Publish and link.**
   - Commit the engineering worktree.
   - Push its branch so the overview resolves.
   - Call [Link Architecture Overview](../artifacts/pull-request-body.md#link-architecture-overview) with the current body and published overview URL.
   - Publish the returned file through [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request).
6. **Report.**
   - Report the pull request, record folder, diagrams and References row.

## Outcomes

- **The change explained.**
  The engineer reviewing the pull request has its structure and its flows, read at the head commit under review.
- **The pull request named.**
  The account is of the pull request the request names, of the open pull request a task in review names, or of each base an epic in review delivers. An initiative has none of its own.
- **One account.**
  The same pull request yields one account, and a later run replaces it with the current change.
