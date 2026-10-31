# Declared Inclusion, Target Profiles and Folder Mocks — October 2026

> Epic set · Created 2026-10-31

## Executive Summary

Three changes to what a run carries and how an argument reaches it. The first retires `prosiform.root`: a local Markdown link is bundled when the document it names declares `prosiform`, and a document's boundary is derived from the links it writes rather than declared. The second admits named *presets* in frontmatter, so a section an argument names is compiled under that argument. The third lets `-m` name a folder pair, so a whole directory is mocked without an entry per file.

They are one record because two of them are ordered by the first. Today `prosiform` admits exactly three keys and refuses any other; a preset is a key that is neither. And today a substitution is exempt from the writing source's root because the root is a boundary; once a boundary is derived from links, what bounds a substitute has to be stated against that instead. Delivering presets first would mean writing the key rule twice.

The set is three epics. **Declared Inclusion** is the load-bearing one: it moves link classification from where a file sits to whether the file opts in, which changes the answer for every document in the example tree, every root-declaring fixture and eleven pages of documentation. **Folder Mocks** is small and lands second, because a folder of stubs is what the preset work is exercised against. **Target Profiles** lands last, once the declaration it reads and the folder it mocks both exist.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Declared Inclusion](epic-a-declared-inclusion.md) | [E11](https://github.com/m2ux/prosiform/issues/434): the epic retiring `root`, with the declaration, the probe, classification and the derived boundary |
| [Target Profiles](epic-b-target-profiles.md) | [E13](https://github.com/m2ux/prosiform/issues/436): the epic admitting named presets and applying one to a compilation |
| [Folder Mocks](epic-c-folder-mocks.md) | [E12](https://github.com/m2ux/prosiform/issues/435): the epic letting `-m` name a folder pair |
| [Exclusion](epic-d-exclusion.md) | [E14](https://github.com/m2ux/prosiform/issues/445): the epic removing a named section from a bundle |
| [A: design clause](a-w00.md) | The clause, the retired codes and the pin |
| [A: metadata](a-w01.md) | Declaration presence, the empty block and the `root` refusal |
| [A: probe](a-w02.md) | Reading a declaration without capturing a source |
| [A: classification](a-w03.md) | The seam that answers whether a link is a dependency |
| [A: absent targets](a-w04.md) | Text for a link naming nothing, a refusal for one an operator marks |
| [A: derived boundary](a-w05.md) | The boundary a document's own links state |
| [A: example tree](a-w06.md) | Declaring 95 documents and withdrawing their roots |
| [A: corpus](a-w07.md) | Every fixture family declaring rather than rooting |
| [A: documentation](a-w08.md) | Five pages that state the declaration |
| [B: design clause](b-w00.md) | The clause, the term and the pin |
| [B: preset keys](b-w01.md) | The key rule `prosiform` admits |
| [B: selection](b-w02.md) | Matching a section name to a preset |
| [B: spec binding](b-w03.md) | A preset's mock entries and their collisions |
| [B: unused presets](b-w04.md) | The warning for a preset nothing applied |
| [B: deferred targets](b-w05.md) | A preset kept for the run that follows the deferral |
| [B: documentation](b-w06.md) | The preset stated in the invocation and the source page |
| [C: design clause](c-w00.md) | The clause and the pin |
| [C: grammar](c-w01.md) | The folder pair and its refusals |
| [C: matching](c-w02.md) | Prefix matching, precedence and the retained section |
| [C: unmatched](c-w03.md) | The warning for a folder key that matched nothing |
| [C: example](c-w04.md) | A whole folder mocked in the example skill |
| [C: documentation](c-w05.md) | The option row |
| [D: design clause](d-w00.md) | The clause, the two codes and the pin |
| [D: grammar](d-w01.md) | The option, its level suffix and its refusals |
| [D: seam](d-w02.md) | Exclusion where the selection settles, and the silent miss |
| [D: scope](d-w03.md) | Bare and document-qualified scope |
| [D: closure](d-w04.md) | An excluded section's links are no dependency |
| [D: conflict](d-w05.md) | Included content beneath an exclusion is refused |
| [D: empty entry](d-w06.md) | A selection excluding everything is refused |
| [D: level](d-w07.md) | A level telling a repeated heading apart |
| [D: preset](d-w08.md) | A document and a preset carrying an exclusion |
| [D: documentation](d-w09.md) | The option row and the selection page |
| [Joins and ordering](joins.md) | The rows that share a pull request, and why the epics are ordered E11, E12, E13, E14 |

## Design

### Inclusion

A link is followed when its target declares `prosiform`. Nothing about where either file sits decides it. The declaration is read from the target's leading frontmatter, so the question is answered by opening the target — which the pipeline does with a **probe** that reads the frontmatter span alone, bounded by the existing byte budget, before deciding whether to capture the document whole.

### Boundary

A document's **derived boundary** is the deepest directory that holds every local Markdown path its own links name, normalised from the document's directory; a document linking no such path has its own directory. The boundary states what the declaration used to state: the deepest place the author already reached.

It is worth being exact about what the boundary now refuses, because `root` refused a great deal. It refuses **no authored link**, by construction — every link a document writes resolves inside it. It confines a positional entry reference, and it is the value a diagnostic names when a path leaves it. Anything else `root` used to bound — a substitute named on the command line, a path a profile names — is command-line or frontmatter material rather than authored text, and the clause states each one's confinement in its own right.

### Classification

`closure.resolvable`, `bundled` and `withholding_target` answer from the target's captured declaration rather than from a `covers` test against a root. `OutsideRoot` survives only for the forms no path grammar admits: a drive path, an absolute path, a path normalising above the invocation working directory. `E_SOURCE_OUTSIDE_ROOT` survives with those cases; `E_ROOT_NOT_FOUND` retires.

### Absent targets

A link naming a document that exists and does not declare is text, and a link naming a document that does not exist is text too, because in neither case does anything state that the bundle is responsible for it. The statement of responsibility moves to the operators: a link whose text opens with an operator, and a fragment-only link, name a compilation or a section of the document itself, and each still fails with `E_TARGET_NOT_FOUND` when nothing is there.

This is the one behaviour the change makes weaker, and it is stated rather than softened: a misspelled link under a directory a previous `root` covered used to fail the run, and now reaches the bundle as authored.

### Profiles

`prosiform` admits, beside its fields, a key that is an argument name or a profile name. A key named for an argument applies that argument to every compilation of the file; any other key whose value is a mapping is a profile; an unknown key whose value is not a mapping is refused, because that is a misspelled field.

A profile applies to a **bundle compilation**, which is one entry reference and everything it reaches: the run's own entry, and each dispatched target's. The profile is chosen by the section the entry reference names — the heading text that fragment resolves to, matched against the names in the entry document's declaration. A profile on a document merged into another bundle applies to nothing, and the run says so with `W_PROFILE_UNUSED`.

### The folder pair

A mapping side ending in a separator makes the entry a folder pairing, and both sides must agree. A key folder matches every reference whose normalised path sits under it, the substitute folder takes the same remainder, and the reference keeps its section. Exact keys answer first, then the longest matching folder key.

### Exclusion

Selection only adds, so `--exclude SECTION` is its subtractive half. A bare `#Section` removes that section in every document the run reads; a qualified `document.md#Section` removes it in that document alone; a trailing `:N` names which heading of a repeated name is meant. An exclusion removes what a fragment of the same name would select — the heading, its content and every subsection beneath it — so inclusion and exclusion describe one shape.

Two properties make it a carve-up rather than a trim. A link written inside an excluded section is no dependency, so the document it names is never read, and a document another link also reaches arrives by that surviving link. And an exclusion holding content another reference selected is refused rather than half-applied, because the bundle cannot carry material beneath a heading its author removed.

An exclusion touching nothing is silent, because a shared preset legitimately names sections some document lacks. An exclusion emptying its own entry is refused, because a bundle carrying no document is not a bundle.

## Decisions

- **Inclusion is target-side, on the frontmatter declaration.** A local Markdown link is a dependency when its target declares `prosiform`. (User, 2026-10-31.)
- **No path boundary decides a link.** `prosiform.root` retires and a link outside every previous root is compiled when its target declares. (User, 2026-10-31.)
- **A document's boundary is derived from its own links: the deepest directory holding each relative path it names.** (User, 2026-10-31.)
- **A folder pair is a trailing separator on both sides, `-m rules/=stubs/`.** No glob, no second pattern syntax. (User, 2026-10-31.)
- **A preset is selected by the heading text the entry reference's fragment resolves to, and governs that compilation alone.** (User, 2026-10-31.)
- **Three epics, delivered in order E11, E12, E13.** The first changes the key rule and the classification both later epics read; the second is small and supplies the stub folders the third is demonstrated against; the third is the largest and depends on both. (Agent, 2026-10-31.)
- **`root` is refused rather than ignored.** A declaration that silently does nothing reads as declaration that took effect, and this repository carries no backward-compatibility layer. (Agent, 2026-10-31.)
- **A declaration is probed, not captured.** Reading every cited document whole to learn that it declares nothing spends the source budget on material the bundle does not carry. (Agent, 2026-10-31.)
- **An absent document is text, and the operators keep the failure.** The run cannot tell a citation from a typo without the declaration that would answer it, so responsibility is stated by the mark instead. (User, 2026-10-31.) An existing document that declares nothing is text too, which is the cost accepted in exchange for a target that qualifies itself.
- **The boundary refuses no authored link.** Deriving it from the links makes that a property rather than a policy, and the clause says so rather than implying a confinement it no longer performs. (Agent, 2026-10-31.)
- **An entry reference is held to the same declaration.** The command line is the one selection made outside the link mechanism, so a document that declares nothing cannot be reached by argument either. (Agent, 2026-10-31.)
- **The per-compilation argument set is a `preset`.** `profile` already names the grammar `skill-markdown-v4`, reported by `-v` and defined in the glossary; a second sense would make the contract's one defined term name two things. (User, 2026-10-31.)
- **Exclusion is the subtractive half of selection.** A named section is removed rather than filtered from the output, so the run reads fewer sources and the consumer receives only what remains. (User, 2026-10-31.)
- **A bare exclusion applies wherever the name appears, a qualified one to its document.** One preset carving several documents needs the bare form; the qualified form scopes a removal that would otherwise reach too far. (User, 2026-10-31.)
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
| Both initiative `Depends on` cells named whole epics that no row pair derives, and `scripts/deps.py` refused them. | High | Both cells emptied; the couplings are task edges, and `E12` gained the two it was missing. |
| Seven independent pairs were named in neither Joins nor the record, so the checker reported every one. | High | Each pair accounted for in `joins.md` with its two ids on one line, and the reason it takes two pull requests stated. |
| `E12` consumed `E09`'s `-m` grammar and `E11`'s classification seam and named neither, so it could have started first. | High | `E12:W02` gained a dependency on `E11:W03`; `E12:W01`'s relation to `E09` is stated in the body, since `E09` is not an epic the checker is given. |
| The three W00 rows contended on `design.md` under one priority number, with the sequencing stated only as prose. | Medium | Each W00 depends on the previous epic's W00, which is what the pin chain actually is. |
| The diagram-following eval's 118 workflow documents declare nothing, and `make harness` requires each form to bundle cleanly. | Critical | `E11:W06` covers the eval tree and states which forms it reaches. |
| Four `real-source` fixtures copy documents whose frontmatter declares nothing, and the family's rule forbids editing a copy. | High | `E11:W07` states where the declaration is added for a copied source. |
| Nothing stated whether an entry reference could name a document that declares nothing. | High | AC15 added, with a fixture, and `E11:W05` carries it. |
| `checks/smoke.py` writes `prosiform: {root: "."}`, so `make smoke` fails as soon as the refusal lands. | High | `E11:W06` owns the check's source and its retired-option assertion. |
| `profile` already names the grammar, and the epic reused it. | High | The concept is a `preset` throughout; the word clash is stated in the clause and the glossary check holds it. |
| `E11:W08` named six pages where eleven state a root. | Medium | AC13 lists all eleven, and AC14 covers the four worked examples and the drawings. |
| AC9 cited `make boundary` and AC6 cited `make mock-scenarios`; neither target existed. | Medium | `E11:W05` creates `make boundary`; `E12:W04` extends the target `E09:W08` lands and states that dependency. |

## Debt this record defers

- **Epic A supersedes two acceptance criteria of [I05:E09](https://github.com/m2ux/prosiform/issues/414).** AC11 and AC20 of that epic make a substitute reachable from a source whose root excludes it; with no root there is no exemption to state. The criteria are reworded in that epic rather than carried here, and the fixture `a-substitute-outside-the-writing-root-is-reachable` is renamed to the boundary it now exercises.
- **`checks/authoring.py` holds a rule about link spelling written in terms of `root`.** Its `DECLARED_ROOT` pattern and `link_form` test exist because a root prefixed a link's spelling. The 2026-10-24 note already found the spy role gone; A retires the declaration the check reads, so the check is rewritten to the derived boundary rather than deleted outright, because it still catches a link written from the wrong directory.

## Open Questions

None outstanding. Two readings were put to the user and answered: the boundary is derived from the file's own links, and a profile matches a resolved heading text and governs one compilation.

## Links

| Resource | Link |
| --- | --- |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Preceding epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Epic A | [I05:E11 Declared Inclusion](https://github.com/m2ux/prosiform/issues/434) |
| Epic C | [I05:E12 Folder Mocks](https://github.com/m2ux/prosiform/issues/435) |
| Epic B | [I05:E13 Target Profiles](https://github.com/m2ux/prosiform/issues/436) |
| Epic D | [I05:E14 Exclusion](https://github.com/m2ux/prosiform/issues/445) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
