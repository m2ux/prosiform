## Overview

What the delivery measured, and what it found that the plan and the brief did not hold.

## What the base already carried

- `W_RESOURCE_PORTABILITY` sits in the catalogue and in `fixtures/manifest.schema.json`, and no source file emits it. `grep -rn RESOURCE_PORTABILITY src/` returns nothing on `6ac9538`. The catalogue holds 25 codes and needs none added, so the two-branch window stays shut; the emission is the work.
- `W_EMPTY_GROUP_RULE`, the catalogue's other warning, is likewise emitted by no source file. Grouping is a later epic, so this is a statement about the schedule rather than a defect of this row.
- W04 is implemented and correct. `bundle.Group` carries `absorbed`, `cli.destination_map` enters the absorbed slug against the file heading's own destination, and a run over a source in a directory shows the mapping is real rather than a coincidence of equal slugs: `docs/repository-labels.md#repository-labels` resolves to `#docsrepository-labels`, the file heading's destination, while `#scope`, which no heading absorbed, resolves to `#scope`.
- A link-reference definition produces no token, so a definition at the document level already lies between two regions and is dropped by the slice that takes them. A definition a container carries sits inside that container's region and was emitted; removing it is this row's work.
- `env["references"]` carries a `map` for each definition, which is the line range the removal needs and the source text the authored destination and title are read from.

## The parser agreement the scan has to keep

`[outer [bare] text][rules]`, where `bare` and `rules` are both defined, is not a full reference. A link label holds no link, so the parser reads a literal `[outer `, the shortcut link `[bare]`, a literal ` text]`, and the shortcut link `[rules]`. A scan that matched the outermost brackets first would publish a use the parser never read.

The scan therefore pairs each closing bracket with the nearest bracket still open, rejects a link whose label already holds a link, and counts what it found against the uses the parser read from the same token. A disagreement is refused rather than published.

A task marker the profile returned to literal text is the one bracket pair a definition does not make a link of, and the token records that it carries one, because a scan over source text has no list structure to read it from.

## Deferred

| Finding | Where it went |
| --- | --- |
| A definition whose destination or title the author spelled across two lines ends the run in an internal error, because the emission writes no line break into the lines an inline token occupies | [#88](https://github.com/m2ux/prosiform/issues/88), [I00:E11](https://github.com/m2ux/prosiform/issues/39) W09 / AC10 |
| A marked link inside an image's alternative content is read as no reference, so the mark reaches the bundle and the document it names is not carried | [#89](https://github.com/m2ux/prosiform/issues/89), [I00:E11](https://github.com/m2ux/prosiform/issues/39) W10 / AC11 |

Each is declared by a fixture carrying the marker: `reference/a-definition-spelled-across-two-lines` and `reference/a-marked-link-inside-image-alternative-content`.
