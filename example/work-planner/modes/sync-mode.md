---
prosiform:
  root: ".."
---
# Sync Mode

Records delivery on an initiative, its epics, and their task issues. Each task that has a pull request is linked to that pull request, open or merged. Criteria that now hold are recorded, complete rows are marked done, complete issues are closed, and the initiative's theme board is brought up to date.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md) and ensure all [Outcomes](#outcomes) are met.

## Procedure

1. **Select.**
   Select an initiative with its open epics, or the epics the user names.
   - Apply [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue) for the initiative, each selected epic and each task issue under it, titled as [Titles](../artifacts/task-body.md#titles) states.
   - Apply [Repair Issue Format](../artifacts/issue-body.md#repair-issue-format) once per kind, with that kind's validator — [Validate Initiative Body](../artifacts/initiative-issue-body.md#validate-initiative-body), [Validate Epic Body](../artifacts/epic-issue-body.md#validate-epic-body), or [Validate Issue Body](../artifacts/issue-body.md#validate-issue-body) with the task [Fields](../artifacts/task-body.md#fields) — its further inputs, each fetched body with its identity, current JSON and output body path, the kind template and required related evidence.
     - Use the saved bodies it returns in the following steps.
     - Return a remaining format failure as a blocker.
   - Apply [Confirm Repository Auto-Close](../artifacts/issue.md#confirm-repository-auto-close) for the repository holding the issues, and pass the confirmed setting to every protocol this run follows.
2. **Record delivery.**
   Follow [⇉ Delivery Recording](../protocols/delivery-recording.md) with the selected repositories and initiative prefix, the fetched epic JSON and task issue records, the project checkout, named instruments, the confirmed setting, the allowance the caller supplied, the run's [change list](../artifacts/plan-change.md#change-list), and output body and comment files.
   - Route what it returns:
     - **Unnamed deliveries.**
       - Put each [unnamed delivery](../artifacts/delivery-evidence.md#unnamed-deliveries) to the user as an [interview](../rules.md).
       - For each the user confirms, apply [Publish Pull Request](../artifacts/pull-request.md#publish-pull-request) with its repository and number and the title [Named Delivery](../artifacts/delivery-evidence.md#named-delivery) states.
       - Follow Delivery Recording again with the same inputs.
     - **Incomplete evidence.**
       - Return it as a blocker.
     - **Pending matches, rows and open questions.**
       - Report each as pending; the epic it concerns stays open.
     - **Conflicts and disagreements.**
       - Report each as unresolved with its pull request and row.
3. **Close each epic.**
   For each selected epic, follow [⇉ Epic Closure](../protocols/epic-closure.md) with the repository, initiative prefix and project checkout, the epic JSON, issue and body with its criterion ids and named instruments, its latest Delivery Findings, task issue records, confirmed matches and the task-merge records among the pull request records, the confirmed setting, and the criterion verification evidence Delivery Recording returned.
   - Report a draft awaiting the user's ready mark, a blocker and each remaining finding it returns as pending.
4. **Close the initiative.**
   Follow [Issue Closure](../protocols/issue-closure.md) for the initiative with the confirmed setting, the criterion verification evidence Epic Closure returned for it and the project checkout.
   - Report an incomplete result with its unmet criteria and open epics.
5. **Sync the board.**
   Apply [Ensure Project Board](../artifacts/board.md#ensure-project-board) with the owner, repository, the initiative's theme name and title, and the originating proposal's identity its [References](../artifacts/initiative-issue-body.md#references) name when a proposal derives the theme.
   - Return a missing selection or unresolved provenance as a blocker.
   - Apply [Record Board Delivery](../artifacts/board-delivery.md#record-board-delivery) with the saved initiative, epic and task identities, the returned board identity and an output directory.
6. **Explain each change entering review.**
   For each task or epic Record Board Delivery newly moves to In Review, follow [Understand Mode](understand-mode.md) with the task's open pull request or each epic review pull request, one run per base, where [Ownership](../artifacts/architecture-overview.md#ownership) gives the overview to this run.
   - Complete each overview before continuing.
7. **Report.**
   Return saved delivery results and unresolved findings to the caller, or present them to the user for a direct request.
   - Report queue decisions unevaluated by this run.
   Report per issue: tasks linked, criteria ticked, rows marked done, criteria left unticked and why, conflicts, test plan disagreements, what was closed, each board and assignee change, and each overview written. What the report names about criteria is [Coverage Reports](../artifacts/issue-body.md#coverage-reports).

## Outcomes

- **Delivery recorded.**
  The user has each landed task tied to the pull request that delivered it, and has what now holds recorded on the initiative and its epics.
- **Complete work closed.**
  Work that is complete is closed.
- **The board is current.**
  The theme board shows where the initiative and its epics stand, including what a reviewer can take up.
- **A change entering review is explained.**
  Each task and epic that enters review has an overview on the pull request a reviewer reads.
- **The queue stays undecided.**
  A sync on its own leaves the choice of what to start next undecided.
