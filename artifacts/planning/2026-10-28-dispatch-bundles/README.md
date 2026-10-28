# I05 Dispatch Bundles — October 2026

> Epic planning · Created 2026-10-28

## Executive Summary

The dispatch (`⇉`) and parallel dispatch (`⫽`) operators are prosiform grammar: `pf` compiles what each states into the bundles it publishes, so an agent follows a bundle without an authored symbol table. Every dispatched target compiles to a bundle of its own beside the bundle that dispatches it. A `⇉` link points at a local sub-section instructing its dispatch; the `⫽` links in one section form a set, and point at one local sub-section instructing their dispatch together. Each bundle opens with a `# Prosiform` section stating the protocols it uses. `pf --guide` serves what remains of the corpus bootstrap, so a skill's bootstrap is one instruction to call it.

## Design

### Output

- **`-o DIR` names a folder.** The default is the working directory. Every bundle a run publishes is written there. No bundle is written to standard output.
- **Every bundle takes the derived name.** A selection's name is its working-directory path with `/` as `_`, plus `__<fragment>` for a section, then `.bundle.md`. A run of several entries joins each entry's name with `+`: `procedure+rules_common.bundle.md`.
- **Publication is all-or-nothing.** Every bundle is validated before any is written, and each is written atomically. A failure writes none. `-c` validates every bundle and writes none. Files in the folder the run does not produce are left as they are.

### Dispatched bundles

- **A dispatched target is a bundle.** A `⇉` or `⫽` link names a Markdown document or section under the root. One run follows dispatches transitively and compiles each distinct target (document and fragment) once, as its own entry, into the output folder. Every dispatch naming that target points at that one bundle.
- **The mark is stripped.** A dispatching link's published text carries no operator; the sub-section it points at states the dispatch.
- **A sub-section sits one level below the section holding the link,** after that section's own content and before its child sections. A dispatch in content above the bundle's first heading takes a sub-section at the bundle's first heading level. A dispatch in a level-6 section is refused: no heading level remains.
- **Budgets are per bundle.** Each bundle is read by one agent, so every budget holds for each bundle's own closure: `-E` counts hops from its entry, and `-F`, `-T`, `-L`, `-I` and `-O` count what it alone opens, reaches and publishes. The number of bundles is the number of distinct dispatched targets.
- **pf's headings are its own.** An authored heading whose text equals one pf emits in the same bundle — `Prosiform`, `Dispatch <link text>` or `Dispatch in parallel` — is refused, naming both.
- **A cycle is refused.** A chain of dispatches returning to a target already on it would start sub-agents without end, so the run publishes nothing and names the chain. A chain deeper than three dispatches still warns. The self-dispatch warning is kept. A dispatched target's shape is the corpus's convention, so pf states no rule on it.

### Dispatch

