---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Standup Report

A board progress report for a selected window, formatted for pasting into Slack.

## Operations

### Compose Standup Report

The copyable report and any missing-evidence findings.

**Inputs:** [Board items](board.md#board-items), [Pull request records](pull-request.md#pull-request-records), [Issue-link snapshot](pull-request.md#issue-link-snapshot), [Window start](#scope), [Initiative filter](#scope), [Off-board initiatives](issue.md#issue-record), [Output paths](#report-files)

**Outputs:** [Standup report](#sections), [Unresolved evidence](#unresolved-evidence)

#### 1. Require the Standup Link Snapshot

Require the complete issue-link snapshot.

#### 2. Summarise Standup Progress

Apply [Render Standup Report](#render-standup-report) with the board items, pull request records, complete issue-link snapshot, the supplied window start and initiative filter, and every supplied off-board initiative record.

#### 3. Resolve Off-Board Initiatives

Read the preliminary summary’s result as [Command result](../conventions.md#command-result) states. Continue with unresolved-initiative findings.

For each unresolved initiative the summary names:
- Apply [Locate Initiative Issue](issue.md#locate-initiative-issue) with its repository and initiative prefix.
- Apply [Read Tracker Issue](issue.md#read-tracker-issue) for the located issue's current JSON into a file under the output paths.
- Add the returned file to the resolved off-board initiative records.
- Apply [Render Standup Report](#render-standup-report) again with the same inputs and every resolved initiative record.

Read each summary’s result as [Command result](../conventions.md#command-result) states and its unresolved initiatives. Repeat while an initiative remains that no read has failed. An unavailable initiative stays an unresolved finding, a gap in the report.

#### 4. Write the Management Paragraph

Write the management paragraph from the rendered Initiatives and Completed sections.
- It must meet [Management Paragraph](#management-paragraph).

#### 5. Render the Final Standup Report

Apply [Render Standup Report](#render-standup-report) with the same inputs and the completed management paragraph file.

#### 6. Return the Standup Report

Read the final renderer’s result as [Command result](../conventions.md#command-result) states. Return an execution failure as a blocker, retaining any unresolved evidence separately.

Return the report and separate unresolved findings.
- The report must meet [Fields](#fields).

### Render Standup Report

The report text for one set of board, delivery and window inputs.

**Inputs:** [Board items](board.md#board-items), [Pull request records](pull-request.md#pull-request-records), [Issue-link snapshot](pull-request.md#issue-link-snapshot), [Window start](#scope), [Initiative filter](#scope), [Off-board initiatives](issue.md#issue-record), [Management paragraph](#management-paragraph)

**Outputs:** [Standup report](#sections)

#### 1. Render the Report

From `<workspace>`, render the report using board items as `--items`, pull requests as `--prs`, the complete link snapshot as `--links`, and any supplied window start, initiative filter, off-board initiative records and management paragraph.

- `--links` is the supplied complete pull-request issue-link snapshot; it identifies the issue each pull request delivers.
- `--since` opens the window on another date than the [Standup Window](../configuration.md#standup-window) default.
- `<initiative-filter>` is an initiative id, or `<owner>/<repo>:<initiative-id>` where that id names initiatives in several repositories. **Examples:** `I08`, `owner/repo:I08`.
- `--initiatives` gives supplied off-board initiative records, each as a separate file argument.
- `--summary` gives the paragraph for management.

The optional flags may be combined or omitted. Omitting all four uses the default window and all initiatives with no off-board records or management paragraph. **Example combinations:** a focused report can use `--since 2026-09-21 --initiative I08`; resolving an off-board initiative adds `--initiatives issue-946.json`; the final report adds `--summary summary.txt` to the same inputs.

`<window-start-date>` uses `YYYY-MM-DD`.

Runs as [Helper invocation](../conventions.md#helper-invocation) states.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/progress.py --items '<board-items-file>' --prs '<pull-request-records-file>' --links '<issue-link-snapshot-file>' --since '<window-start-date>' --initiative '<initiative-filter>' --initiatives '<initiative-json-file>' --summary '<management-paragraph-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/progress.py --items items.json --prs prs.json --links links.json --since 2026-09-21 --initiative I08 --initiatives issue-946.json --summary summary.txt
```

#### 2. Return the Rendered Report

Read the renderer’s result as [Command result](../conventions.md#command-result) states. Return the report and its unresolved evidence.

## Fields

### Scope

The default window opens as the [Standup Window](../configuration.md#standup-window) sets. A supplied start date selects another window, such as the previous working day for a daily standup. An initiative filter names one initiative, qualified by repository when its number is ambiguous.

Each repository numbers its own initiatives, and an initiative's epics and task issues may live in other repositories. Each item's place follows the Work Breakdown links, or for a task issue the pull request whose Development field links it. A pull request counts towards the epic of its reference in the epic's repository or its initiative's.

### Sections

The management paragraph is set off by blank lines, with the board's link beneath the heading.

- **Initiatives.**
  One line for each initiative with work under Completed or In progress, its title's name and subtitle, opening with the mark of its state. One off the board is done when closed, else in progress. An item works for the initiative whose table links its epic and for the one its epic's title names.
- **Completed.**
  Items Done whose issue closed in the window, grouped under their epic, and tasks whose pull requests merged in it. Closing is when an issue became Done; an issue the board caught up with later still falls on its closing date.
- **In progress.**
  Epics and task issues In Progress or In Review, each epic with its open pull requests, or else its next task.
- **Next.**
  The Ready items the [Standup Ready Count](../configuration.md#standup-ready-count) sets, each epic with its next task, and a count of the rest.
  - They rank by the priority label of the initiative their epic belongs to, then by their epic's own.
  - An epic is placed ahead of any listed epic naming it, so a supplier reads before the work drawing on it. An epic names another when a task row names one of its rows or the initiative row names it whole.
- **Key.**
  I Initiative, E Epic and W Work Item. Opening marks are ✅ done, 🔄 in progress (an initiative or epic open and not In Review), 👀 in review, 📝 draft and ▶️ ready.

### Management Paragraph

One plain-language paragraph describes what the window delivered as outcomes for the initiatives it serves, grounded in Initiatives and Completed. It carries no references, links, task ids or tool names, and leaves out work in progress and next. With nothing completed, it says so in one sentence.

### Unresolved Evidence

An unresolved initiative identifies its number and repository. An off-board dependency is blocked. An epic with unreadable Work Breakdown is summarised without tasks and returned as a finding. Unresolved lines are separate from the copyable report.

### Report Files

The local paths the report's working JSON and text are written into: each off-board initiative's issue JSON and the management paragraph file.
