## Overview

This epic lays the ground every pattern page stands on: a page check and a bundle check that hold each page and specimen in `make check`, the catalogue index with its SOLID map and one section per family, its link from the documentation index, and Shared Rule as the first page, which proves the template end to end before any family starts.

## Problem

- **No check reads a usage page.**
  `make links` resolves links and `make corpus` holds the contract, but nothing holds a page's sections or a specimen's bundle.
- **No index or map exists.**
  The [documentation index](https://github.com/m2ux/prosiform/blob/b9a711e40724ba9feb2a75b7dcab5581a5150aa0/docs/README.md) lists architecture and reference pages only.
- **A template no page has passed is a guess.**
  A family written against an unproven template rewrites its pages when the first one fails.

## Proposal

- **A page check.**
  `make pattern-pages` holds each page to the template's sections in order, a cited paradigm, linked grammar documentation and an issue link for each stated limit.
- **A bundle check.**
  `make pattern-bundles` compiles every page and every specimen with the build under test, and fails on any difference from the specimen's committed bundle set.
- **A specimen is linked by a deferral.**
  A page's `Specimen` section links its entry with a deferral, so compiling the page carries the page alone and the link stays followable.
- **The index.**
  `docs/patterns/README.md` holds the SOLID map from each principle to the grammar features that serve it, and one section per family; the documentation index links it.
- **Shared Rule first.**
  The pattern resting on delivered grammar alone is written first, so the template and both checks are proven on a real page.
- **It waits for the grammar to settle.**
  The checks and the index start once the argument-surface work ([#462](https://github.com/m2ux/prosiform/issues/462)) and the grouping work ([#463](https://github.com/m2ux/prosiform/issues/463)) have closed.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| W01 | Pattern page check | AC1, AC2, AC3 | #462, #463 | | | |
| W02 | Page and specimen bundle check | AC4, AC5 | #462, #463 | | | |
| W03 | Catalogue index and SOLID map | AC6 | #462, #463 | W04 | | |
| W04 | Documentation index links the catalogue | AC7 | | W03 | | |
| W05 | Shared Rule page and specimen | AC8 | W01, W02 | | | |

## Acceptance Criteria

- [ ] **AC1.** A pattern page lacking a template section, or carrying the sections out of order, fails `make check`, naming the page and the section, as the page check's tests show.
- [ ] **AC2.** A pattern page whose `Paradigm` cites no external source, or whose `Grammar` links no documentation page, fails `make check`, as the page check's tests show.
- [ ] **AC3.** A limit a pattern page states under `Consequences` with no link to an issue of this repository fails `make check`, as the page check's tests show.
- [ ] **AC4.** A pattern page or catalogue index that `pf` refuses fails `make check`, as the bundle check's tests show.
- [ ] **AC5.** A specimen whose compiled bundle set differs from its committed set fails `make check`, naming the specimen, the file and the first differing line, as the bundle check's tests show.
- [ ] **AC6.** The catalogue index maps each SOLID principle to the grammar features that serve it, each feature linked to its documentation section, as `make links` and a read of the index show.
- [ ] **AC7.** The documentation index links the pattern catalogue, as `make links` shows.
- [ ] **AC8.** The Shared Rule specimen's two procedures link one rule section and compile to a bundle carrying that section once, both links pointing at it, as its committed bundle set, held by `make check`, shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-526-i12-design-patterns) — the work items, the decisions and the dependency check.
