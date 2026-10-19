# I00:E02:W04 Whole-Document Emission Under a Filename Heading - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the fourth task of [I00:E02] Walking Skeleton, and the first that publishes anything. A contributing source is emitted beneath one generated document-level heading whose visible text is its normalized root-relative path with the Markdown extension removed, escaped so that punctuation in a path cannot become a link, an image or inline HTML. The document's own content follows, its preamble before its first retained heading. The task carries no dependency traversal and no link rewriting; one named document becomes one bundle.

It matters because every row before it made the command fail more precisely and none made it succeed. Fifteen fixtures in the corpus declare a successful bundling and fail today on exit status alone, so this is the row that turns a corpus of refusals into a corpus of results, and the first evidence that the three epics of work so far describe a tool that produces something. It matters again because several of those fixtures were authored before anything emitted a bundle: where one disagrees with what this emission produces, which of the two states the contract is a question this row settles rather than resolves by whichever came first. The task covers AC1.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w04.md](w04.md) | The task's plan: the file-group structure, the heading generation and the escaping a path needs to remain literal heading text, and the expected bundles the corpus declared ahead of this row |
| [validation.md](validation.md) | The checks as they were run: the set in one pass, the bundle's structure, the command's statuses and publication, the corpus measured at the base and at this head, six deliberate faults, and the criteria this bundle makes observable |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#4 \[I00:E02\] Walking Skeleton](https://github.com/m2ux/prosiform/issues/4) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W01 record | [Command interface, streams and exit statuses](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w01-command-interface-streams-and) |
| W02 record | [Profile configuration and source parsing](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w02-profile-configuration-and-source) |
| W03 record | [Byte-order mark and frontmatter removal](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w03-byte-order-mark-and) |
| W07 record | [An error code for every failing outcome](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w07-an-error-code-for) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
