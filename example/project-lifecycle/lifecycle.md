---
prosiform:
  default: {}
  waterfall:
    subst:
      - {sdlc/ad-hoc.md: sdlc/waterfall.md}
---

# Project Lifecycle

Moves issues across a project board. Each mode is one transition between board stages:

**Proposed** → **Planned** → **Ready** → **In Progress** → **In Review** → **Done**

## Mode Selection

Select the mode the user's request calls for:

- **[Propose](modes/propose-mode.md)**  Raises a proposal on the board.
- **[Plan](modes/plan-mode.md)**  Moves a proposal from Proposed to Planned.
- **[Advance](modes/advance-mode.md)**  Moves planned work from Planned to Ready.
- **[Deliver](modes/deliver-mode.md)**  Moves ready work through In Progress to In Review.
- **[Sync](modes/sync-mode.md)**  Moves reviewed work from In Review to Done.

## Practices

### Planning Practice

What a plan holds before it is **Planned**.

[↳ Practice](sdlc/ad-hoc.md#plan)

### Implementation Practice

How work in **In Progress** is built.

[↳ Practice](sdlc/ad-hoc.md#deliver)

### Verification Practice

What work in **In Review** shows before it is **Done**.

[↳ Practice](sdlc/ad-hoc.md#verify)
