---
prosiform:
  root: ".."
  group: "protocols"
  group-depth: 1
---
# Epic Closure

An epic whose delivery is recorded carried through review and integration of its bases to its closure, with its initiative's delivery recorded.

## Procedure

1. **Open the review.**
   For each epic base the epic's [Delivery Findings](../artifacts/epic.md#delivery-findings) name as unmerged with no open pull request, follow [Review Pull Request](review-pull-request.md) with those findings, the task merges into that base, the epic's issue and the confirmed repository setting.
2. **Integrate each base.**
   For each open epic pull request, follow [Epic Integration](epic-integration.md) with the epic identity and body, review identity, project checkout, current delivery records, complete issue-link snapshot and criterion verification evidence.
   - Return a draft awaiting the user's ready mark, or a blocker, to the caller as pending.
   - Stop while any epic base remains unmerged.
3. **Refresh the records.**
   Apply [Read Delivery Evidence](../artifacts/delivery-evidence.md#read-delivery-evidence) with the repositories and initiative prefix, the epic's current JSON, authenticated access and destination snapshot files.
   - Apply [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery) with the epic JSON, the returned pull request records and complete issue-link snapshot, task issue records, confirmed matches, project checkout and output body file.
   - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the returned body when it differs from the current one.
4. **Close the epic.**
   Follow [Issue Closure](issue-closure.md) for the epic with the confirmed repository setting, criterion verification evidence and project checkout.
5. **Record the initiative.**
   Apply [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue) for the initiative and every epic it links.
   - Apply [Record Initiative Delivery](../artifacts/initiative-issue-body.md#record-initiative-delivery) with the initiative JSON, every linked epic's current JSON and an output body file.
   - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the returned body when it differs from the current one.
   - Apply [Record Verified Criteria](../artifacts/acceptance-criteria.md#record-verified-criteria) with the repository, the criteria its [Delivery Findings](../artifacts/initiative.md#delivery-findings) name as ready to verify, the saved initiative JSON and body, those findings, delivery revisions, named instruments, project checkout, output body file and every linked epic record.
   - Return the epic's closure result, the initiative's saved identity, its verified criteria with their evidence and its remaining findings to the caller.
