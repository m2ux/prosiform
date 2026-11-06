## Overview

The MVP release cut: `release/v0.17.0` declares the version the previous contract's corpus selects and carries the `contract/v0.17.0` and `python/v0.17.0` tag pair on its one commit. Merging it makes `main` report the shipped version.

## Changes

### Version Declaration

- **The build declares `0.17.0`.**
  `src/pyproject.toml` and the `prosiform` entry of `src/uv.lock` carry the number, and `pf -v` reports it.

## Test Plan

| Test | Description | Coverage | Pass |
| --- | --- | --- | --- |
| T1 | `uv lock --check` resolves the lock at the declared version | AC2 | [✓](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-525-i11-e00-w02-release-cut/checks.md#lock) |
| T2 | `make check` passes at the committed head | AC2, AC6 | [✓](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-525-i11-e00-w02-release-cut/checks.md#full-configured-check) |
| T3 | The branch holds one commit beyond `main`, changing the two files alone | AC2 | [✓](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-525-i11-e00-w02-release-cut/checks.md#full-configured-check) |
| T4 | Both annotated tags name the version commit | AC3, AC4 | [✓](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-525-i11-e00-w02-release-cut/version.md#the-version) |
| T5 | The pull request is open from `release/v0.17.0` into `main` | AC5 | [✓](https://github.com/m2ux/prosiform/pull/678) |

## Merge

`main` requires an approving review, so this pull request is handed over unmerged. The `contract/v0.17.0` and `python/v0.17.0` tags name `b10437ea7`, whose `Checks` run completed `success`.

## References

- **R1.** [Release cut record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-06-525-i11-e00-w02-release-cut) — the version derivation, the tag messages and the validation at the tagged head.
- **R2.** [Version measurement](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-06-525-i11-e00-w01-the-version-the-previous) — the corpus runs that select the number.
