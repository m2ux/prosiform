# I00:E03:W01 Source Heading Slugs and the Heading Index - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the first row of [I00:E03] Outline Hierarchy. Visible heading text is derived from the parser's event stream — text and code content, link labels and decoded entities, with formatting delimiters, HTML tags and images read past — and the slug that text produces is the fragment a GitHub renderer generates for it, measured against the renderer itself. Headings are enumerated in source order, a slug already taken is numbered apart over every ordinal something already carries, and fresh state is kept per complete source document.

It matters because the fragment that reaches a heading is the renderer's, not the tool's. A lookup that invents its own spelling resolves to the wrong heading or to none, and every row that follows — section extraction, destination identity, link rewriting — reads the index this row builds. The row covers AC5, the slug compatibility criterion, and extends the source model, which no other row in this delivery wave touches.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w01.md](w01.md) | The task's plan: the text derivation, the slug transformation, the ordinal rule, the per-document index, and the collision that makes a source fragment observable in a bundle |
| [validation.md](validation.md) | The checks as they were run: GitHub's own anchors for every fixture's headings, the three measurements that changed the implementation, and each gate check's result |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#5 \[I00:E03\] Outline Hierarchy](https://github.com/m2ux/prosiform/issues/5) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
