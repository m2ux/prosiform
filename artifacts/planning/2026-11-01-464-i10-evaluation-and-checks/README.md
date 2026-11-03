# I10 Evaluation and Checks — November 2026

> Initiative planning · Created 2026-11-01

## Executive Summary

I10 makes the repository's own measurements able to fail. The diagram-following eval's baseline is saturated at 5 of 5 in every cell, so it cannot tell its forms apart; the checks workflow runs by branch name, so a build change on an unmatched branch merges unchecked and an unchecked merge reads like a checked one; the link check reads other branches at whatever they hold when it runs; an eval session can inherit a hook from its own tree or an ancestor before any read catches it; and no eval workflow shows how an agent follows a bundle that defers, composes or dispatches past two hops.

The initiative was split out of I05 with three epics raised as standalone issues and no work items. This record gives every task a work item and a declared component, checks the dependency graph, accounts for every independent pair, and traces each initiative criterion to the goal and to the epic criteria that make it true.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [E00 W00 work item](e00/w00.md) | The default matrix running the one model the user chose |
| [E00 W01 work item](e00/w01.md) | Scenarios reaching every failure class the scorer defines |
| [E00 W02 work item](e00/w02.md) | The every-form baseline over the hardened corpus |
| [E00 W04 work item](e00/w04.md) | The baseline runbook's shakedown over the hardened corpus |
| [E01 W01 work item](e01/w01.md) | The checks trigger reading the changed paths |
| [E01 W02 work item](e01/w02.md) | The link check naming the commit each branch resolved to |
| [E01 W03 work item](e01/w03.md) | A pull request whose checks do not run stating so |
| [E01 W04 work item](e01/w04.md) | The checks page stating the trigger rule |
| [E02 W01 work item](e02/w01.md) | The preflight refusing every project-scope settings file declaring a hook |
| [E02 W02 work item](e02/w02.md) | The run record naming the hook a managed settings file declares |
| [E02 W03 work item](e02/w03.md) | The eval README stating each refused settings file, its scope and the remedy |
| [E04 W01 work item](e04/w01.md) | Scenarios stating the `pf` runs a session and its sub-agents make |
| [E04 W02 work item](e04/w02.md) | The `staged` form, given only to a harness with a shell |
| [E04 W03 work item](e04/w03.md) | The scorer holding a session to its stated `pf` runs |
| [E04 W04 work item](e04/w04.md) | Each sub-agent's starts and commands, at every dispatch depth |
| [E04 W05 work item](e04/w05.md) | A skill entry's hand-written `↳` link, bootstrapped and compiled |
| [E04 W06 work item](e04/w06.md) | Conditional and nested deferral, activated only where the path needs it |
| [E04 W07 work item](e04/w07.md) | A deferral under matched presets, followed through its `subst` stand-in |
| [E04 W08 work item](e04/w08.md) | Immediate composition under a conditional step |
| [E04 W09 work item](e04/w09.md) | Arrow-only directives beside a footnote link, and self-composition |
| [E04 W10 work item](e04/w10.md) | A deferred dispatch in the entry bundle, compiled then dispatched |
| [E04 W11 work item](e04/w11.md) | Dispatch three hops deep: a chain, a set, and a question from the deepest level |
| [E04 W12 work item](e04/w12.md) | A sub-agent's first `pf` run at the first, second and third hop |
| [E04 W14 work item](e04/w14.md) | The live run of the edge workflows, committed as one `composition-edges-<harness>.json` per shell harness |
| [E04 W15 work item](e04/w15.md) | The eval's README stating the edge workflows and their run |
| [E04 W16 work item](e04/w16.md) | The edge-run runbook's shakedown over the edge workflows |
| [E04 W17 work item](e04/w17.md) | The triage rubric's entries for the scorer's `pf`-run classes |
| [E05 W00 work item](e05/w00.md) | The triage rubric, a runbook per live run, and the user's model, in `RUNBOOK.md` |
| [E05 W03 work item](e05/w03.md) | A run's managed configuration recorded by count and fingerprint |
| [E05 W01 work item](e05/w01.md) | The live run of the feature workflows, committed as `mvp-proof.json` |
| [E05 W02 work item](e05/w02.md) | The eval page stating the feature workflows and the proof |
| [Initiative draft](initiative-body.md) | The initiative body as saved, the source of its next edit |
| [E04 draft](e04-body.md) | The E04 epic body as saved, the source of its next edit |
| [E05 draft](e05-body.md) | The E05 epic body as saved, the source of its next edit |
| [Joins](joins.md) | Each independent pair, and each same-component pair, that ships as two pull requests |
| [A: agent review of #600](agent-review-600.json) | The agent review record of the I10:E02 integration pull request, by reviewed head and target |
| [A: agent review of #618](agent-review-618.json) | The agent review record of the I10:E01 integration pull request, by reviewed head and target |
| [A: agent review of #616](agent-review-616.json) | The agent review record of the I10:E05 integration pull request, by reviewed head and target |

## Goal

The goal is the initiative's Overview: a measurement that can fail. Its clauses:

- **G1.** The eval's baseline tells the forms it runs apart.
- **G2.** A check runs where a change can break the build, states whether it ran, and states the revision it read.
- **G3.** An eval session reads only what the run gave it.
- **G4.** Validation refuses a bundle whose reference lands on a destination two documents share.
- **G5.** The eval measures how an agent follows a bundle that defers, composes or dispatches.
- **G6.** One live run proves the MVP's features followed.

## Goal Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| G1 | AC1, AC2, AC9, AC11, AC12 | E00 | E00 AC1–AC7 | No marked source |
| G2 | AC3, AC4, AC5, AC7 | E01 | E01 AC1–AC4 | No marked source |
| G3 | AC6, AC8 | E02 | E02 AC1–AC6 | No marked source |
| G4 | AC10 | E03 | E03 AC1–AC3 | No marked source |
| G5 | AC13 | E04 | E04 AC1–AC22 | No marked source |
| G6 | AC14 | E05 | E05 AC1–AC5 | No marked source |

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
| AC10 | E03 AC2 |
| AC11 | E00 AC6 |
| AC12 | E00 AC7 |
| AC13 | E04 AC20, resting on AC1–AC19 and AC22 |

Every initiative criterion traces to a clause, every clause has a criterion, every initiative criterion is made true by the criteria of the one epic citing it, and every epic criterion is covered by exactly one task row. E00 AC2 makes AC2 true by holding the forms of a scenario to one workflow, and E02 AC2 keeps AC6 from being met by a preflight refusing every run. E04 AC20 makes AC13 true only through the scenarios AC6–AC19 state and the form, scoring and harness AC1–AC5 and AC22 build; AC21 states the result on the eval page. The initiative marks no requirement source, so the criteria answer to the Overview, Problem and Proposal alone.

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

## Composition Following

The agent-behaviour evals of composition, deferral and dispatch are their own epic, E04 ([#579](https://github.com/m2ux/prosiform/issues/579)), rather than rows of E00.

- **Placement.** E00 is the default matrix's separability and its one baseline. The edge evals run only on harnesses with a shell, outside the default matrix, wait on I09:E04 W11 and W12, and end in a live run of their own; as E00 rows they would gate E00's baseline on I09 and on a second paid run. A new epic keeps E00's closure as planned and gives the work its own goal clause, G5.
- **A shell form outside the default matrix.** Every edge needs `pf` at run time or a bundle set only `pf` builds, so the edges are written in one `staged` form: the compiled bundle set with the build under test on the session's path. It is outside the default `--forms`, and the Claude harness carries no shell, so the default matrix, `baseline.json` and the Non-Goal against adding a form to it are unchanged. The bootstrap edge uses the existing `bootstrap` form.
- **A scenario states the `pf` runs.** A pass is the agent's path matching the one its bundle states. Where an edge is whether `pf` runs (condition false, nested deferral not needed, a sub-agent's first run), the path alone cannot fail, so a scenario also states each `pf` run and the scorer fails a session whose runs differ.
- **Refusals are not agent evals.** A gap between symbols, `[⇉→]`, a preset mismatch on deferral and an immediate-plus-deferred pair are build refusals I09:E04's corpus fixtures hold.
- **The MVP proof boundary.** I09:E05 W26 writes one section-composition workflow activating an unconditional deferral; E04 measures the conditional, nested, preset-matched and dispatched edges, in workflows of their own, so no component is shared.
- **Its own record.** Each shell harness's live run is committed as `composition-edges-<harness>.json` with its report (user, 2026-11-03, as one `run.py` run takes one harness); `baseline.json` (E00 W02) and `mvp-proof.json` (I09:E05 W28) are untouched. Failing sessions are recorded by class; no pass bar gates the run.
- **Units by area.** The form, scenario field, scorer and harness rows are one unit (W01–W04); the deferral scenarios another (W05–W07); immediate composition and directive labels a third (W08–W09); deferred and nested dispatch and the sub-agent's first run a fourth (W10–W12). W14 and W15 follow the scenarios.

## Measurement of the Name-Based Trigger

Over the eleven most recent merged pull requests at the time E01 was raised, the `i[0-9][0-9]/**` pattern excluded three that changed 29, 9 and 27 files under `src/`, `fixtures/` or `checks/`, and admitted four that changed no build file. This is the evidence for E01, and it lives here rather than on the checks page, which states the rule as it is.

## Delivery Lanes

Two sessions deliver I10 at once (user, 2026-11-03), one per lane. Each work item states its lane as `**Lane:** <n>`, and a session takes the highest-priority row whose dependencies are met in its own lane, so neither waits while the other has work it can feed.

| Lane | Rows, in the order they come free |
| --- | --- |
| 1 | E05 W00 · E00 W01 · E00 W04 · E04 W01, W02, W03, W04 · E04 W05–W12 · E04 W16 |
| 2 | E02 W01–W03 · E01 W01–W04 · E03 W00–W02 (filler, taken while no run is free) · E05 W01, W02 · E00 W00 · E00 W02, W03 · E04 W14, W15 |

- **Lane 1 never waits on lane 2.** E00 W01 depends on E05 W00 for the model, not on E00 W00's code change.
- **Each run is fed by one lane 1 row.** The proof by E05 W00 (and the user's merge of I09:E05), the baseline by E00 W04, the edge run by E04 W16.
- **Filler covers lane 2's waits.** At the start, while E05 W00 runs, and in the long stretch while lane 1 designs E04. E02 goes first so its `harness.py` rows land before E04 W04, which depends on E02 W02.

## Dependency Check

`deps.py` over the initiative, the five epics, every work item (E03's from the [I09 record](../2026-11-02-463-i09-grouping-and-composition/e01/)) and [joins.md](joins.md), on 2026-11-02:

- **Problems.** None. No unaccounted join; E01 W01 and W03, and E02 W01 and W02, extend one component each and stay split with the reason [joins.md](joins.md) records.
- **Longest chain.** Three chains of four steps, each ending E04:W12 → E04:W14 → E04:W15, from E04 W01, W02 or W04.
- **Contention within the initiative.** E04 W04 with E02 W01 and W02 on `evals/diagram-following/harness.py`, and E04 W15 with E02 W03 on `evals/diagram-following/README.md`.
- **Proposed epic priority.** E00 2, E01 2, E02 2, E03 2, E04 1: the contention puts E04 after E02, and no epic depends on another.
- **Not checked.** E00 W03 has no work item, so its component is unread.
- **Numbering.** Rows follow start order; E04's criteria follow its rows, with AC22 split from AC3 at the end.

## Contention Outside the Initiative

| I10 row | Component | Other row | Its component | Kind |
| --- | --- | --- | --- | --- |
| E00:W01 | evals/diagram-following/workflows | I08:E08:W02 | evals/diagram-following/workflows | Declared match |
| E00:W01 | evals/diagram-following/workflows | I07:E00:W10 | fixtures, editing `workflows/*/linked` | Edge taken |
| E00:W02 | evals/diagram-following/baseline.json | I07:E00:W11 | evals/diagram-following/baseline.json | Duplicate work; W11 leaves I07 |
| E02:W01 | evals/diagram-following/harness.py | I07:E00:W08 | evals/diagram-following/harness | Same file, spelled differently |
| E02:W02 | evals/diagram-following/harness.py | I07:E00:W08 | evals/diagram-following/harness | Same file, spelled differently |

| E04:W15 | evals/diagram-following/README.md | I09:E05:W21, I09:E05:W29 | evals/diagram-following/README.md | I09 delivers first by initiative priority |

E00 W02 and E02 W03 both edit `evals/diagram-following/README.md`, in different sections, from epics that start together.

## Decisions

Each decision below is the user's (2026-11-01) unless marked as planning's.

- **E04 runs after E00–E03.** (User, 2026-11-02.) E00–E03 take `priority: 2` and E04 [#579](https://github.com/m2ux/prosiform/issues/579) `priority: 1`, as the dependency check proposes, so E04 follows E02 on `harness.py` and the eval README.
- **No first-run carrier comparison.** (User, 2026-11-02.) E04 W13 is dropped: the Prosiform section carries the `pf` command, and no frontmatter or blockquote carrier is measured against it.

- **The baseline runs after the eval tree declares presets, and proves the harness fixes.** E00 W02 depends on I08:E08 W02, each new scenario's documents declare `prosiform`, and the one default-matrix run is the evidence for AC11 and AC12, the harness criteria taken from I07, which E00 W03 verifies. (2026-11-02.)
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
- **Grouping Targets joins as E03.** (2026-11-02.) I09:E01 (#455) holds an existing reference rule by validation, a check that can fail, so it moves here as E03 with `priority: 1`, adding goal clause G4 and AC10. Its work items stay in the [I09 record](../2026-11-02-463-i09-grouping-and-composition/e01/), and I10 now follows I09 (`priority: 1` against I09's `2`).
- **AC1 and AC2.** They stand as written, although E00 AC3 and AC4 differ from them only by naming the dispatch forms and one model.
- **MVP order.** (User, 2026-11-02.) Initiative priority labels are I08 `priority: 4`, I09 `priority: 3`, I11 MVP Release ([#524](https://github.com/m2ux/prosiform/issues/524)) `priority: 2` and I10 `priority: 1`, so I10 follows the MVP and its release; I07 keeps its label. This supersedes I09's `2` above. `baseline.json` stays E00 W02's: I09:E05's proof run writes `mvp-proof.json` beside it.
- **I10 precedes I11.** (User, 2026-11-02.) I10 takes `priority: 2` and I11 MVP Release ([#524](https://github.com/m2ux/prosiform/issues/524)) `priority: 1`, so the measurement work is delivered before the release is cut.
- **Nested dispatch to depth three.** (User, 2026-11-02.) The evals confirm nested dispatch to at least three hops, within the depth the run publishes without `W_DISPATCH_DEPTH`: a chain entry `⇉` A `⇉` B `⇉` C, the same depth with a `⫽` set at one level returning before the chain continues, inner levels carrying a deferred dispatch or a `↳` line whose sub-agent runs `pf` first, and a question from the deepest level relayed up to the user. E04 W11 (AC14–AC16) and W12 (AC18).
- **Composition-following evals.** (User, 2026-11-02.) Agent-behaviour evals cover a skill's hand-written `↳` link, conditional and nested deferral, preset-matched deferral, a sub-agent's first `pf` run, conditional immediate composition, arrow-only directives, self-composition and a deferred dispatch in the entry bundle. Build refusals are left to I09:E04's fixtures.
- **E04 placement.** (Planning.) A new epic rather than E00 rows, as [Composition Following](#composition-following) states.
- **No pass bar on the edge run.** (Planning.) The run measures; failing sessions are recorded by class, and a refused run is not committed.
- **E04 priority; sibling move held.** (Planning.) E04 carries `priority: 1`, the number the map proposes for it. Moving E00–E03 from `1` to `2`, which separates E04 from E02 on `harness.py` and the eval README, is a re-prioritisation held for the user.
- **The MVP proof joins as E05.** (User, 2026-11-03.) I09:E05's last two rows are evals, so W28 and W29 move here as E05 [#594](https://github.com/m2ux/prosiform/issues/594) W01 and W02, with AC29–AC33 as its AC1–AC5 and I09 AC3 as AC14 under goal clause G6. E05 depends on I09:E05, whose feature workflows it runs, and carries `priority: 3`, so it runs first in I10, ahead of E00–E03 (`2`) and E04 (`1`) (user, 2026-11-03). Its earlier decisions (the pass bar, its own file, `baseline.json` untouched) stay in the [I09 record](../2026-11-02-463-i09-grouping-and-composition/README.md#decisions).
- **Harness and model are asked.** (User, 2026-11-03.) The proof run's session asks the user which harness and, open-ended, which model it uses; E05 AC1 names neither. This supersedes I09's Haiku and full-matrix decisions.
- **Runs follow a runbook.** (User, 2026-11-03.) One row up front, E05 W00, writes `RUNBOOK.md`: a triage rubric giving each scorer class the evidence for agent miss, defect or unclear, and a runbook per live run (E05 W01, E00 W02, E04 W14) proven by a shakedown. Each run row follows its runbook, records the rubric's disposition for every failing session, and escalates a defect or an unclear session; it edits no scenario, harness or scorer. E04 W03 adds its classes to the rubric. Initiative AC15.
- **One model, the user's.** (User, 2026-11-03.) The default matrix runs one model and the corpus is calibrated against it (E00 W00, W01). The plan names no model: E05 W00 asks the user, open-ended. The non-goal on the default matrix now covers harnesses and forms only.
- **Two lanes, minimal slack.** (User, 2026-11-03.) Two sessions run side by side, one per lane, as [Delivery Lanes](#delivery-lanes) states. E05 W00 shakes down only the proof's runbook; E00 W04 and E04 W16 shake down the baseline's and the edge run's once their scenarios exist. Priorities: E05 `4`, E00 `3`, E04 and E02 `2`, E01 and E03 `1`. This supersedes E05 `3` and E00–E03 `2` with E04 `1` above.
- **The default model is asked where it is first needed.** (User, 2026-11-03.) E05 W00's shakedown runs on the model and harness the user names for it; the default matrix's model is asked at E00 W01, which calibrates against it, and E00 W04 records it, so E00 W00 depends on W04.
- **A managed plugin is recorded, not refused.** (User, 2026-11-03.) The eval login carries an org-managed plugin whose SessionStart hook adds a short rules preamble to every session. The claude harness preflight accepts a plugin installed or enabled at managed scope and the run record names it, so each committed run states what its sessions carried; every other isolation refusal stands. Delivered in E05 W00 (#596). E02 W02 AC4 follows: a managed hook is recorded rather than refused.
- **Managed configuration stays generic.** (User, 2026-11-03.) No platform's managed configuration is written into the repository: a run counts the managed plugins, settings and hooks its sessions carried and records a fingerprint of them, naming none (E05 W03, AC9); documents and tests describe managed scope generically. The proof run's record is regenerated in that form before it merges.
- **A sub-agent's pf run is tested by its effect.** (User, 2026-11-03.) No harness reports a command a sub-agent runs, so W12's scenarios state actions only the content a sub-agent's `pf` run compiles defines; a sub-agent that runs no `pf` fails on its path. AC17 and AC18 say so; #623 closed as not planned.
- **`unbootstrapped` retires.** (User, 2026-11-03.) `uncompiled` covers a bootstrap session that ran no `pf` once its scenarios state their runs, so E04 W05 removes `unbootstrapped` with its rubric row.
- **A bootstrap skill names `pf` in its opening paragraph.** (User, 2026-11-03.) "Run `pf`." stands in the skill's opening paragraph, apart from its `↳` line, so a session holds the command before it meets the symbol; folded into E04 W08.
- **Managed hooks are counted from the transcripts.** (User, 2026-11-03.) A run counts the managed hooks its sessions carried from the hook events their transcripts show, so a hook declared where no config read reaches is still counted; E05 integration applies it.
- **Components name their branch.** (Planning.) Every I10 work item declares `main:<path>`, so `deps.py` compares E04's rows with its siblings'.

## Links

| Resource | Link |
| --- | --- |
| Initiative | [I10 Evaluation and Checks](https://github.com/m2ux/prosiform/issues/464) |
| Epic | [I10:E00 Corpus Separability](https://github.com/m2ux/prosiform/issues/403) |
| Epic | [I10:E01 Check Coverage](https://github.com/m2ux/prosiform/issues/454) |
| Epic | [I10:E02 Session Isolation](https://github.com/m2ux/prosiform/issues/456) |
| Epic | [I10:E03 Grouping Targets](https://github.com/m2ux/prosiform/issues/455) |
| Epic | [I10:E04 Composition Following](https://github.com/m2ux/prosiform/issues/579) |
| Prerequisite | [I09:E04 Section Composition](https://github.com/m2ux/prosiform/issues/460) — W11 and W12 |
| Overlap | [I09:E05 MVP Proof](https://github.com/m2ux/prosiform/issues/523) |
| Folded issue | [Contract Reading](https://github.com/m2ux/prosiform/issues/204) — closed as a duplicate of E01's revision row |
| Overlap | [I07:E00 Review Remediation](https://github.com/m2ux/prosiform/issues/443) |
| Overlap | [I08:E08 Declared Tree](https://github.com/m2ux/prosiform/issues/465) |
| Earlier record | [I05:E08 Corpus Separability](../2026-10-29-i05-e08-corpus-separability/README.md) |
