# <img src="docs/images/prosiform-mark.svg" alt="" height="32"> Prosiform

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Profile: skill-markdown-v4](https://img.shields.io/badge/profile-skill--markdown--v4-blue.svg)](https://github.com/m2ux/prosiform/blob/513a9e9f6d99b2a69007bebc425a425b0c4a589b/artifacts/planning/2026-10-17-prosiform-v1/design.md)
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
pf procedure.md rules/common.md
```

The Common and Agents files each declare group `rules` and depth `1`.

![SKILL.md selects procedure.md and rules/common.md. Procedure includes tips.md; Rules includes rules/agents.md. In the bundle, procedure+rules_common.bundle.md, arrows connect the Tips and Agents links to their bundled sections. The bundle groups Common and Agents beneath Rules; Agents directs each harness to its deferred Codex or Claude rules. SKILL.md and the harness-specific rules are excluded.](docs/images/compilation.png)

## Installation

Requires Python 3.13+ on Linux or macOS. From the repository root:

```bash
pip install ./src
pf -v
```
## Usage

Run these from the repository root. A run writes its bundles into a folder of its own, named for its entry with the `.bundles` suffix, in the working directory or in the existing folder `-o` names: the entry's bundle under its derived name, and a bundle for each target its dispatches reach. Several entries join their names with `+`. The folder is written whole and swapped in, so a reader sees one run's bundle set and never a mixture of two. File and directory names use hyphens rather than underscores.

### Print the Guide

```bash
pf
```

With no arguments, `pf` prints the guide an agent follows a skill by: the compile step, the rule that a link whose text opens with `↳` names an inline target to compile, read whole and follow, and that a bundle opening with a Prosiform section is followed from there. A skill's bootstrap is one instruction: run `pf` and follow it.

### Bundle a Source and its Dependencies

```bash
pf example/work-planner/modes/plan-mode.md
```

### Compile a Selected Section

```bash
pf 'example/work-planner/artifacts/epic.md#delivery-findings'
```

### Dispatch to Sub-agents

A link whose text opens with `⇉` dispatches its target, as Plan Mode's link to Sync Mode does in the first run above. The run compiles that target, and each target it dispatches in turn, as a bundle of its own in the same folder. The link points at a `Dispatch <link text>` sub-section one level below its section, whose one line names the bundle to hand to a sub-agent. The `⫽` links in one section's own content form a parallel set, pointing at one `Dispatch in parallel` sub-section that lists the bundles to dispatch together.

A bundle that dispatches opens with a `# Prosiform` section stating how: `## Dispatch` whenever it dispatches, and `## Parallel dispatch` when it carries a set. Each sub-section links the protocol it follows, and the protocols are the same bytes in every bundle.
