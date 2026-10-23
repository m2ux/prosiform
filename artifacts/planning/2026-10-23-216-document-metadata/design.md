# Per-File Conversion Metadata

## Scope

Each source owns its structural conversion settings. The current structural option is grouping (`-g SLUG:DEPTH`). Source roots, entry selection, referrer context, output destination, diagnostic mode, validation mode, fault injection and budgets remain invocation parameters.

The proposed contract below is a design recommendation grounded in the user's per-file decision. The user requested a new Field Refinement epic. Its task files and epic body define delivery; priority 6 schedules it ahead of Section Composition at 5.

## Metadata Contract

Use the Agent Skills extension field, whose keys and values are strings:

```yaml
---
name: artifact-rules
description: Rules for authoring artifacts.
metadata:
  prosiform-group: artifacts
  prosiform-group-depth: "2"
---
```

`name` and `description` illustrate an actual skill document. Prosiform accepts ordinary Markdown and does not require those fields or a `SKILL.md` filename.

| Field | Meaning | Validation |
| --- | --- | --- |
| `metadata.prosiform-group` | The named group this file joins | Nonempty slug using the existing grouping slug grammar |
| `metadata.prosiform-group-depth` | Source heading level at which this file contributes sections to its group | String containing one decimal digit from `1` through `6` |

Both fields are present together or absent together. Absent conversion metadata means the file retains its individual file group. An empty frontmatter block is equivalent to absent metadata. Unknown keys beginning `prosiform-` are input errors; unrelated metadata has no conversion meaning. No schema version, profile registry, raw command string or arbitrary argument list is introduced.

Group membership is explicit, independent of a directory name. Files in different directories can opt into the same group. A sibling without the fields remains ungrouped. Matching a directory or a group name discovers no additional files. Group identity uses the exact declared slug; rendered title and anchor handling follow the existing output rules.

Contributing files with the same group must declare the same depth. A disagreement fails with the group, both declarations and their source locations. There is no caller priority or traversal-order winner. Supporting multiple source depths within one merged group would be a separate renderer capability.

## Source Interpretation

1. Read and capture the source once through the existing rooted, no-follow reader. Parse frontmatter from those captured bytes and retain original source locations.
2. Preserve the current BOM, LF/CRLF, opening `---` and closing `---`/`...` recognition. Parse a present block as YAML; an unterminated block remains an input error.
3. Use an established safe YAML parser. The runtime currently depends only on `markdown-it-py`, so justify and pin the YAML dependency and its lockfile. Verify its documented scalar typing, duplicate-key detection, source marks and resource behavior before selecting it; do not implement YAML by hand.
4. Require a mapping for nonempty frontmatter and a string-key/string-value mapping when `metadata` is present. Reject duplicate mapping keys, custom tags, aliases and merge keys with source diagnostics. Bound parsing under the source-byte and nesting limits, including before constructing deeply nested structures.
5. Decode the reserved fields into an immutable per-source conversion value. Retain the body's original line mapping. Other skill fields remain metadata, not instructions or dependency links.
6. Keep metadata out of rendered content, heading discovery, Markdown dependencies and reference definitions. Raw byte accounting and capture hashes include the complete source, including metadata.

Malformed YAML is an input failure even when it contains no Prosiform keys. This is a deliberate source-language contract: the present implementation discards arbitrary text inside a delimited block. Update those fixtures and document the accepted metadata grammar without introducing a legacy parsing path.

## Selection and Assembly

- A whole-document entry, a fragment-only entry with referrer, a normal link and a transitive link obtain settings from the destination file's source record.
- File metadata applies to any selected section even though the frontmatter lies outside that section. Parent Markdown prose and sibling sections are not implicitly selected.
- A source reached repeatedly has one metadata value and the existing union of selected regions. Cyclic ordinary dependencies retain their existing termination behavior.
- Validate metadata syntax and local field values whenever the normal source reader opens a file, including a deferred target opened for destination validation. Only contributing documents participate in group aggregation and cross-file depth conflicts.
- A deferred-only target contributes no content or group membership; activating it in a later compilation reads its own settings. Its caller supplies no inherited settings.
- External, outside-root and non-Markdown references retain the current reference classification. Metadata does not cause them to be fetched.
- Aggregate explicit membership after closure selection, then pass validated groups to the existing grouping renderer. Preserve deterministic root-relative ordering, member identity, overview placement and destination rewriting.
- Keep shortest-distinguishing member names valid when group names are unrelated to source directories. Cover duplicate basenames across directories and a group heading colliding with another generated heading.
- Candidate validation receives the same per-source grouping decisions as rendering and checks preserved source coverage and outline against them.

