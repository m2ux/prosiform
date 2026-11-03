## Overview

An agent following a bundle meets `↳` links, dispatch sections and returned questions, and the guide bare `pf` prints explains only the first. This epic makes bare `pf` print a plain-text guide holding every rule an agent follows a bundle by, and makes every bundle open by telling its reader to run that guide first. Dispatched targets stay compiled up front, each into a file of its own; a bundle carries no protocol and no dispatch mark, only plain sections that link each dispatched file. The deferred dispatch marks, `¬⇉` and `¬⫽`, retire.

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
- **The eval measures the new bundles.**
  The baseline's and edge run's shakedowns follow this epic's rows, and the edge workflows' scenarios and corpus test are reworked on a row of their own epic. How the `compiled` form follows a bundle opening with the run-pf line is an open question, and the row reconciling that form waits on it.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w00.md) | Design clause | AC1 | | | |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w01.md) | A plain-text guide holding the rules | AC2, AC3, AC4 | W00 | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w02.md) | Every bundle opening with the run-pf line | AC5 | W00 | W03, W04, W05 | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w03.md) | A dispatch section linking its file | AC6, AC7 | W00 | W02, W04, W05 | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w04.md) | One `In parallel` section per set | AC8, AC9 | W00 | W02, W03, W05 | |
| [W05](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w05.md) | Deferred dispatch marks refused | AC10 | W00 | W02, W03, W04 | |
| [W06](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w06.md) | The pages stating the guide and sections | AC11 | W01, W02, W03, W04, W05 | | |
| [W07](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w07.md) | The compiled form following the run-pf line | AC12, AC13 | W02, W03, W04, W05 | | |

## Acceptance Criteria

- [ ] **AC1.** The design states the guide's text, the returned-question marker, the run-pf line every bundle opens with, the Dispatch and `In parallel` sections, a set of one, the withheld link's wording and the refusal of `¬⇉` and `¬⫽` before any build row implements them, as the design at the README's pinned commit and its revision history show.
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
- [ ] **AC12.** A session in the `compiled` form follows a bundle opening with the run-pf line on every harness the default matrix runs, in the form the open question settles, as a harness test `make harness` runs shows.
- [ ] **AC13.** The eval's README states that each bundle a form gives opens with the run-pf line and describes no Prosiform section, as a read of the README against the forms shows.

## Open Questions

- **What the `compiled` form becomes.** Every bundle now says to run `pf`, and the `compiled` form gives a session no build and, on Claude, no shell, which E04's AC26 holds. W07 waits on the answer; the options are in the planning record.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the work items, the decisions and the dependency check.
- **R2.** [Design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md) — *Guide*, *Link classification and resource handling*, *Section composition* and *Agent delivery contract*.
- **R3.** [Dispatch scenarios on a headless session](https://github.com/m2ux/prosiform/issues/637) — the returned question the marker settles.
