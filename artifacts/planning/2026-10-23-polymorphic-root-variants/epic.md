## Overview

One physical file can be reached under more than one effective root. The file is captured once. Each distinct root renders it once, and that rendering resolves the file's own links under that root. An omitted root selects the root of the parent that reached the file. An entry, which has no parent, uses the invocation working directory.

## Problem

Nested files that belong with a parent write a directory climb in `prosiform.root`. The delivered contract treats an omitted root as the invocation working directory for every file, so a climb is how a nested file names its parent's root.

- The delivered rule is stated in the [file-owned invocation decisions](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/design.md): every absent root uses the invocation working directory, including linked sources.
- A file reached from two parents is opened once, keyed by its filesystem path, so the second parent's root is dropped. One file therefore cannot answer under two roots.

## Proposal

- **An omitted root follows the parent that reached the file.**
  An entry that omits `prosiform.root` uses the invocation working directory. A linked file that omits it uses the effective root of the parent that reached it. A further file that also omits it uses that same effective root.

- **A declared root belongs to the file that writes it.**
  The value resolves from that file's directory. A blank `root` value is invalid. Group and group-depth stay that file's own declarations.

- **One file renders once for each root that reaches it.**
  The bytes are captured once. A reaches B under one root and C under another, and both reach D. D is emitted twice, and each emission resolves D's links under the root of the parent that reached it. Two parents whose roots are the same root produce one emission.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-polymorphic-root-variants/w01.md) | Resolve omitted roots from the reaching parent | AC1, AC2, AC3 | [E06:W08](https://github.com/m2ux/prosiform/issues/218) | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-polymorphic-root-variants/w02.md) | Render one variant for each root | AC4, AC5, AC6 | W01 | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-polymorphic-root-variants/w03.md) | State the inherited root contract | AC7, AC8 | W02, [E06:W11](https://github.com/m2ux/prosiform/issues/218) | | |

## Acceptance Criteria

- [ ] **AC1.** An entry that omits `prosiform.root` resolves its links from the invocation working directory, as the file-root suite shows.
- [ ] **AC2.** A linked file that omits `prosiform.root` resolves its links from the effective root of the parent that reached it, including through a further file that also omits it, as the file-root suite shows.
- [ ] **AC3.** A declared `prosiform.root` resolves from the declaring file's directory, as the file-root suite shows.
- [ ] **AC4.** One physical file is captured once however many roots reach it, as the file-root suite shows.
- [ ] **AC5.** That file is emitted once for each distinct effective root that reaches it, as the file-root suite shows.
- [ ] **AC6.** Each emission resolves the file's links under that emission's root, as the file-root suite shows.
- [ ] **AC7.** Group and group-depth remain the declarations of the file that writes them when the reaching parent declares different ones, as the metadata suite shows.
- [ ] **AC8.** The author-facing root contract states that a linked file omitting `prosiform.root` uses the reaching parent's effective root, and that one file is emitted once per distinct reaching root, as the authoring check shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-polymorphic-root-variants/README.md) — the polymorphic root rule, the deferral of its implementation, and the trace to Field Refinement.
