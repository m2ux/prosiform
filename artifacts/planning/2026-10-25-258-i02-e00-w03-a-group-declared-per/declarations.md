# Declarations — W03

> Delivery Record · Created 2026-10-25

## Overview

The declaration this row makes, recorded before the edit, and what each file
carried when it was recorded. Every file under `example/work-planner` declared
`root` and nothing else, so the three keys this row adds are the only change to
any file's frontmatter.

## The Table

| Folder | Group | Depth | Heading emitted | Files |
| --- | --- | --- | --- | --- |
| `artifacts/` | `artifacts` | 2 | no | 30 |
| `protocols/` | `protocols` | 1 | yes | 6 |
| `references/` | `references` | 1 | yes | 1 |
| `modes/` | none | — | — | 10 |
| top level (`SKILL.md`, `guidelines.md`) | none | — | — | 2 |
| **Grouped** | | | | **37** |
| **Ungrouped** | | | | **12** |
| **Total** | | | | **49** |

`group-heading` is written only on the 30 artifact files, because depth 2 stores
the artifacts' own H1s one level down and a heading over them would name a
folder the reader already sees in the member headings. The two depth-1 groups
emit their declared name as the group's H1 by leaving the key absent, which is
the default.

## What Each File Carried

Recorded from the branch head `dab65c4c`, reading the leading frontmatter of
every file. All 49 declare one key inside `prosiform`.

| `prosiform` key | Files declaring it |
| --- | --- |
| `root` | 49 |
| `group` | 0 |
| `group-depth` | 0 |
| `group-heading` | 0 |
| `dispatch` | 0 |

Roots as W01 left them, unchanged by this row: `root: ".."` on 20 files and
`root: "."` on 29.

## What the Build Admits

`invocation.md` states the admitted set as `root`, `group`, `group-depth`,
`group-heading` and `dispatch`, and unidentified keys fail validation.
`src/prosiform/metadata.py` names the same four this row touches as `GROUP`,
`DEPTH`, `HEADING` and the root field beside `DISPATCH`. AC4 requires that the
key set in use is exactly `root`, `group`, `group-depth` and `group-heading`, so
`dispatch` stays undeclared even where a mode routes work to another agent.
