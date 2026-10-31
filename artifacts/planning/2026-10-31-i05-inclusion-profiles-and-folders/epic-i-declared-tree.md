## Overview

The example tree and every corpus source declare their settings in presets. This epic lands last, once every field rule it migrates to is settled, so the largest single edit in the initiative does not sit on the critical path of the epics that decide what it migrates to.

## Problem

A forty-four-file edit was a row of the epic that defined the fields it writes.

- **It gated the epic it sat in.** `E01:W08` depended on that epic's third row and on Declared Inclusion's sixth, which pulled it to level 4 and put a bulk edit inside the chain that defines the preset model.
- **Its content depends on every epic here.** The tree's frontmatter must satisfy the inclusion rule, the preset shape, the `group-depth` list and the exclusion entry — so a row inside one epic will be edited by each later one until the last lands.
- **It is one mechanical change, done once.** No field rule changes during it; the whole epic is a rewrite of declarations and a proof that the published bundles are unchanged.
- **A failure here is unambiguous.** If an expected bundle changes, a field moved rather than a spelling, and that is a finding against whichever epic owns the field.

## Proposal

- **The epic is the migration and nothing else.** Every document in `example/` and every corpus source states its settings in a preset, declares no `group` and no `root`, and the published bundles are byte-identical.
- **It depends on the epics that define the fields, not on the rows.** The tree is rewritten once its last field rule has landed, so this epic names the five epics it follows.
- **The proof is the diff.** A changed expected bundle fails the run, so the epic is complete exactly when `make corpus` and `make examples` pass with unmodified expectations.
- **The check that reads the declarations is rewritten here.** `checks/authoring.py`'s root reader went with Declared Inclusion; its group reader follows the same field and lands with the tree.
- **The eval tree follows the same rule.** The diagram-following workflow documents declare to be included, and their forms must still bundle.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | The example tree declares presets, in one edit | AC1, AC4, AC6 | [I08:E00](https://github.com/m2ux/prosiform/issues/434), [I08:E01](https://github.com/m2ux/prosiform/issues/436), [I08:E02](https://github.com/m2ux/prosiform/issues/445) | | |
| W01 | The corpus sources declare presets | AC2 | W00 | | |
| W02 | The eval workflow tree declares | AC3 | W01 | | |
| W03 | The checks that read a declaration | AC5 | W02 | | |

## Acceptance Criteria

- [ ] **AC1.** Every document in the example tree declares its settings in a preset, declares no `group` and no `root`, and the published example bundles are unchanged, as `make corpus` and `make examples` show.
- [ ] **AC2.** Every corpus source declares its settings in a preset, and every fixture's expected bundle is unchanged, as `make corpus` shows.
- [ ] **AC3.** Every document in the diagram-following eval's workflow tree declares `prosiform`, and every form still bundles, as `make harness` shows.
- [ ] **AC4.** A document declaring `group` or `root` fails the run, so the migration is complete rather than partial, as the corpus fixtures over those refusals show.
- [ ] **AC5.** The checks reading a declaration read the preset shape, and no check reads a retired field, as `make authoring` and `make steps` show.
- [ ] **AC6.** Every document in the example tree declares `prosiform` and none declares a root, as `make authoring` shows.

## References

- **R0.** Epic — [I08:E09 The Declared Tree](https://github.com/m2ux/prosiform/issues/465).
- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions and the epics whose fields this migrates to.
