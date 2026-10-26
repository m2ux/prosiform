---
prosiform:
  root: ".."
  group: "protocols"
  group-depth: 1
---
# Delivery Recording

The task and epic records brought to the delivery an initiative's pull requests establish, with the findings that delivery leaves routed.

## Procedure

1. **Read the evidence.**
   Apply [Read Delivery Evidence](../artifacts/delivery-evidence.md#read-delivery-evidence) with the selected repositories and initiative prefix, each selected epic's fetched JSON, authenticated access and destination snapshot files.
   - Use its pull request records, complete issue-link snapshot and per-epic [Delivery Findings](../artifacts/epic.md#delivery-findings) in the following steps.
   - Return its [unnamed deliveries](../artifacts/delivery-evidence.md#unnamed-deliveries) and any incomplete evidence to the caller with the result.
2. **Match deliveries to tasks.**
   For each selected epic, apply [Match Delivery to Tasks](../artifacts/epic.md#match-delivery-to-tasks) with the epic JSON and the pull requests its Unmatched and In flight findings name, and those linked to the task issue a Note row links, with their changes and descriptions.
   - Use the confirmed task-to-pull-request pairs in the following steps.
   - Return the pending matches to the caller.
3. **Record each merged delivery.**
   For each confirmed match whose pull request has merged:
   - Follow [Issue Delivery](issue-delivery.md) with that pull request, its matched tasks' issue records, the epic JSON, the pull request records, complete issue-link snapshot, confirmed matches, project checkout, named instruments, the caller's allowance and change list, and output body and comment files.
   - Follow [Issue Closure](issue-closure.md) for each task issue whose delivery result it returns as eligible, with the confirmed repository setting.
4. **Record each epic.**
   For each selected epic, apply [Record Epic Delivery](../artifacts/epic-issue-body.md#record-epic-delivery) with its current JSON, the pull request records, complete issue-link snapshot, task issue records, every confirmed match, open or merged, project checkout and output body file.
   - Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the returned body when it differs from the current one.
   - Route the returned [Delivery Findings](../artifacts/epic.md#delivery-findings):
     - **Conflict.**
       - Return each to the caller as an unresolved finding.
     - **Unmatched, in flight or note.**
       - Apply Match Delivery to Tasks with the pull requests it names, or for a note those linked to the row's task issue.
       - Add the confirmed pairs to the matches.
     - **Draft or references.**
       - Follow [Review Pull Request](review-pull-request.md) with the repository, the epic base it names, the delivery findings, the actual task merges into that base, the epic's issue, the confirmed repository setting and the current epic and task-merge records.
     - **Unmerged.**
       - Return the epic base to the caller with its review identity.
     - **Uncited.**
       - Apply [Link Pull Request to Issue](../artifacts/pull-request.md#link-pull-request-to-issue) with the pull request and issue it names, the pull request records, link-snapshot destination, authenticated access and confirmed repository setting.
       - Use its refreshed snapshot in the following steps.
     - **Unplaced.**
       - Apply [Place Unplaced Task Row](../artifacts/epic-issue-body.md#place-unplaced-task-row) with the epic JSON, the unplaced task issue, the caller's allowance and change list, the pull request records, complete issue-link snapshot, task issue records, confirmed matches, project checkout and output body file.
       - Return a row it leaves pending to the caller with the updated change list.
     - **Open questions.**
       - Apply [Resolve Open Questions](../artifacts/issue-body.md#resolve-open-questions) with the epic identity, current JSON, the epic [Template](../artifacts/epic-issue-body.md#template) and [Fields](../artifacts/epic-issue-body.md#fields), the initiative as related context and an output body path.
       - Return the questions it leaves open to the caller.
     - **Ready to verify.**
       - Apply [Record Verified Criteria](../artifacts/acceptance-criteria.md#record-verified-criteria) with the repository, those criterion ids, the epic's current JSON and body, delivery findings, delivery revisions, named instruments, project checkout, output body file, pull request records and complete issue-link snapshot.
       - Retain its verified ids and evidence for the caller.
       - For each criterion it leaves unverified on an unmet row, as Delivery Findings defines one, apply [Plan Gap Task](../artifacts/epic-issue-body.md#plan-gap-task) with the current epic JSON and body, the delivered task row, those criterion ids, the delivery records, complete issue-link snapshot and output body path.
       - Apply Record Verified Criteria again for each criterion Plan Gap Task returns as already holding.
     - **Ticked early.**
       - Apply Match Delivery to Tasks for the delivery the criterion's rows lack.
       - Where no match is confirmed, apply [Apply Body Corrections](../artifacts/issue-body.md#apply-body-corrections) with the current body, the epic template and fields, the criterion unticked as the confirmed resolution and the output path.
       - Apply Save Tracker Issue with that corrected body.
     - **Disagreement.**
       - Return each to the caller with its pull request and row.
   - Repeat Record Epic Delivery, its save and this routing with the saved epic JSON, refreshed records and every confirmed match, until it returns no unmatched, in flight, uncited, note or unplaced finding beyond those returned to the caller as pending.
   - Return to the caller the saved epic and task identities, each epic's latest Delivery Findings, the verified criteria with their evidence, the pull request records and complete issue-link snapshot, the updated change list and every pending or unresolved finding.
