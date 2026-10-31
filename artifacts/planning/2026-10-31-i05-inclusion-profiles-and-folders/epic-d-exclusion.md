## Overview

`--exclude SECTION` removes a named section from a bundle, wherever the run reads it. One preset carves one source several ways for several consumers, and an excluded section contributes nothing — its text, its group, and every link it wrote.

## Problem

A bundle is the union of what its links reach, and there is no way to subtract from it.

- **Selection adds only.** `cli.selection` resolves each fragment through `source.section` and unions the results into a `Selection`. `docs/selection.md` states that consolidation unions overlaps, so the selection model has no subtractive operation at all.
- **A shared document bundles whole.** A document holding material two consumers need differently reaches both bundles entire, so carving one source for several consumers means maintaining several near-copies of it — the duplication the tool exists to remove.
- **The nearest lever is the tree.** An author who needs a variant edits a copy, and the copy drifts from the original exactly as the note in [the mock epic](https://github.com/m2ux/prosiform/issues/414) records.
- **`-x` is taken.** The fault-injection option holds it, and `-e` is the expansion-depth budget, so the exclusion takes a long form rather than a letter the alphabet has few of.

## Proposal

- **One option, repeatable.** `--exclude SECTION`, given once per section, with no short form. The section is a working-directory-relative or bare reference read by the grammar every other reference is read by, so percent decoding, control-character refusal and `..` normalisation are unchanged.
- **Two scopes.** A bare `#Section` excludes that section in every document the run reads, which is what one preset carving several documents needs. A qualified `document.md#Section` excludes it in that document alone.
- **An exclusion is the whole section.** What it removes is what `source.section` selects: the heading, its own content, and every subsection beneath it. Inclusion and exclusion therefore describe one shape, and an exclusion reads the same way a selection does.
- **A level disambiguates.** A document may carry two headings of one name, which `source.section` already refuses as ambiguous for a fragment. `#Section:3` names the heading at level 3, so a carve-up can exclude one of a repeated pair. The level selects which heading; the whole subtree beneath it still goes. A bare `#Section` needs no number wherever the name is unique.
- **Exclusion narrows the closure.** A link written inside an excluded section is no dependency, so the document it names is not read through it and contributes nothing. What the bundle then carries is what the remaining content reaches, and a document another link also reaches still arrives by that link.
- **Exclusion happens where selection settles.** The settled region set is the selected regions less the excluded ones, and every stage already reads that set — discovery, withheld targets, dispatches, operator refusals and emission. One seam removes the material, so no stage can disagree about what the bundle holds.
- **An excluded section holding included content is refused.** Material beneath an excluded heading was selected by something else, and the bundle cannot carry it beneath a heading the author removed. The run refuses with `E_EXCLUDED_CONTENT`, naming the exclusion and the route that selected the content, so the carve-up is corrected rather than half-applied.
- **A selection that excludes everything is refused.** An exclusion emptying its own entry names a bundle that would carry no document at all, and `E_EXCLUDED_ENTRY` states it rather than publishing an empty file.
- **An unmatched exclusion is silent.** A shared preset legitimately names sections some document lacks, so an exclusion touching nothing publishes and exits `0`. A malformed exclusion — an empty section, a level outside one through six, a query — is refused as invalid usage before any source is read.
- **A preset carries an exclusion.** [I05:E13](https://github.com/m2ux/prosiform/issues/436) admits a `prosiform` key naming an argument, so `exclude` set in a file applies to every compilation of that file and an `exclude` in a preset applies to the compilation that preset governs. A carve-up is therefore a document's own statement rather than only a command line's.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause and pin | AC10 | [E13:W00](https://github.com/m2ux/prosiform/issues/436) | | |
| W01 | The exclusion grammar and its refusals | AC11 | W00 | | |
| W02 | The selection seam and the silent miss | AC1, AC7 | W01, [E11:W03](https://github.com/m2ux/prosiform/issues/434) | | |
| W03 | Bare and document-qualified scope | AC2 | W02 | | |
| W04 | An excluded section's links are no dependency | AC3 | W02 | | |
| W05 | Included content beneath an exclusion is refused | AC4 | W04 | | |
| W06 | A selection excluding everything is refused | AC5 | W04 | | |
| W07 | A level tells a repeated heading apart | AC6 | W03 | | |
| W08 | A preset carries an exclusion | AC8 | W07, [E13:W02](https://github.com/m2ux/prosiform/issues/436) | | |
| W09 | The option row and the selection page | AC9 | W06 | | |

## Acceptance Criteria

- [ ] **AC1.** A section named by `--exclude` contributes no heading, no content and no group to the bundle, and the run publishes, as the corpus fixture `fixtures/exclusion/a-named-section-is-excluded` shows.
- [ ] **AC2.** A bare exclusion removes the section in every document the run reads, and a document-qualified one removes it in that document alone, as the corpus fixture `fixtures/exclusion/a-qualified-exclusion-leaves-another-document-whole` shows.
- [ ] **AC3.** A link written inside an excluded section is no dependency, so the document it names is not read through it, while a document another link reaches is still carried by that link, as the corpus fixture `fixtures/exclusion/an-excluded-sections-link-is-not-followed` shows.
- [ ] **AC4.** An exclusion whose section holds content another reference selected is refused with `E_EXCLUDED_CONTENT` naming the exclusion and the route, and nothing is published, as the corpus fixture `fixtures/exclusion/an-excluded-section-holding-selected-content-is-refused` shows.
- [ ] **AC5.** A selection whose every region the exclusions remove is refused with `E_EXCLUDED_ENTRY`, as the corpus fixture `fixtures/exclusion/an-exclusion-of-the-whole-entry-is-refused` shows.
- [ ] **AC6.** `#Section:3` excludes the level-3 heading of that name and leaves the level-2 heading of the same name and its subsections in the bundle, as the corpus fixture `fixtures/exclusion/a-level-tells-a-repeated-heading-apart` shows.
- [ ] **AC7.** An exclusion naming no heading of any document publishes, exits `0`, and reports no diagnostic, as the corpus fixture `fixtures/exclusion/an-unmatched-exclusion-is-silent` shows.
- [ ] **AC8.** An exclusion set in a document's `prosiform` applies to every compilation of that document, and one set in a preset applies to the compilation that preset governs, as the corpus fixtures `fixtures/exclusion/an-argument-key-excludes-for-every-compilation` and `fixtures/exclusion/a-preset-carries-an-exclusion` show.
- [ ] **AC9.** The option's row states the grammar, the two scopes and the level, and agrees with the command's help output, as `make invocation` shows.
- [ ] **AC10.** The design states exclusion as the subtractive half of selection, names the two codes, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.
- [ ] **AC11.** An empty section, a level outside one through six and a section carrying a query are each refused as invalid usage with exit status `2`, as the corpus fixture `fixtures/exclusion/a-malformed-exclusion-is-refused` shows.

## References

- **R0.** Epic — [I05:E14 Exclusion](https://github.com/m2ux/prosiform/issues/445).
- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions and the work items.
- **R2.** [I05:E13 Target Presets](https://github.com/m2ux/prosiform/issues/436) — the epic that admits a preset carrying an exclusion.
- **R3.** [I05:E11 Declared Inclusion](https://github.com/m2ux/prosiform/issues/434) — the epic that moves the classification seam this one narrows.
