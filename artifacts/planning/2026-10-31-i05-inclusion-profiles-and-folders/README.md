# Declared Inclusion, Target Profiles and Folder Mocks — October 2026

> Epic set · Created 2026-10-31

## Executive Summary

Three changes to what a run carries and how an argument reaches it. The first retires `prosiform.root`: a local Markdown link is bundled when the document it names declares `prosiform`, and a document's boundary is derived from the links it writes rather than declared. The second admits named *profiles* in frontmatter, so a section an argument names is compiled under that argument. The third lets `-m` name a folder pair, so a whole directory is mocked without an entry per file.

They are one record because two of them are ordered by the first. Today `prosiform` admits exactly three keys and refuses any other; a profile is a key that is neither. And today a substitution is exempt from the writing source's root because the root is a boundary; once a boundary is derived from links, what bounds a substitute has to be stated against that instead. Delivering the profiles first would mean writing the key rule twice.

The set is three epics. **Declared Inclusion** is the load-bearing one: it moves link classification from where a file sits to whether the file opts in, which changes the answer for every document in the example tree, every root-declaring fixture and five pages of documentation. **Folder Mocks** is small and lands second, because a folder of stubs is what the profile work is exercised against. **Target Profiles** lands last, once the declaration it reads and the folder it mocks both exist.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Declared Inclusion](epic-a-declared-inclusion.md) | [E11](https://github.com/m2ux/prosiform/issues/434): the epic retiring `root`, with the declaration, the probe, classification and the derived boundary |
| [Target Profiles](epic-b-target-profiles.md) | [E13](https://github.com/m2ux/prosiform/issues/436): the epic admitting named profiles and applying one to a compilation |
| [Folder Mocks](epic-c-folder-mocks.md) | [E12](https://github.com/m2ux/prosiform/issues/435): the epic letting `-m` name a folder pair |
| [A: design clause](a-w00.md) | The clause, the retired codes and the pin |
| [A: metadata](a-w01.md) | Declaration presence, the empty block and the `root` refusal |
| [A: probe](a-w02.md) | Reading a declaration without capturing a source |
| [A: classification](a-w03.md) | The seam that answers whether a link is a dependency |
| [A: absent targets](a-w04.md) | Text for a link naming nothing, a refusal for one an operator marks |
| [A: derived boundary](a-w05.md) | The boundary a document's own links state |
| [A: example tree](a-w06.md) | Declaring 95 documents and withdrawing their roots |
| [A: corpus](a-w07.md) | Every fixture family declaring rather than rooting |
| [A: documentation](a-w08.md) | Five pages that state the declaration |
| [B: design clause](b-w00.md) | The clause and the pin |
| [B: profile keys](b-w01.md) | The key rule `prosiform` admits |
| [B: selection](b-w02.md) | Matching a section name to a profile |
| [B: spec binding](b-w03.md) | A profile's mock entries and their collisions |
| [B: unused profiles](b-w04.md) | The warning for a profile nothing applied |
| [B: deferred targets](b-w05.md) | A profile kept for the run that follows the deferral |
| [B: documentation](b-w06.md) | The profile stated in the invocation and the source page |
| [C: design clause](c-w00.md) | The clause and the pin |
| [C: grammar](c-w01.md) | The folder pair and its refusals |
| [C: matching](c-w02.md) | Prefix matching, precedence and the retained section |
| [C: unmatched](c-w03.md) | The warning for a folder key that matched nothing |
| [C: example](c-w04.md) | A whole folder mocked in the example skill |
| [C: documentation](c-w05.md) | The option row |
| [Joins and ordering](joins.md) | The rows that share a pull request, and why the epics are ordered A, C, B |

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

## Decisions

- **Inclusion is target-side, on the frontmatter declaration.** A local Markdown link is a dependency when its target declares `prosiform`. (User, 2026-10-31.)
- **No path boundary decides a link.** `prosiform.root` retires and a link outside every previous root is compiled when its target declares. (User, 2026-10-31.)
- **A document's boundary is derived from its own links: the deepest directory holding each relative path it names.** (User, 2026-10-31.)
- **A folder pair is a trailing separator on both sides, `-m rules/=stubs/`.** No glob, no second pattern syntax. (User, 2026-10-31.)
- **A profile is selected by the heading text the entry reference's fragment resolves to, and governs that compilation alone.** (User, 2026-10-31.)
- **Three epics, delivered in order A, C, B.** A changes the key rule and the classification both later epics read; C is small and supplies the stub folders B is demonstrated against; B is the largest and depends on both. (Agent, 2026-10-31.)
- **`root` is refused rather than ignored.** A declaration that silently does nothing reads as declaration that took effect, and this repository carries no backward-compatibility layer. (Agent, 2026-10-31.)
- **A declaration is probed, not captured.** Reading every cited document whole to learn that it declares nothing spends the source budget on material the bundle does not carry. (Agent, 2026-10-31.)
- **An absent document is text, and the operators keep the failure.** The run cannot tell a citation from a typo without the declaration that would answer it, so responsibility is stated by the mark instead. (Agent, 2026-10-31.)
- **The boundary refuses no authored link.** Deriving it from the links makes that a property rather than a policy, and the clause says so rather than implying a confinement it no longer performs. (Agent, 2026-10-31.)
- **Priority 4 for A, 4 for C, 5 for B.** A touches every tree in the repository, so nothing else should be in flight over the same files; B has no contention and can start once A lands. (Agent, 2026-10-31.)

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
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
