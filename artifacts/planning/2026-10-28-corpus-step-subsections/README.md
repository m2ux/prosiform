# I05 Corpus Steps as Sub-sections — October 2026

> Epic planning · Created 2026-10-28

## Executive Summary

This record holds the plan for I05:E04: the work-planner example corpus writes each numbered procedure step as a heading-rooted sub-section, so a link can name a single step precisely. The change is to the corpus and its guidelines; `pf` is unchanged and bundles the converted corpus as it bundles any sections.

The corpus holds 564 numbered steps across 142 procedures in 53 files. The epic states the convention, converts modes, protocols and artifacts one directory per task, links every prose reference to a step, and guards the convention under `make check`. It follows I05:E03 Dispatch Bundles, which retires the warning keyed on numbered steps and writes Board Reads in this form first.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Survey](survey.md) | The corpus's steps counted by tree, their shape today, the rules and consumers keyed on them, and the skill's own corpus |
| [W01 work item](w01.md) | The step convention in the corpus guidelines |
| [W02 work item](w02.md) | Mode procedures as step sub-sections |
| [W03 work item](w03.md) | Protocol procedures as step sub-sections |
| [W04 work item](w04.md) | Artifact operations as step sub-sections |
| [W05 work item](w05.md) | Step references linked to their sub-sections |
| [W06 work item](w06.md) | The step-shape guard under `make check` |
| [Joins](joins.md) | Independent row pairs that take separate pull requests, and why |

## Decisions

- **Corpus only.** `pf` gains no rule on a procedure's shape; the guard is a repository check, not a build diagnostic.
- **One task per directory.** Modes, protocols and artifacts are each a reviewable pull request; the artifacts' 423 steps need a title written for each, which is the bulk of the work.
- **Fixtures move with each task.** The seven usage-example fixtures compile this tree, so each task regenerates the expected bundles its files reach.
- **After Dispatch Bundles.** W01 depends on E03 W06: E03 retires `W_DISPATCH_NOT_PROCEDURAL`, which would warn on every converted dispatched target, rewrites the run-set and bootstrap rules in the same guidelines file, and writes Board Reads as steps.

## Component Map

| Row | Component | Further paths written |
| --- | --- | --- |
| W01 | `example/work-planner/guidelines.md` | `example/guidelines.md`, `fixtures/usage-example/*/expected/` |
| W02 | `example/work-planner/modes` | `example/README.md`, `fixtures/usage-example/*/expected/` |
| W03 | `example/work-planner/protocols` | `fixtures/usage-example/*/expected/` |
| W04 | `example/work-planner/artifacts` | `fixtures/usage-example/*/expected/` |
| W05 | `example/work-planner` | `fixtures/usage-example/*/expected/` |
| W06 | `checks/steps.py` | `checks/tests`, `Makefile`, `checks.md` |

## Collision Surface

- **I05:E03 Dispatch Bundles.**
  Its W04 writes `delivery-evidence.md`, `guidelines.md` and `rules.md`; its W06 writes `SKILL.md`, `rules.md`, `guidelines.md` and removes `bootstrap.md`; W01 renames and W03–W06 regenerate the usage-example bundles. Every row here writes those bundles, W01 writes `guidelines.md` and W04 writes `delivery-evidence.md`.
- **I05:E01 Diagram Following.**
  Its unmerged base writes `Makefile` and `checks.md`, which W06 writes too.
- **I01:E00 Findings Ledger (draft #325).**
  Writes `Makefile`, `checks.md` and `checks/README.md`, which W06 writes too.

## Epic Priority

`deps.py` proposes E04 at the same number as E01 and E02, because no declared component is shared. The files above are shared, and W01 depends on E03 W06, so the proposed number is one below E03: `priority: 6` with E03 at 7. Pending the user's answer.

## Review

Review Initiative Goal and Check Dependencies and Numbering over the drafts, 2026-10-28.

- **Goal trace.**
  E04 covers I05's AC3 alone: it adds no `pf` behaviour and no bundling rule, and every row holds `make check` and `make corpus` on its revision. I05 marks no source.
- **Format.**
  `format.py` reports nothing to fix or decide on the draft body.
- **Corpus audit.**
  The criterion applies to workflow definitions; this corpus is example material, so the epic carries none.
- **Pending a decision.**
  The step heading's title form, the workspace skill's corpus, the guard row, and the discussion pull request.

## Links

| Resource | Link |
| --- | --- |
| Epic | I05:E04 Corpus Steps (not yet published) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
