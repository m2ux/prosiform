# I11 E00 W01: the version the previous corpus selects — November 2026

> Delivery record · Created 2026-11-06 · Revised 2026-11-06

## Executive Summary

The `contract/v0.15.0` corpus was run against the build at `origin/main`. 305 of its 312 fixtures fail, so the change is major, which below `1.0.0` moves the minor: the version is `0.16.0`.

`main` already declares `0.16.0` in `src/pyproject.toml` and `src/uv.lock`, and no tag for it exists. The measurement confirms the declared number, and that same fact blocks the next unit: W02's acceptance criterion requires a release branch holding a bump commit `main` lacks, which a branch cut from `main` cannot hold.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work item](w01.md) | The row's scope, design, component and tests |
| [Release record](release.md) | The corpus run, its result and the version it selects |
| [Corpus log](corpus-v0.15.0.log) | The complete output of the `contract/v0.15.0` corpus against the release build |
| [Blocker](blocker.md) | Why the joined W02–W04 unit cannot start, and the two resolutions |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I11:E00 Release Cut](https://github.com/m2ux/prosiform/issues/525) |
| Initiative | [I11 MVP Release](https://github.com/m2ux/prosiform/issues/524) |
| Delivering commit | [`9380588ce`](https://github.com/m2ux/prosiform/commit/9380588ce19424594ffc9ea9dc2414beaecbd65e) |
| Previous contract tag | [`contract/v0.15.0`](https://github.com/m2ux/prosiform/releases/tag/contract/v0.15.0) |
| Versioning rule | [Versioning](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md) |
