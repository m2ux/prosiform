## Overview

A command block's source form is written for a renderer: a `<big><pre>` wrapper, HTML entities for `<`, `>` and `\`, and bold link text. An agent reading the bundle gains nothing from that markup and pays for it in tokens. The bundle emits each command block as its linked Markdown alone, and the source keeps the rendered form.

Target: `main`

## Problem

- **The wrapper and its escapes cost tokens on every command.**
  `pf` 0.22.0 carries a command block as written. In a skill's Compute Board Queue section, the wrapper lines, the `&lt;`/`&gt;`/`&#92;` entities and the `**` around each parameter add about a fifth to the block's characters, and a skill holds over a hundred such blocks.
- **The markup serves the renderer, not the reader.**
  `<big><pre>` keeps a block monospaced on GitHub while its links stay live. The entities keep the renderer from reading `<name>` as HTML or `\` as an escape. A bundle is read as text, so neither applies.

## Proposal

- **A command block is emitted as its content.**
  The bundle drops the `<big><pre>` and `</pre></big>` tags, unwraps `**` that encloses a link's whole text, and decodes every character reference in the block. Links are resolved and rewritten as before. Text outside a command block is unchanged.
- **The transformation is declared.**
  The design's bundle transformations name the command-block compaction, so Preservation holds against it. The bundle's reparse accepts the raw `<name>` a decoded placeholder leaves inside link text.
- **The contract moves a minor.**
  The command-block fixture's expected bundle changes, which is a major change. Below `1.0.0` the minor carries it: `contract/v0.23.0` and `python/v0.23.0`, cut after merge.

## Acceptance Criteria

- [ ] **AC1.** A command block's bundle form carries no `<big>`, `<pre>`, character reference or `**` around a link's whole text, and its links are rewritten, as `make corpus` shows.
- [ ] **AC2.** Entities and bold outside a command block are emitted as written, as `make corpus` shows.
- [ ] **AC3.** A copy of the work-planner skill with `prosiform` frontmatter compiles `artifacts/board-queue.md#compute-board-queue` with exit 0, and the command lines read `cd "[<workspace>](#workspace "○")" && \`.
- [ ] **AC4.** `docs/sources.md` and `docs/bundles.md` state the command block's bundle form, each where it owns the rule.

## References

- **R1.** [#697](https://github.com/m2ux/prosiform/issues/697) — F07, which accepts the command block.
- **R2.** [Compute Board Queue](https://github.com/m2ux/workflow-server/blob/workspace/skills/work-planner/artifacts/board-queue.md#compute-board-queue) — a command block as skills write it.
- **R3.** [Bundle invariants](https://github.com/m2ux/prosiform/blob/bf9208311/docs/validation.md) — Preservation and the reparse.
