## Overview

A document's preset `include` keeps only the named sections of that document, and its `exclude` removes named sections, where a link reaches the document whole and selects the preset. One preset carves one source several ways for several consumers, and a section left out contributes nothing — its text, its division, and every link it wrote. A link that names a section selects that section and is never carved.

## Problem

A bundle is the union of what its links reach, and a document has no way to say what part of itself withholds.

- **Selection adds only.**
  `cli.selection` resolves each fragment through `source.section` and unions the results into a `Selection`. `docs/selection.md` states that consolidation unions overlaps, so the selection model has no subtractive operation at all.
- **Keeping a few sections means excluding the rest.**
  A consumer that needs two sections of a ten-section document would list eight exclusions, and every section added to the document later reaches that bundle unasked.
- **A shared document bundles whole.**
  A document holding material two consumers need differently reaches both bundles entire, so carving one source for several consumers means maintaining several near-copies of it — the duplication the tool exists to remove.
- **The nearest lever is the tree.**
  An author who needs a variant edits a copy, and the copy drifts from the original.
- **An exclusion belongs to the document it carves.**
  A document's presets govern its own content and are selected by the section that links it, so what a consumer withholds of the document is one of that document's presets, rather than a command line that cannot know which section meant what.

## Proposal

- **A document's preset declares what it withholds from a whole-file reference.**
  A `prosiform` preset holds an `exclude` of sections, and each named section is removed from the content the selecting reference carries. The names are the **declaring document's own** headings, and no document qualifier is written, because a preset governs only the document that declares it.
- **A document's preset declares the only sections a whole-file reference carries.**
  A `prosiform` preset holds an `include` of sections, read by the same grammar as `exclude`, and the selecting reference carries only those sections, each with its subsections. A preset with no `include` carries the whole document.
- **Include applies first, then exclude.**
  A preset holding both carries the included sections less the excluded ones, so `include: ["Rules"]` with `exclude: ["Draft"]` carries `Rules` without its `Draft` subsection.
- **The carve applies only where the reference names the target whole.**
  `[Rules](rules.md)` under a section whose title selects a preset is carved by that preset's `exclude`. `[Rules](rules.md#Tests)` names one section, so there is nothing to subtract and the preset's `exclude` does not apply. Explicit selection is the more specific statement, and a run that names a section has said which part it wants.
- **The grammar is a bare name, and a level where one is needed.**
  `exclude: ["Draft"]` removes `Draft`. `exclude: ["Draft", {"Tests": 3}]` removes `Draft` whole and the level-3 heading named `Tests`, so a carve-up can exclude one of a repeated pair. Naming a section is the entry's meaning, so no `#` is written; the level selects which heading is meant and the whole subtree beneath it goes. `include` takes the same entries.
- **An inclusion or exclusion is the whole section.**
  What it keeps or removes is what `source.section` selects for that name: the heading, its own content and every subsection beneath it. Both describe one shape, so a reader learns one rule.
- **Inclusion and exclusion narrow the closure.**
  A link written inside a section the preset leaves out, whether not included or excluded, is no dependency, so the document it names is not read through it. What the bundle then carries is what the remaining content reaches, and a document another link also reaches still arrives by that link.
- **Both happen where selection settles.**
  The settled region set is the included regions of what the reference carries, less the excluded ones, and every stage already reads that set — discovery, withheld targets, dispatches, operator refusals and emission. One seam removes the material, so no stage can disagree about what the bundle holds.
- **The scope is the governing preset's, per reference.**
  An exclusion is an entry of the document's own preset, so it carves the content the reference that selected that preset carries, and a second reference selecting a preset that excludes nothing carries the section. Nothing is refused, because the two references asked for two different things and both are stated. A dispatched target's exclusions are its own document's and never the entry's.
- **A reference the preset empties is refused.**
  A preset leaving none of the content a reference carries states a contradiction — a link that names a document whole and receives none of it — so the run refuses with `E_EMPTIED_ENTRY`, naming the reference, the target and the inclusions and exclusions responsible. An `include` matching none of the target's headings empties it the same way.
- **An entry naming a heading the document does not carry is silent.**
  An inclusion or exclusion that matches nothing changes nothing on its own, so a miss is not a fault; only a reference left empty is refused.
- **A deferral is not carried across.**
  An inclusion or exclusion governs what this run compiles. A `¬` link inside an excluded section is never resolved, and a deferral the bundle publishes names a path rather than a set of exclusions, so what the later run withholds is that run's business.
- **A malformed entry is refused where its document is decoded.**
  An empty section, a level outside one through six and a mapping entry holding two keys each fail with `E_INVALID_CONVERSION_METADATA` naming the entry, in `include` as in `exclude`, because an entry is frontmatter and is read with the rest of its document's declaration.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause | AC10 | | | |
