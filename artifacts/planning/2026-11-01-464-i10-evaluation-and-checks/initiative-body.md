## Overview

The repository states its behaviour in a corpus that any implementation can run, and its own checks and its eval are what hold that corpus, the design and the build to each other. The goal is a measurement that can fail: the eval's baseline tells the forms it runs apart, a check states what it measured and on which revision, an eval session reads only what the run gave it, validation refuses a bundle whose reference lands on a destination two documents share, and the eval measures how an agent follows a bundle that defers, composes or dispatches.

## Problem

A measurement that cannot fail measures nothing.

- **Every baseline cell reads 5 of 5.**
  A report detects a whole-cell collapse and says nothing about what bundling adds or whether a branch is resolved by following a link.
- **A branch name states nothing about a build.**
  The checks run by branch name, so a change to the build on an unmatched branch merges unchecked, and an unchecked merge reads like a checked one.
- **A check reads a branch that moves beneath it.**
  The link check resolves references into another branch at that branch's current head and names only the branch.
- **A pooled destination passes by construction alone.**
  A reference into a group reaches its own document's variant because the build places it there, and validation passes a bundle in which two members reach one destination.
- **A session inherits settings it was not given.**
  A session's tree or an ancestor of it can declare a hook, and the run reads neither before its sessions start.
- **No session follows the operators' edges.**
  No eval workflow defers or composes a section or dispatches past two hops, and the eval observes only whether a session ran `pf` at all.

## Proposal

- **The corpus distinguishes its forms.**
  A corpus hard enough that an agent fails in ways the scorer names, and one baseline of every form the matrix runs.
- **A check states what it measured.**
  The checks run on what a change touches, a skipped run says so, a check reading another branch names the revision it read, and the checks page states which changes run them.
- **A destination answers one document.**
  Validation refuses a bundle in which one destination answers two members of a group, so a reference reaches the document it named.
- **A session is isolated.**
  Every settings file a session would read is read before it starts, one declaring a hook refuses the run, and the eval's README names each such file and the way out.
- **The operators' edges are measured.**
  A scenario per edge of deferral, composition and dispatch states the `pf` runs and path a correct agent makes, and one live run of them is committed.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/403) | Corpus Separability | AC1, AC2, AC9, AC11, AC12 | | |
| [E01](https://github.com/m2ux/prosiform/issues/454) | Check Coverage | AC3, AC4, AC5, AC7 | | |
| [E02](https://github.com/m2ux/prosiform/issues/456) | Session Isolation | AC6, AC8 | | |
| [E03](https://github.com/m2ux/prosiform/issues/455) | Grouping Targets | AC10 | | |
| [E04](https://github.com/m2ux/prosiform/issues/579) | Composition Following | AC13 | | |

## Acceptance Criteria

- [ ] **AC1.** The committed diagram-following baseline gives a pass rate for every model, form and scenario the default matrix runs, as a comparison of the baseline file against the matrix shows.
- [ ] **AC2.** The committed baseline gives different forms of at least one scenario different pass rates, as the baseline file shows.
- [ ] **AC3.** A pull request changing the build, the corpus or the checks runs the checks before it merges, whatever its branch is called, as the workflow records of such pull requests show.
- [ ] **AC4.** A pull request's check record states whether the checks ran on its change, as the records of a checked and an unchecked pull request show.
- [ ] **AC5.** A check reading another branch of the repository names the commit it read, as that check's output shows.
- [ ] **AC6.** A diagram-following run starts no session while a settings file its sessions would read declares a hook, as the stub-agent tests `make check` runs show.
- [ ] **AC7.** The checks page states which changes run the checks, as an inspection of the page against the workflow shows.
- [ ] **AC8.** The eval's README states each settings file a run refuses, and `--eval-root` as the remedy for one above the workspaces, as an inspection of the README against the preflight shows.
- [ ] **AC9.** Every failure class the eval's scorer defines is produced by at least one scenario of the corpus, as the corpus test `make check` runs shows.
- [ ] **AC10.** A reference into a group reaches the document it named and no other member of that group, as the candidate-validation tests show.
- [ ] **AC11.** A diagram-following harness crashes on no form the matrix runs, as the committed default-matrix run, against each harness, shows.
- [ ] **AC12.** A dispatched question counts as answered only where the session produced an answer, as the committed default-matrix run, against each harness, shows.
- [ ] **AC13.** Every scenario the eval states for deferral, composition and dispatch has a committed live-run result on each harness carrying a shell, as the committed edge-case record shows.

## Non-Goals

- The eval does not add a model, a harness or a form to its default matrix.
- The checks do not move the contract off its own branch.
- Validation does not change how a reference to a pooled heading resolves; it holds the existing rule.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the goal trace, the work items, the joins, the dependency graph and the planning decisions.
- **R2.** [Inclusion profiles record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the split that raised this initiative and the decisions for the epics it was split from.
- **R3.** [I07 review remediation record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i07-review-remediation) — the overlap: I07:E00 corrects the eval's harness, scorer and corpus forms that the baseline measures.
- **R4.** [Grouping and composition record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-02-463-i09-grouping-and-composition) — where the grouping-targets work was planned, and the work items it carries.


