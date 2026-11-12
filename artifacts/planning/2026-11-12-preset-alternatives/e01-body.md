## Overview

A `?` tag in a deferred link's title leaves the pick of its target's alternative to the agent that compiles it. The deferral publishes the tag, the agent passes the title as `--presets` as it does for every deferred link, and `pf` answers with the alternatives in place of a bundle; the agent reruns with the one that fits. The epic adds the tag, its refusals, the guide entry and a corpus fixture proving the flow end to end, on the alternatives the declared-alternatives work provides.

## Problem

- **No title tag leaves the pick open.**
  A [title's tags select](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/docs/selection.md#L39) the presets its author named, so a deferred link to a generic document names the kind when it is written.
- **The guide names no pick.**
  The agent [passes title tags as one `--presets` value, also for deferred links](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/src/prosiform/cli.py#L333), and the [symbol grammar](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/src/prosiform/cli.py#L348-L359) states no mark for a choice.
- **A dispatch is compiled before any agent reads it.**
  The run [compiles a dispatch up front](https://github.com/m2ux/prosiform/blob/6fc54bbf70c519779bf611f7162fc0fa0b3a383b/docs/references.md#L74), so no reader is present to pick for it.

## Proposal

- **`?` requests the agent's pick.**
  A `?` token in a link title stands beside any fixed tags, and selects no preset.
- **Only a deferred link carries it.**
  It is accepted on a `¬` or `¬↳` link and published with the deferral's title, and refused on an ordinary, `↳`, `⇉` or `⫽` link.
- **A deferred link to alternatives states its pick.**
  It names exactly one alternative or carries `?`, never both, and `?` needs a target declaring alternatives; any other form is refused before a bundle is published.
- **The answer is the listing.**
  Passed as `--presets`, `?` leaves no alternative in force, so the agent's compile fails with the alternatives and their choice lines.
- **The guide states the pick.**
  One symbol-grammar entry: pass the title as usual, read the list, rerun with `?` replaced by the alternative that fits.
- **A router fixture proves the flow.**
  A kind router with alternatives, a mode linking it with `?`, the listing, and each pick's bundle.
- **An agent proves the pick.**
  The diagram-following eval gains an agent-pick workflow in its `compiled` form, where a headless session resolves a `?` pick from what the bundle and `pf` print, and a live run records how often it picks correctly.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/e01/w01.md) | A pick tag rides a deferred link | AC1, AC2 | [E00:W00](https://github.com/m2ux/prosiform/issues/708) | W02 | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/e01/w02.md) | A deferred link states its pick | AC3 | [E00:W01](https://github.com/m2ux/prosiform/issues/708) | W01 | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/e01/w03.md) | The guide states the pick end to end | AC4, AC5 | W02, [E00:W02](https://github.com/m2ux/prosiform/issues/708), [E00:W03](https://github.com/m2ux/prosiform/issues/708) | | | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/e01/w04.md) | The documentation states the pick | AC6 | W03, [E00:W04](https://github.com/m2ux/prosiform/issues/708) | | | |
| [W05](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/e01/w05.md) | An agent-pick eval workflow | AC7 | W03 | | | |
| [W06](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/e01/w06.md) | A measured agent-pick run | AC8 | W05 | | | |

## Acceptance Criteria

- [ ] **AC1.** A `¬` or `¬↳` link whose title carries `?` publishes that title with its deferral, as the deferral fixtures show.
- [ ] **AC2.** A `?` on an ordinary, `↳`, `⇉` or `⫽` link is refused, as the deferral and dispatch fixtures show.
- [ ] **AC3.** A deferred link to a document with alternatives that names none, names two or names one beside `?`, and a `?` link to a document without alternatives, are each refused, as the deferral fixtures show.
- [ ] **AC4.** The guide's symbol grammar states how an agent resolves `?`, as the bare-command test shows.
- [ ] **AC5.** A kind router reached through a `?` link compiles, from the published bundle's command, to the listing and then to each pick's bundle, as the router fixtures show.
- [ ] **AC6.** The references, invocation and glossary pages state the `?` tag and its refusals and pin the design stating them, as `make links` and a read of those pages show.
- [ ] **AC7.** The diagram-following eval holds an agent-pick workflow whose scenarios pass only a session that enters the picked kind's states alone, after running `pf` with `?` replaced by that alternative and reading no source, as `make harness` and a stub-agent run of each scenario show.
- [ ] **AC8.** The agent-pick run record holds the workflow's pass rates from a live run, each failing session with its disposition, as the committed `agent-pick.json` shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-preset-alternatives) — the design, the decisions, the work items and the dependency check.
- **R2.** [Preset Alternatives design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/design.md) — the rules each row implements.
