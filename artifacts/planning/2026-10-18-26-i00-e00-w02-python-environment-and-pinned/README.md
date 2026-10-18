# I00:E00:W02 Python Environment and Pinned Dependencies - October 2026

> Task Plan - Created 2026-10-18

## Executive Summary

This record holds the local plan for the second task of [I00:E00] Project Foundation. The task writes the project definition that declares the supported Python version and the build's dependencies, produces the lockfile that records the exact resolved versions, and documents the command that creates an environment from it. It also declares `docs/glossary.md` as package data, so the glossary reaches an installed build and the epic's published-with-the-build clause has a distribution to assert against.

It matters because the prototype's parser is decided and unpinned. Two checkouts that resolve different parser versions disagree about what a Markdown document means, and a corpus whose expected bundles depend on that disagreement binds nothing. The task covers AC2 of the epic, and carries the packaging assertion that completes AC6.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w02.md](w02.md) | The task's plan: the project definition, the lockfile, the environment command and the glossary the wheel carries |
| [validation.md](validation.md) | The environment setup run as it was performed: procedure, tested revision, observations, the differing-version case it caught, and each dependency measured against the profile |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#26 \[I00:E00\] Project Foundation](https://github.com/m2ux/prosiform/issues/26) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Preceding task | [W01 record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-18-26-i00-e00-w01-repository-layout-readme-and) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
