# Standup Mode

Summarises a project board as a standup, in Slack markup for pasting into a channel: a paragraph for management on what the window accomplished, then what completed, what is in progress, and what is next. The board's Status is the source, so the summary is as current as the board.

## Prerequisites

Command operations use the [Command Conventions](../SKILL.md#command-conventions), read before the first spec.

## Procedure

1. **Bring the board current.**
   When issues have closed or pull requests have merged since the board was last synced, run [Sync Mode](sync-mode.md) first: the summary reads each item's Status as it stands.
2. **Find the board.**
   Select it as [Select](board.md#select) states, or all, and summarise each board in turn.
3. **Fetch.** Read the board as [Read](board.md#read) states.
4. **Summarise.**  Run [Summarise Progress](#summarise-progress).
   - **Window.**
     The window opens a week before today. Give `--since` for another, such as the previous working day for a daily standup.
   - **One initiative.**
     Give `--initiative I08` when the user names one initiative, or `owner/repo:I08` where that number names initiatives in several repositories.
   - **Repositories.**
     Each repository numbers its own initiatives, and an initiative's epics and task issues may live in other repositories. Each item's place follows the Work Breakdown links, or for a task issue the pull request whose Development field links it, and a pull request counts towards the epic of its reference in the epic's repository or its initiative's.

   It prints the `--summary` paragraph, set off by blank lines, and the board's link beneath the heading, then:
   - **Initiatives.**
     - One line for each initiative with work under Completed or In progress, its title's name and subtitle, for context, opening with the mark of its state.
     - One off the board is done when closed, else in progress.
     - An item works for the initiative whose table links its epic and for the one its epic's title names.
   - **Completed.**
     - Items Done whose issue closed in the window, grouped under their epic, and the tasks whose pull requests merged in it.
     - Closing is when an issue became Done, so one the board caught up with later still falls on its closing date.
   - **In progress.**
     Epics and task issues In Progress or In Review, each epic with its open pull requests, or else its next task.
   - **Next.**
     The five Ready items ranked by priority label, each epic with its next task, and a count of the rest.
   - **Key.**
     - The reference letters: I Initiative, E Epic and W Work Item.
     - Each line's opening mark: ✅ done, 🔄 in progress (an initiative or epic open and not In Review), 👀 in review, 📝 draft, ▶️ ready.
5. **Give the initiatives off the board.**
   For each `unresolved` line naming an initiative not on the board (`I08 in owner/repo`), find its issue with [Find Initiative Issue](#find-initiative-issue) in that repository, take it with [Fetch Issue](commands.md#fetch-issue), and re-run [Summarise Progress](#summarise-progress) with `--initiatives`.
6. **Write the paragraph for management.**
   Write it from the Initiatives and Completed sections, to this mode's The paragraph rule, and re-run [Summarise Progress](#summarise-progress) with the same arguments and `--summary`.
7. **Report.**
   - Report the summary verbatim in a fenced block, so the user copies it unaltered.
   - Put any `unresolved` line it prints to stderr beneath:
     - A dependency on an issue off the board, which reads as blocked;
     - An epic whose Work Breakdown cannot be read, summarised without its tasks; [Align Mode](align-mode.md) fixes its body.

## Rules

- **The paragraph.**
  The paragraph for management:
  - is one paragraph in plain language: what the window delivered, as outcomes for the initiatives it serves;
  - carries no references, links, task ids or tool names;
  - leaves out work in progress and next;
  - with nothing completed, says so in one sentence.

## Commands

### Find Initiative Issue

Prints an initiative's issue number, found by its title's prefix.

```bash
gh api --paginate "repos/{owner}/{repo}/issues?state=all&per_page=100" --jq '.[] | select(.pull_request == null) | select(.title | startswith("[I08]")) | .number'
```

### Summarise Progress

Prints the standup from [Fetch Board Items with Status](sync-mode.md#fetch-board-items-with-status) and [Fetch All Initiative Pull Requests](board.md#fetch-all-initiative-pull-requests).

- `--links` is the file [Fetch Pull Request Issue Links](commands.md#fetch-pull-request-issue-links) writes for those pull requests, and is where the issue a pull request delivers is read. A call without it is refused.
- `--since` opens the window on another date than a week before today.
- `--initiative I08` limits it to one initiative, or `owner/repo:I08` where that number names initiatives in several repositories.
- `--initiatives` gives the initiatives off the board, each from [Fetch Issue](commands.md#fetch-issue).
- `--summary` gives the paragraph for management.

```bash
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/progress.py --items items.json --prs prs.json --links links.json
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/progress.py --items items.json --prs prs.json --links links.json --since 2026-09-21 --initiative I08
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/progress.py --items items.json --prs prs.json --links links.json --initiatives issue-946.json
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/progress.py --items items.json --prs prs.json --links links.json --since 2026-09-21 --initiative I08 --summary summary.txt
```
