# I00:E05:W01 Renderer-Generated Destinations and Ambiguity - October 2026

> Task Plan - Created 2026-10-20

## Executive Summary

This record holds the local plan for the first row of [I00:E05] Destination Identity. Every included document and section takes as its destination the fragment the declared renderer generates for the heading the bundle emits, taking the renderer's ordinal where two bundled headings share a slug. Two headings in one source sharing a slug fail as ambiguous when a source fragment requires one of them, and two source paths differing only by Markdown extension fail as ambiguous.

It matters because a bundle is navigable only if every reference reaches exactly one heading, and the ordinal is what makes that true by construction rather than by coincidence. The row carries [#75](https://github.com/m2ux/prosiform/issues/75): a heading a retained container carries is emitted into the bundle but does not enter the list a destination is numbered over, so a renderer indexes it and the map does not, and an entry line can resolve into a blockquote. Numbering over every heading the bundle emits is this row's own subject.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w01.md](w01.md) | The task's plan: the slug, the ordinal assigned over the emitted headings in bundle order, the two ambiguity refusals, and the headings the numbering runs over |
| [validation.md](validation.md) | What the renderer was measured to do, what the base was measured to do, and the checks the delivery was held to |
| [changes.md](changes.md) | Every change applied under the session's allowance and every change held |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#7 \[I00:E05\] Destination Identity](https://github.com/m2ux/prosiform/issues/7) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Destination defect | [#75 A Destination Is Numbered Over the Headings the Bundle Emits](https://github.com/m2ux/prosiform/issues/75) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
