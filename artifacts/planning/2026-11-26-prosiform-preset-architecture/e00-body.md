## Overview

An operator can request a machine-readable effective-build record alongside the validated bundle set. The record identifies what the compiler selected and why; native execution and transport receipts remain separate evidence.

## Problem

- Effective source hashes, selected regions, presets, substitutions and dispatch configuration are recorded internally or reconstructed by callers without one published result contract.
- A structured build record must share the bundle set's atomic publication and refusal boundary.

## Proposal

- **Explicit output selection.**
  The proposed --manifest option adds build-manifest.json inside the run's bundle-set folder. Without that option, the generated Markdown is identical to the frozen baseline. Check mode validates the same record without publishing it.
- **Recorded compiler facts.**
  The record carries a schema version, compiler/profile identity, source-relative paths and hashes, effective preset names/origins, selected regions, substitutions, brief references, dispatch targets, logical levels, resolved model names and bundle hashes. It asserts no runtime effort, provider observation, delivery or semantic completeness.
- **Atomic publication.**
  The record uses the existing capture/provenance and publication paths; a failure publishes neither a partial manifest nor a mixed bundle set.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e00/w00.md) | Contract and frozen control specimens | AC1 |  | | | |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e00/w01.md) | Manifest model and serialization | AC2 | W00, [#865](https://github.com/m2ux/prosiform/issues/865) | | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e00/w02.md) | CLI publication and failure boundary | AC3, AC4 | W01 | | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e00/w03.md) | Public contract and manifest example | AC5 | W02 | | | |

## Acceptance Criteria

- [ ] **AC1.** The output schema and frozen source/bundle controls state which values are compiler facts and which are outside the record, as the contract/specimen review shows.
- [ ] **AC2.** The requested manifest identifies each output's effective source, selection and dispatch facts deterministically, as run-manifest unit and corpus tests show.
- [ ] **AC3.** Enabling manifest output preserves the baseline Markdown bundle bytes, as paired output-hash fixtures show.
- [ ] **AC4.** Manifest and bundle-set publication share the existing complete-or-refused result boundary, as publication/failure tests and make check show.
- [ ] **AC5.** The public invocation contract and executable example describe and exercise the delivered manifest, as documentation and corpus checks show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture) — scope, schema, frozen controls and work items.
- **R2.** [Publication and delivery](https://github.com/m2ux/prosiform/blob/794922d41465b91deb4edb3a7484506cb8f519cd/docs/bundles.md#publication) — existing publication boundaries.
- **R3.** [Branch Declaration](https://github.com/m2ux/prosiform/issues/865) — the main-branch declaration consumed before implementation delivery readiness; it does not gate planning publication.
