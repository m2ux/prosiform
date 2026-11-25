## Overview

Prosiform resolves links between Markdown sources, keeps each region once and rewrites addresses. Markdown goes in and Markdown comes out, which is the work of a bundler. The glossary already states "It bundles; what it produces is a bundle", while the product description, the guide `pf` prints, the diagnostics, the fixtures and the eval say it compiles. This feature gives the act and the tool one word: prosiform is a bundler, and a run bundles.

Target: `main`

## Problem

- **Two words name one act.**
  The glossary defines the act as bundling and has no entry for compiling, yet the README, the guide, the diagnostics and the documentation use "compile" for the same act. A reader meets a term the vocabulary never defines.
- **The word invites the wrong comparison.**
  A compiler translates one language into another, and in agent tooling the word commonly means a tool that optimises instruction wording. Prosiform does neither, so the name sets an expectation the product does not meet.
- **The eval names follow the old verb.**
  The `compiled` form and the `uncompiled`, `overcompiled` and `misordered_compile` classes name pf runs and the bundle set a run writes by a word the glossary does not hold.
- **Nothing holds the choice.**
  The glossary's list of terms deliberately not used omits both words, so the vocabulary check cannot refuse them where the design marks them.

## Proposal

- **Name the tool a bundler and the act bundling.**
  "Compiler" reads "bundler" and "compile" reads "bundle" in every form, in prose, docstrings, identifiers, file names and fixture names. "Compilation" reads "bundling", or "run" where it names one invocation. Each sentence is rewritten to read naturally, as "bundles it on its own" for "compiles it as a bundle of its own".
- **Change what a run emits.**
  The guide bare `pf` prints, the help text, and each diagnostic message and remedy carry the new verb, with the fixture expectations that observe them.
- **Name the eval by what it scores.**
  The `compiled` form is `bundle-set`, after the term the documentation already uses for the bundles of one run. The classes are `missed_run`, `unstated_run` and `misordered_run`, and the scenario table is `[[scenario.run]]`. The committed eval records carry the new names with their figures as recorded.
- **Record the terms as avoided.**
  The glossary's list of terms deliberately not used gains "compiler" and "compile" with their reason.
- **Align the contract design.**
  The design uses the new vocabulary, its section headings included, and the fixture manifests that quote those headings and the shipped links that pin the design follow it.

## Acceptance Criteria

- [ ] **AC1.** A case-insensitive search of the shipped tree for "compil" finds only calls to `re.compile`, the avoided-terms rows of `glossary.md` and the licence text in `LICENSE`.
- [ ] **AC2.** `README.md`, `pyproject.toml` and the package docstring in `__init__.py` describe a deterministic bundler.
- [ ] **AC3.** `glossary.md` names "compiler" and "compile" as terms deliberately not used and states why, and `make vocabulary` passes.
- [ ] **AC4.** The guide and help text in `cli.py`, and every diagnostic message and remedy the build emits, use the new verb, as the corpus fixtures and unit tests that observe them show.
- [ ] **AC5.** `design.md` uses the new vocabulary, each `manifest.toml` quotes its section headings as they stand, and every shipped link to the design pins that revision, as `make conformance` and `make links` show.
- [ ] **AC6.** The eval's form is `bundle-set` and its classes are `missed_run`, `unstated_run` and `misordered_run` in `workflow.py`, `score.py`, `report.py`, each `scenarios.toml` and the eval `README.md`, as `make eval-harness` shows.
- [ ] **AC7.** `baseline.json`, `agent-pick.json`, `dispatch-brief.json` and their reports carry the new form and class names with every figure as recorded.
- [ ] **AC8.** Every image under `docs/images` is the output of the renderer at the delivering revision.
- [ ] **AC9.** A run emits the bundles it emitted before: every expected `.bundle.md` differs from its predecessor only where its own source's prose changed.
- [ ] **AC10.** The delivering revision passes `make check`.

## References

- **R1.** [Glossary](https://github.com/m2ux/prosiform/blob/main/docs/glossary.md) — States "It bundles; what it produces is a bundle" and lists the terms deliberately not used.
- **R2.** [Versioning](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md#what-the-numbers-mean) — Below 1.0.0, a release whose previous corpus fails against it moves the minor.
- **R3.** [Planning record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-850-f39-bundler-vocabulary/README.md) — Scope measured on `main` at 684437c06, the vocabulary mapping and the commit layers.
