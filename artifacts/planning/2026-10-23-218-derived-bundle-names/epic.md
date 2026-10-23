## Overview

Each Markdown file carries the structural settings used when Prosiform compiles it directly or reaches it through a link. This Field Refinement epic delivers the metadata contract, bounded parsing, source integration and the author-facing interface. Entry paths and selected fragments also determine predictable bundle filenames.

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

- **Name bundles from their entry.**
  A single entry derives its bundle filename from the root-relative source path; a section adds its fragment. Single entries write automatically in the working directory; combined entries require an explicit destination. Authoring guidance recommends hyphens instead of underscores.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/pull/219) | Declared metadata contract | AC1 | | | ✓ |
| [W02](https://github.com/m2ux/prosiform/pull/221) | Bounded metadata decoder | AC2, AC3, AC4 | W01 | | ✓ |
| [W03](https://github.com/m2ux/prosiform/pull/223) | Captured source settings | AC5, AC6, AC7 | W02 | | ✓ |
| [W04](https://github.com/m2ux/prosiform/pull/224) | Per-file compilation settings | AC8, AC9, AC10 | W03 | | ✓ |
| [W05](https://github.com/m2ux/prosiform/pull/225) | Metadata authoring guidance | AC11, AC12 | W04 | | ✓ |

| [W06](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/w06.md) | Derived output contract | AC13 | W05 | | |
| [W07](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/w07.md) | Derived output publication | AC14, AC15, AC16 | W06 | | |
| [W08](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/w08.md) | Output naming authoring audit | AC17, AC18 | W07 | | |

## Acceptance Criteria

- [x] **AC1.** The normative design defines per-file conversion metadata and its failure behavior, as the metadata contract review shows.
- [x] **AC2.** The metadata decoder accepts exactly the declared field schema, as its positive and negative schema tests show.
- [x] **AC3.** YAML decoding stays within the declared source-byte and nesting limits, as the parser resource tests show.
- [x] **AC4.** Invalid metadata identifies its original source location, as the metadata diagnostic tests show.
- [x] **AC5.** Each captured source exposes one immutable conversion value alongside its Markdown body, as the source-reader tests show.
- [x] **AC6.** Frontmatter contributes no Markdown content or dependencies, as the source preprocessing fixtures show.
- [x] **AC7.** Source accounting and diagnostic coordinates include the original metadata bytes, as the capture and coordinate regression tests show.
- [x] **AC8.** A contributing file uses its own conversion settings through direct, fragment, repeated and transitive selection, as the end-to-end metadata fixtures show.
- [x] **AC9.** A group with conflicting member depths fails without publishing output, as the conflict and atomic-publication fixtures show.
- [x] **AC10.** The installed CLI accepts structural settings only from source metadata, as retired-option rejection and retained-operational-option smoke tests show.
- [x] **AC11.** Active author-facing instructions express structural settings through the declared frontmatter fields, as the documentation and invocation checks show.
- [x] **AC12.** The declared representative corpus compiles with metadata-driven grouping against the pinned baseline expectations, as the corpus and full-check report shows.

- [ ] **AC13.** The normative contract specifies entry-derived output naming, as the naming-contract review shows.
- [ ] **AC14.** One normalized entry publishes to its derived filename without an output option, as whole-file and fragment end-to-end naming tests show.
- [ ] **AC15.** Multiple distinct selections require an explicit combined output destination, as multi-entry invocation tests show.
- [ ] **AC16.** Derived destinations obey the existing publication safety contract, as atomic-output and installed-wheel regression tests show.
- [ ] **AC17.** Active authoring guidance recommends hyphens rather than underscores in source paths, as the documentation audit shows.
- [ ] **AC18.** The representative corpus preserves compiled content under derived output naming, as pinned-baseline comparisons and the full-check report show.

## References

- **R1.** [Planning Record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-216-document-metadata/README.md) — design, evidence, task details and review.
- **R2.** [Document Metadata Proposal](https://github.com/m2ux/prosiform/issues/216) — originating per-file requirements.
- **R3.** [Agent Skills Metadata](https://agentskills.io/specification#metadata-field) — string-valued extension fields.

- **R4.** [Runtime Epic Review #222](https://github.com/m2ux/prosiform/pull/222) — per-file metadata compilation and authoring guidance; targets `main`, awaiting review.
- **R5.** [Contract Epic Review #220](https://github.com/m2ux/prosiform/pull/220) — normative metadata contract; targets `engineering`, awaiting review.
- **R6.** [Derived Bundle Names](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/README.md) — accepted naming rules, follow-on tasks and output-policy decision.
