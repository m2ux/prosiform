## Overview

`prosiform` holds **presets and nothing else**. A preset is a named block of conversion settings — the divisions a document joins and their depths, the paths its references resolve to instead, the sections it withholds — declared by a document to govern that document's own content when it is bundled. Which of its presets apply is selected by a keyword in the title of the section that links it, or of the entry document itself where a run names a document. Each document's `default` applies always; the presets a keyword selects layer on top of it.

## Problem

A document's declaration is flat, and a run is one set of options for every compilation.

- **Every setting is one per file.**
  `prosiform` admits `root`, `group` and `group-depth` and `metadata.decode` fails any other key. One group means one division, so a document cannot be carved into differently-named divisions for different consumers.
- **Options are run-wide.**
  `-m` and the budgets `argparse` reads are properties of the invocation. Exercising one artifact against stand-ins means running the whole closure against them, so a mode's unrelated dependencies are substituted too.
- **A setting cannot vary with the section that asked for it.**
  The material that needs substituting, excluding or re-grouping belongs to the artifact under authoring — the epic body being drafted, the conventions file being revised — and that artifact is a section of a larger closure. One run reaching two of its sections needs two settings, and a per-file block states one.
- **The word *profile* is taken.**
  `src/prosiform/__init__.py` holds `PROFILE = "skill-markdown-v4"`, the glossary defines *profile* as the named grammar and option set a run declares, and `-v` reports it. A second sense would make the contract's one defined term name two things.
- **Nothing states what a preset reached.**
  A bundle compiled against a preset and one compiled without are the same kind of output, and a preset no section named is indistinguishable from one that applied.

## Proposal

- **`prosiform` holds presets alone.**
  Every key in `prosiform` is a preset name whose value is a mapping. There is no top-level parameter: a key whose value is not a mapping is refused with `E_INVALID_CONVERSION_METADATA`, because `prosiform` states per-preset settings and nothing file-wide.
- **A document's presets govern its own content, selected by the section that links it.**
  For each link that reaches a document, the presets **of that document** whose names appear as words in the title of the section containing the link are selected, and their settings govern that document's content as the link bundles it. Several keywords in one title select several presets, and their settings union.
- **`default` always applies.**
  Each document's own `default` is in force wherever that document is compiled, and a keyword match layers above it. A keyword match never replaces it, and a document with no keyword match is compiled under its own `default` alone.
- **`default` is not selectable by keyword.**
  The name is reserved, so a heading titled `default` selects nothing by that spelling. Its one meaning is what is in force where no keyword matches.
- **A command-line entry reads the presets of the file it names.**
  An entry reference is written in no document, so the file it names is the document being operated on and its presets are the ones in force. A whole-document entry matches keywords against that document's own title heading; a section entry matches them against the section it names.
- **A preset governs the document that declares it, and nothing else.**
  A document's settings never reach the documents it links, nor the document that linked it. Each linked document is governed by its own `default` and by its own presets the linking section selects, so a parent's presets apply to the parent's content only when a further document bundles the parent.
- **No command-line channel exists.**
  A preset is the only way a conversion setting is stated, so a document whose `default` is empty and whose sites match no keyword substitutes nothing and withholds nothing. The `-m` option is retired with the substitution it introduced.
- **`group-depth` replaces `group`, and is applied per reference.**
  One field holds a list of single-entry mappings, each a division name mapped to its depth: `group-depth: [{protocols: 1}, {targets: 2}]`. `group` is refused, so the two halves of a pair are never written apart. A document may join several divisions at different depths. A document's selected preset supplies the pairs that place its own sections; [I09:E02 Section Placement](https://github.com/m2ux/prosiform/issues/458) states the order in which each composed result is merged into its parent.
- **A document in two divisions is emitted under each.**
  `group-depth: [{modes: 1}, {targets: 2}]` places the document's selected content under `Modes` and again under `Targets`. A merged group pools members, and a document in two of them is a member of both, so its regions appear in each. Within one division it is emitted once, by the rule `hierarchy.md` already states; across divisions the content is repeated, because each division is a separate top-level outline.
