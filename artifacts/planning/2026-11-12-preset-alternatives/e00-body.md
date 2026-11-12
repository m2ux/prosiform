## Overview

A preset holding `choice` is an alternative, and a document declaring alternatives compiles only with exactly one of them in force. A missing or wrong pick fails with its own code, naming every alternative with when to pick it, and an alternative's `subst` pairs route its document's links without the warnings a stand-in raises. The epic leaves main with alternatives an author picks by a link title or `--presets`, stated in the v1 design and the documentation.

## Problem

- **No preset says pick one.**
  A preset [holds `group` and `subst`](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/docs/sources.md#L48-L53) alone, so a document cannot require one of a set of its presets in force.
- **An unknown name selects nothing.**
  [Selection ignores](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/docs/selection.md#L39) a name the target does not declare, so a mistyped kind compiles `default` alone without an error.
- **Two picks merge.**
  A document's links [resolve through the pairs of every preset in force](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/docs/selection.md#L50), so two references picking different kinds of one document combine their routes.
- **Routing warns as a stand-in does.**
  [`W_SUBST_USED` and `W_SUBST_UNUSED`](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/docs/selection.md#L56) fire for a routed link and for a pair whose link sits outside the selection, and [`W_PRESET_UNUSED`](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/docs/selection.md#L44) for each kind not picked.

## Proposal

- **The design states the rules first.**
  The v1 design states alternatives, the exactly-one rule, its code, routing pairs and the agent's pick before the build enforces them.
- **`choice` makes an alternative.**
  It holds a non-empty one-line string; a malformed `choice`, a `choice` in `default` and a preset named `?` fail with `E_INVALID_CONVERSION_METADATA`.
- **Exactly one is in force.**
  It is counted on the union every reference reaching the document selects in one bundle; none or several fail with `E_ALTERNATIVE_UNRESOLVED` and exit status 2.
- **The failure lists the alternatives.**
  It names each with its choice line in declaration order, and an alternative no reference picked raises no `W_PRESET_UNUSED`.
- **An alternative routes quietly.**
  Its used pair raises no `W_SUBST_USED`, and `W_SUBST_UNUSED` fires only for a key no link of its document names; an ordinary preset's pairs warn as before.
- **The documentation follows.**
  The sources, selection, invocation, glossary and validation pages state the rules and pin the design that states them.
- **The agent's pick is the next layer.**
  A link handing the pick to the agent builds on these rules and lies outside this epic.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/e00/w00.md) | The v1 design states alternatives | AC1 | | | | |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/e00/w01.md) | A choice line declares an alternative | AC2, AC3 | W00 | | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/e00/w02.md) | Exactly one alternative in force | AC4, AC5, AC6 | W01 | | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/e00/w03.md) | Routing pairs route quietly | AC7, AC8 | W01 | | | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/e00/w04.md) | The documentation states alternatives | AC9 | W02, W03 | | | |

## Acceptance Criteria

- [ ] **AC1.** The v1 design states alternatives, the exactly-one rule, its code, routing pairs and the agent's pick, as a read of its presets, link classification and guide sections shows.
- [ ] **AC2.** A link picking one of its target's alternatives, alone or beside ordinary presets, compiles that document with the alternative's routes in force, as the inclusion fixtures show.
- [ ] **AC3.** A malformed `choice`, a `choice` in `default` and a preset named `?` each fail with `E_INVALID_CONVERSION_METADATA`, as the frontmatter fixtures show.
- [ ] **AC4.** A run in which a document declaring alternatives has none or several of them in force fails with `E_ALTERNATIVE_UNRESOLVED` and exit status 2, as the inclusion fixtures show.
- [ ] **AC5.** An `E_ALTERNATIVE_UNRESOLVED` failure names each alternative with its choice line in declaration order, as the inclusion fixtures show.
- [ ] **AC6.** An alternative no reference picked raises no `W_PRESET_UNUSED`, as the inclusion fixtures show.
- [ ] **AC7.** A routing pair raises neither `W_SUBST_USED` nor `W_SUBST_UNUSED` while a link of its document names its key, as the inclusion fixtures show.
- [ ] **AC8.** A routing pair whose key no link of its document names warns `W_SUBST_UNUSED`, as the inclusion fixtures show.
- [ ] **AC9.** The sources, selection, invocation, glossary and validation pages state each rule this epic adds and pin the design stating it, as `make links` and a read of those pages show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-preset-alternatives) — the design, the decisions, the work items and the dependency check.
- **R2.** [Preset Alternatives design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/design.md) — the rules each row implements.
