# I05 Dispatch Bundles — October 2026

> Epic planning · Created 2026-10-28

## Executive Summary

The dispatch (`⇉`) and run-set (`⫽`) operators are prosiform grammar: `pf` compiles what each states into the bundles it publishes, so an agent follows a bundle without an authored symbol table. A dispatched target compiles to a bundle of its own beside the bundle that dispatches it, and the link points at a local sub-section instructing its dispatch. A run-set target carries an injected instruction to run its calls concurrently. Each bundle opens with a `# Prosiform` section stating the protocols it uses. `pf --guide` serves what remains of the corpus bootstrap, so a skill's bootstrap is one instruction to call it.

## Design

### Output

- **`-o DIR` names a folder.** The default is the working directory. Every bundle a run publishes is written there. No bundle is written to standard output.
- **Every bundle takes the derived name.** A selection's name is its working-directory path with `/` as `_`, plus `__<fragment>` for a section, then `.bundle.md`. A run of several entries joins each entry's name with `+`: `procedure+rules_common.bundle.md`.
- **Publication is all-or-nothing.** Every bundle is validated before any is written, and each is written atomically. A failure writes none. `-c` validates every bundle and writes none. Files in the folder the run does not produce are left as they are.

### Dispatch

- **A dispatched target is a bundle.** One run follows dispatches transitively and compiles each distinct target (document and fragment) once, as its own entry, into the output folder. Every dispatch naming that target points at that one bundle.
- **The link points at a local sub-section.** The mark is stripped from the published link text. The link's destination is a sub-section one level below the section holding the link, placed after that section's own content and before its child sections. Its heading is `Dispatch <link text>`, and its body is one line: dispatch `<bundle file>` to a sub-agent, as [Dispatch](#dispatch) states.
- **One sub-section per target per section.** Links in one section naming one target share a sub-section. Each section dispatching a target carries its own sub-section, and all point at the same bundle.
- **Placement limits.** A dispatch in content above the bundle's first heading takes a sub-section at the bundle's first heading level. A dispatch in a level-6 section is refused: no heading level remains for the sub-section.
- **A cycle is refused.** A chain of dispatches returning to a target already on it would start sub-agents without end, so the run publishes nothing and names the chain. A chain deeper than three dispatches still warns. The self-dispatch and not-procedural warnings are kept.

### Run-set

- **The target carries the instruction.** The mark is stripped from the published link text, and the link points at the compiled target section, as any dependency's does. The target gains one line after its heading and any lead-in prose, before its list: run these calls concurrently, as [Run-set](#run-set) states. A target several run-set links name carries the line once.
- **Lead-in prose is a run-set's.** A run-set is a section, or a whole document, holding optional paragraphs followed by one bulleted list of calls and nothing after it. `W_RUN_SET_SHAPE` reads that shape.
- **A dispatched item is a dispatch.** An item whose link dispatches points at its own `Dispatch` sub-section under the run-set target.

### The Prosiform section

- **A bundle opens with `# Prosiform`.** It precedes the first authored section and holds `## Dispatch` and `## Run-set`, each only when the bundle uses that operator. A bundle using neither has no Prosiform section. An agent reading top-down meets the protocols before the steps that invoke them.
- **Dispatch protocol.** Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.
- **Run-set protocol.** Run the listed calls concurrently as parallel tool calls: top-level items together, a nested item once its parent alone has returned, an item saying "for each" once per item, together. A dispatched item goes to a sub-agent of its own, all at once. Continue when every item has returned. A failed item cancels nothing: the run-set returns every failure together as blockers. Questions dispatched items return are put to the user together once every item has returned, and only the items that asked are dispatched again.
- **The text is pf's.** The protocol and instruction wording is fixed by the profile, so every bundle states it identically.

### Guide

- **`pf -g` / `--guide`** prints the guide to standard output and exits 0. It states the compile step (`pf -o <folder> <destination>` from the skill directory; a non-zero exit stops the run and reports diagnostics), the `↳` inline-target rule, and that a bundle opening with a Prosiform section is followed from there.
- **The corpus bootstrap is one instruction:** run `pf --guide` and follow it. `bootstrap.md` is retired.

## Delivery

Layered tasks, each leaving a working `pf`:

| Row | Task |
| --- | --- |
| W01 | `-o` names a folder; joined derived names for several entries |
| W02 | All-or-nothing publication of several bundles |
| W03 | Dispatch bundles, dispatch sub-sections and the cycle error |
| W04 | Run-set instruction injection and the lead-in shape rule |
| W05 | The `# Prosiform` section and its protocols |
| W06 | `--guide`; bootstrap retirement; docs, glossary, invocation and fixtures |

## Decisions

- **Whole chain in one run.** The agent reads bundles that exist rather than compiling at run time.
- **One bundle per target.** Matches the bundle's include-once rule and keeps a cycle finite at compile time.
- **Cycle refused, depth warned.** A cycle cannot finish; a deep chain finishes slowly.
- **Folder output.** Several bundles need a folder, and the derived scheme names them all.
- **Instruction at the link for dispatch, at the target for a run-set.** A dispatched target is outside the bundle, so the link needs a local destination; a run-set target is inside it, so its own section carries the instruction.
- **Protocols first.** A step can be acted on before later text is read.
- **Profile v4.** The same source bundles differently, as with v3.
- **Breaking, without compatibility.** `-o FILE`, standard-output publication and the bootstrap symbol rows for `⇉` and `⫽` are removed.

## Links

| Resource | Link |
| --- | --- |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
