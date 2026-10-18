## Overview

Agent skills in this workspace are authored as modular instruction sets: an entry point links to modes, modes link to artifacts, and artifacts link to one another's sections. Reaching the complete context for one operation means resolving that graph at read time, which is work the agent currently performs by following prose rules. This proposal scopes prosiform, a tool that compiles a set of linked local Markdown documents into one continuous, validated Markdown document, so that an agent given a reference receives the selected content and every local Markdown dependency it links to, or an explicit failure.

## Problem

Modular Markdown authoring separates the destination a link names from the context an operation needs, and nothing closes that gap except the reading agent.

- **Retrieval is prose the agent must execute.**
  One rule directs the agent to read a linked section and its subsections, stop before the next heading of equal or higher level, read that file's prerequisites first, preserve boundaries in batched reads and recover truncated output: [Linked sections](https://github.com/m2ux/prosiform/blob/acac85867ca963df00251e4cf00a4db11b14bf24/skills/work-planner/SKILL.md#L71-L72).

- **One request reaches 39 documents.**
  [Plan Mode](https://github.com/m2ux/prosiform/blob/acac85867ca963df00251e4cf00a4db11b14bf24/skills/work-planner/modes/plan-mode.md#L5-L23) lists 15 prerequisites; the transitive closure of its Markdown links is 39 files and 139 distinct section targets, 318,018 bytes read whole.

- **Section boundaries are decided by the reader.**
  519 Markdown links run between the 38 files of that one skill, 363 of them naming a section rather than a file, so each read also decides where the named section ends.

- **A shared rule is repeated in every prerequisite list.**
  25 files across this workspace's skills open with their own `Read these files first` list, because a link alone does not retrieve what it names.

- **Nothing establishes the context was complete.**
  A prerequisite the agent skipped and one it never needed produce the same result: an operation that proceeds. There is no step that observes whether the closure was reached.

## Goal

- Given a source root and one or more local document or section references, an agent receives one continuous Markdown document containing the selected content and every local Markdown dependency reachable from it.
- Every internal reference in that document resolves to exactly one destination within it, and each included source region appears exactly once however many paths reach it.
- Selected instruction wording and code examples are byte-identical to their sources apart from the transformations the declared profile names.
- The original outline of each selected section survives: its ancestor headings are present, its relative depth is preserved, and each contributing file's content sits beneath one heading naming that file.
- A run that cannot be fully validated emits no bundle and exits nonzero, with a diagnostic naming the defect, its source location, the offending reference and the inclusion chain that reached it.
- Authors keep their existing modular files; nothing beyond ordinary Markdown links and headings is needed to bundle a document.
- The contract is demonstrated by two independent implementations passing one shared fixture corpus.
- The behavioural contract the production build implements has been exercised by real use and recorded as settled before that build begins.

## Non-Goals

- It does not execute, authorize or sequence the procedures it bundles.
- It does not infer a dependency the source did not state as a Markdown link.
- It does not fetch remote documents, resources or URLs.
- It does not bundle images or other non-Markdown resources into the bundle.
- It does not accept its own output as a source document.
- It does not guarantee that an agent obeys the bundled instructions.
- It does not change `pulldown-cmark` or contribute anything upstream.
- It does not commit to a date by which the contract is settled.

## References

- **R1.** [v1 design](https://github.com/m2ux/prosiform/blob/d45c7f08f3878e71d9d0a99ae728fc69fc21f174/artifacts/planning/2026-10-17-prosiform-v1/design.md) — the approved behavioural contract: input and output, Markdown profile, section extraction, destination identity, validation invariants and resource limits.
- **R2.** [Upstream assessment](https://github.com/m2ux/prosiform/blob/d45c7f08f3878e71d9d0a99ae728fc69fc21f174/artifacts/planning/2026-10-17-prosiform-v1/upstream-assessment.md) — the inspected state of `pulldown-cmark` against the two parser viability gates, and the two narrowly scoped contributions that would satisfy them.
- **R3.** [Planning decisions](https://github.com/m2ux/prosiform/blob/d45c7f08f3878e71d9d0a99ae728fc69fc21f174/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) — the decisions taken with the user, the reasoning behind each, and the measured evidence above.

