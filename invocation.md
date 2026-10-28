# Invocation

Compile local Markdown entries and their dependencies into one validated bundle, and each target they dispatch into a bundle of its own.

```text
pf [OPTIONS] REF [REF ...]
```

## Options

Flags are case-sensitive. Budgets are positive decimal integers; zero is invalid.
`pf -h` and these tables agree; `make invocation` verifies them.

| Option | Effect |
| --- | --- |
| `REF` | document, document#fragment, or #fragment with -f; paths from cwd |
| `-f DOC` | working-directory-relative document for fragment-only references |
| `-o DIR` | existing folder the run's own folder of bundles is written into, swapped in whole; default: the working directory |
| `-c` | discover, bundle, validate; publish nothing; accepts -o |
| `-d {text,json}` | stderr diagnostics; default text |
| `-x {source-changed,internal}` | inject a conformance run fault no source tree expresses; default none |
| `-F N` | distinct source documents opened; positive decimal integer, default 256 |
| `-B N` | raw bytes in one source; positive decimal integer, default 1048576 |
| `-I N` | raw source bytes, counted once per source; positive decimal integer, default 16777216 |
| `-O N` | bytes of the complete bundle; positive decimal integer, default 262144 |
| `-T N` | distinct document and section targets discovered; positive decimal integer, default 4096 |
| `-L N` | authored link and image occurrences in selected content; positive decimal integer, default 32768 |
| `-N N` | levels of container nesting and, independently, YAML collection nesting in one source; positive decimal integer, default 64 |
| `-E N` | link hops from the nearest entry reference; positive decimal integer, default 8 |
| `-C, --codes` | list this build's error and warning codes |
| `-v, --version` | tool version and profile identifier |
| `-h, --help` | usage, defaults and exit statuses |

## Examples

Run from the repository root; [worked examples](example/README.md) show input and output.

```bash
cd example/work-planner
pf modes/plan-mode.md
pf 'artifacts/epic.md#delivery-findings'
pf -o build modes/plan-mode.md
pf modes/plan-mode.md 'artifacts/epic.md#delivery-findings'
pf -c modes/plan-mode.md
```

## Conversion metadata

Each file declares its own group and source heading depth in leading YAML frontmatter:

```yaml
---
author: example-team
prosiform:
  group: rules
  group-depth: 2
---
```

Group and group-depth occur together. Group is a string; group-depth is a YAML Core integer from `1` through `6`, excluding booleans, floats and strings. The group name is a nonblank, printable single-line string containing neither `:` nor `/`; its exact spelling identifies the group. A file without these fields keeps its individual group. Linked files use their own declarations, including when only a section is selected. Group names are independent of directories and discover no additional files.

Frontmatter starts on the first physical line with exactly `---` and closes at the next line exactly `---` or `...`; an optional byte-order mark may precede the opener. A leading blank line makes the following content part of the body. The block is empty or contains one YAML 1.2 Core mapping. Its top-level keys are strings; `prosiform`, when present, is a mapping with string keys. Keep standard skill fields such as `name` and `description` at the top level; ordinary Markdown requires neither field nor a `SKILL.md` filename. The only keys in `prosiform` are `root`, `group` and `group-depth`; unknown keys fail validation. Unrelated fields, including `metadata`, have no conversion meaning. An optional `root` is a nonempty relative directory-path string using forward slashes; controls, absolute or drive paths, URLs, home shortcuts and environment expansion fail validation. The captured value retains its spelling and original location. An explicit root resolves from the declaring file's directory. Every absent root uses the working directory captured at invocation start. A root bounds a source's links and is not their base: each link resolves from the directory of the file that writes it, the path a reader follows, and one landing outside the root stays authored. Root is independent of group and group-depth. Positional files and `-f` resolve from that same working directory, with bounded parent-directory bootstrap permitted. The `-r` option is invalid usage.

