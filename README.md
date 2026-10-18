# 🧩 md-compose

[![Status: planning](https://img.shields.io/badge/status-planning-orange.svg)](https://github.com/users/m2ux/projects/18)
[![Profile: skill-markdown-v1](https://img.shields.io/badge/profile-skill--markdown--v1-blue.svg)](https://github.com/m2ux/md-composer/blob/engineering/artifacts/planning/2026-10-17-md-compose-v1/design.md)
[![CommonMark](https://img.shields.io/badge/CommonMark-based-lightgrey.svg)](https://commonmark.org/)

A deterministic compiler for instruction sets written as linked Markdown. Give it a document or a section; it returns that content and every local Markdown dependency it links to, as one validated document — or it publishes nothing and says why.

---

**[Design](https://github.com/m2ux/md-composer/blob/engineering/artifacts/planning/2026-10-17-md-compose-v1/design.md)** • **[Plan](https://github.com/users/m2ux/projects/18)** • **[Proposal](https://github.com/m2ux/md-composer/issues/1)** • **[Planning record](https://github.com/m2ux/md-composer/tree/engineering/artifacts/planning/2026-10-17-md-compose-v1)**

---

## 🎯 Overview

Agent skills are authored as collections of linked documents: an entry point links to procedures, and procedures link to the sections that govern them. Reaching the complete context for one operation means resolving that graph at read time. md-compose moves that work into a compilation step, so retrieval stops being part of the reasoning task.

### Why?

Leaving retrieval to the agent costs:

* **Missed prerequisites** — a link names a destination; it does not retrieve it
* **Unbounded reads** — one procedure in a real skill reaches 39 documents and 318,018 bytes when read whole
* **No completeness signal** — a prerequisite skipped and one never needed produce the same result
* **Duplicated rules** — shared context gets copied into each document rather than linked once

### How It Works

1. **Resolve** — entry references normalize to source identities confined to an allowed root
2. **Discover** — supported local Markdown links are followed to a fixed point
3. **Consolidate** — overlapping selections merge, so each region appears exactly once
4. **Compose** — source headings shift one level beneath a heading naming their file; references are rewritten to internal destinations
5. **Validate** — the candidate is reparsed and checked against what was selected; nothing reaches stdout until it passes

### Architecture

```
References → Closure → Consolidation → Composite → Validation → stdout
```

- **Reference** — a document, or a document and a section fragment
- **Section** — a document-level heading and its subsections; the smallest unit that can be selected
- **Closure** — every local Markdown document reachable by link from the selection
- **Composite** — one Markdown document, carrying one generated heading per contributing file
- **Profile** — `skill-markdown-v1`: CommonMark with pipe tables, strikethrough and preserved task markers; no typographic substitution

## 🚀 Quick Start

Nothing is built yet. The behavioural contract is specified and the work is planned — this is the interface that contract defines.

```bash
# A whole document and everything it links to
md-compose --root skills/work-planner SKILL.md

# Selected sections
md-compose --root skills/work-planner 'artifacts/epic.md#delivery-findings'

# Compile and validate without publishing
md-compose --root skills/work-planner --check SKILL.md
```

Composed Markdown goes to stdout and diagnostics to stderr. A failed composition publishes nothing; the caller halts and surfaces the diagnostic rather than reading the sources itself.

| Exit | Meaning |
| --- | --- |
| `0` | Compiled, validated, published |
| `1` | Input, dependency, policy, safety or resource-limit failure |
| `2` | Invalid usage or option combination |
| `3` | Publication or delivery failure |
| `4` | Unexpected internal error |

## 🗺️ Status

Three stages, in order. Progress is on the **[Composition board](https://github.com/users/m2ux/projects/18)**.

| Stage | Delivers | State |
| --- | --- | --- |
| **[I00 Prototype](https://github.com/m2ux/md-composer/issues/2)** | A Python build, a language-neutral fixture corpus, and the tool installed for agents to invoke | Planned |
| **[I01 Field Refinement](https://github.com/m2ux/md-composer/issues/20)** | The specification settled by real use, frozen at a tagged revision | Planned |
| **[I02 Production](https://github.com/m2ux/md-composer/issues/10)** | A Rust build implementing that revision, with the prototype retained as its differential oracle | Planned |

The fixture corpus is the contract: it declares each case as a source tree, an invocation and an expected result, so it binds any implementation rather than describing one.

## 📐 Scope

md-compose composes explicitly linked local Markdown. It does **not** execute or authorize the procedures it composes, infer dependencies the source did not state as links, fetch remote documents, bundle non-Markdown resources, or accept its own output as input.
