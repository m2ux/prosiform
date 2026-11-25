# Bundler Vocabulary

## Executive Summary

Prosiform is a bundler and a run bundles: one word names the tool, the act and the output across the product description, the guide and diagnostics `pf` emits, the documentation, the fixtures, the eval and the contract design. The glossary records "compiler" and "compile" as terms deliberately not used.

The feature is proposed and not yet registered. It is delivered on one branch, `f39-bundler-vocabulary`, cut from `main` at 684437c06 (0.34.0), as one pull request to `main` with one commit per layer. Emitted text changes, so the previous corpus fails against the build and the release that carries it is 0.35.0. F38, issue #848, is in flight as pull request #849 and changes fixture bundle names, so whichever merges second rebases.

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

Each layer is one commit that passes `make check`, in this order.

1. **Design.** On `engineering`: the design's statements and section headings. The revision is the one the shipped links pin.
2. **Noun.** The product description, the avoided-terms rows, and every "compiler" in prose and identifiers. No emitted output changes.
3. **Build and corpus.** Emitted text, docstrings and identifiers in `src/prosiform`, its tests, and the fixtures: folder names, manifests, quoted design headings, sample prose with expected bundles, and the re-pinned design links.
4. **Documentation and tools.** `docs/`, `invocation.md`, the READMEs, `checks/` and `scripts/`, with the images re-rendered.
5. **Eval.** The form, the classes, the scenario table, the folders, the identifiers, the tests and the committed records.

## Tasks

- [ ] Register F39 from [issue.md](issue.md) on board 18.
- [ ] Revise the design on `engineering` and record the revision to pin.
- [ ] Cut `f39-bundler-vocabulary` from `main` in a worktree.
- [ ] Land the noun layer.
- [ ] Land the build and corpus layer.
- [ ] Land the documentation and tools layer.
- [ ] Land the eval layer.
- [ ] Run the search of AC1, the previous contract tag's corpus against the build, `make eval-harness` and `make check`, and record the results here.
- [ ] Open the pull request to `main`, link it to F39 through Development, and verify each criterion at the merge revision.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [issue.md](issue.md) | Proposed body of F39, with its acceptance criteria. |

## Links

- [Contract design](../2026-10-17-prosiform-v1/design.md)
- [Versioning](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md)
