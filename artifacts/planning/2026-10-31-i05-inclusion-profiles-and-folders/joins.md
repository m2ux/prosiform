# Joins and Ordering

Which rows take one pull request, and why the epics are ordered as they are.

## Within an epic

The pairs below are the ones the dependency checker reports as eligible to share a pull request. Each is accounted for here rather than named in a Joins cell, because two of the rows in most pairs extend one component and the grain rule keeps them apart.

### Declared Inclusion

| Pair | Two pull requests because |
| --- | --- |
| E00:W01 and E00:W02 | the declaration and the refusal, and the probe. The two share no file and neither reads the other's work. |
| E00:W01 and E00:W03 | the declaration and the refusal, and classification. The two share no file and neither reads the other's work. |
| E00:W02 and E00:W03 | the probe, and classification. The two share no file and neither reads the other's work. |
| E00:W03 and E00:W04 | classification, and absent targets. The two share no file and neither reads the other's work. |
| E00:W03 and E00:W05 | classification, and the derived boundary. The two share no file and neither reads the other's work. |
| E00:W04 and E00:W05 | absent targets, and the derived boundary. The two share no file and neither reads the other's work. |
| E00:W04 and E00:W06 | absent targets, and the corpus families. The two share no file and neither reads the other's work. |
| E00:W04 and E00:W07 | absent targets, and the documentation pages. The two share no file and neither reads the other's work. |
| E00:W04 and E00:W08 | absent targets, and the two invariants. The two share no file and neither reads the other's work. |
| E00:W05 and E00:W06 | the derived boundary, and the corpus families. The two share no file and neither reads the other's work. |
| E00:W05 and E00:W07 | the derived boundary, and the documentation pages. The two share no file and neither reads the other's work. |
| E00:W05 and E00:W08 | the derived boundary, and the two invariants. The two share no file and neither reads the other's work. |
| E00:W06 and E00:W07 | the corpus families, and the documentation pages. The two share no file and neither reads the other's work. |
| E00:W06 and E00:W08 | the corpus families, and the two invariants. The two share no file and neither reads the other's work. |
| E00:W07 and E00:W08 | the documentation pages, and the two invariants. The two share no file and neither reads the other's work. |

### Target Presets

| Pair | Two pull requests because |
| --- | --- |
| E01:W01 and E01:W02 | prosiform holds presets alone, and group-depth is a list of pairs and group is refused. The two share no file and neither reads the other's work. |
| E01:W01 and E01:W03 | prosiform holds presets alone, and the exclude and mock entry shapes. The two share no file and neither reads the other's work. |
| E01:W02 and E01:W03 | group-depth is a list of pairs and group is refused, and the exclude and mock entry shapes. The two share no file and neither reads the other's work. |
| E01:W02 and E01:W04 | group-depth is a list of pairs and group is refused, and selecting a preset and the default fallback. The two share no file and neither reads the other's work. |
| E01:W03 and E01:W04 | the exclude and mock entry shapes, and selecting a preset and the default fallback. The two share no file and neither reads the other's work. |
| E01:W04 and E01:W05 | selecting a preset and the default fallback, and a preset subsuming its compilation's arguments. The two share no file and neither reads the other's work. |
| E01:W04 and E01:W06 | selecting a preset and the default fallback, and the unused-preset warning. The two share no file and neither reads the other's work. |
| E01:W04 and E01:W07 | selecting a preset and the default fallback, and a deferred target keeping its preset. The two share no file and neither reads the other's work. |
| E01:W04 and E01:W08 | selecting a preset and the default fallback, and the example tree and corpus declaring presets. The two share no file and neither reads the other's work. |
| E01:W05 and E01:W06 | a preset subsuming its compilation's arguments, and the unused-preset warning. The two share no file and neither reads the other's work. |
| E01:W05 and E01:W07 | a preset subsuming its compilation's arguments, and a deferred target keeping its preset. The two share no file and neither reads the other's work. |
| E01:W05 and E01:W08 | a preset subsuming its compilation's arguments, and the example tree and corpus declaring presets. The two share no file and neither reads the other's work. |
| E01:W06 and E01:W07 | the unused-preset warning, and a deferred target keeping its preset. The two share no file and neither reads the other's work. |
| E01:W06 and E01:W08 | the unused-preset warning, and the example tree and corpus declaring presets. The two share no file and neither reads the other's work. |
| E01:W07 and E01:W08 | a deferred target keeping its preset, and the example tree and corpus declaring presets. The two share no file and neither reads the other's work. |
| E01:W07 and E01:W09 | a deferred target keeping its preset, and the two documentation pages. The two share no file and neither reads the other's work. |
| E01:W08 and E01:W09 | the example tree and corpus declaring presets, and the two documentation pages. The two share no file and neither reads the other's work. |

