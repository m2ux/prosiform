## Overview

An entry or local preset can explicitly reuse pure settings from a named preset in another captured source without importing its body or changing the receiving role. Effective origins remain visible in the build ledger.

## Problem

- Repeated entry maps and substitution settings have separate owners across source files.
- Reuse must preserve the declaring source's path meaning and the distinction between ordinary local routing, entry level maps and explicit entry stubs.

## Proposal

- **A narrow import declaration.**
  The proposed imports list names a source-relative Markdown path and an exact preset name, selecting exactly one named preset declaration by the existing complete-name normalization.
- **No body and no default.**
  An import reads only the target's own levels, substitutions and pure imports, and counts that declaration as selected; no implicit default or body is selected.
- **Pure settings and local roles.**
  Imported declarations contain only levels, substitutions and imports. The receiving preset owns its existing choice, stub, brief, group and capability role.
- **Existing reach.**
  Imported levels affect dispatch only where the entry-map rules permit them; substitutions retain the receiving role's existing reach.
- **Explicit origins.**
  Keys resolve from their original declaring source and substitutes keep the existing key-relative meaning. Existing selected-over-default layering remains explicit.
- **Explicit conflicts.**
  Equal contributions coalesce with every origin recorded; incompatible values in one flattened preset fail with both origins. Missing sources or presets, impure targets and cycles refuse the build.
- **Ordinary accounting.**
  A source read only for an import counts toward the budgets. An imported substitution warns as unused once, where no importing document names its key.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e02/w00.md) | Pure import contract and controls | AC1 | [E01:W00](https://github.com/m2ux/prosiform/issues/868) | | 1 | |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e02/w01.md) | Pure capture and direct levels | AC2 | W00 | | 2 | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e02/w02.md) | Nested origins refusals and ledger | AC3, AC4 | W01, [E01:W02](https://github.com/m2ux/prosiform/issues/868) | | 1 | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e02/w03.md) | Public reuse example and equivalence | AC5 | W02 | | 2 | |

## Acceptance Criteria

- [ ] **AC1.** The pure import contract fixes the supported fields, exact target selection, lexical origins and conflict and cycle boundary against frozen controls, as the contract review shows.
- [ ] **AC2.** The pure capture service returns only the exact normalized named preset metadata with its captured source identity, as direct-level and purity tests show.
- [ ] **AC3.** Nested levels and substitutions retain lexical origins and receiving-role scope, with missing, impure, cyclic or conflicting imports refusing publication, as the origin and scope corpus and negative fixtures show.
- [ ] **AC4.** The ledger traces imported settings to the captured declarations that contributed them, as ledger and import integration tests and `make check` show.
- [ ] **AC5.** The documented reusable-settings example bundles to the same Markdown as its inline-settings control, as the paired example check and documentation checks show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture) — the import design, valid and invalid matrix and work items.
- **R2.** [Key-relative Substitutes](https://github.com/m2ux/prosiform/issues/830) — the existing path-origin contract that imports preserve.
- **R3.** [Entry Stubs](https://github.com/m2ux/prosiform/issues/833) — explicit run-scoped fixture substitutions retain their current role.
- **R4.** [Capability Levels](https://github.com/m2ux/prosiform/issues/827) — the entry alone supplies the run's level map.
