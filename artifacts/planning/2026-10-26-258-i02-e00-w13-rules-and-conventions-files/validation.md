# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w13`, branch `i02/e00/w13-rules-and-conventions-files`, cut from `i02/e00/main` at `a334c55d`.
- Build: `uv run --project <worktree>/src --frozen pf`, named as `PROSIFORM_BUILD`. This row changes nothing under `src/`.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 260 fixture(s), 260 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build `PROSIFORM_BUILD` names | 0 |
| `make conformance` | 305 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause | 0 |
| `make independence` | every word of every fixture declaration and every report entry is one the contract states | 0 |
| `make links` | every reference in 103 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 38 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1104 passed | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 64 files already formatted | 0 |
| `make typecheck` | no issues found in 63 source files | 0 |
| `make check` | **not run**, as the brief directs | — |

## Structure

- `rules.md` (`# Rules`) and `conventions.md` (`# Conventions`) sit beside `SKILL.md`, frontmatter `prosiform: root: "."` only; their link destinations are byte-identical to those `SKILL.md` wrote.
- `SKILL.md` H2 order: `Bootstrap`, `Modes`, `Dependencies`.
- All ten modes carry `## Outcomes`; each preamble's last paragraph ends `Follow [Rules](../rules.md) and [Conventions](../conventions.md) and ensure all [Outcomes](#outcomes) are met.` (align-mode: second paragraph).
- `The main path meets [Outcomes](#outcomes).`: 0 occurrences under `example/`.
- `## Prerequisites`: 0 occurrences under `example/work-planner` (AC2).

## Guidelines

### `example/work-planner/guidelines.md`

| Rule | Before | After |
| --- | --- | --- |
| Prose — Reachable dependencies | Each required file, heading and operation has a resolving link. Prerequisites include the files those operations require; links to another file's operation include that file. | Each required file, heading and operation has a resolving link; a link to another file's operation names that file. |
| Modes — Prerequisites | Prerequisites open with `Read these files first.` … | Removed; replaced by **Preamble**: the last preamble paragraph closes with the Rules/Conventions/Outcomes sentence. |
| Modes — Other modes | … Prerequisites require reading documents, not executing their procedures. … Called modes are listed under Prerequisites. | Both sentences removed. |
| Modes — Sections | Prerequisites, Procedure, Outcomes, then Guidance … | Procedure, Outcomes, then Guidance … |
| Protocols — Prerequisites | Prerequisites open with `Read these files first.` They list every file the protocol's Procedure links to … | Removed. |
| Protocols — Sections | Prerequisites, Procedure, then Guidance … | Procedure, then Guidance … |
| Artifacts — Prerequisites | Prerequisites open with `Read these files first.` They list every file the artifact's Operations, Fields or Commands link to. … | Removed. |
| Artifacts — Sections | Prerequisites, Operations, Fields, then Guidance … | Operations, Fields, then Guidance … |
| References — Shape | It does not use Prerequisites, Procedure, Fields, … | It does not use Procedure, Fields, … |
| Entry Point — Section order | Rules precedes Dependencies. | **Sections.** Preamble, Bootstrap, Modes, then Dependencies. |
| Entry Point — Common conventions | The entry point supplies [Conventions](SKILL.md#conventions) before mode selection. Graph-specific setup belongs to [Repository Graph]. | **Rules and conventions.** What binds every mode sits beside the entry point in [Rules](rules.md) and [Conventions](conventions.md), which each mode's preamble links. Graph-specific setup belongs to [Repository Graph]. |
| Progressive Disclosure — intro | Modes are read whole; supporting section reads inherit the mode's command prerequisites. | A mode is followed from its bundle, which carries its rules, conventions and every section it links. |

### `example/guidelines.md`

| Rule | Before | After |
| --- | --- | --- |
| SKILL.md structure — Rules | A statement that binds every mode goes in Rules, never as loose prose in another section. | **Rules and conventions.** A statement that binds every mode goes in a rules or conventions file beside SKILL.md, which each mode's preamble links, never as loose prose in SKILL.md. |
| SKILL.md structure — Commands | SKILL.md links the shared command conventions on a required path and holds no command of its own. | SKILL.md holds no command of its own. |
| Commands — Conventions | … skill-wide prerequisites stand where a procedure reaching them opens no further file: SKILL.md, which selects the mode, or the file holding the operations those procedures open anyway. | … skill-wide prerequisites stand in the conventions file each mode's preamble links. |
| Progressive Disclosure — Placement | Keep shared purpose, mode selection and essential constraints in the entry point. | Keep shared purpose and mode selection in the entry point, and what binds every mode in the rules and conventions files each mode links. |
| Progressive Disclosure — Reading boundaries | The skill's reading rules define a heading link as that section and its subsections, … | A heading link names that section and its subsections, … |
| Progressive Disclosure — Batched reads | Preserve each link's boundary when batching retrieval. … | Removed. |

## Bundles

Each mode bundled with `pf -o <scratch>/<mode>.md modes/<mode>-mode.md` from `example/work-planner`, default budgets (`-E 8`, `-O 262144`). Every bundle exits 0 with one `W_ENTRY_DESTINATION` warning and carries `# Rules` and `# Conventions`.

| Mode | Exit | Bytes |
| --- | --- | --- |
| advance | 0 | 171,467 |
| align | 0 | 132,444 |
| deliver | 0 | 246,141 (base 243,268) |
| hoist | 0 | 85,146 |
| plan | 0 | 206,854 |
| propose | 0 | 25,828 |
| revise | 0 | 6,269 |
| standup | 0 | 167,589 |
| sync | 0 | 157,456 |
| understand | 0 | 46,814 |

## Fixtures

- `a-procedure-and-everything-it-reaches`: re-recorded; description now names the rules and conventions documents each mode links, and three deferred links (`rules.md` adds one to `guidelines.md#modes`).
- `every-document-under-a-directory-merged`: re-recorded; its description names only the artifact group, its Overview, Operations, Fields and Commands sections and the References group, all still present.
- `a-bare-fragment-and-its-referring-document`, `two-selected-sections`, `validation-without-publication`: unchanged output, unchanged description.

AC12 holds for all five usage fixtures.