## CLI and Diagnostics

Remove `-g`, its parser, the global rule map, directory matching, idle-rule warnings and associated declarations whose only purpose is CLI grouping. Do not add aliases, precedence rules or a metadata/CLI fallback. A retired structural flag receives the existing invalid-usage result, exit `2`.

Malformed or inconsistent source metadata receives exit `1`, structured source coordinates, and a documented diagnostic code. Assign the codes in the contract before fixtures or implementation. Metadata failure publishes no partial output and leaves an existing output file intact. Text and JSON diagnostics identify the field; group conflicts identify both sources deterministically.

## Delivery Sequence

These are architectural stages; the epic table splits them into component-scoped task identities. Each unit carries its own tests and documentation. Delivery integrates the contract and compiler through their existing owning branches; the metadata feature becomes the public interface only when its complete acceptance set passes.

| Unit | Deliverable | Prerequisite | Verification |
| --- | --- | --- | --- |
| Contract | Metadata grammar, ownership, grouping rules, diagnostics and conformance cases | Confirmed plan placement | Requirement review against the decisions and fixture matrix below |
| Source Model | Bounded YAML parsing, typed per-file settings and source locations | Contract | Parser and reader tests; source byte/hash/coordinate regressions |
| Compilation | Explicit group membership, conflict handling, candidate validation and structural CLI removal | Source Model | End-to-end compilation, deterministic output, rewritten-link and atomic-output checks |
| Consumers | Active corpus, examples, command documentation, checks and authoring guidance use metadata | Compilation | Full repository checks against the identified build; installed-wheel smoke |

The Source Model unit can introduce the complete validated source model without switching assembly until the Compilation unit. Compilation updates directly affected grouping fixtures and invocation checks in the same unit so no delivered intermediate unit has failing checks. Consumers covers the wider corpus audit and release evidence, not postponed fixes required for compilation to work.

## Verification Matrix

| Observable outcome | Required cases |
| --- | --- |
| A file controls its own arrangement | Direct entry, ordinary link, transitive dependency and section-fragment selection of the same file |
| Metadata is local | Entry settings do not affect a linked file; unannotated sibling stays individual; unrelated directory names remain valid |
| Shared groups are coherent | Matching declarations merge; conflicting depths fail with both source locations; discovery order does not change the diagnostic |
| Repeated reachability is stable | Diamond dependency, overlapping fragments, ordinary cycle and entry-order permutations |
| Deferred settings take effect only for contributions | Deferred-only file, later direct activation, and a file reached by both deferred and ordinary links |
| YAML interpretation is explicit | Empty/absent block; malformed YAML; nonmapping root; invalid metadata types; missing paired field; unknown reserved field; duplicate keys; out-of-range and non-string depth |
| Metadata parsing remains bounded | Custom tags, aliases, merge keys, deep nesting, raw byte limit and source-change capture |
| Metadata stays outside the body | Apparent Markdown links and headings in metadata; fenced YAML in body; BOM, CRLF and physical diagnostic coordinates |
| Output retains source meaning | Existing overview/variant cases, shortest member names, heading overflow, duplicate source slugs, anchor collisions and rewritten document/section links |
| Failure publishes nothing | Bad metadata and group conflict under stdout, file output and check mode; existing output file preserved |
| CLI has one structural source | `-g` rejected; retained operational flags still work; help and invocation table agree |
| Published package exercises the contract | Updated corpus and `make check` with `PROSIFORM_BUILD` set to the identified candidate; installed-wheel smoke |

Freeze baseline fixture outputs at the recorded main revision. For representative grouped cases, add explicit metadata to exactly the baseline's contributing members and compare resulting bundle bytes; the metadata declarations replace only the source of grouping decisions. Add negative cases independently from the new parser and assembler. No claim of conformance rests solely on tests inspecting their own implementation.

## Consumers and Related Work

- Update the normative design, glossary, invocation table, package README, active examples, fixture inputs/manifests, grouping/source tests, diagnostic inventory and conformance checks. Search active prose for claims that metadata is ignored, rules are directory-wide or grouping comes from flags.
- Historical run captures retain their original commands and outputs. Active run instructions must describe the current interface.
- The planned authoring skill in issue #208 must teach the resulting contract when implemented. Record this dependency without implementing the skill here.
- Nested-folder layout (#196) and Unicode call-site section composition (#215) remain separate features. They share grouping/selection surfaces, so implementation must inspect their landing status before selecting its base. This plan adds neither behavior.
- The Rust compiler initiative consumes the eventual tagged contract. Updating its implementation is outside this Python refactor; record the changed source-language requirements for its existing contract handoff.
