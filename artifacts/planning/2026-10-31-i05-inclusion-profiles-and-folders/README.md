# Declared Inclusion, Section Presets and Exclusion — October 2026

> Epic set · Created 2026-10-31

## Executive Summary

Three changes to what a run carries and how an argument reaches it. The first retires `prosiform.root`: a local Markdown link is bundled when the document it names declares `prosiform`, and a document's boundary is derived from the links it writes rather than declared. The second admits named *presets* in frontmatter, so a document's content is compiled under its own presets, selected by a keyword in the title of the section that links it. The third removes a named section from what a whole-file link carries, so one preset carves one source several ways for several consumers. A fourth change — a folder pairing in `-m` — moved to [I08:E07](https://github.com/m2ux/prosiform/issues/414), and retires with that option.

They are one record because two of them are ordered by the first. Today `prosiform` admits exactly three keys and refuses any other; a preset is a key that is neither. And today a substitution is exempt from the writing source's root because the root is a boundary; once a boundary is derived from links, what bounds a substitute has to be stated against that instead. Delivering presets first would mean writing the key rule twice.

The set is three epics. **Declared Inclusion** is the load-bearing one: it moves link classification from where a file sits to whether the file opts in, which changes the answer for every document in the example tree, every root-declaring fixture and eleven pages of documentation. **Section Presets** follows, admitting the key rule a preset is written under and the keyword rule that selects one. **Exclusion** lands last, because a carve-up is a preset's use.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Declared Inclusion](epic-a-declared-inclusion.md) | [I08:E00](https://github.com/m2ux/prosiform/issues/434): the epic retiring `root`, with the declaration, the probe, classification and the derived boundary |
| [Section Presets](epic-b-section-presets.md) | [I08:E01](https://github.com/m2ux/prosiform/issues/436): the epic admitting named presets, the keyword that selects one, and `default` |
| [Exclusion](epic-d-exclusion.md) | [I08:E02](https://github.com/m2ux/prosiform/issues/445): the epic removing a named section from what a whole-file link carries |
| [A: design clause](a-w00.md) | The clause, the retired codes and the pin |
| [A: metadata](a-w01.md) | Declaration presence, the empty block and the `root` refusal |
| [A: probe](a-w02.md) | Reading a declaration without capturing a source |
| [A: classification](a-w03.md) | The seam that answers whether a link is a dependency |
| [A: absent targets](a-w04.md) | Text for a link naming nothing, a refusal for one an operator marks |
| [A: derived boundary](a-w05.md) | The boundary a document's own links state, and the entry refusal |
| [A: example and eval trees](a-w06.md) | Declaring 95 example documents and the 118 eval documents |
| [A: corpus](a-w07.md) | Every fixture family declaring rather than rooting |
| [A: documentation](a-w08.md) | Eleven pages and five drawings that state the declaration |
| [A: invariants](a-w09.md) | The one settled selection and the boundary that refuses no link |
| [B: design clause](b-w00.md) | The clause, the term and the pin |
| [B: presets only](b-w01.md) | `prosiform` holding presets and nothing else |
| [B: divisions](b-w02.md) | `group-depth` as pairs, applied per reference |
| [B: entry shapes](b-w03.md) | `exclude` and `path-sub` entries |
| [B: selection](b-w04.md) | Choosing a preset by keyword, and `default` |
| [B: union](b-w05.md) | Several governing presets, and the refusal of a disagreement |
| [B: unused presets](b-w06.md) | The warning for a preset no site matched |
| [B: deferred targets](b-w07.md) | A preset kept for the run that follows the deferral |
| [B: trees](b-w08.md) | The example tree and corpus declaring presets |
| [B: documentation](b-w09.md) | The preset stated in the invocation and the source page |
| [D: design clause](d-w00.md) | The clause, the code and the pin |
| [D: grammar and seam](d-w01.md) | The exclusion grammar, its refusals and the narrow settlement |
| [D: closure](d-w02.md) | An excluded section's links are no dependency |
| [D: whole-file scope](d-w03.md) | A reference naming a section is not carved |
| [D: level](d-w04.md) | A level telling a repeated heading apart |
| [D: empty contribution](d-w05.md) | A reference the preset empties is refused |
| [D: frontmatter](d-w06.md) | A preset carrying an exclusion, and the top-level key refused |
| [D: documentation](d-w07.md) | The selection page and the source page state it |
| [Remove the Referrer](epic-e-remove-referrer.md) | [I08:E03](https://github.com/m2ux/prosiform/issues/449): the epic removing `-f` and the bare-fragment form |
| [E: design clause](e-w00.md) | The clause, the retired option and the pin |
| [E: parser and refusal](e-w01.md) | The option's removal and the usage error that replaces it |
| [E: derived name](e-w02.md) | A section entry naming its own document |
| [E: corpus](e-w03.md) | The three fixtures withdrawn or rewritten |
| [E: documentation](e-w04.md) | The table and the guide without the row |
| [E: superseded work](e-w05.md) | E07's redirected-referrer criterion |
| [Conformance Faults](epic-f-conformance-faults.md) | [I08:E04](https://github.com/m2ux/prosiform/issues/450): the epic moving `-x` to `PROSIFORM_FAULT` |
| [F: design clause](f-w00.md) | The contract section, the variable and the pin |
| [F: reader](f-w01.md) | The option's removal and the environment read |
| [F: runner](f-w02.md) | The manifest field reaching the run |
| [F: documentation](f-w03.md) | The table and the guide without the row |
| [F: corpus page](f-w04.md) | The field stated as a behaviour |
| [F: fixtures](f-w05.md) | The three fault fixtures unchanged |
| [Named Budgets](epic-g-named-budgets.md) | [I08:E05](https://github.com/m2ux/prosiform/issues/451): the epic collapsing eight budget letters into one named option |
| [G: design clause](g-w00.md) | The clause, the eight names and the pin |
| [G: option](g-w01.md) | The option, its parser and its refusals |
| [G: limits](g-w02.md) | Each ceiling gaining a name |
| [G: corpus](g-w03.md) | The sixteen fixtures rewritten to names |
| [G: documentation](g-w04.md) | One table row and the examples |
| [Preset-Only Substitution](epic-h-preset-only-path-sub.md) | [I08:E06](https://github.com/m2ux/prosiform/issues/461): the epic retiring `-m` |
| [H: design clause](h-w00.md) | The clause, the retired option and the pin |
| [H: option](h-w01.md) | The option's removal and the preset read |
| [H: path basis](h-w02.md) | A pair resolving from its declaring file |
| [H: corpus](h-w03.md) | The `-m` fixtures rewritten to presets, and the retired ones withdrawn |
| [H: superseded work](h-w04.md) | E07's `mock`-named criteria |
| [H: documentation](h-w05.md) | The table and the source page |
| [H: own links](h-w06.md) | A pair reaching only its declaring document's links |
| [H: entry](h-w07.md) | An entry reference compiled as named |
| [H: folder pair](h-w08.md) | The folder pair refused and its code removed |
| [H: scenarios](h-w09.md) | The example scenarios stating their stand-ins in presets |
| [E07 W13: selection](e07-w13.md) | A heading outside the selection recording no substitution |
| [Declared Tree](epic-i-declared-tree.md) | The bulk migration: the example and corpus trees declare presets, once every field rule has landed |
| [I: example tree](i-w00.md) | The example tree declaring presets in one edit |
| [I: corpus](i-w01.md) | The corpus sources declaring presets |
| [I: eval tree](i-w02.md) | The workflow documents declaring |
| [I: checks](i-w03.md) | The checks that read a declaration |
| [Joins and ordering](joins.md) | The rows that share a pull request, and why the epics are ordered E00, E01, E02 |

## Design

### Inclusion

A link is followed when its target declares `prosiform`. Nothing about where either file sits decides it. The declaration is read from the target's leading frontmatter, so the question is answered by opening the target — which the pipeline does with a **probe** that reads the frontmatter span alone, bounded by the existing byte budget, before deciding whether to capture the document whole.

### Boundary

A document's **derived boundary** is the deepest directory that holds every local Markdown path its own links name, normalised from the document's directory; a document linking no such path has its own directory. The boundary states what the declaration used to state: the deepest place the author already reached.

It is worth being exact about what the boundary now refuses, because `root` refused a great deal. It refuses **no authored link**, by construction — every link a document writes resolves inside it. It confines a positional entry reference, and it is the value a diagnostic names when a path leaves it. Anything else `root` used to bound — a `path-sub` pair a preset names — is frontmatter material rather than authored text, and the clause states each one's confinement in its own right.

### Classification

`closure.resolvable`, `bundled` and `withholding_target` answer from the target's captured declaration rather than from a `covers` test against a root. `OutsideRoot` survives only for the forms no path grammar admits: a drive path, an absolute path, a path normalising above the invocation working directory. `E_SOURCE_OUTSIDE_ROOT` survives with those cases; `E_ROOT_NOT_FOUND` retires.

### Absent targets

A link naming a document that exists and does not declare is text, and a link naming a document that does not exist is text too, because in neither case does anything state that the bundle is responsible for it. The statement of responsibility moves to the operators: a link whose text opens with an operator, and a fragment-only link, name a compilation or a section of the document itself, and each still fails with `E_TARGET_NOT_FOUND` when nothing is there.

This is the one behaviour the change makes weaker, and it is stated rather than softened: a misspelled link under a directory a previous `root` covered used to fail the run, and now reaches the bundle as authored.

### Presets

`prosiform` holds presets and nothing else: every key is a preset name whose value is a mapping, and a key whose value is anything else is refused. There is no top-level parameter, because a file-wide setting cannot vary with the section that asked for it.

A preset is a named block of settings. A document is governed by its own presets whose names appear as words in the title of the **section that links it** — case-insensitive and whole-word, so `Checks` matches a title `Checks and Draft` and not `Checklist` — and several keywords in one title select several presets, whose entries union. An entry reference is written in no document, so the file it names supplies the presets: a section entry matching against the section it names, and a whole-document entry against that document's own title heading. A preset no site matched raises `W_PRESET_UNUSED`.

`default` is always in force and its name is reserved. A document's `default` applies wherever that document is compiled or writes a reference, and a keyword match layers above it rather than replacing it; a heading titled `default` selects nothing by that spelling. A document reached as a dependency applies its own `default` and its own presets the linking section selects. It takes no preset from the document that linked it and gives none to the documents it links.

A preset holds three entries. `group-depth` is a list of single-entry mappings, each a division name mapped to its depth, so one document may join several divisions, and a document's selected preset supplies the pairs that place its own sections. [I09:E02 Self-Placement](https://github.com/m2ux/prosiform/issues/458) composes each result into its parent from the leaves up. `exclude` is a list of the declaring document's own section names, or of single-entry mappings from a name to a heading level, applied where the link that selected the preset names that document whole. `path-sub` is a list of `ORIGINAL=ALTERNATIVE` strings whose sides resolve from the file that declares the preset, substituting only the links that file writes. Budgets are refused there: a budget bounds a bundle rather than a document, so `--budget` on the command line is the only place one is set.

### Substitution

`path-sub` is the only channel. [I08:E06](https://github.com/m2ux/prosiform/issues/461) retires `-m`, so a link written by a document whose selected presets state no `path-sub` is compiled as authored. A pair substitutes only the links its declaring document writes: an entry reference, the documents it links, the document linking it, a substitute and a dispatched target are each governed by their own presets alone, so a substitute's fragment-only link stays on that substitute. A document under two selected presets consults both — a key they map to two alternatives being refused rather than silently resolved. A key naming a section alone and a side ending in a separator are refused, so a folder of stubs is written one pair at a time. `W_PATH_SUB_USED` names each redirect and `W_PATH_SUB_UNUSED` names a pair no reference named.

### Exclusion

Selection only adds, so a preset can withhold part of a target. A preset holds an `exclude` of sections, and each is removed from the content a **whole-file reference** carries: `[Rules](rules.md)` is carved, and `[Rules](rules.md#Tests)` is not, because an explicit section is the more specific statement. The names are the **declaring document's own** headings, removed where a link names that document whole and selects the preset, and no entry names a document because a preset governs only the document that declares it. No top-level form exists: a list is a preset's shape.

The grammar is a bare section with an optional level: `exclude: ["Draft"]`, and `{"Tests": 3}` to name the level-3 heading of a repeated name. An exclusion removes what a fragment of the same name would select — the heading, its content and every subsection beneath it — so inclusion and exclusion describe one shape.

Two properties make it a carve-up rather than a trim. A link written inside an excluded section is no dependency, so the document it names is never read, and a document another link also reaches arrives by that surviving link. And a section one reference excludes arrives whole by a second reference under a preset excluding nothing, so a conflicting second statement is not refused — it is a second statement, and both are stated.

An exclusion naming a heading the declaring document does not carry is silent, because a preset governs many references and many documents that vary. A reference whose target is emptied by that preset's exclusions is refused with `E_EXCLUDED_ENTRY`, because a reference that names a document whole and receives none of it states a contradiction. A deferral is not carried across: what a later run withholds is that run's business.

## The split

I05's goal was a quality bar, true of every epic forever, so it could be neither reached nor reviewed against. Its 25 epics held three unrelated subjects, and each is now an initiative whose goal its epics can make true: [I08 Argument Surface](https://github.com/m2ux/prosiform/issues/462) holds this record's epics, [I09 Grouping and Composition](https://github.com/m2ux/prosiform/issues/463) holds the grouping work raised alongside it, and [I10 Evaluation and Checks](https://github.com/m2ux/prosiform/issues/464) holds the corpus and session work. I05 is closed.

Every epic in this record is numbered in I08's series, and each letter below names the record's artifact for it: E00 Declared Inclusion, E01 Section Presets, E02 Exclusion, E03 Remove the Referrer, E04 Conformance Faults, E05 Named Budgets, E06 Preset-Only Substitution, E07 Mock Substitution and E09 Declared Tree. The letters predate the split and the tracker's numbers are authoritative; the work-item files keep their letter, so a file named `a-w03.md` holds E00's third row. E08 is Mapping Refusal, a closed epic this record did not plan; it held E08 first, so the tree takes E09.

## Optimisation

Three changes shorten the critical path, each taken because review attention is the constraint rather than agent capacity.

- **One pin moves for every clause.** Seven epics each amended the design and moved the pin, and conformance reads the design at the pinned revision, so those seven pull requests were a strict chain. E00:W00 now moves the pin once and the other six amendments land beside it: seven level-0 rows instead of a seven-row chain.
- **The example tree is edited once.** E00:W06 declared 95 documents and E07:W00 migrated them to presets, and E07 depends on E00, so the same files were edited twice with each edit proving the bundles unchanged. Both now land in E07:W00, and E00's chain is one row shorter.
- **The boundary no longer waits on absent targets.** E00:W05 depended on W04 for adjacency rather than for code: the boundary is the longest common directory holding a document's own links, which has nothing to do with the absent-target refusal. Both rows now sit at one level.

The joins record accounts for every pair the changes made eligible. What remains on the critical path is Declared Inclusion: W01 through W08, with the corpus families and the documentation pages as consecutive bulk edits at its end.

## Initiative criteria

I05's criteria were a quality bar true of every epic forever, and the split renumbered the epics without replanning them. Every I08 row therefore cited all three bars, which made the Coverage column say the same thing nine times and left the initiative with no way to record partial delivery.

The criteria are replanned at the initiative's own grain. Each states an outcome the epics realise together, not one an epic realises alone.

| Criterion | Outcome | Served by |
| --- | --- | --- |
| AC1 | No argument reaches a run outside one grammar | E01, E02, E03, E04, E05 |
| AC2 | Whether a reference is compiled follows from its target's declaration | E00 |
| AC3 | A conversion setting reaches a compilation only through a named preset | E01, E06, E07 |
| AC4 | A bundle can be carved by removing named sections | E02 |
| AC5 | An excluded section contributes no dependency | E02 |
| AC6 | Every ceiling is named rather than lettered | E05 |
| AC7 | Every fault is driven by environment alone | E04 |
| AC8 | The example and corpus trees state their settings in presets | E09 |
| AC9 | Every added behaviour is reached by an end-to-end fixture | each epic adding surface |
| AC10 | The documented surface describes every added behaviour | each epic adding surface |
| AC11 | The checks pass on each delivering revision | every epic |
| AC12 | The initiative may close once every epic is delivered | none; it is the closure condition |

- **AC1, AC3, AC4, AC5, AC6, AC7 and AC8 are coarser than any epic's own criteria.** Each states what the argument surface achieves once several epics have landed, which is why several epics serve one.
- **AC9, AC10 and AC11 survive from I05 deliberately.** They were bars rather than outcomes, and at initiative grain a quality gate over the whole surface is the right shape for them.
- **AC12 is the only criterion no epic serves.** Closure rests on it and on the Done column, which is what makes partial delivery readable.

## Decisions

- **Inclusion is target-side, on the frontmatter declaration.** A local Markdown link is a dependency when its target declares `prosiform`. (User, 2026-10-31.)
- **No path boundary decides a link.** `prosiform.root` retires and a link outside every previous root is compiled when its target declares. (User, 2026-10-31.)
- **A document's boundary is derived from its own links: the deepest directory holding each relative path it names.** (User, 2026-10-31.)
- **A folder pair was a trailing separator on both sides, `-m rules/=stubs/`.** No glob, no second pattern syntax. It retired with `-m`: a preset states one pair per entry, so a folder of stubs is written one entry at a time. (User, 2026-10-31.)
- **A preset is selected by keyword, in the title of the section that links the document declaring it.** Case-insensitive, whole-word, and several keywords in one title select several presets. A document's presets govern its own content, so the section that reaches the document chooses which apply. (User, 2026-11-01.)
- **A preset governs only the document that declares it.** It never reaches the documents its file links, nor the file that linked it. (User, 2026-11-01.)
- **`path-sub` substitutes only the links its own file writes.** A stand-in is reached by adding a preset to the file under test; an entry reference is written by no document, so it is compiled as named. (User, 2026-11-01.)
- **A `path-sub` key naming a section alone is refused.** A key names the document whose link it redirects, so `#section` names none. (User, 2026-11-01.)
- **The epics are numbered in the order the graph orders them.** E00 changes the key rule and the classification every later epic reads; E01 is the largest and states the preset a carve-up is written as; E02 is the carve-up itself. (Agent, 2026-10-31.)
- **Priority is the map the task graph derives.** An epic whose first row has no inbound edge carries the largest number, and each other takes one less than the smallest its prerequisites carry, so the board mirrors the edges rather than a reading of effort. The current map is E00 8, E01 7 and E02 through E06 5, with E09 1 as the migration that waits on all of them. (User, 2026-10-31.)
- **The folder pairing moved to I08:E07, and retired with its option.** A folder side was a shape of `-m`, which [I08:E06](https://github.com/m2ux/prosiform/issues/461) retires. A preset's `path-sub` entry inherits the pair syntax, so the folder form goes with the option and a preset states one pair per entry. (User, 2026-10-31.)
- **`root` is refused rather than ignored.** A declaration that silently does nothing reads as declaration that took effect, and this repository carries no backward-compatibility layer. (Agent, 2026-10-31.)
- **A declaration is probed, not captured.** Reading every cited document whole to learn that it declares nothing spends the source budget on material the bundle does not carry. (Agent, 2026-10-31.)
- **An absent document is text, and the operators keep the failure.** The run cannot tell a citation from a typo without the declaration that would answer it, so responsibility is stated by the mark instead. (User, 2026-10-31.) An existing document that declares nothing is text too, which is the cost accepted in exchange for a target that qualifies itself.
- **The boundary refuses no authored link.** Deriving it from the links makes that a property rather than a policy, and the clause says so rather than implying a confinement it no longer performs. (Agent, 2026-10-31.)
- **Every argument value is a list, for every argument.** One shape for a repeatable option and a single-valued one, and a scalar is refused rather than read as a list of one. (User, 2026-10-31.)
- **A whole-document entry matches against the entry document's own title heading.** It names no section, so the nearest title its document holds is the one keywords are read against, and `default` is in force beneath it. (User, 2026-11-01.)
- **A property the construction holds is held by a check.** Discovery reading one selection and the boundary refusing no authored link are invariants an author cannot break, so each is asserted by a fixture rather than left as prose. (User, 2026-10-31.)
- **An entry reference is held to the same declaration.** The command line is the one selection made outside the link mechanism, so a document that declares nothing cannot be reached by argument either. (Agent, 2026-10-31.)
- **The per-compilation setting is a `preset`.** `profile` already names the grammar `skill-markdown-v4`, reported by `-v` and defined in the glossary; a second sense would make the contract's one defined term name two things. (User, 2026-10-31.)
- **Exclusion is the subtractive half of selection.** A named section is removed rather than filtered from the output, so the run reads fewer sources and the consumer receives only what remains. (User, 2026-10-31.)
- **An exclusion is declared in a preset, and its scope is the declaring document's own content where a link names that document whole.** No entry names a document, and there is no command-line form: what a preset withholds belongs to the document that declares it, and the names are its own headings. An exclusion naming a heading that document lacks is silent. (User, 2026-11-01.)
- **A document in two divisions is emitted under each.** One division is one outline, so a document joining two is a member of both and its regions appear in each. (User, 2026-10-31.)
- **The example tree and corpus migrate to presets in E01.** E00 removes `root` and leaves the flat group pair, so E01 needs a row that rewrites the tree rather than leaving it uncompilable. (User, 2026-10-31.)
- **Each document's own `default` is always in force, and a keyword match layers above it.** A document reached as a dependency applies its own and takes nothing from the document that linked it, so a preset changes one reference and never a closure. (User, 2026-11-01.)
- **Matched presets union, and a setting two of them state differently is refused.** One alternative for one key is what the entry means, so a second is a contradiction; silence would ship one of the two and say nothing about which. (User, 2026-11-01.)
- **A document's selected preset places its own sections, and composition is I09's rule.** A document's `group-depth` pairs place that document's sections, and [I09:E02 Self-Placement](https://github.com/m2ux/prosiform/issues/458) composes each result into its parent from the leaves up. This record states only the entry a preset supplies those pairs through. (User, 2026-11-01.)
- **An exclusion applies to a whole-file reference only, and names the declaring document's own sections.** A reference carrying a fragment is an explicit statement and the more specific one, so a preset's carve does not overrule it; a preset governs only its own document, so no entry names one. (User, 2026-11-01.)
- **The substitution channel is `path-sub`, and its warnings are named for it.** The option and the entry were both called `mock`, a word for the scaffolding the feature was raised for rather than the thing it does; `W_PATH_SUB_USED` and `W_PATH_SUB_UNUSED` report it under one name. (User, 2026-11-01.)
- **E01 is titled Section Presets and keeps its number.** A preset is chosen by the title of the section that links its document, so the old title named the rule this record replaces. (User, 2026-11-01.)
- **`-m` is retired: a preset's `path-sub` is the only channel.** A reference under a preset stating none substitutes nothing. Two channels for one setting meant a reference had two possible answers. (User, 2026-10-31.)
- **A preset's pair resolves from the declaring file.** A document states its own neighbours, so one declaration reads the same from any working directory — unlike the option, which had no declaring file and read from the invocation directory. (User, 2026-10-31.)
- **The eight budgets collapse into one `--budget NAME=VALUE`.** Eight siblings of identical shape are one decision rendered eight times, since the parser generates them from one table. Named ceilings also remove the `-o`/`-O` collision, which no arrangement of letters fixes. (User, 2026-10-31.)
- **The fault moves out of the option surface to `PROSIFORM_FAULT`.** A shipped flag whose only consumer is the corpus reads as a feature a caller may use. The corpus already abstracts the fault through a manifest field, so the channel is the runner's business and the option goes. (User, 2026-10-31.)
- **`-f` and the bare-fragment form are removed.** Every use is rewritable as `document#fragment`, the bare form is a usage error for the thing a caller types first, and three fixtures carry it with no consumer. The link form `[x](#section)` is untouched. (User, 2026-10-31.)
- **A fault stays a command-line concern.** `-x` reaches codes no source tree produces, which is a harness need rather than a document's: `internal` means the tool fails in itself and `cleanup-refused` is about the output folder, so neither has a document to attach to. `source-changed` could not be declared in the file it corrupts, because frontmatter is read during capture and the corruption would follow the read that learns of it. A `prosiform` key holding a fault would also put test scaffolding inside the material under test, which a preset refused on the same ground. (User, 2026-10-31.)
- **There is no top-level `exclude`.** A list is a preset's shape, so a top-level key holding one is a key whose value is not a preset mapping, and is refused. (User, 2026-10-31.)
- **A preset's exclusion is a bare section with an optional level.** The declaring document is the scope, so a qualifier would name the document the preset already belongs to. (User, 2026-10-31.)
- **A deferral is not carried across.** An exclusion governs what this run compiles; the later run's exclusions are its own. (User, 2026-10-31.)
- **An unmatched exclusion is silent, including one naming no heading of the target.** A preset governs many references and many documents that vary, so a miss is ordinary. (User, 2026-10-31.)
- **`W_PATH_SUB_UNUSED` reports per preset and per document.** A pair may be redundant for one reference and live for another, so the warning names the key and the document whose presets never used it. (User, 2026-10-31.)
- **The number after a section names its heading level, and never changes how much is cut.** It exists to tell two headings of one name apart, which a fragment already refuses as ambiguous. A level is optional: `#Section` is the document-level heading. (User, 2026-10-31.)
- **An excluded section's links are not followed.** The closure shrinks, so an exclusion is structural rather than cosmetic. (User, 2026-10-31.)
- **An unmatched exclusion is silent however it misses.** A name the target lacks and one two headings share at one level are both ordinary, because a preset governs many documents that vary. (User, 2026-10-31.)
- **A second reference that carries an excluded section is not a conflict.** The two references asked for two different things and both are stated, so nothing is refused; the only contradiction is a preset that empties the whole of what a reference names. (User, 2026-11-01.)
- **No option carries an exclusion.** There is no `--exclude` and no letter to spend: an exclusion is a preset entry, so what a document withholds is stated by that document's own preset rather than by the caller. (User, 2026-11-01.)
- **The initiative's `Depends on` cells are empty.** The rule derives a whole-epic edge only where every row of the dependent requires every row of the prerequisite, and no row pair here meets it. The gates live in the task edges and in the priority numbers. (User, 2026-10-31.)

## Review

Findings from the plan review against the source, all resolved.

| Finding | Severity | Resolution |
| --- | --- | --- |
| Both initiative `Depends on` cells named whole epics that no row pair derives, and `scripts/deps.py` refused them. | High | Both cells emptied; the couplings are task edges. |
| Seven independent pairs were named in neither Joins nor the record, so the checker reported every one. | High | Each pair accounted for in `joins.md` with its two ids on one line, and the reason it takes two pull requests stated. |
| The folder-mock epic consumed `E07`'s `-m` grammar and `E00`'s classification seam and named neither. | High | Retired: the work moved to `E07:W09`, which names `E00:W03`. |
| The three W00 rows contended on `design.md` under one priority number, with the sequencing stated only as prose. | Medium | Each W00 depends on the previous epic's W00, which is what the pin chain actually is. |
| The diagram-following eval's 118 workflow documents declare nothing, and `make harness` requires each form to bundle cleanly. | Critical | `E00:W06` covers the eval tree and states which forms it reaches. |
| Four `real-source` fixtures copy documents whose frontmatter declares nothing, and the family's rule forbids editing a copy. | High | `E00:W07` states where the declaration is added for a copied source. |
| Nothing stated whether an entry reference could name a document that declares nothing. | High | AC15 added, with a fixture, and `E00:W05` carries it. |
| `checks/smoke.py` writes `prosiform: {root: "."}`, so `make smoke` fails as soon as the refusal lands. | High | `E00:W06` owns the check's source and its retired-option assertion. |
| `profile` already names the grammar, and the epic reused it. | High | The concept is a `preset` throughout; the word clash is stated in the clause and the glossary check holds it. |
| `E00:W08` named six pages where eleven state a root. | Medium | AC13 lists all eleven, and AC14 covers the four worked examples and the drawings. |
| AC9 cited `make boundary` and the folder epic's AC6 cited `make mock-scenarios`; neither target existed. | Medium | `E00:W05` creates `make boundary`; `E07:W11` extends the target `E07:W08` lands and states that dependency. |
| The board held E01 and E02 at priority 5, level with the E07 epic that neither depends on and above the E00 epic both depend on; the graph derives E07 4, E00 3, E01 2, E02 1. | High | The derived map applied to the labels and recorded as a decision. |
| The folder rows read under the inclusion rule, which a reader could take for a dependency on `E00`. | Low | `E07:W09` states that the rule is E00's and that its stubs declare from the first, so the mechanism is buildable before E00 lands and no edge is asserted. The checker refuses a row depending on a later epic, and the row does not. |
| The record's `epic.md` still described ten rows and an unnumbered documented row, so the record and the tracker disagreed. | Medium | Regenerated from the published body. |
| The argument-name set was read from the parser, which makes `-o` and `-c` settable from frontmatter. | High | The settable set is named: `group-depth`, `exclude` and `path-sub`, held to the help output by a test. |
| An argument's value had two shapes, a scalar for `-m` and a list for `--exclude`. | Medium | Every argument value is a list, and a scalar is refused. |
| W02's body invented a title-matching rule for a whole-document entry that no criterion stated. | High | The rule is stated: a whole-document entry matches against the entry document's own title heading, which AC4 states and a fixture holds. |
| Two invariants stated in W04 and W05 were prose with no test behind them. | Medium | Each has a criterion now, and W09 carries the fixture and the boundary assertion. |
| Preset selection was a property of a compilation and the target's heading, so a section could not state how its own links were treated, and a document reached twice could not be treated twice. | High | Selection is by keyword in the title of the section that links a document, per link, and the selected presets govern that document's own content alone. |
| Per-link placement was stated here as well as in [I09:E02 Self-Placement](https://github.com/m2ux/prosiform/issues/458), which owns how a document's composed result merges into its parent. | High | This record states only the `group-depth` entry a preset supplies the pairs through; where those pairs place a target is I09:E02's, which gains a criterion and a row for it. |
| A selected preset replacing its compilation's whole setting left no room for a document's own `default` once it was reached as a dependency. | High | `default` is always in force and a keyword match layers above it; a dependency applies its own and inherits nothing beyond the reference. |
| Several keywords in one title select several presets and nothing stated how their entries meet. | High | Entries union, and a setting two of them state differently is refused as invalid usage rather than silently resolved. |
| An exclusion scoped to the declaring file named that file's headings, which is the wrong document once the preset is chosen by the linking section. | High | An exclusion names the declaring document's own sections and applies where a link names that document whole; `E_EXCLUDED_CONTENT` retires with the collision it refused. |
| The entry and both warning codes were named `mock`, a word for the scaffolding the feature was raised for, and E07's delivered criteria all carry it. | Medium | The entry is `path-sub` and the codes are `W_PATH_SUB_USED` and `W_PATH_SUB_UNUSED`; E07's `mock`-named criteria are marked superseded. |
| The delivered mapping is run-wide: it reaches the entry, every document's links and every dispatched bundle, and no criterion held a pair to its declaring document. | High | E06 W06 and W07 hold a pair to the links its file writes and compile an entry as named; E07 AC2 is superseded. |
| The folder pair retired here and survived in E07's code, six fixtures and the parser E06 kept for `path-sub`. | High | E06 W08 refuses a side ending in a separator and removes the folder code and fixtures; E07 AC25–AC31 are superseded and W11 withdrawn. |
| E06 named four `-m` fixtures; 25 pass it, and `make mock-scenarios` passes it in five scenarios that state no edit to the tree under test. | High | E06 AC4 covers every fixture with a disposition for retired capabilities, and W09 moves the scenarios to presets on the copied file. |
| A withheld link in a heading outside the selection marked its key served, so a run reported a substitution it never made and no unused key. | Major | E07 W13 records a substitution only for selected content. |
| E06's design row covered a fixture criterion and the epic stated no design criterion. | Medium | AC13 states the clause and W00 covers it; W05 covers AC6 and AC7. |

## Debt this record defers

- **[I08:E07](https://github.com/m2ux/prosiform/issues/414)'s root criteria are superseded.** AC6 and AC11 state a substitute's relation to a root, and E00 supersedes them; AC20 reads a substitute from the working directory, and E06's declared-file basis supersedes it. Their fixtures are withdrawn or rewritten by E06 W03.
- **`checks/authoring.py` holds a rule about link spelling written in terms of `root`.** Its `DECLARED_ROOT` pattern and `link_form` test exist because a root prefixed a link's spelling. The 2026-10-24 note already found the spy role gone; A retires the declaration the check reads, so the check is rewritten to the derived boundary rather than deleted outright, because it still catches a link written from the wrong directory.

## Open Questions

None outstanding. Every reading this record raised has been answered: the boundary is derived from the file's own links, a preset is chosen by a keyword in the title of the section that links its document with `default` always in force beneath it and governs that document alone, matched presets union and a disagreement is refused, an exclusion carves a whole-file reference by the declaring document's own headings, `-m` is retired so `path-sub` is the only channel and reaches only the links its file writes, and the fault leaves the option surface.

## Links

| Resource | Link |
| --- | --- |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Preceding epic | [I08:E07 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Epic A | [I08:E00 Declared Inclusion](https://github.com/m2ux/prosiform/issues/434) |
| Epic B | [I08:E01 Section Presets](https://github.com/m2ux/prosiform/issues/436) |
| Epic D | [I08:E02 Exclusion](https://github.com/m2ux/prosiform/issues/445) |
| Epic E | [I08:E03 Remove the Referrer](https://github.com/m2ux/prosiform/issues/449) |
| Epic F | [I08:E04 Conformance Faults](https://github.com/m2ux/prosiform/issues/450) |
| Epic G | [I08:E05 Named Budgets](https://github.com/m2ux/prosiform/issues/451) |
| Epic H | [I08:E06 Preset-Only Substitution](https://github.com/m2ux/prosiform/issues/461) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
