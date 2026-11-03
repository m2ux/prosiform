## Overview

An agent following a bundle meets `↳` links, dispatch sections and returned questions, and the guide bare `pf` prints explains only the first. This epic makes bare `pf` print a plain-text guide holding every rule an agent follows a bundle by, and makes every bundle open by telling its reader to run that guide first. Dispatched targets stay compiled up front, each into a file of its own; a bundle carries no protocol and no dispatch mark, only plain sections that link each dispatched file. The deferred dispatch marks, `¬⇉` and `¬⫽`, retire, and `↳` replaces the arrow directive as the composition mark, so the source grammar is `⇉`, `⫽`, `↳` and `¬`, and the agent learns only `↳`.

## Problem

- **The guide explains one mark.**
  Bare `pf` prints the compile step, the `↳` inline target and a pointer to a bundle's Prosiform section. It does not explain a dispatch section, waiting on a set or a returned question.
- **The guide is Markdown.**
  It prints headings, code spans and a fenced block to a terminal.
- **Each dispatching bundle restates the protocols.**
  The Dispatch and Parallel dispatch paragraphs are copied into every bundle that dispatches, and only a dispatched bundle needing a first run tells its reader to run `pf`.
- **A dispatch section names a file it does not link.**
  A dispatch sub-section's line names its target's file in a code span, links the protocol instead, and calls the file a bundle.
- **Deferred dispatch is a second way to dispatch.**
  `¬⇉` and `¬⫽` publish as plain links an agent cannot tell from citations, and a section holding `[⫽ a](a.md)` and `[¬⫽ b](b.md)` publishes `a` as a set of one and `b` as a plain link.
- **Composition is spelled by an arrow.**
  A directive is a link labelled with one Unicode arrow from a list of blocks, while its deferred form reaches a bundle as a `↳` line, so an author and an agent learn two marks for one placement, and the published link carries only the arrow.
- **No marker names a returned question.**
  The eval reads a return as a question from its first word, inside a hand-back frame that wraps every return ([#637](https://github.com/m2ux/prosiform/issues/637)).

## Proposal

- **Everything is compiled up front.**
  Each distinct target a `⇉` or `⫽` link names is compiled once, transitively, into its own file in the run folder beside the main bundle, as now. The up-front refusals, `W_DISPATCH_SELF`, `W_DISPATCH_DEPTH` and `E_DISPATCH_CYCLE` stay.
- **The agent knows one mark.**
  A bundle carries `↳` and no dispatch mark.
- **A single dispatch is a section that links its file.**
  The author's prose link points at a `Dispatch <text>` section, whose line links the dispatched file, as in "Give [the crew](loading__crew.bundle.md) to a sub-agent and continue with its answer." A condition stays in the prose, on the link leading to the section. Instruction text never says "bundle"; a file name may.
- **A parallel set is one section.**
  The set's `⫽` links point at one `In parallel` section, the set's boundary, listing each member as a link to its compiled file under a plain instruction: give each to its own sub-agent at the same time, and continue when all have answered. A set of one is published as a single dispatch.
- **Every bundle opens with the run-pf line; the guide holds the rules.**
  The Prosiform section and its protocol paragraphs retire. Bare `pf` prints, as plain command-line text, how to run `pf`, what `↳` means, how a `Dispatch` and an `In parallel` section are followed, the inputs a dispatch carries, waiting for all, failures returned together, and a returned question opening with a first line reading `Question:`.
- **Deferral keeps its two plain forms.**
  `¬→` publishes as its `↳` line, its preset rule unchanged, and `[¬ x](x.md)` is a withheld link kept as a plain link at its rebased path, its target not bundled. `¬⇉` and `¬⫽` are refused with `E_UNSUPPORTED_CONSTRUCT`, naming the link; no preset behaviour is lost, since a dispatched target already selects its presets by its own heading.
- **`↳` is the composition mark.**
  `[↳ Title](p.md#s)` composes the section as an arrow directive does today, under every placement rule, its published link carrying the title text. `[¬↳ Title](p.md#s)` builds the same destination section and publishes the `[↳ Title](p.md#s)` line for the agent to inline later; the deferred-preset refusal stays. `[→](…)`, `[¬→](…)` and every other arrow label are refused with `E_UNSUPPORTED_CONSTRUCT`, pointing at `[↳ …]`, and `[⇉↳ …]` and `[⫽↳ …]` contradict. A skill's `SKILL.md` bootstrap link is unaffected, since `pf` never compiles `SKILL.md`.
- **The eval measures the new bundles.**
  The baseline's and edge run's shakedowns follow this epic's rows, and the edge workflows' scenarios and corpus test are reworked on a row of their own epic. `staged` folds into `compiled`: a `compiled` session receives the finished bundles, the build under test as `pf` and a shell limited to `pf`, so it can run bare `pf` for the guide and compile `↳` lines; `authored` is unchanged.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w00.md) | Design clause | AC1 | | | |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w01.md) | A plain-text guide holding the rules | AC2, AC3, AC4 | W00 | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w02.md) | Every bundle opening with the run-pf line | AC5 | W00 | W03, W04 | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w03.md) | A dispatch section linking its file | AC6, AC7 | W00 | W02, W04 | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w04.md) | One `In parallel` section per set | AC8, AC9 | W00 | W02, W03 | |
