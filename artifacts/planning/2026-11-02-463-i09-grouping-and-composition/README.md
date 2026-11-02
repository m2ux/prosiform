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
| [Joins](joins.md) | The candidate unit that ships as separate pull requests, and why |
| [Change list](change-list.md) | The plan changes this run applied and held |

## Goal

The goal is the initiative's Overview: every document arrives under a heading a reader can find. Its clauses:

- **G1.** A reference reaches the document it named.
- **G2.** A file's `group` pair places its own sections, composed from the leaves up.
- **G3.** A referenced section sits where it is named.

## Goal Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| G2 | AC1 | E02 | E02 AC1–AC7 | No marked source |
| G3 | AC2 | E04 | E04 AC1–AC19 | No marked source |

Each initiative criterion states one clause's outcome and is made true by the one epic citing it: E02 AC1–AC4 compose each file under its own pairs before its parent merges it, and E04 AC3 with AC4 places a composed section beneath its containing heading.

### Gaps, Ranked

None remain. Every clause has a criterion, every criterion is delivered by one epic and traces to one clause, and every epic criterion is covered by a task row. The initiative marks no requirement source.

### Outside Threats

- **Every design-clause row moves the README pin on `main`.** The three W00 rows declare the design file and contend; the priority map separates them.
- **Composition and leaves-up assembly meet in `cli.py`.** E02 W01–W02 and E04 W07–W09 contend; the priority map separates the epics.
- **E04 W09 waits on undelivered I08 work.** It depends on I08:E06 W06, the writer's `subst` reaching only its own document's links.
- **The example tree is stale.** No row changes it by intent; E02 W01–W02 re-record any usage-example bundle the leaves-up order changes so the unit passes `make check` alone.

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

- **E01 restated to enforcement.** (Planning, from the brief.) The delivered reference rule leaves the epic with its criteria; the invariant check and its page stay.
- **Preset `include` and `exclude` removed.** (User, 2026-11-02.) E04 drops AC20 and its Proposal clause; W09 covers presets and `subst`.
- **Vocabulary.** (User.) "`group` pairs" replaces "group rules" in the initiative and E02, E02's title included.
- **Epic priority.** (User, 2026-11-02.) E01 `priority: 3`, E02 `priority: 2`, E04 `priority: 1`, as the dependency check proposes.
- **E02's example row dropped as delivered.** (User, 2026-11-02.) I08:E01 W02 (commit `ea80ce79`) moved every pair onto its leaf. At the I08:E01 base [bb404015](https://github.com/m2ux/prosiform/tree/bb404015/example/work-planner), all 44 documents under `artifacts`, `protocols` and `references` declare one pair naming their own directory's group at depth 1, and none of the 15 others (`SKILL.md`, `configuration.md`, `conventions.md`, `guidelines.md`, `rules.md` and the ten modes) declares any pair. E02 drops the row and its two criteria; the hierarchy row becomes W04 and the criteria renumber to AC1–AC7.
- **Initiative criteria are the clauses' outcomes.** (User, 2026-11-02.) One criterion per goal clause replaces the fixture, page, per-revision check and closure criteria; each epic row covers its clause's criterion.
- **Non-Goals.** (User, 2026-11-02.) The four drafted Non-Goals stand.
- **Grouping Targets moves to I10.** (User, 2026-11-02.) The epic holds an existing rule by validation and changes where nothing arrives, so it serves I10's measurement that can fail. It is I10:E03 (#455) with `priority: 1`; G1 and its criterion leave this initiative, the remaining criteria renumber to AC1–AC2, and its work items stay in `e01/` here, which #455 links. The sections above that name E01 record how it was planned.
- **I09 precedes I10.** (User, 2026-11-02.) I09 `priority: 2` and I10 `priority: 1`, so the MVP's I08 and I09 are delivered before the evaluation work.
- **Earlier decisions stand.** (User, 2026-11-02.) E00 and E03 are closed; an earlier E02 row was dropped as delivered by I08; a composed target declaring no `prosiform` is refused.

## Links

| Resource | Link |
| --- | --- |
| Initiative | [I09 Grouping and Composition](https://github.com/m2ux/prosiform/issues/463) |
| Epic | [I09:E02 Section Placement](https://github.com/m2ux/prosiform/issues/458) |
| Epic | [I09:E04 Section Composition](https://github.com/m2ux/prosiform/issues/460) |
| Overlap | [I08 Argument Surface](https://github.com/m2ux/prosiform/issues/462) |
| Earlier record | [Inclusion Profiles and Folders](../2026-10-31-i05-inclusion-profiles-and-folders/README.md) |
| Earlier record | [Section Composition](../2026-10-22-214-section-composition/README.md) |
