# Invocation

Compile local Markdown entries and their dependencies into one validated bundle, and each target they dispatch into a bundle of its own.

```text
pf [OPTIONS] REF [REF ...]
pf
```

## Guide

`pf` with no arguments prints the guide to standard output and exits `0`. It states the compile step, `pf -o <folder> <destination>` run from the skill's directory, which holds `SKILL.md`, with a non-zero exit stopping the run and reporting its diagnostics; that a link whose text opens with `↳` names an inline target, which is compiled, read whole and followed; and that a bundle opening with a Prosiform section is followed from there. A skill's bootstrap is therefore one instruction: run `pf` and follow it. No option prints the guide, `pf -h` names the bare command, and arguments naming no entry reference are invalid usage.

## Options

Flags are case-sensitive. Budgets are positive decimal integers; zero is invalid.
`pf -h` and these tables agree; `make invocation` verifies them. The profile is `skill-markdown-v4`, which `-v` reports beside the version.

| Option | Effect |
| --- | --- |
| `REF` | document, document#fragment, or #fragment with -f; paths from cwd |
| `-f DOC` | working-directory-relative document for fragment-only references |
| `-o DIR` | existing folder the run's own folder of bundles is written into, swapped in whole; default: the working directory |
| `-c` | discover, bundle, validate; publish nothing; accepts -o |
| `-d {text,json}` | stderr diagnostics; default text |
| `-x {source-changed,internal,cleanup-refused}` | inject a conformance run fault no source tree expresses; default none |
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

A source declares its root, group and depth in leading YAML frontmatter. Group and group-depth occur together; a file declaring neither keeps a group of its own.

```yaml
---
prosiform:
  group: rules
  group-depth: 2
---
```

Contributing files declaring the same group must agree on depth.

[Sources](docs/sources.md) states the frontmatter grammar, the fields, the root's meaning and the metadata codes.

## Bundling

Entry references select whole documents or named sections. Each local Markdown link under its author's root is followed until nothing new is reachable; everything else stays as authored. Operators on a link's text withhold it instead: `¬` defers it to another run, `⇉` dispatches it to a sub-agent, and `⫽` dispatches it alongside the other `⫽` links of its section.

The bundle is arranged in file headings and groups, its headings take destinations, and its dispatched targets become bundles of their own. Nothing is published until every bundle has been validated.

- [References](docs/references.md) — classification, operators and diagram links
- [Selection](docs/selection.md) — closure, consolidation and order
- [Hierarchy](docs/hierarchy.md) — file headings, groups and depth
- [Destinations](docs/destinations.md) — slugs, ordinals and rewriting
- [Dispatch](docs/dispatch.md) — sub-sections, the Prosiform section and cycles
- [Validation](docs/validation.md) — invariants, codes and budgets

## Output

A run publishes its bundles into a folder of its own, named for its entry with the `.bundles` suffix, under the folder `-o DIR` names, which must exist, or under the working directory when `-o` is absent. The folder is swapped in whole, so a reader sees one run's set or the one before it.

File and directory names use hyphens rather than underscores. A path separator is written as `_` in the derived name, so a hyphen keeps a directory boundary visible in the filename.

[Bundles](docs/bundles.md) states the derived names, publication and delivery in full.

## Diagnostics

Diagnostics use stderr: text by default; `-d json` emits one JSON object per line. Warnings accompany a published bundle and exit `0`. `E_DISPATCH_CYCLE` refuses a chain returning to a bundle already on it, the entry's included.

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
