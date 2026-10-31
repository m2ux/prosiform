# 441 Two Entries and One Derived Name — October 2026

> Standalone fix · Created 2026-10-31

## Executive Summary

`docs/bundles.md` stated a refusal the run never makes: two entries deriving one name — `a/b.md` and `a_b.md` — "fail the run before anything is written". The run publishes instead, because the design's Combined selection rule joins each selection's name into one run folder, and the join is what keeps the two apart.

The W03 delivery found the sentence while correcting a neighbouring claim about derived names. This record holds the reproduction, the checks, and the correction.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Validation](validation.md) | The reproduction, the checks, and what each observed |

## Links

| Resource | Link |
| --- | --- |
| Issue | [441 The documented refusal of two bundles deriving one name never happens](https://github.com/m2ux/prosiform/issues/441) |
| Found by | [W03 Entry Redirect and Derived Name](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-414-i05-e09-w03-entry-redirect-and-derived) |
| Design | [Combined selection](https://github.com/m2ux/prosiform/blob/a59b62fca8ad2a155e4e32ac7857761b871cf304/artifacts/planning/2026-10-17-prosiform-v1/design.md) |