- **`exclude` holds names, not references, and applies only where a whole-file link names the target.**
  A list whose entries are a bare section name, or a single-entry mapping of name to heading level: `exclude: ["Draft", {Tests: 3}]`. Naming a section is the entry's meaning, so no `#` is written and the entry is not read by the reference grammar. The names are the **declaring document's own** sections, and the entry applies only where the link that selected the preset names that document whole — a link carrying a fragment selects a section and is never carved.
- **`subst` holds colon pairs, resolved from the declaring file.**
  `subst: [{rules.md: stub.md}]`, one single-entry mapping per pair, as `group-depth` writes its pairs. Its sides are references, and a side containing a colon followed by a space is quoted the YAML way, as `{"rules.md#Step 1: Setup": stub.md}`, because YAML splits a key there before the reference grammar reads it. It substitutes references the declaring document writes, and each side resolves from that document, as every other path in a document does, so one declaration reads the same wherever the run starts.
- **An entry is one string key with an integer value, or it is refused.**
  `exclude: [{Tests: 3, Draft: 3}]` and `exclude: [{3: 1}]` are both YAML-legal and neither is what an author could mean. Each fails with `E_INVALID_CONVERSION_METADATA` naming the entry, so the single-entry shape is grammar rather than convention.
- **Only what shapes the bundle is settable, and budgets are not.**
  A preset may hold `group-depth`, `exclude` and `subst`. A budget bounds a *bundle* rather than a document, so `-F`, `-B`, `-I`, `-O`, `-T`, `-L`, `-N` and `-E` are refused in frontmatter: a document raising its own ceiling would move a refusal away from the caller who chose it. `-o`, `-c`, `-d`, `-C`, `-v` and `-h` are refused on the same ground — none is the document's business.
- **Matched presets union, and a disagreement is refused.**
  Two matched presets naming one division at two depths, or mapping one `subst` key to two alternatives, is invalid usage with exit status `2`, naming the two presets and the entry they disagree about. A rule stated within one preset is likewise refused: two entries normalising to one identity, a key and its value normalising to one identity, and a key naming a section alone, as `#section` does, because a key names the document whose links it redirects. Silence is the worse answer, because one of the two settings would be applied and nothing would say which.
- **A preset nothing applied warns.**
  `W_PRESET_UNUSED` names the document and the preset, and accompanies a published bundle and exit status `0`. A preset on a document reached only through a deferral is not unused: the run that follows the deferral compiles it and reads the preset then.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/pull/507) | Design clause, the term | AC11 | | | ✓ |
