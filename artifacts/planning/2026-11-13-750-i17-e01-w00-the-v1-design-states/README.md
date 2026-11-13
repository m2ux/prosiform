# Link Invocation Design — November 2026

> Task · Created 2026-11-13

## Executive Summary

The v1 design states how `pf` is invoked on a link: an entry is a published Markdown link, a Mermaid `click` line or class diagram `link` line, or a plain path, and `pf` decodes the destination, section, operator and presets itself. A `?` deferral takes its pick through `--pick`, which is invalid usage anywhere else, and the design holds no `--presets` option.

The design is the contract the build, the corpus and the documentation of I17:E01 answer to, so it lands first on `engineering`, ahead of the build that implements it.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w00.md](w00.md) | The work item: the design sections restated and the checks they take |
| [test-results.md](test-results.md) | The checks run on the design change and their results |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I17:E01 #750](https://github.com/m2ux/prosiform/issues/750) |
| Initiative planning record | [Click Titles](../2026-11-12-click-titles/README.md) |
