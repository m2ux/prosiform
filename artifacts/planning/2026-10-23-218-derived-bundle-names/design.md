# Derived Bundle Names

## Confirmed Rules

- Derive a single entry's output basename from its normalized source path relative to the declared root. Exclude the root directory name, remove the recognized Markdown extension, preserve spelling and replace path separators with underscores. Append `.bundle.md`.
- For a section entry, append `__` and the resolved fragment identifier before `.bundle.md`. A fragment-only entry uses the document supplied by `-f`.
- Several entry files produce one combined bundle and require an explicit output filename. Several distinct selections from one file also require an explicit destination because neither one source name nor one fragment describes that bundle. Repeated equivalent references count as one normalized selection.
- Authoring guidance recommends hyphens rather than underscores in file and directory names. Literal underscores remain literal; no percent encoding, hashing, collision registry or rejection of otherwise valid Markdown names is introduced.

| Root | Entry | Derived basename |
| --- | --- | --- |
| work-planner | modes/align-mode.md | modes_align-mode.bundle.md |
| work-planner | modes/align-mode.md#prerequisites | modes_align-mode__prerequisites.bundle.md |
| work-planner | SKILL.md | SKILL.bundle.md |
| work-planner | artifacts/epic.markdown | artifacts_epic.bundle.md |

## Automatic Output Policy

A single normalized entry writes its derived filename in the invocation's current working directory. Explicit `-o FILE` selects an exact destination; `-o -` selects stdout, including combined selections. Check mode validates without creating or replacing output. Help, version and diagnostic-code listing write their informational responses to stdout.

The user confirmed automatic naming: `-r` is the only required option for a single positional entry. An output argument is unnecessary in the ordinary case. Example: `pf -r work-planner modes/align-mode.md` writes `modes_align-mode.bundle.md` in the working directory.

## Compiler Boundaries

The CLI owns output naming. Linked dependencies' paths and conversion metadata do not rename the entry's output. Resolve references using existing root confinement and fragment identity before deriving a name; use the selected source's original filename, never generated group headings. Empty fragments resolve as whole-document selections under existing rules.

The derived name joins the confirmed output directory and enters the existing publication path. Input/output overlap checks include captured deferred sources. Check mode, byte budgets, candidate validation and source consistency checks precede atomic replacement. A failed run creates no partial destination and preserves existing output. Retain established output replacement behavior; underscore advice is not a guarantee of globally unique filenames across arbitrary paths, roots or case-insensitive filesystems. Length and filesystem failures use the publication-failure boundary rather than silently shortening names.

## Consumers And Verification

The runtime unit updates directly affected CLI tests, corpus invocation defaults, installed-wheel smoke, command tables and consumers such as the diagram renderer. Consumers requiring stdout select it explicitly. This is part of the behavior change, not deferred compatibility work.

Freeze the runtime baseline at `93fe6b354a85e244f64e33af700a55aab4f26044`. Compare compiled content bytes independently of destination naming; only the publication destination changes. Retain the existing per-file metadata and group-depth behavior.

The final audit checks active invocation documentation, worked examples and the authoring guidance handoff to proposal #208. Implementing a new authoring skill remains outside this extension. Historical captures retain their recorded commands. Normative changes precede the implementation and the final specification freeze consumes the updated audit.
