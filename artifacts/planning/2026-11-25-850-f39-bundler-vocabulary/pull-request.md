## Overview

Prosiform is a bundler and a run bundles. The product description, the guide and diagnostics `pf` emits, the documentation, the fixtures and the eval used "compile" for the act the glossary defines as bundling; they now use one word. The help text's exit-status line changes, so the previous corpus fails two fixtures and the release carrying this is 0.35.0.

## Changes

### Vocabulary

- **Name the tool a bundler.**
  The README headline, the package description, the documentation, and the renderer's titles, options, messages and record keys say "bundler".
- **Name the act bundling.**
  Prose, docstrings, identifiers, fixture folders and manifests say "bundle". Sentences a substitution left reading "bundles a bundle" are reworded, as "bundles the target on its own".
- **Hold the choice.**
  The glossary lists "compile" and "compiler" among the terms deliberately not used.

### Emitted Text

- **Guide, help and diagnostics.**
  The guide bare `pf` prints, the help text's exit-status line, and each diagnostic message and remedy use the new verb. No bundle's bytes change.
- **Design pin.**
  The shipped links pin the design revision that states the same vocabulary, and each manifest quotes its section headings as they stand there.

### Eval

- **Form.**
  The session form given a bundle set with the build is `bundle-set`, with its folders and `instruction-bundle-set.md`.
- **Classes.**
  `missed_run`, `unstated_run` and `misordered_run` score the `pf` runs a scenario states, and the scenario table is `[[scenario.run]]`.
- **Records.**
  The committed run records carry the new names with every figure as recorded.

### Names

- **`cli.bundle_one`.**
  The function that bundles one selection takes this name because `bundled` is a local name in the same module; its result is `cli.Bundled`.
- **`StatedRun`.**
  The eval's record of one stated `pf` run, held by `Scenario.runs`.

### Checks

- **Hyphens recommendation.**
  The authoring check reads the recommendation from the invocation guide, which owns it. `README.md` on `main` states its usage without that sentence, which failed `make harness` there.

## Test Plan

| Test | Description | Coverage | Pass |
| --- | --- | --- | --- |
| T1 | Case-insensitive search of the tree for the old vocabulary | AC1, AC2, AC3 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-850-f39-bundler-vocabulary/test-results.md#vocabulary-search) |
| T2 | Build tests, lint, format and types | AC4 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-850-f39-bundler-vocabulary/test-results.md#build-tests) |
| T3 | Complete fixture corpus, and the corpus of `main` against this build | AC4, AC9 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-850-f39-bundler-vocabulary/test-results.md#fixture-corpus) |
| T4 | Links, vocabulary, invocation, conformance and re-rendered images | AC3, AC5, AC8 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-850-f39-bundler-vocabulary/test-results.md#source-and-documentation) |
| T5 | Eval harness against the stub agent, compared with `main` | AC6 | [39 failures, the same 39 as `main`](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-850-f39-bundler-vocabulary/test-results.md#eval-harness) |
| T6 | Recorded figures compared with `main` | AC7 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-850-f39-bundler-vocabulary/test-results.md#recorded-figures) |
| T7 | `make check` | AC10 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-850-f39-bundler-vocabulary/test-results.md#checks-harness) |

## References

- **R1.** [Test results](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-850-f39-bundler-vocabulary/test-results.md) — The validation observed at head 6b8d5a6cb, with the eval-harness failures `main` already carries.
- **R2.** [Planning record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-850-f39-bundler-vocabulary/README.md) — The vocabulary mapping, the decisions and the commit layers.
- **R3.** [Design revision](https://github.com/m2ux/prosiform/blob/c394f23056ad69400277b008fdd2ccd8841ded5e/artifacts/planning/2026-10-17-prosiform-v1/design.md) — The contract stated in the bundler vocabulary, which the shipped links pin.