| W01 | The exclusion grammar, its refusals and the seam | AC1, AC7, AC11 | W00, [I08:E00:W03](https://github.com/m2ux/prosiform/issues/434) | | |
| W02 | An excluded section's links are no dependency | AC3 | W01 | W05 | |
| W03 | The carve applies only to a whole-file reference | AC2, AC4 | W01 | | |
| W04 | A level tells a repeated heading apart | AC6 | W01 | W06 | |
| W05 | A target emptied by its exclusions is refused | AC5 | W03 | W02 | |
| W06 | A preset carries an inclusion and an exclusion | AC8 | W05, [I08:E01:W03](https://github.com/m2ux/prosiform/issues/436) | W04 | |
| W07 | The pages state inclusion and exclusion | AC9 | W05, W09, W11 | | |
| W08 | An include keeps only the named sections | AC12, AC15 | W05 | | |
| W09 | Include applies first, then exclude | AC13 | W08 | | |
| W10 | A left-out section's links are no dependency | AC16 | W08 | | |
| W11 | An include matching nothing is refused | AC14 | W08 | | |

## Acceptance Criteria

- [ ] **AC1.** A section a preset's `exclude` names contributes no heading, no content and no division from the document the governing reference names, and the run publishes, as the corpus fixture `fixtures/exclusion/a-named-section-is-excluded` shows.
- [ ] **AC2.** The carve applies where the governing reference names its target whole, and a reference of the form `document#fragment` is not carved, as the corpus fixtures `fixtures/exclusion/a-whole-file-reference-is-carved` and `fixtures/exclusion/a-section-reference-is-not-carved` show.
- [ ] **AC3.** A link written inside an excluded section is no dependency, so the document it names is not read through it, while a document another link reaches is still carried by that link, as the corpus fixture `fixtures/exclusion/an-excluded-sections-link-is-not-followed` shows.
- [ ] **AC4.** A section one reference excludes still arrives by a second reference that excludes nothing, and the run publishes without a diagnostic, as the corpus fixture `fixtures/exclusion/a-section-a-second-reference-carries-still-arrives` shows.
- [ ] **AC5.** A reference whose target is emptied by that preset's exclusions is refused with `E_EMPTIED_ENTRY` naming the reference, the target and the exclusions, and nothing is published, as the corpus fixture `fixtures/exclusion/an-exclusion-of-the-whole-entry-is-refused` shows.
- [ ] **AC6.** An entry mapping a name to a level excludes the heading at that level and leaves the heading of the same name at another level with its subsections, as the corpus fixture `fixtures/exclusion/a-level-tells-a-repeated-heading-apart` shows.
- [ ] **AC7.** An exclusion naming a heading the target does not carry publishes, exits `0`, and reports no diagnostic, as the corpus fixture `fixtures/exclusion/an-unmatched-exclusion-is-silent` shows.
- [ ] **AC8.** A preset's `include` and `exclude` each hold a list whose entries are read by one section grammar, and a top-level `include` or `exclude` is refused as a key whose value is not a preset mapping, as the corpus fixtures `fixtures/exclusion/a-preset-carries-an-exclusion`, `fixtures/inclusion/a-preset-carries-an-inclusion`, `fixtures/exclusion/a-top-level-exclude-is-refused` and `fixtures/inclusion/a-top-level-include-is-refused` show.
- [ ] **AC9.** The source page and the selection page state inclusion and exclusion, their order, their whole-file scope and their code, and the glossary carries both terms, as `make vocabulary` and an inspection of those pages show.
- [ ] **AC10.** The design states inclusion and exclusion as the two filters of selection, inclusion applied first, each applied to a whole-file reference under the preset that governs it, names the code, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.
- [ ] **AC11.** An empty name, a level outside one through six, and a mapping entry holding two keys are each refused with `E_INVALID_CONVERSION_METADATA` naming the entry, in `include` as in `exclude`, as the corpus fixtures `fixtures/exclusion/a-malformed-exclusion-is-refused` and `fixtures/inclusion/a-malformed-inclusion-is-refused` show.
- [ ] **AC12.** A preset's `include` carries only the sections it names, each with its subsections, from the document a whole-file reference names, as the corpus fixture `fixtures/inclusion/an-include-keeps-only-the-named-sections` shows.
- [ ] **AC13.** A preset holding both `include` and `exclude` carries the included sections less the excluded ones, so an excluded subsection of an included section is withheld, as the corpus fixture `fixtures/inclusion/an-exclude-carves-within-an-include` shows.
- [ ] **AC14.** An inclusion naming a heading the target does not carry is silent, and an `include` matching none of the target's headings is refused with `E_EMPTIED_ENTRY` naming the reference, the target and the inclusions, as the corpus fixtures `fixtures/inclusion/an-unmatched-inclusion-is-silent` and `fixtures/inclusion/an-include-matching-nothing-is-refused` show.
- [ ] **AC15.** A reference of the form `document#fragment` is not narrowed by the target's `include`, as the corpus fixture `fixtures/inclusion/a-section-reference-is-not-narrowed` shows.
- [ ] **AC16.** A link written in a section the `include` leaves out is no dependency, so the document it names is not read through it, as the corpus fixture `fixtures/inclusion/a-left-out-sections-link-is-not-followed` shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions and the work items.
