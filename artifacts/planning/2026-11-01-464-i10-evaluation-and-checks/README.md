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
| [E02 W02 work item](e02/w02.md) | The eval README stating each refused settings file and its scope |
| [Joins](joins.md) | Each independent pair of tasks and why it ships as two pull requests |

## Goal

The goal is the initiative's Overview: a measurement that can fail. Its clauses:

- **G1.** The eval's baseline tells the forms it runs apart.
- **G2.** A check runs where a change can break the build, states whether it ran, and states the revision it read.
- **G3.** An eval session reads only what the run gave it.

## Goal Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| G1 | AC1, AC2 | E00 | E00 AC1–AC6 | No marked source |
| G2 | AC3, AC4, AC5, AC7 | E01 | E01 AC1–AC5 | No marked source |
| G3 | AC6, AC7 | E02 | E02 AC1–AC4 | No marked source |

Every initiative criterion traces to a clause, every clause has a criterion, and every epic criterion is covered by a task row. The initiative marks no requirement source, so the criteria answer to the Overview and Problem alone.

## Design

- **The baseline follows the eval's corrections.**
  I07:E00 corrects the harness's question and spend counts (W08), the scorer's set and refused-run outcomes (W09), the linked form's entry (W10) and the sub-agent trace name (W16). A baseline taken before them records defective scoring, so E00 W02 depends on W08, W09 and W16, and E00 W01 depends on W10, which W02 reaches through it.
- **The design reads are already pinned.**
  The README's Design link names commit `4c72d818`, and the vocabulary, conformance and independence checks read the design at that commit, the vocabulary check printing it. The one check reading a moving branch is the link check, which resolves `blob/engineering/…` and `tree/engineering/…` URLs at the branch's current head. The concern of the closed contract-reading issue (#204) is therefore one row of E01, scoped to the link check.
- **The skip is a reported result.**
  E01 W03 reports a skipped run under the checks' own name, reading the one path set W01 states, so a run and its report cannot disagree.
- **The ancestor read is a refusal with a remedy.**
  E02 W01 reads every directory from the workspaces' root to the filesystem root and refuses only a `.claude` settings file declaring a hook, naming `--eval-root` as the way out. Whether Claude Code reads an ancestor's settings by project scope is confirmed in that task's analysis against a session's own report of the settings it loaded.

## Measurement of the Name-Based Trigger

Over the eleven most recent merged pull requests at the time E01 was raised, the `i[0-9][0-9]/**` pattern excluded three that changed 29, 9 and 27 files under `src/`, `fixtures/` or `checks/`, and admitted four that changed no build file. This is the evidence for E01, and it lives here rather than on the checks page, which states the rule as it is.

## Dependency Check

`deps.py` over the initiative, the three epics, the eight work items and [joins.md](joins.md):

- **Problems.** None. No unaccounted join.
- **Longest chain.** One chain of three steps: E01:W01 → E01:W03 → E01:W04.
- **Contention within the initiative.** None by declared component.
- **Proposed epic priority.** E00 1, E01 1, E02 1: no epic depends on another and no rows contend, so the three start together.
- **Numbering.** E01's link-check row moved from W04 to W02 so the rows follow start order; its criteria were renumbered to follow the rows.

## Contention Outside the Initiative

| I10 row | Component | Other row | Its component | Kind |
| --- | --- | --- | --- | --- |
| E00:W01 | evals/diagram-following/workflows | I08:E08:W02 | evals/diagram-following/workflows | Declared match |
| E00:W01 | evals/diagram-following/workflows | I07:E00:W10 | fixtures, editing `workflows/*/linked` | Edge taken |
| E00:W02 | evals/diagram-following/baseline.json | I07:E00:W11 | evals/diagram-following/baseline.json | Duplicate work; W11 leaves I07 |
| E02:W01 | evals/diagram-following/harness.py | I07:E00:W08 | evals/diagram-following/harness | Same file, spelled differently |

E00 W02 and E02 W02 both edit `evals/diagram-following/README.md`, in different sections, from epics that start together.

## Decisions

Each decision below is the user's (2026-11-01) unless marked as planning's.

- **One baseline.** I07:E00 W11 committed the same file as E00 W02 from a run over the present corpus. W11 leaves I07; E00 W02 produces the one baseline and its AC4 carries W11's criterion.
- **The baseline's edges on I07.** E00 W01 depends on I07:E00 W10, and E00 W02 on I07:E00 W08, W09 and W16.
- **What separation means.** A cell below 1.0 is met by a corpus failing every form alike, so E00 AC5 requires two forms of one scenario to carry different pass rates.
- **The ancestor refusal.** A run under an ancestor `.claude` whose settings declare a hook is refused, naming `--eval-root` as the remedy; the default root stays. E02 AC3 states it.
- **Initiative criteria.** The fixture criterion (no corpus behaviour is added here), the per-revision `make check` criterion (each task's tests carry it) and the closure criterion (it traces to no clause) are dropped.
- **E00's login question.** The limit it waited on reset on 2026-10-31, so the question is removed.
- **E02's rows.** The workspace and ancestor reads extend one component and together cover three criteria, so they are one row.
- **E01's title.** Check Coverage: A Check States What It Read and Whether It Ran, since the epic holds the revision row.
- **No pinned-design-link guard.** The design reads stay pinned by the README's link alone.
- **E00's dispatch edge.** The edge on I05:E07 W02 is dropped: that epic is closed and the row delivered. (Planning.)
- **Epic priority.** E00 1, E01 1, E02 1; E00's label moves from 6.

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
