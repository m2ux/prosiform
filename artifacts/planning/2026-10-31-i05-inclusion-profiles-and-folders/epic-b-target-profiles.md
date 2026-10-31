## Overview

A file's declaration admits a **preset**: a named block of `-m` entries and budget overrides. The preset named for the section an entry reference selects applies to that compilation alone, so one artifact is compiled against stand-in material and a budget of its own while the rest of the run is unaffected.

## Problem

A run is one set of options, and one artifact is not the run.

- **Options are run-wide.**
  `-m` and the budgets `argparse` reads are properties of the invocation. Exercising one artifact against stand-ins means running the whole closure against them, so a mode's unrelated dependencies are mocked too and the run proves less than it appears to.
- **The key set is closed.**
  `prosiform` admits `root`, `group` and `group-depth`, and `metadata.decode` fails any other key with `E_INVALID_CONVERSION_METADATA`. A preset has nowhere to be written, so a caller keeping stand-in settings beside the document has to keep them on the command line, where they are neither versioned with the document nor reviewed with it.
- **The word *profile* is taken.**
  `src/prosiform/__init__.py` holds `PROFILE = "skill-markdown-v4"`, the glossary defines *profile* as "the named, versioned Markdown grammar and option set a run declares", and `-v` reports it. A second sense would make the glossary's one defined term name two things, and `make vocabulary` reads that glossary.
- **A stand-in is attached to a section, not to a run.**
  The material that needs substituting belongs to the artifact under authoring — the epic body being drafted, the conventions file being revised — and that artifact is a section of a larger closure rather than the whole of it.
- **Nothing states what a preset reached.**
  A bundle compiled against a preset and one compiled without are the same kind of output, and a preset no section named is indistinguishable from one that applied.

## Proposal

- **Two kinds of key, decided by the value.**
  A `prosiform` key that is an argument name holds that argument's value and applies it to every compilation of the file. Any other key whose value is a mapping is a **preset**, named by the key and holding a substitution and budget overrides. A key that is neither an argument name nor a mapping is refused, because it is a misspelled field rather than a preset.
- **Only an argument that shapes the bundle is settable.**
  The settable set is `mock`, `exclude` and the budgets — `-F`, `-B`, `-I`, `-O`, `-T`, `-L`, `-N` and `-E`. An option stating where a run writes or what it reports is not a document's business: `-o` would let a document redirect its own bundle and disagree with a sibling's, and `-c`, `-d` and `-x` describe the invocation rather than the content. A `prosiform` key naming one of those is refused as a misspelled field.
- **Every argument value is a list.**
  A repeatable option and a single-valued one state one shape, so `mock` and `exclude` alike hold a list of values and each entry is read by the option's own parser. A scalar is refused rather than read as a one-element list, because one shape is what makes the rule learnable.
- **A preset applies to one compilation.**
  A **bundle compilation** is one entry reference and everything it reaches: the run's own entry, and each dispatched target's. A preset applies to a compilation when the **section** that compilation's entry reference names has a heading text matching the preset's name. The name matched is the resolved heading text, not the fragment as written, because a fragment is written in a different document from the one that declares the preset and a URL-escaped fragment names no preset directly.
- **A matched preset governs its compilation's own resolution.**
  The preset's substitution entries join the run's mapping for that compilation only, and its budget overrides replace the run's for that compilation only. Each compilation starts from a fresh count already, so the count a preset overrides is that compilation's.
- **A preset collision is refused.**
  Two entries in one preset's substitution normalising to one identity, or a key and its value normalising to one identity, is invalid usage — the same two refusals `-m` carries, stated where the preset is read. A preset entry restating a `-m` entry for the same identity is refused too, because the two state one redirection twice and only one order makes a run reproducible.
- **A preset nothing applied warns.**
  `W_PRESET_UNUSED` names the document, the preset and the sections the run compiled, and accompanies a published bundle and exit status `0`. A preset on a document reached only through a deferral is not unused: the run that follows the deferral compiles that document and reads the preset then.
