# W04+W05 Validation

Source head: `bcd7dc8d6eb3098a700e011b541520d22e1886a3` on `i10/e07/w04-entries-select-presets-through`, based on `i10/e07/main` at `e058df86e511bcda66a0c210a236316c995f824c`.

Runtime design: [`795bbfb67c66b02193f0313138f59f18aa6c5274`](https://github.com/m2ux/prosiform/blob/795bbfb67c66b02193f0313138f59f18aa6c5274/artifacts/planning/2026-10-17-prosiform-v1/design.md).

Required gates: **passed**. The full behavior gate ran at `734c06a6eaaaa04ebe31182dc0ade74aea62db6c`; its original output is retained in [make-check.log](make-check.log). That run passed every target before conformance, which identified two fixture clause names. The final commit changes only those two clause arrays. Runtime, tests, callers, guides and expected bundle bytes are identical. At `bcd7dc8d6eb3098a700e011b541520d22e1886a3`, the complete external-build corpus, conformance and independence pass; see [final-contract-checks.log](final-contract-checks.log). No required instrument is waived.

## Single Entry Grammar

AC8: real command runs refuse positional entries, repeated entry or preset options, preset-only commands, complete Markdown-link expressions, the undeclared `--tags` flag and abbreviations. Bracket/parenthesis filenames remain valid destinations. An empty preset argument is valid and therefore admitted by the corpus schema. Installed-wheel smoke checks the new grammar outside the repository and compiles a selected named preset with its exact qualified filename.

Instruments: `src/tests/test_entry_presets.py`, CLI corpus fixtures and `checks/smoke.py`.

## Shared Reader And Activation

AC3 and AC9: instrumented source and CLI consumers call the shared reader during a real compilation. Whole-document and fragment runs compare direct CLI selection with authored tagged links. Unicode surrounding whitespace, case, repetition, ordering, empty/default names and unknown names produce the required matching set. Named presets govern destination-owned settings above default; existing grouping, substitution, precedence and conflict fixtures exercise that behavior.

The selected-dispatch run verifies both its qualified published link and its separately compiled content. The qualification uses canonical JSON of matched declared names and the full lowercase SHA-256 digest.

Instruments: the explicit-entry suite, selection/substitution tests and inclusion/composition corpus.

## Heading And Label Independence

AC10: absent, empty and unmatched selections leave heading words inert. Varying headings and labels with a fixed title tag preserves selected behavior. Incoming selections supply no tags to outgoing links. Mixed tagged and untagged occurrences preserve the established union of explicit source-owned group memberships; no implicit individual placement is added when that union contains a named pair.

Instruments: `test_headings_and_labels_select_no_presets`, `test_occurrences_union_explicit_group_pairs`, source/selection tests and migrated preset corpus.

## Executable Guide Commands

AC11: the bare guide and guide corpus state source-relative resolution, cwd-relative destinations, same-document fragment qualification, shell quoting and leading-dash values. The guide's own relative fragment command and quoted multiword-preset command are shell-tokenized and executed against matching real sources. The `--entry=-guide.md --presets=-checks` form executes successfully.

Instruments: `test_the_guide_specifies_resolution_and_shell_quoting`, `test_the_guides_relative_fragment_and_quoted_commands_compile`, `test_leading_dash_values_attach_to_their_options` and the guide corpus fixture.

## Public Guidance And Examples

AC21: help and the invocation option table agree. Root usage, focused source/selection/composition/bundle guides, glossary, corpus documentation and active deterministic callers describe the current contract. The runtime README pins the authoritative design and fixture clause mappings name that design's clauses.

`make examples` compiles all nine example cases: eight successful bundle cases and the expected refusal. Their generated SVGs show the current installed command and actual bundle bytes. The renderer measures link positions after code-span delimiters are removed, preserving whole-word link highlights. See [examples.log](examples.log) and [smoke-examples.log](smoke-examples.log).

## Runtime Safety And Fixed Point

The full-set publication guard rejects an input source inside the actual entry run folder even when only a dispatched closure reads it. Its regression preserves that input's bytes and observes invalid usage before publication.

A preset-only incoming selection keeps traversal active until its newly effective substitutions are expanded. Expansion depth counts reference chains, independently of fixed-point rounds. Normal and depth=1 runs now compile the newly selected stand-in and report `W_SUBST_USED`; the language-neutral corpus repeats the depth=1 case through the configured external build. Existing capture, monotonic selection union and final placement remain intact.

Instruments: `test_a_dispatch_only_input_inside_the_entry_run_folder_is_refused`, `test_a_later_occurrence_activates_substitution_at_the_reference_depth` and `inclusion/a-later-title-selection-activates-a-direct-substitution`.

Deferred and dispatch target answers follow the stable substitution mapping. Scheduling and self-composition warnings are derived from the source ranges the final composed groups publish, after candidate validation. A transient old dispatch produces no extra bundle; a dispatch or self-composition found only in an old body absent from final placement produces no handoff or warning. Physical captures and selecting occurrences keep their existing monotonic union.

The explicit-entry suite includes deferred-target confirmation, effective-dispatch-only, hidden-body dispatch and hidden-body warning regressions. The language-neutral corpus checks both transient-dispatch cases through the configured build. All three focused external-build regressions pass; see [targeted-regressions.log](targeted-regressions.log).

## Fixture Preservation Review

Legacy multiple-entry cases now express their inputs through authored links from one entry. Expected names follow that entry alone. Existing body content was compared against the epic-base expectations after excluding destination/heading changes and added input links: no prior body-content line was lost in the 55 adapted cases retained in [fixture-review.json](fixture-review.json). The separate source-heading-slug case retains all five source inputs under its single entry. The two heading-mismatch deferral cases now assert valid tagged or untagged handoff under different headings.

Committed paid-run, baseline and session records remain revision-bound evidence. This unit changes active callers and deterministic fixtures. No paid session ran.

## Full Check

Run from the unit checkout:

```text
PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i10/e07/w04-entries-select-presets-through/src --frozen pf' make check
make examples
```

Final result: **passed across the identical behavior tree and corrected fixture metadata** — 1,814 source tests, 1,416 deterministic harness tests and 530 corpus fixtures; all nine checked examples reproduce. Strict typing checks 89 source files. The gate includes lockfile, lint, formatting, strict typing, source tests, deterministic harness, corpus, installed-wheel smoke, layout, command/dependency tables, online links, vocabulary, invocation, design conformance and independence.

## Delivery Boundary

Covered criteria: AC3, AC8, AC9, AC10, AC11 and AC21. No unit criterion is waived. Full effective-variant dispatch scheduling, cycle/depth identities, parallel-set mapping and collisions remain W06/W07. Later deferred parity and eval expectations retain their planned scope. One selected dispatched target works end to end here.

Coordinator owns engineering publication, PR creation, task merge and tracker reconciliation. The unit source branch is clean; publication uses plain `git push`.

## Final Results

| Instrument | Revision | Result |
| --- | --- | --- |
| Lock, lint, format, typing | `734c06a6e` | Pass; strict typing covers 89 source files. |
| Source tests | `734c06a6e` | 1,814 passed, including 31 explicit-entry and review-regression cases. |
| Deterministic harness | `734c06a6e` | 1,416 passed. |
| Installed-wheel smoke | `734c06a6e` | Pass outside the repository: grammar, selected content and exact qualified name. |
| Layout, tables, online links, vocabulary, invocation | `734c06a6e` | Pass. |
| Checked examples | Same runtime bytes | Nine expected outcomes; current SVGs reproduce without a tracked diff. |
| External-build corpus | Final head | 530 passed; no failures, awaiting markers or unexpected passes. |
| Design conformance and independence | Final head | Pass; no fixture declaration names an absent clause. |
| Change attestation | `734c06a6e` to final head | Exactly two one-line `clauses` arrays differ; runtime, tests, guides and expected outputs are byte-identical. |
| Final source state | Final head | Clean; plain push confirms origin at the exact source head. |

The initial full-gate conformance failure remains in its original log. Focused final corpus, conformance and independence checks completely cover the correcting fixture-only commit; unchanged source and harness tests were not repeated. No open implementation finding or waived unit criterion remains. Coordinator publication, task PR, merge and tracker reconciliation are next.
