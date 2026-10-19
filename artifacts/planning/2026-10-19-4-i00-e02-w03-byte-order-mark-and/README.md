# I00:E02:W03 Byte-Order Mark and Frontmatter Removal - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the third task of [I00:E02] Walking Skeleton. The task removes the transport metadata a source carries ahead of its content: one optional leading byte-order mark, and one leading frontmatter block delimited by a line of exactly three hyphens and closed by three hyphens or three dots. Neither is instruction text, and both would otherwise be published as body. The task also makes the encoding requirement real — a source must be valid UTF-8, and one that is not fails rather than being decoded with replacement characters, which would silently change the bytes the tool promises to preserve.

It matters because the removal is the first thing done to a source and it moves every offset after it, so a diagnostic reporting a location would point at the wrong line unless the shift is recorded. It matters again because the delimiter rules are narrow on purpose: an indented delimiter, a delimiter with trailing spaces, a TOML `+++` fence, a leading blank line before the three hyphens, and a YAML example inside a code block are each *not* frontmatter, and a scan that is generous about any of them eats content. The task covers AC2 and AC8.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w03.md](w03.md) | The task's plan: the delimiter rules, the coordinate shift each removal introduces and how it is recorded, and the encoding failure |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#4 \[I00:E02\] Walking Skeleton](https://github.com/m2ux/prosiform/issues/4) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W01 record | [Command interface, streams and exit statuses](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w01-command-interface-streams-and) |
| W02 record | [Profile configuration and source parsing](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w02-profile-configuration-and-source) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
