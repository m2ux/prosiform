# I00:E04:W04 Selection Consolidation and Expanded Coverage - October 2026

> Task Plan - Created 2026-10-20

## Executive Summary

This record holds the local plan for the fourth row of [I00:E04] Dependency Closure. A selection contained within a larger one is represented by the larger region alone, and that region's own references are resolved; a link whose target is present only as a heading-only ancestor expands closure to include that section's selected body; and one selection produces the same bundle whatever order its entry references were given in and whatever order its dependencies were discovered in, with groups ordered by root-relative path.

It matters because the same region arrives by several paths once traversal runs to a fixed point, and emitting it twice makes the bundle disagree with its sources. The row also carries a defect found while delivering [W03](https://github.com/m2ux/prosiform/pull/77): a run can write its bundle over a source it reached as a dependency and lose that file, because the check refusing an output that names an input source reads the entry references alone. This row walks the completed closure, which is the first point the full set of paths a run read is known.

AC3 and AC9 hold on the merged base and this row supplies the corpus evidence that states them. AC10 stays unticked: a heading-only structural ancestor is [I00:E09:W02](https://github.com/m2ux/prosiform/issues/60)'s work, the build emits none, and no run on this base can reach the state the criterion turns on. The fixture declaring it carries `awaiting = "I00:E09:W02"`.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w04.md](w04.md) | The task's plan: the consolidation rule, the retained target mapping, the re-traversal, the output check the closure completes, and why AC10 stays unticked |
| [validation.md](validation.md) | The validation record: the behaviour measured before the design was built to it, the instrument behind each criterion, and the output each check returned |
| [changes.md](changes.md) | The change list: every plan change this session applied and every one it held |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#6 \[I00:E04\] Dependency Closure](https://github.com/m2ux/prosiform/issues/6) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W03 record | [Link classification and traversal to a fixed point](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-6-i00-e04-w03-link-classification-and-traversal) |
| Structural ancestors | [#60 \[I00:E09\] Outline and Closure Completion](https://github.com/m2ux/prosiform/issues/60) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
