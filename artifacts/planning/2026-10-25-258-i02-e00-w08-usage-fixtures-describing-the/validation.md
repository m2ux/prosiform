# Validation

> Delivery Record · Created 2026-10-25

## Environment

- Worktree: `.worktrees/i02-e00-w08`, branch `i02/e00/w08-usage-fixtures-describing`, cut from `i02/e00/main` at `119e37a6`.
- Build: `.worktrees/review-272/src/.venv/bin/pf`, a build of `119e37a6`, named as `PROSIFORM_BUILD`. This row changes nothing under `src/`.
- Every expected bundle was recorded as the corpus runner invokes the build: from the fixture's `cwd`, with `-o - -d json` before the manifest's arguments.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 260 fixture(s), 260 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make conformance` | 305 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause; 32 declared name(s) reached, 0 unfixturable, 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere, 16 clause(s) no run states, 3 section(s) stating no behaviour, 3 installation claim(s) no run observes | 0 |
| `make independence` | every word of every fixture declaration and every report entry is one the contract states | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build `PROSIFORM_BUILD` names | 0 |
| `make links` | every reference in 101 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 38 contract term(s) marked in the design, every one defined in `docs/glossary.md`, every definition carried across 24 source(s) | 0 |
| `make check` | **not run**, as the brief directs | — |

`make conformance` reports the same counts at `119e37a6`: the two clauses this row adds to manifests, `Grouping — The overview section` and `Link classification and resource handling — The deferral mark`, were already covered by other fixtures.

## AC11 invocation comparison

Every manifest runs from `cwd = "source"`, the link to `example/work-planner`.

| Fixture | Arguments | Expected stdout |
| --- | --- | --- |
| `a-bare-fragment-and-its-referring-document` | `-f artifacts/epic-issue-body.md #record-epic-delivery` | 11,866 bytes, sha256 `7d02a1a2c4ab…` |
| `a-procedure-and-everything-it-reaches` | `modes/plan-mode.md` | 203,906 bytes, sha256 `114a879a0762…` |
| `every-document-under-a-directory-merged` | `modes/hoist-mode.md` | 82,369 bytes, sha256 `c2ed7de89304…` |
| `two-selected-sections` | `artifacts/epic-issue-body.md#record-epic-delivery artifacts/epic.md#delivery-findings` | 11,911 bytes, sha256 `ab9d6c22d9c1…` |
| `validation-without-publication` | `-c artifacts/epic-issue-body.md#record-epic-delivery` | 0 bytes |

All 10 pairs of `[invocation]` tables were compared; none is equal. AC11 holds.

## AC12 description inspection

Each claim a description makes was checked against the fixture's expected output, outside fenced code.

| Fixture | Claim | Evidence in expected output | Holds |
| --- | --- | --- | --- |
| procedure | bundles that procedure | first H1 is `# Plan Mode` | yes |
| procedure | three modes reached as whole documents, each under a heading of its own | `# Modes/Propose-Mode`, `# Modes/Sync-Mode`, `# Modes/Understand-Mode` | yes |
| procedure | artifact, protocol and reference material those documents link | `## Operations`, `## Fields` (artifacts group), `# Protocols`, `# References` | yes |
| procedure | two deferred links, each keeping its root-relative path | `](guidelines.md#modes)` occurs twice | yes |
| procedure | the document they name stays out | no `# Guidelines` heading | yes |
| merged group | artifacts group emitted without a heading of its own | no `# Artifacts` heading; H1s are `Hoist Mode`, `References` | yes |
| merged group | Overview holds the one member reached as a whole document, under its name | `## Overview` holds one H3, `### Epic Issue Body` | yes |
| merged group | Operations, Fields and Commands each hold one subsection per contributing member | `## Operations` 9 H3s, `## Fields` 11, `## Commands` 5, each named by its document's distinguishing path run (`Epic Issue Body`, `Epic`, …) | yes |
| merged group | second group headed References emits its member's one heading at the grouping depth | `# References` followed by `## Requirement Characteristics`, no further H2 | yes |
| merged group | whole-document reference resolves to the overview subsection | `](#epic-issue-body)` occurs; the first `Epic Issue Body` heading is the overview subsection | yes |
| bare fragment | bundles the section the fragment names | `### *Record* Epic Delivery` | yes |
| two sections | selects each from the document that carries it | `### *Record* Epic Delivery` under `Epic Issue Body` material, `#### Delivery Findings` under `### Epic` | yes |
| two sections | the first's reference to the second resolves to that section | `[Delivery Findings](#delivery-findings) for the caller` | yes |
| validation | emits nothing on standard output | expected stdout is 0 bytes | yes |

The validation fixture's remaining claim, that the run reaches the section's closure, names no count, heading or section; the run's exit status `0` and its one `W_ENTRY_DESTINATION` diagnostic are what the manifest declares of it. AC12 holds.

## README excerpts

Every `markdown` and `yaml` block in `example/README.md` was searched for verbatim in the usage fixtures' expected outputs and the example trees.

| Block | Held by |
| --- | --- |
| Publish step, input | `example/work-planner/modes/plan-mode.md` |
| Entry line, procedure bundle | procedure fixture |
| Publish step, output | procedure fixture |
| Epic issue body operation, input | `example/work-planner/artifacts/epic-issue-body.md` |
| Bare fragment entry line | bare fragment fixture |
| Bare fragment operation | bare fragment, two sections, procedure and merged-group fixtures |
| Artifacts frontmatter | every artifact document |
| Overview and Operations, hoist mode | merged-group fixture |
| `# References` group | merged-group fixture |
| my-skill Rules group | no fixture; matches `pf -o - procedure.md rules/common.md` run in `example/my-skill` |

`pf modes/hoist-mode.md`, run from `example/work-planner` as the page states, wrote `modes_hoist-mode.bundle.md`, which `cmp` reports identical to the merged-group fixture's expected output. The file was removed afterwards.
