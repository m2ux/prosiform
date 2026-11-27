## Overview

One document can state independent local component and test choice groups, while ordinary presets remain additive and fixture stubs retain their existing role. The bundler validates each relevant axis, preserves the complete binding through any published pick, and lists a document's choices without bundling it.

## Problem

- Independent component and test selections are not represented as separately named exclusive axes in one document.
- Cardinality, conflicts, briefs and deferred or dispatched picks must remain local and observable as grouping becomes explicit.
- A document's presets and alternatives are listed only by the refusal a build without one raises.

## Proposal

- **Local group identity.**
  The proposed choice-group field names an alternative's local exclusive axis. An alternative without a name belongs to that document's single unnamed group, under one group model.
- **A separate layout group.**
  The existing group field keeps its layout meaning.
- **Independent cardinality.**
  Every group affecting selected content or the entry map has one alternative in force. Ordinary presets are additive and entry stubs remain optional.
- **Bounded picking at a dispatch.**
  A pick token may leave one relevant group open while the others are explicit; a dispatch leaving several open fails with a remedy for each, and no Cartesian pick tree is published.
- **One pick for each open group at the entry.**
  The entry's pick option is repeatable, each occurrence naming one member of one open group.
- **Open groups at a deferral.**
  A deferred link names one alternative of each group or a pick token leaving the rest open, since the run bundling it names one pick for each.
- **Unchanged neighbours.**
  Existing brief-independence, deferral and dispatch rules remain in force.
- **Observable configuration.**
  The ledger names local groups, chosen alternatives and their origins.
- **A listing without a build.**
  The proposed `--presets` option prints one document's presets, its alternatives by group with their choice lines, its stubs and its imports with origins.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e03/w00.md) | Two-axis contract and frozen controls | AC1 | [E02:W00](https://github.com/m2ux/prosiform/issues/869) | | 1 | |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e03/w01.md) | Local group resolver and cardinality | AC2, AC3 | W00 | | 2 | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e03/w02.md) | Pick dispatch deferral and ledger | AC4, AC5, AC6 | W01, [E02:W02](https://github.com/m2ux/prosiform/issues/869) | | 1 | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e03/w03.md) | Public two-axis example and guide | AC7 | W02 | | 2 | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e03/w04.md) | Preset listing without bundling | AC8 | W03 | | 2 | |
| [W05](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e03/w05.md) | Bounded changed-pick mechanism evidence | AC9 | W03 | | 1 | |

## Acceptance Criteria

- [ ] **AC1.** A public synthetic component and test source establishes independent local exclusive axes and their valid and invalid selections against the frozen baseline, as the contract and specimen review shows.
- [ ] **AC2.** A build selects one alternative in every relevant local group while preserving ordinary and stub scope, as the group-selection corpus shows.
- [ ] **AC3.** The local resolution service identifies missing and conflicting selections in each relevant group, as its negative matrix shows.
- [ ] **AC4.** Published dispatches, deferrals, briefs and ledgers preserve fixed and chosen groups, as integration fixtures and `make check` show.
- [ ] **AC5.** A dispatch leaving more than one group open is refused with a remedy for each open group, as the refusal fixtures show.
- [ ] **AC6.** An entry leaving several groups open bundles when one `--pick` names a member of each, as the entry-pick fixtures show.
- [ ] **AC7.** The public contract and executable two-axis example describe the delivered selection and pick behavior, as documentation and example checks show.
- [ ] **AC8.** A listing of one document names its presets, its alternatives by choice group and its imports with their origins, publishing nothing, as the listing fixtures show.
- [ ] **AC9.** A representative changed pick mechanism has a predeclared observation bounded to four fresh contexts, with remaining combinations covered by the deterministic binding matrix and unchanged paths by exact bundle equivalence, as the changed-behavior record shows.

## Open Questions

- What a pick naming a member of an already fixed group reports.
- Whether the preset listing is text or TOML.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture) — group semantics, controls and bounded observation plan.
- **R2.** [Declared Alternatives](https://github.com/m2ux/prosiform/issues/708) — the existing local choice and refusal contract.
- **R3.** [Dispatch Picks](https://github.com/m2ux/prosiform/issues/774) — existing pick publication and caller responsibility.
- **R4.** [Real-Use Eval](https://github.com/m2ux/prosiform/issues/734) — the existing evaluation owner; this work adds only its bounded feature specimen, not a replacement baseline.
