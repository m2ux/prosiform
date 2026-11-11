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

The board's engineering lifecycle (its SDLC) decides how the work inside an issue is planned, delivered and verified. Each mode leaves that to an SDLC hook.

## Configure

The board's description records its SDLC as one line, `SDLC: <name>`. A board recording none follows `ad-hoc`.

The SDLCs are `ad-hoc` and each preset the frontmatter of `sdlc/port.md` names other than `default`.

- When the board records no SDLC, list the SDLCs, ask the user which one the board follows, and record their answer.
- When the user asks to change the board's SDLC, replace its line.
- Refuse a name that is not an SDLC, listing the SDLCs there are.

## SDLC Hooks

A link to `sdlc/port.md` names an SDLC hook. Compile it with `pf <the link's path> --presets <the board's SDLC>`, or with no `--presets` for `ad-hoc`, and follow the result in place of the link.

## Mode Selection

Select the mode the user's request calls for:

- **[Propose](modes/propose-mode.md)**  Raises a proposal on the board.
- **[Plan](modes/plan-mode.md)**  Moves a proposal from Proposed to Planned.
- **[Advance](modes/advance-mode.md)**  Moves planned work from Planned to Ready.
- **[Deliver](modes/deliver-mode.md)**  Moves ready work through In Progress to In Review.
- **[Sync](modes/sync-mode.md)**  Moves reviewed work from In Review to Done.
