## Overview

A preset's `exclude` removes named sections from a document reached whole by a link, scoped to the preset that governed that link. One preset carves one source several ways for several consumers, and an excluded section contributes nothing — its text, its division, and every link it wrote. A link that names a section selects that section and is never carved.

## Problem

A bundle is the union of what its links reach, and a document has no way to say what part of itself withholds.

- **Selection adds only.** `cli.selection` resolves each fragment through `source.section` and unions the results into a `Selection`. `docs/selection.md` states that consolidation unions overlaps, so the selection model has no subtractive operation at all.
- **A shared document bundles whole.** A document holding material two consumers need differently reaches both bundles entire, so carving one source for several consumers means maintaining several near-copies of it — the duplication the tool exists to remove.
- **The nearest lever is the tree.** An author who needs a variant edits a copy, and the copy drifts from the original exactly as the note in [I08:E07](https://github.com/m2ux/prosiform/issues/414) records.
- **An exclusion belongs to the preset that asked for the reference.** A preset is selected by the section that writes a link, so what that section withholds of the document it names belongs in the same declaration, rather than on a command line that cannot know which section meant what.

## Proposal

- **A preset declares what a whole-file reference withholds.**
  A `prosiform` preset holds an `exclude` of sections, and each named section is removed from the content the governing reference carries. The names are the **target document's** headings, and no document qualifier is written, because the reference the preset governs has already named the target.
- **The carve applies only where the reference names the target whole.**
  `[Rules](rules.md)` under a section whose title selects a preset is carved by that preset's `exclude`. `[Rules](rules.md#Tests)` names one section, so there is nothing to subtract and the preset's `exclude` does not apply. Explicit selection is the more specific statement, and a run that names a section has said which part it wants.
- **The grammar is a bare name, and a level where one is needed.**
  `exclude: ["Draft"]` removes `Draft`. `exclude: ["Draft", {"Tests": 3}]` removes `Draft` whole and the level-3 heading named `Tests`, so a carve-up can exclude one of a repeated pair. Naming a section is the entry's meaning, so no `#` is written; the level selects which heading is meant and the whole subtree beneath it goes. The entry shape is [I08:E01](https://github.com/m2ux/prosiform/issues/436)'s.
- **An exclusion is the whole section.** What it removes is what `source.section` selects for that name: the heading, its own content and every subsection beneath it. Inclusion and exclusion describe one shape, so a reader learns one rule.
- **Exclusion narrows the closure.** A link written inside an excluded section is no dependency, so the document it names is not read through it. What the bundle then carries is what the remaining content reaches, and a document another link also reaches still arrives by that link.
- **Exclusion happens where selection settles.** The settled region set is the region set the reference carries less the excluded ones, and every stage already reads that set — discovery, withheld targets, dispatches, operator refusals and emission. One seam removes the material, so no stage can disagree about what the bundle holds.
- **The scope is the governing preset's, per reference.**
  An exclusion is a preset entry, so it carves the content the reference that preset governed carries, and a second reference to the same document under a preset that excludes nothing carries the section. Nothing is refused, because the two references asked for two different things and both are stated. A dispatched target's exclusions are its own document's and never the entry's.
- **A reference the preset empties is refused.** An exclusion removing the whole of the content a reference carries states a contradiction — a link that names a document whole and receives none of it — so the run refuses with `E_EXCLUDED_ENTRY`, naming the reference, the target and each exclusion that removed a region.
- **An exclusion naming a heading the target does not carry is silent.** One preset serves many links and many documents, so a miss is ordinary rather than a fault.
- **A deferral is not carried across.** An exclusion governs what this run compiles. A `¬` link inside an excluded section is never resolved, and a deferral the bundle publishes names a path rather than a set of exclusions, so what the later run withholds is that run's business.
- **A malformed exclusion is invalid usage.** An empty section and a level outside one through six are refused before any source is read, which is where every command-line fault is stated.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause | AC10 | | | |
| W01 | The exclusion grammar, its refusals and the seam | AC1, AC7, AC11 | W00, [I08:E00:W03](https://github.com/m2ux/prosiform/issues/434) | | |
| W02 | An excluded section's links are no dependency | AC3 | W01 | | |
| W03 | The carve applies only to a whole-file reference | AC2, AC4 | W01 | | |
| W04 | A level tells a repeated heading apart | AC6 | W01 | | |
| W05 | A target emptied by its exclusions is refused | AC5 | W03 | | |
| W06 | A preset carries an exclusion | AC8 | W05, [I08:E01:W03](https://github.com/m2ux/prosiform/issues/436) | | |
| W07 | The selection page and the source page state exclusion | AC9 | W05 | | |

## Acceptance Criteria

- [ ] **AC1.** A section a preset's `exclude` names contributes no heading, no content and no division from the document the governing reference names, and the run publishes, as the corpus fixture `fixtures/exclusion/a-named-section-is-excluded` shows.
- [ ] **AC2.** The carve applies where the governing reference names its target whole, and a reference of the form `document#fragment` is not carved, as the corpus fixtures `fixtures/exclusion/a-whole-file-reference-is-carved` and `fixtures/exclusion/a-section-reference-is-not-carved` show.
- [ ] **AC3.** A link written inside an excluded section is no dependency, so the document it names is not read through it, while a document another link reaches is still carried by that link, as the corpus fixture `fixtures/exclusion/an-excluded-sections-link-is-not-followed` shows.
- [ ] **AC4.** A section one reference excludes still arrives by a second reference that excludes nothing, and the run publishes without a diagnostic, as the corpus fixture `fixtures/exclusion/a-section-a-second-reference-carries-still-arrives` shows.
- [ ] **AC5.** A reference whose target is emptied by that preset's exclusions is refused with `E_EXCLUDED_ENTRY` naming the reference, the target and the exclusions, and nothing is published, as the corpus fixture `fixtures/exclusion/an-exclusion-of-the-whole-entry-is-refused` shows.
- [ ] **AC6.** An entry mapping a name to a level excludes the heading at that level and leaves the heading of the same name at another level with its subsections, as the corpus fixture `fixtures/exclusion/a-level-tells-a-repeated-heading-apart` shows.
- [ ] **AC7.** An exclusion naming a heading the target does not carry publishes, exits `0`, and reports no diagnostic, as the corpus fixture `fixtures/exclusion/an-unmatched-exclusion-is-silent` shows.
- [ ] **AC8.** A preset's `exclude` holds a list whose entries are read by the exclusion grammar, and a top-level `exclude` is refused as a key that is neither an argument nor a preset, as the corpus fixtures `fixtures/exclusion/a-preset-carries-an-exclusion` and `fixtures/exclusion/a-top-level-exclude-is-refused` show.
- [ ] **AC9.** The source page and the selection page state exclusion, its whole-file scope and its code, and the glossary carries the term, as `make vocabulary` and an inspection of those pages show.
- [ ] **AC10.** The design states exclusion as the subtractive half of selection, applied to a whole-file reference under the preset that governs it, names the code, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.
- [ ] **AC11.** An empty name, a level outside one through six, and a mapping entry holding two keys are each refused with `E_INVALID_CONVERSION_METADATA` naming the entry, as the corpus fixture `fixtures/exclusion/a-malformed-exclusion-is-refused` shows.

## References

- **R0.** Epic — [I08:E02 Exclusion](https://github.com/m2ux/prosiform/issues/445).
- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions and the work items.
- **R2.** [I08:E01 Section Presets](https://github.com/m2ux/prosiform/issues/436) — the epic that admits a preset carrying an exclusion.
- **R3.** [I08:E00 Declared Inclusion](https://github.com/m2ux/prosiform/issues/434) — the epic that moves the classification seam this one narrows.
