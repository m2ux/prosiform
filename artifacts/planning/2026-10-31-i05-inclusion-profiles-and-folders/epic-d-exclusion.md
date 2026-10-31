## Overview

A preset's `exclude` removes named sections from the bundle, scoped to the file that declares it. One preset carves one source several ways for several consumers, and an excluded section contributes nothing — its text, its group, and every link it wrote.

## Problem

A bundle is the union of what its links reach, and a document has no way to say what part of itself it withholds.

- **Selection adds only.** `cli.selection` resolves each fragment through `source.section` and unions the results into a `Selection`. `docs/selection.md` states that consolidation unions overlaps, so the selection model has no subtractive operation at all.
- **A shared document bundles whole.** A document holding material two consumers need differently reaches both bundles entire, so carving one source for several consumers means maintaining several near-copies of it — the duplication the tool exists to remove.
- **The nearest lever is the tree.** An author who needs a variant edits a copy, and the copy drifts from the original exactly as the note in [the mock epic](https://github.com/m2ux/prosiform/issues/414) records.
- **An argument belongs to the document that names it.** A preset is written by the file it governs, so what that file withholds belongs in the same declaration rather than on a command line that cannot know which file meant what.

## Proposal

- **A preset declares what its file withholds.** A `prosiform` preset holds an `exclude` of sections, and each named section is removed from the contribution of the file that declares the preset — the scope is the declaring file, and no document qualifier is written.
- **The grammar is a bare name, and a level where one is needed.**
  `exclude: ["Draft"]` removes `Draft`. `exclude: ["Draft", {"Tests": 3}]` removes `Draft` whole and the level-3 heading named `Tests`, so a carve-up can exclude one of a repeated pair. Naming a section is the entry's meaning, so no `#` is written; the level selects which heading is meant and the whole subtree beneath it goes. The entry shape is [I08:E01](https://github.com/m2ux/prosiform/issues/436)'s.
- **An exclusion is the whole section.** What it removes is what `source.section` selects for that name: the heading, its own content and every subsection beneath it. Inclusion and exclusion describe one shape, so a reader learns one rule.
- **Exclusion narrows the closure.** A link written inside an excluded section is no dependency, so the document it names is not read through it. What the bundle then carries is what the remaining content reaches, and a document another link also reaches still arrives by that link.
- **Exclusion happens where selection settles.** The settled region set is the selected regions less the excluded ones, and every stage already reads that set — discovery, withheld targets, dispatches, operator refusals and emission. One seam removes the material, so no stage can disagree about what the bundle holds.
- **The scope is the preset's.** An exclusion is a preset entry, so it governs the compilation that preset was selected for, and the file that declares it is the scope. There is no top-level form: a list is a preset's shape, and a top-level key that held one would be neither an argument nor a preset. A dispatched target's exclusions are therefore its own document's and never the entry's.
- **An excluded section holding included content is refused.** Material beneath an excluded heading was selected by something else, and the bundle cannot carry it beneath a heading the author removed. The run refuses with `E_EXCLUDED_CONTENT`, naming the exclusion and the route that selected the content.
- **A failed exclusion is refused only where it names a contradiction.** An exclusion naming a heading the declaring file does not carry is silent, because a preset is shared across documents that vary. An exclusion emptying the file's own contribution is refused with `E_EXCLUDED_ENTRY`, because a document that withholds everything it holds states a contradiction.
- **A deferral is not carried across.** An exclusion governs what this run compiles. A `¬` link inside an excluded section is never resolved, and a deferral the bundle publishes names a path rather than a set of exclusions, so what the later run withholds is that run's business.
- **A malformed exclusion is invalid usage.** An empty section and a level outside one through six are refused before any source is read, which is where every command-line fault is stated.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause and pin | AC10 | [I08:E01:W00](https://github.com/m2ux/prosiform/issues/436) | | |
| W01 | The exclusion grammar, its refusals and the seam | AC1, AC7, AC11 | W00, [I08:E00:W03](https://github.com/m2ux/prosiform/issues/434) | | |
| W02 | An excluded section's links are no dependency | AC3 | W01 | | |
| W03 | Included content beneath an exclusion is refused | AC4 | W02 | | |
| W04 | A file withholding everything is refused | AC5 | W02 | | |
| W05 | A level tells a repeated heading apart | AC6 | W01 | | |
| W06 | A preset carries an exclusion | AC2, AC8 | W05, [I08:E01:W03](https://github.com/m2ux/prosiform/issues/436) | | |
| W07 | The clause and the selection page state exclusion | AC9 | W04 | | |

## Acceptance Criteria

- [ ] **AC1.** A section a preset's `exclude` names contributes no heading, no content and no group from the file that declares it, and the run publishes, as the corpus fixture `fixtures/exclusion/a-named-section-is-excluded` shows.
- [ ] **AC2.** An exclusion declared in a preset removes its sections from that compilation alone, and a second compilation of the same file selected by another section is unaffected, as the corpus fixtures `fixtures/exclusion/a-preset-carries-an-exclusion` and `fixtures/exclusion/a-sibling-compilation-of-the-same-file-is-unaffected` show.
- [ ] **AC3.** A link written inside an excluded section is no dependency, so the document it names is not read through it, while a document another link reaches is still carried by that link, as the corpus fixture `fixtures/exclusion/an-excluded-sections-link-is-not-followed` shows.
- [ ] **AC4.** An exclusion whose section holds content another reference selected is refused with `E_EXCLUDED_CONTENT` naming the exclusion and the route, and nothing is published, as the corpus fixture `fixtures/exclusion/an-excluded-section-holding-selected-content-is-refused` shows.
- [ ] **AC5.** A file whose own exclusion removes every region it contributes is refused with `E_EXCLUDED_ENTRY`, as the corpus fixture `fixtures/exclusion/an-exclusion-of-the-whole-entry-is-refused` shows.
- [ ] **AC6.** An entry mapping a name to a level excludes the heading at that level and leaves the heading of the same name at another level with its subsections, as the corpus fixture `fixtures/exclusion/a-level-tells-a-repeated-heading-apart` shows.
- [ ] **AC7.** An exclusion naming a heading the declaring file does not carry publishes, exits `0`, and reports no diagnostic, as the corpus fixture `fixtures/exclusion/an-unmatched-exclusion-is-silent` shows.
- [ ] **AC8.** A preset's `exclude` holds a list whose entries are read by the exclusion grammar, and a top-level `exclude` is refused as a key that is neither an argument nor a preset, as the corpus fixtures `fixtures/exclusion/a-preset-carries-an-exclusion` and `fixtures/exclusion/a-top-level-exclude-is-refused` show.
- [ ] **AC9.** The source page and the selection page state exclusion, its scope and its two codes, and the glossary carries the term, as `make vocabulary` and an inspection of those pages show.
- [ ] **AC10.** The design states exclusion as the subtractive half of selection, scoped to the file that declares it, names the two codes, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.
- [ ] **AC11.** An empty name, a level outside one through six, and a mapping entry holding two keys are each refused with `E_INVALID_CONVERSION_METADATA` naming the entry, as the corpus fixture `fixtures/exclusion/a-malformed-exclusion-is-refused` shows.

## References

- **R0.** Epic — [I08:E02 Exclusion](https://github.com/m2ux/prosiform/issues/445).
- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions and the work items.
- **R2.** [I08:E01 Target Presets](https://github.com/m2ux/prosiform/issues/436) — the epic that admits a preset carrying an exclusion.
- **R3.** [I08:E00 Declared Inclusion](https://github.com/m2ux/prosiform/issues/434) — the epic that moves the classification seam this one narrows.
