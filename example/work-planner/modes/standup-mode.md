---
prosiform:
  root: ".."
---
# Standup Mode

Summarises a project board as a standup, in Slack markup for pasting into a channel: a paragraph for management on what the window accomplished, then what completed, what is in progress, and what is next. The board's Status is the source, so the summary is as current as the board.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md) and ensure all [Outcomes](#outcomes) are met.

## Procedure

1. **Select the scope.**
   Apply [Select Project Board](../artifacts/board.md#select-project-board) for the requested board, each requested board when the scope is all, or the theme board of the named initiative.
   - Retain the selected window and initiative filter.
   - Complete steps 2–6 separately for each selected board.
2. **Bring delivery current.**
   - Use the delivery results and board state a caller passed in, where this run follows one that already brought the board current. A request made directly by the user supplies none, so the checkpoint is absent.
   - If the checkpoint is absent:
     - Read the board through [Read Board State](../artifacts/board.md#read-board-state).
     - Treat each selected initiative's delivery state as needing refresh.
   - For initiatives with known delivery changes or unknown freshness, follow [⇉ Sync Mode](sync-mode.md) for the affected initiatives on that board.
   - Resume the read step after their delivery results are saved.
   - Report a blocker that prevents a current summary.
   - Retain it as a gap if presenting a partial report.
3. **Read the evidence.**
   Apply [Read Board Delivery Evidence](../artifacts/delivery-evidence.md#read-board-delivery-evidence) with the selected board owner and number, authenticated access, output paths and destination snapshot files.
   - Retain incomplete evidence as a gap.
4. **Compose.**
   Apply [Compose Standup Report](../artifacts/standup-report.md#compose-standup-report) with the returned board items, pull request records and complete issue-link snapshot, the selected window and initiative filter, and output paths.
5. **Repair.**
   For an epic the report names with an unreadable Work Breakdown, apply [Repair Issue Format](../artifacts/issue-body.md#repair-issue-format) with [Validate Epic Body](../artifacts/epic-issue-body.md#validate-epic-body) as the validator and its further inputs, the epic identity, current JSON and output body path, the [epic template](../artifacts/epic-issue-body.md#template) and required related evidence.
   - If it confirms a saved correction, repeat steps 3–6, retaining the selected board, window and initiative filter.
   - If it reports a blocker or no correction, carry the unresolved finding to the report without repeating the same repair.
6. **Report.**
   Present the returned report verbatim in a fenced block for copying.
   - Put unresolved findings and gaps beneath it.

## Outcomes

- **A standup for the window.**
  The user has a summary they can paste, of what the window accomplished, what completed, what is in progress, and what is next.
- **Current with the board.**
  The summary matches the board's Status.
- **The board they asked for.**
  The summary covers the board they name, every board, or the one initiative they name.
- **A paragraph for management.**
  The user has one paragraph on what the window delivered for the initiatives it serves.
