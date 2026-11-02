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
- **The first-run carrier is compared.**
  Two further forms rewrite the dispatched bundles' Prosiform first-run section as a frontmatter entry and as a top blockquote line.
- **One live run, its own record.**
  The edge workflows run once on every harness carrying a shell and are committed beside the baseline in a file of their own; failing sessions are recorded by class rather than gating the run.
- **Refusals stay with the corpus.**
  A gap between symbols, a dispatch mark against a directive, a preset mismatch on deferral and an immediate-plus-deferred pair are build refusals that [#460](https://github.com/m2ux/prosiform/issues/460)'s fixtures hold; no agent meets them.
- **The boundary with the MVP proof.**
  The MVP proof's feature workflows ([#523](https://github.com/m2ux/prosiform/issues/523)) show each feature followed in its plain permutations; this epic measures the edges between them.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w01.md) | Scenarios stating the `pf` runs a session makes | AC1 | | W02, W03, W04 | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w02.md) | The `staged` form for shell harnesses | AC2, AC3, AC22 | | W01, W03, W04 | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w03.md) | A session held to its stated runs | AC4 | | W01, W02, W04 | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w04.md) | Sub-agent starts and commands at every depth | AC5 | | W01, W02, W03 | |
| [W05](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w05.md) | A scenario bootstrapping a skill's `↳` link | AC6 | W01 | W06, W07 | |
| [W06](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w06.md) | Scenarios activating conditional and nested deferrals | AC7, AC8 | W01, W02 | W05, W07 | |
| [W07](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w07.md) | A scenario deferring under matched presets | AC9 | W01, W02, [I09:E04:W11](https://github.com/m2ux/prosiform/issues/460) | W05, W06 | |
| [W08](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w08.md) | Scenarios composing under a conditional step | AC10 | W01, W02 | W09 | |
| [W09](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w09.md) | Scenarios reading arrow, footnote and self-composition | AC11, AC12 | W01, W02, [I09:E04:W12](https://github.com/m2ux/prosiform/issues/460) | W08 | |
| [W10](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w10.md) | A scenario compiling a deferred dispatch | AC13 | W01, W02 | W11, W12 | |
| [W11](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w11.md) | Scenarios dispatching three hops deep | AC14, AC15, AC16 | W01, W02, W04 | W10, W12 | |
| [W12](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w12.md) | Scenarios of a sub-agent's first `pf` run | AC17, AC18 | W01, W02, W04, [I09:E04:W12](https://github.com/m2ux/prosiform/issues/460) | W10, W11 | |
| [W13](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w13.md) | Frontmatter and blockquote first-run carriers | AC19 | W12 | | |
| [W14](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w14.md) | Live run of the edge workflows | AC20 | W03, W05, W06, W07, W08, W09, W10, W11, W13 | | |
| [W15](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w15.md) | The eval page stating the edge workflows | AC21 | W14 | | |

## Acceptance Criteria

- [ ] **AC1.** A scenario's `scenarios.toml` states each `pf` run a correct session and each of its sub-agents makes, in order and with its arguments, and the corpus test refuses a stated run naming no document of the workflow's sources, as the corpus test `make harness` runs shows.
- [ ] **AC2.** A `staged` session receives the workflow's compiled bundle set with the build under test as `pf` on its path, as a harness test `make harness` runs shows.
- [ ] **AC3.** A run gives a `staged` session only where its `--forms` names `staged` and its harness carries a shell, as a harness test `make harness` runs shows.
- [ ] **AC4.** A session whose trace is its path with every action done fails with a class the scorer names where its `pf` runs omit one its scenario states, add one on a deferred line its path did not reach, or come in another order, as a scorer test `make harness` runs shows.
- [ ] **AC5.** The session record lists each sub-agent's starts and shell commands under the section it followed, at every dispatch depth the harness's stream reports, as a harness test over a recorded transcript `make harness` runs shows.
- [ ] **AC6.** A `bootstrap` scenario whose skill entry declares no `prosiform` and holds a hand-written `[↳ <title>](<path>)` link states bare `pf`, then `pf` on that link's path, then the path the compiled target walks, as the corpus test `make harness` runs shows.
- [ ] **AC7.** A workflow whose bundle holds a `↳` line generated from `[¬→]` under a conditional step carries a scenario whose input reaches the line and states `pf` on its path, and one whose input does not and states no such run, as the corpus test `make harness` runs shows.
- [ ] **AC8.** A workflow whose activated bundle holds a further `↳` line carries a scenario whose path needs the nested content and states `pf` on that line, and one whose path does not and states no such run, as the corpus test `make harness` runs shows.
- [ ] **AC9.** A scenario whose deferring step heading and target heading select one preset, whose `subst` names a stand-in, states the path the stand-in's content walks, as the corpus test `make harness` runs shows.
- [ ] **AC10.** A workflow holding content composed with `[→]` under a conditional step carries a scenario whose path enters the composed content's state where the condition holds, and one whose path omits it where the condition fails, as the corpus test `make harness` runs shows.
- [ ] **AC11.** A scenario whose sources hold a footnote-style `[†](<path>#<section>)` link and an arrow `[→]` directive states the path that opens the footnote's target as a linked document and reads the composed section in place, as the corpus test `make harness` runs shows.
- [ ] **AC12.** A scenario whose source composes a section of its own document, published with the self-composition warning, states the path its bundle walks, as the corpus test `make harness` runs shows.
- [ ] **AC13.** A scenario whose entry bundle carries a deferred dispatch published as a plain link states `pf` on that link's path where its path reaches the link, and the sub-agents that run's bundle dispatches as its trace, as the corpus test `make harness` runs shows.
- [ ] **AC14.** A scenario dispatching a chain three hops deep, which compiles with no `W_DISPATCH_DEPTH`, states each sub-agent's start in hop order and each returning `done` before its caller continues, as the corpus test `make harness` runs shows.
- [ ] **AC15.** A scenario dispatching three hops deep with a `⫽` set at one level states every member of the set started together and returned before the chain continues, as the corpus test `make harness` runs shows.
- [ ] **AC16.** A scenario whose third-hop sub-agent returns a question states that question relayed up each level to the user and the chain dispatched again with the answers, as the corpus test `make harness` runs shows.
- [ ] **AC17.** A scenario whose first-hop dispatched bundle carries a `↳` line and opens with the Prosiform section saying `pf` runs first states that sub-agent's bare `pf` run before its `pf` run on the line, as the corpus test `make harness` runs shows.
- [ ] **AC18.** A scenario whose bundles at the second and third hop carry a deferred dispatch or a `↳` line states each such sub-agent's bare `pf` run before its `pf` run on that line, as the corpus test `make harness` runs shows.
- [ ] **AC19.** The sub-agent first-run scenarios run in two further forms whose dispatched bundles carry the instruction to run `pf` first as a frontmatter entry and as a top blockquote line, with no Prosiform first-run section, as a harness test `make harness` runs shows.
- [ ] **AC20.** The committed edge-case record carries a cell for every model of the default matrix, harness carrying a shell, form and scenario of the edge workflows, as a comparison of the record against those workflows shows.
- [ ] **AC21.** The eval's README states the `staged` and carrier forms, each edge workflow and scenario, and the pass rates the edge-case record holds, as an inspection of the README against the corpus and the record shows.
- [ ] **AC22.** A harness reporting no sub-agent's commands is given no scenario stating a sub-agent's `pf` run, as a harness test `make harness` runs shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the work items, the joins, the placement decision and the dependency check.
- **R2.** [Grouping and composition record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-463-i09-grouping-and-composition) — the composition decisions these scenarios measure.
- **R3.** [Design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md) — *Link classification and resource handling*, *Section composition* and *Guide*.