- **One sub-section per target per section.** Its heading is `Dispatch <link text>`, and its body is one line: dispatch `<bundle file>` to a sub-agent, as [Dispatch](#dispatch) states. Links in one section naming one target share it. Each section dispatching a target carries its own, and all point at the same bundle.

### Parallel dispatch

- **A section's `⫽` links are one set.** Any section may carry `⫽` links anywhere in its prose. The set is the `⫽` links in the section's own content; a child section's links form that section's set.
- **One sub-section per set.** Its heading is `Dispatch in parallel`, and its body lists each bundle file with its link text, to be dispatched together, as [Parallel dispatch](#parallel-dispatch) states. Every `⫽` link in the section points at it. A target named twice in one set is listed once.
- **Sets and dispatches are independent.** A section carrying `⇉` and `⫽` links has a sub-section for each `⇉` target and one for its `⫽` set.
- **A set has no order.** Every item starts together; work depending on an item's result is a later step outside the set.

### The Prosiform section

- **A bundle opens with `# Prosiform`.** It precedes the first authored section and holds `## Dispatch` and `## Parallel dispatch`, each only when the bundle uses that operator. A bundle using neither has no Prosiform section. An agent reading top-down meets the protocols before the steps that invoke them.
- **Dispatch protocol.** Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.
- **Parallel dispatch protocol.** Dispatch every listed bundle at once, each to a sub-agent of its own as [Dispatch](#dispatch) states; an item the invoking step applies "for each" of several values is dispatched once per value, together. Continue when every item has returned. A failed item cancels nothing: the set returns every failure together as blockers. Questions items return are put to the user together once every item has returned, and only the items that asked are dispatched again.
- **The text is pf's.** The protocol and instruction wording is fixed by the profile, so every bundle states it identically.

### Guide

- **`pf -g` / `--guide`** prints the guide to standard output and exits 0. It states the compile step (`pf -o <folder> <destination>` from the skill directory; a non-zero exit stops the run and reports diagnostics), the `↳` inline-target rule, and that a bundle opening with a Prosiform section is followed from there.
- **The corpus bootstrap is one instruction:** run `pf --guide` and follow it. `bootstrap.md` is retired.

### Evaluation

- **Correctness is proven end to end.** Corpus fixtures compile source trees to their expected bundle sets under `make check`. They cover each layout permutation: a dispatch in a section, a nested section and the preamble; one target dispatched from two sections; chains of depth one to three and past the limit; a refused cycle and a refused level-6 dispatch; a parallel set in one section, in sibling and nested sections, and beside a `⇉` link; one target named twice in a set; several joined entries.
- **Navigation is measured by agents.** A dispatch and parallel-dispatch scenario set extends the I05:E01 eval: its headless runner follows each scenario's bundle set from `pf --guide`, and its trace scorer checks that each bundle is dispatched to a sub-agent, a set's bundles are dispatched together, questions are relayed rather than asked, and the run completes. Each scenario also runs in the bootstrap-driven form the current corpus uses, so the report states whether compiled protocols improve on authored ones. The report is compared against a committed baseline.

## Delivery

Layered tasks, each leaving a working `pf`:

| Row | Task |
| --- | --- |
| W01 | `-o` names a folder; joined derived names for several entries |
| W02 | All-or-nothing publication of several bundles |
| W03 | Dispatched bundles, `Dispatch` sub-sections and the cycle error; `W_DISPATCH_NOT_PROCEDURAL` retired |
| W04 | Parallel dispatch sets and their sub-section; the run-set shape rule retired; Board Reads rewritten as sequential step sub-sections |
| W05 | The `# Prosiform` section and its protocols |
| W06 | `--guide`; bootstrap retirement; docs, glossary and invocation |
| W07 | Layout-permutation corpus fixtures for the bundle set |
| W08 | Dispatch and parallel-dispatch scenarios in the E01 eval, and their first baseline |

## Decisions

- **Whole chain in one run.** The agent reads bundles that exist rather than compiling at run time.
- **One bundle per target.** Matches the bundle's include-once rule and keeps a cycle finite at compile time.
- **Cycle refused, depth warned.** A cycle cannot finish; a deep chain finishes slowly.
- **Folder output.** Several bundles need a folder, and the derived scheme names them all.
- **Parallelism is a property of dispatches.** `⫽` marks a link, not a target's shape, so any section's prose can run work together; a target holds no list of calls, and inline calls run in sequence.
- **Steps are sub-sections, by corpus convention.** A step a heading roots is a precise link destination. Converting the work-planner corpus is its own epic; this epic writes Board Reads in that form.
- **Protocols first.** A step can be acted on before later text is read.
- **Profile v4.** The same source bundles differently, as with v3.
- **Navigation extends E01.** One runner, scorer and baseline serve every agent eval; W08 takes an edge on I05:E01.
- **Breaking, without compatibility.** `-o FILE`, standard-output publication, the run-set target shape and the bootstrap symbol rows for `⇉` and `⫽` are removed.

## Links

| Resource | Link |
| --- | --- |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
