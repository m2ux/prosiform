## Overview

Prosiform resolves links between Markdown sources, keeps each region once and rewrites addresses. Markdown goes in and Markdown comes out, which is the work of a bundler. The glossary already states "It bundles; what it produces is a bundle", while the README, the package metadata and the supporting tools name the product a compiler. This hot-fix names the product a bundler throughout the shipped tree and the contract design.

Target: `main`

## Problem

- **Two nouns name one product.**
  The glossary defines the act as bundling and has no entry for a compiler, yet the README headline, the package description and the renderer's output call the product one. A reader meets a term the vocabulary never defines.
- **The noun invites the wrong comparison.**
  In agent tooling a compiler commonly means a tool that optimises instruction wording. Prosiform changes no wording, so the name sets an expectation the product does not meet.
- **Nothing holds the choice.**
  The glossary's list of terms deliberately not used omits the word, so the vocabulary check cannot refuse it where the design marks it.

## Proposal

- **Name the product a bundler.**
  The README headline, the package description and the package docstring read "a deterministic bundler for instruction sets written as linked Markdown". Prose in the documentation, checks, eval and fixture descriptions that names the tool follows.
- **Rename the identifiers that carry the noun.**
  The diagram renderer's card title, option help, error messages and run-record keys, the linked-bootstrap test's identity artifact, and the test names that carry the noun use "bundler".
- **Record the term as avoided.**
  The glossary's list of terms deliberately not used gains "compiler" with its reason: a compiler translates between languages, and a run resolves, consolidates and rewrites within one.
- **Align the contract design.**
  The design's statements naming a compiler name a bundler, and the shipped links to the design pin the revised revision.
- **Leave emitted bytes alone.**
  The verb "compile", the guide `pf` prints, the eval's `compiled` form and its `overcompiled`, `uncompiled` and `misordered_compile` classes stay as they are. The guide is emitted output a fixture observes, so the verb is a contract change of its own.

## Acceptance Criteria

- [ ] **AC1.** The word "compiler" appears in the shipped tree only in the avoided-terms row of `glossary.md`, as a case-insensitive repository search shows.
- [ ] **AC2.** `README.md`, `pyproject.toml` and the package docstring in `__init__.py` describe a deterministic bundler.
- [ ] **AC3.** `glossary.md` names "compiler" as a term deliberately not used and states why, and `make vocabulary` passes.
- [ ] **AC4.** `render-diagram.py`, `render-example.py` and `test_linked_bootstrap.py` carry "bundler" in their titles, option help, messages, record keys and artifact names, as their tests show.
- [ ] **AC5.** `design.md` names a bundler wherever it named a compiler, and every shipped link to the design pins that revision.
- [ ] **AC6.** A run emits the bytes it emitted before: the previous contract tag's corpus passes against the delivering build, and the guide bare `pf` prints is byte-identical.
- [ ] **AC7.** The delivering revision passes `make check`.

## References

- **R1.** [Glossary](https://github.com/m2ux/prosiform/blob/main/docs/glossary.md) — States "It bundles; what it produces is a bundle" and lists the terms deliberately not used.
- **R2.** [Versioning](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md#what-the-numbers-mean) — Wording in the design and prose in a guide are a patch: a change no fixture can observe.
- **R3.** [Planning record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-bundler-term/README.md) — Scope measured on `main` at 684437c06 and the open decisions.
