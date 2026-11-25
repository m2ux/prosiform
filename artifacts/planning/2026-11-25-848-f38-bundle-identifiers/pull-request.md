## Overview

Preset-qualified filenames use a **12-character digest** so paths and dispatch links remain readable. Canonical selection identity and existing collision refusal remain in force; a forced prefix collision preserves the previous published set.

## Changes

- Keep naming consistent across entry folders, children, rewritten links, fixtures, documentation and the lifecycle example.
- Test collisions between different full digests sharing the same short prefix.
- Record F38 retrospectively after implementation and observing checks.

## Test Plan

| Test | Description | Coverage | Pass |
| --- | --- | --- | --- |
| T1 | 2,324 source cases, including installed-wheel checks | AC1, AC2, AC4 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-848-f38-bundle-identifiers/test-results.md) |
| T2 | 708 exact-output corpus fixtures | AC1, AC2, AC4 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-848-f38-bundle-identifiers/corpus.log) |
| T3 | Final 10 publication cases, including atomic prefix-collision refusal | AC3 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-848-f38-bundle-identifiers/collision-tests.log) |
| T4 | Lint/format and type checking of 87 files | AC4 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-848-f38-bundle-identifiers/types.log) |

## References

- **R1.** [F38 #848](https://github.com/m2ux/prosiform/issues/848) — Defect and acceptance criteria.
- **R2.** [Retrospective record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-848-f38-bundle-identifiers/README.md) — Source pins, verification and limits.
