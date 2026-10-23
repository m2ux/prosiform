# Documentation

The documentation this repository owns, published with the build.

- [Diagram Renderer](diagram-renderer.md) — render one Markdown entry document and its dependencies, with optional compact content.

- [Glossary](glossary.md) — every term the contract uses, defined once. The design, the acceptance criteria, the fixture corpus and the tool's diagnostics draw their vocabulary from it.
- [Corpus vocabulary](corpus-vocabulary.md) — the words the fixture corpus's declarations and the conformance report's entries state that the contract's own vocabulary does not. The independence check admits a claim stating these and reports every other word.
- [Versioning](versioning.md) — what the contract's and each build's version numbers assert, how a major, a minor and a patch are told apart, and why a build's major and minor are the contract revision it implements.
- [The output budget, measured](output-budget.md) — the bundled size of the closure the proposal measured, recorded against the configured output budget, with the procedure that re-takes it.

The behavioural contract is declared by the [fixture corpus](../fixtures/README.md). The design it implements is the [captured source settings contract](https://github.com/m2ux/prosiform/blob/a35cb50522c509cd79f57f53095f8d2481eb722d/artifacts/planning/2026-10-23-218-i01-e06-w03-captured-source-settings/design.md).
