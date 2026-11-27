# Decisions And Review

## Standing Decisions

- I20 is feature planning on board 18 under `theme:python`. No proposal is required.
- Existing doc-only patterns remain with I12; the frozen Rust contract target stays independent. No other issue is amended by this plan.
- Imports reference a path and one exact normalized preset name. Only that metadata declaration is selected; no implicit default and no body. Only levels, subst and pure imports are admitted; imported and local conflicts fail within a flattened preset. Selected-over-default layering stays distinct.
- The `group` of a `choice` mapping names a local axis; an alternative whose `choice` is a plain string belongs to the document's single unnamed group in the same resolution model.
- The agent checkpoint is representative mechanism evidence, at most four fresh contexts, never a full combination sweep or a general performance or quality proof. It uses declared thin adapters over existing public harness owners and needs a separate release.

## Review Rulings, 2026-11-27

The user reviewed the published plan against pf 0.36.0 and ruled on each point.

- **Reference release.** pf 0.36.0 at `8cedda4cc06b0486168addc05f057161192a22a6` is the baseline. The five retained controls reproduce under it byte for byte: exit status, diagnostics and bundle hashes.
- **Specimen stage.** A new first epic, Design Specimens, holds one specimen set for each feature, a combined set and the scrutiny ruling. The existing epics follow it as E01 to E03, and each contract row waits on the ruling.
- **Record name.** The file is named for one word, `ledger`, and written by `--ledger`. "Manifest" names the corpus fixture declaration and "provenance" is a glossary term, so neither is used. Its notation was first TOML and is YAML, as [Scrutiny Rulings](#scrutiny-rulings-2026-11-27) records.
- **Order of code work.** The three features are built in turn, each end to end, and the epic priorities carry that order: an epic of a lower number waits while a higher one runs. Local Choice Groups is last, since it alone changes behaviour pf 0.36.0 has. The parallel work is the three specimen rows.
- **Lanes.** Two capability lanes with cross-family review, as [Lanes](#lanes) states.
- **Additions admitted.** A repeatable `--pick` at the entry; the ledger written to standard output in check mode; `--verify` holding a published set to its ledger; `--presets` listing a document's choices without bundling.
- **Gap fixes.** The ledger records the invocation; its schema ships on main beside the fixture schema.

## Scrutiny Rulings, 2026-11-27

The user ruled on each design point the specimen sets showed, one at a time, and on the ledger's notation once the same ledger was rendered by each candidate's library. The user then accepted the ledger, import, choice-group and combined sets as they stand.

| Point | Ruling | Declined |
| --- | --- | --- |
| Warnings in the ledger | Omitted: the ledger records what was built | Recording each code with what it names |
| Verification codes | `E_LEDGER_MISMATCH` and `E_LEDGER_NOT_FOUND` | Reusing `E_SOURCE_CHANGED` and `E_TARGET_NOT_FOUND` |
| A source read only for an import | Counts toward the file and byte budgets | Standing outside the budgets |
| An imported pair no link names | Warns once, where no importer in the run names its key | Warning in each importing document |
| Import refusal codes | Existing codes, with `E_IMPORT_CYCLE` new | A code for each import refusal |
| Two declarations stating one value | Coalesce, the ledger recording every origin under `also` | Recording the first origin alone; refusing the duplicate |
| A pick naming a member of a fixed group | `E_INVALID_USAGE`, naming the fixed and the open group | Reporting it as an unmade pick |
| The preset listing's format | Text | The ledger's notation and vocabulary |
| The ledger's notation | YAML, each string quoted, written by the `ruamel-yaml` library pf already ships; the file is `ledger.yaml` | TOML through `tomli-w`, a new dependency whose layout carries no indentation and one list item to a line |
| Where hashes and file names live | In the ledger, an output of the build: each source's and each bundle's hash and each bundle's file name, which `--verify` holds a published set to | A `SHA256SUMS` file apart, written by a `--sums` option and checked by `sha256sum -c`, which the user ruled for and then withdrew |
| A hash of the ledger itself | `ledger.yaml.sha256`, written with the ledger and holding its hash alone; `--verify` reads it first | A hash file listing each bundle as well, which states a bundle's hash twice; no hash file |
| The schema across the three deliveries | One schema, numbered 1 and whole from the ledger epic; the later epics write fields it already admits | A number raised by each epic that adds a field |
| The part of a source a bundle carries | `lines`, the first and last source line carried | Leaving it out, which the user ruled for and then withdrew |
| The line a setting or link was written on | Not recorded: a setting's origin is its document and preset, and a link is named by its source, target and title | `line` on each origin and link row, which the user restored and then dropped on its cost: pf 0.36.0 keeps no position for a level, stub, alternative or brief |
| Where an alternative's group is written | In `choice`, a mapping of `group` and `states`; an alternative with no group keeps the plain string | A `choice-group` field beside `choice`; a mapping for every alternative |

## Lanes

A lane marks the model class a row's delivery session needs. The index is board-wide.

| Lane | Model class | Rows |
| --- | --- | --- |
| `1` | Frontier: Opus 5.5 or Fable 5.2 | Every specimen and ruling row; each contract row; the wiring rows crossing selection, dispatch and deferral; the bounded observation |
| `2` | Mid: Sonnet 5.5 | The three isolated services; documentation and examples; verification; the preset listing |

The Review part of each lane `1` row runs on a model of another family than the delivering session, through the Codex agent the eval harness drives.

## Joins

- E02:W01, E02:W02 remain split: capture and lookup is a separately reviewable source-boundary service the complete resolver consumes, and the two rows sit in different lanes.

## Conventions

- **A fixture is declared by its manifest.** A work item names a corpus fixture by its `manifest.toml`; the fixture's source and expected files sit beside it and belong to the same row.
- **The design link moves with the admitting change.** The change that admits a form moves the README's design link to the contract revision stating it, with the fixtures and code entries that revision needs, so the conformance check never reads a contract ahead of the build.
- **Each documentation row moves the link on the pages it rewrites.**

## Considered And Left Out

- **A services epic.** One epic holding the three isolated services would run them at the same time. It is left out: the layer ships nothing a user can run.
- **A YAML file as the import target.** Shared settings would sit in a plain YAML file a document imports, where an import names a Markdown source's frontmatter. It is left out for now, on the user's ruling of 2026-11-27.
- **Presets held outside frontmatter.** A document's own presets would move to a settings file, through an import list under `prosiform:` or split by who reads each setting. It is left out: the user stopped it at scrutiny on 2026-11-27, and every setting is authored in frontmatter.
- **Fixture-first rows on a small-model lane.** Corpus fixtures landed ahead of their wiring under the `awaiting` marker would add a third lane and parallel work inside each epic. It is left out: whether a fixture may name a contract clause before the design link moves is unverified.

## Public Boundary

Publish only the curated generic scope, draft bodies, work items, design, matrix, public synthetic controls and specimens, review and validation records. Raw live tracker captures, local helper scripts and host-specific command logs are coordinator evidence, never public source requirements. No private application source, names, findings or journals enter the upstream record.
