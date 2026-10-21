# I00:E11:W20 Nested Link Rewriting: A Link Inside a Nested Image Stops the Run — October 2026

> Work Record · Created 2026-10-21

## Executive Summary

A link written inside an image's alternative content, where an enclosing link carries that image, ends the run with `E_UNEXPECTED_INTERNAL_ERROR`. The parser reads three uses in that run and the emission's own text scan reads two, because the scan takes a link whose label already holds a link to be literal text, and a link inside an image inside a link is such a label.

This row covers AC21 of the deferred-debt epic, which states what fixing the defect establishes rather than the defect it removes. It is delivered on the epic base rebuilt on the design I00:E12 landed, so what it measures is the product as it now stands.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w20.md](w20.md) | The task's plan: where the emission's scan discards an enclosing link, and the containment rule that keeps it |
| [validation.md](validation.md) | What the build was measured to do and the checks the delivery was held to |
| [changes.md](changes.md) | The plan changes this session applied, and the ones it holds |

## Links

| Resource | Link |
| --- | --- |
| Task issue | [#135 \[I00:E11:W20\] Nested Link Rewriting: A Link Inside a Nested Image Stops the Run](https://github.com/m2ux/prosiform/issues/135) |
| Epic issue | [#39 \[I00:E11\] Deferred Debt](https://github.com/m2ux/prosiform/issues/39) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Base rebuild | [I00:E11 Base Rebuild](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-39-i00-e11-base-rebuild) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