- **A declared preset is inert where the document is merged.**
  A preset governs a compilation's resolution, not its inclusion. A document whose section is merged into another compilation carries its content as that compilation's own preset directed, because one bundle answers to one set of options.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause, the term and the pin | AC12 | [E11:W00](https://github.com/m2ux/prosiform/issues/434) | | |
| W01 | The preset key and the argument-name key | AC1, AC2 | W00 | | |
| W02 | The settable set and the list value | AC13, AC15 | W01 | | |
| W03 | Matching a section name to a preset | AC3, AC4, AC7 | W02, [E11:W03](https://github.com/m2ux/prosiform/issues/434) | | |
| W04 | A whole-document entry matches no preset | AC14 | W03 | | |
| W05 | A preset's entries bound and collisions refused | AC5, AC6 | W03, [E09:W09](https://github.com/m2ux/prosiform/issues/414) | | |
| W06 | A preset nothing applied warns | AC8 | W05 | | |
| W07 | A deferred target keeps its preset | AC9 | W05 | | |
| W08 | The preset stated in the invocation and the source page | AC10, AC11 | W06 | | |

## Acceptance Criteria

- [ ] **AC1.** A `prosiform` key naming a preset whose value is a mapping is accepted, and the same key whose value is a scalar fails with `E_INVALID_CONVERSION_METADATA`, as the corpus fixtures `fixtures/inclusion/a-preset-key-holds-a-mapping` and `fixtures/inclusion/a-preset-key-holding-a-scalar-is-refused` show.
- [ ] **AC2.** A `prosiform` key naming an argument holds that argument's value and applies it to every compilation of that document, as the corpus fixture `fixtures/inclusion/an-argument-key-applies-to-every-compilation` shows.
- [ ] **AC3.** An entry reference naming a section whose heading text matches a preset in the entry document compiles under that preset's substitution, as the corpus fixture `fixtures/inclusion/a-section-matching-a-preset-is-compiled-under-it` shows.
- [ ] **AC4.** A section whose heading text matches no preset compiles under the run's own options, as the corpus fixture `fixtures/inclusion/a-section-matching-no-preset-is-unaffected` shows.
- [ ] **AC5.** A preset's substitution applies to that compilation alone, and a sibling compilation reached by the same run resolves the same identities without it, as the corpus fixture `fixtures/inclusion/a-preset-leaves-a-sibling-compilation-alone` shows.
- [ ] **AC6.** Two entries in one preset normalising to one identity, a key and value normalising to one identity, and a preset entry restating a `-m` entry are each invalid usage with exit status `2`, as the corpus fixtures `fixtures/inclusion/a-duplicate-preset-key-is-refused` and `fixtures/inclusion/a-preset-entry-restating-a-m-argument-is-refused` show.
- [ ] **AC7.** A budget override in a preset bounds that compilation and leaves the run's budget governing every other compilation, as the corpus fixture `fixtures/inclusion/a-preset-budget-bounds-one-compilation` shows.
- [ ] **AC8.** A preset no compiled section named raises `W_PRESET_UNUSED`, and the run publishes with exit status `0`, as the corpus fixture `fixtures/inclusion/an-unused-preset-warns` shows.
- [ ] **AC9.** A preset on a document reached only through a deferral raises no warning, and the run that compiles the deferral reads it then, as the corpus fixture `fixtures/inclusion/a-deferred-target-keeps-its-preset` shows.
- [ ] **AC10.** The invocation states the preset, its key rule and what it governs, and agrees with the command's help output, as `make invocation` shows.
- [ ] **AC11.** The source page states the two kinds of `prosiform` key and the preset's shape, and the glossary distinguishes a preset from the grammar `profile`, as `make vocabulary` shows.
- [ ] **AC12.** The design states presets as a property of a compilation chosen by a section's heading text, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.
- [ ] **AC13.** A `prosiform` key naming `-o`, `-c`, `-d`, `-x` or `-f` is refused with `E_INVALID_CONVERSION_METADATA`, as the corpus fixture `fixtures/inclusion/an-option-that-writes-is-not-settable` shows.
- [ ] **AC14.** An entry naming a whole document matches no preset, compiles under the run's own options, and a preset named for the document's title raises `W_PRESET_UNUSED`, as the corpus fixture `fixtures/inclusion/a-whole-document-entry-matches-no-preset` shows.
- [ ] **AC15.** Every argument value is a list, and a scalar value is refused with `E_INVALID_CONVERSION_METADATA`, as the corpus fixtures `fixtures/inclusion/an-argument-value-is-a-list` and `fixtures/inclusion/a-scalar-argument-value-is-refused` show.

## References

- **R0.** Epic - [I05:E13 Target Profiles](https://github.com/m2ux/prosiform/issues/436).
- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions and the work items.
- **R2.** [Declared Inclusion](epic-a-declared-inclusion.md) — the epic that opens the key set this one fills.
- **R3.** [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) — the mapping a preset's entries join.
