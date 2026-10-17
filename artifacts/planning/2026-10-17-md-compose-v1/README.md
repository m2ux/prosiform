# md-compose v1 — October 2026

> Initiative Plan · Created 2026-10-17

## Executive Summary

md-compose compiles a set of linked local Markdown documents into one continuous, validated Markdown document. Agent skills in this workspace are authored as modular instruction sets: a skill entry point links to modes, modes link to artifacts, and artifacts link to one another's sections. Reaching the complete context for one operation currently means the agent resolves that graph itself, deciding which sections to read, where each section ends, and when the closure is complete. md-compose moves that retrieval into a deterministic compilation step that either returns the whole composite or fails with a diagnostic.

The work is partitioned by solution maturity. A Python 3 prototype implements the behavioural contract and produces a language-neutral fixture corpus of exact expected composites; it is retained as a differential oracle rather than discarded. A Rust implementation then delivers production md-compose against that same corpus, opening with an empirical verdict on two parser viability gates that `pulldown-cmark` may not satisfy. The corpus is the contract, so neither implementation is the specification of the other.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Design](design.md) | The approved v1 behavioural contract: input/output, profile, extraction, anchors, validation and limits |
| [Upstream Assessment](upstream-assessment.md) | The inspected state of `pulldown-cmark` and two narrowly scoped contributions, deferred and unauthorized |
| [Decisions](decisions.md) | The planning decisions taken with the user and the reasoning behind each |

## Links

| Resource | Link |
| --- | --- |
| pulldown-cmark issue #423 | https://github.com/pulldown-cmark/pulldown-cmark/issues/423 |
| pulldown-cmark PR #845 | https://github.com/pulldown-cmark/pulldown-cmark/pull/845 |
| pulldown-cmark issue #1129 | https://github.com/pulldown-cmark/pulldown-cmark/issues/1129 |
