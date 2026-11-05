## Overview

This epic writes the patterns that give a skill its structure: an artifact owning its data and operations, a contract composed apart from its implementation, a role interface, a facade entry and layered calls. Each is a page under the catalogue's template with a specimen the build compiles, and the family's section of the index lists them.

## Problem

- **A skill's shape is stated as private rules.**
  Work Planner states its [layering](https://github.com/m2ux/workflow-server/blob/785a5ee8c715b802498aa41712e0489425a22cfa/skills/work-planner/SKILL.md#L75-L76) and its artifact and mode shapes for itself, so another skill re-derives them.
- **Nothing shows a contract apart from its body.**
  A link to an operation carries its whole section; composing a contract while deferring its body is grammar no page demonstrates.
- **Narrow links are a choice nobody explains.**
  Section selection lets a caller depend on one section, and no page says why that is interface segregation.

## Proposal

- **Artifact.**
  An artifact's Fields hold its data and its Operations its procedures; a mode binds artifacts and calls operations by heading link, as DCI's context does.
- **Contract and Implementation.**
  A step composes each called operation's contract section while a deferral withholds the body, as a signature stands apart from its structure.
- **Role Interface.**
  Each consumer links the section it uses rather than the whole document.
- **Facade Entry.**
  One entry names the modes it fronts by deferral, so its bundle stays small and each mode compiles in its own run.
- **Layered Calls.**
  Each layer's documents declare that layer's group, so the bundle's divisions stand in layer order.
- **Boundary.**
  Substituting what a link reaches belongs to the polymorphism family; combining sections without copies belongs to the composition family.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| W01 | Artifact page and specimen | AC1 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W02 | Contract and Implementation page and specimen | AC2 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W03 | Role Interface page and specimen | AC3 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W04 | Facade Entry page and specimen | AC4 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W05 | Layered Calls page and specimen | AC5 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W06 | Family section of the catalogue index | AC6 | W01, W02, W03, W04, W05, [E00:W03](https://github.com/m2ux/prosiform/issues/527) | | | |

## Acceptance Criteria

- [ ] **AC1.** The Artifact specimen's mode calls two of an artifact's three operations by heading link and compiles to a bundle carrying those two and the Fields section they link, and not the third, as its committed bundle set, held by `make check`, shows.
- [ ] **AC2.** The Contract and Implementation specimen compiles to a bundle whose step carries one composed contract section, each called operation's contract beneath its own parent's name, and neither operation's body, as its committed bundle set, held by `make check`, shows.
- [ ] **AC3.** The Role Interface specimen's two consumers compile to two bundles, each carrying only the section its consumer names and the ancestors placing it, as their committed bundle sets, held by `make check`, show.
- [ ] **AC4.** The Facade Entry specimen's entry compiles to a bundle carrying neither mode it names, each linked by the path its own run compiles, as its committed bundle set, held by `make check`, shows.
- [ ] **AC5.** The Layered Calls specimen compiles to a bundle with one division per layer, in the order modes, protocols, artifacts, as its committed bundle set, held by `make check`, shows.
- [ ] **AC6.** The catalogue index's structure-and-contracts section lists each of the family's pages with the paradigm it realises and, in its Principles column, the SOLID principles it serves, as `make links` and a read of the index show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-526-i12-design-patterns) — the work items, the decisions and the dependency check.
- **R2.** [The DCI Architecture](https://www.artima.com/articles/the-dci-architecture-a-new-vision-of-object-oriented-programming) — data, context and interaction, which the Artifact pattern follows.