Duplicate keys, aliases, merge keys and custom tags are invalid throughout the frontmatter. Frontmatter bytes count toward the source byte budgets, and YAML collections obey `-N` independently of Markdown containers. Frontmatter supplies no rendered content, links or headings.

Contributing files declaring the same group must agree on depth. A conflict reports both declarations and publishes nothing. Deferred-only files are validated but contribute no group membership. Each selected destination supplies its settings once, whether reached directly, by fragment or through several callers; declarations do not propagate to siblings or dependencies.

Metadata errors return exit status `1`: `E_INVALID_FRONTMATTER` identifies invalid YAML, `E_INVALID_CONVERSION_METADATA` identifies invalid fields, and `E_GROUP_DEPTH_CONFLICT` identifies conflicting contributing declarations. Diagnostics locate the original source; JSON diagnostics include `location` and, for conflicts, `related` locations. Existing output files remain intact on failure.

## Bundling rules

- **Sources:** valid UTF-8; validate leading frontmatter as bounded YAML 1.2 Core and retain each file's conversion metadata; parse the body after one leading byte-order mark and frontmatter block as `skill-markdown-v4`.
- **Closure:** entries select whole documents or named sections. Follow each local Markdown link from the directory of the source that writes it, within that source's root, until no new dependencies remain. Compiled links target bundle headings. Outside-root links stay authored and contribute nothing.
- **Diagram links:** in a fenced code block whose info string opens with `mermaid`, each destination a diagram link line names is a use on the line it is written, counted against `-L`, and is followed like any link. The lines are `click <node> href "<destination>"` and `click <node> "<destination>"` in any diagram; `link <class> "<destination>"` in a class diagram; and, in a sequence diagram, `link <actor>: <label> @ <destination>`, whose destination is the trimmed text after the first `@`, and `links <actor>: {…}`, each string value of whose JSON object is one destination. A diagram's type is the word its text opens on once a leading front matter block, its `%%{…}%%` directives and its `%%` comments are set aside, as Mermaid detects it, so a line beginning `link` in any other diagram is carried as written. Their keywords match in any letter case. A sequence line's text ends at its first `;` or `#` that opens no entity, as Mermaid's sequence lexer ends it, so a `link` destination or a `links` object ends there and the bytes after it are carried as written; a `#35;` in a sequence destination names `#`, so `<doc>.md#35;<fragment>` names the section `<fragment>`. A `links` object is read as `JSON.parse` reads it: a key written twice names its last value alone, and a value that is not a string fails the run with `E_UNSUPPORTED_CONSTRUCT` naming the line. A destination naming a Markdown document or section under the root is bundled, and its characters are rewritten to the anchor of the group it names. A Gantt task's `click` is the one link Mermaid draws as no anchor: it binds a handler that opens the destination when the task is clicked in the running page, so the rewritten anchor is what that click opens. A sequence diagram's `link` and `links` destinations spell that anchor `#35;<slug>`, the entity Mermaid renders as `#`, because its sequence lexer reads a bare `#` as opening a comment; every other byte of the fence is carried as written. A click naming a callback, a destination outside the root, a destination naming no Markdown document, a `links` value holding a JSON escape and a `links` line holding no JSON object are carried as written and open nothing, as is a C4 diagram's `$link`. A Kanban ticket's link, which Mermaid builds by putting the ticket in place of `#TICKET#` in the `ticketBaseUrl` the diagram's front matter or `%%{init}%%` directive sets, and an HTML anchor in a node label are links Mermaid renders and the reader does not follow: one naming a local Markdown document fails the run with `E_UNSUPPORTED_CONSTRUCT` naming its line, as raw HTML naming one does, so the author writes it as a `click`, and one naming a remote address is carried as written. A diagram link carries no operator, since a diagram gives it no link text. Apparent links in any other code span or block are example text and are never followed.
- **Groups:** each contributing document that declares no group is headed by its title (its first heading, where that is its only H1) or, without one, by its title-cased path relative to the working directory, Markdown suffix removed. Coinciding file headings take distinct destinations, the later carrying an ordinal. A root names no heading, order or output. Merged groups use title-cased declared names. Member subsections contain content above grouping depth, under `Overview` when merged sections also occur at grouping depth, otherwise directly under the group. A titled entry member — the first entry, whose selection carries its title above grouping depth — opens its group with its own title and preamble in place of the group's name: its sections lead, and the other members' subsections follow in the `Overview`, or directly under the title when no merged section occurs. Members have distinct destinations and shortest-distinguishing-path, title-cased headings; members whose paths differ only by Markdown extension or capitalization share one name. Authored headings and filesystem paths retain their spelling.
- **Dependency order:** each document is placed at the first link naming it: the entry references in command-line order, then each placed document's selected content in turn, in source order. Groups stand where their first document is placed, and a merged group's members follow placement order. Its merged sections follow the parent's own, then first appearance across the members; a section's variants follow member order, the parent's first. An author sets the order by writing the links in it: a preamble reading `Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md)` places Rules, then Conventions, directly after the entry document's own sections. Conflicting group declarations are reported in path order.
- **Deferred links:** link text starting with `¬` followed by a space requires an existing document/section but adds no content through that link. Emit the link's text without the marker and the blanks following it, because the destination already states the deferral, and emit a URI-escaped working-directory-relative destination for a separate run. A link or image opening with `¬` that names anything but a Markdown document or section under the root — a remote address, a resource, an image, a document outside the root — fails with `E_UNSUPPORTED_CONSTRUCT` naming the reference and its location.
- **Dispatched links:** link text starting with `⇉` followed by a space requires an existing document/section and adds no content, dependency or group membership to the bundle carrying it. The run compiles the target, transitively, as a bundle of its own in the run's folder: each distinct document or section once, named by its own selection, every dispatch naming it naming that bundle. The link is published without its mark and points at a `Dispatch <link text>` sub-section one level below the section holding it, after that section's own content and before its child sections, whose one line names the target's bundle file; links in one section naming one target share it, and a dispatch above a group's first heading takes that heading's level. A mark with no space after it opens no operator: `[⇉Sync](sync.md)` and `[¬Sync](sync.md)` are ordinary links, compiled with the mark kept as text, and so is `[¬⇉ Sync](sync.md)`. One link states one operator: text opening with any two operators, as in `[¬ ⇉ Sync](sync.md)` or `[⫽ ⇉ Sync](sync.md)`, fails with `E_UNSUPPORTED_CONSTRUCT` naming the link, and so does `⇉` naming anything but a Markdown document or section under the root, as a deferred link does. Every budget holds per bundle: `-E` counts hops from each bundle's entry, and the others count what each bundle alone opens, reaches and publishes. A chain of dispatches reaching a fourth hop from the entry warns. A chain returning to a bundle already on it is a cycle and fails, as do a dispatch in a level-6 section, which leaves no level for its sub-section, and an authored heading equal to one pf emits in the same bundle — `Prosiform`, `Dispatch in parallel` or a sub-section's. A dispatched link naming the document that writes it, by fragment or by path, warns where it closes no cycle. A target's shape is the corpus's convention: one carrying no numbered step compiles with no diagnostic.
- **Parallel dispatch links:** link text starting with `⫽` followed by a space is a dispatch: its target is required to exist, adds nothing to the bundle carrying the link, and compiles to a bundle of its own under the rules above, its hops counted with `⇉` hops. The `⫽` links in one section's own content are one set, and a child section's links form its own. Each is published without its mark and points at the section's one `Dispatch in parallel` sub-section, one level below the section, after its own content and its `Dispatch <link text>` sub-sections and before its child sections, which lists each target's bundle file once with the first link's text. A set states no order, and its targets' shape is the corpus's convention: a target holding a paragraph, a numbered list or an item linking no document compiles with no diagnostic. A mark with no space after it opens no operator, so `[⫽Reviews](plan.md#reviews)` is an ordinary link. `⫽` naming anything but a Markdown document or section under the root fails with `E_UNSUPPORTED_CONSTRUCT`, as the other operators do.
- **Invalid input:** invalid UTF-8, unterminated or invalid frontmatter, invalid conversion metadata, conflicting group depths, raw HTML, unsupported dependency/section-naming constructs, a link operator naming no Markdown document/section under the root, missing in-root documents/sections (deferred and dispatched targets included), a cycle of dispatches, a dispatch in a level-6 section, or an authored heading equal to one pf emits return `1` with the defect and source location.

