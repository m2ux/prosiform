# Link-Tag Presets

## Goal

An authored Markdown link identifies both the content to compile and the target document's named presets. An agent compiles that link through an explicit command, and one entry publishes a validated set of bundles whose dispatched selections remain distinct.

## Link and Command

```markdown
[Plan Report](guide.md#plan-report "checks,draft")
```

```sh
pf --entry guide.md#plan-report --tags checks,draft
pf --entry guide.md#plan-report
```

The second command selects `default` alone. The destination is resolved relative to the invocation directory; an agent resolves a link relative to its authoring document before choosing that directory and command path. `--tags` carries the whole comma-separated list as one shell argument, quoted when needed. A fragment-only authored link is qualified with its containing document in the command.

## Selection

The parser supplies a Markdown link's title separately from its visible label and containing heading. A single tag-list reader serves source links and CLI arguments. It splits on commas, trims whitespace, discards empty tokens and duplicates, and compares the complete tokens case-insensitively with the target document's preset names. It applies every matching preset in declaration order above `default`. Unknown tokens select nothing and emit no unknown-tag diagnostic. `default` is implicit and selecting it adds nothing.

An empty or absent list selects no named preset. `checks` selects `checks`, while `Checklist`, a containing heading `Checks`, and a link label `Checks` select nothing by that spelling alone. `Checks and Draft` is one token and only matches a preset with that complete name. The list syntax has no quoting or escape grammar for a comma within a preset name.

A selected preset's `group` pair and `subst` alternatives retain their current precedence over `default`. Selected named presets retain the existing union and conflict refusals. Each document's presets govern its own content; its outgoing links select the next document through their own titles. Existing substitution accumulation within one bundle remains in force. Existing unused-preset warnings remain; silence for unknown tags does not waive a declared preset's unused warning.

Markdown inline and reference-style links, including preamble links and operator-marked links, carry tags. Images and external references remain resources. Mermaid link destinations select the target's `default`; interpreting Mermaid tooltip text as a tag list is outside this epic.

## Occurrences and Deferred Runs

Reference occurrence metadata carries normalized tags separately from the heading title needed for composition placement. Substitution preserves the occurrence's tag selection while changing its resolved destination; the substitute's own presets answer that selection. Traversal retains distinct selecting occurrences while source capture still reads each physical document once per bundle.

A deferred link retains its title when published. The guide tells an agent to compile its destination with the same `--tags` list. Heading equality supplies no selection guarantee; the deferred-composition refusal comparing the two headings' keyword matches has no role in explicit selection and is retired. Immediate and deferred compilation of an equivalent occurrence select the same presets.

## Bundle Variants

A bundle identity comprises its document, optional fragment, and canonical effective named-preset set. Only presets actually matched on that destination enter the set. Reordering, case changes, repetitions, unknown tags and explicit `default` cannot manufacture another identity. Two distinct effective selections of one destination compile separately, with their own grouping and substitution mappings and per-bundle budgets.

The ordinary destination-derived name identifies an empty named selection. A nonempty selection adds a deterministic, filesystem-safe qualifier derived from the canonical preset set. Names do not depend on traversal order or process hash randomization. Publication detects a filename collision rather than replacing a different variant. Every dispatch and parallel-set item points at its selected variant; equal variants share one file. Dispatch cycle and depth analysis identifies the same variants that compilation schedules, and existing budget and atomic-publication gates apply to the complete set.

## Agent Guide and Consumers

The one guide printed by bare `pf` states how an agent translates the destination and title to `pf --entry REF --tags TAGS`, omitting `--tags` for an empty list. It includes relative-file and same-file-fragment examples and shell quoting. Bundle instruction headings continue to point readers to that guide. Bundles carry no duplicate guide protocol.

The command's help, invocation tables, smoke and corpus runners, fixtures, checked examples, renderer examples and eval command builders use the single-entry grammar. Any existing multi-entry example is expressed by an authored entry document linking its inputs. Eval expectations account for tag-preserving deferred compilation and variant output names. Deterministic harness tests validate command expectations without a new paid baseline or a paid live agent run.

## Delivery Boundary

The engineering design clause and its conformance vocabulary state this selection contract. Main-branch source, fixtures, docs and eval callers consume it together through the epic's task sequence. The existing source-declaration grammar, bundle directory publication, operator meanings and preset setting types remain their owning contracts. This epic adds selection variants where a run must distinguish them; it does not introduce a second bundle-publication mechanism.
