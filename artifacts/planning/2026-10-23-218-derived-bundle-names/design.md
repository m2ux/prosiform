# File-Owned Root And Bundle Names

## Command And Metadata

The normal command is `pf work-planner/modes/align-mode.md`. The positional file path is resolved from the working directory. No root or output option is required.

For that entry, the leading frontmatter includes:

```yaml
---
prosiform:
  root: ".."
  group: modes
  group-depth: 2
---
```

`prosiform.root` is a nonempty relative directory-path string, interpreted from the containing Markdown file's directory. Here `..` identifies `work-planner`. A file in the root directory declares `"."`. The root field is independent of the optional paired group/depth fields. Absolute paths, home shortcuts, environment expansion and URL interpretations are outside the schema.

The field belongs to each source file. Its resolved directory is the base for local Markdown paths authored in that file, including deferred targets. A linked file can declare a different root, such as a library directory. An absent declaration uses the invocation working directory for every source, including linked files. There is no `-r` option or global-root agreement requirement. Fragment-only links still identify headings in their own source document.

## Derived Names

- Derive one normalized entry's basename from its source path relative to the declared root. Exclude the root's directory name, remove the recognized Markdown extension, preserve spelling and replace path separators with underscores. Append `.bundle.md`.
- For a section entry, append `__` and the resolved fragment identifier before `.bundle.md`. A fragment-only reference uses the file supplied by `-f`; that file path is resolved from the working directory and supplies the root declaration.
- Several distinct entries produce one combined bundle and require an explicit output destination. This also applies to multiple distinct sections of one file. Repeated equivalent references count as one normalized selection; an empty fragment uses the existing whole-document identity.
- Write automatic output in the working directory. Explicit `-o FILE` selects an exact destination; `-o -` selects stdout, including combined selections. Check mode publishes nothing. Informational responses use stdout.
- Recommend hyphens rather than underscores in file and directory names. Literal underscores remain literal; no percent encoding, hashing, collision registry or rejection of otherwise valid Markdown names is introduced.

| Command | Resolved root | Output |
| --- | --- | --- |
| `pf work-planner/modes/align-mode.md` | work-planner | modes_align-mode.bundle.md |
| `pf work-planner/modes/align-mode.md#prerequisites` | work-planner | modes_align-mode__prerequisites.bundle.md |
| `pf work-planner/SKILL.md` with root `"."` | work-planner | SKILL.bundle.md |
| `pf work-planner/artifacts/epic.markdown` with root `".."` | work-planner | artifacts_epic.bundle.md |

The selected entry's path relative to its own effective root determines the filename; linked files' roots and conversion group names do not rename it. A declared library root need not contain its authoring file: retain parent segments in the relative path before flattening separators, so they become filename text rather than directory traversal. Underscore guidance reduces collisions but does not guarantee uniqueness across arbitrary source paths, roots or case-insensitive filesystems. Existing atomic replacement behavior remains; filesystem length failures are reported, not silently shortened.

## Capture And Resolution

Use the same per-source captured metadata model for root, group and depth. The root value resolves relative to its declaring file's directory. Every path-bearing local Markdown reference resolves from that source's effective root; opening its target then reads the target's own metadata for its outgoing links. Explicit entries may have different roots and still produce one combined bundle when an explicit destination is supplied.

Capture the positional entry under existing byte, aggregate and YAML nesting limits before following references. Store the effective per-source root with the captured source and preserve original locations, immutable metadata, rooted no-follow access and full-file consistency checks. Bind each dependency access to the root of the source that authored the link. The existing outside-root classification applies against that source's effective root, rather than a shared invocation root. A file may intentionally point its relative links into a library by declaring that library as its root.

Canonical physical identity controls source-byte capture. Each source has one effective root within an invocation: its explicit file-relative declaration or the invocation working directory. A shared file reached through different parents therefore resolves its outgoing links identically. W06 defines deterministic deduplication and cycle behavior before W08 implements it. Preserve fragment-only self references, deferred-target validation and resources that the compiler does not open. Diagnostics and link chains must identify the actual source even when files sit under different declared roots.

Check mode, captured-source/output overlap, limits, candidate validation and atomic publication retain their safeguards. Invalid roots and confinement failures receive stable contract diagnostics before implementation; differing valid roots are not a conflict. A source change after capture fails before publication.

## Delivery Layers And Consumers

First define the contract, then implement the top-level mapping and bounded root value, then implement per-source root resolution, then automatic output naming, then audit authoring and the corpus. Each runtime unit updates its own immediately affected consumers and tests, so every intermediate delivered build works end to end.

The root-resolution unit migrates active entry fixtures and CLI consumers away from `-r`, including `-f` file resolution, installed-wheel smoke and diagram renderer invocations. The output unit migrates stdout-dependent consumers to explicit `-o -`. A caller can compile a section using `pf file.md#fragment`; source-authored Markdown paths use the declaring file's effective root.

Freeze runtime content expectations at `93fe6b354a85e244f64e33af700a55aab4f26044`. Compare bundle content independently of the invocation and output destination. Annotating fixture entry roots must preserve body content and update physical-location expectations deliberately. Include absent roots on entries and linked files with a working directory distinct from their directories, invalid roots, relative parent traversal, symlink refusal, different library roots, repeated physical targets, cycles, entry mutation during capture, raw byte limits and atomic failure cases.

The final audit checks all active guidance and representative sources. Authoring proposal #208 must teach per-file root declarations for intended standalone entries and linked library files and recommend hyphens instead of underscores. Implementing the authoring skill remains separate. The specification freeze consumes this extension's final audit. Contract PR #220 is merged; new contract work uses a successor review. Runtime PR #222 remains draft and is refreshed from actual subsequent task merges.

## Frontmatter Schema

Frontmatter contains a top-level `prosiform` mapping with full key names: `root`, `group` and `group-depth`. Root and group are strings; group-depth is an integer from 1 through 6, paired with group. An absent root uses the invocation working directory for every source, including linked files. Explicit roots resolve relative to the declaring file's directory. Empty or malformed values fail validation. The command is `pf`, with short operational flags such as `-o` and `-f`. This is a Prosiform frontmatter extension; strict Agent Skills schema compatibility is not a requirement.
