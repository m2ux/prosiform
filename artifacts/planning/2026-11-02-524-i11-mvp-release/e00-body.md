## Overview

The release cut for the MVP: the version the previous contract's corpus selects, a release branch holding the one commit that sets it, the `contract/` and `python/` tag pair on that commit, and the pull request raising it into `main`.

## Problem

- **The MVP has no version.**
  `main` carries the merged MVP; its package metadata still reports the version `python/v0.15.0` tagged.
- **The bump is a measured fact.**
  It is read from the `contract/v0.15.0` corpus run against the release build, so it cannot be chosen before that run.
- **A tag message is a record.**
  `contract/v0.15.0` states the profile, the corpus count and the previous corpus's result; `python/v0.15.0` states the contract it implements and the validation counts.

## Proposal

- **The release waits for completed evaluation.**
  The evaluation initiative must close before the version measurement or release preparation starts.
- **The run first.**
  The `contract/v0.15.0` corpus runs against the release build, and the release record states its result and the version it selects: any failure is incompatible, which below 1.0 bumps the minor.
- **One commit on a release branch.**
  `release/vX.Y.Z` is cut from `main` and holds one commit bumping `src/pyproject.toml` and the prosiform entry in `src/uv.lock`.
- **The tag pair on that commit.**
  Annotated `contract/vX.Y.Z` and `python/vX.Y.Z`, their messages following the previous pair.
- **A pull request into `main`.**
  The release branch is raised into `main` with its checks passing; merging it is the user's.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| W01 | The version the previous corpus selects | AC1 | #462, #463, #464 | | | |
| W02 | The release branch and its version commit | AC2 | W01 | W03, W04 | | |
| W03 | The `contract/` and `python/` tag pair | AC3, AC4 | W01 | W02, W04 | | |
| W04 | The release pull request into `main` | AC5, AC6 | W01 | W02, W03 | | |

## Acceptance Criteria

- [ ] **AC1.** The release record states the `contract/v0.15.0` corpus's result against the release build and the version that result selects under `docs/versioning.md`, as the recorded run output shows.
- [ ] **AC2.** `release/vX.Y.Z`, cut from `main`, holds one commit setting the selected version in `src/pyproject.toml` and the prosiform entry in `src/uv.lock`, as `git log main..release/vX.Y.Z` and `make lock-check` show.
- [ ] **AC3.** An annotated `contract/vX.Y.Z` tag names the version commit, its message stating the revision's subject, its profile, its corpus count and the previous corpus's result as `contract/v0.15.0`'s does, as `git tag -n` shows.
- [ ] **AC4.** An annotated `python/vX.Y.Z` tag names the same commit, its message stating the contract it implements, its profile, its package version and its validation counts as `python/v0.15.0`'s does, as `git tag -n` shows.
- [ ] **AC5.** A pull request from `release/vX.Y.Z` into `main` is open, as its head, base and state show.
- [ ] **AC6.** Every check on the release pull request passes, as its check conclusions show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-524-i11-mvp-release) — the decisions and the work items.
- **R2.** [Versioning](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md) — what a bump means and how the corpus run settles it.
