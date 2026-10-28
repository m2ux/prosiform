# I05 Dispatch Bundles — October 2026

> Epic planning · Created 2026-10-28

## Executive Summary

The dispatch (`⇉`) and parallel dispatch (`⫽`) operators are prosiform grammar: `pf` compiles what each states into the bundles it publishes, so an agent follows a bundle without an authored symbol table. Every dispatched target compiles to a bundle of its own beside the bundle that dispatches it. A `⇉` link points at a local sub-section instructing its dispatch; the `⫽` links in one section form a set, and point at one local sub-section instructing their dispatch together. Each bundle opens with a `# Prosiform` section stating the protocols it uses. A bare `pf` serves what remains of the corpus bootstrap, so a skill's bootstrap is one instruction to run it.

The epic is I05:E03: sixteen task rows delivered as ten pull requests, each leaving a working `pf`, with one edge outside it: the eval row waits on I05:E01's baseline.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W01 work item](w01.md) | The output folder, joined derived names and the corpus runner reading the folder |
| [W02 work item](w02.md) | All-or-nothing publication of a bundle set |
| [W03 work item](w03.md) | Dispatched bundles, dispatch sub-sections and per-bundle budgets |
| [W04 work item](w04.md) | Dispatch refusals and the retired step warning |
| [W05 work item](../2026-10-28-351-i05-e03-w05-run-folder-bundles-suffix/w05.md) | The run folder named `<entry>.bundles`, replacing only a folder of that name |
| [W06 work item](w06.md) | Parallel dispatch sets and their sub-section |
| [W07 work item](w07.md) | Board Reads as numbered step sub-sections |
| [W08 work item](w08.md) | The Prosiform section, its protocols and profile v4 |
| [W09 work item](w09.md) | The guide a bare `pf` prints, bootstrap retirement and the documentation |
| [W10 work item](w10.md) | Layout-permutation fixtures for the bundle set |
| [W11 work item](../2026-10-28-351-i05-e03-w11-run-folder-swap-safe/w11.md) | The run folder's swap: a link at its path, a refused restore and a refused cleanup |
| [W12 work item](../2026-10-28-351-i05-e03-w11-run-folder-swap-safe/w12.md) | Name collisions, a missing output folder and a source read two ways, refused before any write |
| [W13 work item](../2026-10-28-351-i05-e03-w11-run-folder-swap-safe/w13.md) | Staging and aside names independent of the run folder's |
| [W14 work item](../2026-10-28-351-i05-e03-w11-run-folder-swap-safe/w14.md) | Dispatch link text, empty-text refusal, reserved headings and one dispatched-link reader |
| [W15 work item](../2026-10-28-351-i05-e03-w11-run-folder-swap-safe/w15.md) | Schema-valid test manifests and the renamed fixture families |
| [W16 work item](w16.md) | Dispatch scenarios in the diagram-following eval and their baseline |
| [Review findings](../2026-10-28-351-i05-e03-w11-run-folder-swap-safe/findings.md) | The seven findings of the review of the epic as merged to `main` |
| [Joins](joins.md) | Independent row pairs that take separate pull requests, and why |

## Design

### Output

- **`-o DIR` names the root.** The default is the working directory. A run writes its whole bundle set — the entry's bundle and every bundle it dispatches — into `DIR/<entry name>.bundles/`, the entry's derived name without `.bundle.md` and with the `.bundles` suffix, so an author folder named like the entry is never a run folder. No bundle is written to standard output.
- **Every bundle takes the derived name.** A selection's name is its working-directory path with `/` as `_`, plus `__<fragment>` for a section, then `.bundle.md`. A run of several entries joins each entry's name with `+`, which names both its folder and its entry bundle: `procedure+rules_common.bundles/procedure+rules_common.bundle.md`.
- **Publication is all-or-nothing.** Every bundle is validated before any is written. The set is written into a fresh hidden folder beside the run's folder and renamed onto it; an older run folder, only ever one carrying that `.bundles` name, is renamed aside first and removed after, so a reader sees the whole old set or the whole new set. A failure before the swap leaves `DIR` as it was. `-c` validates every bundle and writes none. Everything else under `DIR` is left as it is. (User, 2026-10-28, during W03.)

