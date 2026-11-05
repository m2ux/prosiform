## Overview

This epic writes the patterns that bind one procedure to different material: a generic procedure instantiated per subject, dispatch chosen by the calling section, an injected strategy, a hook section, a null object, a test double and the structural conformance a substitute must keep. Each is a page under the catalogue's template with a specimen the build compiles, and the family's section of the index lists them.

## Problem

- **Call-site binding is unnamed.**
  A [preset](https://github.com/m2ux/prosiform/blob/b9a711e40724ba9feb2a75b7dcab5581a5150aa0/docs/sources.md#L48) the linking section's title selects can carry a `subst`, so the caller decides what a callee's links reach, and no page calls that injection or polymorphism.
- **Substitution is documented as a mechanism.**
  The documentation states what `subst` redirects, not the strategy, template method, null object or test double an author builds from it.
- **What a substitute must carry is implicit.**
  A fragment the substitute lacks fails the run, which is a structural check nobody describes as Liskov substitution.

## Proposal

- **Generic Procedure.**
  Two caller sections select two presets of one procedure, each substituting its subject, so one run carries an instance per subject.
- **Call-Site Dispatch.**
  A caller's title selects several presets of a callee, whose settings union, as multiple dispatch combines arguments.
- **Injected Strategy.**
  A procedure links a port; presets substitute adapters; the entry is the composition root.
- **Hook Section.**
  A section-keyed `subst` replaces one hook of a base procedure, as a template method's subclass fills a step.
- **Null Object.**
  A hook substituted by a section stating no action replaces a conditional skip.
- **Test Double.**
  A test preset substitutes a stub for a side-effecting dependency.
- **Structural Conformance.**
  A substitute carries every heading its callers name by fragment, as a structure ascribes to a signature.
- **Boundary.**
  The structure a skill takes belongs to the structure family; combining sections without copies belongs to the composition family.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| W01 | Generic Procedure page and specimen | AC1 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W02 | Call-Site Dispatch page and specimen | AC2 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W03 | Injected Strategy page and specimen | AC3 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W04 | Hook Section page and specimen | AC4 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W05 | Null Object page and specimen | AC5 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W06 | Test Double page and specimen | AC6 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W07 | Structural Conformance page and specimen | AC7 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W08 | Family section of the catalogue index | AC8 | W01, W02, W03, W04, W05, W06, W07, [E00:W03](https://github.com/m2ux/prosiform/issues/527) | | | |

## Acceptance Criteria

- [ ] **AC1.** The Generic Procedure specimen compiles one procedure under two presets to a bundle carrying an instance per subject, each instance's subject link reaching its own subject, as its committed bundle set, held by `make check`, shows.
- [ ] **AC2.** The Call-Site Dispatch specimen's caller title selects two presets of one callee and compiles to a bundle placing the callee by the one's `group` pair and redirecting it by the other's `subst`, as its committed bundle set, held by `make check`, shows.
- [ ] **AC3.** The Injected Strategy specimen's entry selects the safe adapter and compiles to a bundle carrying it in place of the port, and not the fast adapter, as its committed bundle set, held by `make check`, shows.
- [ ] **AC4.** The Hook Section specimen compiles to a bundle carrying the replacement for its redirected hook and the base's own section for every other hook, as its committed bundle set, held by `make check`, shows.
- [ ] **AC5.** The Null Object specimen compiles to a bundle in which the audit step's link reaches the no-op section, as its committed bundle set, held by `make check`, shows.
- [ ] **AC6.** The Test Double specimen compiles under its test preset to a bundle carrying the stub tracker in place of the real one, as its committed bundle set, held by `make check`, shows.
- [ ] **AC7.** The Structural Conformance specimen compiles to a bundle in which each section its callers name by fragment resolves to the substitute, as its committed bundle set, held by `make check`, shows.
- [ ] **AC8.** The catalogue index's polymorphism-and-substitution section lists each of the family's pages with the paradigm it realises and, in its Principles column, the SOLID principles it serves, as `make links` and a read of the index show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-526-i12-design-patterns) — the work items, the decisions and the dependency check.
- **R2.** [On Understanding Types, Data Abstraction, and Polymorphism](https://classes.cs.uchicago.edu/archive/2012/spring/22300-1/papers/Cardelli-Wegner.pdf) — the kinds of polymorphism the family's pages place themselves among.
