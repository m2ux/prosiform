---
prosiform:
  root: ".."
  group: "protocols"
  group-depth: 1
---
# Issue Placement

One orphan's work saved in its confirmed destination, with the orphan rewritten or closed as its disposition states.

## Procedure

1. **Populate the destination.**
   Apply [Apply Issue Placement](../artifacts/placement.md#apply-issue-placement) with the confirmed placement, the current source and destination records, the affected initiative and epic bodies, and an output path for each body the placement changes.
   - Use the returned body files, temporary links, destination and disposition in the steps below.
2. **Check the graph.**
   When the placement adds a task or an epic, apply [Check Dependencies and Numbering](../artifacts/dependency-graph.md#check-dependencies-and-numbering) with the initiative and epic body files as local drafts, the planning record that registered each task row, current pull request records, the confirmed numbering map when there is one, the caller's allowance when it has one, and the run's current change list.
   - Use the checked bodies it returns in the steps below, and carry its updated change list.
   - Return a failed renumbering to the caller as a blocker before any save.
3. **Save the bodies.**
   - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) for each new issue the placement returns, with the repository, its body file, title and labels, and each label's colour and description.
   - When the placement returned a temporary link, apply [Resolve Placeholder Links](../artifacts/initiative-issue-body.md#resolve-placeholder-links) with the initiative body file, each epic body file and the saved issue identities.
     - Return a temporary link left unresolved, with the file that holds it, to the caller as a blocker.
   - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the body change for each existing issue whose body file changed, a newly saved issue whose links were resolved among them.
4. **Record the graph.**
   When step 2 ran and the initiative has a planning record, apply [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record) with the record identity, folder path, the longest chains, contending pairs and proposed [Epic Priority](../artifacts/dependency-graph.md#epic-priority) map that Check Dependencies and Numbering returned as its [Dependency Check](../artifacts/planning-record.md#dependency-check), the saved destination issue links, and the caller's commit message file when it asks to publish.
5. **Settle the orphan.**
   By the returned disposition:
   - **Kept or left.**
     - Apply [Rewrite Orphan Issue](../artifacts/placement.md#rewrite-orphan-issue) with the orphan's identity, the selected destination kind, and the evidence and design its body carries.
   - **Subsumed.**
     - Apply [Subsume Orphan Work](../artifacts/placement.md#subsume-orphan-work) with the orphan's identity and the saved destination evidence.
   - Return the saved destination, every affected issue identity, the orphan's rewrite or closure, the proposed Epic Priority map, the updated change list, and each unresolved finding or blocker to the caller.
