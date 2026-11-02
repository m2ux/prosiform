## Overview

The example tree is removed, and every corpus source and eval workflow document declares its settings in presets. This epic lands last, once every field rule it migrates to is settled, so the bulk edits in the initiative do not sit on the critical path of the epics that decide what they migrate to.

## Problem

A tree the build compiles holds settings stated outside presets, and one tree costs upkeep that nothing reads.

- **The example tree is stale and unmaintained.**
  `example/work-planner` copies a skill that has moved on, so every field rule needs a rewrite of a tree nobody reads, and a check or fixture holding to it proves nothing current.
- **Checks and fixtures are built on it.**
  `make steps`, `make authoring`, `make boundary`, `make examples` and the `usage-example` fixtures read that tree alone, and `scripts/examples.json` renders diagrams from it.
- **The corpus and eval trees must declare.**
  Their frontmatter must satisfy the inclusion rule, the preset shape, and the `group` and `subst` entries, so an edit inside one epic is redone by each later one until the last lands.
- **A failure here is unambiguous.**
  If an expected bundle changes, a field moved rather than a spelling, and that is a finding against whichever epic owns the field.

## Proposal

- **The example tree is removed, and stays reachable from history.**
  An annotated tag `archive/example-work-planner` names the last commit holding `example/work-planner`, so `git show archive/example-work-planner:example/work-planner/...` and the tree link at that tag still read it.
- **Everything built on the tree goes with it.**
  `example/`, its `scripts/examples.json` entries, the regenerated diagrams, the `make` targets and checks that build or read it, the `usage-example` fixtures and every doc naming it.
- **The corpus and eval trees migrate once.**
  Every corpus source and every diagram-following workflow document states its settings in a preset, once its last field rule has landed.
- **The proof is the diff.**
  A changed expected bundle fails the run, so the migration is complete exactly when `make corpus` and `make harness` pass with unmodified expectations.
- **The checks read the preset shape.**
  A check reading a declaration reads a preset's entries, and none reads a retired field.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | The example tree and its checks removed | AC1, AC4, AC6 | | | |
| W01 | The corpus sources declare presets | AC2 | W00, [I08:E06:W03](https://github.com/m2ux/prosiform/issues/461) | | |
| W02 | The eval workflow tree declares | AC3 | W01 | | |
| W03 | The checks that read a declaration | AC5 | W02 | | |

## Acceptance Criteria

- [ ] **AC1.** No file in the repository holds or names the example tree: no `example/` directory, `scripts/examples.json` entry, rendered example diagram, fixture, check, `make` target or document, as a search of the repository at the merged revision shows.
- [ ] **AC2.** Every corpus source declares its settings in a preset, and every fixture's expected bundle is unchanged, as `make corpus` shows.
- [ ] **AC3.** Every document in the diagram-following eval's workflow tree declares `prosiform`, and every form still bundles, as `make harness` shows.
- [ ] **AC4.** Every check the repository runs passes with the example tree removed, as `make check` shows.
- [ ] **AC5.** The checks reading a declaration read the preset shape, and no check reads a retired field, as `make check` and a search of `checks/` for the retired fields show.
- [ ] **AC6.** The annotated tag `archive/example-work-planner` names the parent of the commit that removes `example/work-planner`, so the tree reads from the tag, as `git show archive/example-work-planner:example/work-planner/SKILL.md` and `git rev-parse` of the tag and that parent show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions and the epics whose fields this migrates to.
