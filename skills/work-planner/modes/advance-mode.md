# Advance Mode

Decides which initiatives and epics on a theme board are underway and which are next, from current recorded delivery.

## Prerequisites

Read these files first.

- [Board](../artifacts/board.md)
- [Sync Mode](sync-mode.md)
- [Pull Request](../artifacts/pull-request.md)
- [Board Queue](../artifacts/board-queue.md)
- [Issue](../artifacts/issue.md)
- [Repository Labels](../artifacts/repository-labels.md)
- [Guidelines](../guidelines.md)

## Procedure

The main path meets [Outcomes](#outcomes).

1. **Select the board.**
   Run [Select Project Board](../artifacts/board.md#select-project-board) with the requested theme or board identity.
   - Use the returned owner and board number for the sync and fetch steps.
   - Resolve a pending theme selection before continuing.
2. **Sync.**
   Run [Sync Mode](sync-mode.md) for each open initiative on the selected board.
   - Wait for its saved delivery results before the fetch step.
   - Return any blocker that prevents current delivery from being established.
3. **Fetch.**
   - Run [Read Board State](../artifacts/board.md#read-board-state) for the current board items and Status field.
   - Run [Fetch All Initiative Pull Requests](../artifacts/pull-request.md#fetch-all-initiative-pull-requests) for the [repositories](../artifacts/board.md#repositories) Read Board State returned.
   - Run [Fetch Pull Request Issue Links](../artifacts/pull-request.md#fetch-pull-request-issue-links) for those pull requests, which is where the issue each one delivers is read.
   - Run [Read Board Configuration](../artifacts/board.md#read-board-configuration) for the board fields.
   - Run [Read Board Assignee](../artifacts/board.md#read-board-assignee) for the assignee login.
4. **Plan.**
   Call [Plan Board Queue](../artifacts/board-queue.md#plan-board-queue) with the selected board identity, current board items with Status, initiative pull request records, board fields, assignee login and an output directory such as `board/`.
   - Include every resolved off-board issue file and confirmed unplanned initiative identity.
5. **Resolve missing evidence.**
   For each unresolved issue reference:
   - Run [Read Tracker Issue](../artifacts/issue.md#read-tracker-issue) into a file.
     - Add the returned file to the resolved off-board issue files.
   - Call [Plan Board Queue](../artifacts/board-queue.md#plan-board-queue) with the current board items, initiative pull request records, board fields, assignee login, board identity and output directory, retaining every resolved issue file and confirmed unplanned initiative identity.
   - Repeat while references remain unresolved; an unavailable issue leaves the queue pending.
6. **Resolve queue decisions.**
   Ask only from an `order` or `ask` line in [Report Lines](../artifacts/board-queue.md#report-lines).
   - Follow the interview rules in the [guidelines](../guidelines.md#modes).
   - For `order`, ask for the [parallel work map](../artifacts/board-queue.md#priority-sets): a positive integer on each listed initiative, or leave it unordered.
   - For `ask`:
     - Ask for a positive integer or none.
     - Record the initiative's identity as confirmed unplanned when the user chooses none.
   - After an answer:
     - Call [Ensure Repository Labels](../artifacts/repository-labels.md#ensure-repository-labels) with the priority label each confirmed number names, for every repository holding one of those initiatives.
     - Call [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with each initiative identity and its confirmed priority-label addition.
     - Run [Read Board State](../artifacts/board.md#read-board-state) again.
     - Call [Plan Board Queue](../artifacts/board-queue.md#plan-board-queue) with the refreshed board items, the same initiative pull request records, board fields, assignee login, board identity and output directory, and every resolved off-board issue file and confirmed unplanned initiative identity.
   - Resolve any further missing evidence through step 5.
   - Repeat this step while a decision is pending. An unanswered question leaves the queue pending.
7. **Write.**
   Once the queue is [complete](../artifacts/board-queue.md#completeness), run each proposed Status and assignee call it returned.
   - Run [Read Board State](../artifacts/board.md#read-board-state) again.
   - Call [Plan Board Queue](../artifacts/board-queue.md#plan-board-queue) with the refreshed board items, the same initiative pull request records, board fields, assignee login, board identity and output directory, retaining every resolved off-board issue file and confirmed unplanned initiative identity.
   - Resolve new missing evidence or decisions through steps 5 and 6.
   - Repeat this step until the refreshed queue is complete and contains no further call.
8. **Report.**
   Report each move and each `order`, `ask`, `wait` and `next` line using [Report Lines](../artifacts/board-queue.md#report-lines).

## Outcomes

- **A queue.**
  The user has a queue for one theme: which initiatives are underway together, which are next, and which wait.
- **A parallel work map.**
  Initiatives the user ranks with the same priority run together. One left unordered waits.
- **Epics follow the initiative.**
  On the initiative that is underway, the epics planned to start together can start, and a partly completed epic stays underway.
