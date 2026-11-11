---
name: project-lifecycle
description: >-
  Moves tracker issues across a project board, from proposal to done, under
  the engineering lifecycle the board's owner selects.
prosiform: {}
---

# Project Lifecycle

Project Lifecycle moves issues across a project board. Each mode is one transition between board stages:

**Proposed** → **Planned** → **Ready** → **In Progress** → **In Review** → **Done**

The board's engineering lifecycle (its SDLC) decides how the work inside an issue is planned, delivered and verified.

## SDLC

The board's description records the SDLC it follows as one line, `SDLC: <name>`. A board recording none follows Ad Hoc. The SDLCs are:

- [¬ Ad Hoc](sdlc/port.md)
- [¬ Waterfall](sdlc/port.md "waterfall")

When the board records no SDLC, ask the user which of these it follows, and record their answer. When the user asks to change it, replace its line. Refuse any other name, listing these.

Follow the board's SDLC for each practice a mode applies.

## Mode Selection

Select the mode the user's request calls for:

- **[Propose](modes/propose-mode.md)**  Raises a proposal on the board.
- **[Plan](modes/plan-mode.md)**  Moves a proposal from Proposed to Planned.
- **[Advance](modes/advance-mode.md)**  Moves planned work from Planned to Ready.
- **[Deliver](modes/deliver-mode.md)**  Moves ready work through In Progress to In Review.
- **[Sync](modes/sync-mode.md)**  Moves reviewed work from In Review to Done.
