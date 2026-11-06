# Invocation

Compile one local Markdown entry and their dependencies into one validated bundle, and each target they dispatch into a bundle of its own.

```text
pf [OPTIONS] --entry REF [--presets PRESETS]
pf
```

## Guide

`pf` with no arguments prints the guide to standard output and exits `0`. It states the compile step, `pf -o <folder> --entry <document>[#<section>] [--presets <presets>]` run in the directory holding the source document, into a folder the run makes if it is not there, with a non-zero exit stopping the run and reporting its diagnostics; that a link whose text opens with `↳` names an inline target, which is compiled, read whole and followed; that a link whose text opens with `⇉` names a bundle given to a sub-agent, and one opening with `⫽` marks a dispatch set, whose members are given to their own sub-agents at once. Every bundle opens with the run-pf line, which tells its reader to run `pf` first. A document's bootstrap is therefore one instruction: run `pf` and follow it. The build requires no skill: any Markdown document declaring `prosiform` is a valid entry. No option prints the guide, `pf -h` names the bare command, and arguments naming no entry reference are invalid usage.

## Options

Flags are case-sensitive.
`pf -h` and these tables agree; `make invocation` verifies them. The profile is `prosiform-markdown`, which `-v` reports beside the version. A conformance run's fault is not an option: the run reads it from its environment, as the design's [Conformance faults](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md#conformance-faults) section states.

| Option | Effect |
| --- | --- |
| `--entry REF` | one document or document#fragment; paths from cwd |
| `--presets PRESETS` | comma-separated preset names for the entry; default: no named presets |
| `-o DIR` | folder the run's own folder of bundles is written into, made if absent, swapped in whole; default: the working directory |
| `-c` | discover, bundle, validate; publish nothing; accepts -o |
| `-d {text,json}` | stderr diagnostics; default text |
| `--budget NAME=VALUE` | set the budget NAME to VALUE, a positive decimal integer, given once per budget; repeatable; the budgets, their defaults and what each counts are listed below |
| `-C, --codes` | list this build's error and warning codes |
| `-v, --version` | tool version and profile identifier |
| `-h, --help` | usage, defaults and exit statuses |

Compilation requires exactly one `--entry` and accepts at most one `--presets`. Positional entries, repeated entry or preset options, `--presets` without an entry, and a complete Markdown-link expression as the entry are invalid usage and exit `2`. Informational invocations require no entry.

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

An agent encountering `[Plan Report](guide.md#plan-report "checks,draft")` supplies:

```text
pf --entry guide.md#plan-report --presets checks,draft
pf --entry modes/review.md#review --presets 'checks, final draft'
pf --entry guide.md#plan-report
pf --entry=-guide.md --presets=-checks
pf -c --entry guide.md#plan-report --presets checks,draft
```

Resolve the destination from the document carrying the link, then express it from the command's working directory. Qualify a same-document fragment with its document's path. Pass the link title as one shell argument, quoting spaces and shell metacharacters. Attach a value beginning with `-` to its option with `=`. Omit `--presets` when the title carries no tags.

The following commands use the checked source tree of a [preset fixture](fixtures/inclusion/a-link-title-selects-its-preset/manifest.toml):

```bash
cd fixtures/inclusion/a-link-title-selects-its-preset/source
pf --entry guide.md
pf -c --entry guide.md
```

## Conversion metadata

A document declares `prosiform` in leading YAML frontmatter. Every key is a preset name holding a mapping of settings. `default` applies wherever the document is compiled. A link's title supplies comma-separated complete preset names; `--presets` supplies the entry's names through the same grammar. Split on literal commas, trim surrounding Unicode whitespace, compare without case and ignore empty, repeated and unknown names. Headings and visible link labels select no presets.

Matching presets layer over `default` in declaration order and govern the destination document's own content. A selected `group` pair holds over `default`'s; [Sources](docs/sources.md) states what `subst` holds. Selected presets union their settings. Different group pairs in one selection, or conflicting alternatives for one document's substitution key, fail with `E_INVALID_USAGE`, naming both presets. [Selection](docs/selection.md#presets-in-force) gives the full rules. `prosiform: {}` declares with no preset; a document with no group pair keeps its own file group. A preset no compiled reference selected warns with `W_PRESET_UNUSED` and the run publishes.

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

A link such as `[Review](rules.md "checks")` selects `checks` above `default`: the document joins `checks` at depth 1. A link carrying no matching tag applies `default` alone, joining `rules` at depth 2.

A link places a document under one group. Two links selecting different pairs place it in each of their groups, and it is emitted under each. Contributing files declaring the same group must agree on depth.

A named group nests inside the division of the document whose link placed its first member in that group, one heading level deeper per enclosing division, and a heading pushed past H6 fails the run with `E_HEADING_DEPTH_OVERFLOW`. [Hierarchy](docs/hierarchy.md#where-a-group-stands) states where each group stands and what an author changes when nesting overflows.

[Sources](docs/sources.md) states the frontmatter grammar, the declaration, the fields, the derived boundary and the metadata codes.

## Bundling

Entry references select whole documents or named sections, a section written as `document#fragment`, and each names a document that declares `prosiform`. A fragment alone names no document and is invalid usage. Each local Markdown link resolves from the file that writes it and is followed when its target declares, wherever that target sits, until nothing new is reachable; everything else stays as authored. The working directory bounds entry references and the paths diagnostics name. Operators on a link's text withhold it instead: `¬` defers it to another run, `⇉` dispatches it to a sub-agent, and `⫽` dispatches it alongside the other `⫽` links of its section. A link whose text opens with `↳` and a space, as in `[↳ Inputs](read.md#inputs)`, is a composition directive: it places the section it names beneath the section that writes it, and `[¬↳ Inputs](read.md#inputs)` defers that placement to a run of its own.

A substitution is stated in a document, never on the command line: a preset's `subst` entry pairs a reference with the document or section the run reads in its place, as [Sources](docs/sources.md) states. A pair belongs to the document that declares it and redirects only the links that document writes, under the presets every reference reaching that document selects, and each side resolves from the declaring file. The [substitution mapping](docs/selection.md#the-substitution-mapping) states the lookup and the warnings a run reports.

The bundle is arranged in file headings and groups, composed sections stand beneath the sections that place them, its headings take destinations, and its dispatched targets become bundles of their own. Nothing is published until every bundle has been validated.

- [References](docs/references.md) — classification, operators and diagram links
- [Selection](docs/selection.md) — closure, presets in force, substitution, consolidation and order
- [Hierarchy](docs/hierarchy.md) — file headings, groups and depth
- [Composition](docs/composition.md) — directives, destination sections, contributions and deferral
- [Destinations](docs/destinations.md) — slugs, ordinals and rewriting
- [Dispatch](docs/dispatch.md) — dispatch links, dispatch-set sub-sections, the run-pf line and cycles
- [Validation](docs/validation.md) — invariants, codes and budgets

## Output

A run publishes its bundles into a folder of its own, named for its entry with the `.bundles` suffix, under the folder `-o DIR` names, made if absent, or under the working directory when `-o` is absent. The folder is swapped in whole, so a reader sees one run's set or the one before it. Standard output carries no bundle: the guide and the help, version and code-listing responses use it. `-o -`, which names standard output, and a run folder holding a source the run read are each invalid usage.

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
