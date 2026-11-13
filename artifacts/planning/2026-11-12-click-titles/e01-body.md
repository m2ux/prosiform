## Overview

`pf` takes a link exactly as a bundle publishes it, a Markdown link or a diagram `click` line, and reads its destination, section and presets itself, setting aside the operator marks that direct the agent. A deferral leaving the pick to the agent takes `--pick` beside the unedited link, and `--presets` leaves the interface. The epic removes the conversion an agent makes between a published link and a command.

## Problem

- **An agent converts each link into a command.**
  The [usage](https://github.com/m2ux/prosiform/blob/c77dba6a707023fe09bcac505ae3ec11dbccaa7e/src/prosiform/cli.py#L323-L343) has the agent split a link into `<document>#<section>` and a `--presets` value, and the entry [refuses a Markdown link](https://github.com/m2ux/prosiform/blob/c77dba6a707023fe09bcac505ae3ec11dbccaa7e/src/prosiform/cli.py#L1086).
- **A click's tooltip is not its title.**
  A click's tooltip opens with its operator marks, so an agent passing `"¬ Epic"` as `--presets '¬ Epic'` selects no preset and loops on `E_ALTERNATIVE_UNRESOLVED`.
- **A pick edits the link.**
  The guide's [pick instruction](https://github.com/m2ux/prosiform/blob/c77dba6a707023fe09bcac505ae3ec11dbccaa7e/src/prosiform/cli.py#L364-L366) and the failure's [remedy](https://github.com/m2ux/prosiform/blob/c77dba6a707023fe09bcac505ae3ec11dbccaa7e/src/prosiform/cli.py#L836) have the agent rewrite the title with `?` replaced.

## Proposal

- **The link is the argument.**
  `pf -o <folder> '<link>'` takes a Markdown link or a diagram `click` or class diagram `link` line as published, read by the readers that already classify links; a plain path stays the bootstrap entry.
- **Operator marks are the agent's.**
  Marks opening a link's text or a tooltip direct the agent that reads the bundle; the entry strips them unchecked and compiles the destination with the link's presets.
- **A pick is its own option.**
  `--pick <alternative>` beside a link whose title carries `?` puts that alternative in force, on the first run or after the listing, which names `--pick` as its remedy.
- **A stray pick is invalid usage.**
  `--pick` beside an entry whose title carries no `?`, a plain path included, exits `2`.
- **`--presets` is removed.**
  The option, its usage text, fixtures, checks and eval harness invocations leave; a fixture selecting presets uses a link entry.
- **The guide states one instruction.**
  Run `pf` on the link as written, adding `--pick` when the link defers and the agent knows its pick or `pf` lists alternatives.
- **Another initiative's wording follows the build.**
  Preset Alternatives' statement that a pick passes as `--presets` is reworded once the documentation lands.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-13-750-i17-e01-w00-the-v1-design-states/) | The v1 design states link invocation | AC1 | [E00:W00](https://github.com/m2ux/prosiform/issues/739) | | | |
| W01 | pf reads a published link as entry | AC2, AC3, AC4 | W00, [E00:W01](https://github.com/m2ux/prosiform/issues/739) | W02, W03 | | |
| W02 | Corpus fixtures for link entries | AC5 | W00, [E00:W02](https://github.com/m2ux/prosiform/issues/739) | W01 | | |
| W03 | Checks and eval harness pass links | AC6 | W00 | W01 | | |
| W04 | Documentation states one invocation instruction | AC7 | W01, W02, W03, [E00:W03](https://github.com/m2ux/prosiform/issues/739) | | | |

## Acceptance Criteria

- [ ] **AC1.** The v1 design states that an entry is a published Markdown or diagram link or a plain path, that `--pick` resolves a `?` deferral and is invalid usage elsewhere, and holds no `--presets` option, as a read of its invocation and Presets sections shows.
- [ ] **AC2.** `pf` given a published Markdown link, `click` line or class diagram `link` line compiles its destination and section with the presets its title or tooltip selects, the same whatever operator marks open it, malformed combinations included, as `test_cli.py` shows.
- [ ] **AC3.** `--pick` beside a link carrying `?` compiles the named alternative, the alternatives listing names `--pick` as its remedy, and `--pick` beside an entry carrying no `?` exits `2`, as `test_cli.py` shows.
- [ ] **AC4.** `pf -h`, the guide and `invocation.md` state the link entry and `--pick`, and the build accepts no `--presets`, as `make invocation` and `test_cli.py` show.
- [ ] **AC5.** The corpus holds a fixture for a link entry opening with operator marks, a diagram link entry, a first-run pick, a pick after the listing and a stray pick, and no manifest passes `--presets`, as `make corpus` and `make conformance` show.
- [ ] **AC6.** The smoke check and the diagram-following eval harness invoke `pf` with links as written and `--pick`, and neither passes `--presets`, as `make smoke` and `make eval-harness` show.
- [ ] **AC7.** The README, `docs/` and Preset Alternatives' issue body state the link invocation and `--pick`, and none mentions `--presets`, as a search of each and `make links` show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-click-titles) — the invocation decisions, the joins and the release that ships them.
- **R2.** [pf takes a published link verbatim](https://github.com/m2ux/prosiform/issues/747) — the raised design this epic carries.

