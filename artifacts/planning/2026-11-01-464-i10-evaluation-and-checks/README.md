# I10 Evaluation and Checks — November 2026

> Initiative planning · Created 2026-11-01

## Executive Summary

I10 makes the repository's own measurements able to fail. The diagram-following eval's baseline is saturated at 5 of 5 in every cell, so it cannot tell its forms apart; the checks workflow runs by branch name, so a build change on an unmatched branch merges unchecked and an unchecked merge reads like a checked one; the link check reads other branches at whatever they hold when it runs; and an eval session can inherit a hook from its own tree or an ancestor before any read catches it.

The initiative was split out of I05 with three epics raised as standalone issues and no work items. This record gives every task a work item and a declared component, checks the dependency graph, accounts for every independent pair, and traces each initiative criterion to the goal and to the epic criteria that make it true.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [E00 W01 work item](e00/w01.md) | Scenarios reaching every failure class the scorer defines |
| [E00 W02 work item](e00/w02.md) | The every-form baseline over the hardened corpus |
| [E01 W01 work item](e01/w01.md) | The checks trigger reading the changed paths |
| [E01 W02 work item](e01/w02.md) | The link check naming the commit each branch resolved to |
| [E01 W03 work item](e01/w03.md) | A pull request whose checks do not run stating so |
| [E01 W04 work item](e01/w04.md) | The checks page stating the trigger rule |
| [E02 W01 work item](e02/w01.md) | The preflight refusing every project-scope settings file declaring a hook |
| [E02 W02 work item](e02/w02.md) | The preflight refusing a managed settings file declaring a hook |
| [E02 W03 work item](e02/w03.md) | The eval README stating each refused settings file, its scope and the remedy |
| [Joins](joins.md) | Each independent pair of tasks and why it ships as two pull requests |

## Goal

The goal is the initiative's Overview: a measurement that can fail. Its clauses:

- **G1.** The eval's baseline tells the forms it runs apart.
- **G2.** A check runs where a change can break the build, states whether it ran, and states the revision it read.
- **G3.** An eval session reads only what the run gave it.

## Goal Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| G1 | AC1, AC2, AC9 | E00 | E00 AC1–AC4 | No marked source |
| G2 | AC3, AC4, AC5, AC7 | E01 | E01 AC1–AC4 | No marked source |
| G3 | AC6, AC8 | E02 | E02 AC1–AC6 | No marked source |

| Initiative criterion | Epic criteria that make it true |
| --- | --- |
| AC1 | E00 AC3 |
| AC2 | E00 AC2, AC4 |
| AC3 | E01 AC1 |
| AC4 | E01 AC1, AC3 |
| AC5 | E01 AC2 |
| AC6 | E02 AC1, AC2, AC3, AC4 |
| AC7 | E01 AC4 |
| AC8 | E02 AC5, AC6 |
| AC9 | E00 AC1 |

Every initiative criterion traces to a clause, every clause has a criterion, every initiative criterion is made true by the criteria of the one epic citing it, and every epic criterion is covered by exactly one task row. E00 AC2 makes AC2 true by holding the forms of a scenario to one workflow, and E02 AC2 keeps AC6 from being met by a preflight refusing every run. The initiative marks no requirement source, so the criteria answer to the Overview, Problem and Proposal alone.

## Design

- **The baseline follows the eval's corrections.**
  I07:E00 corrects the harness's question and spend counts (W08), the scorer's set and refused-run outcomes (W09), the linked form's entry (W10) and the sub-agent trace name (W16). A baseline taken before them records defective scoring, so E00 W02 depends on W08, W09 and W16, and E00 W01 depends on W10, which W02 reaches through it.
