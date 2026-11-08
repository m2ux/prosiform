## Overview

Skills write each command as a paragraph wrapped in `<big><pre>` … `</pre></big>`, with its parameters as links to their definitions. `pf` refuses the wrapper as raw HTML, and the section it sits in fails a second way in the link rewrite. The profile accepts that one wrapper and the rewrite is fixed, so a section carrying a command block compiles.

Target: `main`

## Problem

- **Every command block is refused.**
  117 blocks across the work-planner skill use the wrapper, and each fails with `E_RAW_HTML`. `<big>` opening the line makes CommonMark read the block as a paragraph, so the links inside already parse; only the profile's inline HTML refusal stops the run.
- **The rewrite fails on the surrounding section.**
  With the block removed, `artifacts/board-queue.md#compute-board-queue` fails with `E_UNEXPECTED_INTERNAL_ERROR`: `Unrewritable('the parser read 2 use(s) against the 3 the emission can edit in place')`. An internal error is a defect whatever the source.

## Proposal

- **The profile accepts the command-block wrapper.**
  A paragraph whose first inline is `<big><pre>` and whose last is `</pre></big>` is carried into the bundle as written, and its links are discovered, resolved and rewritten as any paragraph's are. All other raw HTML is refused with `E_RAW_HTML`.
- **The rewrite counts what it edits.**
  The trigger is isolated to a minimal fixture and the use count and the emission agree on it.
- **The contract moves a minor.**
  Fixtures are added and none change, so the release is `contract/v0.20.0` and `python/v0.20.0`, cut after merge.

## Acceptance Criteria

- [ ] **AC1.** A paragraph wrapped in `<big><pre>` and `</pre></big>` compiles, its local links rewritten, as `make corpus` shows.
- [ ] **AC2.** `<pre>` alone, `<big>` alone, an unclosed wrapper and a wrapper with attributes are each refused with `E_RAW_HTML`, as `make corpus` shows.
- [ ] **AC3.** The minimal source that raised `Unrewritable` compiles, as `make corpus` shows.
- [ ] **AC4.** A scratch copy of work-planner with `prosiform` frontmatter compiles `artifacts/board-queue.md#compute-board-queue` without a diagnostic.
- [ ] **AC5.** `docs/sources.md` states the accepted wrapper beside the raw HTML refusal.