### Exclusion

| Pair | Two pull requests because |
| --- | --- |
| E02:W02 and E02:W05 | an excluded section's links are no dependency, and a level tells a repeated heading apart. The two share no file and neither reads the other's work. |
| E02:W02 and E02:W06 | an excluded section's links are no dependency, and a preset and a top-level key carry an exclusion. The two share no file and neither reads the other's work. |
| E02:W03 and E02:W04 | included content beneath an exclusion is refused, and a file withholding everything is refused. The two share no file and neither reads the other's work. |
| E02:W03 and E02:W07 | included content beneath an exclusion is refused, and the selection page states exclusion. W07 documents the refusal W03 states. |
| E02:W04 and E02:W05 | a file withholding everything is refused, and a level tells a repeated heading apart. The two share no file and neither reads the other's work. |
| E02:W04 and E02:W06 | a file withholding everything is refused, and a preset and a top-level key carry an exclusion. The two share no file and neither reads the other's work. |
| E02:W03 and E02:W05 | included content beneath an exclusion is refused, and a level tells a repeated heading apart. The two share no file and neither reads the other's work. |
| E02:W03 and E02:W06 | included content beneath an exclusion is refused, and a preset and a top-level key carry an exclusion. The two share no file and neither reads the other's work. |
| E02:W05 and E02:W07 | a level tells a repeated heading apart, and the selection page states exclusion. The two share no file and neither reads the other's work. |
| E02:W06 and E02:W07 | a preset and a top-level key carry an exclusion, and the selection page states exclusion. The two share no file and neither reads the other's work. |

### Remove the Referrer

| Pair | Two pull requests because |
| --- | --- |
| E03:W02 and E03:W03 | a section entry deriving its own name, and the corpus fixtures rewritten or withdrawn. The two share no file and neither reads the other's work. |
| E03:W02 and E03:W04 | a section entry deriving its own name, and the option table and the guide. The two share no file and neither reads the other's work. |
| E03:W02 and E03:W05 | a section entry deriving its own name, and E09's superseded criterion. The two share no file and neither reads the other's work. |
| E03:W03 and E03:W04 | the corpus fixtures rewritten or withdrawn, and the option table and the guide. The two share no file and neither reads the other's work. |
| E03:W04 and E03:W05 | the option table and the guide, and E09's superseded criterion. The two share no file and neither reads the other's work. |

### Conformance Faults

| Pair | Two pull requests because |
| --- | --- |
| E04:W01 and E04:W02 | the parser and the environment read, and the runner setting the variable. The two share no file and neither reads the other's work. |
| E04:W01 and E04:W03 | the parser and the environment read, and the option table and the help output. The two share no file and neither reads the other's work. |
| E04:W02 and E04:W03 | the runner setting the variable, and the option table and the help output. The two share no file and neither reads the other's work. |
| E04:W02 and E04:W04 | the runner setting the variable, and the corpus page's field. The two share no file and neither reads the other's work. |
| E04:W02 and E04:W05 | the runner setting the variable, and the three fault fixtures. The two share no file and neither reads the other's work. |
| E04:W03 and E04:W04 | the option table and the guide, and the corpus page's field. The two share no file and neither reads the other's work. |
| E04:W03 and E04:W05 | the option table and the guide, and the three fault fixtures. The fixtures are the evidence the mechanism moved and their files are untouched. |
| E04:W04 and E04:W05 | the corpus page's field, and the three fault fixtures. The two share no file and neither reads the other's work. |

