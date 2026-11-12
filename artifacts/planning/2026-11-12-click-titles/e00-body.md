## Overview

A Mermaid click's quoted tooltip is read as its link's title: its opening marks state the operator and the rest selects presets. The design states the rule first, the build and its fixtures carry it together, and the documentation follows.

## Problem

- **The parser skips the tooltip.**
  [`QUOTED`](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/src/prosiform/source.py#L159-L163) matches a tooltip without capturing it, and [`uses`](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/src/prosiform/source.py#L1210-L1214) and [`carried`](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/src/prosiform/candidate.py#L354-L362) give every click an empty opening and no tags.
- **The contract states the opposite rule.**
  - The design's [Selection belongs to the link](https://github.com/m2ux/prosiform/blob/7f9ac79024860197012595d8c54359a25ce559f4/artifacts/planning/2026-10-17-prosiform-v1/design.md#L451) and its [Presets fixture family](https://github.com/m2ux/prosiform/blob/7f9ac79024860197012595d8c54359a25ce559f4/artifacts/planning/2026-10-17-prosiform-v1/design.md#L811) say a Mermaid tooltip selects no preset.
  - The fixture [`diagram-tooltips-supply-no-preset-selection`](https://github.com/m2ux/prosiform/tree/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/fixtures/reference/diagram-tooltips-supply-no-preset-selection) encodes it.
- **The documentation states it.**
  [Diagram links](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/references.md#L123), the glossary's [pick](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/glossary.md#L30) and [Exactly one alternative is in force](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/selection.md#L45) say a diagram link carries no operator and selects no preset.

## Proposal

- **The tooltip's opening marks are the operator.**
  Marks opening a `click` tooltip, or a class diagram `link` tooltip, followed by a blank or the tooltip's end, state the operator under the [Operators](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/references.md#operators) rules, combinations and refusals included. A mark followed directly by text opens none.
- **The rest is the title.**
  The tooltip after the marks and blank, or the whole tooltip where no mark opens it, is read through the shared title-tag reader, `?` included.
- **Publication follows the operator.**
  The destination is published as each operator states for a link; the tooltip and every other byte of the fence are carried as written.
- **The retired rule leaves.**
  Each statement and fixture saying a tooltip selects nothing or a diagram link carries no operator is replaced or removed.
- **The documentation follows the build.**
  The Diagram links section states the rule once, and the glossary and selection pages link it.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-click-titles/e00/w00.md) | The v1 design states click tooltips | AC1 | | | | |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-click-titles/e00/w01.md) | Click tooltip read as operator and title | AC2, AC3, AC4 | W00 | W02 | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-click-titles/e00/w02.md) | Corpus fixtures for click tooltips | AC5 | W00 | W01 | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-click-titles/e00/w03.md) | The documentation states click tooltips | AC6 | W01, W02 | | | |

## Acceptance Criteria

- [ ] **AC1.** The v1 design states that a Mermaid click's or class diagram link's tooltip carries the link's operator and title, and holds no statement that a Mermaid tooltip selects no preset, as a read of its Presets, Link classification and fixture-family sections shows.
- [ ] **AC2.** A click, written with or without `href`, or a class diagram link whose tooltip opens with operator marks followed by a blank or the tooltip's end is read with that operator, accepted and refused as the same marks opening a Markdown link's text are, as `test_source.py` shows.
- [ ] **AC3.** A click's tooltip, less its opening marks and blank, selects presets and carries the pick token as a Markdown link's title does, as `test_source.py` and `test_cli.py` show.
- [ ] **AC4.** A dispatched, deferred, parallel or composed click publishes its destination as that operator's Markdown link does, with its tooltip and the rest of its fence as written, as `test_cli.py` shows.
- [ ] **AC5.** The corpus holds a fixture for each click tooltip rule, a dispatch, a deferral, a preset selection, a pick and a refused combination, and none stating that a Mermaid tooltip selects no preset, as `make corpus` and `make conformance` show.
- [ ] **AC6.** The Diagram links section states the click tooltip rule, and no documentation page or module docstring states that a diagram link carries no operator or selects no preset, as a search of `docs/` and `src/prosiform/` and `make links` show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-click-titles) — the tooltip design, the defaults taken and why the build and its fixtures share a pull request.
