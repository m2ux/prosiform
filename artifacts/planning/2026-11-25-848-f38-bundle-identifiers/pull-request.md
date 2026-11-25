## Overview

Bundle paths currently hide preset selections behind long hashes. This change uses **the preset names themselves**: `workflow-codex.bundle.md`, or `workflow-codex+recorded.bundle.md`. Equivalent requests still share a bundle, and filename collisions fail before publication.

## Changes

- Sort effective declaration names, escape each safely and join them with `+` after a single hyphen.
- Keep entry folders, dispatched filenames, rewritten links, documentation, lifecycle examples and exact-output fixtures consistent.
- Cover literal plus signs, slashes, percent signs, spaces, Unicode and collisions with source-derived filenames, including preservation of earlier output.

## Test Plan

| Test | Description | Coverage | Pass |
| --- | --- | --- | --- |
| T1 | Complete source suite: canonical selection, escaping and atomic collision refusal | AC1, AC2, AC3 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-848-f38-bundle-identifiers/named-final-check.log) |
| T2 | Exact-output corpus, check harness and installed-wheel smoke | AC1, AC2, AC4 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-848-f38-bundle-identifiers/named-final-check.log) |
| T3 | Full make check: lint, format, types, docs and contract checks | AC4 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-848-f38-bundle-identifiers/named-final-check.log) |

## References

- **R1.** [F38 #848](https://github.com/m2ux/prosiform/issues/848) — Defect and acceptance criteria.
- **R2.** [Verification](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-848-f38-bundle-identifiers/test-results.md) — Source-bound evidence and historical candidates.
- **R3.** [Agent review](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-848-f38-bundle-identifiers/agent-review.json) — Exact-head review and criterion evidence.

- **R4.** [Source and bundle examples](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-848-f38-bundle-identifiers/README.md#source-and-bundles) — One and two effective presets, including child links.
