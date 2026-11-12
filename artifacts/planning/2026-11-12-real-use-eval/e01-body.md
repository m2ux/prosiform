## Overview

Every workflow of the eval becomes skill variants, so each comparison the eval drew between forms is drawn between skills. The epic converts the five families still written as bare-prompt forms onto the skill-entry runner, one family a task, then retires the bare-prompt path once nothing runs on it.

## Problem

- **The forms are not skills.**
  A workflow gives a session [only the forms it is written in](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/README.md#L19), and every form but `bootstrap` is a tree or a bundle handed over by name.
- **Three instruction files drive the bare prompt.**
  [`instruction()`](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/workflow.py#L1134-L1145) fills one with the entry document's name for every form.
- **Bundles are compiled for the agent.**
  The `bundle`, `prose` and `compiled` forms hand a session what `pf` already wrote, so no session compiles a workflow it discovered.

## Proposal

- **The product variant is a skill of sources.**
  Its `SKILL.md` says to run `pf` and links the workflow's entry with `↳`, so the agent compiles what it follows; it takes the workflow's `compiled/` tree, or `diagram/` where it has none.
- **Each control is a plain-Markdown skill.**
  `tree`, `prose`, `linked` and `authored` link the same workflow's entry as an ordinary skill does, from the tree that form was written in.
- **A workflow keeps the comparisons it drew.**
  The diagram workflows take the product and the `tree`, `prose` and `linked` controls; the dispatch workflows the product and `authored`; the feature workflows the product and `tree`; the deferral and composition workflows the product alone.
- **Stated runs resolve from the skill.**
  A scenario's `compile` entries name references from the skill's directory, where its sources sit.
- **The variants share a description.**
  A workflow's variants carry one name and description, so a pass rate's difference is the material and not discovery.
- **A family stops its bare-prompt forms as it converts.**
  Until the last family converts, the others run as they did, so the eval stays runnable throughout.
- **The bare-prompt path leaves last.**
  Once every family is a skill, the three instruction files, the entry-file wiring and the bundled forms' layouts are removed, and `--forms` becomes `--variants`.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e01/w01.md) | Diagram workflows as skill variants | AC1 | [E00:W03](https://github.com/m2ux/prosiform/issues/735) | | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e01/w02.md) | Dispatch workflows as skill variants | AC2 | [E00:W03](https://github.com/m2ux/prosiform/issues/735) | | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e01/w03.md) | Deferral workflows as skills | AC3 | [E00:W03](https://github.com/m2ux/prosiform/issues/735) | | | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e01/w04.md) | Composition workflows as skills | AC4 | [E00:W03](https://github.com/m2ux/prosiform/issues/735) | | | |
| [W05](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e01/w05.md) | Feature workflows as skill variants | AC5 | [E00:W03](https://github.com/m2ux/prosiform/issues/735) | | | |
| [W06](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e01/w06.md) | The bare-prompt path retired | AC6 | W01, W02, W03, W04, W05 | | | |

## Acceptance Criteria

- [ ] **AC1.** Each of `linear`, `branching`, `looping`, `pricing` and `rework` is a product skill and `tree`, `prose` and `linked` control skills, each walking its scenarios' paths, as the corpus test shows.
- [ ] **AC2.** Each of the four dispatch workflows is a product skill and an `authored` control skill, each walking its scenarios' paths and dispatch traces, as the corpus test shows.
- [ ] **AC3.** Each of the four deferral workflows is a product skill whose stated runs resolve from the skill's directory, as the corpus test shows.
- [ ] **AC4.** Each of the two composition workflows, `dispatch-depth` and `subagent-first-run` is a product skill walking its scenarios' paths, traces and stated runs, as the corpus test shows.
- [ ] **AC5.** Each of the six feature workflows is a product skill and a `tree` control skill, each walking its scenarios' paths, as the corpus test shows.
- [ ] **AC6.** The runner starts no session from a prompt naming an entry document, as the corpus and run tests show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-real-use-eval) — the variant layout, the families and why each task stays its own pull request.
