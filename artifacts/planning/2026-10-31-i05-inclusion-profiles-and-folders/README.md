# Declared Inclusion, Target Presets and Exclusion — October 2026

> Epic set · Created 2026-10-31

## Executive Summary

Three changes to what a run carries and how an argument reaches it. The first retires `prosiform.root`: a local Markdown link is bundled when the document it names declares `prosiform`, and a document's boundary is derived from the links it writes rather than declared. The second admits named *presets* in frontmatter, so a section an argument names is compiled under that argument. The third removes a named section from a bundle, so one preset carves one source several ways for several consumers. A fourth change — a folder pairing in `-m` — moved to [I08:E07](https://github.com/m2ux/prosiform/issues/414), because a folder side is a shape of the option that epic owns.

They are one record because two of them are ordered by the first. Today `prosiform` admits exactly three keys and refuses any other; a preset is a key that is neither. And today a substitution is exempt from the writing source's root because the root is a boundary; once a boundary is derived from links, what bounds a substitute has to be stated against that instead. Delivering presets first would mean writing the key rule twice.

The set is three epics. **Declared Inclusion** is the load-bearing one: it moves link classification from where a file sits to whether the file opts in, which changes the answer for every document in the example tree, every root-declaring fixture and eleven pages of documentation. **Target Presets** follows, admitting the key rule a preset is written under. **Exclusion** lands last, because a carve-up is a preset's use.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Declared Inclusion](epic-a-declared-inclusion.md) | [E11](https://github.com/m2ux/prosiform/issues/434): the epic retiring `root`, with the declaration, the probe, classification and the derived boundary |
| [Target Presets](epic-b-target-profiles.md) | [E13](https://github.com/m2ux/prosiform/issues/436): the epic admitting named presets and applying one to a compilation |
| [Exclusion](epic-d-exclusion.md) | [E14](https://github.com/m2ux/prosiform/issues/445): the epic removing a named section from a bundle |
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
| [B: groupings](b-w02.md) | `group-depth` as pairs, and the two divisions it allows |
| [B: entry shapes](b-w03.md) | `exclude` and `mock` entries |
| [B: selection](b-w04.md) | Selecting a preset, and `default` |
| [B: subsumption](b-w05.md) | A preset as its compilation's whole setting |
| [B: unused presets](b-w06.md) | The warning for a preset nothing selected |
| [B: deferred targets](b-w07.md) | A preset kept for the run that follows the deferral |
| [B: trees](b-w08.md) | The example tree and corpus declaring presets |
| [B: documentation](b-w09.md) | The preset stated in the invocation and the source page |
| [D: design clause](d-w00.md) | The clause, the two codes and the pin |
| [D: grammar and seam](d-w01.md) | The exclusion grammar, its refusals and the narrow settlement |
| [D: closure](d-w02.md) | An excluded section's links are no dependency |
| [D: conflict](d-w03.md) | Included content beneath an exclusion is refused |
| [D: empty contribution](d-w04.md) | A file withholding everything is refused |
| [D: level](d-w05.md) | A level telling a repeated heading apart |
| [D: frontmatter](d-w06.md) | A preset carrying an exclusion, and the top-level key refused |
| [D: documentation](d-w07.md) | The selection page and the source page state it |
| [Remove the Referrer](epic-e-remove-referrer.md) | [E15](https://github.com/m2ux/prosiform/issues/449): the epic removing `-f` and the bare-fragment form |
| [E: design clause](e-w00.md) | The clause, the retired option and the pin |
| [E: parser and refusal](e-w01.md) | The option's removal and the usage error that replaces it |
| [E: derived name](e-w02.md) | A section entry naming its own document |
| [E: corpus](e-w03.md) | The three fixtures withdrawn or rewritten |
| [E: documentation](e-w04.md) | The table and the guide without the row |
| [E: superseded work](e-w05.md) | E09's redirected-referrer criterion |
| [Conformance Faults](epic-f-conformance-faults.md) | [E16](https://github.com/m2ux/prosiform/issues/450): the epic moving `-x` to `PROSIFORM_FAULT` |
| [F: design clause](f-w00.md) | The contract section, the variable and the pin |
| [F: reader](f-w01.md) | The option's removal and the environment read |
| [F: runner](f-w02.md) | The manifest field reaching the run |
| [F: documentation](f-w03.md) | The table and the guide without the row |
| [F: corpus page](f-w04.md) | The field stated as a behaviour |
| [F: fixtures](f-w05.md) | The three fault fixtures unchanged |
| [Named Budgets](epic-g-named-budgets.md) | [E17](https://github.com/m2ux/prosiform/issues/451): the epic collapsing eight budget letters into one named option |
| [G: design clause](g-w00.md) | The clause, the eight names and the pin |
| [G: option](g-w01.md) | The option, its parser and its refusals |
| [G: limits](g-w02.md) | Each ceiling gaining a name |
| [G: corpus](g-w03.md) | The sixteen fixtures rewritten to names |
| [G: documentation](g-w04.md) | One table row and the examples |
| [Preset-Only Substitution](epic-h-preset-only-mock.md) | [E26](https://github.com/m2ux/prosiform/issues/461): the epic retiring `-m` |
| [H: design clause](h-w00.md) | The clause, the retired option and the pin |
| [H: option](h-w01.md) | The option's removal and the preset read |
| [H: path basis](h-w02.md) | A pair resolving from its declaring file |
| [H: corpus](h-w03.md) | The four fixtures rewritten to presets |
| [H: superseded work](h-w04.md) | E09's option criterion |
| [H: documentation](h-w05.md) | The table and the source page |
| [Joins and ordering](joins.md) | The rows that share a pull request, and why the epics are ordered E11, E13, E14 |

## Design

### Inclusion

A link is followed when its target declares `prosiform`. Nothing about where either file sits decides it. The declaration is read from the target's leading frontmatter, so the question is answered by opening the target — which the pipeline does with a **probe** that reads the frontmatter span alone, bounded by the existing byte budget, before deciding whether to capture the document whole.

### Boundary

A document's **derived boundary** is the deepest directory that holds every local Markdown path its own links name, normalised from the document's directory; a document linking no such path has its own directory. The boundary states what the declaration used to state: the deepest place the author already reached.

It is worth being exact about what the boundary now refuses, because `root` refused a great deal. It refuses **no authored link**, by construction — every link a document writes resolves inside it. It confines a positional entry reference, and it is the value a diagnostic names when a path leaves it. Anything else `root` used to bound — a substitute named on the command line, a path a preset names — is command-line or frontmatter material rather than authored text, and the clause states each one's confinement in its own right.

### Classification

`closure.resolvable`, `bundled` and `withholding_target` answer from the target's captured declaration rather than from a `covers` test against a root. `OutsideRoot` survives only for the forms no path grammar admits: a drive path, an absolute path, a path normalising above the invocation working directory. `E_SOURCE_OUTSIDE_ROOT` survives with those cases; `E_ROOT_NOT_FOUND` retires.

### Absent targets

A link naming a document that exists and does not declare is text, and a link naming a document that does not exist is text too, because in neither case does anything state that the bundle is responsible for it. The statement of responsibility moves to the operators: a link whose text opens with an operator, and a fragment-only link, name a compilation or a section of the document itself, and each still fails with `E_TARGET_NOT_FOUND` when nothing is there.

This is the one behaviour the change makes weaker, and it is stated rather than softened: a misspelled link under a directory a previous `root` covered used to fail the run, and now reaches the bundle as authored.

### Presets

`prosiform` holds presets and nothing else: every key is a preset name whose value is a mapping, and a key whose value is anything else is refused. There is no top-level parameter, because a file-wide setting cannot vary with what a caller selected.

A preset is the whole setting of the **bundle compilation** that selects it — one entry reference and everything it reaches, the run's own entry and each dispatched target's. It is chosen by the section the entry reference names: the heading text that fragment resolves to, matched against the preset names in the entry document's declaration. A preset covers every document its compilation reaches, so a document reached as a dependency is compiled under the entry's preset rather than its own; its own applies only where some run names a section of it as an entry. A preset nothing selected raises `W_PRESET_UNUSED`.

`default` is the fallback and its name is reserved: a compilation whose section matches no preset name — including one whose entry names a whole document — selects it. Where a document declares none, that compilation substitutes nothing and withholds nothing.

A preset holds three entries. `group-depth` is a list of single-entry mappings, each a group name mapped to its depth, so one document may join several divisions. `exclude` is a list of section names, or of single-entry mappings from a name to a heading level. `mock` is a list of `ORIGINAL=ALTERNATIVE` strings whose sides resolve from the file that declares the preset. Budgets are refused there: a budget bounds a bundle rather than a document, so `--budget` on the command line is the only place one is set.

### Substitution

`mock` is the only channel. [I08:E06](https://github.com/m2ux/prosiform/issues/461) retires `-m`, so a compilation selecting no preset substitutes nothing rather than inheriting a default. The mapping a preset holds is the one its compilation resolves through, and a document reached under two different presets resolves two ways.

### Exclusion

Selection only adds, so a file can withhold part of itself. A preset holds an `exclude` of sections, and each is removed from the contribution of the **file that declares it** — the scope is the declaring file, so no entry names a document. An exclusion is a preset entry, so it governs the compilation that preset was selected for, and no top-level form exists: a list is a preset's shape.

The grammar is a bare section with an optional level: `exclude: ["#Draft"]`, and `#Tests:3` to name the level-3 heading of a repeated name. An exclusion removes what a fragment of the same name would select — the heading, its content and every subsection beneath it — so inclusion and exclusion describe one shape.

Two properties make it a carve-up rather than a trim. A link written inside an excluded section is no dependency, so the document it names is never read, and a document another link also reaches arrives by that surviving link. And an exclusion holding content another reference selected is refused rather than half-applied, because the bundle cannot carry material beneath a heading its author removed.

An exclusion naming a heading the file does not carry is silent, because a preset is shared across documents that vary. An exclusion withholding a file's whole contribution is refused, because a document that withholds everything it holds states a contradiction. A deferral is not carried across: what a later run withholds is that run's business.

## The split

I05's goal was a quality bar, true of every epic forever, so it could be neither reached nor reviewed against. Its 25 epics held three unrelated subjects, and each is now an initiative whose goal its epics can make true: [I08 Argument Surface](https://github.com/m2ux/prosiform/issues/462) holds this record's epics, [I09 Grouping and Composition](https://github.com/m2ux/prosiform/issues/463) holds the grouping work raised alongside it, and [I10 Evaluation and Checks](https://github.com/m2ux/prosiform/issues/464) holds the corpus and session work. I05 is closed.

Every epic in this record was renumbered into I08's series: E11 became E00, E13 E01, E14 E02, E15 E03, E16 E04, E17 E05, the preset-only epic E06, E09 E07 and E22 E08. The work-item files keep their names, so a row's number and its file differ where the epic moved.

## Optimisation

Three changes shorten the critical path, each taken because review attention is the constraint rather than agent capacity.

- **One pin moves for every clause.** Seven epics each amended the design and moved the pin, and conformance reads the design at the pinned revision, so those seven pull requests were a strict chain. E00:W00 now moves the pin once and the other six amendments land beside it: seven level-0 rows instead of a seven-row chain.
- **The example tree is edited once.** E00:W06 declared 95 documents and E09:W00 migrated them to presets, and E09 depends on E00, so the same files were edited twice with each edit proving the bundles unchanged. Both now land in E09:W00, and E00's chain is one row shorter.
- **The boundary no longer waits on absent targets.** E00:W05 depended on W04 for adjacency rather than for code: the boundary is the longest common directory holding a document's own links, which has nothing to do with the absent-target refusal. Both rows now sit at one level.

The joins record accounts for every pair the changes made eligible. What remains on the critical path is Declared Inclusion: W01 through W08, with the corpus families and the documentation pages as consecutive bulk edits at its end.

## Decisions

- **Inclusion is target-side, on the frontmatter declaration.** A local Markdown link is a dependency when its target declares `prosiform`. (User, 2026-10-31.)
- **No path boundary decides a link.** `prosiform.root` retires and a link outside every previous root is compiled when its target declares. (User, 2026-10-31.)
- **A document's boundary is derived from its own links: the deepest directory holding each relative path it names.** (User, 2026-10-31.)
- **A folder pair was a trailing separator on both sides, `-m rules/=stubs/`.** No glob, no second pattern syntax. It retired with `-m`: a preset states one pair per entry, so a folder of stubs is written one entry at a time. (User, 2026-10-31.)
- **A preset is selected by the heading text the entry reference's fragment resolves to, and governs that compilation alone.** (User, 2026-10-31.)
- **Seven epics, delivered in order E11, E13, E14, E15, E16, E17, E26.** The first changes the key rule and the classification both later epics read; the second is the largest and states the preset a carve-up is written as; the third is the carve-up itself. (Agent, 2026-10-31.)
- **Priority is the map the task graph derives: E09 4, E11 3, E13 2, E14 1.** An epic with no prerequisite epic carries the largest number and each other takes one less than the smallest its prerequisites carry, so the board mirrors the edges rather than a reading of effort. The published labels were E11 4, E13 5, E14 5 before this review, which put two dependent epics level with their prerequisite. (User, 2026-10-31.)
- **The folder pairing moved to I08:E07, and retired with its option.** A folder side was a shape of `-m`, which [I08:E06](https://github.com/m2ux/prosiform/issues/461) retires. A preset's `mock` entry inherits the pair syntax, so the folder form goes with the option and a preset states one pair per entry. (User, 2026-10-31.)
- **`root` is refused rather than ignored.** A declaration that silently does nothing reads as declaration that took effect, and this repository carries no backward-compatibility layer. (Agent, 2026-10-31.)
- **A declaration is probed, not captured.** Reading every cited document whole to learn that it declares nothing spends the source budget on material the bundle does not carry. (Agent, 2026-10-31.)
- **An absent document is text, and the operators keep the failure.** The run cannot tell a citation from a typo without the declaration that would answer it, so responsibility is stated by the mark instead. (User, 2026-10-31.) An existing document that declares nothing is text too, which is the cost accepted in exchange for a target that qualifies itself.
- **The boundary refuses no authored link.** Deriving it from the links makes that a property rather than a policy, and the clause says so rather than implying a confinement it no longer performs. (Agent, 2026-10-31.)
- **Every argument value is a list, for every argument.** One shape for a repeatable option and a single-valued one, and a scalar is refused rather than read as a list of one. (User, 2026-10-31.)
- **A whole-document entry matches no preset.** Nothing names a section, so the compilation runs under the run's own options and a preset named for the document's title raises `W_PRESET_UNUSED`. (User, 2026-10-31.)
- **A property the construction holds is held by a check.** Discovery reading one selection and the boundary refusing no authored link are invariants an author cannot break, so each is asserted by a fixture rather than left as prose. (User, 2026-10-31.)
- **An entry reference is held to the same declaration.** The command line is the one selection made outside the link mechanism, so a document that declares nothing cannot be reached by argument either. (Agent, 2026-10-31.)
- **The per-compilation setting is a `preset`.** `profile` already names the grammar `skill-markdown-v4`, reported by `-v` and defined in the glossary; a second sense would make the contract's one defined term name two things. (User, 2026-10-31.)
- **Exclusion is the subtractive half of selection.** A named section is removed rather than filtered from the output, so the run reads fewer sources and the consumer receives only what remains. (User, 2026-10-31.)
- **An exclusion is declared in a preset, and its scope is the file that declares it.** No entry names a document, and there is no command-line form: what a file withholds belongs in that file's own declaration. (User, 2026-10-31.)
- **A document in two divisions is emitted under each.** One division is one outline, so a document joining two is a member of both and its regions appear in each. (User, 2026-10-31.)
- **The example tree and corpus migrate to presets in E13.** E11 removes `root` and leaves the flat group pair, so E13 needs a row that rewrites the tree rather than leaving it uncompilable. (User, 2026-10-31.)
- **A preset covers the closure of the compilation that selects it.** A document reached as a dependency is compiled under the entry's preset, not its own, which is what lets one top-level source set the treatment of everything it links. (User, 2026-10-31.)
- **`-m` is retired: a preset is the only channel.** A compilation selecting no preset substitutes nothing. Two channels for one setting meant a compilation had two possible answers. (User, 2026-10-31.)
- **A preset's pair resolves from the declaring file.** A document states its own neighbours, so one declaration reads the same from any working directory — unlike the option, which had no declaring file and read from the invocation directory. (User, 2026-10-31.)
- **The eight budgets collapse into one `--budget NAME=VALUE`.** Eight siblings of identical shape are one decision rendered eight times, since the parser generates them from one table. Named ceilings also remove the `-o`/`-O` collision, which no arrangement of letters fixes. (User, 2026-10-31.)
- **The fault moves out of the option surface to `PROSIFORM_FAULT`.** A shipped flag whose only consumer is the corpus reads as a feature a caller may use. The corpus already abstracts the fault through a manifest field, so the channel is the runner's business and the option goes. (User, 2026-10-31.)
- **`-f` and the bare-fragment form are removed.** Every use is rewritable as `document#fragment`, the bare form is a usage error for the thing a caller types first, and three fixtures carry it with no consumer. The link form `[x](#section)` is untouched. (User, 2026-10-31.)
- **A fault stays a command-line concern.** `-x` reaches codes no source tree produces, which is a harness need rather than a document's: `internal` means the tool fails in itself and `cleanup-refused` is about the output folder, so neither has a document to attach to. `source-changed` could not be declared in the file it corrupts, because frontmatter is read during capture and the corruption would follow the read that learns of it. A `prosiform` key holding a fault would also put test scaffolding inside the material under test, which the mock feature refused on the same ground. (User, 2026-10-31.)
- **There is no top-level `exclude`.** A list is a preset's shape, so a top-level key holding one is neither an argument nor a preset and is refused. (User, 2026-10-31.)
- **A preset's exclusion is a bare section with an optional level.** The declaring file is the scope, so a qualifier would name what the scope already states. (User, 2026-10-31.)
- **A deferral is not carried across.** An exclusion governs what this run compiles; the later run's exclusions are its own. (User, 2026-10-31.)
- **An unmatched exclusion is silent, including one naming no heading of the declaring file.** A preset is shared across documents that vary, so a miss is ordinary. (User, 2026-10-31.)
- **`W_MOCK_UNUSED` reports per compilation.** A key may be redundant for one compilation and live for another, so the warning names the key and the compilation it did not serve. (User, 2026-10-31.)
- **The number after a section names its heading level, and never changes how much is cut.** It exists to tell two headings of one name apart, which a fragment already refuses as ambiguous. A level is optional: `#Section` is the document-level heading. (User, 2026-10-31.)
- **An excluded section's links are not followed.** The closure shrinks, so an exclusion is structural rather than cosmetic. (User, 2026-10-31.)
- **An unmatched exclusion is silent.** A shared preset names sections a given document lacks, and a filter matching nothing is unremarkable. (User, 2026-10-31.)
- **An exclusion holding selected content is refused, not resolved.** The two readings — re-parent the content or drop it — are both silent about which the author meant, and either ships a bundle a consumer should not receive. (User, 2026-10-31.)
- **Long form only: `--exclude`.** `-x` is the fault-injection option and `-e` the expansion-depth budget, so the letters a caller reaches for are taken. (User, 2026-10-31.)
- **The initiative's `Depends on` cells are empty.** The rule derives a whole-epic edge only where every row of the dependent requires every row of the prerequisite, and no row pair here meets it. The gates live in the task edges and in the priority numbers. (User, 2026-10-31.)

## Review

Findings from the plan review against the source, all resolved.

| Finding | Severity | Resolution |
| --- | --- | --- |
| Both initiative `Depends on` cells named whole epics that no row pair derives, and `scripts/deps.py` refused them. | High | Both cells emptied; the couplings are task edges. |
| Seven independent pairs were named in neither Joins nor the record, so the checker reported every one. | High | Each pair accounted for in `joins.md` with its two ids on one line, and the reason it takes two pull requests stated. |
| The folder-mock epic consumed `E09`'s `-m` grammar and `E11`'s classification seam and named neither. | High | Retired: the work moved to `E09:W09`, which names `E11:W03`. |
| The three W00 rows contended on `design.md` under one priority number, with the sequencing stated only as prose. | Medium | Each W00 depends on the previous epic's W00, which is what the pin chain actually is. |
| The diagram-following eval's 118 workflow documents declare nothing, and `make harness` requires each form to bundle cleanly. | Critical | `E11:W06` covers the eval tree and states which forms it reaches. |
| Four `real-source` fixtures copy documents whose frontmatter declares nothing, and the family's rule forbids editing a copy. | High | `E11:W07` states where the declaration is added for a copied source. |
| Nothing stated whether an entry reference could name a document that declares nothing. | High | AC15 added, with a fixture, and `E11:W05` carries it. |
| `checks/smoke.py` writes `prosiform: {root: "."}`, so `make smoke` fails as soon as the refusal lands. | High | `E11:W06` owns the check's source and its retired-option assertion. |
| `profile` already names the grammar, and the epic reused it. | High | The concept is a `preset` throughout; the word clash is stated in the clause and the glossary check holds it. |
| `E11:W08` named six pages where eleven state a root. | Medium | AC13 lists all eleven, and AC14 covers the four worked examples and the drawings. |
| AC9 cited `make boundary` and the folder epic's AC6 cited `make mock-scenarios`; neither target existed. | Medium | `E11:W05` creates `make boundary`; `E09:W11` extends the target `E09:W08` lands and states that dependency. |
| The board held E13 and E14 at priority 5, level with the E09 epic that neither depends on and above the E11 epic both depend on; the graph derives E09 4, E11 3, E13 2, E14 1. | High | The derived map applied to the labels and recorded as a decision. |
| The folder rows read under the inclusion rule, which a reader could take for a dependency on `E11`. | Low | `E09:W09` states that the rule is E11's and that its stubs declare from the first, so the mechanism is buildable before E11 lands and no edge is asserted. The checker refuses a row depending on a later epic, and the row does not. |
| The record's `epic.md` still described ten rows and an unnumbered documented row, so the record and the tracker disagreed. | Medium | Regenerated from the published body. |
| The argument-name set was read from the parser, which makes `-o` and `-c` settable from frontmatter. | High | The settable set is named: `mock`, `exclude` and the budgets, held to the help output by a test. |
| An argument's value had two shapes, a scalar for `-m` and a list for `--exclude`. | Medium | Every argument value is a list, and a scalar is refused. |
| W02's body invented a title-matching rule for a whole-document entry that no criterion stated. | High | A whole-document entry matches no preset, which AC14 states and a fixture holds. |
| Two invariants stated in W04 and W05 were prose with no test behind them. | Medium | Each has a criterion now, and W09 carries the fixture and the boundary assertion. |

## Debt this record defers

- **Epic A supersedes two acceptance criteria of [I08:E07](https://github.com/m2ux/prosiform/issues/414).** AC11 and AC20 of that epic make a substitute reachable from a source whose root excludes it; with no root there is no exemption to state. The criteria are reworded in that epic rather than carried here, and the fixture `a-substitute-outside-the-writing-root-is-reachable` is renamed to the boundary it now exercises.
- **`checks/authoring.py` holds a rule about link spelling written in terms of `root`.** Its `DECLARED_ROOT` pattern and `link_form` test exist because a root prefixed a link's spelling. The 2026-10-24 note already found the spy role gone; A retires the declaration the check reads, so the check is rewritten to the derived boundary rather than deleted outright, because it still catches a link written from the wrong directory.

## Open Questions

None outstanding. Every reading this record raised has been answered: the boundary is derived from the file's own links, a preset matches a resolved heading text and covers its compilation's closure, `-m` is retired so a preset is the only channel, and the fault leaves the option surface.

## Links

| Resource | Link |
| --- | --- |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Preceding epic | [I08:E07 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Epic A | [I08:E00 Declared Inclusion](https://github.com/m2ux/prosiform/issues/434) |
| Epic B | [I08:E01 Target Presets](https://github.com/m2ux/prosiform/issues/436) |
| Epic D | [I08:E02 Exclusion](https://github.com/m2ux/prosiform/issues/445) |
| Epic E | [I08:E03 Remove the Referrer](https://github.com/m2ux/prosiform/issues/449) |
| Epic F | [I08:E04 Conformance Faults](https://github.com/m2ux/prosiform/issues/450) |
| Epic G | [I08:E05 Named Budgets](https://github.com/m2ux/prosiform/issues/451) |
| Epic H | [I08:E06 Preset-Only Substitution](https://github.com/m2ux/prosiform/issues/461) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
