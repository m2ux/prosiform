## Overview

A Python 3 build of prosiform compiles one or more local Markdown document or section references into one continuous, validated Markdown document, and a language-neutral fixture corpus states what that document must be. The corpus declares each case as a source tree, an invocation and an expected result, so it binds any implementation rather than describing this one. The repository is laid out, its environment pinned and its checks runnable before the first of that work lands. The build installs as the tool agents in this workspace invoke, with a wrapper that delivers a bundle whole or reports a delivery failure. The initiative is complete when the corpus covers every behavioural clause of the design, the Python build passes it, and an agent bundles by invoking the installed tool.

## Problem

Modular Markdown authoring separates the destination a link names from the context an operation needs, and nothing closes that gap except the reading agent.

- **Retrieval is prose the agent must execute.**
  One rule directs the agent to read a linked section and its subsections, stop before the next heading of equal or higher level, read that file's prerequisites first, preserve boundaries in batched reads and recover truncated output: [Linked sections](https://github.com/m2ux/prosiform/blob/acac85867ca963df00251e4cf00a4db11b14bf24/skills/work-planner/SKILL.md#L71-L72).

- **One request reaches 39 documents.**
  [Plan Mode](https://github.com/m2ux/prosiform/blob/acac85867ca963df00251e4cf00a4db11b14bf24/skills/work-planner/modes/plan-mode.md#L5-L23) lists 15 prerequisites; the transitive closure of its Markdown links is 39 files and 139 distinct section targets, 318,018 bytes read whole.

- **Section boundaries are decided by the reader.**
  519 Markdown links run between the 38 files of that one skill, 363 of them naming a section rather than a file, so each read also decides where the named section ends.

- **Nothing establishes the context was complete.**
  A prerequisite the agent skipped and one it never needed produce the same result: an operation that proceeds.

- **A behavioural contract with no executable form binds nothing.**
  The design states its invariants in prose. Prose cannot report that an implementation violates one.

## Proposal

- **The corpus is the contract.**
  Each fixture declares a source tree, an invocation and the exact expected bundle, exit status and diagnostics. A runner decides pass or fail from the declaration alone, naming no implementation.

- **Python proves the semantics.**
  Dependency closure, overlap consolidation, destination identity and the post-compilation invariants are parser-independent, so a Python build establishes them at a fraction of the cost of establishing them in the production language.

- **The build grows in layers, and the earliest useful layer ships.**
  A whole-document bundling that works end to end comes first. Section selection, dependency closure, destination identity and the one validation check that proves a candidate carries its sources follow, and the tool installs at that point. Boundary safety, diagnostics, validation scope, the outline a partial selection skipped, directory grouping and the measured budget extend a product agents are already invoking.

- **Coverage depth follows the ship rather than preceding it.**
  Each row before the ship carries the fixture that proves its behaviour, and declares its boundary, failure and adversarial cases as fixtures awaiting the conformance epic. A declared fixture that unexpectedly passes fails the run, so a deferral cannot outlive its reason and the corpus names every gap it carries.

- **Span-level editing is out of scope here.**
  Byte-exact source-preserving edits are specific to the production parser and are proven where that parser lives. This build may reconstruct its output, provided the corpus's preservation fixtures hold.

- **The build ships to be used.**
  It installs with a stable entry point and a wrapper owning the delivery contract, because the specification is refined by what real use reveals and nothing is revealed by a build nobody invokes.

- **The conformance report is the handover.**
  It maps every behavioural clause of the design to the fixtures that exercise it, and lists any clause no fixture covers, so the next implementation inherits a measured contract rather than an assumed one.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/26) | Project Foundation | | | ✓ |
