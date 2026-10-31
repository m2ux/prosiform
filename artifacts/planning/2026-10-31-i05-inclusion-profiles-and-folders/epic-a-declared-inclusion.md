## Overview

A local Markdown link is compiled when the document it names declares `prosiform`, and nothing about where either file sits decides it. The declaration `prosiform.root` retires, and a document's boundary is derived from the relative paths its own links name rather than authored ahead of them.

## Problem

Inclusion is decided by directory, and the directory is authored twice.

- **The root is a second statement of what the links already say.**
  `prosiform.root` is declared in 95 example documents and bounds every link its author writes. `closure.covers` compares the resolved path against it, and `cli.read_document` walks it, binds its directory identity and re-checks that identity before publication. An author who writes `[Rules](../rules.md)` and declares `root: ".."` has stated the same reachable set twice, and the two can disagree.
- **A file's inclusion is not a property of the file.**
  Whether `rules/common.md` travels in a bundle depends on the declaration of whichever procedure happened to link it. The same document reached from two sources is two answers, and neither is written on the document.
- **The boundary refuses material the bundle is responsible for.**
  A link above the root is a citation rather than a dependency, so a tree kept beside the skill — the fixture tree a mock exercises, the stand-in an author is drafting — is unreachable by the document being tested. [I05:E09](https://github.com/m2ux/prosiform/issues/414) exists only to exempt substitutes from that boundary.
- **Link spelling is already known to be unsound.**
  The [2026-10-24 note](../2026-10-24-root-declaration-roles/README.md) records that a root prefixes a link's spelling, that `[Codex](codex.md)` fails where `[Codex](rules/codex.md)` resolves, and that two commits to the example tree were wrong in exactly that way without any check reporting it.

## Proposal

- **The declaration is the qualification.**
  A link naming a local Markdown document is a dependency when, and only when, the target's leading frontmatter declares `prosiform`. The question is asked of the target rather than of the writing source, so one document is included by every run that reaches it, and a document reached by two sources is one answer.
- **The answer costs a frontmatter read, not a source capture.**
  A caller's link is answered by a **probe**: the target is opened by the same rooted no-follow walk, its frontmatter span is delimited and decoded within the existing byte budget, and the read stops there. A document that declares is then captured whole and becomes a source; one that declares nothing is never read again, is not counted as a source and carries no content, group or destination.
- **Presence is a fact of its own.**
  An empty `prosiform` block declares, and a document carrying no block does not. `metadata.decode` today returns one absent value for both, so the distinction is added there rather than inferred at the call site.
- **`root` is refused, not ignored.**
  A `prosiform` mapping carrying `root` fails the run with `E_INVALID_CONVERSION_METADATA`, naming the field and the remedy. A declaration that silently does nothing is read as a declaration that took effect.
- **The boundary is derived from the links the document writes.**
  A document's boundary is the deepest directory holding every local Markdown path its own links name, normalised from the document's directory; a document linking none has its own directory. The property that follows is the point of the derivation: the boundary refuses no authored link, so a run compiles each link its author wrote and each document that declares.
- **What the boundary still confines.**
  A positional entry reference, and the path a diagnostic names when one leaves it. A substitute named on the command line and a path a profile names are command-line or frontmatter material rather than authored text, and each states its own confinement. `OutsideRoot` survives for the forms no path grammar admits — a drive path, an absolute path, a path normalising above the invocation working directory — and `E_SOURCE_OUTSIDE_ROOT` survives with them. `E_ROOT_NOT_FOUND` retires.
- **Responsibility is stated by the mark.**
  A link naming a document that declares nothing is text; so is one naming a document that does not exist, because nothing states the bundle is answerable for it. A link whose text opens with an operator, and a fragment-only link, name a compilation or a section of the document itself, and each still fails with `E_TARGET_NOT_FOUND` when nothing is there.
- **Every tree states its declaration.**
  The 95 example documents declare `prosiform`, every fixture family that declares a root declares instead, and the documentation states inclusion as a property of the target. Bytes other than the metadata are unchanged, so the bundles the example published before this epic are the bundles it publishes after it.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause, retired codes and pin | AC10 | | | |
| W01 | Declaration presence and the `root` refusal | AC4, AC5 | W00 | | |
| W02 | A declaration probed without a capture | AC6 | W01 | | |
| W03 | Classification that asks the target | AC1, AC3 | W02 | | |
| W04 | Absent targets and the operators that hold | AC7, AC8 | W03 | | |
| W05 | The boundary a document's links state | AC2, AC9 | W03 | | |
| W06 | The example tree declares, rootless | AC11 | W05 | | |
| W07 | Every corpus family declares | AC12 | W06 | | |
| W08 | The pages that state the declaration | AC13 | W07 | | |

## Acceptance Criteria

- [ ] **AC1.** A link whose target declares `prosiform` is compiled into the bundle and its destination rewritten, as the corpus fixture `fixtures/inclusion/a-declaring-target-is-compiled` shows.
- [ ] **AC2.** A link naming a declaring document above the writing document's directory is compiled, where the same tree under a declared root would have carried it as a citation, as the corpus fixture `fixtures/inclusion/a-target-above-the-writing-directory-is-compiled` shows.
- [ ] **AC3.** A link whose target declares nothing is emitted as authored, its target contributes no content and no group, and it is counted against no source budget, as the corpus fixture `fixtures/inclusion/a-silent-target-is-text` shows.
- [ ] **AC4.** A `prosiform` mapping carrying `root` fails with `E_INVALID_CONVERSION_METADATA` and exit status `1`, as the corpus fixture `fixtures/inclusion/a-declared-root-is-refused` shows.
- [ ] **AC5.** An empty `prosiform` block qualifies its document, and a document with no block does not, as the corpus fixture `fixtures/inclusion/an-empty-block-declares` shows.
- [ ] **AC6.** A cited target larger than `-B` that declares nothing is text and the run publishes, where the same target declaring fails, as the corpus fixture `fixtures/inclusion/an-oversized-silent-target-is-text` shows.
- [ ] **AC7.** A link naming no document and carrying no operator is emitted as authored and the run publishes, as the corpus fixture `fixtures/inclusion/a-link-naming-no-document-is-text` shows.
- [ ] **AC8.** A link naming no document whose text opens with an operator fails with `E_TARGET_NOT_FOUND`, and a fragment-only link naming a heading its document does not carry fails with the same code, as the corpus fixtures `fixtures/inclusion/operators-keep-the-absent-target-refusal` and `fixtures/inclusion/a-fragment-naming-no-heading` show.
- [ ] **AC9.** A document's derived boundary is the deepest directory holding every local Markdown path its own links name, as `make boundary` reports over the example tree.
- [ ] **AC10.** The design states inclusion as a property of the target document, states the derived boundary and the refusal of `root`, names the retired code, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.
- [ ] **AC11.** Every document in [the example tree](https://github.com/m2ux/prosiform/blob/main/example/work-planner/SKILL.md) declares `prosiform` and none declares a root, as `make authoring` shows.
- [ ] **AC12.** Every corpus family that declared a root declares its targets instead, and the corpus passes with the same expected bundles, as `make corpus` shows.
- [ ] **AC13.** No page states a root as a property of a source: the source page, the reference page, the architecture page, the hierarchy page, the glossary and the invocation describe inclusion by declaration, as an inspection of those pages shows.

## References

- **R0.** Epic - [I05:E11 Declared Inclusion](https://github.com/m2ux/prosiform/issues/434).


- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions, the work items and the debt this epic takes on.
- **R2.** [The `root` declaration: three roles, one of them questionable](../2026-10-24-root-declaration-roles/README.md) — the note that found the spelling role unsound, and the change it declined to make.
- **R3.** [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) — the epic whose root exemption this one removes the need for.
