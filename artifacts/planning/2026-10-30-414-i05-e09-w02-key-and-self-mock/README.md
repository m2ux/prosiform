# I05:E09 W02 Key and Self-Mock Refusals — October 2026

> Task delivery · Created 2026-10-30

## Executive Summary

The three mapping shapes that state nothing and must be refused: two keys normalizing to one identity, a key whose sides normalize to one identity, and a key of the form `#section` that names no document to redirect. Each is invisible in a bundle and fails no other check, so the first silently wins and the second reads as a substitution that took effect.

All three are decided where the whole mapping is known — after every entry has been parsed, before any source is read — and each carries `E_INVALID_USAGE` with exit status 2, the outcome the contract gives a command line it refuses. Nothing is published, because a refused run opens nothing.

Three corpus fixtures prove it, and the duplicate's message names both spellings the author wrote, so a caller is sent to the two options to edit rather than to the identity they share. The epic's mapping table lists a fourth refusal — a value naming no Markdown document — that no criterion covers; it is raised as deferred debt rather than landed here.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W02 work item](w02.md) | The three mapping refusals, the fixtures that show each, and the review's two additions |
| [Validation](validation.md) | The checks T1–T11 at the revisions they ran, with their observations |
| [Change list](change-list.md) | Every plan change this session applied, and every one it held |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic record | [Mock Substitution design](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-mock-substitution) |
| Predecessor | [W01 Mapping, option and identity](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-w01-mapping-option-and-identity) |
| Pull request | [#431 Key and Self-Mock Refusals](https://github.com/m2ux/prosiform/pull/431) |
| Deferred debt | [#432 A Value Naming No Markdown Document](https://github.com/m2ux/prosiform/issues/432) |
