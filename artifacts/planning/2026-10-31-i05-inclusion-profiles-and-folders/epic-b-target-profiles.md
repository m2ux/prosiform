## Overview

`prosiform` holds **presets and nothing else**. A preset is a named block of conversion settings — the groupings a document joins and their depths, the substitutions its references take, the sections it withholds — selected by the section an entry reference names. A preset named `default` applies wherever no other is selected.

## Problem

A document's declaration is flat, and a run is one set of options for every compilation.

- **Every setting is one per file.**
  `prosiform` admits `root`, `group` and `group-depth` and `metadata.decode` fails any other key. One group means one division, so a document cannot be carved into differently-named divisions for different consumers.
- **Options are run-wide.**
  `-m` and the budgets `argparse` reads are properties of the invocation. Exercising one artifact against stand-ins means running the whole closure against them, so a mode's unrelated dependencies are mocked too.
- **A setting cannot vary with what a caller selected.**
  The material that needs substituting, excluding or re-grouping belongs to the artifact under authoring — the epic body being drafted, the conventions file being revised — and that artifact is a section of a larger closure rather than the whole of it.
- **The word *profile* is taken.**
  `src/prosiform/__init__.py` holds `PROFILE = "skill-markdown-v4"`, the glossary defines *profile* as the named grammar and option set a run declares, and `-v` reports it. A second sense would make the contract's one defined term name two things.
- **Nothing states what a preset reached.**
  A bundle compiled against a preset and one compiled without are the same kind of output, and a preset no section named is indistinguishable from one that applied.

## Proposal

- **`prosiform` holds presets alone.**
  Every key in `prosiform` is a preset name whose value is a mapping. There is no top-level parameter: a key whose value is not a mapping is refused with `E_INVALID_CONVERSION_METADATA`, because `prosiform` states per-preset settings and nothing file-wide.
- **`default` is the fallback, and its name is reserved.**
  A compilation selects the preset whose name equals the exact heading text of the section its entry reference names. Where no name matches — including an entry naming a whole document — `default` applies. A document may carry a heading headed `default`; naming it selects the fallback, and no preset can be selected by that name literally.
- **A preset subsumes.**
  The selected preset is the whole conversion setting for its compilation. A `-m` on the command line is the default for compilations that select no preset at all; where a preset is selected, it is the entire argument set, and nothing outside it reaches that compilation.
- **`group-depth` replaces `group`.**
  One field holds a list of single-entry mappings, each a group name mapped to its depth: `group-depth: [{protocols: 1}, {targets: 2}]`. `group` is refused, so the two halves of a pair are never written apart. A document may join several divisions, at different depths, in one preset.
- **A document in two divisions is emitted under each.**
  `group-depth: [{modes: 1}, {targets: 2}]` places the document's selected content under `Modes` and again under `Targets`. A merged group pools members, and a document in two of them is a member of both, so its regions appear in each. Within one division it is emitted once, by the rule `hierarchy.md` already states; across divisions the content is repeated, because each division is a separate top-level outline.
- **`exclude` holds names, not references.**
  A list whose entries are a bare section name, or a single-entry mapping of name to heading level: `exclude: ["Draft", {Tests: 3}]`. Naming a section is the entry's meaning, so no `#` is written and the entry is not read by the reference grammar.
- **`mock` holds pairs written as strings.**
  `mock: ["rules.md=stub.md"]`. Its sides are references, and a reference in a mapping key would collide with the colons a path may contain, so the pair keeps the `=` the option uses.
- **An entry is one string key with an integer value, or it is refused.**
  `exclude: [{Tests: 3, Draft: 3}]` and `exclude: [{3: 1}]` are both YAML-legal and neither is what an author could mean. Each fails with `E_INVALID_CONVERSION_METADATA` naming the entry, so the single-entry shape is grammar rather than convention.
- **Only what shapes the bundle is settable, and budgets are not.**
  A preset may hold `group-depth`, `exclude` and `mock`. A budget bounds a *bundle* rather than a document, so `-F`, `-B`, `-I`, `-O`, `-T`, `-L`, `-N` and `-E` are refused in frontmatter: a document raising its own ceiling would move a refusal away from the caller who chose it. `-f`, `-o`, `-c`, `-d`, `-x`, `-C`, `-v` and `-h` are refused on the same ground — none is the document's business.
- **A preset collision is refused.**
  Two entries in one preset's `mock` normalising to one identity, a key and its value normalising to one identity, and two entries naming one group are each refused as invalid usage.
