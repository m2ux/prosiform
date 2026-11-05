## Overview

This epic writes the patterns that express control flow, concurrency and staging: a linked flowchart, a sequence protocol, a dispatched command, a fork-join set and staged compilation. Each is a page under the catalogue's template with a specimen the build compiles, and the family's section of the index lists them.

## Problem

- **Diagram links are documented as syntax.**
  [Diagram links](https://github.com/m2ux/prosiform/blob/b9a711e40724ba9feb2a75b7dcab5581a5150aa0/docs/references.md#L97) lists the link lines a diagram may write, and not that a flowchart so linked is a program whose steps the bundle carries.
- **Dispatch is documented as output.**
  [Dispatch](https://github.com/m2ux/prosiform/blob/b9a711e40724ba9feb2a75b7dcab5581a5150aa0/docs/dispatch.md) states the bundles a run writes, and not the command, actor and fork-join forms an author builds from them.
- **Deferral is documented as a mark.**
  A deferral compiles its target in a later run, which is staging, and no page says so.

## Proposal

- **Linked Flowchart.**
  A flowchart's nodes click to procedure sections, so the network stands outside the procedures and the bundle carries each one.
- **Sequence Protocol.**
  A sequence diagram's participants link the artifacts taking part, so the protocol and its parties travel together.
- **Dispatched Command.**
  A dispatch hands a sub-agent a bundle of its own, the request reified as a command and answered as an actor answers.
- **Fork-Join Set.**
  A parallel set starts its bundles together, and the section after it joins their reports.
- **Staged Compilation.**
  A deferral leaves its target to a later run, so a first stage compiles what is known now.
- **Boundary.**
  The structure a skill takes belongs to the structure family; a facade's deferrals are that family's, and this family states staging as such.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| W01 | Linked Flowchart page and specimen | AC1 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W02 | Sequence Protocol page and specimen | AC2 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W03 | Dispatched Command page and specimen | AC3 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W04 | Fork-Join Set page and specimen | AC4 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W05 | Staged Compilation page and specimen | AC5 | [E00:W05](https://github.com/m2ux/prosiform/issues/527) | | | |
| W06 | Family section of the catalogue index | AC6 | W01, W02, W03, W04, W05, [E00:W03](https://github.com/m2ux/prosiform/issues/527) | | | |

## Acceptance Criteria

- [ ] **AC1.** The Linked Flowchart specimen compiles to a bundle carrying each node's procedure section, every click rewritten to that section, as its committed bundle set, held by `make check`, shows.
- [ ] **AC2.** The Sequence Protocol specimen compiles to a bundle carrying each participant's artifact, every menu destination rewritten to it, as its committed bundle set, held by `make check`, shows.
- [ ] **AC3.** The Dispatched Command specimen compiles to a bundle set whose entry bundle carries a dispatch sub-section naming the review's own bundle, which the set holds, as its committed bundle set, held by `make check`, shows.
- [ ] **AC4.** The Fork-Join Set specimen compiles to a bundle set whose entry carries one parallel dispatch sub-section listing three review bundles, which the set holds, as its committed bundle set, held by `make check`, shows.
- [ ] **AC5.** The Staged Compilation specimen compiles to a first-stage bundle carrying the deferred target's path and none of its content, and a second-stage bundle carrying that target, as its committed bundle sets, held by `make check`, show.
- [ ] **AC6.** The catalogue index's flow-concurrency-and-staging section lists each of the family's pages with the paradigm it realises and, in its Principles column, the SOLID principles it serves, as `make links` and a read of the index show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-526-i12-design-patterns) — the work items, the decisions and the dependency check.
- **R2.** [Communicating Sequential Processes](https://dl.acm.org/doi/10.1145/359576.359585) — parallel composition, which the Fork-Join Set and Sequence Protocol pages cite.
