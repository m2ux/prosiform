## Overview

One document can state independent local component and test choice groups, while ordinary presets remain additive and fixture stubs retain their existing role. The compiler validates each relevant axis and preserves the complete binding through any published pick.

## Problem

- Independent component and test selections are not represented as separately named exclusive axes in one document.
- Cardinality, conflicts, briefs and deferred or dispatched picks must remain local and observable as grouping becomes explicit.

## Proposal

- **Local group identity.**
  The proposed choice-group field names an alternative's local exclusive axis. An alternative without a name belongs to that document's single unnamed group; this is one group model, not a second selection path. The layout group field keeps its existing meaning.
- **Independent cardinality.**
  Every group affecting selected content or the entry map has one alternative in force. Ordinary presets are additive and entry stubs remain optional. A public synthetic component/test source demonstrates the actual two-axis use.
- **Bounded picking.**
  Explicit tags may select one member of each group. A pick token may leave one relevant group unresolved while other groups are explicit; several unresolved groups fail with grouped remedies rather than generating a Cartesian pick tree. Existing brief-independence, deferral and dispatch rules remain in force.
- **Observable configuration.**
  The manifest names local groups, chosen alternatives and their origins. Generic source/corpus controls establish valid and refused combinations before any bounded agent observation.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e02/w00.md) | Two-axis contract and frozen controls | AC1 | [E01:W00](https://github.com/m2ux/prosiform/issues/869) | | | |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e02/w01.md) | Local group resolver and cardinality | AC2, AC3 | W00, [E01:W02](https://github.com/m2ux/prosiform/issues/869) | | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e02/w02.md) | Pick dispatch deferral and manifest | AC4 | W01 | | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e02/w03.md) | Public two-axis example and guide | AC5 | W02, [E01:W03](https://github.com/m2ux/prosiform/issues/869) | | | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e02/w04.md) | Bounded changed-pick mechanism evidence | AC6 | W03 | | | |

## Acceptance Criteria

- [ ] **AC1.** A public synthetic component/test source establishes independent local exclusive axes and their valid/invalid selections against the frozen baseline, as the contract/specimen review shows.
- [ ] **AC2.** A build selects one alternative in every relevant local group while preserving ordinary and stub scope, as the group-selection corpus shows.
- [ ] **AC3.** The local resolution service identifies missing and conflicting selections in each relevant group, as its negative matrix shows.
- [ ] **AC4.** Published dispatches, deferrals, briefs and manifests preserve fixed and chosen groups, while multiple unresolved groups refuse publication, as integration fixtures and make check show.
- [ ] **AC5.** The public contract and executable two-axis example describe the delivered selection and pick behavior, as documentation and corpus checks show.
- [ ] **AC6.** A representative changed pick mechanism has a predeclared observation bounded to four fresh contexts, with remaining combinations covered by the deterministic binding matrix and unchanged paths by exact bundle equivalence, as the changed-behavior record shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture) — group semantics, controls and bounded observation plan.
- **R2.** [Declared Alternatives](https://github.com/m2ux/prosiform/issues/708) — the existing local choice and refusal contract.
- **R3.** [Dispatch Picks](https://github.com/m2ux/prosiform/issues/774) — existing pick publication and caller responsibility.
- **R4.** [Real-Use Eval](https://github.com/m2ux/prosiform/issues/734) — the existing evaluation owner; this work adds only its bounded feature specimen, not a replacement baseline.
