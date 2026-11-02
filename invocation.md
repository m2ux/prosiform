# Invocation

Compile local Markdown entries and their dependencies into one validated bundle, and each target they dispatch into a bundle of its own.

```text
pf [OPTIONS] REF [REF ...]
pf
```

## Guide

`pf` with no arguments prints the guide to standard output and exits `0`. It states the compile step, `pf -o <folder> <destination>` run from the skill's directory, which holds `SKILL.md`, with a non-zero exit stopping the run and reporting its diagnostics; that a link whose text opens with `↳` names an inline target, which is compiled, read whole and followed; and that a bundle opening with a Prosiform section is followed from there. A skill's bootstrap is therefore one instruction: run `pf` and follow it. No option prints the guide, `pf -h` names the bare command, and arguments naming no entry reference are invalid usage.

## Options

Flags are case-sensitive.
`pf -h` and these tables agree; `make invocation` verifies them. The profile is `skill-markdown-v4`, which `-v` reports beside the version. A conformance run's fault is not an option: the run reads it from its environment, as the design's [Conformance faults](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md#conformance-faults) section states.

| Option | Effect |
| --- | --- |
| `REF` | document or document#fragment; paths from cwd |
| `-m, --mock ORIGINAL=ALTERNATIVE` | redirect one reference to the document or section the run reads instead, given once per pairing; both sides read from the working directory; repeatable; default none |
| `-o DIR` | folder the run's own folder of bundles is written into, made if absent, swapped in whole; default: the working directory |
| `-c` | discover, bundle, validate; publish nothing; accepts -o |
| `-d {text,json}` | stderr diagnostics; default text |
| `--budget NAME=VALUE` | set the budget NAME to VALUE, a positive decimal integer, given once per budget; repeatable; the budgets, their defaults and what each counts are listed below |
| `-C, --codes` | list this build's error and warning codes |
| `-v, --version` | tool version and profile identifier |
| `-h, --help` | usage, defaults and exit statuses |

### Budgets

Each budget fails the run rather than truncating a bundle, and holds per bundle. An entry naming a budget outside these, an entry carrying no `=`, an empty name or a value that is no positive decimal integer, a budget named twice, and `nesting` below 2 are each invalid usage.

| Budget | Effect |
| --- | --- |
| `files` | default 256; distinct source documents opened |
| `file-bytes` | default 1048576; raw bytes in one source |
| `input-bytes` | default 16777216; raw source bytes, counted once per source |
| `output-bytes` | default 262144; bytes of the complete bundle |
| `targets` | default 4096; distinct document and section targets discovered |
| `links` | default 32768; authored link and image occurrences in selected content |
| `nesting` | default 64; levels of container nesting and, independently, YAML collection nesting in one source; at least 2 |
| `depth` | default 8; link hops from the nearest entry reference |

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

A document declares `prosiform` in leading YAML frontmatter to be compiled. Every key of the mapping is a preset name holding a mapping of settings, and a key holding anything else is refused. The `default` preset is in force wherever the document is compiled. A preset whose name appears as a whole word, in any case, in the title of the section holding the link that reaches the document is in force above it; a command-line entry matches the title of the section it names, or the document's own title. The presets in force decide the one group the document joins and its depth (`group`), a selected preset's pair holding over `default`'s; [Sources](docs/sources.md) states what a `subst` entry holds. They govern the document's own content alone: a file's `group` pair places its own sections wherever a parent bundles it, and the parent's pair places the parent's sections where a further link bundles the parent in turn. `prosiform: {}` declares with no preset. A file whose presets in force name no group keeps a group of its own. A `root` key is refused. A preset no reference of the run selected warns with `W_PRESET_UNUSED`, and the run publishes.

```yaml
---
prosiform:
  default:
    group: {rules: 2}
  checks:
    group: {checks: 1}
    subst: [{steps.md: strict-steps.md}]
---
```

A link under a section titled `Release checks` puts `default` and `checks` in force: the `checks` pair holds over `default`'s, so the document joins `checks` at depth 1. Any other link puts `default` alone in force, joining the document to `rules` at depth 2.

A link places a document under one group. Two links selecting different pairs place it in each of their groups, and it is emitted under each. Contributing files declaring the same group must agree on depth.

A named group nests inside the division of the document whose link placed its first member, one heading level deeper per enclosing division, and a heading pushed past H6 fails the run with `E_HEADING_DEPTH_OVERFLOW`. [Hierarchy](docs/hierarchy.md#where-a-group-stands) states where each group stands and what an author changes when nesting overflows.

[Sources](docs/sources.md) states the frontmatter grammar, the declaration, the fields, the derived boundary and the metadata codes.

## Bundling

Entry references select whole documents or named sections, a section written as `document#fragment`, and each names a document that declares `prosiform`. A fragment alone names no document and is invalid usage. Each local Markdown link resolves from the file that writes it and is followed when its target declares, wherever that target sits, until nothing new is reachable; everything else stays as authored. The working directory bounds entry references and the paths diagnostics name. Operators on a link's text withhold it instead: `¬` defers it to another run, `⇉` dispatches it to a sub-agent, and `⫽` dispatches it alongside the other `⫽` links of its section.

A mapping entry redirects what a reference names. `-m ORIGINAL=ALTERNATIVE`, given once per pairing, matches a key against the identity a reference normalizes to and names the document or section the run reads in its place; a key carrying a fragment redirects that section alone and takes precedence over a key naming the whole document. Both sides resolve from the working directory, wherever the source whose link names it sits. The substitute is the target outright: its title, its group and its own links are the ones the bundle carries, as if the author had written its path in the link. Every reference is redirected — an entry reference and a compiled, deferred, dispatched or parallel-dispatched target alike, a reference naming a declaring document and one carried as a citation — and a run states each redirected target and each key no reference named, publishing either way.

The bundle is arranged in file headings and groups, its headings take destinations, and its dispatched targets become bundles of their own. Nothing is published until every bundle has been validated.

- [References](docs/references.md) — classification, operators and diagram links
- [Selection](docs/selection.md) — closure, consolidation and order
- [Hierarchy](docs/hierarchy.md) — file headings, groups and depth
- [Destinations](docs/destinations.md) — slugs, ordinals and rewriting
- [Dispatch](docs/dispatch.md) — sub-sections, the Prosiform section and cycles
- [Validation](docs/validation.md) — invariants, codes and budgets

## Output

A run publishes its bundles into a folder of its own, named for its entry with the `.bundles` suffix, under the folder `-o DIR` names, made if absent, or under the working directory when `-o` is absent. The folder is swapped in whole, so a reader sees one run's set or the one before it.

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

The supported environment is POSIX (Linux, macOS). Working-directory confinement rests on rooted, no-follow source access using `O_NOFOLLOW`, `O_DIRECTORY`, `O_CLOEXEC`. Refuse symbolic links along a source's path; refuse startup if these flags are unavailable.
