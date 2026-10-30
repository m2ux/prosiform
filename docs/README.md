# Documentation

The documentation this repository owns, published with the build.

## Architecture

Each page covers one part of a run, and they read in the order a run happens.

| Page | Answers |
| --- | --- |
| [Concept](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md) | The original design concept |
| [Architecture](architecture.md) | The whole run, and where each of the pages below fits |
| [Sources](sources.md) | What a source is, how its root confines it, and what its frontmatter declares |
| [References](references.md) | Which links are dependencies, which are text, and what an operator states |
| [Selection](selection.md) | How the closure is reached, consolidated and ordered |
| [Hierarchy](hierarchy.md) | File headings, groups, member names and the level shift |
| [Destinations](destinations.md) | How a heading is named and how each link is rewritten |
| [Dispatch](dispatch.md) | How dispatched material becomes a bundle of its own |
| [Bundles](bundles.md) | Derived names, publication and delivery |
| [Checking](checking.md) | The invariants, the diagnostics and the budgets checked by [Makefile](../Makefile) |

## Reference

| Page | What it is |
| --- | --- |
| [Invocation](../invocation.md) | The command line, its options and its exit statuses |
| [Fixture corpus](../fixtures/README.md) | The behavioural contract, stated as cases |
| [Glossary](glossary.md) | Every term the contract uses, defined once |
| [Versioning](versioning.md) | What the contract's and each build's version numbers assert |
| [Diagram Renderer](diagram-renderer.md) | Render one entry and its dependencies as a diagram |
| [Output budget](output-budget.md) | The bundled size of a measured closure, and how to re-take it |

## Commands

[Checks](../checks.md) states each target the  declares and what it asserts. `make check` runs the set, stopping at the first failure.
