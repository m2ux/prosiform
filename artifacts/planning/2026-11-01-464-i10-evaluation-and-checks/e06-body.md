## Overview

An agent following a bundle meets `↳` and `⇉` links, parallel sets and returned questions, and the guide bare `pf` prints explains only the first. This epic makes bare `pf` print a plain-text guide holding every rule an agent follows a bundle by, and makes every bundle open by telling its reader to run that guide first. Dispatched targets stay compiled up front, each into a file of its own; a bundle carries no protocol: a `⇉` link stays inline, pointing at the file compiled for its target, and a parallel set is one `In parallel` section of `⇉` items. The deferred dispatch marks, `¬⇉` and `¬⫽`, retire, and `↳` replaces the arrow directive as the composition mark, so the source grammar is `⇉`, `⫽`, `↳` and `¬`, and the agent learns only `↳` and `⇉`.

## Problem

- **The guide explains one mark.**
  Bare `pf` prints the compile step, the `↳` inline target and a pointer to a bundle's Prosiform section. It does not explain `⇉`, waiting on a set or a returned question.
- **The guide is Markdown.**
  It prints headings, code spans and a fenced block to a terminal.
- **Each dispatching bundle restates the protocols.**
  The Dispatch and Parallel dispatch paragraphs are copied into every bundle that dispatches, and only a dispatched bundle needing a first run tells its reader to run `pf`.
- **A dispatch link points away from its file.**
  A `⇉` link publishes without its mark, pointing at a generated sub-section whose line names the target's file in a code span, links the protocol and calls the file a bundle.
- **Deferred dispatch is a second way to dispatch.**
  `¬⇉` and `¬⫽` publish as plain links an agent cannot tell from citations, and a section holding `[⫽ a](a.md)` and `[¬⫽ b](b.md)` publishes `a` as a set of one and `b` as a plain link.
- **Composition is spelled by an arrow.**
  A directive is a link labelled with one Unicode arrow from a list of blocks, while its deferred form reaches a bundle as a `↳` line, so an author and an agent learn two marks for one placement, and the published link carries only the arrow.
