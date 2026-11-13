## Overview

A Mermaid `click` line's quoted tooltip is read as the link's title: marks opening it state the link's operator, and the rest selects presets as a Markdown link's title does. A click can then be a dispatch, a deferral or any other operator, and can pick an alternative. `pf` takes any published link as written, with `--pick` for a deferral. The goal the reviews test against: `click Intake href "activities/intake.md" "⇉"` bundles as a dispatch and `"¬"` as a deferral, and `pf` run on either line as written compiles its destination, in a released build.

## Problem

A diagram link follows its destination and ignores everything else on its line, so a click can carry no operator and select no preset.

- **The tooltip is read past.**
  [`CLICK_LINE`](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/src/prosiform/source.py#L159-L163) captures the destination and skips the quoted tooltip after it, and [each click becomes a use](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/src/prosiform/source.py#L1210-L1214) opening with nothing and carrying no tags.
- **The contract states the gap as a rule.**
  The design's [Selection belongs to the link](https://github.com/m2ux/prosiform/blob/7f9ac79024860197012595d8c54359a25ce559f4/artifacts/planning/2026-10-17-prosiform-v1/design.md#L451) says a Mermaid tooltip selects no preset, and [Diagram links](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/references.md#L123) says a diagram link carries no operator.
- **An agent rewrites each link into a command.**
  The [usage](https://github.com/m2ux/prosiform/blob/c77dba6a707023fe09bcac505ae3ec11dbccaa7e/src/prosiform/cli.py#L323-L343) has an agent split a link into a destination and a `--presets` value, which a tooltip opening with operator marks defeats.
- **A diagram cannot dispatch.**
  A workflow drawn as a flowchart whose nodes are sub-agent units must restate each click as a Markdown link to mark it `⇉`, and a document declaring alternatives reached through clicks alone [fails](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/selection.md#L45).

## Proposal

- **The tooltip is the link's title.**
  Marks opening a click's tooltip, followed by a blank or its end, state the operator as Markdown link text's marks do; the remainder is read as a Markdown link's title.
- **One rule for quoted diagram destinations.**
  A class diagram's `link` with a tooltip reads the same way.
- **The contract states it.**
  The design, the corpus and the documentation state the rule, and the rule they replace leaves.
- **The link is the command.**
  `pf` takes a published Markdown or diagram link as written and decodes it, a deferral takes its pick as an option of its own, and `--presets` leaves.
- **A release carries it.**
  A release cut under the project's versioning procedure ships the behaviour.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/739) | Click Titles | AC1, AC2 | | ✓ |
| [E01](https://github.com/m2ux/prosiform/issues/750) | Link Invocation | AC4, AC6 | | ✓ |
| [E02](https://github.com/m2ux/prosiform/issues/740) | Click Titles Release | AC3, AC5 | [E00](https://github.com/m2ux/prosiform/issues/739), [E01](https://github.com/m2ux/prosiform/issues/750) | |

## Acceptance Criteria

- [x] **AC1.** A Mermaid click's quoted tooltip states the link's operator and selects its presets as a Markdown link's opening marks and title do, so a click bundles as a dispatch, a deferral or any other operator, as the contract corpus shows.
- [x] **AC2.** The design and the documentation state the click tooltip rule, and neither holds a claim that a diagram link carries no operator or that a Mermaid tooltip selects no preset, as a search of both and `make links` show.
- [ ] **AC3.** A release's paired contract and Python tags name a commit on `main` that carries the click tooltip rule and the link invocation, as the release pull request and `pf -v` on the tagged commit show.
- [x] **AC4.** `pf` given a published Markdown link or diagram link as written compiles the destination with the presets it carries, whatever operator marks open it, as the contract corpus and `make smoke` show.
- [ ] **AC5.** That release's number is the one the previous contract tag's corpus chooses, as the release pull request's recorded corpus run shows.
- [x] **AC6.** A deferral link given a pick option compiles the picked alternative, as the contract corpus shows.

## Non-Goals

- It gives a sequence diagram's `link` or `links` destinations no operator, since neither carries a tooltip.
- It reads no operator or preset from a node label.
- It changes no other operator rule.
- It gives an operator mark no effect on what an entry compiles.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-click-titles) — the goal, defaults taken, goal trace and work items.
- **R2.** **Source.** [Decisions](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-click-titles/decisions.md) — the goal and the tooltip design the criteria answer to.
- **R3.** **Source.** [Cutting a release](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/versioning.md#cutting-a-release) — the release procedure the last criterion answers to.
- **R4.** **Source.** [pf takes a published link verbatim](https://github.com/m2ux/prosiform/issues/747) — the invocation design the link criterion answers to.