| [W05](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w05.md) | Deferred dispatch marks refused | AC10 | W02, W03, W04 | W08 | |
| [W06](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w06.md) | The pages stating the guide and sections | AC11 | W01, W05 | | |
| [W07](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w07.md) | One compiled form carrying `pf` | AC12, AC13, AC18 | W05 | | |
| [W08](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w08.md) | `↳` composing, arrow labels refused | AC14, AC15, AC16 | W02, W03, W04 | W05 | |
| [W09](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w09.md) | The composition page stating `↳` | AC17 | W05, W08 | | |

## Acceptance Criteria

- [ ] **AC1.** The design states the guide's text, the returned-question marker, the run-pf line every bundle opens with, the Dispatch and `In parallel` sections, a set of one, the withheld link's wording, the refusal of `¬⇉` and `¬⫽`, and `↳` as the composition mark with arrow labels refused before any build row implements them, as the design at the README's pinned commit and its revision history show.
- [ ] **AC2.** Bare `pf` prints how to run `pf`, what a `↳` link means, how a `Dispatch` section and an `In parallel` section are followed, the inputs a dispatch carries, that a set is waited on until every member answers, that failures return together, and how a returned question is handled, as the guide fixture `make check` runs shows.
- [ ] **AC3.** The guide bare `pf` prints carries no Markdown heading, emphasis, link or code fence, as a CLI test `make check` runs shows.
- [ ] **AC4.** The guide states that a dispatched run opens a returned question with a first line reading `Question:`, as the guide fixture `make check` runs shows.
- [ ] **AC5.** Every bundle a run writes opens with the run-pf line the design fixes, whatever the bundle holds, as the conformance fixtures `make check` runs show.
- [ ] **AC6.** No bundle carries a Prosiform section, a protocol paragraph or a dispatch mark, as the dispatch fixtures `make check` runs show.
- [ ] **AC7.** A `⇉` link publishes pointing at a `Dispatch <text>` section whose line links the dispatched file and whose instruction text holds no word "bundle", as the dispatch fixtures `make check` runs show.
- [ ] **AC8.** A section's `⫽` links publish pointing at one `In parallel` section listing each member as a link to its compiled file under the instruction the design fixes, as the dispatch fixtures `make check` runs show.
- [ ] **AC9.** A `⫽` set of one member publishes as a single dispatch, as a dispatch fixture `make check` runs shows.
- [ ] **AC10.** A link opening with `¬⇉` or `¬⫽` fails with `E_UNSUPPORTED_CONSTRUCT`, naming the link, and publishes nothing, as refused conformance fixtures `make check` runs show.
- [ ] **AC11.** The README and `docs/` state the guide's contents, the run-pf line and the dispatch sections in one page, and describe no Prosiform section or deferred dispatch, as a read of the pages against the guide and the fixtures shows.
- [ ] **AC12.** A `compiled` session receives the finished bundles, the build under test as `pf` on its path and a shell limited to `pf`, `Bash(pf:*)` on Claude, on every harness the default matrix runs, as a harness test `make harness` runs shows.
- [ ] **AC13.** The eval's README states one `compiled` form, that each bundle it gives opens with the run-pf line, and no `staged` form or Prosiform section, as a read of the README against the forms shows.
- [ ] **AC14.** A `[↳ Title](p.md#s)` link composes its section beneath its scope under every placement rule the arrow directive had, and the link published to the destination carries its title text, as the composition fixtures `make check` runs show.
- [ ] **AC15.** A `[¬↳ Title](p.md#s)` link builds the same destination section and publishes the `[↳ Title](p.md#s)` line, and a deferral whose scope selects other presets than its target's heading is still refused, as the deferred-composition fixtures `make check` runs show.
- [ ] **AC16.** A link labelled with an arrow, `[→](…)` and `[¬→](…)` among them, fails with `E_UNSUPPORTED_CONSTRUCT` naming the link and pointing at `[↳ …]`, and `[⇉↳ …]` and `[⫽↳ …]` fail as contradicting, each publishing nothing, as refused conformance fixtures `make check` runs show.
- [ ] **AC17.** `docs/composition.md` states `↳` as the composition mark and `¬↳` as its deferral, and no page of the README or `docs/` describes an arrow directive, as a read of the pages against the composition fixtures shows.
- [ ] **AC18.** No form is named `staged`: a run given `--forms staged` is refused as naming an unknown form, as a harness test `make harness` runs shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the work items, the decisions and the dependency check.
- **R2.** [Design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md) — *Guide*, *Link classification and resource handling*, *Section composition* and *Agent delivery contract*.
- **R3.** [Dispatch scenarios on a headless session](https://github.com/m2ux/prosiform/issues/637) — the returned question the marker settles.