## Output

A run publishes its bundles into a folder of its own, named for its entry with the `.bundles` suffix, under the folder `-o DIR` names, which must exist, or under the working directory when `-o` is absent. A selection's name is its path relative to the working directory, without the Markdown suffix, with each separator written as `_`; a section adds `__` and the fragment. A run of several distinct selections joins their names with `+` in the order the command line first names each; equivalent references count once. The joined name with `.bundles` names the run's folder, and with `.bundle.md` the entry's bundle in it, so `pf modes/plan-mode.md 'artifacts/epic.md#delivery-findings'` publishes `modes_plan-mode+artifacts_epic__delivery-findings.bundles/modes_plan-mode+artifacts_epic__delivery-findings.bundle.md`. Each dispatched target's bundle sits in the same folder under its own selection's name, as `modes_sync-mode.bundle.md`. The folder is written whole beside the earlier one and swapped in, so a reader sees one run's set or the one before it, never a mixture; nothing else under `-o DIR` is touched, an author folder named like the entry included. A run folder holding a source the run reads is invalid usage, and so is `-o -`: standard output carries no bundle.

File and directory names use hyphens rather than underscores. A path separator is written as `_` in that derived name, and an underscore in the source path is written as `_` there too, so a hyphen keeps a directory boundary visible in the filename. A source path that contains an underscore remains valid and compiles.

