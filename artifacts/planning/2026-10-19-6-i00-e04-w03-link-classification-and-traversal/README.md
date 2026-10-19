# I00:E04:W03 Link Classification and Traversal to a Fixed Point - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the third row of [I00:E04] Dependency Closure, and the row that turns a document transformer into a compiler. A reference is classified as a marked local Markdown document, an unmarked local Markdown link, a fragment-only link, or a resource; the marked ones are resolved against their own originating document, bundled and included; and traversal continues over newly included content until nothing further is reachable, without a recursive-call cap that would refuse a valid cyclic graph.

It matters because this is where the marking proposal [P03](https://github.com/m2ux/prosiform/issues/55) becomes behaviour. A dependency is the reference its author marked, and an unmarked local Markdown link is emitted as authored and resolves as nothing, even where the bundle carries the document it names. The row covers five criteria — AC1, AC2, AC12, AC15 and AC16 — and carries the correction of `docs/glossary.md`, whose definition of a dependency the mark replaced.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w03.md](w03.md) | The task's plan: the classification, the worklist traversal, the fixed-point condition, and the glossary definition this row corrects |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#6 \[I00:E04\] Dependency Closure](https://github.com/m2ux/prosiform/issues/6) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Marking proposal | [#55 \[P03\] Bundled Links: Dependencies the Author Marks](https://github.com/m2ux/prosiform/issues/55) |
| W02 record | [Root confinement and no-symlink source access](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-6-i00-e04-w02-root-confinement-and-no) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
