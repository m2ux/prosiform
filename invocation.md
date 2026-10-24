# Invocation

Compile local Markdown entries and their dependencies into one validated bundle.

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
| `-o FILE` | atomic validated output to FILE; -: stdout; default: derived filename |
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
| `-C` | list this build's error and warning codes |
| `-v` | tool version and profile identifier |
| `-h` | usage, defaults and exit statuses |

## Examples

Run from the repository root; [worked examples](example/README.md) show input and output.

```bash
cd example/work-tracker
pf modes/plan-mode.md
pf 'artifacts/epic.md#delivery-findings'
pf -o context.md modes/plan-mode.md
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

Frontmatter starts on the first physical line with exactly `---` and closes at the next line exactly `---` or `...`; an optional byte-order mark may precede the opener. A leading blank line makes the following content part of the body. The block is empty or contains one YAML 1.2 Core mapping. Its top-level keys are strings; `prosiform`, when present, is a mapping with string keys. Keep standard skill fields such as `name` and `description` at the top level; ordinary Markdown requires neither field nor a `SKILL.md` filename. The only keys in `prosiform` are `root`, `group`, `group-depth`, `group-heading` and `dispatch`; unknown keys fail validation. `group-heading` is a boolean and is valid only together with `group` and `group-depth`. Absent, or `true`, the group name is emitted as the group's H1. `false` omits that heading, and the sections at `group-depth` stay at H2. Every member of a group declares the same value. `dispatch` is a nonblank, printable single-line string stating what a dispatch-marked link means for that skill; the compiler assigns it no structure and emits it after the entry sentence in the bundle's opening line. Every contributing source declares the same value, and a second value fails with `E_INVALID_CONVERSION_METADATA` naming both locations. Unrelated fields, including `metadata`, have no conversion meaning. An optional `root` is a nonempty relative directory-path string using forward slashes; controls, absolute or drive paths, URLs, home shortcuts and environment expansion fail validation. The captured value retains its spelling and original location. An explicit root resolves from the declaring file's directory. Every absent root uses the working directory captured at invocation start. Root is independent of group and group-depth. Positional files and `-f` resolve from that same working directory, with bounded parent-directory bootstrap permitted. The `-r` option is invalid usage.

Duplicate keys, aliases, merge keys and custom tags are invalid throughout the frontmatter. Frontmatter bytes count toward the source byte budgets, and YAML collections obey `-N` independently of Markdown containers. Frontmatter supplies no rendered content, links or headings.

Contributing files declaring the same group must agree on depth. A conflict reports both declarations and publishes nothing. Deferred-only files are validated but contribute no group membership. Each selected destination supplies its settings once, whether reached directly, by fragment or through several callers; declarations do not propagate to siblings or dependencies.

Metadata errors return exit status `1`: `E_INVALID_FRONTMATTER` identifies invalid YAML, `E_INVALID_CONVERSION_METADATA` identifies invalid fields, and `E_GROUP_DEPTH_CONFLICT` identifies conflicting contributing declarations. Diagnostics locate the original source; JSON diagnostics include `location` and, for conflicts, `related` locations. Existing output files remain intact on failure.

## Bundling rules

- **Sources:** valid UTF-8; validate leading frontmatter as bounded YAML 1.2 Core and retain each file's conversion metadata; parse the body after one leading byte-order mark and frontmatter block as `skill-markdown-v1`.
- **Closure:** entries select whole documents or named sections. Follow local Markdown links from each authoring source's effective root, until no new dependencies remain. Compiled links target bundle headings. Outside-root links stay authored and contribute nothing.
- **Groups:** each contributing document uses its title-cased root-relative path as its group heading unless its metadata declares a group. Merged groups use title-cased declared names. Member subsections contain content above grouping depth, under `Overview` when merged sections also occur at grouping depth, otherwise directly under the group. Members have distinct destinations and shortest-distinguishing-path, title-cased headings. Authored headings and filesystem paths retain their spelling.
- **Deferred links:** link text starting with `¬` requires an existing document/section but adds no content through that link. Emit the link's text without the marker and the spaces following it, because the destination already states the deferral, and emit a URI-escaped working-directory-relative destination for a separate run.
- **Dispatched links:** link text starting with `»` withholds the compilation exactly as a deferred link does, requires an existing document/section, and adds no dependency or group membership. The mark is published, because it is what tells a reader the material belongs to another agent, and the destination is the same URI-escaped working-directory-relative path a deferred link carries. One link states one operator: text opening with both `¬` and `»` fails with `E_UNSUPPORTED_CONSTRUCT` naming the link.
- **Invalid input:** invalid UTF-8, unterminated or invalid frontmatter, invalid conversion metadata, conflicting group depths, raw HTML, unsupported dependency/section-naming constructs, document paths differing only by Markdown extension, or missing in-root documents/sections (deferred targets included) return `1` with the defect and source location.

## Output

One normalized entry publishes a file in the working directory. The name is that entry's path relative to its effective root, without the Markdown suffix, with each separator written as `_`, then `.bundle.md`. A section inserts `__` and the fragment before that suffix. Distinct selections require an explicit `-o` destination. `-o FILE` names an exact file and `-o -` selects stdout.

File and directory names use hyphens rather than underscores. A path separator is written as `_` in that derived name, and an underscore in the source path is written as `_` there too, so a hyphen keeps a directory boundary visible in the filename. A source path that contains an underscore remains valid and compiles.

Stdout contains that bundle when `-o -` selects it, an informational response, or nothing. A bundle opens by telling the agent to follow the selected entries:

```markdown
Follow [Plan](#plan). The other sections are material that procedure references.
```

An entry document declaring `prosiform.dispatch` adds that text after the entry sentence, in the same paragraph, so a reader meets the rule that governs the marked links and the entries as one instruction. Absent the key, the opening line is the entry sentence alone.

Diagnostics use stderr: text by default; `-d json` emits one JSON object per line.
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
