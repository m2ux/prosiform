## Overview

`-m` accepts a **folder pair**, one trailing separator on each side, so a whole directory is mocked by one entry. A key folder matches every reference under it, the substitute folder takes the same remainder, and the section the reference names is kept.

## Problem

A folder of stand-ins costs one entry per file.

- **The mapping is one pair at a time.**
  [I05:E09](https://github.com/m2ux/prosiform/issues/414) landed `-m ORIGINAL=ALTERNATIVE` with `closure.Substitution` holding `(path, fragment)` keys, exact-first. A run exercising a mode against a folder of stubs names each stub, and a stub added to the folder is invisible to the run until somebody edits the command line.
- **A fixture tree is a folder.**
  The case the parameter exists for — exercising a skill against material that must not ship — is a directory of alternate documents, so the unit a caller draws the line around is the directory rather than the file.
- **The command line stops being reviewable.**
  Twelve pairs for one folder is a command line a reader cannot check against the folder it names, and a pair missing from it fails as a bundle that quietly carries one real document.

## Proposal

- **A trailing separator makes a side a folder.**
  `-m rules/=stubs/` redirects each reference whose normalised path sits under `rules/` to the path with the same remainder under `stubs/`. Both sides carry the separator or neither does; one of each is invalid usage, because a folder and a file state different questions and one entry cannot ask both.
- **The remainder is the identity.**
  A reference to `rules/visual/red.md` matches the key folder and redirects to `stubs/visual/red.md`. The reference keeps its section, so `rules/red.md#checks` redirects to `stubs/red.md#checks`, exactly as a document key leaves a section the reference named.
- **Exact answers first, then the longest folder.**
  A key naming the whole document answers before any folder key, and a section key before either. Two folder keys that both hold a reference are ordered by the length of the key, so `rules/visual/` beats `rules/` and the more specific folder is the author's statement.
- **A substitute the folder does not hold is a refusal.**
  A folder key that matches a reference with no file at the corresponding path fails with `E_TARGET_NOT_FOUND` naming the reference, the key and the path it resolved to. The mapping stated that the run reads a document there, so its absence is the command line being wrong rather than the tree.
- **A folder key that matched nothing warns.**
  `W_MOCK_UNUSED` already names a key no reference touched, and a folder key is a key. It accompanies a published bundle and exit status `0`, as an unmatched document key does.
- **Nothing else about the mapping changes.**
  A folder side resolves from the invocation working directory through the reference grammar the other sides use, with parent bootstrap permitted and the Markdown-suffix test applied to the path each reference resolves to rather than to the key.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause and pin | AC8 | [E11:W00](https://github.com/m2ux/prosiform/issues/434) | | |
| W01 | The folder grammar and its refusals | AC3 | W00 | | |
| W02 | Prefix matching, precedence and retained section | AC1, AC2 | W01, [E11:W03](https://github.com/m2ux/prosiform/issues/434) | | |
| W03 | Absent substitute and unmatched folder | AC4, AC5 | W02 | | |
| W04 | A whole folder mocked in the example | AC6 | W03 | | |
| W05 | The option row states the folder form | AC7 | W03 | | |

## Acceptance Criteria

- [ ] **AC1.** A reference under a key folder compiles the document at the same remainder under the substitute folder and keeps the section it named, as the corpus fixture `fixtures/mock/a-folder-key-redirects-each-reference-under-it` shows.
- [ ] **AC2.** An exact key answers before a folder key, and of two folder keys holding one reference the longer is used, as the corpus fixture `fixtures/mock/an-exact-key-beats-a-folder-key` shows.
- [ ] **AC3.** A pairing with a separator on one side and not the other is invalid usage with exit status `2`, as the corpus fixture `fixtures/mock/a-half-folder-pair-is-refused` shows.
- [ ] **AC4.** A folder key matching a reference whose substitute path holds no document fails with `E_TARGET_NOT_FOUND`, naming the reference and the path, as the corpus fixture `fixtures/mock/a-folder-substitute-that-is-absent-fails` shows.
- [ ] **AC5.** A folder key no reference touched raises `W_MOCK_UNUSED` and the run publishes with exit status `0`, as the corpus fixture `fixtures/mock/an-unused-folder-key-warns` shows.
- [ ] **AC6.** One folder pair compiles the example skill's plan mode against a folder of stubs with no entry per file, as `make mock-scenarios` shows.
- [ ] **AC7.** The option's documented row states the folder form and agrees with the command's help output, as `make invocation` shows.
- [ ] **AC8.** The design states the folder pairing, its precedence and its two outcomes, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.

## References

- **R0.** Epic - [I05:E12 Folder Mocks](https://github.com/m2ux/prosiform/issues/435).


- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions and the work items.
- **R2.** [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) — the epic that landed the mapping this one extends.
