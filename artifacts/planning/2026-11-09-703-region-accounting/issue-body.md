## Overview

A skill's mode compiled with `pf` 0.23.0 fails its bundle's no-accidental-expansion check: the candidate holds a few more regions than provenance accounts for, and the run reports `E_UNEXPECTED_INTERNAL_ERROR`. Nine of eleven entries of one skill fail this way. Provenance accounts for every region the candidate holds, so those entries compile.

Target: `main`

## Problem

- **Most of a real skill cannot compile.**
  With `prosiform: {}` declared on every document of the work-planner skill, SKILL.md and seven of its ten modes fail with `Invalid('no accidental expansion: the candidate holds 3036 region(s) against the 3028 the provenance accounts for')` or the same with other counts (474/473 to 3036/3028). Two modes compile.
- **An internal error is a defect whatever the source.**
  Either the sources hold a construct the profile should refuse with its own code, or the build counts a region it emitted without recording it.

## Proposal

- **The trigger is isolated to a minimal fixture.**
  The smallest work-planner excerpt that reproduces the mismatch becomes a corpus fixture.
- **Provenance accounts for every region the candidate holds.**
  The fix is made where the build emits or records the region, so the check holds for valid sources. A source outside the profile is refused with its documented code.
- **The contract moves a minor.**
  A fixture is added; the release is `contract/v0.24.0` and `python/v0.24.0`, cut after merge.

## Acceptance Criteria

- [ ] **AC1.** The minimal source that raised the mismatch compiles, or is refused with a documented code, as `make corpus` shows.
- [ ] **AC2.** A copy of the work-planner skill with `prosiform: {}` on every document compiles each mode with exit 0, or fails only `E_RESOURCE_LIMIT`.
- [ ] **AC3.** `make check` passes.

## References

- **R1.** [#700](https://github.com/m2ux/prosiform/issues/700) — F08, the release the failure reproduces on.
- **R2.** [Bundle invariants](https://github.com/m2ux/prosiform/blob/940f59254/docs/validation.md) — the no-accidental-expansion check.
