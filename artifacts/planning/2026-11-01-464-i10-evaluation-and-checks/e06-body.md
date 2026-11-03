## Overview

An agent following a bundle meets `↳` and `⇉` links, dispatch sections and returned questions, and the guide bare `pf` prints explains only the first. This epic makes bare `pf` print a plain-text guide stating what an agent does with each, the dispatch rules among them and the marker a returned question opens with, and makes every bundle open by telling its reader to run that guide first. The guide becomes the one home of those rules, so a bundle carries only its own dispatch lists. A deferred dispatch keeps its `⇉` mark in the bundle, and a parallel set lists its deferred members beside its compiled ones.

## Problem

- **The guide explains one mark.**
  Bare `pf` prints the compile step, the `↳` inline target and a pointer to a bundle's Prosiform section. It does not explain `⇉`, a dispatch section or a returned question.
- **The guide is Markdown.**
  It prints headings, code spans and a fenced block to a terminal.
- **Each dispatching bundle restates the protocols.**
  The Dispatch and Parallel dispatch paragraphs are copied into every bundle that dispatches, and only a dispatched bundle needing a first run tells its reader to run `pf`.
- **A deferred dispatch reads as a citation.**
  A deferred `⇉` link is published with its mark removed, pointing at a source path, so it reads like a link to a document that declares nothing.
- **A deferred parallel member falls out of its set.**
  A section holding `[⫽ a](a.md)` and `[¬⫽ b](b.md)` publishes `a` as a set of one and `b` as a plain link, so the author's "run together" disappears.
- **No marker names a returned question.**
  The eval reads a return as a question from its first word, inside a hand-back frame that wraps every return ([#637](https://github.com/m2ux/prosiform/issues/637)).

## Proposal

- **One guide, in plain text.**
  Bare `pf` prints command-line text with no Markdown. It states that `[↳ x](path)` is compiled and kept in context, followed inline; that `[⇉ x](path)` is compiled and dispatched to a sub-agent; how a Dispatch sub-section and a `Dispatch in parallel` section are followed; and the line a dispatched run opens a returned question with. `⫽` and `¬` never reach a bundle, so the guide does not teach them.
- **Every bundle opens with the run-pf line.**
  Whatever it holds, a bundle's preamble opens with one fixed line telling its reader to run bare `pf` and follow the guide. The Prosiform section and its protocol paragraphs retire; a bundle keeps only its Dispatch sub-sections and `Dispatch in parallel` sections.
- **A deferred dispatch keeps its mark.**
  A deferred `⇉` is published as `[⇉ four](four.md#do)`, its path rebased so it resolves from where the agent runs `pf`.
- **A parallel set lists deferred and compiled members together.**
  A deferred `⫽` member keeps no `⫽`; the set is built as an immediate set is, its prose links pointing at `#dispatch-in-parallel`. The section lists a compiled member as its bundle file, ``- `two__do.bundle.md` (two)``, and a deferred member as a deferred dispatch, `- [⇉ five](five.md#do)`. The guide's rule: compile each `⇉` item first, then dispatch the whole set together, and dispatch none if any compile fails.
- **A set of one is a plain dispatch.**
  A one-member set, deferred or immediate, publishes as a Dispatch sub-section or a deferred `[⇉ x]` link, never a parallel list of one.
- **The design first.**
  The design states the guide, the marker, the run-pf line and the published dispatch forms before any build row lands.
- **The eval measures the new bundles.**
  The baseline's and edge run's shakedowns follow this epic's rows, and the edge workflows' corpus test is reconciled on a row of its own epic. How the `compiled` form follows a bundle opening with the run-pf line is an open question, and the row reconciling that form waits on it.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w00.md) | Design clause | AC1 | | | |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w01.md) | A plain-text guide stating what bundles carry | AC2, AC3, AC4 | W00 | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w02.md) | Every bundle opening with the run-pf line | AC5 | W00 | W03, W04 | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w03.md) | Dispatch sections without protocols, sets mixing members | AC6, AC11, AC12 | W00 | W02, W04 | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w04.md) | A deferred dispatch published with its mark | AC7 | W00 | W02, W03 | |
| [W05](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w05.md) | The pages stating the guide and line | AC8 | W01, W02, W03, W04 | | |
| [W06](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w06.md) | The compiled form following the run-pf line | AC9, AC10 | W02, W03, W04 | | |

## Acceptance Criteria

- [ ] **AC1.** The design states the guide's text, the returned-question marker, the run-pf line every bundle opens with, a deferred dispatch's published form, a parallel set's deferred members and a set of one before any build row implements them, as the design at the README's pinned commit and its revision history show.
- [ ] **AC2.** Bare `pf` prints an instruction for a `↳` link, a `⇉` link, a Dispatch sub-section, a `Dispatch in parallel` section, whose instruction compiles each `⇉` item before the set is dispatched together and dispatches none if a compile fails, and a returned question, as the guide fixture `make check` runs shows.
- [ ] **AC3.** The guide bare `pf` prints carries no Markdown heading, emphasis, link or code fence, as a CLI test `make check` runs shows.
- [ ] **AC4.** The guide states the one line a dispatched run opens a returned question with, as the guide fixture `make check` runs shows.
- [ ] **AC5.** Every bundle a run writes opens with the run-pf line the design fixes, whatever the bundle holds, as the conformance fixtures `make check` runs show.
- [ ] **AC6.** No bundle carries a Prosiform section or a protocol paragraph, and a dispatching bundle carries its Dispatch sub-sections and `Dispatch in parallel` sections alone, as the dispatch fixtures `make check` runs show.
- [ ] **AC7.** A deferred dispatch is published as a `⇉` link at its path rebased to the invocation working directory, as the deferral fixtures `make check` runs show.
- [ ] **AC8.** The README and `docs/` state the guide's contents and the run-pf line in one page and describe no Prosiform section, as a read of the pages against the guide and the fixtures shows.
- [ ] **AC9.** A session in the `compiled` form follows a bundle opening with the run-pf line on every harness the default matrix runs, in the form the open question settles, as a harness test `make harness` runs shows.
- [ ] **AC10.** The eval's README states that each bundle a form gives opens with the run-pf line and describes no Prosiform section, as a read of the README against the forms shows.
- [ ] **AC11.** A parallel set mixing deferred and immediate members publishes one `Dispatch in parallel` section listing each compiled member as its bundle file and each deferred member as a `⇉` link, every member's prose link pointing at that section, as a dispatch fixture `make check` runs shows.
- [ ] **AC12.** A parallel set of one member publishes as a Dispatch sub-section when immediate and as a `⇉` link when deferred, never as a parallel list, as dispatch fixtures `make check` runs show.

## Open Questions

- **What the `compiled` form becomes.** Every bundle now says to run `pf`, and the `compiled` form gives a session no build and, on Claude, no shell, which E04's AC26 holds. W06 waits on the answer; the options are in the planning record.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the work items, the decisions and the dependency check.
- **R2.** [Design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md) — *Guide*, *Link classification and resource handling*, *Section composition* and *Agent delivery contract*.
- **R3.** [Dispatch scenarios on a headless session](https://github.com/m2ux/prosiform/issues/637) — the returned question the marker settles.
