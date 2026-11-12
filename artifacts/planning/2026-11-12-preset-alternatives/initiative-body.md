## Overview

A document generic over a kind of work declares one preset per kind as an alternative and compiles only with exactly one of them in force. A deferred link can leave that pick to the agent that compiles it, and `pf` answers the request with every alternative and when to pick it. The goal the reviews test against: a document generic over a kind compiles for the kind its reader is handling, and a missing or wrong pick fails rather than compiling the wrong route.

## Problem

A link's presets are fixed when its author writes the link, so a document generic over a kind of work cannot be compiled for the kind an agent is handling.

- **The pick is the author's alone.**
  A [link title selects](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/docs/selection.md#L39-L40) the target's presets and an entry's `--presets` repeats a title, so nothing leaves the choice to the reader.
- **A wrong name compiles the general route.**
  The [tag reader](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/src/prosiform/tags.py#L11-L17) keeps any name and selection ignores one the target does not declare, so a mistyped kind compiles `default` alone without an error.
- **Two picks merge.**
  A document's links [resolve through the `subst` pairs of every preset in force](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/docs/selection.md#L50) for it, so two references picking different kinds of one document combine their routes.
- **Routing warns as a stand-in does.**
  `subst` [flags each pair a link used and each pair no link used](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/docs/selection.md#L56), and [each preset nothing selected](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/docs/selection.md#L44) warns, so a document routing by kind warns on every compile.
- **A generic skill routes as it is read.**
  work-planner's [Work Kind](https://github.com/m2ux/workflow-server/blob/e6eb1af6d9ba6de3b97ff49a85ce82548224e285/skills/work-planner/artifacts/work-kind.md#L5-L32) lists every kind's operation in each step, and the agent applies the line for its item's kind as it reads.

## Proposal

- **A document declares its alternatives.**
  A preset holding `choice`, one line stating when to pick it, is an alternative, and exactly one is in force wherever its document compiles.
- **A missing or wrong pick fails with the list.**
  None or several in force fail with a code of their own, naming every alternative with its choice line.
- **An alternative routes quietly.**
  Its `subst` pairs route the document's links to the picked kind, and warn only for a key no link of the document names.
- **A deferred link can leave the pick to the agent.**
  A `?` title tag travels with the deferral, and passed as `--presets` it draws the list in place of a bundle.
- **The guide states the pick.**
  One symbol-grammar entry tells the agent to rerun with `?` replaced by the alternative that fits its task.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/708) | Declared Alternatives | AC1, AC2, AC3, AC4, AC5 | | ✓ |
| [E01](https://github.com/m2ux/prosiform/issues/709) | Agent Pick | AC1, AC2, AC4, AC5 | [E00](https://github.com/m2ux/prosiform/issues/708) | ✓ |
| [E02](https://github.com/m2ux/prosiform/issues/733) | Agent Pick in Real Use | AC4 | [E01](https://github.com/m2ux/prosiform/issues/709) | |

## Acceptance Criteria

- [x] **AC1.** A document generic over a kind compiles for the one kind picked for it, by its author's link or by the agent following the bundle, as the fixture corpus shows.
- [x] **AC2.** A pick left missing, unknown or plural fails before any bundle is published, as the fixture corpus shows.
- [x] **AC3.** Routing by kind warns only for a route no link of its document names, as the fixture corpus shows.
- [ ] **AC4.** An agent following a bundle resolves a pick left to it from what the bundle and `pf` print, without reading a source, as the router fixtures, the bare-command test and the agent-pick eval show.
- [x] **AC5.** The documentation and the v1 design state each rule of alternatives and picks the build enforces, as `make links` and a read of the documentation show.

## Non-Goals

- It adds no pick to a dispatch link, which the run compiles before any agent reads it.
- It forwards no pick to the documents a target links, and applies none across a run.
- It migrates no skill to alternatives; a corpus fixture shaped like a kind router proves the pattern.
- It implements nothing in the Rust build.
- It adds no design-pattern page.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-preset-alternatives) — the design interview's decisions, the work items and the dependency check.
- **R2.** **Source.** [Preset Alternatives design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/design.md) — the rules the criteria answer to.
- **R3.** [Work Kind](https://github.com/m2ux/workflow-server/blob/e6eb1af6d9ba6de3b97ff49a85ce82548224e285/skills/work-planner/artifacts/work-kind.md) — the kind router whose read-time routing motivates the design.
- **R4.** [Production Build](https://github.com/m2ux/prosiform/issues/532) — the Rust build of the contract, which shares the fixture corpus these rules extend.


