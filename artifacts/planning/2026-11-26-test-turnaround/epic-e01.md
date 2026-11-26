## Overview

This epic shortens the work between a change to the build and a green tree. One run names every failing check, a fixture whose output moved is restated by a command and read as a diff, and a behaviour the corpus holds is held nowhere else. Within the initiative it is the work on what a failing tree reports and on what restating it writes.

## Problem

A change to the build is paid for again in the tests and fixtures around it.

- **Expected output is restated by hand.**
  [The bundle comparison](https://github.com/m2ux/prosiform/blob/b0eb7a2335436f2ce9c35546d3bfd2e39f7ae3be/checks/runner.py#L284-L342) reports a difference and writes nothing, so a change to bundle text or names is typed into each fixture it reaches.
- **A failing tree reports one failure.**
  [The check target](https://github.com/m2ux/prosiform/blob/b0eb7a2335436f2ce9c35546d3bfd2e39f7ae3be/Makefile#L78) stops at its first failing target, so each further failure costs another run.
- **One fixture's verdict costs a run of every fixture.**
  [The corpus runner](https://github.com/m2ux/prosiform/blob/b0eb7a2335436f2ce9c35546d3bfd2e39f7ae3be/checks/corpus.py#L256) takes no fixture to run, so a change to one is read from a run of all.
- **A crash and a drift are one verdict.**
  [The result's passed check](https://github.com/m2ux/prosiform/blob/b0eb7a2335436f2ce9c35546d3bfd2e39f7ae3be/checks/runner.py#L127) is false for a fixture whose output moved and for one whose run failed in itself.
- **One behaviour is held twice.**
  [The command-line tests](https://github.com/m2ux/prosiform/blob/b0eb7a2335436f2ce9c35546d3bfd2e39f7ae3be/src/tests/test_cli.py#L233-L260) run the command end to end, as a fixture does, so a behaviour change is restated in both.

## Proposal

- **One run reports the set.**
  A second make target runs every check whether or not an earlier one failed, and names each that did.
- **The runner takes a fixture's identity.**
  The selected fixture is run by the comparison the corpus run performs and reported under the same identity.
- **A fixture's verdict has three states.**
  A run met its manifest, its output moved, or it failed in itself. Only the second is drift.
- **Drift is classified before it is restated.**
  Triage names each stale fixture under one declared category, and a category can be selected.
- **Restatement writes the bundles and their names.**
  It is dry unless asked to write, and it writes the expected bundles and the manifest's `bundles` entry. Every other line of the manifest is copied through.
- **Restatement refuses what a reader must decide.**
  A fixture whose run failed in itself, whose exit status or diagnostics differ, or whose run writes a different number of bundles than declared is named and left alone.
- **The corpus owns what an invocation can state.**
  Each command-line test is read against the fixtures reaching the same code. One a fixture already holds is removed once the user approves it.
- **Boundary with the repository checks epic.**
  A check that reads or refuses the wrong thing stays there. This epic holds what a failing tree reports and what restating it costs.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/issues/255) | Whether a tree is sound | AC1, AC2 | | | | |
| [W02](https://github.com/m2ux/prosiform/issues/243) | A stale fixture classified before it is rewritten | AC3, AC4, AC5 | W01 | | | |
| [W03](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-test-turnaround/w03.md) | Restatement that writes only the bundles | AC6, AC7, AC8 | W02 | W04 | | |
| [W04](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-test-turnaround/w04.md) | Restatement refuses what a reader decides | AC9, AC10, AC11 | | W03 | | |
| [W05](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-test-turnaround/w05.md) | Command-line tests read against the corpus | AC12 | | | | |
| [W06](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-test-turnaround/w06.md) | Approved command-line tests removed | AC13, AC14 | W05 | | | |
| [W07](https://github.com/m2ux/prosiform/issues/189) | One fixture run by its identity | AC15 | | | | |

## Acceptance Criteria

- [ ] **AC1.** `make check-all` names every failing target among those the `check` target names, as a tree with two failing targets shows.
- [ ] **AC2.** A fixture whose run failed in itself is distinguished from one whose output moved, as the runner's result for each of the two shows.
- [ ] **AC3.** Triage reports each fixture's difference as one declared category, and a run over a corpus holding one of each category names each fixture under its own, as that run shows.
- [ ] **AC4.** `--only` reports fixtures in the selected drift category alone, as a run over a corpus holding two categories with one selected shows.
- [ ] **AC5.** A green corpus run produces no drift report, as the tool run over `make corpus`'s passing tree shows.
- [ ] **AC6.** Restatement without `--write` leaves the working tree unmodified and names every fixture it would rewrite, as `git status` after a run over a corpus with one stale fixture shows.
- [ ] **AC7.** Restatement with `--write` replaces only the expected bundles and the manifest's `bundles` entry, as a manifest carrying a non-ASCII clause and a second declaration compared before and after shows.
- [ ] **AC8.** Triage and restatement are reachable from the corpus guide and import the corpus's own runner, as the repository's file check and a read of the imports show.
- [ ] **AC9.** Restatement refuses a fixture whose run failed in itself and names it, as a corpus holding one such fixture shows.
- [ ] **AC10.** Restatement refuses a fixture whose exit status or diagnostics differ from its manifest and names it, as a corpus holding one such fixture shows.
- [ ] **AC11.** Restatement refuses a fixture whose run writes a different number of bundles than its manifest declares and names it, as a corpus holding one such fixture shows.
- [ ] **AC12.** Every test in `src/tests/test_cli.py` has a row in the overlap table naming the fixtures that hold its assertion or stating that none does, as the table compared with the tests pytest collects from that file shows.
- [ ] **AC13.** No test the overlap table records as approved for removal is collected from `src/tests/test_cli.py`, as the table compared with pytest's collection shows.
- [ ] **AC14.** Every clause the conformance report lists as covered at the revision before the removal is listed as covered after it, as `make conformance` at both revisions shows.
- [ ] **AC15.** The corpus runner asked for one fixture by its identity reports that fixture's verdict under that identity, by the comparison the corpus run performs, and refuses an identity no fixture carries, as the corpus harness shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-test-turnaround) — the measurements behind this epic, its decisions and each work item.
- **R2.** [Preserved tools and their evidence](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-24-corpus-drift-tools) — the triage and regeneration scripts an earlier session wrote, with the runs that establish each property.
- **R3.** [Fixture guide](https://github.com/m2ux/prosiform/blob/b0eb7a2335436f2ce9c35546d3bfd2e39f7ae3be/fixtures/README.md) — what a manifest declares and what `expected/` holds.
