# Dependency Graph

The task edges an initiative's epics declare, and the row numbers that graph permits.

## Prerequisites

Read these files first.

- [Issue](issue.md)
- [Initiative Issue Body](initiative-issue-body.md)
- [Plan Change](plan-change.md)

## Operations

### *Check* Dependencies and Numbering

The task graph and the row numbers it permits, checked and renumbered across the supplied bodies.

**Inputs:** Initiative and epic bodies or local drafts, current pull request records, confirmed numbering maps when any, the caller's change allowance when it has one, and explicitly authorized outside-initiative files.

1. Use the supplied local drafts when reviewing unpublished work.
   - For published issues, fetch the initiative and each epic body with [Read Tracker Issue](issue.md#read-tracker-issue).
   - Run [Check Dependencies](#check-dependencies) with the initiative body and every epic body.
2. Resolve each finding, as [Check Plan Change Autonomy](plan-change.md#check-plan-change-autonomy) returns it for the supplied allowance: an automatic correction is taken, and a held one is settled as [Held Change](plan-change.md#held-change) states.
   - Preserve task edges when correcting a whole-epic edge.
   - Name the producing row for each consumed output, meeting [Edges](#edges).
   - Retain a whole-epic edge only where [Whole-Epic Edges](#whole-epic-edges) permits it.
   - Read tasks for implied consumption edges.
   - Account for every independent pair as [Joins](#joins) states.
   - Resolve backward references by moving work to the epic owning its inputs, or removing duplicate work already owned there. Work claimed twice has one owner and a boundary in both bodies.
3. Renumber the confirmed maps, preserving the numbers [Numbering Map](#numbering-map) protects.
   - For a confirmed epic map, run [Renumber Epics](#renumber-epics) with current pull request records and every affected body.
   - For a confirmed task map, run [Renumber Tasks](#renumber-tasks) with the initiative and epic identities, owning epic body, confirmed old-to-new task-number map and every affected body file.
   - Re-sort rewritten tables.
   - Inspect every reported range.
   - Search prose for references the script cannot see.
   - Repeat Check Dependencies after each edge or numbering change until it reports no problem.
   - Record the printed longest chains and each binding whole-epic edge in the planning record.
   - Return the checked bodies, the proposed [Epic Priority](#epic-priority) map and unresolved findings to the caller; do not publish a failed renumbering.

## Fields

- **Scope.** One initiative, its epics and their task rows.
- **Source.** The initiative body and every epic body it links, published or as local drafts.

### Edges

A task edge names the producing row for each output the depending row consumes. An edge a task's prose implies is carried explicitly.

### Whole-Epic Edges

An initiative Depends on cell takes the epics it derives, as [Work Breakdown](initiative-issue-body.md#work-breakdown) states. A whole-epic edge holds only where every prerequisite row is required; a narrower dependency stays in the task graph.

### Epic Priority

The map proposes one positive integer for each epic supplied, derived from the whole-epic edges: an epic with no prerequisite epic, one whose tasks are not yet written among them, carries the largest number, and each other epic takes one less than the smallest its prerequisites carry. Epics that share a number have the same prerequisite depth, so they can start together.

### Joins

Every pair of tasks in an epic where neither depends on the other is named in the epic's Joins, or accounted for in the planning record.

### Numbering Map

A comma-separated list of `<old-number>:<new-number>` pairs assigning each old number one distinct new number. A number a pull request already names is preserved, and a row a pull request names is not renumbered. A source absent from the supplied files, or a duplicate destination, is refused.

## Commands

### Check Dependencies

Checks the task dependency graph across the epics given, and with `I=` the initiative's Depends on cells.

**Inputs:** Initiative body file and each epic id with its body file.

- Keep `I=` for the initiative. Repeat the `<epic-id>=<epic-body-file>` argument once per epic.

- Initiative edges follow the [whole-epic prerequisite rule](initiative-issue-body.md#work-breakdown); narrower dependencies stay in the task graph.
- It also reports dependencies listed twice or already implied, and Joins pairs.
- It prints each pair of tasks in an epic where neither depends on the other and the two do not name each other in Joins.
- It prints each whole-epic dependency with that epic's row count, the binding row and its level, and the earliest row and its level.
- It prints the proposed [Epic Priority](#epic-priority) of each epic, largest first.
- It reads bodies from [Read Tracker Issue](issue.md#read-tracker-issue), or local drafts.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deps.py 'I=<initiative-body-file>' '<epic-id>=<epic-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/deps.py I=live-936.md E00=live-943.md E01=live-937.md
```

### Renumber Tasks

Renumbers one epic's tasks by the map given, in the files given.

**Inputs:** Initiative number, epic number, epic body file, task-number map and affected body files.

- `<task-number-map>` is a comma-separated list of `<old-number>:<new-number>` pairs. Pass each affected body file as a separate argument.

- It renumbers `<epic-id> Wxx` and `<epic-id>:Wxx` everywhere, and bare `Wxx` inside that epic's own body. **Example:** for `E01`, the qualified forms are `E01 Wxx` and `E01:Wxx`.
- The map assigns each old task number a distinct new number. A source absent from the files or a duplicate destination is refused.
- Append `--outside` followed by each explicitly authorized outside-initiative body file when supplied; only this initiative's prefixed references change there.
- Only rows no pull request names may be renumbered. Inspect the rewritten files before publishing them.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/renumber.py --initiative '<initiative-number>' --epic '<epic-number>' --own '<epic-body-file>' --tasks '<task-number-map>' '<affected-body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/renumber.py --initiative 07 --epic 1 --own live-937.md --tasks 7:3,3:5 live-*.md
```

### Renumber Epics

Renumbers an initiative's epics across supplied body files.

**Inputs:** Initiative number, current pull request records, confirmed epic-number map, body files and explicitly authorized outside-initiative files when present.

- The map is a comma-separated list of `<old-number>:<new-number>` pairs. Pass each body file as a separate argument; append `--outside` followed by each outside-initiative file when supplied.
- Files are rewritten in place. Outside files change only references carrying this initiative's prefix; links retain their targets. A collision or a number already named by a pull request is refused.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/renumber.py --initiative '<initiative-number>' --prs '<pull-request-records-file>' --map '<epic-number-map>' '<body-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/renumber.py --initiative 07 --prs prs.json --map 6:0,0:1 live-936.md live-943.md
```
