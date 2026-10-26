# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w12`, branch `i02/e00/w12-entry-reference-unwarned`, cut from `i02/e00/main` at `a334c55d`; validated at `79bc6bcd`.
- Build: `uv run --project <worktree>/src --frozen pf`, named as `PROSIFORM_BUILD`.
- Design: `artifacts/planning/2026-10-17-prosiform-v1/design.md` at `698a75e0`, as `README.md` pins it.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 260 fixture(s), 260 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build `PROSIFORM_BUILD` names | 0 |
| `make conformance` | 304 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause; 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere | 0 |
| `make independence` | every word of every fixture declaration and every report entry is one the contract states | 0 |
| `make links` | every reference in 101 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 38 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1101 passed | 0 |
| `make harness` | 624 passed | 0 |
| `make smoke` | the installed command is named on the path, independent of the working directory, independent of this repository | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 64 files already formatted | 0 |
| `make typecheck` | no issues found in 63 source files | 0 |
| `make check` | **not run**, as the brief directs | — |

`make test` counts three fewer than W11's 1104: the two tests asserting the report and its text form, and the validation-only test asserting it, are removed.

## Search

- `W_ENTRY_DESTINATION` or `Entry destinations` (case-insensitive) in the task branch: 0 occurrences.
- `design.md` at `698a75e0`: 0 occurrences.
- `decisions.md` still names the warning; it is left to the orchestrator.
- `fixtures/entry-line/an-entry-destination-carrying-an-ordinal` keeps its name: it observes the entry line's link destination, not the report.
