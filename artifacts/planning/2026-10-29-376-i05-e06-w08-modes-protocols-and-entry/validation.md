# Validation — I05:E06 W08

Base: `758d7f41323d0a5d18a20c4a8d3f07fa3d2dbfdc` (`i05/e06/main`).

Validated head: `e601f1448e234220be6a1edc4eb904d9e8010bef`, comprising source commit `ff13e97d` and fixture commit `e601f144`. The task branch is pushed and its worktree is clean. Validation and delivery are complete.

## Delivery Evidence

- [Task pull request #388](https://github.com/m2ux/prosiform/pull/388) merges the exact validated head into `i05/e06/main` at `38fda13465b524a25e152f324e787d91f7660b2c`.
- [GitHub Checks](https://github.com/m2ux/prosiform/actions/runs/40836782692/job/123323302196) passed for the validated head. The epic base had no branch protection or active rules, and the pull request was clean and mergeable.
- The post-merge comparison against the validated head returns no changed files.
- Epic #376 records W08 Done and AC8 checked, and remains open and In Progress on Project 18.
- Epic review #386 remains an open draft from `i05/e06/main` to `main`. Its body includes W08, and complete Development readback confirms the #376/#386 relation in both directions.
- W08 has no separate task issue and no residual work. W09 is the next task.

## Repository Checks

The complete `make check` passes: 1,302 source tests, 758 harness tests, 342/342 corpus fixtures, smoke, lock validation, lint, formatting, types, layout, tables, online links over 107 documents, vocabulary, invocation, conformance, independence and steps. The full authoring scan passes separately; W10 owns its inclusion in `make check`.

## Consumer Walkthrough

Revise mode separates script tests, skill-file checks, disclosure verification and delivery into numbered steps. All three original bash blocks remain verbatim, with their working directories and parameter mapping stated at execution.

- Documentation-only changes skip script tests and reach the skill-file check directly.
- Executable-script, consumed-template and test changes run tests first; a failure is corrected and retested before the structural check.
- The structural check accepts one directory argument per affected skill and runs from the workspace. Its result is read before disclosure verification.
- Changed SKILL frontmatter retains its delimiters, name and description checks. Deferred guideline links, whole-file reads, representative scenarios and dependency resolution remain intact.
- Delivery follows passed checks and disclosure verification. Distinct commits, push and per-file reporting remain in the procedure.

## Authoring Scope

The full authoring scan reports zero findings in modes, protocols, artifacts, references and entry files. AC8's non-artifact scope passes, and W07's artifact scope remains clear. Size findings remain advisory for W09.

## Fixture and Preservation Checks

Regeneration covers seven fixture sets and 15 usage-example bundles; only the Revise bundle changes. All 1,834 local fragment links resolve. The three bash command blocks and four deferred guideline links are preserved verbatim and in order. The source diff is limited to Revise mode, and `git diff --check` passes.

Session evidence: `/tmp/deliver18-20261029/w08-authoring.log`, `w08-regenerate.log`, `w08-preservation.log` and `w08-check.log`.

## Entry Review

- `SKILL.md` has the required issue-type opening, mode-selection descriptions, deployment-configuration link and dependency list. Its mode links retain dispatch markers. These identify and route requests; they do not duplicate mode procedures.
- `rules.md` owns Decisions, Layers and Execution. Modes and protocols reach it through their required preambles. Removing those operative rules would remove their owning definitions.
- `example/work-planner/README.md` does not exist. The original work item names a stale path. `example/README.md` is the compiler's worked-example guide, with intentionally exact fixture excerpts, rather than a skill navigation README.
- The full non-artifact inventory contains ten modes, twelve protocols, one reference, and the entry/configuration/conventions/guideline files. Baseline authoring findings are limited to Revise mode's Commands section and three command placements.
- Source search finds no external links to the Revise command headings or numbered verification/delivery headings. The affected generated fixture is `a-mode-and-the-guidelines-it-defers`.
