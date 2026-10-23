## Overview

Each Markdown file carries the structural settings used when Prosiform compiles it directly or reaches it through a link. This Field Refinement epic delivers the metadata contract, bounded parsing, source integration and the author-facing interface.

## Problem

- **Structural intent lives in the invocation.**
  The [group option](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/cli.py#L533-L541) supplies global rules that linked files cannot declare for themselves.
- **The reader discards configuration.**
  [Frontmatter preprocessing](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/source.py#L239-L255) retains no metadata value for compilation.

## Proposal

- **Use skill-compatible extension fields.**
  `metadata.prosiform-group` and `metadata.prosiform-group-depth` are paired strings; depth is `"1"` through `"6"`. Other skill fields remain metadata.
- **Each file declares its membership.**
  Declared group names are independent of directory names. Missing fields mean an individual file group; declarations discover no additional files.
- **Selection preserves ownership.**
  Direct entries, section fragments and linked dependencies use the destination file's settings. Callers supply no inherited configuration.
- **Group contributions agree.**
  Contributing members of one group declare equal depths. Conflicts identify both sources and publish nothing; deferred-only files contribute no membership.
- **Decode captured metadata once.**
  A bounded safe YAML decoder supplies typed settings and original coordinates from the captured source bytes; metadata never becomes Markdown content.
- **Keep the interface singular.**
  Remove structural CLI flags and global directory-rule machinery. Output paths, roots, entries, diagnostics and resource limits remain operational controls.
- **Verify each implementation unit.**
  Tests and immediately affected consumers accompany the behavior they verify. The final authoring audit supplies corpus-wide evidence.
- **Bound the refactor.**
  Nested-folder layout, Unicode call-site composition, authoring-skill implementation and the Rust compiler implementation remain separate work.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-216-document-metadata/w01.md) | Declared metadata contract | AC1 |  | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-216-document-metadata/w02.md) | Bounded metadata decoder | AC2, AC3, AC4 | W01 | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-216-document-metadata/w03.md) | Captured source settings | AC5, AC6, AC7 | W02 | | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-216-document-metadata/w04.md) | Per-file compilation settings | AC8, AC9, AC10 | W03 | | |
| [W05](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-216-document-metadata/w05.md) | Metadata authoring guidance | AC11, AC12 | W04 | | |

## Acceptance Criteria

- [ ] **AC1.** The normative design defines per-file conversion metadata and its failure behavior, as the metadata contract review shows.
- [ ] **AC2.** The metadata decoder accepts exactly the declared field schema, as its positive and negative schema tests show.
- [ ] **AC3.** YAML decoding stays within the declared source-byte and nesting limits, as the parser resource tests show.
- [ ] **AC4.** Invalid metadata identifies its original source location, as the metadata diagnostic tests show.
- [ ] **AC5.** Each captured source exposes one immutable conversion value alongside its Markdown body, as the source-reader tests show.
- [ ] **AC6.** Frontmatter contributes no Markdown content or dependencies, as the source preprocessing fixtures show.
- [ ] **AC7.** Source accounting and diagnostic coordinates include the original metadata bytes, as the capture and coordinate regression tests show.
- [ ] **AC8.** A contributing file uses its own conversion settings through direct, fragment, repeated and transitive selection, as the end-to-end metadata fixtures show.
- [ ] **AC9.** A group with conflicting member depths fails without publishing output, as the conflict and atomic-publication fixtures show.
- [ ] **AC10.** The installed CLI accepts structural settings only from source metadata, as retired-option rejection and retained-operational-option smoke tests show.
- [ ] **AC11.** Active author-facing instructions express structural settings through the declared frontmatter fields, as the documentation and invocation checks show.
- [ ] **AC12.** The declared representative corpus compiles with metadata-driven grouping against the pinned baseline expectations, as the corpus and full-check report shows.

## References

- **R1.** [Planning Record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-216-document-metadata/README.md) — design, evidence, task details and review.
- **R2.** [Document Metadata Proposal](https://github.com/m2ux/prosiform/issues/216) — originating per-file requirements.
- **R3.** [Agent Skills Metadata](https://agentskills.io/specification#metadata-field) — string-valued extension fields.
