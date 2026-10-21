# I00:E11:W21 Resource Portability: An Image Naming a Document Warns Like Any Resource — October 2026

> Work Record · Created 2026-10-21

## Executive Summary

A bundle whose only resource is an image naming a Markdown document emits no `W_RESOURCE_PORTABILITY` warning. The design makes an image a resource whatever file it points at, because image syntax embeds rather than links, so such a bundle names a resource and says nothing about it.

This row covers AC22 of the deferred-debt epic, which states what fixing the defect establishes rather than the defect it removes. It is delivered on the epic base rebuilt on the design I00:E12 landed, so what it measures is the product as it now stands.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w21.md](w21.md) | The row's plan: where the portability question is asked, and what the use contributes to it |
| [validation.md](validation.md) | The checks this row ran, the revision they ran against, and what each observed |
| [changes.md](changes.md) | The plan changes this session applied, and the ones it held for the user |

## Links

| Resource | Link |
| --- | --- |
| Task issue | [#144 \[I00:E11:W21\] Resource Portability: An Image Naming a Document Warns Like Any Resource](https://github.com/m2ux/prosiform/issues/144) |
| Epic issue | [#39 \[I00:E11\] Deferred Debt](https://github.com/m2ux/prosiform/issues/39) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Base rebuild | [I00:E11 Base Rebuild](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-39-i00-e11-base-rebuild) |
| Pull request | [#151 \[I00:E11\] An Image Naming a Document Warns Like Any Resource](https://github.com/m2ux/prosiform/pull/151) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
