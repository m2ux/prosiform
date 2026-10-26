# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w19`, branch `i02/e00/w19-artifacts-grouped-per-file`. Commits: `537ecdb6` (declarations), `f9f82c94` (merge of `i02/e00/main` at `7c47e0a0`), `ecb3508c` (fixtures), `8b4f65d1` (README) and `6fcb6b23` (fixture description wording).
- Build: `uv run --frozen --project <worktree>/src pf`, named as `PROSIFORM_BUILD`. This row changes nothing under `src/`.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 252 fixture(s), 252 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build `PROSIFORM_BUILD` names | 0 |
| `make conformance` | 288 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause | 0 |
| `make independence` | every word of every fixture declaration and every report entry is one the contract states | 0 |
| `make links` | every reference resolved; external URLs warned only, no network in the sandbox | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 37 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1065 passed (run outside the sandbox: the linked-bootstrap tests build a wheel) | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 64 files already formatted | 0 |
| `make typecheck` | no issues found in 63 source files | 0 |
| `make check` | **not run**, as the brief directs | — |

`make independence` first failed on the word `twelve` in the grouped fixture's description; the description now names no count.

## Mode Bundles

All ten modes build with exit 0 within the default budgets (`-E 8`, `-O 262144`). Before is base `8040ab68`; after is the branch with `7c47e0a0` merged.

| Mode | Bytes before | Bytes after |
| --- | --- | --- |
| advance-mode | 172,176 | 172,258 |
| align-mode | 132,884 | 132,942 |
| deliver-mode | 247,030 | 247,088 |
| hoist-mode | 85,650 | 85,701 |
| plan-mode | 207,650 | 207,742 |
| propose-mode | 26,324 | 26,373 |
| revise-mode | 6,765 | 6,796 |
| standup-mode | 168,327 | 168,411 |
| sync-mode | 158,133 | 158,222 |
| understand-mode | 47,325 | 47,335 |

## Sync Bundle

Outline after, H1 and H2:

- `# Sync Mode`: `## Procedure`, `## Outcomes`.
- `# Artifacts`: `## Acceptance Criteria`, `## Architecture Overview`, `## Board Delivery`, `## Board Queue`, `## Board`, `## Delivery Branches`, `## Delivery Evidence`, `## Epic Issue Body`, `## Epic`, `## Initiative Issue Body`, `## Initiative`, `## Issue Body`, `## Issue`, `## Plan Change`, `## Planning Record`, `## Pull Request Body`, `## Pull Request`, `## Repository Graph`, `## Task Body`. Each holds its own `### Operations`, `### Fields` and `### Commands`, as many as the artifact has.
- `# Conventions`.
- `# Understand Mode`: `## Procedure`, `## Outcomes`.
- `# Protocols`: `## Change Overview`, `## Epic Integration`, `## Issue Closure`, `## Review Pull Request`.
- `# References`: `## Requirement Characteristics`.
- `# Rules`.

Anchor links, measured by a script that slugs headings outside code fences GitHub-style, with `-N` suffixes for repeats, and checks every `](#...)`:

| Measure | Before | After |
| --- | --- | --- |
| Lines | 3,238 | 3,272 |
| Anchor links | 333 | 333 |
| Unresolved anchors | 0 | 0 |
| Median link distance (lines) | 899 | 147 |
| p90 link distance (lines, nearest rank) | 2,237 | 1,659 |
| Repeated heading slugs | 26 over 74 headings | 13 over 78 headings |

The repeats after are mostly the per-artifact `Operations` (18), `Fields` (19) and `Commands` (12), each told apart by its ordinal. Every mode bundle resolves every anchor; the median link distance falls in every mode but revise-mode, whose one artifact contributes a single field and whose median holds at 33.5.

## Fixtures

Re-recorded from the build, with `-o -` and `-d json` as the corpus runner invokes it:

- `usage-example/a-bare-fragment-and-its-referring-document`
- `usage-example/a-procedure-and-everything-it-reaches`
- `usage-example/every-document-under-a-directory-merged`
- `usage-example/two-selected-sections`

`every-document-under-a-directory-merged` now describes one group headed Artifacts, one section per member headed by its own title, holding its own Operations, Fields and Commands, and a whole-document reference resolving to that section. Its clauses drop `Document content above the grouping depth` and `The overview section` and add `A heading for every member`. The other three descriptions hold unchanged.

## Prose

- `example/README.md`: the fragment example quotes `# Artifacts`, `## Epic Issue Body`, `### Operations` and the operation at H4. `Declare groups per file` opens with `One block per document`, quoting the depth-1 declaration and the bundle's `# Artifacts` / `## Dependency Graph` opening. The references paragraph and the my-skill paragraph no longer contrast with an Overview. Every markdown excerpt was checked as a verbatim substring of a fixture output or source.
- `example/work-planner/guidelines.md` and `example/guidelines.md` state nothing about the artifacts' grouping, so they are unchanged. `invocation.md`'s `group-depth: 2` sample declares a generic `rules` group, not the example.
