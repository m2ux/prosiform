## Overview

The agent-pick scenarios score a pick by either path the guide gives an agent: `--pick` on its first run, or the alternatives listing followed by the rerun. A session following the guide scores as compiled.

## Problem

- **A guide-compliant pick fails scoring.**
  The agent-pick scenarios [hold a session to the listing run and the picked rerun](https://github.com/m2ux/prosiform/blob/c77dba6a707023fe09bcac505ae3ec11dbccaa7e/evals/diagram-following/workflows/agent-pick/scenarios.toml#L18-L24), so a session passing `--pick` on its first run, as the guide tells an agent that knows its pick, scores as uncompiled.

## Proposal

- **Either pick satisfies a scenario.**
  A scenario's picked run is met by a first-run `--pick` or by the listing followed by the rerun, and the scorer states which path the session took.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/pull/762) | Agent-pick scoring accepts a first-run pick | AC2 | [E01:W05](https://github.com/m2ux/prosiform/issues/709), [I17:E01:W01](https://github.com/m2ux/prosiform/issues/750), [I17:E01:W03](https://github.com/m2ux/prosiform/issues/750) | | | ✓ |

## Acceptance Criteria

- [x] **AC2.** A session that passes `--pick` on its first run of an agent-pick scenario's link, and one that reruns after the listing, each score as compiled, as `make eval-harness` shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-preset-alternatives) — the decisions placing this epic and moving the real-use agent-pick run to the real-use eval.
- **R2.** [Agent-pick scenarios accept a first-run pick](https://github.com/m2ux/prosiform/issues/754) — the scoring gap the first-run pick opened.

