---
prosiform:
  root: ".."
---
# Advance Mode

Decides which initiatives and epics on a theme board are underway and which are next, from current recorded delivery.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md) and ensure all [Outcomes](#outcomes) are met.

## Procedure

1. **Select the board.**
   Apply [Select Project Board](../artifacts/board.md#select-project-board) with the requested theme or board identity.
   - Use the returned owner and board number for the sync and read steps.
   - Resolve a pending theme selection before continuing.
2. **Sync.**
   Follow [⇉ Sync Mode](sync-mode.md) for each open initiative on the selected board, with the allowance the caller supplied.
   - Wait for its saved delivery results before the read step.
   - Return any blocker that prevents current delivery from being established.
3. **Read the evidence.**
   Apply [Read Board Delivery Evidence](../artifacts/delivery-evidence.md#read-board-delivery-evidence) with the selected board owner and number, authenticated access, output paths and destination snapshot files.
   - Return incomplete evidence as a blocker.
4. **Apply the queue.**
   Apply [Apply Board Queue](../artifacts/board-queue.md#apply-board-queue) with the board identity, the returned board items with Status, initiative pull request records, board fields and assignee login, an output directory such as `board/`, every resolved off-board issue file and every confirmed unplanned initiative identity.
   - Return a reference it reports as missing evidence as a blocker; the queue stays pending.
   - When it returns pending decisions, settle them in the decide step, then return to the read step.
5. **Decide.**
   For each pending `order` or `ask` line, a re-prioritisation as [Report Lines](../artifacts/board-queue.md#report-lines) states, apply [Settle Plan Change](../artifacts/plan-change.md#settle-plan-change) with the line, the initiatives it names, its [recommended decision](../artifacts/board-queue.md#recommended-decisions), those initiatives' identities, the allowance the caller supplied and the run's [change list](../artifacts/plan-change.md#change-list).
   - For each initiative an applied option or answer numbers, apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with its identity and the [priority label](../artifacts/board-queue.md#priority-sets) that number names, with the label's colour and description.
   - Add each initiative an `ask` answer leaves with no number to the confirmed unplanned initiative identities.
   - A held or unanswered line leaves the queue pending: report it and continue at the report step.
6. **Report.**
   Report each move and each `order`, `ask`, `wait` and `next` line using [Report Lines](../artifacts/board-queue.md#report-lines).
   - Return the change list with the queue, so the caller reports each decision this mode made and each it held.

## Outcomes

- **A queue.**
  The user has a queue for one theme: which initiatives are underway together, which are next, and which wait.
- **A parallel work map.**
  Initiatives ranked with the same priority run together. One left unordered waits.
- **Epics follow the initiative.**
  On the initiative that is underway, the epics planned to start together can start, and a partly completed epic stays underway.
