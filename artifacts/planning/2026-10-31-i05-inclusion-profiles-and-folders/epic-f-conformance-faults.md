## Overview

The fault a run performs on itself moves from `-x` to `PROSIFORM_FAULT`. The option leaves the command line, the help output and the documented table, and the three faults stay testable because the corpus runner is what sets the variable.

## Problem

A shipped flag exists only for tests, and every surface presents it as a feature.

- **It sits among the options.** `pf -h` lists `-x {source-changed,internal,cleanup-refused}` beside `-o` and `-c`, where a reader has no reason not to try it.
- **The documented table states it.** `invocation.md` carries a row for it, and `make invocation` holds that table to the help output, so the option is presented as part of the contract a caller may use.
- **Nothing in a real run wants it.** A caller has no reason to ask the tool to fail in itself, to change a source's bytes, or to refuse its own cleanup. The only consumer is the corpus.
- **The corpus already abstracts it.** A manifest declares `fault = "internal"` and `runner.py` translates that into the command line, so the build's way of receiving the fault is already separated from how a fixture states it.

## Proposal

- **The variable is the only channel.** `PROSIFORM_FAULT` holds one fault name, and the run reads it where `options.fault` was read. `-x` is removed from the parser, the help output and the option table.
- **The runner sets it.** `runner.py` reads a manifest's `fault` field and passes it as an environment variable beside the working directory it already controls, so no fixture changes.
- **The three faults are unchanged.** `source-changed`, `internal` and `cleanup-refused` keep their names, their positions and their effects.
- **The contract states it in a section of its own.** The design gains a *Conformance faults* section rather than an option row: what the variable holds, that a run without it performs no fault, and that the mechanism exists so clauses no source tree can reach carry fixtures.
- **An unrecognized value is refused.** A variable holding anything but the three names fails as invalid usage, so a mistyped conformance setting is a fault rather than a silent pass.
- **`make invocation` loses the comparison for it.** The row goes with the option, so the two-way check no longer has it to compare — which is the point: it stops being presented as an option.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause, the variable | AC7 | [I08:E03](https://github.com/m2ux/prosiform/issues/449) | | |
| W01 | The parser and the run reading the variable | AC1, AC6 | W00, [I08:E00:W00](https://github.com/m2ux/prosiform/issues/434) | | |
| W02 | The runner setting it from a manifest | AC2 | W01 | | |
| W03 | The option table and the help output | AC3 | W01 | | |
| W04 | The declaration the corpus carries | AC4 | W02 | | |
| W05 | The three fixtures unchanged | AC5 | W02 | | |

## Acceptance Criteria

- [ ] **AC1.** `PROSIFORM_FAULT=internal` makes a run fail in itself with exit status `4`, and a run without it performs no fault, as the corpus fixture `fixtures/diagnostics/a-run-that-fails-in-itself` shows.
- [ ] **AC2.** A manifest declaring `fault` reaches the build through the environment, and no fixture passes the option, as `make corpus` shows.
- [ ] **AC3.** `pf -h` and the documented option table name no `-x`, and agree in both directions, as `make invocation` shows.
- [ ] **AC4.** The corpus states the fault as a manifest field and the runner translates it, so a fixture names no command-line spelling, as an inspection of `fixtures/README.md` and `runner.py` shows.
- [ ] **AC5.** All three faults remain reachable: the fixtures for `source-changed`, `internal` and `cleanup-refused` pass unchanged, as `make corpus` shows.
- [ ] **AC6.** A `PROSIFORM_FAULT` holding a value outside the three fails as invalid usage with exit status `2`, as the corpus fixture `fixtures/cli/an-unknown-fault-is-invalid-usage` shows.
- [ ] **AC7.** The design states the variable, its values and why the mechanism exists, in a section of its own rather than among the options, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.

## References

- **R0.** Epic — [I08:E04 Faults Out of the Option Surface](https://github.com/m2ux/prosiform/issues/450).
- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions this change comes from.
