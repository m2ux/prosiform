# I02 MVP Demonstration — October 2026

> Initiative planning · Created 2026-10-25

## Executive Summary

This record plans a new initiative on the bundling theme: a three-day demonstration of the feature set prosiform already delivers, run against the example tree its documentation points at. The work moves the example-migration epic out of the field-refinement initiative, where it competes with twenty-six rows of non-demonstration work, and defers the rest of that initiative until after the demonstration.

The example as it stands is a four-file reduction of a skill its users write, so it cannot show a grouped folder, a mode that runs another mode, or a protocol. The migration epic already planned the larger tree, the per-folder metadata, the per-mode bundles and the regenerated fixtures; this initiative carries those seven rows as its delivery and adds the ground a demonstration needs: a tagged baseline, one repeatable command, and the repository's own checks held green on the branch the demonstration runs from.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Evidence](evidence.md) | The measured baseline the plan stands on, and the gaps it found |
| [Decisions](decisions.md) | Each design choice, with the evidence behind it |
| [Initiative draft](i02.md) | The initiative body as published |
| [Demonstration Ground draft](e01.md) | The epic supplying the tagged revision and the published command |
| [Deferred Debt draft](e02.md) | The epic holding what the delivery defers |
| [Published](published.md) | The issues created, and the edits made to the issues that carried the work before |

## Open Questions

- **Q1. Which long-lived branch the demonstration runs from.**  The tag in the ground epic names a revision of whichever branch carries the example and the build together. Its recommended answer is `main`, because the checks and the corpus already run there, and the migration's own branch merges into it.
- **Q2. Which mode the demonstration bundles.**  A mode cannot show the group its peers belong to, so the demonstrated bundle shows the artifacts and protocols groups instead. Its recommended answer is the planning mode, because it is the mode the example's published invocation already names.


## Links

| Resource | Link |
| --- | --- |
| Originating proposal | [P00 Markdown Bundling](https://github.com/m2ux/prosiform/issues/1) |
| Migration epic carried into the initiative | [I01:E11 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative this one defers | [I01 Field Refinement](https://github.com/m2ux/prosiform/issues/20) |
| Production compiler, renumbered behind this initiative | [Production Compiler](https://github.com/m2ux/prosiform/issues/10) |
| Grouping defect deferred past the demonstration | [Parent Merge](https://github.com/m2ux/prosiform/issues/234) |
| Board | [Board 18](https://github.com/users/m2ux/projects/18) |
