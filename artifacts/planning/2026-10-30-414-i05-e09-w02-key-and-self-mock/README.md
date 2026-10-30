# I05:E09 W02 Key and Self-Mock Refusals — October 2026

> Task delivery · Created 2026-10-30

## Executive Summary

The three mapping shapes that state nothing and must be refused: two keys normalizing to one identity, a key whose sides normalize to one identity, and a key of the form `#section` that names no document to redirect. Each is invisible in a bundle and fails no other check, so the first silently wins and the second reads as a substitution that took effect.

All three are decided where the whole mapping is known — after every entry has been parsed, before any source is read — and each carries `E_INVALID_USAGE` with exit status 2, the outcome the contract gives a command line it refuses. Nothing is published, because a refused run opens nothing.

## Artifacts

| Artifact | What it holds |
| --- | --- |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic record | [Mock Substitution design](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-mock-substitution) |
| Predecessor | [W01 Mapping, option and identity](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-w01-mapping-option-and-identity) |
