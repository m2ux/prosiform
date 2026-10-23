# Document Metadata — October 2026

> Refactor Planning · Created 2026-10-23

## Executive Summary

Prosiform derives each Markdown file's structural conversion settings from that file's YAML frontmatter. The user confirmed per-file ownership on 2026-10-23: direct entries, linked dependencies and section selections use the selected source's settings.

This record scopes the refactor, records its source evidence and proposes an implementation sequence. The user requested a new epic under the existing refinement initiative. Epic #218 has priority 6, ahead of Section Composition at 5, as the user requested. Compiler implementation is outside this planning request.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Design](design.md) | Proposed metadata contract, compiler boundaries and verification |
| [Epic](epic.md) | Acceptance criteria and task dependency table |
| [Initiative Update](initiative-draft.md) | Scoped parent criteria and epic row with published issue links |
| [Freeze Handoff](freeze-draft.md) | Final contract tag dependency with published issue links |
| [Review](review.md) | Goal coverage, graph review and integration decisions |
| [W01](w01.md) | Declared metadata contract |
| [W02](w02.md) | Bounded metadata decoder |
| [W03](w03.md) | Captured source settings |
| [W04](w04.md) | Per-file compilation settings |
| [W05](w05.md) | Metadata authoring guidance |
| [Evidence and Decisions](evidence.md) | Baseline, confirmed scope, related work and planning progress |

## Links

| Resource | Link |
| --- | --- |
| Proposal | [#216 — Document Metadata](https://github.com/m2ux/prosiform/issues/216) |
| Metadata Convention | [Agent Skills Specification](https://agentskills.io/specification#metadata-field) |
| Epic | [#218 — I01 E06 Document Metadata](https://github.com/m2ux/prosiform/issues/218) |
| Discussion | [Draft PR #217](https://github.com/m2ux/prosiform/pull/217) |
