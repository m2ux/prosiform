# Sources

A **source** is one local Markdown document a run opens. Its bytes are captured once, and everything the run decides about it comes from those bytes.

## Capture

The run opens each distinct source once and keeps its path, bytes, hash and metadata together. Before publication it rechecks each one. A source that changed, disappeared or now resolves elsewhere fails the run, because the bytes that were validated are no longer the bytes the path names.

Only files are sources. A directory, a symbolic link, or a path that cannot be read fails the run rather than being worked around.

## The root

Every source has an effective **root**, a directory that bounds which of its links the run will follow.

An explicit root resolves from the declaring file's directory. Every absent root uses the invocation working directory, captured once at the start.

The root bounds a link; it is not the base a link resolves from. Each path-bearing link resolves from the directory of the file that wrote it — the path a reader would follow in an editor — and the root then decides whether the result is inside. A link landing outside stays as the author wrote it and is never opened.

A root may name a sibling library that does not contain its declaring source. It authorizes content; it does not require the file to move.

## Frontmatter

Leading YAML frontmatter is read for metadata and excluded from the body. It opens on the first physical line with exactly `---` and closes at the next line exactly `---` or `...`. A byte-order mark may precede the opener.

The block is one YAML 1.2 Core mapping. Duplicate keys, aliases, merge keys and custom tags are invalid. An opener with no closer fails the run.

`prosiform` holds the conversion settings. The only keys in `prosiform` are `root`, `group` and `group-depth`; a key outside them fails the run.

| Key | Holds |
| --- | --- |
| `root` | a relative directory path using forward slashes |
| `group` | a group name, containing neither `:` nor `/` |
| `group-depth` | an integer from `1` to `6` |

`group` and `group-depth` are declared together or not at all. Other top-level fields, `name` and `description` among them, are skill metadata and carry no conversion meaning. A file with no conversion fields keeps a group of its own.

Frontmatter counts toward the byte budgets and obeys the nesting budget independently of Markdown containers. It supplies no headings, links or rendered content.

## The profile

Sources are parsed under one versioned grammar, `skill-markdown-v4`, reported by `-v`. It is CommonMark with pipe tables and double-tilde strikethrough, and task-list markers are preserved as written rather than rendered as checkboxes.

Sources must be valid UTF-8 — a byte sequence that is not fails rather than being decoded with replacement characters. One leading byte-order mark is tolerated and removed. `.md` and `.markdown` are recognized case-insensitively.

Raw HTML in selected content is refused: the bundle is Markdown and nothing else. Constructs the profile does not support — footnotes, wiki links, heading attributes — are refused where they would name a dependency or a section.

## Text that is not a source

Two things inside a source look like local Markdown and are not followed.

- A link written inside a code span, a fenced block or an indented block is an example. The one exception is a diagram's own link lines, which [References](references.md#diagram-links) covers.
- A bare path in prose is text. The run does not infer a dependency from it.

## Why a source is read whole

The run parses the complete file even when only one section was selected. It needs the heading index of the whole document to resolve a fragment, and the definitions of the whole document to resolve a reference-style link. What the file contains therefore fails the run only where the run needed it: an unselected sibling may carry a broken link, and the run passes.

A file can still fail for a reason that is about the file rather than about the selection — an unreadable encoding, or a nesting depth beyond the budget. That is reported as an inability to index the source safely.
