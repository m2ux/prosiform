## Overview

This epic writes the patterns that combine sections without copying them: a trait group whose conflicts stay visible, a composite outline built from the leaves up, a decorator section and a prototype override. Each is a page under the catalogue's template with a specimen the build compiles, and the family's section of the index lists them with the Shared Rule page.

## Problem

- **Reuse by link is described as arrangement.**
  [Hierarchy](https://github.com/m2ux/prosiform/blob/b9a711e40724ba9feb2a75b7dcab5581a5150aa0/docs/hierarchy.md) states how merged groups, variants and members are emitted, and not that they are trait composition with its conflicts kept.
- **Override without inheritance has no worked form.**
  An author who wants a variant of a procedure copies it, where linking the base's sections and writing only the difference would serve.
- **Wrapping a section is new grammar.**
  Section composition places a referenced section beneath its caller's heading, and no page shows it adding rules around what it wraps.

## Proposal

- **Trait Group.**
  Two documents declaring one group contribute one section each; the bundle keeps both as attributed variants, where a trait system would demand a resolution.
- **Composite Outline.**
  Each file's `group` pair places its own sections, and a parent merges its children's results, as a composite builds a whole from parts.
- **Decorator Section.**
  A section states its own rules and composes the wrapped section beneath them.
- **Prototype Override.**
  A variant writes the sections it changes and links the base's others, as a prototype delegates what it does not override.
- **Boundary.**
  Substituting what a link reaches belongs to the polymorphism family; the Shared Rule page is the foundation's, and this family's index section lists it.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| W01 | Trait Group page and specimen | AC1 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W02 | Composite Outline page and specimen | AC2 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W03 | Decorator Section page and specimen | AC3 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W04 | Prototype Override page and specimen | AC4 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W05 | Family section of the catalogue index | AC5 | W01, W02, W03, W04, [E00:W03](https://github.com/m2ux/prosiform/issues/527) | | | |

## Acceptance Criteria

- [ ] **AC1.** The Trait Group specimen compiles to a bundle in which the section both members contribute is one heading with a variant for each member, as its committed bundle set, held by `make check`, shows.
- [ ] **AC2.** The Composite Outline specimen compiles to a bundle placing the grandchild inside the child's result and the child's inside the parent's, as its committed bundle set, held by `make check`, shows.
- [ ] **AC3.** The Decorator Section specimen compiles to a bundle in which the publish section sits beneath the guard's heading, after the guard's own content, as its committed bundle set, held by `make check`, shows.
- [ ] **AC4.** The Prototype Override specimen compiles to a bundle carrying the variant's own `Verify` and the base's `Prepare` and `Publish`, and not the base's `Verify`, as its committed bundle set, held by `make check`, shows.
- [ ] **AC5.** The catalogue index's composition-and-reuse section lists each of the family's pages, Shared Rule among them, with the paradigm it realises and, in its Principles column, the SOLID principles it serves, as `make links` and a read of the index show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-526-i12-design-patterns) — the work items, the decisions and the dependency check.
- **R2.** [Traits: Composable Units of Behaviour](https://scg.unibe.ch/archive/phd/schaerli-phd.pdf) — the flattening property and conflict rules the Trait Group page cites.