| [W01](https://github.com/m2ux/prosiform/pull/509) | `prosiform` holds presets alone | AC1 | W00, [I08:E00:W00](https://github.com/m2ux/prosiform/issues/434) | | ✓ |
| [W02](https://github.com/m2ux/prosiform/pull/510) | `group-depth` as a list of pairs, `group` refused | AC12, AC13 | W01 | | ✓ |
| [W03](https://github.com/m2ux/prosiform/pull/511) | `exclude` and `path-sub` entry shapes | AC14 | W02 | | ✓ |
| [W04](https://github.com/m2ux/prosiform/pull/512) | Selecting a preset by keyword, and `default` | AC2, AC3, AC4 | W03, [I08:E00:W03](https://github.com/m2ux/prosiform/issues/434) | | |
| W05 | Matched presets union, and a disagreement is refused | AC5, AC16 | W09 | | |
| W06 | A preset nothing applied warns | AC6, AC7 | W05 | | |
| W07 | A deferred target keeps its preset | AC8 | W05 | | |
| W08 | The invocation and source page state presets | AC9, AC10 | W06 | | |
| W09 | `subst` holds colon pairs | AC15 | W04 | | |

## Acceptance Criteria

- [x] **AC1.** Every key in `prosiform` is a preset name holding a mapping, and a key whose value is not a mapping fails with `E_INVALID_CONVERSION_METADATA`, as the corpus fixtures `fixtures/inclusion/a-preset-key-holds-a-mapping` and `fixtures/inclusion/a-preset-key-holding-a-scalar-is-refused` show.
- [ ] **AC2.** A linked document is governed by its own presets whose names appear as words in the title of the section that links it, matched case-insensitively and as whole words, so a title `Checks and Draft` selects both presets and `Checklist` selects neither, as the corpus fixtures `fixtures/inclusion/a-section-title-selects-its-preset`, `fixtures/inclusion/a-title-matching-two-keywords-selects-both` and `fixtures/inclusion/a-presets-pairs-reach-the-reference-it-governs` show.
- [ ] **AC3.** Each document's own `default` applies wherever that document is compiled, and a keyword match layers above it rather than replacing it, as the corpus fixtures `fixtures/inclusion/default-applies-in-every-section` and `fixtures/inclusion/a-section-matching-no-preset-selects-default` show.
- [ ] **AC4.** A command-line entry reads the presets of the file it names — a whole-document entry matching against that document's own title heading, and a section entry against the section it names — as the corpus fixtures `fixtures/inclusion/a-whole-document-entry-selects-default` and `fixtures/inclusion/an-entry-name-reads-its-documents-presets` show.
- [ ] **AC5.** Matched presets union their settings, and a document's presets govern only that document's content — a linked document is governed by its own `default` and its own selected presets, never by the linking document's — as the corpus fixtures `fixtures/inclusion/a-preset-governs-its-own-document` and `fixtures/inclusion/a-dependencys-preset-comes-from-itself` show.
- [ ] **AC6.** A preset no site matched raises `W_PRESET_UNUSED` naming the document and the preset, and the run publishes with exit status `0`, as the corpus fixture `fixtures/inclusion/an-unused-preset-warns` shows.
- [ ] **AC7.** A preset on a document reached only through a deferral raises no warning, and the run that compiles the deferral reads it then, as the corpus fixture `fixtures/inclusion/a-deferred-target-keeps-its-preset` shows.
- [ ] **AC8.** A document declaring several presets is governed by the one its calling section's title selects for each reference, so one run reaching it twice may use two, as the corpus fixture `fixtures/inclusion/one-document-two-presets` shows.
- [ ] **AC9.** The invocation states the preset, the keyword rule, `default`, and what a match governs, and agrees with the command's help output, as `make invocation` shows.
- [ ] **AC10.** The source page states `prosiform` as presets, the two pair encodings and the refused keys, and the glossary distinguishes a preset from the grammar `profile`, as `make vocabulary` shows.
- [x] **AC11.** The design states presets as a property of the document whose content they govern, chosen by a keyword in the title of the section that links it, states `default` as always applying, states union and its refusal, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.
- [x] **AC12.** `group` is refused with `E_INVALID_CONVERSION_METADATA`, as the corpus fixture `fixtures/inclusion/a-declared-group-is-refused` shows.
- [x] **AC13.** `group-depth` holds a list of single-entry mappings, one document may join several divisions at different depths, a document's selected preset supplies the pairs that place its own sections, and a mapping entry holding two keys or a non-string key is refused, as the corpus fixtures `fixtures/inclusion/a-document-joins-two-divisions` and `fixtures/inclusion/a-malformed-group-entry-is-refused` show. The order composed results merge in is [I09:E02](https://github.com/m2ux/prosiform/issues/458)'s rule.
- [x] **AC14.** `exclude` holds bare section names and single-entry name-to-level mappings in one list, and a mapping entry holding two keys, a non-string key or a level outside one through six is refused naming the entry, as the corpus fixtures `fixtures/inclusion/an-exclude-list-holds-names-and-levels` and `fixtures/inclusion/a-malformed-exclude-entry-is-refused` show. The level telling a repeated heading apart is [I08:E02](https://github.com/m2ux/prosiform/issues/445)'s AC6.
- [ ] **AC15.** `subst` holds single-entry mappings from an original reference to its alternative, each side read by the reference grammar, and an entry that is not a single-entry mapping is refused naming the entry, as the corpus fixtures `fixtures/inclusion/a-subst-entry-is-a-colon-pair` and `fixtures/inclusion/a-subst-side-is-read-by-the-reference-grammar` show.
- [ ] **AC16.** Two matched presets disagreeing about one setting, two entries in one preset naming one division, two `subst` entries normalising to one identity, a `subst` key and value normalising to one identity, and a `subst` key naming a section alone, as `#section` does, are each invalid usage with exit status `2`, as the corpus fixtures `fixtures/inclusion/two-presets-disagreeing-are-refused`, `fixtures/inclusion/a-duplicate-subst-entry-is-refused` and `fixtures/inclusion/a-section-only-subst-key-is-refused` show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions and the work items.
