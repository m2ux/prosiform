# <img src="docs/images/prosiform-mark.svg" alt="" height="32"> Prosiform

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Profile: prosiform-markdown](https://img.shields.io/badge/profile-prosiform--markdown-blue.svg)](https://github.com/m2ux/prosiform/blob/2f8d860e8/artifacts/planning/2026-10-17-prosiform-v1/design.md)
[![CommonMark](https://img.shields.io/badge/CommonMark-based-lightgrey.svg)](https://commonmark.org/)

A deterministic compiler for instruction sets written as linked Markdown. Give it a document or a section; it returns that content and the linked sources it reaches as validated bundles.

---
**[Invocation](invocation.md)** • **[Architecture](docs/architecture.md)** • **[Glossary](docs/glossary.md)** • **[Fixtures](fixtures/README.md)** • **[Docs](docs/README.md)** • **[Examples](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-22-work-planner-compact-diagram/work-planner-compact.review.md)**

---

## 🎯 Overview

Agent skills are authored as collections of linked documents: an entry point links to procedures, and procedures link to the sections that govern them. Reaching the complete context for one operation means resolving that graph at read time. prosiform moves that work into a compilation step, so retrieval stops being part of the reasoning task.

Authors can maintain shared rules in one place and reuse them across procedures. The agent receives the selected material in one continuous document, with repeated content included once and links pointing to the relevant sections. Each bundle is validated before publication; invalid content produces an explicit failure. Completeness follows the links to declared sources.

### Why?

Leaving retrieval to the agent costs:

* **Missed prerequisites** — a link names a destination; it does not retrieve it
* **Unbounded reads** — linked content in a real skill spans to many documents when read whole
* **No completeness signal** — a prerequisite skipped and one never needed produce the same result
* **Duplicated rules** — shared context gets copied into each document rather than linked once

### How It Works

One run turns `SKILL.md` and its linked procedure and rules into one bundle. [Bundles](docs/bundles.md) walks through the example.

![A source tree and SKILL.md select Review Mode. Arrows trace its two Rules links to one Tests section. The compiled bundle contains Work Planner, Review Mode and the test rules once, with every link pointing to its heading inside the bundle.](docs/images/run.svg)

## Installation

Requires Python 3.13+ on Linux or macOS. From the repository root:

```bash
pip install ./src
pf -v
```

## Usage

Sources declare `prosiform` in [YAML frontmatter](docs/sources.md#frontmatter). Run `pf` with no arguments for the agent guide. Each run writes a `.bundles` folder containing the entry's bundle and any dispatched bundles; [Invocation](invocation.md) covers options and output names.

A link such as `[Review](rules.md#tests "checks,draft")` selects the target document's `checks` and `draft` presets above its `default`. Compile that occurrence with `pf rules.md#tests --presets checks,draft`, resolving the destination from the document carrying the link. Headings and link labels select no presets. [Selection](docs/selection.md#presets-in-force) states normalization and layering; [Invocation](invocation.md#examples) covers shell quoting and later compilation of deferred links; [Bundles](docs/bundles.md#derived-names) explains the filenames that distinguish dispatched selections.

Start each example below from the repository root. Both use source trees from the [fixture corpus](fixtures/README.md). File and directory names use hyphens rather than underscores.

### Bundle a Source and its Dependencies

```bash
cd fixtures/dispatch/a-dispatched-target-is-a-bundle-of-its-own/source
pf guide.md
```

### Compile a Selected Section

```bash
cd fixtures/extraction/section-to-the-next-sibling/source
pf 'guide.md#run'
```