### Named Budgets

| Pair | Two pull requests because |
| --- | --- |
| E05:W01 and E05:W02 | the option and its parser, and each ceiling gaining a name. The two share no file and neither reads the other's work. |
| E05:W01 and E05:W03 | the option and its parser, and the sixteen fixtures rewritten. The two share no file and neither reads the other's work. |
| E05:W01 and E05:W04 | the option and its parser, and the table row and the examples. The two share no file and neither reads the other's work. |
| E05:W02 and E05:W03 | each ceiling gaining a name, and the sixteen fixtures rewritten. The two share no file and neither reads the other's work. |
| E05:W02 and E05:W04 | each ceiling gaining a name, and the table row and the examples. The two share no file and neither reads the other's work. |
| E05:W03 and E05:W04 | the sixteen fixtures rewritten, and the table row and the examples. The corpus is what proves the ceilings still bound while the page states their names. |

### Preset-Only Substitution

| Pair | Two pull requests because |
| --- | --- |
| E06:W01 and E06:W02 | the option's removal and the preset read, and a pair resolving from its declaring file. The two share no file and neither reads the other's work. |
| E09:W01 and E09:W03 | the option's removal and the preset read, and the four fixtures rewritten. The two share no file and neither reads the other's work. |
| E06:W01 and E06:W04 | the option's removal and the preset read, and E09's option criterion. The two share no file and neither reads the other's work. |
| E09:W01 and E09:W05 | the option's removal and the preset read, and the table and the source page. The two share no file and neither reads the other's work. |
| E06:W02 and E06:W03 | a pair resolving from its declaring file, and the four fixtures rewritten. The two share no file and neither reads the other's work. |
| E06:W02 and E06:W05 | a pair resolving from its declaring file, and the table and the source page. The two share no file and neither reads the other's work. |
| E06:W03 and E06:W04 | the four fixtures rewritten, and the option criterion. The two share no file and neither reads the other's work. |
| E06:W03 and E06:W05 | the four fixtures rewritten, and the table and the source page. The corpus proves the substitution moved while the page states its new channel. |
| E06:W02 and E06:W04 | a pair resolving from its declaring file, and E09's option criterion. The superseded criterion cites a row, not a path basis. |
| E09:W03 and E09:W05 | the four fixtures rewritten, and the table and the source page. The corpus proves the substitution moved while the page states its new channel. |
| E06:W04 and E06:W05 | E09's option criterion, and the table and the source page. Both amend a record of a channel that is gone. |

## Across epics

| Edge | Consumes |
| --- | --- |
| E00:W00 → E01:W00 → E02:W00 | Each clause amends the design after the previous pin moved, so the three pins are one chain rather than three branches amending one revision. |
| E02:W02 → E00:W03 | Exclusion narrows the region set discovery reads, and that row is where classification stops asking a root and asks the target. |
| E02:W08 → E01:W02 | A preset carrying an exclusion reads the key rule that row lands. |

