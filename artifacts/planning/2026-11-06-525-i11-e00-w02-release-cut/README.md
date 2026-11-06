# I11 E00 W02–W04: the release cut — November 2026

> Delivery record · Created 2026-11-06

## Executive Summary

The release is cut as `release/v0.17.0`, one commit beyond `main` that declares the version the previous contract selects. The version is `0.17.0`, measured rather than preferred: `main`'s declared `0.16.0` names a contract revision whose own corpus already fails against this build, so the minor moves once from that declaration under the pre-1.0 rule.

The annotated `contract/v0.17.0` and `python/v0.17.0` tags name that commit, and the pull request raising it into `main` is open with every check passing. The merge is the user's, since `main` requires an approving review.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Version derivation](version.md) | Both candidate baselines, their corpus runs, and why the number is 0.17.0 |
| [Branch work item](w02.md) | The release branch and its version commit |
| [Tag work item](w03.md) | The `contract/` and `python/` tag pair |
| [Pull request work item](w04.md) | The release pull request into `main` |
| [Validation](checks.md) | `make check` and `uv lock --check` at the committed head |
| [Pull request body](pr-body.md) | The body the release pull request carries |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I11:E00 Release Cut](https://github.com/m2ux/prosiform/issues/525) |
| Initiative | [I11 MVP Release](https://github.com/m2ux/prosiform/issues/524) |
| Release pull request | [#678](https://github.com/m2ux/prosiform/pull/678) |
| Version measurement | [W01 record](../2026-11-06-525-i11-e00-w01-the-version-the-previous/README.md) |
| Versioning rule | [Versioning](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md) |
