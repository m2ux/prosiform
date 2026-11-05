## Overview

A skill author, human or agent, can take an established programming paradigm — SOLID, traits, polymorphism, inheritance and composition, contracts, concurrency, staging — and find the pattern that realises it in prosiform's grammar, on a page whose specimen the build compiles and checks. The goal the reviews test against is that catalogue: one template, every specimen held by `make check`, an index mapping each SOLID principle to the grammar, and every limit a pattern meets raised as an issue.

## Problem

An author can learn what each feature does, but not how to combine features into a skill with a structure.

- **The documentation describes one feature at a time.**
  The [documentation index](https://github.com/m2ux/prosiform/blob/b9a711e40724ba9feb2a75b7dcab5581a5150aa0/docs/README.md#L7) gives each of its 14 pages one part of a run, and none names a design pattern, a paradigm or a way to combine features.
- **The one worked composition is leaving.**
  The [README's usage](https://github.com/m2ux/prosiform/blob/b9a711e40724ba9feb2a75b7dcab5581a5150aa0/README.md#L65-L71) and [invocation](https://github.com/m2ux/prosiform/blob/b9a711e40724ba9feb2a75b7dcab5581a5150aa0/invocation.md#L45) compile `example/work-planner`, a 95-file tree that [#465](https://github.com/m2ux/prosiform/issues/465) removes.
- **A skill states its architecture as private rules.**
  Work Planner states its [layering](https://github.com/m2ux/workflow-server/blob/785a5ee8c715b802498aa41712e0489425a22cfa/skills/work-planner/SKILL.md#L75-L76) and spends [117 lines](https://github.com/m2ux/workflow-server/blob/785a5ee8c715b802498aa41712e0489425a22cfa/skills/work-planner/guidelines.md#L84-L200) on mode, protocol and artifact shapes, with no shared pattern to cite.
- **The paradigms the grammar affords have no names.** Nothing names:
  - a [preset](https://github.com/m2ux/prosiform/blob/b9a711e40724ba9feb2a75b7dcab5581a5150aa0/docs/sources.md#L48) whose `subst` the linking section's title selects, which binds a callee at its call site;
  - the [operators](https://github.com/m2ux/prosiform/blob/b9a711e40724ba9feb2a75b7dcab5581a5150aa0/docs/references.md#L59-L67), which stage what a later run or a sub-agent compiles;
  - [diagram links](https://github.com/m2ux/prosiform/blob/b9a711e40724ba9feb2a75b7dcab5581a5150aa0/docs/references.md#L97), which carry the procedure each node names.

## Proposal

- **A catalogue under `docs/patterns/`.**
  One page per pattern and an index, each declaring `prosiform`, so a reader browses them and an agent compiles one with `pf`.
- **One template, held by a check.**
  Intent, Paradigm with a citation, Grammar, Structure, Specimen, Consequences and Related, in that order; a page check fails `make check` on a page that departs.
- **Every specimen compiled.**
  A tree beside each page compiles to an expected bundle set committed with it; a bundle check fails `make check` on any difference.
- **An index with a SOLID map.**
  Each principle names the grammar features that serve it; each family's section lists its pages with the principles each serves.
- **Four families.**
  Structure and contracts; polymorphism and substitution; composition and reuse; flow, concurrency and staging.
- **A limit becomes an issue.**
  A limit a pattern meets is stated under the page's `Limits` and raised as a standalone issue, which the page links.
- **The grammar as it will stand.**
  The catalogue starts once the argument-surface and grouping work has closed, and documents the grammar that work leaves.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/527) | Catalogue Foundation | AC1, AC2, AC3, AC4, AC5, AC7 | | |
| [E01](https://github.com/m2ux/prosiform/issues/528) | Structure and Contracts | AC4, AC6 | | |
| [E02](https://github.com/m2ux/prosiform/issues/529) | Polymorphism and Substitution | AC4, AC6 | | |
| [E03](https://github.com/m2ux/prosiform/issues/530) | Composition and Reuse | AC4, AC6 | | |
| [E04](https://github.com/m2ux/prosiform/issues/531) | Flow and Concurrency | AC4, AC6 | | |

## Acceptance Criteria

- [ ] **AC1.** Every pattern page cites the paradigm it realises and links the documentation of the grammar it uses, as `make check` shows.
- [ ] **AC2.** Every pattern page carries the template's sections in order, as `make check` shows.
- [ ] **AC3.** Every pattern's specimen compiles to its committed expected bundle set, and a specimen whose bundle set changes fails `make check`, as the bundle check's tests show.
- [ ] **AC4.** The catalogue index maps each SOLID principle to the grammar features that serve it, and each pattern page to the principles it serves, as `make links` and a read of the index show.
- [ ] **AC5.** Every limit a pattern page states links the issue raised for it, as `make check` shows.
- [ ] **AC6.** The catalogue index lists pattern pages under each of structure and contracts, polymorphism and substitution, composition and reuse, and flow, concurrency and staging, as a read of the index and `make links` show.

- [ ] **AC7.** Every pattern page compiles under `pf`, as `make check` shows.

## Non-Goals

- It changes no grammar or compiler behaviour.
- It runs no live agent-following session; a specimen is proven by compilation alone.
- It neither uses nor maintains `example/work-planner`.
- It documents no grammar before the argument-surface and grouping work closes, and no form that work retires.
- It does not derive a procedure's input and output contract from the references it carries.
- It does not replace the documentation pages that define each feature.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-526-i12-design-patterns) — the work items, the goal trace, the dependency check and the decisions.
- **R2.** [Traits: Composable Units of Behaviour](https://scg.unibe.ch/archive/phd/schaerli-phd.pdf) — the flattening property and conflict rules the composition patterns cite.
- **R3.** [Solid Relevance](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html) — the five SOLID principles stated for modules rather than classes, which the SOLID map follows.
- **R4.** [DITA 1.3 Architectural Specification](https://dita-lang.org/1.3/dita/archspec/base/conref-overview) — conref, keyref and conditional processing, the closest prior art in documentation reuse.
- **R5.** [A Prompt Pattern Catalog](https://arxiv.org/abs/2302.11382) — a pattern catalogue for prompt authoring, and the lean template it uses.
