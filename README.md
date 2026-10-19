# 🧩 prosiform

[![Status: building](https://img.shields.io/badge/status-building-orange.svg)](https://github.com/users/m2ux/projects/18)
[![Profile: skill-markdown-v1](https://img.shields.io/badge/profile-skill--markdown--v1-blue.svg)](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md)
[![CommonMark](https://img.shields.io/badge/CommonMark-based-lightgrey.svg)](https://commonmark.org/)

A deterministic compiler for instruction sets written as linked Markdown. Give it a document or a section; it returns that content and every local Markdown dependency it reaches, as one validated bundle.

---

**[Design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md)** • **[Glossary](docs/glossary.md)** • **[Plan](https://github.com/users/m2ux/projects/18)** • **[Proposal](https://github.com/m2ux/prosiform/issues/1)** • **[Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1)**

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
2. **Discover** — supported local Markdown links are followed to a fixed point
3. **Consolidate** — overlapping selections merge, so each region appears exactly once
4. **Arrange** — regions are emitted into groups, source headings shifting one level beneath the heading that names their group
5. **Rewrite** — every reference is repointed at the fragment a renderer generates for the heading it now names
6. **Validate** — the candidate is reparsed and checked against what was selected; nothing reaches stdout until it passes

### Architecture

```
References → Closure → Consolidation → Grouping → Rewriting → Validation → Bundle
```

- **Reference** — a document, or a document and a section fragment
- **Section** — a document-level heading and its subsections; the smallest unit a reference can select
- **Closure** — every local Markdown document reachable by link from the selection
- **Group** — a top-level division of the bundle: one source document by default, or one merged directory
- **Destination** — the fragment a renderer generates for an emitted heading, which is what every rewritten reference names
- **Bundle** — the single validated Markdown document one run produces
- **Profile** — `skill-markdown-v1`: CommonMark with pipe tables, strikethrough and preserved task markers; no typographic substitution

Every term the contract uses is defined once, in the [glossary](docs/glossary.md), which ships with the tool.

## 🗂️ Repository Layout

Three trees, each created by the stage that writes into it.

| Tree | Holds |
| --- | --- |
| [`fixtures/`](fixtures/README.md) | The language-neutral corpus and the contract it encodes. Both builds run it. |
| [`prototype/`](prototype/README.md) | The Python build: the contract's first implementation, retained as a differential oracle. |
| [`docs/`](docs/README.md) | The documentation this repository owns, the [glossary](docs/glossary.md) among it. |
| [`checks/`](checks/README.md) | The checks that hold the layout, every document's references, the README tables, and the glossary's coverage true. |

The production build's tree is created by the initiative that writes that build. The design and the planning record stay on the [engineering branch](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) and are reached by link, so there is one copy of each.

## ✅ Checks

Every check is a named command. Continuous integration runs these same names, so a check cannot hold on a working copy and be absent remotely.

```bash
make check
```

| Command | Asserts |
| --- | --- |
| `make lock-check` | The lockfile describes the dependency list the project definition declares. |
| `make lint` | The repository's Python carries no lint error. |
| `make format-check` | That same Python is formatted as the declared configuration formats it. |
| `make typecheck` | That same Python type checks in strict mode. |
| `make test` | The Python build's suite passes. A run that collects no test fails. |
| `make corpus` | Every fixture the corpus holds matches the [manifest schema](fixtures/README.md), each catalogue of diagnostic codes is the set the design declares, and the runner decides a fixture from its manifest and files alone. |
| `make layout` | Each of the three trees holds a tracked file. |
| `make tables` | The command and dependency tables in these READMEs name every target the [`Makefile`](Makefile) declares and every dependency [`prototype/pyproject.toml`](prototype/README.md) declares, and nothing besides. |
| `make links` | Every reference every document in this repository carries resolves, the fixture corpus excepted. |
| `make vocabulary` | The [glossary](docs/glossary.md) defines every contract term the design marks. |
| `make check` | All of the above, in the order listed, stopping at the first failure. |

The tools the first six call are pinned by [`prototype/uv.lock`](prototype/README.md); `make layout`, `make tables`, `make links` and `make vocabulary` are standard-library scripts in [`checks/`](checks/README.md). `make links` reaches addresses outside this repository, so it needs network access and GitHub credentials.

## 📦 Installation

prosiform installs from the Python build in [`prototype/`](prototype/README.md):

```bash
pip install ./prototype
```

A working copy takes its environment from the lockfile, which records the exact version of every dependency a checkout installs:

```bash
cd prototype
uv sync --frozen
```

Installing the build puts the `prosiform` command on the path and ships the [glossary](docs/glossary.md) with the package. The status table below tracks the stage the build sits in.

## 🚀 Invocation

The command answers to every option the contract declares, and `prosiform --help` reports them with their defaults and the exit statuses below. Bundling is the stage under it, and the walking skeleton is building it now: a run reads and parses every source its entry references name under the `skill-markdown-v1` profile, so a source carrying raw HTML or an unsupported dependency or section-naming construct returns `1` naming the construct and where it sits, and a source the profile accepts returns `4`, which says this build cannot carry the request out rather than that the source it names is at fault.

```bash
# A procedure and everything it reaches. The routing document the caller read
# to find it, SKILL.md, is not an entry reference and is not bundled.
prosiform --root skills/work-planner modes/plan-mode.md

# Selected sections
prosiform --root skills/work-planner 'artifacts/epic.md#delivery-findings'

# Every document under a named directory merged at a heading level
prosiform --root skills/work-planner \
  --group artifacts:2 --group modes:2 \
  modes/plan-mode.md

# Compile and validate without publishing
prosiform --root skills/work-planner --check modes/plan-mode.md
```

Standard output carries exactly one thing per run: the bundle a compiling run publishes, the response an informational run returns, or nothing at all. Diagnostics go to standard error, as text for a reader or, under `--diagnostics json`, as one JSON object per line and nothing else. A bundle opens by naming what it was built for, so the caller reaches its procedure without searching:

```markdown
This bundle was built for [Plan Mode](#plan-mode); everything else is material it references.
```

A failed run publishes nothing. The caller halts and surfaces the diagnostic rather than reading the sources itself.

| Exit | Meaning |
| --- | --- |
| `0` | Compiled, validated, published |
| `1` | Input, dependency, policy, safety or resource-limit failure |
| `2` | Invalid usage or option combination |
| `3` | Publication or delivery failure |
| `4` | Unexpected internal error |

## 📏 Measured

One procedure of this workspace's `work-planner` skill, bundled under the v1 rules:

| | Read whole | Bundled |
| --- | --- | --- |
| Documents | 27 | 27 |
| Bytes | 239,331 | 187,594 |
| References resolved by the reader | 421 | 0 |

Rendered by GitHub, all 775 fragment links on the page resolve against the 353 anchors it generates, none broken. The same closure merged into three groups is 306 headings and 186,907 bytes, and rewrites the same 421 references.

## 🗺️ Status

Three stages, in order. Progress is on the **[Bundling board](https://github.com/users/m2ux/projects/18)**.

| Stage | Delivers | State |
| --- | --- | --- |
| **[I00 Prototype](https://github.com/m2ux/prosiform/issues/2)** | A Python build, a language-neutral fixture corpus, and the tool installed for agents to invoke | In Progress |
| **[I01 Field Refinement](https://github.com/m2ux/prosiform/issues/20)** | The specification settled by real use, frozen at a tagged revision | Ready |
| **[I02 Production](https://github.com/m2ux/prosiform/issues/10)** | A Rust build implementing that revision, with the prototype retained as its differential oracle | Planned |

The fixture corpus is the contract: it declares each case as a source tree, an invocation and an expected result, so it binds any implementation rather than describing one.

## 📐 Scope

prosiform bundles explicitly linked local Markdown. It does **not** execute or authorize the procedures it bundles, infer dependencies the source did not state as links, fetch remote documents, bundle non-Markdown resources, or accept its own output as input.
