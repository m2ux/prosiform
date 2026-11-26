## Overview

Every rule the repository's checks and its design record state is stated exactly: each check reports what it claims to and refuses what it claims to refuse. A contributor reading a check's output learns what the check read, what it passed over and why it failed, a stale fixture is restated without rewriting what the run did not establish, and a behaviour a fixture holds is held by no command-line test beside it. The goal the reviews test against: no check passes over, accepts or rewrites anything its own rule says it reads, refuses or keeps.

## Problem

The repository's checks and design record state some rules imprecisely, and nothing a run of the tool produces shows it.

- **A check passes over what its rule says it reads.**
  The link check skips content inside a list item that holds an indented code block, and the document checks skip a Markdown file present and not tracked.
- **A check accepts what its rule says it refuses.**
  A build tag whose version the build does not report, a corpus declaration naming a build word or an avoided term, and a function nothing calls all pass today.
- **A failing run does not say what failed.**
  `make check` stops at its first failing target, the corpus runner cannot run one fixture by its identity, and a fixture that failed in itself reads the same as one whose output moved.
- **Restating a fixture rewrites more than its expectation.**
  No command restates only the declared output of a stale fixture, or refuses a fixture whose run failed in itself.
- **One behaviour is held twice.**
  [The command-line tests](https://github.com/m2ux/prosiform/blob/b0eb7a2335436f2ce9c35546d3bfd2e39f7ae3be/src/tests/test_cli.py#L233-L260) run the command end to end, as a fixture does, so a behaviour change is restated in both.

## Proposal

- **Each rule is stated once, where its check lives.**
  A row's issue holds the rule and the criterion stating what fixing it makes true, and the fix lands in the check that states the rule.
- **Product behaviour stays out.**
  A fix that would change what a run of `pf` produces belongs to the initiative that ships it.
- **A failing tree explains itself.**
  One make target reports every failing check, and the corpus runner distinguishes a fixture that failed in itself from one whose output moved.
- **Restatement writes only what the run established.**
  Drift is triaged into declared categories before any rewrite, and restatement replaces only the expected bundles and their names.
- **The corpus owns what an invocation can state.**
  A command-line test a fixture already holds is removed once the user approves it.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/187) | Repository Checks | AC1, AC2 | | ✓ |
| [E01](https://github.com/m2ux/prosiform/issues/858) | Change Turnaround | AC3, AC4, AC5 | | ✓ |
| [E02](https://github.com/m2ux/prosiform/issues/877) | Check Gaps | AC1, AC2 | | |

## Acceptance Criteria

- [ ] **AC1.** Each repository check reads every document and construct its rule names, and names any it passes over, as the checks' own tests run by `make check` show.
- [ ] **AC2.** Each repository check refuses every case its rule states it refuses, a build tag whose version the build does not report among them, as the checks' own tests run by `make check` show.
- [x] **AC3.** One run names every failing check and tells a fixture that failed in itself from one whose output moved, as the corpus harness and the aggregate check target show.
- [x] **AC4.** Restating a stale fixture changes only its expected bundles and their names, and refuses a fixture whose run failed in itself, as the corpus harness shows.
- [x] **AC5.** No test the overlap table records as approved for removal is collected from `src/tests/test_cli.py`, as that table compared with pytest's collection shows.

## Non-Goals

- It does not change what a run of `pf` produces.
- It adds no rule to a check that the design or that check does not already state.
- It does not restate a fixture without a passing run behind it.
- It does not remove a test whose assertion no fixture holds.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-13-20-i01-retirement) — why these checks form their own initiative and the decisions behind it.
- **R2.** [Criticality assessment](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-21-163-i00-e11-w29-a-member-whose-whole/analysis.md#why-these-three-and-not-the-other-seven) — the distribution ships `prosiform` alone, so a check, a fixture declaration and the design record reach no user of the tool.
- **R3.** [Versioning policy](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md) — what the contract tag and each build tag assert.
- **R4.** [[I01] Field Refinement: The Specification Settled by Use](https://github.com/m2ux/prosiform/issues/20) — the initiative this work was carried in before it took its own goal.
- **R5.** [Test turnaround record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-test-turnaround) — the measurements of what a change costs in fixtures and tests.
