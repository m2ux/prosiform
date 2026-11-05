## Overview

The diagram-following eval supplies ordered pf-run scoring and workflows for following compiled bundles, activating deferred sections and handing dispatched bundles to sub-agents. Its corpus and harness tests cover the delivered compiled form and composition and dispatch grammar. Live edge measurements are held by the evaluation-refinement initiative.

## Problem

- **A path alone does not show which compilation occurred.**
  The scorer needs ordered pf runs for each agent, together with the source and bundle set the session received.
- **Composition and dispatch need explicit edge scenarios.**
  Conditional and nested deferral, self-composition and deep dispatch require corpus evidence of the expected path and sub-agent starts.

## Proposal

- **A scenario states each agent's `pf` runs.**
  Its ordered commands, path and sub-agent trace are checked together, so a session that compiles too little, too much or in the wrong order fails with a named class.
- **The compiled form carries its inputs.**
  A session receives the sources, the compiled bundle set and the build as `pf`, with a shell limited to it. A bootstrapping entry follows its declared bootstrap path.
- **Composition uses the declared grammar.**
  Immediate composition uses `↳`; deferred composition uses `¬↳`. A deferred section may contain a dispatch, which its later compilation publishes as an inline link or dispatch set.
- **One guide governs the reader.**
  Every bundle directs its reader to run bare `pf` before its source content; the guide describes inline `⇉` links and dispatch-set subsections. Questions return through the agent conversation.
- **One workflow per edge.**
  The corpus covers conditional, nested and preset-selected deferral; conditional and self-composition; a deferred section containing a dispatch; deep dispatch; and each sub-agent's first required compile.
- **Invalid source forms belong to conformance checks.**
  Retired arrow labels and deferred-dispatch operators are refused by the build; live workflows carry admitted forms alone.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/pull/621) | Scenarios stating the `pf` runs a session makes | AC1 |  | W02, W03, W04 | 1 | ✓ |
