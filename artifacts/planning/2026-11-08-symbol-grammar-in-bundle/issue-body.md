## Overview

Every bundle tells its reader to run `pf` and follow the guide it prints, only so the reader learns what `↳`, `⇉` and `⫽` mean. The symbol grammar becomes one object in the code. The guide bare `pf` prints and every bundle's `§ Instructions` section both render it.

Target: `main`

## Problem

- **A bundle is not self-contained.**
  Its `§ Instructions` section holds one line, ``Run `pf`, then follow the guidance it prints.`` An agent reading a bundle must make a tool call before it can follow any mark the bundle holds.
- **The symbol grammar has one home, and it is outside the bundle.**
  It is written inline in `GUIDE` in `cli.py`, so nothing else can carry it without a second copy.

## Proposal

- **The symbol grammar is one object.**
  `prosiform/symbols.py` holds the three `(mark, meaning)` entries. `GUIDE` renders them as plain text, so bare `pf` prints the same bytes it does today.
- **The bundle states the marks.**
  `§ Instructions` renders the same entries as a Markdown list, then the existing `Follow [<first heading>](#…) next.` line. The run-pf line goes.
- **The contract moves a minor.**
  Every expected bundle changes, so the release is `contract/v0.21.0` and `python/v0.21.0`, cut after merge.

## Acceptance Criteria

- [ ] **AC1.** Every bundle opens with `# § Instructions`, the three symbol entries and the follow line, and no line telling its reader to run `pf`, as `make corpus` shows.
- [ ] **AC2.** Regenerated fixtures differ from `main` only in their `§ Instructions` section.
- [ ] **AC3.** Bare `pf` prints the same bytes as on `main`, and the symbol wording appears once in `src/prosiform/`, as `tests/test_cli.py` and a grep show.
- [ ] **AC4.** `checks/smoke.py` and the diagram-following eval tests pass against the new opening.
- [ ] **AC5.** No doc, docstring or test describes the run-pf line or the guide as the home of the symbol grammar.
