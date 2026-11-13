# Link Entry Build — November 2026

> Task · Created 2026-11-13

## Executive Summary

`pf` takes a published Markdown link, Mermaid `click` line or class diagram `link` line as its entry, strips the operator marks that direct the agent, and compiles the destination with the presets the title or tooltip selects. `--pick` resolves a `?` deferral and is invalid usage anywhere else, and `--presets` is removed from the build, the corpus, the smoke check and the eval harness.

The build, the corpus fixtures and the checks share one pull request because removing `--presets` turns the corpus, the smoke check and the eval harness red until each changes with it.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w01.md](w01.md) | W01's work item: the link entry, `--pick` and the build's text |
| [w02.md](w02.md) | W02's work item: the corpus fixtures for link entries and `--pick` |
| [w03.md](w03.md) | W03's work item: the smoke check and eval harness on link entries |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I17:E01 #750](https://github.com/m2ux/prosiform/issues/750) |
| Initiative planning record | [Click Titles](../2026-11-12-click-titles/README.md) |
| Design | [W00 #751](https://github.com/m2ux/prosiform/pull/751) |