### Dispatched bundles

- **A dispatched target is a bundle.** A `⇉` or `⫽` link names a Markdown document or section under the root. One run follows dispatches transitively and compiles each distinct target (document and fragment) once, as its own entry, into the output folder. Every dispatch naming that target points at that one bundle.
- **The mark is stripped.** A dispatching link's published text carries no operator; the sub-section it points at states the dispatch.
- **A sub-section sits one level below the section holding the link,** after that section's own content and before its child sections. A dispatch in content above the bundle's first heading takes a sub-section at the bundle's first heading level. A dispatch in a level-6 section is refused: no heading level remains.
- **Budgets are per bundle.** Each bundle is read by one agent, so every budget holds for each bundle's own closure: `-E` counts hops from its entry, and `-F`, `-T`, `-L`, `-I` and `-O` count what it alone opens, reaches and publishes. The number of bundles is the number of distinct dispatched targets.
- **pf's headings are its own.** An authored heading whose text equals one pf emits in the same bundle — `Prosiform`, `Dispatch`, `Parallel dispatch`, `Dispatch <link text>` or `Dispatch in parallel` — is refused, naming both. `Dispatch` and `Parallel dispatch` are refused where the bundle carries that protocol.
- **A cycle is refused.** A chain of dispatches returning to a target already on it would start sub-agents without end, so the run publishes nothing and names the chain. A chain deeper than three dispatches still warns. The self-dispatch warning is kept. A dispatched target's shape is the corpus's convention, so pf states no rule on it.

### Dispatch

