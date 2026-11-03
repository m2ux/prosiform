## Overview

An agent meets `pf`'s marks in a skill's sources and in the bundles it compiles, and today only two of them are explained anywhere it reads. This epic makes bare `pf` print a plain-text guide giving an instruction for every mark an agent can meet, the dispatch protocols and the marker a returned question opens with, and makes every bundle open by telling its reader to run that guide first. The guide becomes the one home of those rules, so a bundle carries only its own dispatch lists, and the eval's runs measure the bundles and guide an agent now gets.

## Problem

- **The guide explains two marks.**
  Bare `pf` prints the compile step, the `↳` inline target and a pointer to a bundle's Prosiform section. Nothing an agent reads explains `⇉`, `⫽`, `¬` or an arrow directive.
- **The guide is Markdown.**
  It prints headings, code spans and a fenced block to a terminal.
- **Each dispatching bundle restates the protocols.**
  The Dispatch and Parallel dispatch paragraphs are copied into every bundle that dispatches, and only a dispatched bundle needing a first run tells its reader to run `pf`.
- **A deferred link reads as a citation.**
  The design publishes a deferred link with its marks removed, pointing at a source path, so it reads like a link to a document that declares nothing.
- **A mixed parallel set loses its members silently.**
  A section holding `[⫽ a](a.md)` and `[¬⫽ b](b.md)` publishes `a` as a set of one and `b` as a plain link, so the author's "run together" disappears.
- **No marker names a returned question.**
  The eval reads a return as a question from its first word, inside a hand-back frame that wraps every return ([#637](https://github.com/m2ux/prosiform/issues/637)).

## Proposal

- **One guide, every mark.**
  Bare `pf` prints plain command-line text giving a succinct instruction for `⇉`, `⫽`, `¬`, an arrow directive, `↳`, a dispatch sub-section, a `Dispatch in parallel` list and a returned question, and the Dispatch and Parallel dispatch protocols.
- **A fixed returned-question marker.**
  The guide states the line a dispatched run opens a returned question with, which the eval reads.
- **Every bundle opens with the run-pf line.**
  Whatever it holds, a bundle's preamble opens with one fixed line telling its reader to run bare `pf` and follow the guide. The Prosiform section and its protocol paragraphs retire; a bundle keeps only its dispatch sub-sections and `Dispatch in parallel` lists.
- **A set is deferred whole or not at all.**
  A parallel set whose members are some deferred and some immediate is refused with `E_UNSUPPORTED_CONSTRUCT`, naming the set and each member as immediate or deferred, and publishes nothing: the run says so rather than choosing. The guide's `⫽` and `¬` instructions state it.
- **The design first.**
  The design states the guide, the marker, the line and a deferred link's published form before any build row lands.
- **The eval measures the new bundles.**
  The `compiled` form can run bare `pf`, and the baseline and edge runs measure the new guide. The baseline's and edge run's shakedowns follow this epic's rows, and the edge workflows' corpus test is reconciled on a row of its own epic.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w00.md) | Design clause | AC1 | | | |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w01.md) | A plain-text guide naming every mark | AC2, AC3, AC4 | W00 | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w02.md) | Every bundle opening with the run-pf line | AC5 | W00 | W03 | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w03.md) | Dispatch lists without protocol paragraphs | AC6, AC11 | W00 | W02 | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w04.md) | A deferred link published with its marks | AC7 | W00 | | |
| [W05](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w05.md) | The pages stating the guide and line | AC8 | W01, W02, W03, W04 | | |
| [W06](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w06.md) | A compiled session able to run `pf` | AC9, AC10 | W02, W03 | | |

## Acceptance Criteria

- [ ] **AC1.** The design states the guide's instruction for every mark, the returned-question marker, the run-pf line every bundle opens with, a deferred link's published form and the refusal of a parallel set mixing deferred and immediate members before any build row implements them, as the design at the README's pinned commit and its revision history show.
- [ ] **AC2.** Bare `pf` prints an instruction for each of `⇉`, `⫽`, `¬`, an arrow directive, `↳`, a dispatch sub-section, a `Dispatch in parallel` list and a returned question, and the Dispatch and Parallel dispatch protocols, as the guide fixture `make check` runs shows.
- [ ] **AC3.** The guide bare `pf` prints carries no Markdown heading, emphasis, link or code fence, as a CLI test `make check` runs shows.
- [ ] **AC4.** The guide states the one line a dispatched run opens a returned question with, as the guide fixture `make check` runs shows.
- [ ] **AC5.** Every bundle a run writes opens with the run-pf line the design fixes, whatever the bundle holds, as the conformance fixtures `make check` runs show.
- [ ] **AC6.** No bundle carries a Prosiform section or a protocol paragraph, and a dispatching bundle carries its dispatch sub-sections and `Dispatch in parallel` lists alone, as the dispatch fixtures `make check` runs show.
- [ ] **AC7.** A deferred link, a deferred dispatch among them, is published in the form the design states, as the deferral fixtures `make check` runs show.
- [ ] **AC8.** The README and `docs/` state the guide's contents and the run-pf line in one page and describe no Prosiform section, as a read of the pages against the guide and the fixtures shows.
- [ ] **AC9.** A `compiled` session can run bare `pf` on every harness the default matrix runs, as a harness test `make harness` runs shows.
- [ ] **AC10.** The eval's README states that each bundle a form gives opens with the run-pf line and describes no Prosiform section, as a read of the README against the forms shows.
- [ ] **AC11.** A section whose `⫽` set holds both deferred and immediate members fails with `E_UNSUPPORTED_CONSTRUCT`, naming the set and each member as immediate or deferred, and publishes nothing, as a refused conformance fixture `make check` runs shows.

## Open Questions

- **A deferred link's published form.** The design strips `¬`, `⇉` and `⫽` from a deferred link, so no source operator mark reaches a bundle; only an arrow directive's label and the `↳` line do. Recommendation in the planning record: keep the marks the source wrote. W04 delivers the answer.
- **How a compiled session reaches the guide.** The `compiled` form carries no build, and a Claude session in it no shell, which E04's AC26 holds. Recommendation in the planning record: the `compiled` session carries the build on its path and a shell, and `staged` folds into it.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the work items, the decisions and the dependency check.
- **R2.** [Design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md) — *Guide*, *Link classification and resource handling*, *Section composition* and *Agent delivery contract*.
- **R3.** [Dispatch scenarios on a headless session](https://github.com/m2ux/prosiform/issues/637) — the returned question the marker settles.
