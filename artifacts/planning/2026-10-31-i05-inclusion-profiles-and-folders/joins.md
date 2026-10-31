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

### Target Presets

| Pair | Two pull requests because |
| --- | --- |
| E13:W04 and E13:W05 | W04 adds a warning to the run's trailing diagnostics; W05 records a deferred document's presets. Both touch `cli.py` and neither reads the other's work. |
| E13:W05 and E13:W06 | W06 is the two documentation pages, and documentation lands after the warning whose wording it quotes. |

### Exclusion

| Pair | Two pull requests because |
| --- | --- |
| E14:W03 and E14:W04 | W03 states which documents an exclusion reaches; W04 states that a removed section's links stop being dependencies. Both are properties of one seam, and the fixtures one needs would have to predict the other's behaviour. |
| E14:W03 and E14:W05 | W05 refuses a carve-up that collides with a selection. The collision test needs to know a region was excluded before it can say the removal was contradictory. |
| E14:W03 and E14:W06 | W06 refuses an entry emptied by its exclusions, which is stated per compilation rather than per document and shares no function with the scope rule. |
| E14:W03 and E14:W09 | W09 is documentation, and it lands once the behaviour it states is settled. |
| E14:W04 and E14:W07 | W07 adds a level to the heading lookup; W04 narrows discovery. One changes a lookup, the other a traversal round. |
| E14:W04 and E14:W08 | W08 admits a frontmatter sequence value; W04 is a property of the closure. The two share no file. |
| E14:W05 and E14:W06 | W05 refuses a conflict between an exclusion and a selection; W06 refuses an empty result where no conflict exists. The two are distinguished by which one fires, so one pull request could not show the other does not. |
| E14:W05 and E14:W07 | W05 states the refusal; W07 makes a repeated heading excludable at all, which W05's fixtures would otherwise have to avoid. |
| E14:W05 and E14:W08 | W08 reads the option's grammar from frontmatter, so a preset's exclusion is refused by the same test W05 states. The corpus rows are separate. |
| E14:W05 and E14:W09 | W09 documents both codes, and documentation follows the refusals it names. |
| E14:W06 and E14:W07 | W06 tests emptiness; W07 changes which heading answers a name. A level that matches nothing must stay silent under W06's rule, and one branch cannot show both. |
| E14:W06 and E14:W08 | W08's preset can empty a dispatch, which is W06's second fixture. The frontmatter plumbing and the emptiness test are separate components. |
| E14:W07 and E14:W09 | W09 documents the level; documentation follows it. |
| E14:W08 and E14:W09 | W09 documents the frontmatter form; documentation follows it. |

## Across epics

| Edge | Consumes |
| --- | --- |
| E11:W00 → E13:W00 → E14:W00 | Each clause amends the design after the previous pin moved, so the three pins are one chain rather than three branches amending one revision. |
| E13:W02 → E11:W03 | A preset governs a compilation's resolution, and resolution is the seam that row moves. |
| E13:W03 → E09:W11 | A preset's entries reach one `Substitution`, and that row is where the value holds two kinds of key. |
| E14:W02 → E11:W03 | Exclusion narrows the region set discovery reads, and that row is where classification stops asking a root and asks the target. |
| E14:W08 → E13:W02 | A preset carrying an exclusion reads the key rule that row lands. |

The folder pairing the record once carried as its own epic is [I05:E09](https://github.com/m2ux/prosiform/issues/414)'s `W11` to `W13`, because a folder side is a shape of the `-m` option that epic owns. Its dependency on `E11:W03` and its place in `E13:W03`'s chain travel with it.

## Why this order rather than another

- **E11 first.** It narrows the key set E13 fills and moves the classification seam E13 and E14 read. Delivering either first would mean writing the key rule twice, once against `root` and once against the declaration.
- **E13 second.** It is the largest and the only one whose subject is a compilation rather than a source, and it reads E11.
- **E14 last.** A carve-up is a preset's use, so it lands once presets exist to carry it. Its seam is E11's, so it could be delivered earlier; the order is the value of the feature rather than a hard gate.

The initiative's `Depends on` cells are empty. The rule derives a whole-epic edge only where every row of the dependent requires every row of the prerequisite, and no epic here meets that: E13's W06 documentation row consumes nothing from E11, and E14's W09 documentation row consumes nothing from either. The board keeps each epic out of Ready by its priority number and by the task edges above.

## What each epic's base is

Each epic cuts its base from `i05/main` after the previous epic's merge, so the clause pins chain and no epic branch carries another's frontmatter edits.
