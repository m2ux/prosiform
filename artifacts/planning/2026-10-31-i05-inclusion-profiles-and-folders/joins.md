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
| E11:W06 and E11:W09 | W06 edits the example tree; W09 adds a fixture and a boundary assertion. The two share no file. |
| E11:W07 and E11:W09 | W07 reworks the corpus families; W09 adds one fixture and states the invariant it holds. |
| E11:W08 and E11:W09 | W08 is the documentation pages, and documentation follows the invariant it describes. |

### Target Presets

| Pair | Two pull requests because |
| --- | --- |
| E13:W02 and E13:W03 | the settable set and the list value, and matching a section name to a preset. The two share no file and neither reads the other's work. |
| E13:W04 and E13:W05 | a whole-document entry matching no preset, and a preset's entries bound. W04 changes which preset a compilation selects and W05 refuses a collision inside one, so one branch could not show the other does not fire. |
| E13:W04 and E13:W06 | a whole-document entry matching no preset, and the unused-preset warning. The two share no file and neither reads the other's work. |
| E13:W04 and E13:W07 | a whole-document entry matching no preset, and a deferred target keeping its preset. The two share no file and neither reads the other's work. |
| E13:W04 and E13:W08 | a whole-document entry matching no preset, and the two documentation pages. The two share no file and neither reads the other's work. |
| E13:W06 and E13:W07 | the unused-preset warning, and a deferred target keeping its preset. The two share no file and neither reads the other's work. |
| E13:W07 and E13:W08 | a deferred target keeping its preset, and the two documentation pages. The two share no file and neither reads the other's work. |

### Exclusion

| Pair | Two pull requests because |
| --- | --- |
| E14:W02 and E14:W05 | an excluded section's links are no dependency, and a level tells a repeated heading apart. The two share no file and neither reads the other's work. |
| E14:W02 and E14:W06 | an excluded section's links are no dependency, and a preset and a top-level key carry an exclusion. The two share no file and neither reads the other's work. |
| E14:W03 and E14:W04 | included content beneath an exclusion is refused, and a file withholding everything is refused. The two share no file and neither reads the other's work. |
| E14:W03 and E14:W07 | included content beneath an exclusion is refused, and the selection page states exclusion. W07 documents the refusal W03 states. |
| E14:W04 and E14:W05 | a file withholding everything is refused, and a level tells a repeated heading apart. The two share no file and neither reads the other's work. |
| E14:W04 and E14:W06 | a file withholding everything is refused, and a preset and a top-level key carry an exclusion. The two share no file and neither reads the other's work. |
| E14:W03 and E14:W05 | included content beneath an exclusion is refused, and a level tells a repeated heading apart. The two share no file and neither reads the other's work. |
| E14:W03 and E14:W06 | included content beneath an exclusion is refused, and a preset and a top-level key carry an exclusion. The two share no file and neither reads the other's work. |
| E14:W05 and E14:W07 | a level tells a repeated heading apart, and the selection page states exclusion. The two share no file and neither reads the other's work. |
| E14:W06 and E14:W07 | a preset and a top-level key carry an exclusion, and the selection page states exclusion. The two share no file and neither reads the other's work. |

## Across epics

| Edge | Consumes |
| --- | --- |
| E11:W00 → E13:W00 → E14:W00 | Each clause amends the design after the previous pin moved, so the three pins are one chain rather than three branches amending one revision. |
| E14:W02 → E11:W03 | Exclusion narrows the region set discovery reads, and that row is where classification stops asking a root and asks the target. |
| E14:W08 → E13:W02 | A preset carrying an exclusion reads the key rule that row lands. |

The folder pairing the record once carried as its own epic is [I05:E09](https://github.com/m2ux/prosiform/issues/414)'s `W09` to `W11`, because a folder side is a shape of the `-m` option that epic owns. Its place in `E13:W05`'s chain travels with it.

## Why this order rather than another

- **E11 first.** It narrows the key set E13 fills and moves the classification seam E13 and E14 read. Delivering either first would mean writing the key rule twice, once against `root` and once against the declaration.
- **E13 second.** It is the largest and the only one whose subject is a compilation rather than a source, and it reads E11.
- **E14 last.** A carve-up is a preset's use, so it lands once presets exist to carry it. Its seam is E11's, so it could be delivered earlier; the order is the value of the feature rather than a hard gate.

The initiative's `Depends on` cells are empty. The rule derives a whole-epic edge only where every row of the dependent requires every row of the prerequisite, and no epic here meets that: E13's W06 documentation row consumes nothing from E11, and E14's W09 documentation row consumes nothing from either. The board keeps each epic out of Ready by its priority number and by the task edges above.

## What each epic's base is

Each epic cuts its base from `i05/main` after the previous epic's merge, so the clause pins chain and no epic branch carries another's frontmatter edits.
