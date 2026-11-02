## Overview

The Rust build is the `pf` agents invoke. Both builds bundle every corpus input and agree, every dependency is pinned, the corpus runner, continuous integration and the repository checks take the Rust build as their primary target, a released binary installs from one documented path, every caller resolves the command to it, and the Python build remains only as the differential oracle.

## Problem

A build that passes the corpus is not yet the tool in use.

- **Two implementations diverge quietly.**
  A behaviour no fixture declares can differ between the builds without any fixture failing.

- **An unpinned dependency changes the contract.**
  Parser behaviour on duplicate definitions, offsets and option-controlled extensions is what the profile rests on, so an unpinned upgrade can change how existing source is interpreted.

- **The checks prove the prototype.**
  The corpus runner, continuous integration and the repository checks invoke the Python entry point, so a passing run says nothing about the build agents would be given.

- **No binary reaches a caller.**
  `pf` installs from the Python package, and the Rust build has no release and no install path.

- **Callers resolve the command to the prototype.**
  The skill bootstrap, dispatch and the delivery wrapper run whatever `pf` is installed, which is the Python build.

- **Two delivered builds are two products.**
  While the prototype stays installable as `pf`, a caller can reach either build, and a defect report names neither.

## Proposal

- **Both builds run every input.**
  A differential run bundles each corpus input with both builds and compares the results byte for byte, so a divergence outside the declared expectations is still a failure.

- **Pins come after the fixtures pass.**
  Exact versions are chosen once the corpus holds against them, and the lockfile is what every run uses.

- **The Rust build is the primary target.**
  The corpus runner, the repository checks and continuous integration run the Rust build by default, and the prototype runs where it is named.

- **One released binary.**
  A tagged release publishes a versioned binary with one documented install path, and the invocation documentation is checked against that binary's own help.

- **Callers move at one recorded point.**
  Every caller resolves `pf` to the Rust binary from one recorded release onward.

- **The prototype stays as the oracle.**
  Its install path as `pf` is removed, and it keeps running in the differential job.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/17) | Differential Conformance | AC1, AC2 | [I13:E05](https://github.com/m2ux/prosiform/issues/16) | |
| [E01](https://github.com/m2ux/prosiform/issues/533) | Corpus Migration | AC3 | [E00](https://github.com/m2ux/prosiform/issues/17) | |
| [E02](https://github.com/m2ux/prosiform/issues/534) | Release Distribution | AC4, AC5 | [E00](https://github.com/m2ux/prosiform/issues/17) | |
| [E03](https://github.com/m2ux/prosiform/issues/535) | Caller Cut-Over | AC6 | | |
| [E04](https://github.com/m2ux/prosiform/issues/536) | Python Retirement | AC7 | [E01](https://github.com/m2ux/prosiform/issues/533), [E03](https://github.com/m2ux/prosiform/issues/535) | |

## Acceptance Criteria

- [ ] **AC1.** Both builds produce identical output for each corpus input, as the differential run in continuous integration shows.
- [ ] **AC2.** Every dependency of the production build is pinned to an exact version against which the corpus passes, as the lockfile and the pinned run show.
- [ ] **AC3.** The corpus runner, the repository checks and continuous integration run the production build as their primary target, as the checks workflow shows.
- [ ] **AC4.** A production binary installed from the documented install path bundles a reference from a source root, as the released-build smoke run shows.
- [ ] **AC5.** The repository documents the command's options, defaults, exit statuses and profile identifier, as the invocation check against the production binary's own help output shows.
- [ ] **AC6.** An agent following the skill bootstrap compiles and follows a bundle with the production binary, as the agent smoke run shows.
- [ ] **AC7.** No documented install path delivers the prototype as the command, as the install check shows.

## Non-Goals

- It does not change the behavioural contract or a corpus fixture without a recorded decision.
- It does not remove the prototype, which stays in use as the differential oracle.
- It does not open an issue or a pull request on another project.

## References

- **R1.** **Source.** [v1 design](https://github.com/m2ux/prosiform/blob/d45c7f08f3878e71d9d0a99ae728fc69fc21f174/artifacts/planning/2026-10-17-prosiform-v1/design.md) — the CLI contract the released binary and its documentation answer to.
- **R2.** [Planning decisions](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) — why the prototype is retained as the oracle, and why cut-over is its own initiative on its own board.
- **R3.** [Proposal](https://github.com/m2ux/prosiform/issues/1) — the originating proposal: the scoped problem and the goal clauses these criteria trace to.
- **R4.** [I13 Production Build](https://github.com/m2ux/prosiform/issues/532) — the Rust build this initiative cuts over to.
