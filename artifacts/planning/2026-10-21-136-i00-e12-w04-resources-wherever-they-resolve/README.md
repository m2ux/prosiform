# I00:E12:W04 and W05 Resources and Self-References — October 2026

> Task Plan · Created 2026-10-21

## Executive Summary

This record holds the local plan for the pair of rows that retire the rules the old mark existed to serve. A resource is emitted as the author wrote it wherever it resolves, the allowed source root included, because only Markdown documents are bundleable; and a link naming the section it sits in, or an ancestor of that section, resolves to that content's destination in the bundle like any other reference.

The two rows share a pull request because they retire the same pair of refusals — a marked resource and a marked self-reference — and the catalogue entry each removes is read by one check. Splitting them would leave the catalogue red between the two merges.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w04.md](w04.md) | The resource row's plan: where a resource reference is classified and emitted |
| [w05.md](w05.md) | The self-reference row's plan: where a self or ancestor reference resolves |
| [validation.md](validation.md) | The checks the rows ran, the revision they ran against, and what each observed |
| [changes.md](changes.md) | The plan changes this session applied, and the ones it held for the user |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#136 \[I00:E12\] Positional Dependencies](https://github.com/m2ux/prosiform/issues/136) |
| Epic plan | [2026-10-21-136-i00-e12-positional-dependencies](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-136-i00-e12-positional-dependencies) |
| Design and decision | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Preceding row | [2026-10-21-136-i00-e12-w01-classification-by-where-a](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-136-i00-e12-w01-classification-by-where-a) |
| Pull request | [#142 \[I00:E12\] Resources as Authored and Self-References Resolved](https://github.com/m2ux/prosiform/pull/142) |
| Deferred debt | [#144](https://github.com/m2ux/prosiform/issues/144) and [#145](https://github.com/m2ux/prosiform/issues/145), placed as `I00:E11:W21` and `W22` |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
