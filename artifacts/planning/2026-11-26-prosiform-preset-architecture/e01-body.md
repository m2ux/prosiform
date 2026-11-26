## Overview

An entry or local preset can explicitly reuse pure settings from a named preset in another captured source without importing its body or changing the receiving role. Effective origins remain visible in the build manifest.

## Problem

- Repeated entry maps and substitution settings have separate owners across source files.
- Reuse must preserve the declaring source's path meaning and the distinction between ordinary local routing, entry level maps and explicit entry stubs.

## Proposal

- **A narrow import declaration.**
  The proposed imports list names a source-relative Markdown path and an exact preset name. It uses existing complete-name normalization to select exactly one named preset metadata declaration and count it selected. It reads only its own levels, subst and pure imports; no implicit default or body is selected.
- **Pure settings and local roles.**
  Imported declarations contain only levels, subst and imports. The receiving preset owns its existing choice, stub, brief, group and capability role. Imported levels affect dispatch only where the current entry-map rules permit them; substitutions retain the receiving role's existing reach.
- **Explicit origins and conflicts.**
  Keys resolve from their original declaring source and substitutes keep the existing key-relative meaning. Equal contributions coalesce; incompatible imported/imported or imported/receiving-local values in one flattened preset fail with both origins. Existing selected-over-default layering remains explicit. Missing sources/presets, impure targets and cycles refuse the build.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e01/w00.md) | Pure import contract and controls | AC1 | [E00:W00](https://github.com/m2ux/prosiform/issues/NEW_E00) | | | |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e01/w01.md) | Pure capture and direct levels | AC2 | W00, [E00:W01](https://github.com/m2ux/prosiform/issues/NEW_E00) | | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e01/w02.md) | Nested origins refusals and manifest | AC3, AC4 | W01, [E00:W02](https://github.com/m2ux/prosiform/issues/NEW_E00) | | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e01/w03.md) | Public reuse example and equivalence | AC5 | W02 | | | |

## Acceptance Criteria

- [ ] **AC1.** The pure import contract fixes the supported fields, exact target selection, lexical origins and conflict/cycle boundary against frozen controls, as the contract review shows.
- [ ] **AC2.** The pure capture service returns only the exact normalized named preset metadata with its captured source identity, as direct-level and purity tests show.
- [ ] **AC3.** Nested levels and substitutions retain lexical origins and receiving-role scope, with missing, impure, cyclic or conflicting imports refusing publication, as the origin/scope and negative fixtures show.
- [ ] **AC4.** The effective manifest traces imported settings to the captured declarations that contributed them, as manifest/import integration tests and make check show.
- [ ] **AC5.** The documented reusable-settings example compiles to the same Markdown bundles as its inline-settings control, as the paired corpus specimen and documentation checks show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture) — the import contract, valid/invalid matrix and work items.
- **R2.** [Key-relative Substitutes](https://github.com/m2ux/prosiform/issues/830) — the existing path-origin contract that imports preserve.
- **R3.** [Entry Stubs](https://github.com/m2ux/prosiform/issues/833) — explicit run-scoped fixture substitutions retain their current role.
- **R4.** [Capability Levels](https://github.com/m2ux/prosiform/issues/827) — the entry alone supplies the run's level map.
