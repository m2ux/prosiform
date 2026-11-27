## Overview

An operator can request a machine-readable ledger alongside the validated bundle set, read it without publishing, and hold a published set to it. The ledger identifies what the bundler selected and why; agent execution and transport receipts remain separate evidence.

## Problem

- Effective source hashes, selected regions, presets, substitutions and dispatch configuration are recorded internally or reconstructed by callers, with no published result contract.
- A structured ledger must share the bundle set's atomic publication and refusal boundary.
- A published set carries nothing a later reader can hold its sources and bundles to.

## Proposal

- **Explicit output selection.**
  The proposed `--ledger` option adds one TOML ledger inside the run's bundle-set folder. Without the option, the generated Markdown is identical to the frozen baseline.
- **Recorded build facts.** The ledger carries:
  - a schema version, the build and profile identity and the invocation;
  - source-relative paths and hashes, selected regions, effective presets and their origins;
  - substitutions, brief references, dispatch and deferral targets, levels and resolved model names;
  - the hash of each bundle.
- **Stated exclusions.**
  The ledger asserts no runtime effort, provider observation, delivery or semantic completeness.
- **Atomic publication.**
  The ledger uses the existing capture, provenance and publication paths; a failure publishes neither a partial ledger nor a mixed bundle set.
- **Inspection without publication.**
  A check-mode run with the option writes the same ledger to standard output and publishes nothing.
- **Verification.**
  The proposed `--verify` option re-hashes the sources and bundles a published ledger names and reports each that differs.
- **A published schema.**
  A JSON Schema for the ledger sits with the corpus, which holds each fixture's ledger to it.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e01/w00.md) | Ledger contract and frozen controls | AC1 | [E00:W04](https://github.com/m2ux/prosiform/issues/890) | | 1 | |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e01/w01.md) | Ledger projection and serialization | AC2 | W00 | | 2 | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e01/w02.md) | CLI publication and check mode | AC3, AC4, AC5 | W01 | | 1 | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e01/w03.md) | Public ledger contract and example | AC6 | W02 | | 2 | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e01/w04.md) | Ledger verification of a published set | AC7 | W03 | | 2 | |

## Acceptance Criteria

- [ ] **AC1.** The ledger schema and frozen source and bundle controls state which values are build facts and which are outside the ledger, as the contract and specimen review shows.
- [ ] **AC2.** The requested ledger identifies each output's effective source, selection, dispatch and invocation facts deterministically, as ledger unit and corpus tests show.
- [ ] **AC3.** Enabling ledger output preserves the baseline Markdown bundle bytes, as paired output-hash fixtures show.
- [ ] **AC4.** Ledger and bundle-set publication share the existing complete-or-refused result boundary, as publication and failure tests and `make check` show.
- [ ] **AC5.** A check-mode run with the ledger option writes the ledger to standard output and publishes nothing, as the check-mode fixtures show.
- [ ] **AC6.** The public invocation contract and executable example describe and exercise the delivered ledger, as documentation and corpus checks show.
- [ ] **AC7.** A published set whose source or bundle bytes differ from its `ledger.toml` is reported with the differing path, as the verification fixtures show.

## Open Questions

- Whether the ledger records the warnings a build raises.
- Which code a verification mismatch reports.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture) — scope, ledger design, frozen controls and work items.
- **R2.** [Publication and delivery](https://github.com/m2ux/prosiform/blob/8cedda4cc06b0486168addc05f057161192a22a6/docs/bundles.md#publication) — existing publication boundaries.
