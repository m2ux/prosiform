# md-compose v1 — October 2026

> Initiative Plan · Created 2026-10-17

## Executive Summary

md-compose compiles a set of linked local Markdown documents into one continuous, validated Markdown document. Agent skills in this workspace are authored as modular instruction sets: a skill entry point links to modes, modes link to artifacts, and artifacts link to one another's sections. Reaching the complete context for one operation currently means the agent resolves that graph itself, deciding which sections to read, where each section ends, and when the closure is complete. md-compose moves that retrieval into a deterministic compilation step that either returns the whole composite or fails with a diagnostic.

The work is partitioned by solution maturity. A Python 3 prototype implements the behavioural contract and produces a language-neutral fixture corpus of exact expected composites; it is retained as a differential oracle rather than discarded. A Rust implementation then delivers production md-compose against that same corpus, opening with an empirical verdict on two parser viability gates that `pulldown-cmark` may not satisfy. The corpus is the contract, so neither implementation is the specification of the other.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Design](design.md) | The approved v1 behavioural contract: input and output, Markdown profile, section extraction, anchor identity, validation invariants and resource limits |
| [Upstream Assessment](upstream-assessment.md) | The inspected state of `pulldown-cmark` against the parser gates, and the two narrowly scoped contributions, deferred and unauthorized |
| [Decisions](decisions.md) | The planning decisions taken with the user, the reasoning behind each, and the measured evidence |
| [Review](review.md) | The goal trace, the source alignment, the threats checked, and the independent task pairs |
| [I00 initiative body](i00-initiative.md) | The local source for issue #2, the prototype initiative |
| [I01 initiative body](i01-initiative.md) | The local source for issue #10, the production initiative |
| [I00:E00 body](i00-e00.md) | The local source for issue #3, Corpus Harness |
| [I00:E01 body](i00-e01.md) | The local source for issue #4, Walking Skeleton |
| [I00:E02 body](i00-e02.md) | The local source for issue #5, Outline Hierarchy |
| [I00:E03 body](i00-e03.md) | The local source for issue #6, Dependency Closure |
| [I00:E04 body](i00-e04.md) | The local source for issue #7, Destination Identity |
| [I00:E05 body](i00-e05.md) | The local source for issue #8, Validation Gate |
| [I00:E06 body](i00-e06.md) | The local source for issue #9, Corpus Conformance |
| [I01:E00 body](i01-e00.md) | The local source for issue #11, Parser Verdict |
| [I01:E01 body](i01-e01.md) | The local source for issue #12, Source-Range Adapter |
| [I01:E02 body](i01-e02.md) | The local source for issue #13, Profile and Outline |
| [I01:E03 body](i01-e03.md) | The local source for issue #14, Closure and Budgets |
| [I01:E04 body](i01-e04.md) | The local source for issue #15, Destination Identity |
| [I01:E05 body](i01-e05.md) | The local source for issue #16, Validation and Delivery |
| [I01:E06 body](i01-e06.md) | The local source for issue #17, Differential Conformance |
| [I00:E00:W01](i00-e00/w01.md) | The implementation plan for fixture layout and manifest schema |
| [I00:E00:W02](i00-e00/w02.md) | The implementation plan for corpus runner and result comparison |
| [I00:E00:W03](i00-e00/w03.md) | The implementation plan for corpus run on every change |
| [I00:E01:W01](i00-e01/w01.md) | The implementation plan for command interface, streams and exit statuses |
| [I00:E01:W02](i00-e01/w02.md) | The implementation plan for profile configuration and source parsing |
| [I00:E01:W03](i00-e01/w03.md) | The implementation plan for byte-order mark and frontmatter removal |
| [I00:E01:W04](i00-e01/w04.md) | The implementation plan for whole-document emission under a filename heading |
| [I00:E01:W05](i00-e01/w05.md) | The implementation plan for fixtures from unmodified workspace skills |
| [I00:E02:W01](i00-e02/w01.md) | The implementation plan for source heading slugs and duplicate numbering |
| [I00:E02:W02](i00-e02/w02.md) | The implementation plan for eligible section extraction and boundaries |
| [I00:E02:W03](i00-e02/w03.md) | The implementation plan for plus-one heading shift and setext conversion |
| [I00:E02:W04](i00-e02/w04.md) | The implementation plan for heading-only ancestor scaffolding |
| [I00:E02:W05](i00-e02/w05.md) | The implementation plan for heading depth overflow fails |
| [I00:E03:W01](i00-e03/w01.md) | The implementation plan for reference normalization and path identity |
| [I00:E03:W02](i00-e03/w02.md) | The implementation plan for root confinement and no-symlink source access |
| [I00:E03:W03](i00-e03/w03.md) | The implementation plan for link classification and traversal to a fixed point |
| [I00:E03:W04](i00-e03/w04.md) | The implementation plan for selection consolidation and expanded coverage |
| [I00:E03:W05](i00-e03/w05.md) | The implementation plan for self-reference and ancestor-reference classification |
| [I00:E03:W06](i00-e03/w06.md) | The implementation plan for resource budgets fail at the boundary |
| [I00:E04:W01](i00-e04/w01.md) | The implementation plan for custom anchor recognition and alias resolution |
| [I00:E04:W02](i00-e04/w02.md) | The implementation plan for qualified destinations and collision detection |
| [I00:E04:W03](i00-e04/w03.md) | The implementation plan for reference conversion and definition removal |
| [I00:E04:W04](i00-e04/w04.md) | The implementation plan for resource rebasing and the resource base |
| [I00:E05:W01](i00-e05/w01.md) | The implementation plan for candidate validation and provenance invariants |
| [I00:E05:W02](i00-e05/w02.md) | The implementation plan for block boundary safety |
| [I00:E05:W03](i00-e05/w03.md) | The implementation plan for source consistency and generated-input rejection |
| [I00:E05:W04](i00-e05/w04.md) | The implementation plan for diagnostic content and the json format |
| [I00:E06:W01](i00-e06/w01.md) | The implementation plan for adversarial fixture families completed |
| [I00:E06:W02](i00-e06/w02.md) | The implementation plan for clause-to-fixture mapping and the report |
| [I00:E06:W03](i00-e06/w03.md) | The implementation plan for implementation independence check |
| [I01:E00:W01](i01-e00/w01.md) | The implementation plan for definition-occurrence reproducer |
| [I01:E00:W02](i01-e00/w02.md) | The implementation plan for reference-suppression reproducer |
| [I01:E00:W03](i01-e00/w03.md) | The implementation plan for offset-iterator reproducer and version check |
| [I01:E00:W04](i01-e00/w04.md) | The implementation plan for gate report and the recorded route |

## Links

| Resource | Link |
| --- | --- |
| Proposal | https://github.com/m2ux/md-composer/issues/1 |
| I00 Prototype Compiler | https://github.com/m2ux/md-composer/issues/2 |
| I01 Production Compiler | https://github.com/m2ux/md-composer/issues/10 |
| Composition theme board | https://github.com/users/m2ux/projects/18 |
| Proposals board | https://github.com/users/m2ux/projects/16 |
| pulldown-cmark issue #423 | https://github.com/pulldown-cmark/pulldown-cmark/issues/423 |
| pulldown-cmark PR #845 | https://github.com/pulldown-cmark/pulldown-cmark/pull/845 |
| pulldown-cmark issue #1129 | https://github.com/pulldown-cmark/pulldown-cmark/issues/1129 |