- **No marker names a returned question.**
  The eval reads a return as a question from its first word, inside a hand-back frame that wraps every return ([#637](https://github.com/m2ux/prosiform/issues/637)).

## Proposal

- **Everything is compiled up front.**
  Each distinct target a `⇉` or `⫽` link names is compiled once, transitively, into its own file in the run folder beside the main bundle, as now. The up-front refusals, `W_DISPATCH_SELF`, `W_DISPATCH_DEPTH` and `E_DISPATCH_CYCLE` stay.
- **The agent knows two marks.**
  A bundle carries `↳` and `⇉`, and no `⫽` or `¬`.
- **A single dispatch stays inline.**
  `[⇉ x](path)` keeps its mark in the bundle and points at the file `pf` compiled for its target, as `[⇉ the crew](loading__crew.bundle.md)`; the guide says to give the linked file to a sub-agent and continue with its answer. No dispatch section is generated, and a condition stays in the prose around the link.
- **A parallel set is one section.**
  The set's `⫽` links point at one `In parallel` section, the set's boundary, listing each member as a `⇉` item linking its compiled file, as `- [⇉ the lift](lift__do.bundle.md)`, under a plain instruction: give each to its own sub-agent at the same time, and continue when all have answered. A set of one is published as a single inline `⇉` link.
- **Every bundle opens with the run-pf line; the guide holds the rules.**
  The Prosiform section and its protocol paragraphs retire. Bare `pf` prints, as plain command-line text, how to run `pf`, what `↳` and `⇉` mean, how an `In parallel` section is followed, the inputs a dispatch carries, waiting for all, failures returned together, and a returned question opening with a first line reading `Question:`.
- **Deferral keeps its two plain forms.**
  `¬→` publishes as its `↳` line, its preset rule unchanged, and `[¬ x](x.md)` is a withheld link kept as a plain link at its rebased path, its target not bundled. `¬⇉` and `¬⫽` are refused with `E_UNSUPPORTED_CONSTRUCT`, naming the link; no preset behaviour is lost, since a dispatched target already selects its presets by its own heading.
- **`↳` is the composition mark.**
  `[↳ Title](p.md#s)` composes the section as an arrow directive does today, under every placement rule, its published link carrying the title text. `[¬↳ Title](p.md#s)` builds the same destination section and publishes the `[↳ Title](p.md#s)` line for the agent to inline later; the deferred-preset refusal stays. `[→](…)`, `[¬→](…)` and every other arrow label are refused with `E_UNSUPPORTED_CONSTRUCT`, pointing at `[↳ …]`, and `[⇉↳ …]` and `[⫽↳ …]` contradict. A skill's `SKILL.md` bootstrap link is unaffected, since `pf` never compiles `SKILL.md`.
- **The eval measures the new bundles.**
  The baseline's and edge run's shakedowns follow this epic's rows, and the edge workflows' scenarios and corpus test are reworked on a row of their own epic. `staged` folds into `compiled`: a `compiled` session receives the finished bundles, the build under test as `pf` and a shell limited to `pf`, so it can run bare `pf` for the guide and compile `↳` lines; `authored` is unchanged.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/pull/641) | Design clause | AC1 | | | ✓ |
| [W01](https://github.com/m2ux/prosiform/pull/642) | A plain-text guide holding the rules | AC2, AC3, AC4 | W00 | | ✓ |
| [W02](https://github.com/m2ux/prosiform/pull/643) | Every bundle opening with the run-pf line | AC5 | W00 | W03, W04 | ✓ |
| [W03](https://github.com/m2ux/prosiform/pull/643) | A `⇉` link kept inline at its file | AC6, AC7 | W00 | W02, W04 | ✓ |
| [W04](https://github.com/m2ux/prosiform/pull/643) | One `In parallel` section per set | AC8, AC9 | W00 | W02, W03 | ✓ |
| [W05](https://github.com/m2ux/prosiform/pull/644) | Deferred dispatch marks refused | AC10 | W02, W03, W04 | W08 | ✓ |
| [W06](https://github.com/m2ux/prosiform/pull/645) | The pages stating the guide and `⇉` | AC11 | W01, W05 | | ✓ |
| [W07](https://github.com/m2ux/prosiform/pull/646) | One compiled form carrying `pf` | AC12, AC13, AC18 | W05 | | ✓ |
| [W08](https://github.com/m2ux/prosiform/pull/644) | `↳` composing, arrow labels refused | AC14, AC15, AC16 | W02, W03, W04 | W05 | ✓ |
| [W09](https://github.com/m2ux/prosiform/pull/647) | The composition page stating `↳` | AC17 | W05, W08 | | ✓ |
| [W10](https://github.com/m2ux/prosiform/pull/649) | Dispatch refusals stating no link to publish | AC19 | W03, W05, W08 | | ✓ |

## Acceptance Criteria

- [x] **AC1.** The design states the guide's text, the returned-question marker, the run-pf line every bundle opens with, the inline `⇉` link to its compiled file and the `In parallel` section, a set of one, the withheld link's wording, the refusal of `¬⇉` and `¬⫽`, and `↳` as the composition mark with arrow labels refused before any build row implements them, as the design at the README's pinned commit and its revision history show.
- [x] **AC2.** Bare `pf` prints how to run `pf`, what a `↳` link and a `⇉` link mean, how an `In parallel` section is followed, the inputs a dispatch carries, that a set is waited on until every member answers, that failures return together, and how a returned question is handled, as the guide fixture `make check` runs shows.
- [x] **AC3.** The guide bare `pf` prints carries no Markdown heading, emphasis, link or code fence, as a CLI test `make check` runs shows.
- [x] **AC4.** The guide states that a dispatched run opens a returned question with a first line reading `Question:`, as the guide fixture `make check` runs shows.
- [x] **AC5.** Every bundle a run writes opens with the run-pf line the design fixes, whatever the bundle holds, as the conformance fixtures `make check` runs show.
- [x] **AC6.** No bundle carries a Prosiform section, a protocol paragraph, a generated dispatch sub-section, or a `⫽` or `¬` mark, as the dispatch fixtures `make check` runs show.
- [x] **AC7.** A `⇉` link publishes in place with its mark, pointing at the file its target was compiled to, as the dispatch fixtures `make check` runs show.
- [x] **AC8.** A section's `⫽` links publish pointing at one `In parallel` section listing each member as a `⇉` link to its compiled file under the instruction the design fixes, as the dispatch fixtures `make check` runs show.
- [x] **AC9.** A `⫽` set of one member publishes as a single inline `⇉` link, as a dispatch fixture `make check` runs shows.
- [x] **AC10.** A link opening with `¬⇉` or `¬⫽` fails with `E_UNSUPPORTED_CONSTRUCT`, naming the link, and publishes nothing, as refused conformance fixtures `make check` runs show.
- [x] **AC11.** The README and `docs/` state the guide's contents, the run-pf line, `⇉` and the `In parallel` section in one page, and describe no Prosiform section or deferred dispatch, as a read of the pages against the guide and the fixtures shows.
- [x] **AC12.** A `compiled` session receives the finished bundles, the build under test as `pf` on its path and a shell limited to `pf`, `Bash(pf:*)` on Claude, on every harness the default matrix runs, as a harness test `make harness` runs shows.
- [x] **AC13.** The eval's README states one `compiled` form, that each bundle it gives opens with the run-pf line, and no `staged` form or Prosiform section, as a read of the README against the forms shows.
- [x] **AC14.** A `[↳ Title](p.md#s)` link composes its section beneath its scope under every placement rule the arrow directive had, and the link published to the destination carries its title text, as the composition fixtures `make check` runs show.
- [x] **AC15.** A `[¬↳ Title](p.md#s)` link builds the same destination section and publishes the `[↳ Title](p.md#s)` line, and a deferral whose scope selects other presets than its target's heading is still refused, as the deferred-composition fixtures `make check` runs show.
- [x] **AC16.** A link labelled with an arrow, `[→](…)` and `[¬→](…)` among them, fails with `E_UNSUPPORTED_CONSTRUCT` naming the link and pointing at `[↳ …]`, and `[⇉↳ …]` and `[⫽↳ …]` fail as contradicting, each publishing nothing, as refused conformance fixtures `make check` runs show.
- [x] **AC17.** `docs/composition.md` states `↳` as the composition mark and `¬↳` as its deferral, and no page of the README or `docs/` describes an arrow directive, as a read of the pages against the composition fixtures shows.
- [x] **AC18.** No form is named `staged`: a run given `--forms staged` is refused as naming an unknown form, as a harness test `make harness` runs shows.
- [x] **AC19.** A dispatch in a heading the bundle emits as text alone fails with `E_UNSUPPORTED_CONSTRUCT`, its diagnostic stating the heading is emitted as text alone, and no diagnostic, docstring or fixture manifest names a dispatch sub-section, as the dispatch fixtures `make check` runs and a read of `src/` and `fixtures/` show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the work items, the decisions and the dependency check.
- **R2.** [Design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md) — *Guide*, *Link classification and resource handling*, *Section composition* and *Agent delivery contract*.
- **R3.** [Dispatch scenarios on a headless session](https://github.com/m2ux/prosiform/issues/637) — the returned question the marker settles.

