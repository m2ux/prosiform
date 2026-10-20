# I00:E05:W02 Link Rewriting Through the Destination Map - October 2026

> Task Plan - Created 2026-10-20

## Executive Summary

This record holds the local plan for the second row of [I00:E05] Destination Identity. Each local Markdown link and each fragment-only link in selected content is rewritten to the destination of the target it resolved to, through the map [W01](https://github.com/m2ux/prosiform/pull/83) built. After the rewrite no link in the bundle names a source path, and every destination resolves to exactly one heading in it. The row also finishes the entry line, which links each entry reference to the destination it resolved to and so is written through that same map.

It matters because the rewrite is the point of the bundling: an outbound reference becomes a reference inside the document the reader already holds, so the content it names is present rather than fetched. Until this row lands, a bundle carries correct destinations and links that still go nowhere.

The row is where the mark leaves the bundle. A dependency is a reference whose author marked it, and the contract says a *rewritten* link carries the text that followed the mark; traversal resolves a marked reference but does not rewrite it, so every expected bundle in the corpus currently states a marked link reaching the bundle whole. Those bundles change here. The mark survives only where the text was never a link, which is why one fixture carries a marked reference inside a code example alongside a real one.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w02.md](w02.md) | The task's plan: the link kinds carrying a local destination, the map lookup and rewrite, the entry line this row completes, and the expected bundles the rewrite changes |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#7 \[I00:E05\] Destination Identity](https://github.com/m2ux/prosiform/issues/7) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Preceding row | [#83 \[I00:E05\] Renderer-Generated Destinations and Ambiguity](https://github.com/m2ux/prosiform/pull/83) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
