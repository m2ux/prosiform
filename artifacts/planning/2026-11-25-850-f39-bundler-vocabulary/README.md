# Bundler Vocabulary

## Executive Summary

Prosiform is a bundler and a run bundles: one word names the tool, the act and the output across the product description, the guide and diagnostics `pf` emits, the documentation, the fixtures, the eval and the contract design. The glossary records "compiler" and "compile" as terms deliberately not used.

[F39, issue #850](https://github.com/m2ux/prosiform/issues/850) holds the feature and stands In Progress on Python board 18. It is delivered on one branch, `f39-bundler-vocabulary`, cut from `main` at 684437c06 (0.34.0), as one draft pull request to `main` with one commit per layer, at head 20bd147152b8ee9f2f68e299a35bee7a225ba0c8. Emitted text changes, so the previous corpus fails against the build and the release that carries it is 0.35.0. The pull request awaits review and is not merged; [test-results.md](test-results.md) records the validation and the two failures `main` already carries. F38, issue #848, is in flight as pull request #849 and changes fixture bundle names, so whichever merges second rebases.

## Decisions

| Decision | Outcome |
| --- | --- |
| Scope | The noun and the verb together. |
| The set of bundles one run writes | "Bundle set", the term the documentation already uses. |
| Eval form `compiled` | `bundle-set`. |
| Eval classes | `missed_run`, `unstated_run`, `misordered_run`; the scenario table is `[[scenario.run]]`. |
| Delivery | One branch and one pull request, with one commit per layer. |

## Vocabulary

| Present | Becomes |
| --- | --- |
| compiler | bundler |
| compile, compiles, compiling, compiled | bundle, bundles, bundling, bundled |
| compilation | bundling, or "run" where it names one invocation |
| the compile step | the bundle step |
| eval form `compiled`, its `compiled/` folders and `instruction-compiled.md` | `bundle-set`, `bundle-set/` and `instruction-bundle-set.md` |
| `uncompiled`, `overcompiled`, `misordered_compile` | `missed_run`, `unstated_run`, `misordered_run` |
| `[[scenario.compile]]` | `[[scenario.run]]` |
| `Compiled`, `compiled()` and the other identifiers in `src/prosiform` | `Bundled`, `bundled()` and their counterparts |

Prose is rewritten sentence by sentence. "Bundle" is already the noun for the output, so a substituted sentence can read "bundles a bundle"; each such sentence is reworded, as "bundles it on its own" for "compiles it as a bundle of its own". `re.compile` is the standard library's and stays.

## Scope

Measured on `main` at 684437c06 with a case-insensitive search for "compil": about 1,680 occurrences in 275 files, of which 140 are `re.compile` and stay.

| Area | Occurrences | What changes |
| --- | --- | --- |
| `evals/` | 1,099 | The form and class names, the scenario table, 127 files under `compiled/` folders, `instruction-compiled.md`, identifiers such as `compiled_form` and `compiled_set`, the README and runbook, and the committed records. |
| `src/` | 217 | Emitted text in `cli.py`, `dispatch.py` and `metadata.py`; docstrings and identifiers across the package; the tests, `test_conversion_compilation.py` by name. |
| `fixtures/` | 200 | 158 manifests (descriptions and quoted design headings), eleven fixture folder names, sample prose in a few sources with their expected bundles, and the README. |
| `docs/`, `invocation.md`, `README.md`, `checks.md` | 131 | Prose, and eleven images under `docs/images` re-rendered. |
| `checks/`, `scripts/` | 98 | Prose, test names, the renderer's titles, option help, messages and record keys. |
| Contract design on `engineering` | 69 | Statements and section headings in `design.md`, then the shipped links re-pinned. |

### Emitted Text

These are bytes a fixture or an agent observes, so they change with their expectations in one commit.

- The exit-status line of the help text, "successful compilation".
- The guide bare `pf` prints: its opening sentence, "Compiling a link" and the `↳` rule.
- Diagnostic messages and remedies in `cli.py`, `dispatch.py` and `metadata.py`.

## Out of Scope

- **Historical records.** Planning folders, run records and review artifacts on `engineering` keep the wording they were written with.
- **A paid eval run.** The committed baselines measure the guide as it read at their revisions, which the eval README already states. `make eval-harness` holds the renamed runner, scorer and report against the stub agent.
- **The release.** Version 0.35.0 is cut by the release procedure after the merge.
- **Consuming skills.** Skills in other repositories that quote the guide or describe prosiform follow in their own repositories.

## Layers

Each layer is one commit, in this order. The build, the corpus and the documentation share one commit, because `make invocation` holds the documented invocation to the build's help text and `make conformance` holds the fixtures to the design the documentation pins.

| Layer | Commit | Holds |
| --- | --- | --- |
| Design | c394f23056ad69400277b008fdd2ccd8841ded5e on `engineering` | The design's statements, section headings and guide text. The shipped links pin this revision. |
| Noun | 0c88cef34 | The product description, the avoided-terms row, and every "compiler" in prose and identifiers. No emitted output changes. |
| Build, corpus and documentation | a07763564 | Emitted text, docstrings and identifiers in `src/prosiform`, its tests, the fixtures, `docs/`, `invocation.md`, the READMEs, `checks/` and `scripts/`, the re-rendered images and the re-pinned design links. |
| Eval | 20bd14715 | The form, the classes, the scenario table, the folders, the identifiers, the tests and the committed records. |

## Names Chosen in Delivery

| Present | Becomes | Why |
| --- | --- | --- |
| `cli.compiled` | `cli.bundle_one` | `bundled` is a local name in the same module. |
| `cli.Compiled` | `cli.Bundled` | One bundle with its run evidence. |
| The eval's `Compile` | `StatedRun` | One `pf` run a scenario states. |
| `Scenario.compile` | `Scenario.runs` | The runs a scenario states. |
| `COMPILED_SET` | `BUNDLE_SET` | The session form given a bundle set. |
| `compile_root`, `compile_faults`, `read_compile` | `run_root`, `run_faults`, `read_run` | Each concerns stated runs. |

## Tasks

- [x] Register F39 from [issue.md](issue.md) on board 18.
- [x] Revise the design on `engineering` and record the revision to pin.
- [x] Cut `f39-bundler-vocabulary` from `main` in a worktree.
- [x] Land the noun layer.
- [x] Land the build, corpus and documentation layer.
- [x] Land the eval layer.
- [x] Run the search of AC1, the previous corpus against the build, `make eval-harness` and every target of `make check`, and record the results.
- [x] Open the draft pull request to `main` and link it to F39 through Development.
- [ ] Review the pull request, verify each criterion at the merge revision, merge and record delivery.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [issue.md](issue.md) | Body of F39, issue #850, with its acceptance criteria. |
| [pull-request.md](pull-request.md) | Body of the delivering pull request. |
| [test-results.md](test-results.md) | The validation observed at the pull request's head. |

## Links

- [Contract design](../2026-10-17-prosiform-v1/design.md)
- [Versioning](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md)