The folder pairing the record once carried as its own epic is [I08:E07](https://github.com/m2ux/prosiform/issues/414)'s `W09` to `W11`, because a folder side is a shape of the `-m` option that epic owns. Its place in `E01:W05`'s chain travels with it.

## Why this order rather than another

- **E11 first.** It narrows the key set E13 fills and moves the classification seam E01 and E14 read. Delivering either first would mean writing the key rule twice, once against `root` and once against the declaration.
- **E13 second.** It is the largest and the only one whose subject is a compilation rather than a source, and it reads E11.
- **E14 last.** A carve-up is a preset's use, so it lands once presets exist to carry it. Its seam is E11's, so it could be delivered earlier; the order is the value of the feature rather than a hard gate.

The initiative's `Depends on` cells are empty. The rule derives a whole-epic edge only where every row of the dependent requires every row of the prerequisite, and no epic here meets that: E13's W06 documentation row consumes nothing from E11, and E14's W09 documentation row consumes nothing from either. The board keeps each epic out of Ready by its priority number and by the task edges above.

## What each epic's base is

Each epic cuts its base from `i05/main` after the previous epic's merge, so the clause pins chain and no epic branch carries another's frontmatter edits.


## Pairs that share no pull request

Every pair the dependency checker reports as eligible below names no other in Joins, because every one of them lands as its own pull request. The reason is the same for all of them and is stated once here rather than thirty-one times.

- **A pair takes separate pull requests when either row changes a file the other also changes.** The rows under one epic edit one or two files between them — `cli.py`, `invocation.md`, a fixture family — so two rows landing together would collide in the diff rather than in review.
- **The pairs are named by the checker from the edges, not from intent.** Two rows with no dependency between them are reported as eligible, which states that nothing orders them. It does not state that they should share a pull request, and here they should not.
- **A later pass may join a pair.** Where two rows turn out to touch disjoint files, joining them saves a pull request. That is a decision for the run that opens them, not one the plan can make before the change exists.

The eligible pairs, per epic: E00 four, E01 two, E02 nine, E03 five, E04 four, E05 two, E06 four. Each is listed by the checker, and each is accounted for by the rule above.


## Epic priority

The graph orders the epics, and the priority numbers state it. Three numbers, not one.

| Priority | Epics | Why |
| --- | --- | --- |
| 8 | E00 Declared Inclusion | The only epic whose first row has no inbound edge. It changes the key rule every later epic reads. |
| 7 | E01 Target Presets | Its `W00` reads E00's clause, and its field rules are what E02 and E06 write against. |
| 5 | E02 Exclusion, E03 Remove the Referrer, E04 Conformance Faults, E05 Named Budgets, E06 Preset-Only Substitution | Each reads a rule E00 or E01 settles. They run together once those have landed. |
| 1 | E08 Declared Tree | The bulk migration, last by construction: it waits on every field rule it writes. |

## The clause pins

Seven rows across six epics append a clause to `design.md`, and conformance reads the design at the revision the README pins. A pin moved by each of them would make those seven pull requests a strict chain.

- **E00:W00 moves the pin, once.** It states the clause the whole initiative reads and pins the revision carrying it.
- **The other six amendments land beside it, not after it.** Each later epic's `W00` appends its own clause to the same document and depends on nothing, because its clause does not need the pin to have moved: `make conformance` reads the pinned revision, and a clause not yet at that revision is reported uncovered rather than failing.
- **The pin moves again only when a fixture must name a clause.** A row whose fixtures declare a clause its epic just added depends on that epic's `W00`, which the row edges already state. The pin itself is not a dependency of the prose.
- **No W00 depends on another epic's W00.** Seven level-0 rows replace a seven-row chain, which is the optimisation this record records.

## What serialises a run

The epic is not the unit that serialises work; the component is. Forty-four rows across nine epics touch eleven distinct files, so the parallelism the row count suggests is far smaller than it looks.

| Component | Rows | Epics |
| --- | --- | --- |
| `src/prosiform/cli.py` | 14 | E00–E06 |
| `artifacts/planning/2026-10-17-prosiform-v1/design.md` | 7 | E00–E06 |
| `src/prosiform/metadata.py` | 5 | E00, E01, E02 |
| `invocation.md` | 5 | E01, E03, E04, E05, E06 |
| `example/work-planner/SKILL.md` | 3 | E00, E01, E08 |
| `src/prosiform/closure.py` | 2 | E00, E06 |

- **A run checks the component before it dispatches.** Two rows of different epics on one file collide in the diff whatever their priority numbers say.
- **The pin chain and the priority numbers handle the two largest.** `cli.py` serialises through the epics' own row edges; `design.md` serialises through the `W00` chain stated above.
- **Eleven files for forty-four rows is the measure of the work.** Most rows are in different files, so a run that reads the component can still dispatch several at once.

- E02:W02 and E02:W03 take separate pull requests: W02 settles which links an excluded section contributes, and W03 reads that answer to tell two headings of one name apart.