- **The design reads are already pinned.**
  The README's Design link names commit `4c72d818`, and the vocabulary, conformance and independence checks read the design at that commit, the vocabulary check printing it. The one check reading a moving branch is the link check, which resolves `blob/engineering/…` and `tree/engineering/…` URLs at the branch's current head. The concern of the closed contract-reading issue (#204) is therefore one row of E01, scoped to the link check.
- **The skip is a reported result.**
  E01 W03 reports a skipped run under the checks' own name, reading the one path set W01 states, so a run and its report cannot disagree.
- **The ancestor read is a refusal with a remedy.**
  E02 W01 reads every directory from the workspaces' root to the filesystem root and refuses only a `.claude` settings file declaring a hook, naming `--eval-root` as the way out. Whether Claude Code reads an ancestor's settings by project scope is confirmed in that task's analysis against a session's own report of the settings it loaded.
- **The managed settings are read after the project scopes.**
  E02 W02 reads the host's managed settings file in the preflight W01 widens, at a path the harness holds so a test can plant it. It extends W01's preflight in the same file, so it follows W01 rather than contending with it, and E02 W03 documents both.

## Measurement of the Name-Based Trigger

Over the eleven most recent merged pull requests at the time E01 was raised, the `i[0-9][0-9]/**` pattern excluded three that changed 29, 9 and 27 files under `src/`, `fixtures/` or `checks/`, and admitted four that changed no build file. This is the evidence for E01, and it lives here rather than on the checks page, which states the rule as it is.

## Dependency Check

`deps.py` over the initiative, the three epics, the nine work items and [joins.md](joins.md):

- **Problems.** None. No unaccounted join.
- **Longest chain.** Two chains of three steps: E01:W01 → E01:W03 → E01:W04, and E02:W01 → E02:W02 → E02:W03.
- **Contention within the initiative.** None by declared component.
- **Proposed epic priority.** E00 1, E01 1, E02 1: no epic depends on another and no rows contend, so the three start together.
- **Numbering.** E01's link-check row is W02 so the rows follow start order, and E02's managed-settings row is W02 ahead of the README row it feeds; each epic's criteria follow its rows.

## Contention Outside the Initiative

| I10 row | Component | Other row | Its component | Kind |
| --- | --- | --- | --- | --- |
| E00:W01 | evals/diagram-following/workflows | I08:E08:W02 | evals/diagram-following/workflows | Declared match |
| E00:W01 | evals/diagram-following/workflows | I07:E00:W10 | fixtures, editing `workflows/*/linked` | Edge taken |
| E00:W02 | evals/diagram-following/baseline.json | I07:E00:W11 | evals/diagram-following/baseline.json | Duplicate work; W11 leaves I07 |
| E02:W01 | evals/diagram-following/harness.py | I07:E00:W08 | evals/diagram-following/harness | Same file, spelled differently |
| E02:W02 | evals/diagram-following/harness.py | I07:E00:W08 | evals/diagram-following/harness | Same file, spelled differently |

E00 W02 and E02 W03 both edit `evals/diagram-following/README.md`, in different sections, from epics that start together.

## Decisions

Each decision below is the user's (2026-11-01) unless marked as planning's.

- **One baseline.** I07:E00 W11 committed the same file as E00 W02 from a run over the present corpus. W11 leaves I07; E00 W02 produces the one baseline and its AC3 carries W11's criterion.
- **The baseline's edges on I07.** E00 W01 depends on I07:E00 W10, and E00 W02 on I07:E00 W08, W09 and W16.
- **What separation means.** A cell below 1.0 is met by a corpus failing every form alike, so E00 AC4 requires two forms of one scenario to carry different pass rates.
- **The ancestor refusal.** A run under an ancestor `.claude` whose settings declare a hook is refused, naming `--eval-root` as the remedy; the default root stays. E02 AC3 states it.
- **Initiative criteria.** The fixture criterion (no corpus behaviour is added here), the per-revision `make check` criterion (each task's tests carry it) and the closure criterion (it traces to no clause) are dropped.
- **E00's login question.** The limit it waited on reset on 2026-10-31, so the question is removed.
- **E02's rows.** The workspace and ancestor reads extend one component and together cover three criteria, so they are one row.
- **E01's title.** Check Coverage: A Check States What It Read and Whether It Ran, since the epic holds the revision row.
- **No pinned-design-link guard.** The design reads stay pinned by the README's link alone.
- **E00's dispatch edge.** The edge on I05:E07 W02 is dropped: that epic is closed and the row delivered. (Planning.)
- **Epic priority.** E00 1, E01 1, E02 1; E00's label moves from 6.
- **Failure-class coverage.** The Problem's link-following failure and the Proposal's failures the scorer names are a goal clause, so initiative AC9 states that every failure class the scorer defines is produced by a scenario, and E00 covers it through its AC1.
- **E00's measured cost.** No initiative criterion or goal clause asks for it, so the criterion and its Problem bullet are dropped; the README's measured cost stays in E00 W02's work item.
- **E00's revision check.** The criterion that the checks pass on the delivering revision is dropped: each task's tests carry it.
- **E00's edges criterion.** The expected path and the forms' edges are one condition: the path walks the diagram over the edges each form states.
- **E01's trigger evidence.** The pull-request criterion names `src/`, `fixtures/` and `checks/`, one run each, so the build, the corpus and the checks are each shown to run the checks.
- **E01's push to `main`.** The criterion is dropped, since no initiative criterion asks for it; W01's test still reads the run for a merge commit on `main`.
- **E01's checks page.** The page criterion states which changes run the checks, as AC7 does; what a skip reports stays in W04's work item.
- **AC7 and AC8 in the Proposal.** The Proposal states the checks page and the eval's README, so each criterion traces to a clause.
- **AC8's remedy.** `--eval-root` is the remedy for a refused file above the workspaces only, and E02 states it in its own criterion on the README row.
- **E02's ancestor files.** The ancestor criterion names `settings.json` and `settings.local.json`.
- **Managed settings.** The host's managed settings file is a settings file a session reads, so E02 refuses one declaring a hook, on its own row after W01.
- **AC1 and AC2.** They stand as written, although E00 AC3 and AC4 differ from them only by naming the dispatch forms and one model.

## Links

| Resource | Link |
| --- | --- |
| Initiative | [I10 Evaluation and Checks](https://github.com/m2ux/prosiform/issues/464) |
| Epic | [I10:E00 Corpus Separability](https://github.com/m2ux/prosiform/issues/403) |
| Epic | [I10:E01 Check Coverage](https://github.com/m2ux/prosiform/issues/454) |
| Epic | [I10:E02 Session Isolation](https://github.com/m2ux/prosiform/issues/456) |
| Folded issue | [Contract Reading](https://github.com/m2ux/prosiform/issues/204) — closed as a duplicate of E01's revision row |
| Overlap | [I07:E00 Review Remediation](https://github.com/m2ux/prosiform/issues/443) |
| Overlap | [I08:E08 Declared Tree](https://github.com/m2ux/prosiform/issues/465) |
| Earlier record | [I05:E08 Corpus Separability](../2026-10-29-i05-e08-corpus-separability/README.md) |
