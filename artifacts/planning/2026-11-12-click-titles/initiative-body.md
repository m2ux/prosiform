## Overview

A Mermaid `click` line's quoted tooltip is read as the link's title: marks opening it state the link's operator, and the rest selects presets as a Markdown link's title does. A click can then be a dispatch, a deferral or any other operator, and can pick an alternative. The goal the reviews test against: `click Intake href "activities/intake.md" "⇉"` bundles as a dispatch and `"¬"` as a deferral, in a released build.

## Problem

A diagram link follows its destination and ignores everything else on its line, so a click can carry no operator and select no preset.

- **The tooltip is read past.**
  [`CLICK_LINE`](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/src/prosiform/source.py#L159-L163) captures the destination and skips the quoted tooltip after it, and [each click becomes a use](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/src/prosiform/source.py#L1210-L1214) opening with nothing and carrying no tags.
- **The contract states the gap as a rule.**
  The design's [Selection belongs to the link](https://github.com/m2ux/prosiform/blob/7f9ac79024860197012595d8c54359a25ce559f4/artifacts/planning/2026-10-17-prosiform-v1/design.md#L451) says a Mermaid tooltip selects no preset, and [Diagram links](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/references.md#L123) says a diagram link carries no operator.
- **A diagram cannot dispatch.**
  A workflow drawn as a flowchart whose nodes are sub-agent units must restate each click as a Markdown link to mark it `⇉`, and a document declaring alternatives reached through clicks alone [fails](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/selection.md#L45).

## Proposal

- **The tooltip is the link's title.**
  Marks opening a click's tooltip, followed by a blank or its end, state the operator as Markdown link text's marks do; the remainder is read as a Markdown link's title.
- **One rule for quoted diagram destinations.**
  A class diagram's `link` with a tooltip reads the same way.
- **The contract states it.**
  The design, the corpus and the documentation state the rule, and the rule they replace leaves.
- **A release carries it.**
  A release cut under the project's versioning procedure ships the behaviour.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/739) | Click Titles | AC1, AC2 | | |
| [E01](https://github.com/m2ux/prosiform/issues/740) | Click Titles Release | AC3 | [E00](https://github.com/m2ux/prosiform/issues/739) | |

## Acceptance Criteria

- [ ] **AC1.** A Mermaid click's quoted tooltip states the link's operator and selects its presets as a Markdown link's opening marks and title do, so a click bundles as a dispatch, a deferral or any other operator, as the contract corpus shows.
- [ ] **AC2.** The design and the documentation state the click tooltip rule, and neither holds a claim that a diagram link carries no operator or that a Mermaid tooltip selects no preset, as a search of both and `make links` show.
- [ ] **AC3.** A release's paired contract and Python tags name a commit on `main` that carries the click tooltip rule, its number chosen by the previous contract tag's corpus, as the release pull request and `pf -v` on the tagged commit show.

## Non-Goals

- It gives a sequence diagram's `link` or `links` destinations no operator, since neither carries a tooltip.
- It reads no operator or preset from a node label.
- It changes no other operator rule.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-click-titles) — the goal, defaults taken, goal trace and work items.
- **R2.** **Source.** [Decisions](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-click-titles/decisions.md) — the goal and the tooltip design the criteria answer to.
- **R3.** **Source.** [Cutting a release](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/versioning.md#cutting-a-release) — the release procedure the last criterion answers to.
