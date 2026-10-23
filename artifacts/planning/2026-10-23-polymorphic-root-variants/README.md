# Polymorphic Root Variants — October 2026

> Plan · Created 2026-10-23

## Executive Summary

A linked file that omits `prosiform.root` takes the effective root of the parent that reached it. One physical file reached under two roots is captured once and rendered once for each root, and each rendering resolves that file's links under its own root. That is the polymorphic root rule: the same bytes, one behaviour per reaching root.

The rule is planned here and the implementation is deferred. Document Metadata stays the delivered contract in review. This record is the design change, written before any corpus or build change. The epic issue is not opened until a priority is confirmed.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Epic draft](epic.md) | The epic body to publish as I01 E08 |
| [Inherited roots](w01.md) | Resolving an omitted root from the reaching parent |
| [Root variants](w02.md) | One capture and one rendering per distinct root |
| [Author contract](w03.md) | The author-facing statement of the rule |
| [Trace](trace.md) | Goal, initiative criteria, and the source this rule departs from |
| [Decisions](decisions.md) | Placement, deferral, numbering, and the held freeze handoff |
| [Joins](joins.md) | Why the three rows do not share a pull request |

## Links

| Resource | Link |
| --- | --- |
| Initiative | [Field Refinement](https://github.com/m2ux/prosiform/issues/20) |
| Epic | [Inherited Roots](https://github.com/m2ux/prosiform/issues/233) |
| Delivered root contract | [Document Metadata](https://github.com/m2ux/prosiform/issues/218) |
| Board | [Board 18](https://github.com/users/m2ux/projects/18) |