Stdout contains an informational response or nothing. A bundle opens on its first group's content; an instruction to follow an entry belongs in that source's own preamble.

Diagnostics use stderr: text by default; `-d json` emits one JSON object per line.
Warnings accompany a published bundle and exit `0`. `W_COINCIDENT_HEADING` names generated headings that read alike but for capitalization — two file headings, or two member headings of one merged group — once per set, with the shared text, a `location` for the first source and a `related` location for each other. Headings an author repeats raise no warning. `W_DISPATCH_DEPTH` names a chain of dispatches reaching a fourth hop, once per target the entry dispatches, at the first link dispatching it: `location` is that link, `related` locates each later hop's link and the target it dispatches, and `chain` names the entry and every hop's target. The depth limit is fixed. `E_DISPATCH_CYCLE` refuses a chain returning to a bundle already on it, the entry's included, with the same fields. `W_DISPATCH_SELF` names a dispatched link naming its own document, with the link as `location` and the target as `resolved`. `W_RESOURCE_PORTABILITY` reports a bundle naming a resource.
Use exit status to determine the outcome:

| Exit | Meaning |
| --- | --- |
| `0` | successful compilation, validation, or informational response |
| `1` | input, dependency, policy, safety, or resource-limit failure |
| `2` | invalid usage or option combination |
| `3` | output publication or delivery failure, a broken pipe among them |
| `4` | unexpected internal error |

A failed run publishes nothing. Halt and surface its diagnostic; reading the sources itself is unsupported.

## Supported environment

The supported environment is POSIX (Linux, macOS). Root confinement rests on rooted, no-follow source access using `O_NOFOLLOW`, `O_DIRECTORY`, `O_CLOEXEC`. Refuse symbolic links below the root; refuse startup if these flags are unavailable.
