## Overview

Each Markdown file carries the structural settings used when Prosiform compiles it directly or reaches it through a link. This Field Refinement epic delivers the metadata contract, bounded parsing, source integration and the author-facing interface. Each source supplies its link-resolution root, and a selected entry determines its output filename, so the ordinary command is `pf <file>`.

## Problem

- **Structural intent lives in the invocation.**
  The [group option](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/cli.py#L533-L541) supplies global rules that linked files cannot declare for themselves.
- **The reader discards configuration.**
  [Frontmatter preprocessing](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/source.py#L239-L255) retains no metadata value for compilation.

## Proposal

- **Use skill-compatible extension fields.**
  `metadata.prosiform-group` and `metadata.prosiform-group-depth` are paired strings; depth is `"1"` through `"6"`. The schema follows Agent Skills string-valued metadata. Other skill fields remain metadata.
- **Each file declares its membership.**
  Declared group names are independent of directory names. Missing fields mean an individual file group; declarations discover no additional files.
- **Selection preserves ownership.**
  Direct entries, section fragments and linked dependencies use the destination file's settings. Group and depth remain file-owned. An absent root inherits the linking parent's effective root.
- **Group contributions agree.**
  Contributing members of one group declare equal depths. Conflicts identify both sources and publish nothing; deferred-only files contribute no membership.
- **Decode captured metadata once.**
  A bounded safe YAML decoder supplies typed settings and original coordinates from the captured source bytes; metadata never becomes Markdown content.
- **Keep the interface singular.**
  Remove structural CLI flags and global directory-rule machinery. Entries, explicit output overrides, diagnostics and resource limits remain operational controls; each source supplies the root for its own links.
- **Verify each implementation unit.**
  Tests and immediately affected consumers accompany the behavior they verify. The final authoring audit supplies corpus-wide evidence.
- **Bound the refactor.**
  Nested-folder layout, Unicode call-site composition, authoring-skill implementation and the Rust compiler implementation remain separate work.

- **A file supplies the complete invocation.**
  `metadata.prosiform-root` resolves relative to the entry file. `pf <file>` derives that root and the root-relative bundle filename; section selections append their fragment, and combined selections require an explicit destination.
- **Roots belong to their source files.**
  Each file resolves its relative Markdown links from its effective root: an explicit declaration or the inherited parent root, including linked files that address a separate library. Captured physical source identities preserve bounded traversal and consistency.
- **Authors avoid ambiguous flattened paths.**
  Guidance recommends hyphens rather than underscores in file and directory names.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/pull/219) | Declared metadata contract | AC1 | | | ✓ |
| [W02](https://github.com/m2ux/prosiform/pull/221) | Bounded metadata decoder | AC2, AC3, AC4 | W01 | | ✓ |
| [W03](https://github.com/m2ux/prosiform/pull/223) | Captured source settings | AC5, AC6, AC7 | W02 | | ✓ |
| [W04](https://github.com/m2ux/prosiform/pull/224) | Per-file compilation settings | AC8, AC9, AC10 | W03 | | ✓ |
| [W05](https://github.com/m2ux/prosiform/pull/225) | Metadata authoring guidance | AC11, AC12 | W04 | | ✓ |
| [W06](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/w06.md) | File-owned invocation contract | AC13 | W05 | | |
| [W07](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/w07.md) | Bounded root metadata | AC19 | W06 | | |
| [W08](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/w08.md) | Per-file root resolution | AC20, AC21, AC22 | W07 | | |
| [W09](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/w09.md) | Derived output publication | AC14, AC15, AC16 | W08 | | |
| [W10](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/w10.md) | File-only authoring audit | AC17, AC18 | W09 | | |

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

- [ ] **AC13.** The normative contract specifies file-owned root and output naming, as the invocation-contract review shows.
- [ ] **AC14.** One normalized entry publishes to its derived filename without an output option, as whole-file and fragment end-to-end tests show.
- [ ] **AC15.** Multiple distinct selections require an explicit combined output destination, as multi-entry invocation tests show.
- [ ] **AC16.** Derived destinations obey the publication safety contract, as atomic-output and installed-wheel regression tests show.
- [ ] **AC17.** Active authoring guidance recommends hyphens rather than underscores in source paths, as the documentation audit shows.
- [ ] **AC18.** The representative corpus preserves compiled content under file-only invocation, as pinned-baseline comparisons and the full-check report show.
- [ ] **AC19.** Bounded metadata decoding exposes a validated root declaration with its original location, as root-schema and coordinate tests show.
- [ ] **AC20.** The installed command resolves its link-resolution root from the selected entry's metadata, as file-only invocation tests show.
- [ ] **AC21.** Each local Markdown dependency resolves from its declaring source file's effective root, as per-file library-root and confinement tests show.
- [ ] **AC22.** The installed CLI rejects the retired root option, as -r rejection tests show.

## References

- **R1.** [Planning Record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-216-document-metadata/README.md) — design, evidence, task details and review.
- **R2.** [Document Metadata Proposal](https://github.com/m2ux/prosiform/issues/216) — originating per-file requirements.
- **R3.** [Agent Skills Metadata](https://agentskills.io/specification#metadata-field) — string-valued extension fields.

- **R4.** [Runtime Epic Review #222](https://github.com/m2ux/prosiform/pull/222) — per-file metadata compilation and authoring guidance; targets `main`, awaiting review.
- **R5.** [Contract Epic Review #220](https://github.com/m2ux/prosiform/pull/220) — normative metadata contract; merged into `engineering`.
- **R6.** [File-Owned Root and Bundle Names](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/README.md) — accepted file-only invocation, metadata root, naming and follow-on work.
