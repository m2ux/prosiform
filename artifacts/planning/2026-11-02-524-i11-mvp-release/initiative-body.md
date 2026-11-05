## Overview

The MVP, the argument surface and the grouping and composition work merged into `main`, is released: one version commit carries an annotated `contract/` and `python/` tag pair, its version chosen by running the previous contract's corpus against the build, and the release branch is raised into `main`. The goal the reviews test against is a released MVP a caller can name by its tags.

## Problem

The MVP's work lands on `main` with no release naming it.

- **The last release predates the MVP.**
  `contract/v0.15.0` and `python/v0.15.0` tag the build before presets, `subst`, section entries, placement and composition.
- **A version is settled by a run, not by judgement.**
  [`docs/versioning.md`](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md) chooses the bump by running the previous contract's corpus against the new build.

## Proposal

- **The release follows the merged MVP.**
  The argument-surface and grouping-and-composition prerequisites establish the release input. Deferred edge evaluation measurements do not gate release preparation.

- **The corpus run chooses the version.**
  The `contract/v0.15.0` corpus runs against the release build; any failure is incompatible, which below 1.0 bumps the minor.
- **One commit carries the release.**
  A `release/vX.Y.Z` branch from `main` holds one commit bumping `src/pyproject.toml` and the prosiform entry in `src/uv.lock`.
- **The tag pair names that commit.**
  Annotated `contract/vX.Y.Z` and `python/vX.Y.Z` tags, their messages following the previous pair.
- **The release reaches `main` by pull request.**
  The release branch is raised into `main`; the merge is the user's.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/525) | Release Cut | AC1, AC2 | | |

## Acceptance Criteria

- [ ] **AC1.** The release version is the one the `contract/v0.15.0` corpus run against the release build selects under the versioning rules, as the release record shows.
- [ ] **AC2.** An annotated `contract/` and `python/` tag pair names the release's version commit, and a pull request raises that commit into `main` with every check passing, as the tags and the pull request show.

## Non-Goals

- It does not declare the contract settled at `1.0.0`.
- It does not add install or quickstart material.
- It does not change the build, the corpus or the documentation it releases.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-524-i11-mvp-release) — the decisions, the goal trace and the work items.
- **R2.** **Source.** [Versioning](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md) — how a contract and a build are versioned and what a bump means.
