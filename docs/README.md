# Documentation

The documentation this repository owns, published with the build.

## Architecture

Each page covers one part of a run, and they read in the order a run happens.

| Page | Answers |
| --- | --- |
| [Contract design](https://github.com/m2ux/prosiform/blob/2f8d860e8/artifacts/planning/2026-10-17-prosiform-v1/design.md) | The pinned contract implemented by this build, including explicit link-title preset selection |
| [Architecture](architecture.md) | The whole run, and where each of the pages below fits |
| [Sources](sources.md) | What a source is, how its declaration and presets include it, and the boundary its links derive |
| [References](references.md) | Which links are dependencies, which are text, and what an operator states |
| [Selection](selection.md) | How the closure is reached, which presets are in force, how a `subst` pair redirects a link, and how the closure is consolidated and ordered |
| [Hierarchy](hierarchy.md) | File headings, groups, member names and the level shift |
| [Composition](composition.md) | How a directive places a section beneath the section that writes it, and the grammar it is written in |
| [Destinations](destinations.md) | How a heading is named and how each link is rewritten |
| [Dispatch](dispatch.md) | How dispatched material becomes a bundle of its own |
| [Bundles](bundles.md) | The bundle set, derived names, publication, the output folder and delivery |
| [Validation](validation.md) | The invariants a bundle is held to, the diagnostics and the budgets |

## Reference

| Page | What it is |
| --- | --- |
| [Invocation](../invocation.md) | The command line, its options and its exit statuses |
| [Fixture corpus](../fixtures/README.md) | The behavioural contract, stated as cases |
| [Glossary](glossary.md) | Every term the contract uses, defined once |
| [Versioning](versioning.md) | What the contract's and each build's version numbers assert |
| [Diagram Renderer](diagram-renderer.md) | Draw the files one entry reads beside the bundles it writes, and re-render the architecture pages' examples |
| [Output budget](output-budget.md) | What each named budget bounds, the bundled size of a measured closure, and how to re-take it |

## Commands

[Checks](../checks.md) states each target the [`Makefile`](../Makefile) declares and what it asserts. `make check` runs the set, stopping at the first failure.
