## Overview

The diagram-following eval measures how an agent follows a bundle, but no workflow it runs defers, composes or dispatches past two hops, so nothing shows an agent running `pf` on a deferred line, applying composed content under a condition, or relaying a question up a deep chain. This epic adds a shell form, the scoring that holds a session to the `pf` runs its scenario states, one workflow per edge of composition, deferral and dispatch, and one live run of them committed as its own record.

## Problem

- **No session compiles a deferred line.**
  The only compile the eval observes is whether a `bootstrap` session [ran `pf` at all](https://github.com/m2ux/prosiform/blob/ef9a884cc3e366396a4cb03f7b19914071734b03/evals/diagram-following/run.py#L604-L623), so running too few, too many or in the wrong order passes.
- **No form gives a session a bundle and the build.**
  The `compiled` form has no shell and `bootstrap` hands over sources, so a bundle carrying a `↳` line or a deferred dispatch has no form to run in.
- **The eight workflows stop short of the operators.**
  None composes a section, defers one, or dispatches more than two hops deep, so the behaviours settled for them are stated only by build fixtures.
- **A sub-agent's commands are unread.**
  The harnesses read the session's shell calls; nothing shows what a sub-agent ran before acting on its bundle.

## Proposal

- **A scenario states the `pf` runs.**
  Beside its path and dispatch trace, a scenario names each `pf` run the session and each sub-agent makes, in order, and the scorer fails a session whose runs differ with a class it names.
- **A `staged` form carries the bundle set and the build.**
  It is outside the default `--forms` and given only to a harness with a shell, so the default matrix and its baseline are unchanged.
- **One workflow per edge.**
  A bootstrapping skill's `↳` link; conditional and nested deferral; a preset-matched deferral; conditional immediate composition; arrow-only directives and self-composition; a deferred dispatch in the entry bundle; dispatch three hops deep with a set and a returned question; and a sub-agent's first `pf` run at each depth.
- **One live run, its own record.**
  The edge workflows run once on every harness carrying a shell and are committed beside the baseline in a file of their own; failing sessions are recorded by class rather than gating the run.
- **Refusals stay with the corpus.**
  A gap between symbols, a dispatch mark against a directive, a preset mismatch on deferral and an immediate-plus-deferred pair are build refusals that [#460](https://github.com/m2ux/prosiform/issues/460)'s fixtures hold; no agent meets them.
- **The boundary with the MVP proof.**
  The MVP proof's feature workflows ([#523](https://github.com/m2ux/prosiform/issues/523)) show each feature followed in its plain permutations; this epic measures the edges between them.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/pull/621) | Scenarios stating the `pf` runs a session makes | AC1 | | W02, W03, W04 | ✓ |
| [W02](https://github.com/m2ux/prosiform/pull/621) | The `staged` form for shell harnesses | AC2, AC3, AC22 | | W01, W03, W04 | ✓ |
| [W03](https://github.com/m2ux/prosiform/pull/621) | A session held to its stated runs | AC4 | | W01, W02, W04 | ✓ |
| [W04](https://github.com/m2ux/prosiform/pull/621) | Sub-agent starts and commands at every depth | AC5 | [I10:E02:W02](https://github.com/m2ux/prosiform/issues/456) | W01, W02, W03 | ✓ |
| [W05](https://github.com/m2ux/prosiform/pull/626) | A scenario bootstrapping a skill's `↳` link | AC6 | W01 | W06, W07 | ✓ |
| [W06](https://github.com/m2ux/prosiform/pull/626) | Scenarios activating conditional and nested deferrals | AC7, AC8 | W01, W02 | W05, W07 | ✓ |
| [W07](https://github.com/m2ux/prosiform/pull/626) | A scenario deferring under matched presets | AC9 | W01, W02, [I09:E04:W11](https://github.com/m2ux/prosiform/issues/460) | W05, W06 | ✓ |
| [W08](https://github.com/m2ux/prosiform/pull/628) | Scenarios composing under a conditional step | AC10 | W01, W02 | W09 | ✓ |
| [W09](https://github.com/m2ux/prosiform/pull/628) | Scenarios reading arrow, footnote and self-composition | AC11, AC12 | W01, W02, [I09:E04:W12](https://github.com/m2ux/prosiform/issues/460) | W08 | ✓ |
| [W10](https://github.com/m2ux/prosiform/pull/634) | A scenario compiling a deferred dispatch | AC13 | W01, W02 | W11, W12 | ✓ |
| [W11](https://github.com/m2ux/prosiform/pull/634) | Scenarios dispatching three hops deep | AC14, AC15, AC16 | W01, W02, W04 | W10, W12 | ✓ |
| [W12](https://github.com/m2ux/prosiform/pull/634) | Scenarios of a sub-agent's first `pf` run | AC17, AC18 | W01, W02, W04, [I09:E04:W12](https://github.com/m2ux/prosiform/issues/460) | W10, W11 | ✓ |
| [W14](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w14.md) | Live run of the edge workflows | AC20, AC24 | W03, W05, W06, W07, W08, W09, W10, W11, W12, W16 | | |
| [W15](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w15.md) | The eval page stating the edge workflows | AC21 | W14 | | |
| [W16](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w16.md) | Shake down the edge-run runbook | AC25 | W05, W06, W07, W08, W09, W11, W17, W18, W19, [I10:E06:W01](https://github.com/m2ux/prosiform/issues/639), [I10:E06:W06](https://github.com/m2ux/prosiform/issues/639) | | |
| [W17](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w17.md) | Triage rubric entries for the run classes | AC23 | W03, [I10:E05:W00](https://github.com/m2ux/prosiform/issues/594) | | |
| [W18](https://github.com/m2ux/prosiform/pull/638) | A staged Claude session carrying a shell | AC26 | W02, W04 | | ✓ |
| [W19](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w19.md) | The edge corpus test reading E06's bundles | AC27 | W10, W12, [I10:E06:W02](https://github.com/m2ux/prosiform/issues/639), [I10:E06:W03](https://github.com/m2ux/prosiform/issues/639), [I10:E06:W04](https://github.com/m2ux/prosiform/issues/639) | | |

## Acceptance Criteria

- [x] **AC1.** A scenario's `scenarios.toml` states each `pf` run a correct session and each of its sub-agents makes, in order and with its arguments, and the corpus test refuses a stated run naming no document of the workflow's sources, as the corpus test `make harness` runs shows.
- [x] **AC2.** A `staged` session receives the workflow's compiled bundle set with the build under test as `pf` on its path, as a harness test `make harness` runs shows.
- [x] **AC3.** A run gives a `staged` session only where its `--forms` names `staged` and its harness carries a shell, as a harness test `make harness` runs shows.
- [x] **AC4.** A session whose trace is its path with every action done fails with a class the scorer names where its `pf` runs omit one its scenario states, add one on a deferred line its path did not reach, or come in another order, as a scorer test `make harness` runs shows.
- [x] **AC5.** The session record lists each sub-agent's starts and shell commands under the section it followed, at every dispatch depth the harness's stream reports, as a harness test over a recorded transcript `make harness` runs shows.
- [x] **AC6.** A `bootstrap` scenario whose skill entry declares no `prosiform` and holds a hand-written `[↳ <title>](<path>)` link states bare `pf`, then `pf` on that link's path, then the path the compiled target walks, as the corpus test `make harness` runs shows.
- [x] **AC7.** A workflow whose bundle holds a `↳` line generated from `[¬→]` under a conditional step carries a scenario whose input reaches the line and states `pf` on its path, and one whose input does not and states no such run, as the corpus test `make harness` runs shows.
- [x] **AC8.** A workflow whose activated bundle holds a further `↳` line carries a scenario whose path needs the nested content and states `pf` on that line, and one whose path does not and states no such run, as the corpus test `make harness` runs shows.
- [x] **AC9.** A scenario whose deferring step heading and target heading select one preset, whose `subst` names a stand-in, states the path the stand-in's content walks, as the corpus test `make harness` runs shows.
- [x] **AC10.** A workflow holding content composed with `[→]` under a conditional step carries a scenario whose path enters the composed content's state where the condition holds, and one whose path omits it where the condition fails, as the corpus test `make harness` runs shows.
- [x] **AC11.** A scenario whose sources hold a footnote-style `[†](<path>#<section>)` link and an arrow `[→]` directive states the path that opens the footnote's target as a linked document and reads the composed section in place, as the corpus test `make harness` runs shows.
- [x] **AC12.** A scenario whose source composes a section of its own document, published with the self-composition warning, states the path its bundle walks, as the corpus test `make harness` runs shows.
- [x] **AC13.** A scenario whose entry bundle carries a deferred dispatch published as a plain link states `pf` on that link's path where its path reaches the link, and the sub-agents that run's bundle dispatches as its trace, as the corpus test `make harness` runs shows.
- [x] **AC14.** A scenario dispatching a chain three hops deep, which compiles with no `W_DISPATCH_DEPTH`, states each sub-agent's start in hop order and each returning `done` before its caller continues, as the corpus test `make harness` runs shows.
- [x] **AC15.** A scenario dispatching three hops deep with a `⫽` set at one level states every member of the set started together and returned before the chain continues, as the corpus test `make harness` runs shows.
- [x] **AC16.** A scenario whose third-hop sub-agent returns a question states that question relayed up each level to the user and the chain dispatched again with the answers, as the corpus test `make harness` runs shows.
- [x] **AC17.** A scenario whose first-hop dispatched bundle carries a `↳` line and opens with the Prosiform section saying `pf` runs first states actions of that sub-agent that only the content its `pf` run on the line compiles defines, so a sub-agent that runs no `pf` fails with a class the scorer names, as the corpus test `make harness` runs shows.
- [x] **AC18.** A scenario whose bundles at the second and third hop carry a deferred dispatch or a `↳` line states, for each such sub-agent, actions that only the content its `pf` run on that line compiles defines, so a sub-agent that runs no `pf` fails with a class the scorer names, as the corpus test `make harness` runs shows.
- [ ] **AC20.** Each harness carrying a shell has a committed edge-case record, `composition-edges-<harness>.json`, carrying a cell for every model of the default matrix, form and scenario of the edge workflows, as a comparison of the records against those workflows shows.
- [ ] **AC21.** The eval's README states the `staged` form, each edge workflow and scenario, and the pass rates each edge-case record holds, as an inspection of the README against the corpus and the records show.
- [x] **AC22.** A harness reporting no sub-agent's commands is given no scenario stating a sub-agent's `pf` run, as a harness test `make harness` runs shows.
- [ ] **AC23.** Every class the scorer gains for a session's `pf` runs has an entry in `RUNBOOK.md`'s triage rubric, as a read of the rubric against the scorer shows.
- [ ] **AC24.** Each edge-case record gives every failing session the triage rubric's disposition, as the records show.
- [ ] **AC25.** `RUNBOOK.md`'s edge-run runbook carries a shakedown over the edge workflows on each harness carrying a shell, whose measured cost sets its budget, and each rubric entry for a `pf`-run class decides a shakedown session or is recorded as produced by none, as the file shows.
- [x] **AC26.** A Claude session given the `staged` form carries a shell and no other form does, and `make eval-diagrams` gives the nested-dispatch scenarios a Claude cell whose scorer reads each start's `pf` runs, as a harness test `make harness` runs shows.
- [ ] **AC27.** The edge workflows' corpus test holds each dispatched bundle a scenario follows to the run-pf line every bundle opens with, and each deferred dispatch to the form the design publishes it in, against I10:E06's build, as the corpus test `make harness` runs shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the work items, the joins, the placement decision and the dependency check.
- **R2.** [Grouping and composition record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-463-i09-grouping-and-composition) — the composition decisions these scenarios measure.
- **R3.** [Design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md) — *Link classification and resource handling*, *Section composition* and *Guide*.

