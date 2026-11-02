# I09 Grouping and Composition — November 2026

> Initiative planning · Created 2026-11-02

## Executive Summary

I09 decides where each document arrives in a bundle's outline: a file's `group` pair places its own sections in the result its parent merges, a destination answers the one document a reference named, and a section a reference composes sits beneath the heading naming it.

The initiative was split out of I05 with its epics raised as standalone issues and no work items. This record gives every row a work item and a declared component, adds the design-clause rows, checks the dependency graph, accounts for every candidate unit, traces each initiative criterion to the goal, and records what earlier work already delivered of the grouping-targets epic.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [E01 W00 work item](e01/w00.md) | The design listing one member per destination among the invariants |
| [E01 W01 work item](e01/w01.md) | Candidate validation refusing a heading that answers two members |
| [E01 W02 work item](e01/w02.md) | The validation page naming the invariant |
| [E02 W00 work item](e02/w00.md) | The design stating leaves-up composition |
| [E02 W01 work item](e02/w01.md) | Each file composed under its own pairs before its parent merges it |
| [E02 W02 work item](e02/w02.md) | An intermediate group nested in its parent's result |
| [E02 W03 work item](e02/w03.md) | The invocation guide stating placement |
| [E02 W04 work item](e02/w04.md) | The hierarchy page stating the titled member's heading |
| [E04 W00 work item](e04/w00.md) | The design declaring the composition contract |
| [E04 W01 work item](e04/w01.md) | Recognition of the reserved label |
| [E04 W02 work item](e04/w02.md) | Sections composed into their scope |
| [E04 W03 work item](e04/w03.md) | Contributions keeping their source |
| [E04 W04 work item](e04/w04.md) | Ordering, matching and diagnostics |
| [E04 W05 work item](e04/w05.md) | Recursion bounded and budgeted |
| [E04 W06 work item](e04/w06.md) | The eligible target and deferred activation |
| [E04 W07 work item](e04/w07.md) | Nothing published from a failed composition |
| [E04 W08 work item](e04/w08.md) | Inline-only targets bundled once |
| [E04 W09 work item](e04/w09.md) | Composition under presets and `subst` |
| [E04 W10 work item](e04/w10.md) | The composition page |
| [E05 W01 work item](e05/w01.md) | The whole-product review against the pinned design |
| [E05 W02 work item](e05/w02.md) | The repository README brought to the build |
| [E05 W03 work item](e05/w03.md) | The invocation guide brought to the build |
| [E05 W04 work item](e05/w04.md) | The checks page brought to the build |
| [E05 W05 work item](e05/w05.md) | The checks README brought to the build |
| [E05 W06 work item](e05/w06.md) | The docs index brought to the build |
| [E05 W07 work item](e05/w07.md) | The architecture page brought to the source, read through GitNexus |
| [E05 W08 work item](e05/w08.md) | The bundles page brought to the build |
| [E05 W09 work item](e05/w09.md) | The destinations page brought to the build |
| [E05 W10 work item](e05/w10.md) | The diagram-renderer page brought to the build |
| [E05 W11 work item](e05/w11.md) | The dispatch page brought to the build |
| [E05 W12 work item](e05/w12.md) | The glossary brought to the build |
| [E05 W13 work item](e05/w13.md) | The hierarchy page brought to the build |
| [E05 W14 work item](e05/w14.md) | The output-budget page brought to the build |
| [E05 W15 work item](e05/w15.md) | The references page brought to the build |
| [E05 W16 work item](e05/w16.md) | The selection page brought to the build |
| [E05 W17 work item](e05/w17.md) | The sources page brought to the build |
| [E05 W18 work item](e05/w18.md) | The validation page brought to the build |
| [E05 W19 work item](e05/w19.md) | The versioning page brought to the build |
| [E05 W20 work item](e05/w20.md) | The fixtures README brought to the build |
| [E05 W21 work item](e05/w21.md) | The eval page brought to the build |
| [E05 W22 work item](e05/w22.md) | The preset selection workflow and its scenarios |
| [E05 W23 work item](e05/w23.md) | The `group` placement workflow and its scenarios |
| [E05 W24 work item](e05/w24.md) | The `subst` workflow and its scenarios |
| [E05 W25 work item](e05/w25.md) | The section entry workflow and its scenarios |
| [E05 W26 work item](e05/w26.md) | The section composition workflow and its scenarios |
| [E05 W27 work item](e05/w27.md) | The declared inclusion workflow and its scenarios |
| [E05 W28 work item](e05/w28.md) | The live default-matrix run committed as `mvp-proof.json` |
| [E05 W29 work item](e05/w29.md) | The eval page stating the feature workflows and the proof |
| [Joins](joins.md) | The candidate unit that ships as separate pull requests, and why |
| [Change list](change-list.md) | The plan changes this run applied and held |
| [A: agent review of #541](agent-review-541.json) | The agent review record of the I09:E02 integration pull request, by reviewed head and target |

## Goal

The goal is the initiative's Overview: every document arrives under a heading a reader can find. Its clauses:

- **G1.** A reference reaches the document it named.
- **G2.** A file's `group` pair places its own sections, composed from the leaves up.
- **G3.** A referenced section sits where it is named.
- **G4.** The MVP is proven: an agent follows each merged feature from its compiled bundle on a live run.

## Goal Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| G2 | AC1 | E02 | E02 AC1–AC7 | No marked source |
| G3 | AC2 | E04 | E04 AC1–AC19 | No marked source |
| G4 | AC3 | E05 | E05 AC1–AC33 | No marked source |

Each initiative criterion states one clause's outcome and is made true by the one epic citing it: E02 AC1–AC4 compose each file under its own pairs before its parent merges it, E04 AC3 with AC4 places a composed section beneath its containing heading, and E05 AC23–AC30 run a workflow per feature live, after AC1–AC22 bring the build and every page to the pinned design.

### Gaps, Ranked

None remain. Every clause has a criterion, every criterion is delivered by one epic and traces to one clause, and every epic criterion is covered by a task row. The initiative marks no requirement source.

### Outside Threats

- **Every design-clause row moves the README pin on `main`.** The three W00 rows declare the design file and contend; the priority map separates them.
- **Composition and leaves-up assembly meet in `cli.py`.** E02 W01–W02 and E04 W07–W09 contend; the priority map separates the epics.
- **E04 W09 waits on undelivered I08 work.** It depends on I08:E06 W06, the writer's `subst` reaching only its own document's links.
- **The example tree is removed.** I08:E08 W00 removes it and every check and fixture built on it; no row here changes, reads or proves on it.
- **E05 waits on I08.** (User, 2026-11-02.) E05 W01 depends on E02 and E04 and on I08's final rows (E03 W05, E04 W05, E05 W02 and W05, E06 W10 and W11, E08 W03), so the review starts only once everything it reviews has merged.

## E01 Against Earlier Work

E01 was raised to make a reference to a pooled heading reach its own document's variant. That is delivered:

- **The reference rule.** Commit [02ec51b1](https://github.com/m2ux/prosiform/commit/02ec51b1) (part of #263, merged through #320) resolves a reference into a shared section to its document's variant heading, and to the merged heading where one document contributes it.
- **The clause and the fixture agree.** *Merged section references* states the variant rule, and `grouping/a-reference-to-a-grouping-depth-heading` records `#plan` and `#review` for the two documents' `#procedure`, its description stating the same rule.
- **Titled parents.** I07's #488 sends a titled parent's whole-document reference inside a merged group to its title at every grouping depth, and #497 (task #490) does the same for a titled entry heading its own file group. These are whole-document references, beside E01's section references.

What remains is enforcement: *A heading for every member* concludes that no two members reach one destination, and candidate validation's target integrity passes a heading that answers two members' targets, which is how the regression 02ec51b1 repaired stayed green. E01 is restated to that: a design clause (W00), the candidate check (W01) and the validation page (W02). Its former AC1–AC3 and rows W01–W02 leave the epic as delivered.

## Design

- **A design-clause row opens each epic.** E01 and E02 gain W00, as E04 has, so every fixture cites a clause the pinned design carries.
- **Leaves-up composition is one pull request.** E02 W01 and W02 extend `cli.py` with one structural change and four criteria, so they join; the unit re-records the fixtures its arrangement changes.
- **The hierarchy page is its own row.** E02 W03 named the invocation guide and the hierarchy page, two components, so the hierarchy page's criterion moves to W04.
- **The composition grammar page is its own row.** E04 W08 named a documentation page and an assembly behaviour; the behaviour (AC17) stays W08 on `cli.py`, and the page (AC16) becomes W10 after every behaviour row it describes.
- **Composition obeys presets and `subst`.** E04 W09 covers AC18 and AC19; preset `include` and `exclude` are removed from the design, so no row reads them.

## Dependency Check

`deps.py` over the initiative, the three epics, the nineteen work items and [joins.md](joins.md):

- **Problems.** None.
- **Joins.** E02 W01 and W02 joined. E04 W01–W06 extend `composition.py` and are split by rule, thirteen criteria exceeding the bound of six. E04 W07–W09 are accounted for in [joins.md](joins.md).
- **Advisory numbering.** E04 W08 (level 3) is numbered after W07 (level 7); the rows keep their published numbers.
- **Longest chain.** Nine steps: E04:W00 → W01 → W02 → W03 → W04 → W05 → W06 → W07 → W10.
- **Contention.** The three W00 rows on the design file; E02 W01 and W02 against E04 W07, W08 and W09 on `main:src/prosiform/cli.py`.
- **Epic priority.** E01 3, E02 2, E04 1. No epic depends on another; contention separates them.

## Decisions

- **A deferral keeps its step's presets or is refused.** (User, 2026-11-02.) A deferred directive whose containing heading selects other presets than its target's own heading selects is refused, naming the link and both selections: activation selects by the target's heading, and no option names a referrer, so deferred content would compile otherwise than composed. Row W11, AC20.
- **A section is composed or deferred, not both.** (User, 2026-11-02.) A scope that composes a section immediately and also defers it is refused, naming both directives. Row W11, AC21.
- **No authoring guidance on conditional composition.** (User, 2026-11-02.) The grammar page states no rule about deferring conditionally needed content.
- **Activation is its own entry run.** (User, 2026-11-02.) The run a deferred directive's generated line names compiles the target as an entry and publishes its own bundle; the earlier bundle keeps the line. A nested deferral may be taken conditionally, so only the agent following the bundle can decide whether to run `pf` on it. AC13 is reworded to this outcome.
- **E01 restated to enforcement.** (Planning, from the brief.) The delivered reference rule leaves the epic with its criteria; the invariant check and its page stay.
- **Preset `include` and `exclude` removed.** (User, 2026-11-02.) E04 drops AC20 and its Proposal clause; W09 covers presets and `subst`.
- **Vocabulary.** (User.) "`group` pairs" replaces "group rules" in the initiative and E02, E02's title included.
- **Epic priority.** (User, 2026-11-02.) E01 `priority: 3`, E02 `priority: 2`, E04 `priority: 1`, as the dependency check proposes.
- **E02's example row dropped as delivered.** (User, 2026-11-02.) I08:E01 W02 (commit `ea80ce79`) moved every pair onto its leaf. At the I08:E01 base [bb404015](https://github.com/m2ux/prosiform/tree/bb404015/example/work-planner), all 44 documents under `artifacts`, `protocols` and `references` declare one pair naming their own directory's group at depth 1, and none of the 15 others (`SKILL.md`, `configuration.md`, `conventions.md`, `guidelines.md`, `rules.md` and the ten modes) declares any pair. E02 drops the row and its two criteria; the hierarchy row becomes W04 and the criteria renumber to AC1–AC7.
- **Initiative criteria are the clauses' outcomes.** (User, 2026-11-02.) One criterion per goal clause replaces the fixture, page, per-revision check and closure criteria; each epic row covers its clause's criterion.
- **Non-Goals.** (User, 2026-11-02.) The four drafted Non-Goals stand.
- **Grouping Targets moves to I10.** (User, 2026-11-02.) The epic holds an existing rule by validation and changes where nothing arrives, so it serves I10's measurement that can fail. It is I10:E03 (#455) with `priority: 1`; G1 and its criterion leave this initiative, the remaining criteria renumber to AC1–AC2, and its work items stay in `e01/` here, which #455 links. The sections above that name E01 record how it was planned.
- **I09 precedes I10.** (User, 2026-11-02.) I09 `priority: 2` and I10 `priority: 1`, so the MVP's I08 and I09 are delivered before the evaluation work.
- **E05 proves the MVP.** (User, 2026-11-02.) Its scope is a whole-product review of everything merged since `contract/v0.15.0` with every finding fixed in this epic, every documentation page brought to the build (architecture included, verified against the source), a workflow per feature with a scenario per permutation, and one live run. It adds no design-clause row, since it adds no corpus fixture citing the design. G4 and AC3 are its goal clause and criterion.
- **The proof is the full default matrix.** (User, 2026-11-02.) One live run over every model, harness and form the default matrix runs.
- **The proof is its own file.** (User, 2026-11-02.) The run is committed as `evals/diagram-following/mvp-proof.json` beside the baseline; `baseline.json` is I10:E00 W02's and stays untouched.
- **The example tree is not evidence.** (User, 2026-11-02.) It is removed by I08:E08 W00, so no row reads, maintains or proves on it.
- **Undelivered rows test on surviving checks.** (User, 2026-11-02.) With the example tree and its checks removed, a row's test cites a check that survives: E02 W01 re-records the corpus fixtures its order changes, and E02 W03 and AC5 rest on `make invocation`, `make links` and a read of the guide against the pinned design.
- **The documentation row is one row per page.** (Planning.) A row extends one component, so the user's single documentation row is twenty, each with one criterion naming its page and how agreement is shown.
- **MVP order.** (User, 2026-11-02.) Initiative priority labels are I08 `priority: 4`, I09 `priority: 3`, I11 `priority: 2` and I10 `priority: 1`, so the MVP's I08 and I09 are delivered, then its release, then the evaluation work. I07 keeps its label. This supersedes the I09 `priority: 2` and I10 `priority: 1` decision above.
- **I10 precedes I11.** (User, 2026-11-02.) I10 [#464](https://github.com/m2ux/prosiform/issues/464) takes `priority: 2` and I11 [#524](https://github.com/m2ux/prosiform/issues/524) `priority: 1`, so the measurement work is delivered before the MVP release is cut.
- **Epic priority by order.** (User, 2026-11-02.) E02 `priority: 3`, E04 `priority: 2`, E05 `priority: 1`, the order E05's edges set.
- **The live run's pass bar.** (User, 2026-11-02.) E05 AC30 requires every feature scenario to pass every run in at least one model, harness and form cell, and no cell to pass no run; failing runs are recorded with the class the scorer names. Agents are not deterministic, so a bar of every run in every cell would block on noise rather than on the bundle.
- **A composed section is governed by `subst`, not placed.** (User, 2026-11-02.) E04's design clause gives a `group` pair no say over a composed contribution, so AC18 reads that a selected preset's `subst` governs the composed section.
- **Operator symbols are written together.** (User, 2026-11-02.) No blank stands between two symbols, and the one blank stands between the last symbol and the link's text. `[¬→](a.md#out)` is a deferred directive and `[¬⇉ the rules](rules.md)` a deferred dispatch; `[¬ →]`, `[¬ ⇉ x]` and `[⇉ →]` are refused with `E_UNSUPPORTED_CONSTRUCT`. A single mark then a blank then text, and a mark followed directly by plain text, keep their meaning. *Operators that combine* in the design states the rule; E04 W06 delivers it.
- **A dispatch mark against a directive's label is refused.** (User, 2026-11-02.) A dispatch sends its material to a sub-agent and a directive places it inline, so `[⇉→](a.md#out)`, `[⫽→](a.md#out)` and `[¬⇉→](a.md#out)` are refused with `E_UNSUPPORTED_CONSTRUCT`, naming the link, where W06 left `[⇉→]` an ordinary link of two characters. *Operators that combine* in the design states the rule; E04 W07 delivers it as folded work.
- **E05 rows name their work and join by area.** (User, 2026-11-02.) Each E05 Description names the work done rather than restating its criterion, and the twenty page rows join into four delivery units: the top-level pages (W02–W06), `docs/` architecture to glossary (W07–W12), `docs/` hierarchy to validation (W13–W18), and versioning with the fixtures and eval READMEs (W19–W21).
- **A nested group past H6 fails.** (User, 2026-11-02.) A shared group nests under the division of the document that placed its first member, and a heading pushed past H6 is refused with `E_HEADING_DEPTH_OVERFLOW`; the build does not lift shared groups to the top level. The refusal makes the author choose a shallower grouping. The guide (W03) and the hierarchy page (W04) state the nesting cost and that remedy.
- **Earlier decisions stand.** (User, 2026-11-02.) E00 and E03 are closed; an earlier E02 row was dropped as delivered by I08; a composed target declaring no `prosiform` is refused.

## MVP Proof

E05 proves the MVP: the I08 and I09 work merged into `main` since `contract/v0.15.0`.

- **Review, then documentation, then scenarios, then the run.** W01 reviews against the pinned design and raises each departure as a row here; W02–W21 bring each page to the build, one page per row since a row extends one component; W22–W27 write one workflow per feature; W28 runs the default matrix live; W29 states the result on the eval page.
- **Dependency check.** No problems. W21 and W29 both extend the eval page and are split by rule, since W29 needs W22, which needs W21. E02 W03 and E05 W03 contend on `invocation.md`, and E02 W04 and E05 W13 on `docs/hierarchy.md`; E05 depends on E02, so the priority map separates them. Longest chain: fourteen steps, E04:W00 through E04:W10, then E05 W01, a page row, a scenario row, W28 and W29.
- **Proposed epic priority.** E02 3, E04 2, E05 1, derived from E05's edges to E02 and E04.

## Links

| Resource | Link |
| --- | --- |
| Initiative | [I09 Grouping and Composition](https://github.com/m2ux/prosiform/issues/463) |
| Epic | [I09:E02 Section Placement](https://github.com/m2ux/prosiform/issues/458) |
| Epic | [I09:E04 Section Composition](https://github.com/m2ux/prosiform/issues/460) |
| Epic | [I09:E05 MVP Proof](https://github.com/m2ux/prosiform/issues/523) |
| Overlap | [I08 Argument Surface](https://github.com/m2ux/prosiform/issues/462) |
| Earlier record | [Inclusion Profiles and Folders](../2026-10-31-i05-inclusion-profiles-and-folders/README.md) |
| Earlier record | [Section Composition](../2026-10-22-214-section-composition/README.md) |
