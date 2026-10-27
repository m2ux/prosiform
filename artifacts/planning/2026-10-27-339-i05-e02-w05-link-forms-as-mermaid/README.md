# I05:E02:W05–W08 Link Forms as Mermaid Reads Them — October 2026

> Task delivery · Created 2026-10-27

## Executive Summary

This record holds the delivery of I05:E02 W05, W06, W07 and W08, joined in one pull request. The diagram link reader matches Mermaid 11.16.0 at its edges: each form is read in its own diagram type, a sequence destination ends at `;` and resolves a `#35;` anchor, and a `links` object is read as `JSON.parse` reads it. The anchor spellings have one home, a menu line is parsed once, and every link form the reader follows is proven by an end-to-end fixture whose bundle renders under Mermaid.

The findings that raised these rows are in [review.md](review.md). The epic's plan and the Mermaid 11.16.0 survey are in the [epic record](../2026-10-27-339-i05-e02-link-forms/README.md).

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [review.md](review.md) | The review of PR #342 whose findings these rows correct. |
| [w05.md](w05.md) | W05's plan: each form in its own diagram, the sequence statement's end and the entity anchor. |
| [w06.md](w06.md) | W06's plan: a `links` object read as `JSON.parse` reads it. |
| [w07.md](w07.md) | W07's plan: one home for the anchor spellings and one read per fence. |
| [w08.md](w08.md) | W08's plan: every diagram link form rendered end to end, and the boundary carried as written. |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E02 Link Forms](https://github.com/m2ux/prosiform/issues/339) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic pull request | [#342](https://github.com/m2ux/prosiform/pull/342) |
