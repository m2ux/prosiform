# W00 Validation

Revision: `d6f95677d6dfa6d6b7b37f9106cb7e2a4fafabfd`. The [immutable design pin](https://github.com/m2ux/prosiform/blob/d6f95677d6dfa6d6b7b37f9106cb7e2a4fafabfd/artifacts/planning/2026-10-17-prosiform-v1/design.md) is the contract this preparatory unit delivers. The running compiler's README pin is `6deca17d6b56c61f477c815da6eeecc3949d8ca1`; the joined CLI/caller/fixture unit adopts this candidate with its implementation.

## T1: Contract and Fixture Review

Result: pass for AC1. The [clause-to-fixture review](clause-review.md) checks the committed contract against the confirmed link title, CLI, default, unknown-tag, selection-locality, deferral and dispatch-variant requirements. It names concrete scenarios and the existing fixtures their implementation adapts. Coordinator inspection verifies the single-entry guide, complete-name matching, per-occurrence scope, deterministic canonical JSON/SHA-256 names and consistent dispatch identities.

This is design acceptance. It does not claim that the new source behavior or its runtime fixtures are implemented. Candidate parsing reports 365 clauses and 69 uncovered clauses. One retired clause identifier is named by 15 existing fixtures; their migration accompanies the CLI/caller unit, whose work item explicitly updates the README pin and manifest clause names together.

## T2: Structural Checks

Result: pass for AC1. Run from the project checkout:

```sh
.worktrees/i10/e00/main/src/.venv/bin/python .worktrees/e07-w00-validate.py
git -C .worktrees/i10/e07/w00-the-design-states-explicit diff --check
```

The [replay script](validation-replay.py) is the first command's complete source and can be copied to that temporary path. The [output](validation-output.txt) records zero unresolved internal links across 11 distinct destinations, 47 defined marked terms, zero stale operative selection/CLI claims, balanced fences and the independently recomputed digest example. Six existing remote references were not fetched. Candidate code declarations match the current reported codes; candidate runtime conformance is not claimed.

## T3: Existing Pin Conformance

Result: pass for the existing compiler/contract baseline, with no claim about candidate feature support. Run from the project checkout:

```sh
env PROSIFORM_BUILD=/home/mike1/projects/dev/md-composer/.worktrees/i10/e00/main/src/.venv/bin/pf .worktrees/i10/e00/main/src/.venv/bin/python .worktrees/i10/e07/main/checks/conformance.py
```

The [report](pinned-conformance.txt) reads the existing immutable pin: 361 clauses, 64 uncovered clauses, no missing clause declarations and no code mismatches. The build environment is the existing E00 checkout; this check observes declarations and codes, not a new paid eval or tag execution.

## Delivery Boundaries

Only the engineering design document changes in the task commit. Product source, fixture behavior and the current main README pin are outside W00. The task PR targets `i10/e07/engineering`. Its target has no branch protection and no active rules, as the fetched target evidence records. Repository automatic issue closure is confirmed disabled by the user on 2026-11-06; no repository setting is changed.

## Merged Delivery

PR #663 merged into `i10/e07/engineering` at `dfbcca186371e02d8be84514d8f4da25baec6b54`. The design file at that merge is byte-identical to reviewed head `d6f95677d6dfa6d6b7b37f9106cb7e2a4fafabfd`, verified with `git diff --exit-code <head> <merge> -- artifacts/planning/2026-10-17-prosiform-v1/design.md`.

The epic reads back W00 done and AC1 ticked, and remains In Progress. The engineering integration is draft PR #664 with its Development link to #662 verified from both ends. Full-epic automated base/target checks remain unevaluable because the engineering base carries no `config/branches`; that limitation does not claim full epic readiness. The next task is W01; I11 remains blocked on #464.
