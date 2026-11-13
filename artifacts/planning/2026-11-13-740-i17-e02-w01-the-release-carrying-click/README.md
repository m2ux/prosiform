# Click Titles Release — November 2026

> Task · Created 2026-11-13

## Executive Summary

A release ships the click tooltip rule and the link entry: a `release/vX.Y.Z` branch from `main` with one version commit, the number the previous contract tag's corpus chooses when run against the release build, the release pull request merged into `main`, and annotated `contract/` and `python/` tags on that merge.

The latest pair, `contract/v0.24.0` and `python/v0.24.0`, reads past a click's tooltip and takes `--presets`, so an installed `pf` carries neither rule until this release.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Release work item](../2026-11-12-click-titles/e02/w01.md) | The branch, version commit, number, pull request and tags |
| [test-results.md](test-results.md) | The checks run on W01, the previous corpus run and the prepared tag messages |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I17:E02 #740](https://github.com/m2ux/prosiform/issues/740) |
| Initiative planning record | [Click Titles](../2026-11-12-click-titles/README.md) |
| Release procedure | [Cutting a release](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md#cutting-a-release) |
