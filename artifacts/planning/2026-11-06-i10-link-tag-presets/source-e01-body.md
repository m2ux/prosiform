## Overview

The checks workflow reads a branch name, and a branch name states little about whether the branch carries a build; the link check reads other branches by name, and a name states nothing about the revision read. This epic makes the checks run where a change can break the build, makes a merge record say whether its change was checked, and makes a check reading another branch name the revision it read.

## Problem

- **A branch name is the only thing the trigger reads.**
  The [workflow's trigger](https://github.com/m2ux/prosiform/blob/23882b7d9c4faa78407468072a9eee1f8baeba4c/.github/workflows/checks.yml#L9-L16) is a push to `main` or to `i[0-9][0-9]/**`. Three merged pull requests changing 29, 9 and 27 files under `src/`, `fixtures/` or `checks/` ran no workflow.
- **A branch descended from `engineering` cannot run the checks whatever it is called.**
  The planning branch holds no build, so no workflow file exists on it, and a name-based trigger cannot express that descent.
- **A skipped run and a passing run read alike.**
  Nothing on a pull request distinguishes a change that was verified from one that was never attempted, so the distinction survives only in a check made afterwards.
- **The link check reads a branch that moves beneath it.**
  A [reference into another branch](https://github.com/m2ux/prosiform/blob/23882b7d9c4faa78407468072a9eee1f8baeba4c/checks/links.py#L217-L231) resolves against that branch's current head, and the output names the branch alone, so two runs over one commit that disagree are indistinguishable.

## Proposal

- **The trigger reads what the change touches.**
  A pull request touching the build, the corpus or the checks runs them, whatever the branch is called, and a push to `main` runs them; a change touching none runs nothing.
- **A skipped run states itself.**
  A pull request whose checks do not run reports that under the checks' own name, so a merge record states whether its change was checked.
- **The checks page states the rule.**
  The page a reader judges a merge by names the paths and events that run the checks and what a skip reports.
- **A check names the revision it read.**
  The link check resolves each branch it reads to a commit once per run and names that commit in its summary and its failures. The design reads are already pinned to the commit the README names.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/pull/607) | The trigger reads the changed paths | AC1 | | | ✓ |
| [W02](https://github.com/m2ux/prosiform/pull/608) | The link check names each revision read | AC2 | | | ✓ |
| [W03](https://github.com/m2ux/prosiform/pull/614) | A skipped run states itself | AC3 | W01 | | ✓ |
| [W04](https://github.com/m2ux/prosiform/pull/617) | The checks page states the trigger rule | AC4 | W03 | | ✓ |
| [W05](https://github.com/m2ux/prosiform/pull/619) | Every Markdown document runs the checks | AC5 | W01 | | ✓ |

## Acceptance Criteria

- [x] **AC1.** A pull request whose branch lies outside the initiative naming pattern and whose change touches `src/`, `fixtures/` or `checks/` runs the checks before it merges, as the workflow runs on such pull requests, one touching each, show.
- [x] **AC2.** The link check names the commit each branch it reads resolved to, in its summary and in each failure on a reference into that branch, as a link-check test `make check` runs shows.
- [x] **AC3.** A pull request whose change touches no checked path carries a check result stating that the checks did not run, as the check record of a pull request changing no build file shows.
- [x] **AC4.** The checks page names every path and event that runs the checks, and none the workflow does not, as an inspection of the page against the workflow shows.
- [x] **AC5.** A pull request whose change touches only a Markdown document in a directory the workflow's path set names no other way, such as `.github/`, runs the checks, as `git diff --name-only` over the workflow's `CHECKED_PATHS` on a commit adding such a document shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the design, the work items, the joins, the measurement of the name-based trigger and the planning decisions.
- **R2.** [Checks workflow](https://github.com/m2ux/prosiform/blob/23882b7d9c4faa78407468072a9eee1f8baeba4c/.github/workflows/checks.yml) — the trigger, and the comment stating that `workspace` and `engineering` hold no build to check.