| [E01](https://github.com/m2ux/prosiform/issues/3) | Corpus Harness | AC8 | | ✓ |
| [E02](https://github.com/m2ux/prosiform/issues/4) | Walking Skeleton | AC7, AC13 | | ✓ |
| [E03](https://github.com/m2ux/prosiform/issues/5) | Outline Hierarchy | AC5 | | ✓ |
| [E04](https://github.com/m2ux/prosiform/issues/6) | Dependency Closure | AC1, AC3, AC10 | | ✓ |
| [E05](https://github.com/m2ux/prosiform/issues/7) | Destination Identity | AC2 | | |
| [E06](https://github.com/m2ux/prosiform/issues/8) | Candidate Validation | AC4, AC6 | [E05](https://github.com/m2ux/prosiform/issues/7) | |
| [E07](https://github.com/m2ux/prosiform/issues/19) | Field Deployment | AC11, AC12 | | |
| [E08](https://github.com/m2ux/prosiform/issues/59) | Validation Gate | AC6 | [E05](https://github.com/m2ux/prosiform/issues/7) | |
| [E09](https://github.com/m2ux/prosiform/issues/60) | Outline and Closure Completion | AC5, AC14 | | |
| [E10](https://github.com/m2ux/prosiform/issues/9) | Corpus Conformance | AC9 | [E06](https://github.com/m2ux/prosiform/issues/8) | |
| [E11](https://github.com/m2ux/prosiform/issues/39) | Deferred Debt | AC15 | | |

The order these epics start in is carried by each one's priority label rather than by this table. A cell here names a prerequisite only where every task of the dependent epic requires every task of the one named; every other edge stays in the task tables, so an epic starts on the rows that are free and waits only on the rows that are not.

## Acceptance Criteria

- [x] **AC1.** A bundling returns one Markdown document holding the selected content and every local Markdown dependency reachable from it, as the corpus runner's output comparison shows.
- [ ] **AC2.** Each internal reference in a published bundle resolves to exactly one destination within that bundle, as the corpus runner's destination check shows.
- [x] **AC3.** Each selected source region appears once in a published bundle however many reference paths reach it, as the corpus runner's output comparison shows.
- [ ] **AC4.** Selected instruction wording and code examples are byte-identical to their sources apart from the transformations the declared profile names, as the corpus runner's preservation check shows.
- [ ] **AC5.** Each selected section keeps its ancestor chain and its relative depth beneath the heading naming its source file, as the corpus runner's outline comparison shows.
- [ ] **AC6.** A bundling that fails validation publishes nothing, exits nonzero and writes a diagnostic carrying the defect, its source location, the offending reference and the inclusion chain, as the corpus's failure fixtures show.
- [x] **AC7.** A document bundles with no markup beyond ordinary Markdown links and headings, as the fixtures taken from unmodified workspace skills show.
- [x] **AC8.** A fixture declares its sources, its invocation and its expected result, and the runner decides pass or fail from that declaration alone, as the runner's own test suite shows.
- [ ] **AC9.** Every behavioural clause the design states maps to at least one corpus fixture, or is listed as uncovered, as the conformance report shows.
- [x] **AC10.** Each resource limit the profile names fails at the first boundary it crosses, publishing nothing, as the corpus's limit fixtures show.
- [ ] **AC11.** An agent bundles its context by invoking the installed tool rather than by reading the linked documents itself, as the installation smoke run against a documented entry point shows.
- [ ] **AC12.** A bundle the transport cannot deliver whole is reported as a delivery failure rather than as a truncated success, as the corpus's delivery fixtures show.
- [x] **AC13.** A corpus run reproduces on a fresh checkout at the dependency versions a lockfile records, as the continuous-integration run shows.
- [ ] **AC14.** The output budget rests on the measured size of a real bundling rather than an assumed figure, as the recorded measurement shows.
- [ ] **AC15.** The technical debt this initiative's delivery defers is fixed, as the Done column of its final epic's Work Breakdown shows.

## Non-Goals

- It does not apply byte-exact edits to identified source spans.
- It does not create the production build's tree, toolchain or dependencies.
- It does not settle the specification, which use refines.
- It does not execute, authorize or sequence the procedures it bundles.
- It does not infer a dependency the source did not state as a Markdown link.
- It does not fetch remote documents, resources or URLs.
- It does not accept its own output as a source document.

## References

- **R1.** **Source.** [v1 design](https://github.com/m2ux/prosiform/blob/d45c7f08f3878e71d9d0a99ae728fc69fc21f174/artifacts/planning/2026-10-17-prosiform-v1/design.md) — the behavioural contract these criteria answer to: input and output, Markdown profile, section extraction, destination identity, validation invariants and resource limits.
- **R2.** [Planning decisions](https://github.com/m2ux/prosiform/blob/d45c7f08f3878e71d9d0a99ae728fc69fc21f174/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) — why the prototype is a retained oracle, where the corpus lives, and the measured evidence behind the Problem.
- **R3.** [Proposal](https://github.com/m2ux/prosiform/issues/1) — the scoped problem and the goal clauses these criteria trace to.

