## Overview

Preset-qualified bundle filenames carry the full 64-character SHA-256 digest even though the compiler already refuses distinct selections that derive the same name. This hotfix uses a **12-character qualifier** so entry folders and dispatched bundle links are easier to read, retaining canonical selection identity and atomic publication.

Target: `main`

## Problem

- **Generated names overwhelm the useful path.**
  A full digest dominates filenames used to navigate and hand over preset-qualified bundles.
- **Every published reference must agree.**
  Entry folders, child filenames, rewritten dispatch links, documentation and expected examples share the derived-name contract.

## Proposal

- **Keep selection names succinct.**
  Use the first 12 lowercase hexadecimal SHA-256 characters of the existing canonical preset serialization. Preserve path/fragment naming and equivalence under tag order, case, repetition and unknown tags.
- **Retain collision refusal.**
  Reject distinct effective selections deriving one filename before publication, with the existing publication error. Preserve any earlier output set, including a collision whose full digests differ after their common prefix.
- **Keep the contract and examples exact.**
  Align the derived-name specification, fixture manifests, expected filenames, linked contents, lifecycle example, diagram and installed-wheel smoke expectations. Retire the full-digest output names.
- **Record the completed implementation retrospectively.**
  The local implementation and its tests precede tracker registration. Publish one isolated hotfix and draft PR without an initiative, epic or dependency.

## Acceptance Criteria

- [ ] **AC1.** Preset-qualified entry folders and dispatched bundles use 12 hexadecimal digest characters with valid rewritten links, as source regressions and the corpus verify.
- [ ] **AC2.** Equivalent effective selections retain one bundle and distinct selections retain their content, as preset/dispatch tests verify.
- [ ] **AC3.** Distinct selections forced to one truncated digest name fail with E_PUBLICATION_FAILED and preserve the earlier output bytes, as the collision regression verifies.
- [ ] **AC4.** The documented naming contract, expected fixtures and examples agree, with source, installed-wheel and corpus checks passing.

## References

- **R1.** [Derived names](https://github.com/m2ux/prosiform/blob/684437c06/docs/bundles.md#derived-names) — Published full-digest contract and existing collision refusal.