- **A preset nothing applied warns.**
  `W_PRESET_UNUSED` names the document and the preset, and accompanies a published bundle and exit status `0`. A preset on a document reached only through a deferral is not unused: the run that follows the deferral compiles it and reads the preset then.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause, the term and the pin | AC11 | [E11:W00](https://github.com/m2ux/prosiform/issues/434) | | |
| W01 | `prosiform` holds presets alone | AC1 | W00 | | |
| W02 | `group-depth` as a list of pairs, `group` refused | AC12, AC13 | W01 | | |
| W03 | `exclude` and `mock` entry shapes | AC14, AC15 | W02 | | |
| W04 | Selecting a preset, and `default` | AC2, AC3, AC4 | W03, [E11:W03](https://github.com/m2ux/prosiform/issues/434) | | |
| W05 | A preset subsumes its compilation's arguments | AC5, AC16 | W04 | | |
| W06 | A preset nothing applied warns | AC6, AC7 | W05 | | |
| W07 | A deferred target keeps its preset | AC8 | W05 | | |
| W08 | The example tree and the corpus declare presets | AC17 | W03, [E11:W06](https://github.com/m2ux/prosiform/issues/434) | | |
| W09 | The preset stated in the invocation and the source page | AC9, AC10 | W06, W08 | | |

## Acceptance Criteria

- [ ] **AC1.** Every key in `prosiform` is a preset name holding a mapping, and a key whose value is not a mapping fails with `E_INVALID_CONVERSION_METADATA`, as the corpus fixtures `fixtures/inclusion/a-preset-key-holds-a-mapping` and `fixtures/inclusion/a-preset-key-holding-a-scalar-is-refused` show.
- [ ] **AC2.** A compilation selects the preset whose name equals the exact heading text of the section its entry reference names, as the corpus fixture `fixtures/inclusion/a-section-matching-a-preset-is-compiled-under-it` shows.
- [ ] **AC3.** A compilation whose section matches no preset name, and one whose entry names a whole document, both select `default`, as the corpus fixtures `fixtures/inclusion/a-section-matching-no-preset-selects-default` and `fixtures/inclusion/a-whole-document-entry-selects-default` show.
- [ ] **AC4.** A document whose `prosiform` carries no `default` and whose section matches no preset compiles under the run's options with no conversion setting, as the corpus fixture `fixtures/inclusion/no-default-and-no-match-is-bare` shows.
- [ ] **AC5.** The selected preset is the whole argument set: a `-m` pair the preset does not name does not reach that compilation, as the corpus fixture `fixtures/inclusion/a-preset-subsumes-the-command-line` shows.
- [ ] **AC6.** A preset no compilation selected raises `W_PRESET_UNUSED` naming the document and the preset, and the run publishes with exit status `0`, as the corpus fixture `fixtures/inclusion/an-unused-preset-warns` shows.
- [ ] **AC7.** A preset on a document reached only through a deferral raises no warning, and the run that compiles the deferral reads it then, as the corpus fixture `fixtures/inclusion/a-deferred-target-keeps-its-preset` shows.
- [ ] **AC8.** A document declaring several presets is compiled under the one its section names for each compilation, so one run reaching it twice may use two, as the corpus fixture `fixtures/inclusion/one-document-two-presets` shows.
- [ ] **AC9.** The invocation states the preset, the fallback and what it governs, and agrees with the command's help output, as `make invocation` shows.
- [ ] **AC10.** The source page states `prosiform` as presets, the two pair encodings and the refused keys, and the glossary distinguishes a preset from the grammar `profile`, as `make vocabulary` shows.
- [ ] **AC11.** The design states presets as a property of a compilation chosen by a section's heading text, states subsumption and the fallback, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.
- [ ] **AC12.** `group` is refused with `E_INVALID_CONVERSION_METADATA`, as the corpus fixture `fixtures/inclusion/a-declared-group-is-refused` shows.
- [ ] **AC13.** `group-depth` holds a list of single-entry mappings, one document may join several divisions at different depths, and a mapping entry holding two keys or a non-string key is refused, as the corpus fixtures `fixtures/inclusion/a-document-joins-two-divisions` and `fixtures/inclusion/a-malformed-group-entry-is-refused` show.
- [ ] **AC14.** `exclude` holds bare section names and single-entry name-to-level mappings in one list, and the level selects which heading of a repeated name is meant, as the corpus fixture `fixtures/exclusion/a-level-tells-a-repeated-heading-apart` shows.
- [ ] **AC15.** `mock` holds `ORIGINAL=ALTERNATIVE` strings whose sides are read by the reference grammar, as the corpus fixture `fixtures/inclusion/a-mock-entry-is-a-pair-string` shows.
- [ ] **AC16.** Two entries in one preset naming one group, two `mock` entries normalising to one identity, and a `mock` key and value normalising to one identity are each invalid usage with exit status `2`, as the corpus fixtures `fixtures/inclusion/a-duplicate-group-entry-is-refused` and `fixtures/inclusion/a-duplicate-mock-entry-is-refused` show.
- [ ] **AC17.** Every document in the example tree and every corpus source declares its settings inside a preset, no document declares `group`, and the published example bundles are unchanged by the migration, as `make corpus` and `make examples` show.

## References

- **R0.** Epic — [I05:E13 Target Presets](https://github.com/m2ux/prosiform/issues/436).
- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions and the work items.
- **R2.** [Declared Inclusion](https://github.com/m2ux/prosiform/issues/434) — the epic that opens the key set this one fills.
- **R3.** [I05:E14 Exclusion](https://github.com/m2ux/prosiform/issues/445) — the epic whose `exclude` entry this one's grammar states.
