# <img src="docs/images/prosiform-mark.svg" alt="" height="32"> Prosiform

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Profile: skill-markdown-v3](https://img.shields.io/badge/profile-skill--markdown--v3-blue.svg)](https://github.com/m2ux/prosiform/blob/e04d0886c83a10056ff6bdd61eea844765f93a59/artifacts/planning/2026-10-17-prosiform-v1/design.md)
[![CommonMark](https://img.shields.io/badge/CommonMark-based-lightgrey.svg)](https://commonmark.org/)

A deterministic compiler for instruction sets written as linked Markdown. Give it a document or a section; it returns that content and every local Markdown dependency it reaches, as one validated bundle.

---
**[Invocation](invocation.md)** • **[Glossary](docs/glossary.md)** • **[Fixtures](fixtures/README.md)** • **[Docs](docs/README.md)** • **[Examples](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-22-work-planner-compact-diagram/work-planner-compact.review.md)**

---

## 🎯 Overview

Agent skills are authored as collections of linked documents: an entry point links to procedures, and procedures link to the sections that govern them. Reaching the complete context for one operation means resolving that graph at read time. prosiform moves that work into a compilation step, so retrieval stops being part of the reasoning task.

Authors can maintain shared rules in one place and reuse them across procedures. The agent receives the selected material in one continuous document, with repeated content included once and links pointing to the relevant sections. Each bundle is validated before delivery; missing dependencies or invalid content produce an explicit failure. Completeness follows the links authors provide.

### Why?

Leaving retrieval to the agent costs:

* **Missed prerequisites** — a link names a destination; it does not retrieve it
* **Unbounded reads** — linked content in a real skill spans to many documents when read whole
* **No completeness signal** — a prerequisite skipped and one never needed produce the same result
* **Duplicated rules** — shared context gets copied into each document rather than linked once

### How It Works

Diagram example from `example/`, using [my-skill](example/my-skill/SKILL.md).

```bash
cd example/my-skill
pf -o skill-bundle.md procedure.md rules/common.md
```

The Common and Agents files each declare group `rules` and depth `1` in their [conversion metadata](invocation.md#conversion-metadata).

![SKILL.md selects procedure.md and rules/common.md. Procedure includes tips.md; Rules includes rules/agents.md. In skill-bundle.md, arrows connect the Tips and Agents links to their bundled sections. The bundle groups Common and Agents beneath Rules; Agents directs each harness to its deferred Codex or Claude rules. SKILL.md and the harness-specific rules are excluded.](docs/images/compilation.png)

## Installation

Requires Python 3.13+ on Linux or macOS. From the repository root:

```bash
pip install ./src
pf -v
```
## Usage

Run these from the repository root. One entry writes its bundle to an entry-derived filename in the working directory. Pass `-o -` to write that bundle to standard output. File and directory names use hyphens rather than underscores.

### Bundle a Source and its Dependencies

```bash
pf example/work-planner/modes/plan-mode.md
```

### Compile a Selected Section

```bash
pf 'example/work-planner/artifacts/epic.md#delivery-findings'
```
