# I05:E06 Example Authoring — October 2026

> Epic planning · Created 2026-10-28

## Executive Summary

This record holds the placement and plan of [#376](https://github.com/m2ux/prosiform/issues/376): the work-planner example under `example/work-planner/` brought to one set of authoring rules — bindings stated once, Inputs and Outputs as contract links, commands inline in their steps, one home per rule, one subject per file — with the `N. Action` step sub-sections kept. The issue is kept and becomes I05's epic E06; its original body is preserved as a comment on it.

The change is to the corpus, its guidelines and one repository check; `pf` is unchanged. A check first reports the findings by area, one sample file shows every rule for approval, and the rollout follows by area, ending with the check held under `make check`. The epic starts from the step sub-section conversion of the same corpus, I05:E04, which [#372](https://github.com/m2ux/prosiform/pull/372) merged into `main`.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W01 work item](w01.md) | The authoring rules in the corpus guidelines |
| [W02 work item](w02.md) | The authoring check and its findings report by area |
| [W03 work item](w03.md) | The configuration document for the example's bindings |
| [W04 work item](w04.md) | The shared conventions stated once |
| [W05 work item](w05.md) | The sample artifact under the rules |
| [W06 work item](w06.md) | Artifact Inputs and Outputs as contract links |
| [W07 work item](w07.md) | Artifact commands inline in their steps |
| [W08 work item](w08.md) | Modes, protocols and entry files under the rules |
| [W09 work item](w09.md) | One home per rule and one subject per file |
| [W10 work item](w10.md) | The authoring guard under `make check` |
| [W11 work item](w11.md) | The shared skill guidelines under the authoring rules |
| [Joins](joins.md) | Independent row pairs that take separate pull requests, and why |
| [Change list](change-list.md) | The plan changes this session applied and held |

## Survey

Counted on the I05:E04 base, [`14d059d1`](https://github.com/m2ux/prosiform/tree/14d059d114161c1b5955849eb2a952102b0e9d17/example/work-planner).

- **Inputs.** 221 `**Inputs:**` lines across 32 files: 219 in the 31 artifacts, 2 in `modes/revise-mode.md`; protocols carry none.
- **Commands.** 19 files carry `## Commands`: 18 artifacts and `modes/revise-mode.md`.
- **Size.** Four files exceed 20 KB: `artifacts/pull-request.md` (28 KB), `guidelines.md` (25 KB), `artifacts/epic-issue-body.md` (23 KB), `artifacts/issue.md` (21 KB).
- **Headings.** All 58 Markdown files open with an H1.
- **Links.** No cross-file link in the example is root-relative or a repository URL to the example itself.

## Decisions

- **Placement.** A new epic of I05, as the user asked; #376 is kept and rewritten as the epic, since it carries the design and its evidence.
- **Number.** E06, after the Deferred Debt epic E05; the held decision on Deferred Debt staying I05's last epic, recorded with #373's placement, covers this number too.
- **Corpus only.** The rules bind the example; `pf` gains no rule. The check is a repository check.
- **Fixtures move with each task.** Each row regenerates the usage-example bundles its files reach; the epic's last criterion states the end state on the base.
- **Initiative coverage.** The row covers I05's AC3 alone, as E04's does: no `pf` behaviour or bundling rule changes.
- **Epic split.** The ten rows as published: rules, check, configuration, conventions, sample, artifact contracts, artifact commands, the other files, homes and splits, guard. (User, 2026-10-28.)
- **Epic priority.** `priority: 8`, the number E01, E03, E04 and E05 carry: E04 has merged, so the contention that would place E06 below it is gone. (User, 2026-10-28.)
- **Title headings kept.** Each file keeps its H1, and the guidelines state that a file's H1 is its heading in the bundle, the name pf gives the file's section when it groups bundled content. W01 states the rule. (User, 2026-10-28.)
- **Configuration home.** The bindings live in a new `example/work-planner/configuration.md`, beside `conventions.md` and linked from `SKILL.md`: bindings are values and conventions are rules, so each file keeps one subject. W03 creates it, and AC3 names it. (User, 2026-10-28.)

## Component Map

| Row | Component | Further paths written |
| --- | --- | --- |
| W01 | `example/work-planner/guidelines.md` | `fixtures/usage-example/*/expected/` |
| W02 | `checks/authoring.py` | `checks/tests`, `checks/README.md` |
| W03 | `example/work-planner/configuration.md` | `example/work-planner/SKILL.md`, the files restating a binding, `fixtures/usage-example/*/expected/` |
| W04 | `example/work-planner/conventions.md` | The operations restating a convention, `fixtures/usage-example/*/expected/` |
| W05 | `example/work-planner/artifacts/placement.md` | `example/work-planner/guidelines.md`, `fixtures/usage-example/*/expected/` |
| W06 | `example/work-planner/artifacts` | `fixtures/usage-example/*/expected/` |
| W07 | `example/work-planner/artifacts` | `fixtures/usage-example/*/expected/` |
| W08 | `example/work-planner` | `fixtures/usage-example/*/expected/` |
| W09 | `example/work-planner` | `fixtures/usage-example/*/expected/` |
| W10 | `Makefile` | `checks.md`, `checks/tests` |
| W11 | `example/guidelines.md` | `fixtures/usage-example/*/expected/` |

## Collision Surface

- **I05:E04 Corpus Steps.**
  Its base merged into `main` through #372, so its rewrite of `example/work-planner/` and the usage-example bundles is the tree this epic starts from, and E06 W01's dependency on E04 W05 is met on `main`. `deps.py` still lists E04 W01 against E06 W01 on `guidelines.md`, and E04 W04 against E06 W06 and E06 W07 on `artifacts`, since it reads row components rather than merges; with every E04 row delivered and its base merged, no pair can conflict.
- **I05:E04 W06 and repository checks.**
  E04's guard wrote `Makefile`, `checks.md` and `checks/README.md`, which W02 and W10 write too; any other open work on those files, such as I05:E01's unmerged base and I01:E00's draft, rebases against W10.
- **I05:E03 Dispatch Bundles.**
  Its open row W16 writes `evals/diagram-following/workflows`, outside this epic's components.
- **I05:E05 Deferred Debt.**
  Its W01 writes `src/prosiform` and the round-trip test; no overlap.

## Epic Priority

`priority: 8`, shared with E01, E03, E04 and E05, as Decisions records. The contention with E04 that `deps.py` reports is with delivered rows on a merged base.

## Review

Validate Issue Body and Check Dependencies and Numbering over the saved bodies, 2026-10-28, and again after the user's decisions.

- **Format.** `format.py` reports nothing to fix, apply or decide on #376 or #327.
- **Dependencies.** No problem in I05:E06; the one problem `deps.py` prints, E01 W01's edge to I05:E00 W02, is outside this run, since E00 was not supplied. No numbering advisory.
- **Joins.** Every independent pair in E06 is accounted for in [Joins](joins.md).
- **Longest chain.** 16 steps, through E03 W01–W09, E04 W01 and W05, then E06 W01, W05, W09 and W10.
- **Contending pairs.** E04:W01 with E06:W01 on `example/work-planner/guidelines.md`; E04:W04 with E06:W06 and with E06:W07 on `example/work-planner/artifacts`.
- **Second pass.** With the decisions applied and the open questions removed, `format.py` reports nothing to fix, apply or decide on #376, and `deps.py` reports no problem in E06, no unaccounted pair and no numbering advisory.
- **Corpus audit.** The criterion applies to workflow definitions; this corpus is example material, so the epic carries none.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E06 Example Authoring](https://github.com/m2ux/prosiform/issues/376) |
| Prerequisite epic | [I05:E04 Corpus Steps](https://github.com/m2ux/prosiform/issues/352) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
