# Merged-Epic Review — October 2026

> Review record · Created 2026-10-31

## Executive Summary

Fifteen epics already merged into `main` were each reviewed by an independent agent for delivered defects, five epics at a time, at `23882b7d`. A defect is recorded only where the reviewer named the current tree's `path:line` and showed a case that fails; every blocker below was reproduced against the working tree, and four of the five were reproduced a second time outside the reviewing agent.

Eighty-two defects were found: five blockers, thirty-six major and forty-one minor. Three of them were named by one reviewer and attributed to an edit after the epic merged, and each still holds at the head reviewed. Three patterns account for most of them. Guards whose reach is narrower than the rule they state account for eleven findings across six epics. Acceptance criteria that enumerate the documents to update, rather than the rule to hold, account for five. The example skill is validated as documents and never executed, which is why 39 of its command blocks name a script the repository does not carry.
    10|
## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Findings table](findings.md) | Every finding, ordered by severity, with the epic that delivered it |

## Links

| Resource | Link |
| --- | --- |
| Epic | [`main`](https://github.com/m2ux/prosiform/commits/main) — reviewed at `23882b7d` |
| Findings | [Findings table](findings.md) |
| Reviewed epics | [I05:E10](https://github.com/m2ux/prosiform/issues/423), [I05:E07](https://github.com/m2ux/prosiform/issues/389), [I05:E06](https://github.com/m2ux/prosiform/issues/376), [I05:E05](https://github.com/m2ux/prosiform/issues/374), [I05:E04](https://github.com/m2ux/prosiform/issues/352), [I05:E03](https://github.com/m2ux/prosiform/issues/351), [I05:E02](https://github.com/m2ux/prosiform/issues/339), [I05:E01](https://github.com/m2ux/prosiform/issues/333), [I05:E00](https://github.com/m2ux/prosiform/issues/326), [I02:E03](https://github.com/m2ux/prosiform/issues/290), [I02:E02](https://github.com/m2ux/prosiform/issues/263), [I02:E01](https://github.com/m2ux/prosiform/issues/262), [I02:E00](https://github.com/m2ux/prosiform/issues/258), [I01:E06](https://github.com/m2ux/prosiform/issues/218), [I01:E02](https://github.com/m2ux/prosiform/issues/195) |
| Unreviewed epics | I00:E00–E12 (thirteen epics) |
