# 🧩 prosiform

[![Profile: skill-markdown-v1](https://img.shields.io/badge/profile-skill--markdown--v1-blue.svg)](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md)
[![CommonMark](https://img.shields.io/badge/CommonMark-based-lightgrey.svg)](https://commonmark.org/)

A deterministic compiler for instruction sets written as linked Markdown. Give it a document or a section; it returns that content and every local Markdown dependency it reaches, as one validated bundle.

---

**[Design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md)** • **[Glossary](docs/glossary.md)**

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

Every term the contract uses is defined once, in the [glossary](docs/glossary.md), which ships with the tool. The words the corpus's own declarations add to it — the English a sentence is written in, the names Markdown and its encodings carry — are registered in the [corpus vocabulary](docs/corpus-vocabulary.md), and the independence check reports a declaration stating a word neither source holds.

## 🗂️ Repository Layout

Each tree holds one kind of thing.

| Tree | Holds |
| --- | --- |
| [`fixtures/`](fixtures/README.md) | The language-neutral corpus and the contract it encodes. The build runs it. |
| [`src/`](src/README.md) | The Python build, which the corpus holds to the contract. |
| [`docs/`](docs/README.md) | The documentation this repository owns, the [glossary](docs/glossary.md) among it. |
| [`checks/`](checks/README.md) | The checks that hold the layout, every document's references, the README tables, and the glossary's coverage true. |
| [`example/`](example/README.md) | The example skill tree the design's usage examples name, which the corpus bundles through each of them. |

The fixture corpus is the contract: it declares each case as a source tree, an invocation and an expected result, so it binds any implementation rather than describing one. The design stays on the [engineering branch](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md) and is reached by link, so there is one copy of it.

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
| `make harness` | Every fixture the corpus holds matches the [manifest schema](fixtures/README.md), each catalogue of diagnostic codes is the set the design declares, and the runner decides a fixture from its manifest and files alone. |
| `make corpus` | Every fixture the corpus holds, run against the build under test, produces the result its manifest declares. A fixture declaring work a later epic delivers is reported as awaiting it; one that meets its manifest while awaiting fails, as does a run with no build configured. |
| `make smoke` | The build installs into an environment and its entry point bundles a reference from a source root, resolved by name from a directory unrelated to this repository. |
| `make layout` | Each of the three trees holds a tracked file. |
| `make tables` | The command and dependency tables in these READMEs name every target the [`Makefile`](Makefile) declares and every dependency [`src/pyproject.toml`](src/README.md) declares, and nothing besides. |
| `make links` | Every reference every document in this repository carries resolves, the fixture corpus excepted. |
| `make vocabulary` | The [glossary](docs/glossary.md) defines every contract term the design marks. |
| `make invocation` | The documented invocation names every argument and exit status the build under test reports for itself, and nothing besides, each reproducing that build's own help output. |
| `make conformance` | Each behavioural clause of the design carries the fixtures exercising it, each clause no fixture reaches is listed as uncovered, each clause no source tree and invocation can state is recorded as unfixturable with the reason and what states it instead, each section of the design that states no behaviour is declared as such and carries no clause, and each error code, warning code and exit status the contract declares is listed with the fixtures reaching it, one only an awaiting fixture declares named unfixturable with the work it awaits, each installation claim no run of the corpus observes listed as unfixturable with the reason it is unreachable and the smoke-run property that would observe it, and the codes the build under test reports for itself are exactly the codes the contract declares. It fails without a build configured. |
| `make independence` | Every word a fixture declaration states and every word the conformance report prints is one the contract's vocabulary holds: the design's own words and clause names, the terms the [glossary](docs/glossary.md) defines, the names the contract declares as its interface, and the [corpus vocabulary](docs/corpus-vocabulary.md). It renders the conformance report, so it fails without a build configured. |
| `make check` | All of the above, in the order listed, stopping at the first failure. |

The tools the first seven call are pinned by [`src/uv.lock`](src/README.md), and `make conformance` and `make independence` read the corpus through the same manifest reader and the build through the same runner, so they run from that environment too; `make smoke`, `make layout`, `make tables`, `make links` and `make vocabulary` are standard-library scripts in [`checks/`](checks/README.md). `make smoke` builds and installs the wheel through `uv` and needs network access for the dependencies the wheel declares. `make links` reaches addresses outside this repository, so it needs network access and GitHub credentials.

`make conformance` reads the design, the corpus and the codes the build under test reports for itself, so the coverage it reports and the comparison it makes are both read from the contract and the build rather than from either alone. `make independence` reads those same three and the report between them, and holds what the corpus binds to the behaviour the design states rather than to the build that happens to be written beside it. `make corpus`, `make invocation`, `make conformance` and `make independence` run a build named by configuration rather than one they choose, so one corpus, one documented invocation and one declared surface bind every implementation of the contract. `PROSIFORM_BUILD` holds that build's command line, split as a shell splits one, and a corpus run resolves it from the fixture's own directory:

```bash
export PROSIFORM_BUILD="uv run --project $PWD/src --frozen prosiform"
```

There is no default and no fallback: with nothing configured the run fails rather than passing over the corpus, because a corpus run that skips sits inside a passing suite saying nothing.

## 📦 Installation

prosiform installs from the Python build in [`src/`](src/README.md):

```bash
pip install ./src
```

A working copy takes its environment from the lockfile, which records the exact version of every dependency a checkout installs:

```bash
cd src
uv sync --frozen
```

Installing the build puts the `prosiform` command on the path and ships the [glossary](docs/glossary.md) with the package, so an installed build carries the vocabulary its diagnostics use. The command is the entry point every caller depends on, and three properties are what make it one:

- **Named on the path.** The installation puts the one documented name in the environment's executable directory, so a caller writes `prosiform` and resolves nothing for itself.
- **Independent of the working directory.** A run's outcome follows from its options and the source root they name, and from nothing about where the process was started.
- **Independent of this repository.** The installed build reads nothing out of the tree it was built from, and the source root a caller names is the caller's own.

`make smoke` holds all three on every change: it builds the wheel, installs it into a throwaway environment, and bundles a reference from a source root outside this repository with the command resolved by name from a directory unrelated to it. `prosiform --version` reports the installed version and the `skill-markdown-v1` profile the build implements. The status table below tracks the stage the build sits in.

## 🚀 Invocation

The command answers to every option the contract declares, and `prosiform --help` reports them with their defaults and the exit statuses. The tables in this section reproduce that output word for word, and `make invocation` holds each row to the help the build under test prints, so the invocation a caller reads here and the one the command offers cannot drift apart.

| Option | Effect |
| --- | --- |
| `REF` | an entry reference: a root-relative document, a document and a fragment, or a fragment alone with --from |
| `--root DIR` | the allowed source root; required, and resolved from the working directory |
| `--from DOC` | the root-relative referring document a fragment-only reference resolves against |
| `-o, --output FILE` | publish the validated bundle to FILE, atomically; default or - is standard output |
| `--group SLUG:DEPTH` | merge every document under a directory named SLUG at source heading level DEPTH, 1 through 6; repeatable, once per slug |
| `--check` | discover, bundle and validate without emitting or publishing the bundle; accepted with --output |
| `--diagnostics {text,json}` | the diagnostic format on standard error; default text |
| `--fault {source-changed,internal}` | perform a fault on the run itself, so a conformance run reaches an outcome no source tree states; none by default |
| `--max-files N` | the budget of distinct source documents opened; a positive decimal integer, default 256 |
| `--max-file-bytes N` | the budget of raw bytes in one source; a positive decimal integer, default 1048576 |
| `--max-input-bytes N` | the budget of raw source bytes, counted once per source; a positive decimal integer, default 16777216 |
| `--max-output-bytes N` | the budget of bytes of the complete bundle; a positive decimal integer, default 262144 |
| `--max-targets N` | the budget of distinct document and section targets discovered; a positive decimal integer, default 4096 |
| `--max-links N` | the budget of authored link and image occurrences in selected content; a positive decimal integer, default 32768 |
| `--max-nesting N` | the budget of levels of container nesting in one source; a positive decimal integer, default 64 |
| `--max-expansion-depth N` | the budget of link hops from the nearest entry reference; a positive decimal integer, default 8 |
| `--codes` | report the error and warning codes this build can emit |
| `--version` | report the tool version and the profile identifier |
| `--help` | show this usage, the defaults, and the exit-status meanings |

Each effect is that argument's own help text, so the default an option carries is stated where the option is. A budget is a positive decimal integer; zero is refused rather than read as unlimited.

Bundling runs under it: a run reads every source its entry references name, requires it to be valid UTF-8, removes the one leading byte-order mark and the one leading frontmatter block it may carry ahead of its content, parses what is left under the `skill-markdown-v1` profile, selects the whole document or the section each reference names, and publishes each contributing document as one file group headed by that document's root-relative path. It then follows the dependencies its selected content carries — a link resolving to a Markdown document under the allowed source root — resolving each against the document carrying it and bundling what it reaches, until a round of the traversal reaches nothing new. A link resolving outside that root is a citation: it is emitted as its author wrote it and carries no document into the bundle. A source that is not valid UTF-8, one whose frontmatter opener no later line closes, one carrying raw HTML or an unsupported dependency or section-naming construct, two documents whose paths differ only by Markdown extension, and a reference under the root naming no document or no heading in the document it resolves to each return `1` naming the defect and the line of the file it sits on. A compiled link reaches the bundle with its destination repointed at the heading the bundle emits for what it named.

One mark says otherwise, and it defers a compilation rather than asking for one. A link whose text opens with `¬` is not compiled by this run: its target is confirmed to exist and carried nowhere, so the document it names is neither opened nor bundled through it. The bundle emits the link's text with its mark exactly as the author wrote it, the spaces following the character included, and gives the link its target's path from the allowed source root as its destination, so the agent reading the bundle needs that root and nothing else to compile it in a run of its own. A deferred reference naming no document, or no heading in the document it resolves to, fails like any other the root makes this run responsible for.

```bash
# A procedure and everything it reaches. The routing document the caller read
# to find it, SKILL.md, is not an entry reference and is not bundled.
prosiform --root example/work-tracker modes/plan-mode.md

# Selected sections
prosiform --root example/work-tracker 'artifacts/epic.md#delivery-findings'

# Every document under a named directory merged at a heading level
prosiform --root example/work-tracker \
  --group artifacts:2 --group modes:2 \
  modes/plan-mode.md

# Compile and validate without publishing
prosiform --root example/work-tracker --check modes/plan-mode.md
```

Standard output carries exactly one thing per run: the bundle a compiling run publishes, the response an informational run returns, or nothing at all. Diagnostics go to standard error, as text for a reader or, under `--diagnostics json`, as one JSON object per line and nothing else. A bundle opens by naming what it was built for, so the caller reaches its procedure without searching:

```markdown
This bundle was built for [modes/plan-mode](#modesplan-mode); everything else is material it references.
```

### Exit statuses

A run returns the status naming the category of its outcome, and a caller reads the result from that status rather than from what reached standard output.

| Exit | Meaning |
| --- | --- |
| `0` | successful compilation, validation, or informational response |
| `1` | input, dependency, policy, safety, or resource-limit failure |
| `2` | invalid usage or option combination |
| `3` | output publication or delivery failure, a broken pipe among them |
| `4` | unexpected internal error |

### A failed run stops the work

A failed run publishes nothing. The caller halts and surfaces the diagnostic, and reading the sources itself is unsupported: there is no option, no status and no documented path by which a caller meeting a failure resolves the closure for itself. A fallback restores the behaviour bundling replaces, and restores it silently, so the failure teaches nothing and the next run fails the same way.

### Supported environment

The supported environment is POSIX: Linux and macOS. The confinement of a run to its allowed source root rests on rooted, no-follow source access, which descends a path one segment at a time through the `O_NOFOLLOW`, `O_DIRECTORY` and `O_CLOEXEC` open flags, so a source reached through a symbolic link below the root is refused by the open rather than by a string comparison ahead of it. A platform offering no such flags cannot enforce that policy, and the build refuses to start there rather than weakening the confinement to a check on the spelling of a path.

## 📏 Measured

One procedure of this workspace's `work-planner` skill, bundled under the v1 rules:

| | Read whole | Bundled |
| --- | --- | --- |
| Documents | 27 | 27 |
| Bytes | 239,331 | 187,594 |
| References resolved by the reader | 421 | 0 |

Rendered by GitHub, all 775 fragment links on the page resolve against the 353 anchors it generates, none broken. The same closure merged into three groups is 306 headings and 186,907 bytes, and rewrites the same 421 references.

## 📐 Scope

prosiform bundles the local Markdown its sources link under one allowed source root. It does **not** execute or authorize the procedures it bundles, follow a reference resolving outside that root, fetch remote documents, bundle non-Markdown resources, or accept its own output as input.
