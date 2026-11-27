## Overview

An author can reuse narrowly scoped preset settings and select independent local component and test alternatives, while an operator can inspect the exact effective sources and configuration behind every published bundle. The goal the reviews test against is reproducible, local configuration with readable authored policy, observable selection results and forms accepted from specimen files.

## Problem

Effective configuration is spread across sources, and nothing published relates, reuses, groups or checks it.

- **Effective configuration is reconstructed by hand.**
  Sources, preset selections, substitutions and dispatched bundles are individually inspectable, but no published result relates them or lets a later reader check them.
- **Shared settings are repeated across entries.**
  A named preset governs its declaring document, so entry model maps and repeated substitution settings have separate copies.
- **Independent exclusive choices lack local identities.**
  A document's alternatives form one exclusive set, so separate component and test choices cannot each require one member.
- **A document's choices are learned from a refusal.**
  The alternatives a document declares are listed only when a build fails for want of one.
- **Proposed forms are judged from prose.**
  New metadata and output are described before any file shows an author's source or an operator's result.

## Proposal

- **Specimens before contract.**
  Each proposed form is written as source and expected-output files, marked real or hand-written, and ruled on before its contract text exists.
- **A build ledger.**
  An explicit option publishes one YAML ledger beside the bundle set, naming effective selections, source origins, dispatch configuration and the invocation, with authored Markdown unchanged.
- **A checkable result.**
  A second option holds a published set to its ledger, so a changed source or bundle is reported.
- **Pure explicit imports.**
  A preset imports a named source's levels and substitutions, retaining their lexical origins and the receiving preset's scope, with explicit conflict and cycle refusals.
- **Named local choices.**
  Alternatives name local exclusive groups, so independent component and test selections stay separate from optional stubs and additive presets.
- **A listing without a build.**
  One option prints a document's presets, grouped alternatives and imports, publishing nothing.
- **One observable contract.**
  Frozen build specimens, public documentation and bounded source-bound observations distinguish accepted output, refusal and actual execution.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/890) | Design Specimens | AC5 | | |
| [E01](https://github.com/m2ux/prosiform/issues/868) | Build Ledger | AC1, AC3, AC4, AC6 | [E00](https://github.com/m2ux/prosiform/issues/890) | |
| [E02](https://github.com/m2ux/prosiform/issues/869) | Preset Imports | AC1, AC2, AC3, AC4 | [E00](https://github.com/m2ux/prosiform/issues/890) | |
| [E03](https://github.com/m2ux/prosiform/issues/870) | Local Choice Groups | AC1, AC2, AC3, AC4, AC7 | [E00](https://github.com/m2ux/prosiform/issues/890) | |

## Acceptance Criteria

- [ ] **AC1.** A published build's effective source bindings, local selections and invocation can be reconstructed from its ledger with the authored bundle text unchanged, as the ledger corpus and end-to-end checks show.
- [ ] **AC2.** Reused settings and independent local selections retain their declared scope and source-relative meaning through dispatch and deferral, as the preset-scope corpus shows.
- [ ] **AC3.** Invalid configuration publishes no partial result and identifies the conflicting or incomplete declaration, as the refusal and publication fixtures show.
- [ ] **AC4.** Public usage examples agree with the delivered configuration contract and preserve their authored outcomes, as `make check` and the bounded changed-behavior record show.
- [ ] **AC5.** The delivered configuration contract states only forms accepted from specimen files, as the planning record's rulings and the contract's clauses show.
- [ ] **AC6.** A published bundle set whose sources or bundles differ from its ledger is reported by one command, as the verification fixtures show.
- [ ] **AC7.** A document's presets, grouped alternatives and imports can be read without bundling it, as the listing fixtures show.

## Non-Goals

- It defines no generic inheritance or automatic rule or context injection.
- It changes no authored Contract, operation or result policy through metadata imports.
- It adds no inline-brief behavior or model-capability guarantee.
- It embeds no permissions, secrets, runtime sessions or capacity settings in presets.
- It implements no structured model or effort descriptor and no focused reviewer mode.
- It changes no Rust build's frozen contract target and evaluates no private application data.

## References

- **R1.** **Source.** [Confirmed goal and boundary](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/scope.md) — the feature scope this plan makes true.
- **R2.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture) — the design, specimen sets, work items and review.
- **R3.** [Source metadata at 0.36.0](https://github.com/m2ux/prosiform/blob/8cedda4cc06b0486168addc05f057161192a22a6/docs/sources.md#frontmatter) — the fixed baseline fields.
- **R4.** [Design Patterns](https://github.com/m2ux/prosiform/issues/526) — the existing documentation-only catalogue; this plan owns bundler changes rather than its pattern pages.
- **R5.** [Production Build](https://github.com/m2ux/prosiform/issues/532) — the independent frozen-contract Rust implementation.