- **One sub-section per target per section.** Its heading is `Dispatch <link text>`, and its body is one line: dispatch `<bundle file>` to a sub-agent, as [Dispatch](#dispatch) states. Links in one section naming one target share it. Each section dispatching a target carries its own, and all point at the same bundle.

### Parallel dispatch

- **A section's `⫽` links are one set.** Any section may carry `⫽` links anywhere in its prose. The set is the `⫽` links in the section's own content; a child section's links form that section's set.
- **One sub-section per set.** Its heading is `Dispatch in parallel`, and its body lists each bundle file with its link text, to be dispatched together, as [Parallel dispatch](#parallel-dispatch) states. Every `⫽` link in the section points at it. A target named twice in one set is listed once.
- **Sets and dispatches are independent.** A section carrying `⇉` and `⫽` links has a sub-section for each `⇉` target and one for its `⫽` set.
- **A set has no order.** Every item starts together; work depending on an item's result is a later step outside the set.

### The Prosiform section

- **A bundle opens with `# Prosiform`.** It is the bundle's first heading, ahead of a file heading and after any content above the entry's title, and holds `## Dispatch` whenever the bundle uses `⇉` or `⫽`, and `## Parallel dispatch` only when it uses `⫽`: a parallel dispatch is dispatch done together, and its protocol defers to Dispatch. A bundle using neither has no Prosiform section. Its levels are fixed, so each protocol is the same bytes in every bundle. An agent reading top-down meets the protocols before the steps that invoke them.
- **Dispatch protocol.** Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.
- **Parallel dispatch protocol.** Dispatch every listed bundle at once, each to a sub-agent of its own as [Dispatch](#dispatch) states; an item the invoking step applies "for each" of several values is dispatched once per value, together. Continue when every item has returned. A failed item cancels nothing: the set returns every failure together as blockers. Questions items return are put to the user together once every item has returned, and only the items that asked are dispatched again.
- **The text is pf's.** The protocol and instruction wording is fixed by the profile, so every bundle states it identically.

### Guide

- **`pf` with no arguments** prints the guide to standard output and exits 0; `pf -h` says so. It states the compile step (`pf -o <folder> <destination>` from the skill directory; a non-zero exit stops the run and reports diagnostics), the `↳` inline-target rule, and that a bundle opening with a Prosiform section is followed from there.
- **The corpus bootstrap is one instruction:** run `pf` and follow it. `bootstrap.md` is retired.

### Evaluation

- **Correctness is proven end to end.** Corpus fixtures compile source trees to their expected bundle sets under `make check`. They cover each layout permutation: a dispatch in a section, a nested section and the preamble; one target dispatched from two sections; chains of depth one to three and past the limit; a refused cycle and a refused level-6 dispatch; a parallel set in one section, in sibling and nested sections, and beside a `⇉` link; one target named twice in a set; several joined entries.
- **Navigation is measured by agents.** A dispatch and parallel-dispatch scenario set extends the I05:E01 eval: its headless runner follows each scenario's bundle set from the guide a bare `pf` prints, and its trace scorer checks that each bundle is dispatched to a sub-agent, a set's bundles are dispatched together, questions are relayed rather than asked, and the run completes. Each scenario also runs in the bootstrap-driven form the current corpus uses, so the report states whether compiled protocols improve on authored ones. The report is compared against a committed baseline.

## Delivery

Layered tasks, each leaving a working `pf`. Rows sharing a pull request are joined.

| Row | Task | Pull request |
| --- | --- | --- |
| W01 | `-o` names a folder; joined derived names for several entries | 1 |
| W02 | All-or-nothing publication of several bundles | 2 |
| W03 | Dispatched bundles, `Dispatch` sub-sections and per-bundle budgets | 3 |
| W04 | The cycle, level-6 and heading-collision refusals; `W_DISPATCH_NOT_PROCEDURAL` retired | 3 |
| W05 | The run folder named `<entry>.bundles`; only a folder of that name replaced | 4 |
| W06 | Parallel dispatch sets and their sub-section; the run-set shape rule retired | 5 |
| W07 | Board Reads rewritten as sequential numbered step sub-sections | 5 |
| W08 | The `# Prosiform` section and its protocols; profile v4 | 6 |
| W09 | The guide from a bare `pf`; bootstrap retirement; docs, glossary and invocation | 7 |
| W10 | Layout-permutation corpus fixtures for the bundle set | 8 |
| W11 | The run folder's swap: a link at its path replaced, a refused restore and cleanup reported | 9 |
| W12 | Name collisions, a missing output folder and a source read two ways refused before any write, `-c` included | 9 |
| W13 | Staging and aside names of fixed length | 9 |
| W14 | Dispatch link text collapsed, empty text refused, only emitted headings reserved | 9 |
| W15 | Schema-valid test manifests; `parallel-dispatch` and `publication` families | 9 |
| W16 | Dispatch and parallel-dispatch scenarios in the E01 eval, and their first baseline | 10 |

## Decisions

- **A bare `pf` is the guide.** One path prints it, so no option duplicates it; the bootstrap reads "run `pf` and follow it".
- **Whole chain in one run.** The agent reads bundles that exist rather than compiling at run time.
- **One bundle per target.** Matches the bundle's include-once rule and keeps a cycle finite at compile time.
- **Cycle refused, depth warned.** A cycle cannot finish; a deep chain finishes slowly.
- **Folder output.** Several bundles need a folder, and the derived scheme names them all. A run's set lands in a sub-folder named for its entry and swapped in whole, so a reader never meets a mixture of two runs' bundles. (User, 2026-10-28, during W03.)
- **Parallelism is a property of dispatches.** `⫽` marks a link, not a target's shape, so any section's prose can run work together; a target holds no list of calls, and inline calls run in sequence.
- **Steps are sub-sections, by corpus convention.** A step a heading roots is a precise link destination. Converting the work-planner corpus is its own epic; this epic writes Board Reads in that form.
- **Protocols first.** A step can be acted on before later text is read.
- **Profile v4.** The same source bundles differently, as with v3.
- **Navigation extends E01.** One runner, scorer and baseline serve every agent eval; W16 takes an edge on I05:E01 W05.
- **Breaking, without compatibility.** `-o FILE`, standard-output publication, the run-set target shape and the bootstrap symbol rows for `⇉` and `⫽` are removed.
- **Profile v4 lands with the Prosiform section.** W08 changes what every dispatching bundle opens with and fixes the protocol wording as a profile constant, so the profile bump is its criterion. (Planning, 2026-10-28.)
- **Each pf task carries its own contract edits.** `make conformance` reads the design from `engineering` at the README's pin and holds the build's codes to it, and `make invocation` holds the help text to `invocation.md`, so W01–W06 and W08 each edit their design clauses, the pin and their `invocation.md` rows; W09 sweeps the remaining prose. (Planning, 2026-10-28.)
- **The stdout consumers move with W01.** The corpus runner, the manifest schema, the 308 `expected/stdout.md` files, `checks/render.py`, `checks/smoke.py` and the delivery wrapper all read a bundle from standard output; W01 moves or removes each, so `make check` holds on its revision. (Planning, 2026-10-28.)
- **Ten rows, eight pull requests.** The dispatched-bundles and parallel-sets tasks each exceeded three criteria, so each is split into two joined rows sharing one pull request: W03 with W04, W06 with W07. (User, 2026-10-28.)
- **Priority 8, beside E01.** The collision rule would rank this epic 7, behind I05:E01, because W16 (then W11) and E01 W01 both write `evals/diagram-following/workflows`. The user overrode it ("I want this work now"): W16's edge on E01 W05 already holds the only shared folder until E01's eval is written, so nothing else waits. (User, 2026-10-28.)
- **The run folder carries a suffix.** A run writes into `<entry name>.bundles/` and replaces only a folder of that name, so an author folder named like the entry is never its run folder; raised as #358 from W03 and placed as W05, after W04 and ahead of the parallel sets. The rows after it moved up one number. (User, 2026-10-28.)
- **Step headings carry their number.** A step sub-section is headed by its position and action, as `### 6. Publish`; Board Reads (W07) is written that way first, and Corpus Steps' first row states the convention. Inserting a step renumbers the anchors below it, and `pf`'s unresolved-link check reports a link left naming an old one. (User, 2026-10-28.)
- **Dispatch accompanies Parallel dispatch.** `## Dispatch` is present whenever a bundle uses either operator, because the Parallel dispatch protocol dispatches each item as Dispatch states; `## Parallel dispatch` only with `⫽`. An authored `Dispatch` or `Parallel dispatch` heading is refused wherever pf emits it. AC16 states the rule. (Orchestrating session, 2026-10-28, during W08.)
- **Review findings are one pull request into the epic base.** The seven findings of the review of `main` at 8e56baf3 (#355) are all fixed in one task pull request into `i05/e03/main`, as joined rows W11–W15, each criterion with its test or fixture; a new draft review pull request then carries `i05/e03/main` into `main` for the user to merge. (User, 2026-10-28.)
- **The fix rows precede the eval.** They wait on nothing outside the epic, and the eval waits on I05:E01 W05, so the fix rows take W11–W15 and the eval row moves from W11 to W16. No pull request named it. (Planning, 2026-10-28.)
- **No discussion pull request.** The records pushed to `engineering` are the discussion, as for I05's earlier epics. (User, 2026-10-28.)

## Component Map

Each row's declared component, and every other path its pull request writes. The declared component is the one the implementation extends; the further paths are what the collision check reads.

| Row | Component | Further paths written |
| --- | --- | --- |
| W01 | `src/prosiform/cli.py` | `src/prosiform/delivery.py` (removed), `src/tests`, `checks/runner.py`, `checks/render.py`, `checks/smoke.py`, `checks/tests`, `fixtures/manifest.schema.json`, every `fixtures/**/expected/`, `fixtures/README.md`, `invocation.md`, `README.md` (pin), `example/README.md`; `design.md` on `engineering` |
| W02 | `src/prosiform/cli.py` | `src/tests`, `fixtures/cli`, `README.md` (pin); `design.md` |
| W03 | `src/prosiform/dispatch.py` | `cli.py`, `bundle.py`, `rewrite.py`, `closure.py`, `src/tests`, `fixtures/dispatch`, `fixtures/usage-example/*/expected/`, `invocation.md`, `README.md` (pin); `design.md` |
| W04 | `src/prosiform/dispatch.py` | `cli.py`, `src/tests`, `fixtures/dispatch`, `invocation.md`, `README.md` (pin); `design.md` |
| W05 | `src/prosiform/cli.py` | `src/tests`, `checks/runner.py`, `checks/smoke.py`, `checks/tests`, `scripts/render-diagram.py`, `fixtures/cli`, `fixtures/rewriting`, `fixtures/README.md`, `invocation.md`, `docs/glossary.md`, `README.md` (pin), `example/README.md`; `design.md` |
| W06 | `src/prosiform/run_set.py` | `cli.py`, `bundle.py`, `src/tests`, `fixtures/run-set`, `example/work-planner/guidelines.md`, `example/work-planner/rules.md`, `invocation.md`, `README.md` (pin); `design.md` |
| W07 | `example/work-planner/artifacts/delivery-evidence.md` | `fixtures/usage-example/*/expected/` |
| W08 | `src/prosiform/bundle.py` | `__init__.py`, `profile.py`, `src/tests`, `fixtures/`, `fixtures/cli` (version), `fixtures/usage-example/*/expected/`, `README.md` (pin); `design.md` |
| W09 | `src/prosiform/cli.py` | `src/tests`, `fixtures/cli`, `fixtures/usage-example/*/expected/`, `example/work-planner/bootstrap.md` (removed), `example/work-planner/SKILL.md`, `example/work-planner/rules.md`, `example/work-planner/guidelines.md`, `invocation.md`, `docs/glossary.md`, `README.md`; `design.md` |
| W10 | `fixtures/dispatch` | `fixtures/run-set` |
| W11 | `src/prosiform/cli.py` | `src/tests`, `invocation.md`, `README.md` (pin); `design.md` |
| W12 | `src/prosiform/cli.py` | `src/tests`, `README.md` (pin); `design.md` |
| W13 | `src/prosiform/cli.py` | `src/tests` |
| W14 | `src/prosiform/dispatch.py` | `cli.py`, `src/tests`, `fixtures/dispatch`, `README.md` (pin); `design.md` |
| W15 | `fixtures` | `fixtures/run-set` → `fixtures/parallel-dispatch`, `fixtures/delivery` → `fixtures/publication`, `checks/tests` |
| W16 | `evals/diagram-following/workflows` | `evals/diagram-following/score.py`, `run.py`, `stub_agent.py`, `report.py`, `baseline.json`, `README.md` |

## Collision Surface

Checked against the in-flight I05 epics, the open pull requests and the open epics of other initiatives on 2026-10-28.

- **I05:E02 Link Forms (#339).**
  Every row is merged and its base reached `main` through #342 and the v0.15.0 release; the epic awaits closure. No collision.
- **I05:E01 Diagram Following (#333).**
  `i05/e01/main` is unmerged and holds `evals/diagram-following/`, `Makefile`, `checks.md`, `checks/layout.py` and `src/README.md`; its W05 (the baseline run) waits on the user's eval login. W16 writes the same eval and takes an edge on E01 W05; no other row touches E01's paths. `deps.py` reports E01:W01 and E03:W16 (then W11) both extending `evals/diagram-following/workflows`, which the user accepted at the same priority.
- **I05:E04 Corpus Steps.**
  W06, W07 and W09 write `example/work-planner/` (`delivery-evidence.md`, `guidelines.md`, `rules.md`, `SKILL.md`) and the usage-example bundles, which every E04 row also writes. E04's first row depends on W09 and the epic sits one number below.
- **I01:E00 Findings Ledger (#21, draft pull request #325).**
  Changes `Makefile`, `checks.md` and `checks/README.md`; no row here writes those, though W01 changes `checks/`.
- **I01:E03 Repository Checks (#187).**
  Its open W08 (#189, Corpus Runner: One Fixture Run by Its Identity) would change `checks/runner.py`, which W01 rewrites. I01:E03 carries priority 2 and has no pull request open.
- **I03 Production Compiler (#10).**
  Binds the same language-neutral corpus; W01 changes how every fixture declares its output. I03 targets the tagged revision I01:E13 freezes, so it is unaffected until it re-targets.

## Epic Priority

`deps.py` over I05's body with E03 and E04 added, the work items and the joins records proposes E03 one below E01 and E02 from the E01:W01 / E03:W16 contention. Confirmed: E03 `priority: 8` beside E01 and E02, at the user's request; E04 `priority: 7`.

Longest chains: 24, each of 9 steps, every one running E03 W01, W02, W08 and W09 then E04 W01.

## Review

Review Initiative Goal and Check Dependencies and Numbering over the drafts, 2026-10-28.

- **Goal trace.**
  I05's goal clauses (tests, rules, passing checks) map to its AC1–AC3. E03 delivers AC1 through its end-to-end fixture criteria (AC1–AC3, AC7, AC8, AC10–AC14, AC16, AC19, AC22), AC2 through AC18 (`pf -v`) and AC21 (`invocation.md`), and AC3 through every row's `make check` and `make corpus`. I05 marks no source, so no source alignment applies.
- **Folded without a decision.**
  Profile v4 assigned to W08; each pf row's design, pin and `invocation.md` edits; the stdout consumers moved in W01; the delivery wrapper removed in W01 under the no-compatibility decision; AC10 restated as one refusal condition over three causes; AC22 kept as one condition over its list of layouts, which `format.py` flags as possibly several.
- **Settled by the user.**
  The row split, the priority, the step heading form and the discussion pull request, as Decisions records.
- **Second pass.**
  After the split, `deps.py` reports no problem and no unaccounted pair, and `format.py` reports only the AC22 flag above.

### Review of the merged epic

Review of `main` at 8e56baf3, the #355 merge, 2026-10-28. Seven findings, each verified; the [findings record](../2026-10-28-351-i05-e03-w11-run-folder-swap-safe/findings.md) holds their evidence.

- **Publication.**
  1 (high) the run folder resolved through a link at its path, so the swap removes or writes outside `-o`; 4 (medium) a derived-name collision found only by the write, so `-c` passes it; 5 (medium-low) captures merged last-wins, so a source changed between two bundles' reads publishes; 6 (low) an unguarded restore, a cleanup failure reported as a failed publication, and staging names overflowing long run names; 7b `-c` passing a missing output folder.
- **Dispatch.**
  2 (high) link text entering a heading unnormalised, so wrapped, trailing-space or empty text ends in an internal error; 3 (medium) `Prosiform` and `Dispatch in parallel` reserved in every bundle; 7a a deferral message for dispatched links; 7c repeated deduplication; 7d dispatched links read by two readers.
- **Tests and fixtures.**
  7e test manifests carrying the retired `stdout` field; 7f two fixture families named for retired concepts.
- **Resolution.**
  Rows W11–W15 with AC27–AC38, joined in one pull request; AC12–AC14 name `fixtures/parallel-dispatch`. The user's decision is under Decisions.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E03 Dispatch Bundles](https://github.com/m2ux/prosiform/issues/351) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Prerequisite epic | [I05:E01 Diagram Following](https://github.com/m2ux/prosiform/issues/333) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
