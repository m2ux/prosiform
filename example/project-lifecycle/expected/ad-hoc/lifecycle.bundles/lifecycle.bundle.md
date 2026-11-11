# § Instructions

Run `pf`, then follow the guidance it prints. Follow [Project Lifecycle](#project-lifecycle) next.

# Project Lifecycle

Moves issues across a project board. Each mode is one transition between board stages:

**Proposed** → **Planned** → **Ready** → **In Progress** → **In Review** → **Done**

## Mode Selection

Select the mode the user's request calls for:

- **[Propose](#propose)**  Raises a proposal on the board.
- **[Plan](#plan-1)**  Moves a proposal from Proposed to Planned.
- **[Advance](#advance)**  Moves planned work from Planned to Ready.
- **[Deliver](#deliver-1)**  Moves ready work through In Progress to In Review.
- **[Sync](#sync)**  Moves reviewed work from In Review to Done.

## Practices

### Planning Practice

What a plan holds before it is **Planned**.

[Practice](#ad-hoc)

#### Plan

##### Ad Hoc

Each task states its outcome.

### Implementation Practice

How work in **In Progress** is built.

[Practice](#ad-hoc-1)

#### Deliver

##### Ad Hoc

Build the task in the order that suits it.

### Verification Practice

What work in **In Review** shows before it is **Done**.

[Practice](#ad-hoc-2)

#### Verify

##### Ad Hoc

The pull request's checks pass.

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
2. Apply the [Planning Practice](#planning-practice).
3. Move the proposal to **Planned**.

#### Advance

1. Confirm each dependency of the work is in **Done**.
2. Confirm the work carries a priority.
3. Move the work to **Ready**.

#### Deliver

1. Move the work to **In Progress**.
2. Apply the [Implementation Practice](#implementation-practice).
3. Open a pull request for the work.
4. Move the work to **In Review**.

#### Sync

1. Apply the [Verification Practice](#verification-practice).
2. Merge the pull request.
3. Move the work to **Done**.
