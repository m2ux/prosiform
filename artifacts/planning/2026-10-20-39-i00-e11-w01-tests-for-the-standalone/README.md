# I00:E11:W01 Tests for the Standalone Checks, Slug Rule Included - October 2026

> Task Plan - Created 2026-10-20

## Executive Summary

This record holds the local plan for the row that puts the repository's standalone checks under tests of their own. The heading-slug rule the link check applies is held to the anchor GitHub generates, measured against headings the rule would otherwise get wrong, and each check's parsing is held by tests that run beside the others against a document the parser would read wrongly.

It matters because the checks are what the repository trusts to read its own documents, and they are the one body of code nothing observes. A slug rule that drifts from GitHub's anchor, or a parser that misreads a document, reports a clean run over a defect, and a check nobody can trust is a check that teaches its reader to skip it.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w01.md](w01.md) | The task's plan: the checks under test, the slug comparison and the parsing cases |
| [validation.md](validation.md) | The test procedure, the runs and what each one establishes |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#39 \[I00:E11\] Deferred Debt](https://github.com/m2ux/prosiform/issues/39) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Slug observation | [W04 validation record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-18-26-i00-e00-w04-continuous-integration-running-those) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
