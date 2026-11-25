## Overview

`make eval-harness` fails 39 tests on `main`, left by three merged changes the tests had not followed. This pull request brings the eval's walk and tests to the current contract, so the suite passes. `make check` does not run the suite, which is why the failures reached `main`.

## Changes

### Deferred-Line Walks

- **Read a deferred line from the form's root.**
  A bundle names each `↳` line's target from the folder it is in, since #819. `rooted` reads each line from the form's root, naming the same target, wherever the walk reads a bundle: the entry's, each run's and each dispatched bundle a sub-agent follows. Stated runs keep the names their scenarios give.
- **Read raw bundles the same way.**
  The tests that compare a bundle's lines with a stated target read the bundle through `rooted`.

### Brief Sections

- **Find a brief by the dispatch's name.**
  A named brief's sub-section is headed by the dispatch's text, since #841, and the dispatch line inside it keeps its mark. The tests select and hold the sub-section that way.

### Guide Opening

- **Hold a bare run to the build's guide.**
  The tests compare a bare `pf` run's output with `prosiform.cli.GUIDE`, which opens on following a bundle since #810.

### Out of Scope

- **Live sessions.**
  A live session still cannot bundle a deferred line its bundle set carries: the runner copies bundles made in a temporary folder, and the instruction and sandbox predate #819. [F40, #853](https://github.com/m2ux/prosiform/issues/853) holds it.

## Test Plan

| Test | Description | Coverage | Pass |
| --- | --- | --- | --- |
| T1 | `make eval-harness` | AC1 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-852-eval-harness/test-results.md#eval-harness) |
| T2 | Each cluster run before and after the merge that broke it | AC2 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-852-eval-harness/test-results.md#failing-clusters) |
| T3 | `make check` | AC1 | [Pass](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-852-eval-harness/test-results.md#full-check) |

## References

- **R1.** [Test results](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-852-eval-harness/test-results.md) — The validation at head e298a4604 and the change each cluster started failing at.
- **R2.** [Planning record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-852-eval-harness/README.md) — The commits, the open decision and the live defect.
