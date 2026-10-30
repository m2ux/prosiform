# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w11`, branch `i02/e00/w11-bootstrap-mode-links`, cut from `i02/e00/main` at `4c9c8a18`; validated at `8c3effa1`.
- Build: `uv run --project <worktree>/src --frozen pf`, named as `PROSIFORM_BUILD`. This row changes nothing under `src/`.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 260 fixture(s), 260 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build `PROSIFORM_BUILD` names | 0 |
| `make conformance` | 305 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause | 0 |
| `make independence` | every word of every fixture declaration and every report entry is one the contract states | 0 |
| `make links` | every reference in 101 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 38 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1104 passed | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 64 files already formatted | 0 |
| `make typecheck` | no issues found in 63 source files | 0 |
| `make check` | **not run**, as the brief directs | — |

## AC15 search

- Modes-list items opening `- **[↳ `: 10; unmarked Modes-list items: 0.
- Destinations: `modes/propose-mode.md`, `plan-mode.md`, `align-mode.md`, `sync-mode.md`, `advance-mode.md`, `deliver-mode.md`, `understand-mode.md`, `hoist-mode.md`, `standup-mode.md`, `revise-mode.md`, each as the base writes it.
- H2 order: `Bootstrap` (line 21), `Modes` (25), `Rules`, `Conventions`, `Dependencies`.
- Frontmatter `prosiform` holds `root` only.

AC15 holds.

## AC16 search

- `Linked sections` (case-insensitive): 0 occurrences in `SKILL.md`.
- `Prerequisites`: 0 occurrences.
- No file in the repository links `SKILL.md#rules` or a Linked sections anchor.

AC16 holds.

## Bundles

Each of the ten modes was bundled from `example/work-planner` at the base and at `8c3effa1`.

| Mode | Exit | Lines (base = W11) | `↳` | Bootstrap | Linked sections |
| --- | --- | --- | --- | --- | --- |
| advance | 0 | 3400 | no | no | no |
| align | 0 | 2556 | no | no | no |
| deliver | 0 | 4657 | no | no | no |
| hoist | 0 | 1555 | no | no | no |
| plan | 0 | 4085 | no | no | no |
| propose | 0 | 662 | no | no | no |
| revise | 0 | 77 | no | no | no |
| standup | 0 | 3355 | no | no | no |
| sync | 0 | 3198 | no | no | no |
| understand | 0 | 1089 | no | no | no |

No bundle compiles the Modes list's `↳` links, and no usage fixture is re-recorded. `pf -o <scratch>/plan.bundle.md modes/plan-mode.md`, run from `example/work-planner` as the Bootstrap section directs, exits 0 with one `W_ENTRY_DESTINATION` warning and writes 203,906 bytes (sha256 `114a879a0762…`), `cmp`-identical to `a-procedure-and-everything-it-reaches`'s expected output.
