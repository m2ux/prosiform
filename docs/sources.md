# Sources

A run's raw material is Markdown files on disk: a skill's entry point, the procedures it links to, the rules those procedures cite. Every one of them is a **source**, and the run's answer can only be as good as the bytes it read.

Each file is opened once, and everything the run decides about it is decided from that one reading: whether it declares itself part of a bundle, which parts of it the bundle takes, and where its links lead.

Both files below declare `prosiform` in leading frontmatter, and the first links the second in the directory above. The run reads each declaration and drops it, and resolves the `..` before the link is rewritten:

![modes/review.md and rules.md on the left, each opening with frontmatter declaring prosiform. On the right, the bundle: Review Mode and Rules with no frontmatter, and the link now pointing at #tests.](images/source.svg)

*Each declaration is read and dropped, and the `..` in the link is resolved before it disappears.*

## Capture

The run opens each distinct source once and keeps its path, bytes, hash and metadata together. Before publication it rechecks each one. A source that changed, disappeared or now resolves elsewhere fails the run, because the bytes that were validated are no longer the bytes the path names. A failed run writes nothing rather than publishing a bundle built from a file that has since moved.

Only files are sources. A directory, a symbolic link, or a path that cannot be read fails the run rather than being worked around.

## The declaration

A document is compiled because it says so. A document whose leading frontmatter carries a `prosiform` mapping **declares**, an empty `prosiform: {}` included, and a link naming it is a dependency the bundle carries. A document carrying no `prosiform` mapping declares nothing: a link naming it is text, emitted as authored, and the run reads its frontmatter and no further byte of it. A link naming a document that does not exist is text on the same ground, because nothing states the bundle answers for it.

Each path-bearing link resolves from the directory of the file that wrote it — the path a reader would follow in an editor — and the target's own declaration then decides whether it is compiled. Nothing about where either file sits decides it, so one document reached by two sources is one answer, and a link may name a declaring document anywhere, above the working directory included.

```mermaid
flowchart LR
  Doc["modes/plan-mode.md"] -- "resolves from the file's own directory" --> Ask{"does the target<br/>declare prosiform?"}
  Ask -- "declares" --> Rules["../rules/common.md<br/><i>compiled</i>"]
  Ask -. "declares nothing, carried as authored" .-> Guide["../library/guide.md"]
```

*Figure 1. A Link Resolves from Its Own File, and the Target's Declaration Decides Whether It Is Compiled.*

Every entry reference names a document that declares. One naming a document that declares nothing fails with `E_TARGET_NOT_FOUND` before any source is read.

## The boundary

A document's **boundary** is the deepest directory holding every local Markdown path its own links name, normalised from the document's directory; a document naming none has its own directory. `modes/plan-mode.md` above links `../rules/common.md` and `../library/guide.md`, so its boundary is the skill's directory, the deepest one holding both. The boundary is derived from the links, so it admits every link its author wrote and is never stated beside them.

What confines a run is the invocation working directory, captured once at the start. An entry reference resolves from it, and every path a diagnostic names is written from it.

## Frontmatter

Leading YAML frontmatter is read for metadata and excluded from the body. It opens on the first physical line with exactly `---` and closes at the next line exactly `---` or `...`. A byte-order mark may precede the opener.

The block is one YAML 1.2 Core mapping. Duplicate keys, aliases, merge keys and custom tags are invalid. An opener with no closer fails the run.

`prosiform` holds the conversion settings, and its presence is the declaration. Every key in `prosiform` is a **preset** name, and its value is a mapping of that preset's settings; a key holding anything else fails the run with `E_INVALID_CONVERSION_METADATA`. The `default` preset is in force wherever its document is compiled. Above it, a link selects each preset of the document it reaches whose name appears as a whole word, in any case, in the title of the section holding the link, so `Checks and Draft` selects `checks` and `draft` and `Checklist` selects neither; `default` is selected by no title. A command-line entry selects by the title of the section it names, or by its document's own title. Each link selects for itself, so two sections linking one document put the presets each title selects in force, and one run may bundle that document under two of its presets. A selected preset's `group` pair holds over `default`'s. The presets one title selects union their settings, and two of them stating different `group` pairs, or mapping one `subst` key to two alternatives, fail the run with `E_INVALID_USAGE` and exit status 2, naming both presets. A document's presets govern its own content alone: a document it links is governed by that document's own `default` and selected presets. A preset holds the keys below, and a key outside them fails the run as an unknown field. A key naming a budget (`files`, `file-bytes`, `input-bytes`, `output-bytes`, `targets`, `links`, `nesting`, `depth`) or a caller's option (the output folder, the diagnostics format, check mode, the version, the help) is such a key: a budget bounds a bundle rather than a document, and those options are the caller's. `root` fails, at the top level or within a preset, with `E_INVALID_CONVERSION_METADATA`, naming the field: a boundary is derived from a document's links, so a declared one states nothing a run reads.

| Key | Holds |
| --- | --- |
| `group` | one single-entry mapping of a group name, containing neither `:` nor `/`, to an integer from `1` to `6` |
| `subst` | a list of single-entry mappings, each an original reference mapped to its alternative |

`group: {modes: 1}` joins the document to group `modes` at depth `1`, and a link places the document under one group; a consumer needing another placement selects another preset. `subst: [{rules.md: stub.md}]` pairs one reference with its alternative, and each side is read by the reference grammar a link is read by. A run checks each `subst` entry and redirects no reference by it: the [substitution mapping](references.md#the-substitution-mapping) is the one substitution a run applies. YAML splits a plain key at a colon followed by a space, so a side holding one is quoted, as `{"rules.md#Step 1: Setup": stub.md}`. A `group` value or `subst` entry that is not a single-entry mapping, a key that is not a string, a `group` depth outside `1` to `6`, a `subst` side that is empty or not a string, and a side the reference grammar refuses each fail the run with `E_INVALID_CONVERSION_METADATA` naming the entry. Within one preset, two `subst` keys normalising to one identity, a `subst` key and value normalising to one identity, and a `subst` key naming a section alone, as `#Checks` does, each fail the run with `E_INVALID_USAGE` and exit status 2. Other top-level fields, `name` and `description` among them, are skill metadata and carry no conversion meaning. A file whose presets in force name no group keeps a group of its own.

A preset of a document the run's bundles carry that no reference reaching the document selected, in any bundle of the run, raises `W_PRESET_UNUSED`, naming the document as its source and the preset in its message, and the run publishes at exit status 0. `default` is in force wherever its document is compiled, so it is never unused. A document reached only through a deferral raises none: the deferral contributes no content to the run's bundles, and the run compiling the deferral reads its presets.

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
