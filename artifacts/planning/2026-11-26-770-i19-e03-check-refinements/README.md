# I19 E03: Check Refinements

> Epic plan. Created 2026-11-26.

## Executive Summary

The check gaps epic closed its four cases, and its delivering sessions found four more: two checks with their own fence reading, a build-word rule that refuses ordinary words, avoided terms in the documentation, and a document boundary the documentation defines and the build no longer computes.

The user placed them in the initiative rather than as standalone issues, so the initiative closes with every check reading and refusing exactly what its rule states.

## Decisions

| Decision | State |
| --- | --- |
| Where the gaps go | Decided by the user: a new I19 epic. |
| Epic priority | 1: it is the initiative's only open epic once E02 merges. |
| W01 and W03 | One pull request: both change the vocabulary check and its tests. |
| The boundary | Decided by the user: removed from the documentation. If the design on the engineering branch states it as behaviour, the session asks the user before changing the contract. |

## Sources

| Row | Found by |
| --- | --- |
| W01 | The I19 E02 W01 delivery, as an arising issue. |
| W02, W03 | The I19 E02 W02 and W03 delivery, as arising issues. |
| W04 | The I19 E02 W04 delivery, which removed `closure.boundary`. |

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [epic-e03.md](epic-e03.md) | Body of the epic. |
| [w01.md](w01.md) | Work item: every check reads the shared code-block reading. |
| [w02.md](w02.md) | Work item: build words are marked terms. |
| [w03.md](w03.md) | Work item: avoided terms in the documentation. |
| [w04.md](w04.md) | Work item: the documentation without a boundary. |

## Links

| Resource | URL |
| --- | --- |
| Initiative I19 | https://github.com/m2ux/prosiform/issues/770 |
