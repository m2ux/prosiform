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
| [test-results.md](test-results.md) | The checks run on the joined unit and their results |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I17:E01 #750](https://github.com/m2ux/prosiform/issues/750) |
| Initiative planning record | [Click Titles](../2026-11-12-click-titles/README.md) |
| Design | [W00 #751](https://github.com/m2ux/prosiform/pull/751) |

## Plan Changes

| Change | Kind | State |
| --- | --- | --- |
| #750's W02 and W03 rows name each other in Joins, as the one pull request #752 delivered them | Task creation | Applied |
| [#754](https://github.com/m2ux/prosiform/issues/754) Agent-pick scenarios accept a first-run pick, arising from #752's review | Folded work | Held: the eval harness belongs to I15:E02 and I16, so its placement is the user's |
