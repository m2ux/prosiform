# Placement

A proposed destination and disposition for one orphan's work.

## Operations

### Draft Issue Placement

One placement option from the supplied orphan and candidate destinations.

**Inputs:** Current orphan body, candidate destinations, proposed work and supplied planning-record references.

1. Identify an existing task, a new task, a new epic, a new initiative, or Leave. Record the destination and the work it takes, meeting [Fields](#fields).
2. Record whether the orphan is kept, subsumed or left, meeting [Disposition Conditions](#disposition-conditions). Include the reason, the original-body preservation requirement and any planning record reference.
3. Return the placement for the caller to offer and apply. The output is the [Placement](#placement-record), including the draft issue changes.

### Find Placement Candidates

The issue candidates and available destinations from supplied records.

**Inputs:** Complete repository issue collection.

- Run [List Orphans](#list-orphans) with the supplied issue file. Return the [Candidate Issues](#candidate-issues) and open initiative and epic destinations for the caller to investigate.

## Fields

- **Source.** The orphan's repository, issue number and current body.
- **Destination.** The selected issue or proposed work, with the criteria and design it takes.
- **Disposition.**
  Kept, subsumed or left, with a reason. A referenced planning record is carried with the source reference.
- **Draft bodies.**
  Each proposed body meets its own kind's shape and states the result. It carries no account of how the work arrived. A source reference says what detail it holds.
- **Links.**
  An initiative row identifies its epic issue. A task issue has its delivery link through Development.
- **Preservation.**
  A kept or left issue has the complete original-body comment ready before its rewrite. A subsumed issue retains its body.

### Placement Record

| Destination | Work | Issue Disposition |
| --- | --- | --- |
| Existing task | Criteria and design in a task that has its own issue | Subsumed |
| New task | A row in an existing epic, with its criteria | Kept or subsumed |
| New epic | An epic in an existing initiative | Kept or subsumed |
| New initiative | An initiative | Kept or subsumed |
| Leave | Work outside the initiative structure | Left open |

### Original Body

The comment starts with `The body before this issue took the [I07:E01:W04] layout:` for a kept issue, or `The body before this issue took the standalone layout:` for one left in place. A blank line separates that lead from the complete original body.

### Disposition Conditions

A source with a planning-record reference is subsumed, with that folder cited beside the source in the destination. Otherwise the source is kept when its work needs its own discussion or evidence, and subsumed when its detail fits in rows, criteria and a reference. Work an existing criterion already states is subsumed into the issue holding that criterion, without a new row; for cited standalone work this is usually the citing issue.

### Candidate Issues

Candidates are open issues without an agent-engineering prefix. Orphans have no incoming link from an open initiative, epic or task. Cited standalone issues have such a link in prose or References; their records include labels, citing issues and any linked planning folder. An investigation cited by an epic is a candidate, with disposition determined from supplied criteria.

### Destination Work

An existing-epic option identifies the row to add, with Description, criteria, Depends on and Joins, or the existing task already delivering the work. Leave applies when no initiative goal covers it or it is not planned work. Each option names whether the source is kept or subsumed.

## Commands

### List Orphans

Lists the hoist candidates, and the open initiatives and epics they could join.

**Inputs:** Complete supplied repository issue collection.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/orphans.py '<issues-json-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/orphans.py issues.json
```
