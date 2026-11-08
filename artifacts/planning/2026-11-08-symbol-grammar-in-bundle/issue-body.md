## Overview

Every bundle tells its reader to run `pf` and follow the guide it prints, only so the reader learns what `↳`, `⇉` and `⫽` mean. The bundle carries that symbol grammar in its own `§ Instructions` section, and the guide bare `pf` prints keeps everything else.

Target: `main`

## Problem

- **A bundle is not self-contained.**
  Its `§ Instructions` section holds one line, ``Run `pf`, then follow the guidance it prints.`` An agent reading a bundle must make a tool call before it can follow any mark the bundle holds.
- **The symbol grammar has two audiences in one place.**
  Bare `pf` serves both the agent compiling a link and the agent reading a bundle. Only the second needs the marks.

## Proposal

- **The bundle states the marks.**
  `§ Instructions` holds the guide's three symbol entries as a list, then the existing `Follow [<first heading>](#…) next.` line. The run-pf line goes.
- **Bare `pf` states how to compile.**
  The guide keeps usage, compiling a link and exit status, and drops the Symbol grammar.
- **The contract moves a minor.**
  Every expected bundle changes, so the release is `contract/v0.21.0` and `python/v0.21.0`, cut after merge.

## Acceptance Criteria

- [ ] **AC1.** Every bundle opens with `# § Instructions`, the three symbol entries and the follow line, and no line telling its reader to run `pf`, as `make corpus` shows.
- [ ] **AC2.** Regenerated fixtures differ from `main` only in their `§ Instructions` section.
- [ ] **AC3.** Bare `pf` prints no `↳`, `⇉` or `⫽` entry and exits `0`, as `tests/test_cli.py` shows.
- [ ] **AC4.** `checks/smoke.py` and the diagram-following eval tests pass against the new opening.
- [ ] **AC5.** No doc, docstring or test describes the run-pf line or the guide as the home of the symbol grammar.