| [W02](https://github.com/m2ux/prosiform/pull/621) | Compiled bundles with a limited `pf` shell | AC2, AC3, AC22 |  | W01, W03, W04 | 1 | ✓ |
| [W03](https://github.com/m2ux/prosiform/pull/621) | A session held to its stated runs | AC4 |  | W01, W02, W04 | 1 | ✓ |
| [W04](https://github.com/m2ux/prosiform/pull/621) | Sub-agent starts and commands at every depth | AC5 | [I10:E02:W02](https://github.com/m2ux/prosiform/issues/456) | W01, W02, W03 | 1 | ✓ |
| [W05](https://github.com/m2ux/prosiform/pull/626) | A scenario bootstrapping a skill's `↳` link | AC6 | W01 | W06, W07 | 1 | ✓ |
| [W06](https://github.com/m2ux/prosiform/pull/626) | Scenarios activating conditional and nested deferrals | AC7, AC8 | W01, W02 | W05, W07 | 1 | ✓ |
| [W07](https://github.com/m2ux/prosiform/pull/626) | A scenario deferring under matched presets | AC9 | W01, W02, [I09:E04:W11](https://github.com/m2ux/prosiform/issues/460) | W05, W06 | 1 | ✓ |
| [W08](https://github.com/m2ux/prosiform/pull/628) | Scenarios composing under a conditional step | AC10 | W01, W02 | W09 | 1 | ✓ |
| [W09](https://github.com/m2ux/prosiform/pull/628) | Composition, footnote and self-composition scenarios | AC11, AC12 | W01, W02, [I09:E04:W12](https://github.com/m2ux/prosiform/issues/460) | W08 | 1 | ✓ |
| [W10](https://github.com/m2ux/prosiform/pull/634) | Deferred composition reaching a dispatch | AC13 | W01, W02 | W11, W12 | 1 | ✓ |
| [W11](https://github.com/m2ux/prosiform/pull/634) | Scenarios dispatching three hops deep | AC14, AC15, AC16 | W01, W02, W04 | W10, W12 | 1 | ✓ |
| [W12](https://github.com/m2ux/prosiform/pull/634) | Scenarios of a sub-agent's first `pf` run | AC17, AC18 | W01, W02, W04, [I09:E04:W12](https://github.com/m2ux/prosiform/issues/460) | W10, W11 | 1 | ✓ |
| [W17](https://github.com/m2ux/prosiform/pull/640) | Triage rubric entries for the run classes | AC23 | W03, [I10:E05:W00](https://github.com/m2ux/prosiform/issues/594) |  | 1 | ✓ |
| [W18](https://github.com/m2ux/prosiform/pull/638) | Compiled Claude per-agent command evidence | AC26 | W02, W04 |  | 1 | ✓ |
| [W19](https://github.com/m2ux/prosiform/pull/651) | Edge corpus using the declared bundle grammar | AC27, AC28, AC29 | W05, W06, W07, W08, W09, W10, W11, W12, [I10:E06:W02](https://github.com/m2ux/prosiform/issues/639), [I10:E06:W03](https://github.com/m2ux/prosiform/issues/639), [I10:E06:W04](https://github.com/m2ux/prosiform/issues/639), [I10:E06:W05](https://github.com/m2ux/prosiform/issues/639), [I10:E06:W07](https://github.com/m2ux/prosiform/issues/639), [I10:E06:W08](https://github.com/m2ux/prosiform/issues/639) |  | 2 | ✓ |

## Acceptance Criteria

- [x] **AC1.** A scenario's `scenarios.toml` states each `pf` run a correct session and each of its sub-agents makes, in order and with its arguments, and the corpus test refuses a stated run naming no document of the workflow's sources, as the corpus test `make harness` runs shows.
- [x] **AC2.** A `compiled` session receives its sources, the compiled bundle set and the build under test as `pf` on its path, as a harness test `make harness` runs shows.
- [x] **AC3.** A session receives the `compiled` form only when the selected forms include it and its harness supplies the required shell, as a harness test `make harness` runs shows.
- [x] **AC4.** A session whose trace is its path with every action done fails with a class the scorer names where its `pf` runs omit one its scenario states, add one on a deferred line its path did not reach, or come in another order, as a scorer test `make harness` runs shows.
- [x] **AC5.** The session record lists each sub-agent's starts and shell commands under the section it followed, at every dispatch depth the harness's stream reports, as a harness test over a recorded transcript `make harness` runs shows.
- [x] **AC6.** A `bootstrap` scenario whose skill entry declares no `prosiform` and holds a hand-written `[↳ <title>](<path>)` link states bare `pf`, then `pf` on that link's path, then the path the compiled target walks, as the corpus test `make harness` runs shows.
- [x] **AC7.** A workflow whose bundle holds a `↳` line from a deferred composition under a conditional step carries a scenario that reaches and compiles it, and one that does not reach it and states no such run, as the corpus test `make harness` runs shows.
- [x] **AC8.** A workflow whose activated bundle holds a further `↳` line carries a scenario whose path needs the nested content and states `pf` on that line, and one whose path does not and states no such run, as the corpus test `make harness` runs shows.
- [x] **AC9.** A scenario whose deferring step heading and target heading select one preset, whose `subst` names a stand-in, states the path the stand-in's content walks, as the corpus test `make harness` runs shows.
- [x] **AC10.** A workflow composing content with `↳` under a conditional step carries a scenario that enters the composed state when the condition holds, and one that omits it when the condition fails, as the corpus test `make harness` runs shows.
- [x] **AC11.** A scenario whose sources hold a footnote-style `[†](<path>#<section>)` link and a `↳` directive states the path that opens the footnote target as a linked document and reads the composed section in place, as the corpus test `make harness` runs shows.
- [x] **AC12.** A scenario whose source composes a section of its own document, published with the self-composition warning, states the path its bundle walks, as the corpus test `make harness` runs shows.
- [x] **AC13.** A scenario deferring a section that contains a dispatch states the `pf` run on its published line when that line is reached and the sub-agent starts its compiled content requires, as the corpus test `make harness` runs shows.
- [x] **AC14.** A scenario dispatching a chain three hops deep, which compiles with no `W_DISPATCH_DEPTH`, states each sub-agent's start in hop order and each returning `done` before its caller continues, as the corpus test `make harness` runs shows.
- [x] **AC15.** A scenario dispatching three hops deep with a `⫽` set at one level states every member of the set started together and returned before the chain continues, as the corpus test `make harness` runs shows.
- [x] **AC16.** A scenario whose third-hop sub-agent returns a question states that question relayed up each level to the user and the chain dispatched again with the answers, as the corpus test `make harness` runs shows.
- [x] **AC17.** A scenario whose first-hop dispatched bundle carries a `↳` line states actions that require the content that sub-agent compiles after reading the run-pf line, so omitting the required compile fails with a named class, as the corpus test `make harness` runs shows.
- [x] **AC18.** A scenario whose second- and third-hop bundles carry deferred content states actions at each hop that require that sub-agent to compile the reached line, so omitting a required compile fails with a named class, as the corpus test `make harness` runs shows.
- [x] **AC22.** A harness reporting no sub-agent's commands is given no scenario stating a sub-agent's `pf` run, as a harness test `make harness` runs shows.
- [x] **AC23.** Every class the scorer gains for a session's `pf` runs has an entry in `RUNBOOK.md`'s triage rubric, as a read of the rubric against the scorer shows.
- [x] **AC26.** A compiled Claude session exposes each nested sub-agent's `pf` runs to the scorer, as the nested-scenario harness test `make harness` runs shows.
- [x] **AC27.** Each edge workflow uses admitted operator forms: composition is written `↳` or `¬↳`, and no source writes `¬⇉`, `¬⫽` or an arrow-labelled link, as the corpus tests `make harness` runs show.

- [x] **AC28.** Every non-bootstrap edge scenario supplies a `compiled` form and no `staged` form, as the corpus and runner tests `make harness` runs show.
- [x] **AC29.** Each dispatched target an edge scenario follows is a written bundle carrying the run-pf instruction before its source content, as the dispatch-bundle corpus tests `make harness` runs show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the work items, the joins, the placement decision and the dependency check.
- **R2.** [Grouping and composition record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-463-i09-grouping-and-composition) — the composition decisions these scenarios measure.
- **R3.** [Design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md) — *Link classification and resource handling*, *Section composition* and *Guide*.
- **R4.** [Board alignment](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-05-project-18-alignment/alignment.md) — the confirmed criterion reconciliation, lane evidence and verification results.

- **R5.** [Evaluation Refinement](https://github.com/m2ux/prosiform/issues/660) — the deferred shakedown, live edge run and publication, with their source criteria and work-item mapping.
