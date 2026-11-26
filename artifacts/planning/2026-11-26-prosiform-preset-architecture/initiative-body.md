## Overview

An author can reuse narrowly scoped preset settings and select independent local component/test alternatives, while an operator can inspect the exact effective sources and configuration behind every emitted bundle. The goal the reviews test against is reproducible, local configuration with readable authored policy and observable selection results.

## Problem

- **Effective configuration is reconstructed by hand.**
  Sources, preset selections, substitutions and dispatched bundles are individually inspectable, but no public build record relates them in one result.
- **Shared settings are repeated across entries.**
  A named preset governs its declaring document, so entry model maps and repeated substitution settings have separate copies.
- **Independent exclusive choices lack local identities.**
  A document can declare alternatives, but cannot state separate component and test choice groups with independent cardinality.

## Proposal

- **An effective-build manifest.**
  An explicit compiler option publishes a structured record beside the bundle set, identifying effective selections, source origins and dispatch configuration without changing authored Markdown.
- **Pure explicit imports.**
  A preset imports a named source's levels and substitutions, retaining their lexical origins and the receiving preset's existing scope, with explicit conflict and cycle refusals.
- **Named local choices.**
  Alternatives name local exclusive groups, so independent component and test selections remain separate from optional fixture stubs and ordinary additive presets.
- **One observable contract.**
  Frozen compiler specimens, public documentation and bounded source-bound observations distinguish accepted output, refusal and actual execution.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/868) | Effective Manifest | AC1, AC3, AC4 | | |
| [E01](https://github.com/m2ux/prosiform/issues/869) | Preset Imports | AC1, AC2, AC3, AC4 | | |
| [E02](https://github.com/m2ux/prosiform/issues/870) | Local Choice Groups | AC1, AC2, AC3, AC4 | | |

## Acceptance Criteria

- [ ] **AC1.** A published build's effective source bindings and local selections can be reconstructed from its structured record without changing the authored bundle text, as the build-manifest corpus and end-to-end checks show.
- [ ] **AC2.** Reused settings and independent local selections retain their declared scope and source-relative meaning through dispatch and deferral, as the preset-scope corpus shows.
- [ ] **AC3.** Invalid configuration publishes no partial result and identifies the conflicting or incomplete declaration, as the refusal and publication fixtures show.
- [ ] **AC4.** Public usage examples agree with the delivered configuration contract and preserve their authored outcomes, as make check and the bounded changed-behavior record show.

## Non-Goals

- It defines no generic inheritance or automatic rule/context injection.
- It changes no authored Contract, operation or result policy through metadata imports.
- It adds no inline-brief behavior or model-capability guarantee.
- It embeds no permissions, secrets, runtime sessions or capacity settings in presets.
- It implements no structured model/effort descriptor or focused reviewer mode.
- It changes no Rust build's frozen contract target or evaluates private application data.

## References

- **R1.** **Source.** [Confirmed goal and boundary](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/scope.md) — the feature scope this plan makes true.
- **R2.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture) — the design, evidence, work items and review.
- **R3.** [Current source metadata](https://github.com/m2ux/prosiform/blob/794922d41465b91deb4edb3a7484506cb8f519cd/docs/sources.md#frontmatter) — the fixed baseline fields.
- **R4.** [Design Patterns](https://github.com/m2ux/prosiform/issues/526) — the existing documentation-only catalogue; this plan owns compiler changes rather than its pattern pages.
- **R5.** [Production Build](https://github.com/m2ux/prosiform/issues/532) — the independent frozen-contract Rust implementation.
