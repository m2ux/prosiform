## Overview

`make eval-harness` fails 15 tests on `main` at f890d8522. #849 shortened the preset qualifier in bundle file names, and #854 merged beside it, so neither pull request's checks saw the two together; CI runs neither through the suite. This pull request names an entry's bundle by the build's own function, so the eval reads the files `pf` writes.

## Changes

### Bundle Names

- **Take the build's name.**
  `entry_bundle` in `workflow.py` takes `prosiform.cli.selection_name` and `bundle_file`. The eval derived the name itself, with the full SHA256 qualifier #849 replaced, and looked for files no run wrote.

## Test Plan

| Test | Description | Coverage | Pass |
| --- | --- | --- | --- |
| T1 | `make eval-harness` on `main` at f890d8522 | AC1 | [15 failures](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-852-eval-harness/test-results.md#main-after-merge) |
| T2 | `make eval-harness` at this head | AC1 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-852-eval-harness/test-results.md#bundle-names) |
| T3 | `make check` at this head | AC1 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-852-eval-harness/test-results.md#bundle-names) |

## References

- **R1.** [Test results](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-852-eval-harness/test-results.md) — The suite on `main` after both merges, and at this head.
- **R2.** [#854](https://github.com/m2ux/prosiform/pull/854) — The first delivery of #852, merged.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
