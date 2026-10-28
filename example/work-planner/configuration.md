---
prosiform:
  root: "."
---
# Configuration

The values one deployment of this skill sets: the labels it writes, the boards and fields it reads, the branch its planning records live on, and the limits of its reports. Each is stated here once, and every file using one links its entry.

## Labels

### Kind Labels

The label naming an agent-engineering issue's kind.

| Kind | Label |
| --- | --- |
| Proposal | `type:proposal` |
| Initiative | `type:initiative` |
| Epic | `type:epic` |
| Task | `type:task` |

### Theme Labels

The label naming the theme an initiative and its epics belong to: `theme:` and the theme's name in lowercase. This deployment's themes:

| Theme | Label | Description |
| --- | --- | --- |
| Canon | `theme:canon` | Definitions Checked Against the Design Canon |
| Language | `theme:language` | The Definition Language and Its Rules |
| Mechanical | `theme:mechanical` | The Engine That Runs Definitions |
| Delivery | `theme:delivery` | What Reaches Agents and Hosts |

### Priority Labels

The label carrying a priority set: `priority:` and a positive integer `<n>`.

- **Colour.**  `BFD4F2`.
- **Description.**  `Priority set <n>; a larger number starts sooner`, with `<n>` its integer.

## Boards

### Proposals Board

The board holding proposal issues, titled `Proposals`.

### Board Templates

The open boards a new board is copied from, by exact title.

| Board | Template title |
| --- | --- |
| Proposals board | `Proposals Template` |
| Theme board | `Initiative Template` |

### Status Field

The single-select field a board item's status is read from and written to, named `Status`.

- **Theme board options.**  Backlog, Ready, In Progress, In Review and Done.
- **Proposals board options.**  Suggested, Considering, Approved, Held and Declined.

### Proposals Priority Field

The single-select field `Priority` on the proposals board, with the options High, Medium and Low.

## Planning Records

### Engineering Branch

The long-lived branch holding every planning record, named `engineering`, checked out in one worktree.

- **Records folder.**  `artifacts/planning/`, relative to that worktree.

## Standup

### Standup Window

The default reporting window opens one week before today.

### Standup Ready Count

The number of Ready items the report lists by name: 5.
