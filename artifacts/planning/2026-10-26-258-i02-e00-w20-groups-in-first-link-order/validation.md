# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w20`, branch `i02/e00/w20-groups-in-first-link-order`, cut from `i02/e00/main` at `7c47e0a0`, `f171675d` merged in; validated at `334958e4`.
- Build: `uv run --frozen --project <worktree>/src pf`, named as `PROSIFORM_BUILD`.
- Design: `artifacts/planning/2026-10-17-prosiform-v1/design.md` at `409d6c7b`, as `README.md` pins it.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 252 fixture(s), 252 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build | 0 |
| `make conformance` | 288 clause(s), 55 covered by no fixture, 0 declaration(s) naming no clause; 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere | 0 |
| `make independence` | every word of every fixture declaration and every report entry is one the contract states | 0 |
| `make links` | every reference in 104 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 38 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1067 passed | 0 |
| `make harness` | 614 passed | 0 |
| `make smoke` | installed command named on the path, independent of the working directory and the repository | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 64 files already formatted | 0 |
| `make typecheck` | no issues found in 63 source files | 0 |
| `make check` | **not run**, as the brief directs | — |

## Re-record diff check

The base outputs were restored from `i02/e00/main` at `f171675d`, the 12 failing fixtures re-recorded from the build, and each pair compared by two scripts:

- **Reorder only.** Each output split into heading-delimited blocks (fences respected, trailing blank lines dropped, `#slug-N` normalized to `#slug`); the two block multisets are equal for all 12.
- **Same targets.** Every `](#fragment)` resolved through `prosiform.source.fragments` to the block it heads; per block, the targets match before and after for all 12 (0 unresolved).

Moved sibling sets: top-level groups (all 12), merged sections in `grouping/a-whole-document-reference-to-a-member`, overview and variant subsections in `grouping/one-spelling-for-every-generated-heading`, and Artifacts and Protocols members in the two usage-example bundles.

## Example outlines

- `modes/sync-mode.md`: Sync Mode (Procedure, Outcomes), Rules, Conventions, Artifacts (Issue, Issue Body, Task Body, Delivery Evidence, …), Protocols (Issue Closure, Review Pull Request, Epic Integration, Change Overview), Understand Mode, References (Requirement Characteristics).
- `modes/plan-mode.md`: Plan Mode (Procedure, Outcomes), Rules, Conventions, Artifacts (Issue, Planning Record, Pull Request Body, Pull Request, …), Propose Mode, Sync Mode, References, Protocols (Issue Closure, Review Pull Request, Epic Integration, Change Overview), Understand Mode.

## Search

- `path order`, `by path`, `alphabetic`, `lexical` across manifests, docs, `invocation.md`, `README.md` and `src/prosiform`: only the corpus run order, declaration-conflict order and the traversal's per-round read order remain, each still true.
