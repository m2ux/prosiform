# 🧩 prosiform

[![Profile: skill-markdown-v1](https://img.shields.io/badge/profile-skill--markdown--v1-blue.svg)](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md)
[![CommonMark](https://img.shields.io/badge/CommonMark-based-lightgrey.svg)](https://commonmark.org/)

A deterministic compiler for instruction sets written as linked Markdown. Give it a document or a section; it returns that content and every local Markdown dependency it reaches, as one validated bundle.

---

**[Installation](installation.md)** • **[Invocation](invocation.md)** • **[Checks](checks.md)** • **[Design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md)** • **[Glossary](docs/glossary.md)** • **[Fixtures](fixtures/README.md)** • **[Source](src/README.md)** • **[Docs](docs/README.md)** • **[Check implementation](checks/README.md)** • **[Example](example/README.md)**

---

## 🎯 Overview

Agent skills are authored as collections of linked documents: an entry point links to procedures, and procedures link to the sections that govern them. Reaching the complete context for one operation means resolving that graph at read time. prosiform moves that work into a compilation step, so retrieval stops being part of the reasoning task.

### Why?

Leaving retrieval to the agent costs:

* **Missed prerequisites** — a link names a destination; it does not retrieve it
* **Unbounded reads** — one procedure in a real skill reaches 39 documents and 318,018 bytes when read whole
* **No completeness signal** — a prerequisite skipped and one never needed produce the same result
* **Duplicated rules** — shared context gets copied into each document rather than linked once

### How It Works

1. **Resolve** — entry references normalize to source identities confined to an allowed root
2. **Discover** — supported local Markdown links under the allowed root are followed to a fixed point; one its author defers is confirmed and left to a run of its own
3. **Consolidate** — overlapping selections merge, so each region appears exactly once
4. **Arrange** — regions are emitted into groups, source headings shifting one level beneath the heading that names their group
5. **Rewrite** — every compiled reference is repointed at the fragment a renderer generates for the heading it now names, and a deferred one at its target's path from the root
6. **Validate** — the candidate is reparsed and checked against what was selected; nothing reaches stdout until it passes

### Architecture

```
References → Closure → Consolidation → Grouping → Rewriting → Validation → Bundle
```

- **Reference** — a document, or a document and a section fragment
- **Section** — a document-level heading and its subsections; the smallest unit a reference can select
- **Closure** — every local Markdown document reachable by link from the selection
- **Deferral** — a reference whose link text opens with `¬`: this run confirms its target and compiles it nowhere, and the bundle carries the mark as written
- **Group** — a top-level division of the bundle: one source document by default, or one merged directory
- **Destination** — the fragment a renderer generates for an emitted heading, which is what every rewritten reference names
- **Bundle** — the single validated Markdown document one run produces
- **Profile** — `skill-markdown-v1`: CommonMark with pipe tables, strikethrough and preserved task markers; no typographic substitution

Every term the contract uses is defined once, in the [glossary](docs/glossary.md), which ships with the tool.
