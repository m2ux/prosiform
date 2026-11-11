# § Instructions

Run `pf`, then follow the guidance it prints. Follow [Project Lifecycle](#project-lifecycle) next.

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

- **[Propose](#propose)**  Raises a proposal on the board.
- **[Plan](#plan)**  Moves a proposal from Proposed to Planned.
- **[Advance](#advance)**  Moves planned work from Planned to Ready.
- **[Deliver](#deliver)**  Moves ready work through In Progress to In Review.
- **[Sync](#sync)**  Moves reviewed work from In Review to Done.

## Modes

### Overview

#### Propose

Raises a proposal on the board.

#### Plan

Moves a proposal from **Proposed** to **Planned**.

#### Advance

Moves planned work from **Planned** to **Ready**.

#### Deliver

Moves ready work through **In Progress** to **In Review**.

#### Sync

Moves reviewed work from **In Review** to **Done**.

### Procedure

#### Propose

1. Raise an issue stating the problem and the outcome sought.
2. Place it in **Proposed**.

#### Plan

1. Break the proposal into epics and tasks.
2. Apply the [Plan Practice](sdlc/port.md#on-plan).
3. Move the proposal to **Planned**.

#### Advance

1. Confirm each dependency of the work is in **Done**.
2. Confirm the work carries a priority.
3. Move the work to **Ready**.

#### Deliver

1. Move the work to **In Progress**.
2. Apply the [Deliver Practice](sdlc/port.md#on-deliver).
3. Open a pull request for the work.
4. Move the work to **In Review**.

#### Sync

1. Apply the [Verify Practice](sdlc/port.md#on-verify).
2. Merge the pull request.
3. Move the work to **Done**.
