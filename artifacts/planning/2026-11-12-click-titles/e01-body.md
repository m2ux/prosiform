## Overview

A release ships the click tooltip rule: a release branch and its version commit, the number the previous contract's corpus chooses, the release merged into `main`, and the paired tags on that merge.

## Problem

- **The rule ships in no build.**
  The latest tags, `contract/v0.24.0` and `python/v0.24.0`, read past a click's tooltip, and a caller holding an installed `pf` gets no click operator until a release carries it.

## Proposal

- **The procedure is the project's own.**
  [Cutting a release](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/versioning.md#cutting-a-release) states every step; this epic follows it once the click tooltip rule is on `main`.
- **The previous corpus chooses the number.**
  The previous contract tag's corpus runs against the new build; the retired tooltip fixture failing there makes the change incompatible, and the number moves as [What the numbers mean](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/versioning.md#what-the-numbers-mean) states.
- **The release branch is the delivery branch.**
  The row is delivered by `release/vX.Y.Z` cut from `main` and pull-requested into `main`; the epic takes no `i17/e01/main` base.
- **The tags go on `main`.**
  The release pull request merges first, and the paired tags name that merge.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-click-titles/e01/w01.md) | The release carrying click tooltips | AC1, AC2, AC3 | [E00:W03](https://github.com/m2ux/prosiform/issues/739) | | | |

## Acceptance Criteria

- [ ] **AC1.** The release's number is the one the previous contract tag's corpus, run against the release build, chooses under the versioning rules, as the recorded corpus run in the release pull request shows.
- [ ] **AC2.** The release pull request merges the release branch's one version commit into `main`, and `pf -v` on `main` reports that version, as the merged pull request and `pf -v` show.
- [ ] **AC3.** Annotated `contract/` and `python/` tags of that version name the release merge on `main`, their messages following the previous pair's, as `git show` of each tag shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-click-titles) — why the release is its own epic.
- **R2.** [Versioning](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/versioning.md) — the release procedure and the meaning of each number.
