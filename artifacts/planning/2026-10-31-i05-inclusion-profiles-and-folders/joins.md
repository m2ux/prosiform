# Joins and Ordering

Which rows take one pull request, and why the epics are ordered as they are.

## Within an epic

The pairs below are the ones the dependency checker reports as eligible to share a pull request. Each is accounted for here rather than named in a Joins cell, because two of the rows in most pairs extend one component and the grain rule keeps them apart.

### Declared Inclusion

| Pair | Two pull requests because |
| --- | --- |
| E11:W04 and E11:W05 | W04 states which links fail and W05 states the boundary a document's links derive. W05 depends on W04, so the pair is an ordered pair rather than a join, and the two land separately because one rewrites `cli.required` and the other adds a target and a source field. |
| E11:W04 and E11:W06 | W06 edits 213 documents and two checks; W04 changes a refusal. One review cannot read both with any care. |
| E11:W04 and E11:W07 | W07 is the corpus's own row, and a corpus row that lands with an implementation row cannot tell a passing fixture from a fixture written to match the code. |
| E11:W04 and E11:W08 | W08 is documentation, and documentation lands once the behaviour it states is settled. |
| E11:W04 and E11:W07 (corpus and tree) | Every corpus row after W04 is a whole-tree edit, so each is one review of one tree. |

### Folder Mocks

| Pair | Two pull requests because |
| --- | --- |
| E12:W04 and E12:W05 | W04 extends a check the earlier epic lands; W05 rewrites the option table and the help string. The two share no file. |

### Target Presets

| Pair | Two pull requests because |
| --- | --- |
| E13:W04 and E13:W05 | W04 adds a warning to the run's trailing diagnostics; W05 records a deferred document's presets. Both touch `cli.py` and neither reads the other's work. |
| E13:W05 and E13:W06 | W06 is the two documentation pages, and documentation lands after the warning whose wording it quotes. |

## Across epics

| Edge | Consumes |
| --- | --- |
| E11:W00 → E12:W00 → E13:W00 | Each clause amends the design after the previous pin moved, so the three pins are one chain rather than three branches amending one revision. |
| E12:W01 → E09:W01 | The folder grammar extends the `-m` option and the `Substitution` value that row lands. |
| E12:W02 → E11:W03 | A substitution reaches a substitute through the inclusion rule, so a folder of stubs is meaningful only once a stub declares. |
| E13:W02 → E11:W03 | A preset governs a compilation's resolution, and resolution is the seam that row moves. |
| E13:W03 → E12:W02 | A preset's entries reach one `Substitution`, and that row is where the value holds two kinds of key. |

## Why this order rather than another

- **E11 first.** It narrows the key set E13 fills and moves the classification seam E13 reads. Delivering E13 first would mean writing the key rule twice, once against `root` and once against the declaration.
- **E12 second.** It is small, it amends a value E11 touched only to remove a parameter from, and E13's demonstration needs a folder of stubs to point at.
- **E13 last.** It is the largest and the only one whose subject is a compilation rather than a source, and it reads both of the other two.

The initiative's `Depends on` cells are empty. The rule derives a whole-epic edge only where every row of the dependent requires every row of the prerequisite, and neither epic meets that: E13's W06 documentation row consumes nothing from E11, and E12's W05 option row consumes nothing from either. The board keeps each epic out of Ready by its priority number and by the task edges above.

## What each epic's base is

Each epic cuts its base from `i05/main` after the previous epic's merge, so the clause pins chain and no epic branch carries another's frontmatter edits.
