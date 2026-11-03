# Validation

The checks W09's work item names, run against task branch `i10/e06/w09-the-composition-page-stating` at `18192a67`, with `origin/i10/e06/main` at `1e1bdc42` merged.

## T1 Pages Read Against The Composition Fixtures

`docs/composition.md` was read against the `composition/` fixtures and the design's Section composition and Recognition rules. It states `↳` followed by a space as the composition mark and `¬↳` as its deferral, in its opening, its Operator marks table and its Deferred directives section; the opening now states the deferral with its published form. A search of `README.md`, every page of `docs/`, `invocation.md`, `checks.md`, `fixtures/README.md`, the example drawings and the eval README for an arrow directive, `[→`, `[¬→` and the Unicode-block rule found only statements that an arrow label is refused, and the glossary's `arrow` entry that defines it as refused. No page describes an arrow directive. Result: held. Observes AC17.

## T2 Make Check

`make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`, after `git fetch origin engineering`: the documents, links, layout and vocabulary checks are ok and 515 fixtures pass. Result: held. Observes AC17.
