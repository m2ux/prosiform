# Invocation

Compile a document or section and its local Markdown dependencies into one validated bundle.

## Options

`prosiform --help` lists options, defaults, and exit statuses. The tables below match that output; `make invocation` verifies them.

| Option | Effect |
| --- | --- |
| `REF` | an entry reference: a root-relative document, a document and a fragment, or a fragment alone with --from |
| `--root DIR` | the allowed source root; required, and resolved from the working directory |
| `--from DOC` | the root-relative referring document a fragment-only reference resolves against |
| `-o, --output FILE` | publish the validated bundle to FILE, atomically; default or - is standard output |
| `--group SLUG:DEPTH` | merge every document under a directory named SLUG at source heading level DEPTH, 1 through 6; repeatable, once per slug |
| `--check` | discover, bundle and validate without emitting or publishing the bundle; accepted with --output |
| `--diagnostics {text,json}` | the diagnostic format on standard error; default text |
| `--fault {source-changed,internal}` | perform a fault on the run itself, so a conformance run reaches an outcome no source tree states; none by default |
| `--max-files N` | the budget of distinct source documents opened; a positive decimal integer, default 256 |
| `--max-file-bytes N` | the budget of raw bytes in one source; a positive decimal integer, default 1048576 |
| `--max-input-bytes N` | the budget of raw source bytes, counted once per source; a positive decimal integer, default 16777216 |
| `--max-output-bytes N` | the budget of bytes of the complete bundle; a positive decimal integer, default 262144 |
| `--max-targets N` | the budget of distinct document and section targets discovered; a positive decimal integer, default 4096 |
| `--max-links N` | the budget of authored link and image occurrences in selected content; a positive decimal integer, default 32768 |
| `--max-nesting N` | the budget of levels of container nesting in one source; a positive decimal integer, default 64 |
| `--max-expansion-depth N` | the budget of link hops from the nearest entry reference; a positive decimal integer, default 8 |
| `--codes` | report the error and warning codes this build can emit |
| `--version` | report the tool version and the profile identifier |
| `--help` | show this usage, the defaults, and the exit-status meanings |

Resource budgets must be positive decimal integers. Zero is invalid.

## Examples

Run these from the repository root. See [worked examples](example/README.md) for input and output excerpts.

### Bundle a procedure

```bash
prosiform --root example/work-tracker modes/plan-mode.md
```

### Select a section

```bash
prosiform --root example/work-tracker 'artifacts/epic.md#delivery-findings'
```

### Merge directories

```bash
prosiform --root example/work-tracker \
  --group artifacts:2 --group modes:2 \
  modes/plan-mode.md
```

### Validate without publishing

```bash
prosiform --root example/work-tracker --check modes/plan-mode.md
```

## Bundling rules

### Source preparation

Sources must be valid UTF-8. The build removes one leading byte-order mark and one leading frontmatter block, then parses the content under `skill-markdown-v1`.

### Selection and dependencies

- Each entry selects a whole document or a named section.
- Links to local Markdown under `--root` resolve relative to the source document and are followed until no new dependencies remain.
- Each contributing document forms a group headed by its root-relative path, unless `--group` merges it.
- Compiled links point to headings in the bundle.
- Links outside the root remain as authored and contribute no content.

### Deferred links

A link whose text starts with `¬` defers compilation of its target. The target must exist, including any named section, but contributes no content through that link.

The emitted link preserves its text, marker, and following spaces. Its destination is relative to the allowed root, ready for a separate run.

### Invalid input

These failures return `1` with a diagnostic naming the defect and source location:

- Invalid UTF-8 or unterminated frontmatter.
- Raw HTML or unsupported dependency or section-naming constructs.
- Document paths that differ only by Markdown extension.
- Missing documents or sections referenced under the root, including deferred targets.

## Output

### Bundle and responses

Standard output contains the bundle, an informational response, or nothing. A bundle opens with links to its entry points:

```markdown
This bundle was built for [Modes/Plan-Mode](#modesplan-mode); everything else is material it references.
```

### Diagnostics

Diagnostics go to standard error. The default is text; `--diagnostics json` emits one JSON object per line.

### Exit statuses

Use the exit status to determine the outcome.

| Exit | Meaning |
| --- | --- |
| `0` | successful compilation, validation, or informational response |
| `1` | input, dependency, policy, safety, or resource-limit failure |
| `2` | invalid usage or option combination |
| `3` | output publication or delivery failure, a broken pipe among them |
| `4` | unexpected internal error |

### Failed runs

A failed run publishes nothing. The caller halts and surfaces the diagnostic; reading the sources itself is unsupported.

## Supported environment

The supported environment is POSIX: Linux and macOS.

Root confinement rests on rooted, no-follow source access using `O_NOFOLLOW`, `O_DIRECTORY`, and `O_CLOEXEC`. Symbolic links below the root are refused. The build refuses to start when these flags are unavailable.
