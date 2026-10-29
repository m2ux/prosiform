# Validation — I05:E06 W07

## Checkpoint

Base: `0febf1d228612c0ed09774ce36c767a7187c78c9` (`i05/e06/main`), containing merged W06.

Validated head: `9c200ffc5145d9ed407cbee7dbda5da820d359cb`. Source commit: `e4e2c58d`; generated bundles: `9c200ffc`. The task branch is pushed and the worktree is clean.

## Checks

Implementation, consumer review, repository checks and delivery are complete.

## Delivery Evidence

- [Task pull request #387](https://github.com/m2ux/prosiform/pull/387) merges the exact validated head into `i05/e06/main` at `758d7f41323d0a5d18a20c4a8d3f07fa3d2dbfdc`.
- [GitHub Checks](https://github.com/m2ux/prosiform/actions/runs/40833520896/job/123312894489) passed for `9c200ffc5145d9ed407cbee7dbda5da820d359cb`. The target had no branch protection or active rules and no review requirement; the pull request was clean and mergeable.
- The post-merge comparison between the validated head and merge commit returns no changed files.
- Epic #376 records W07 Done and AC7 checked. The epic remains open and In Progress on Project 18.
- Epic review #386 remains an open draft from `i05/e06/main` to `main`, with its overview and references refreshed. The complete issue and pull request Development relations still link #376 and #386 in both directions.
- W07 has no separate task issue. No closure is due; W08 is the next task.

## Repository Check Execution

The complete `make check` run passes, including 1,302 source tests, 758 harness tests, all 342 corpus fixtures, lock validation, lint, formatting, types, smoke, layout, tables, online links, vocabulary, invocation, conformance, independence and step checks. The step check covers all 59 example documents. `git diff --check` passes.

Logs for the delivery session: `/tmp/deliver18-20261029/w07-check.log`, `w07-regenerate.log` and `w07-authoring.log`. The four out-of-scope mode authoring findings are recorded separately below; authoring enforcement enters `make check` under W10.

## Authoring Scope

The full authoring report scans 59 documents and reports zero findings under `artifacts/`, including zero Inputs and Outputs, Commands section, command-placement and file-relative-link findings. AC7 is satisfied by the artifact scan.

The full report retains four findings in `modes/revise-mode.md`: one Commands section and three command placements. These belong to W08. The size report remains advisory for W09.

## Fixture Regeneration

Regeneration covers seven usage-example fixture sets and produces 15 bundles, of which 14 change. The Revise fixture is unchanged. The example README describes the artifact group's current Operations and Fields sections.

All 1,834 local fragment links in the generated bundles resolve.

## Consumer Walkthrough

The conversion maps 96 command definitions to 123 execution sites across 17 artifact files. Review covered linked calls and calls written only as command names, without executing the documented tracker mutations.

The final preservation audit confirms identical operation names and Inputs/Outputs contracts in all 17 artifacts. Every command definition is accounted for: 158 of 163 shell blocks are exact copies, and five templates include optional flags already documented at their call sites. Evidence: `w07-preservation.log` in the session log directory.

- **Delivery branches.** Missing-configuration findings remain recoverable. The three revision reads, main-worktree path anchoring, detached review reuse, prerequisite checks and distinct push destinations remain explicit. Protection and active rules retain separate snapshots.
- **Issues.** Creation and selected updates remain distinct. Each mutation is checked before another; optional comments and final reads have result handling. Completion and transfer retain their different closure reasons. Closure gates use fresh evidence, and Development snapshots retain their complete JSON shape.
- **Pull requests.** Task, epic and discussion creation remain alternatives. Creation is confirmed before linking; issue-less row tasks omit linking. Updates preserve unspecified fields. Collection fetches replace the first destination and append subsequent repositories, stopping on failure.
- **Planning records.** Folder creation is checked before README population. The engineering worktree is resolved before writes; commits name only the record folder and pushes follow successful commits. Missing record matches remain distinct from listing failures.
- **Repository graph.** Every command runs in the supplied worktree. Indexing and queries are checked before dependent operations; stale measurements are discarded and retried once.

Review corrections include recovery for expected nonzero helper results, immediate checks for repeated mutations, conditional link edits, creation-result handling before pull request linking, and explicit result steps after terminal commands.

## Baseline Review

An independent read-only inventory of delivery branches and issue operations identifies the conditions the conversion must preserve:

- Repository commands run in the repository checkout; merge and push commands run in the destination worktree. Paths are anchored under the main working tree.
- Missing-base creation, fetch failures, merge conflicts, verified-head checks and detached-worktree reuse retain their guards. The review-worktree operation contains three revision reads, including two calls written as plain prose.
- Protection and active rules are separate persisted records. A protection 404 does not establish that no active rules apply.
- Tracker reads distinguish JSON from body-only Markdown, and paginate optional comments. Publication selects creation or specific updates and verifies the saved fields.
- Inline and file comments are alternatives. Completion and transfer use different closure reasons. A completion gate uses fresh, complete evidence and absolute file paths where the helper changes directory.
- Development snapshots retain their JSON shape and their distinction between unreadable and empty relations.
- Pull request creation preserves task versus draft epic/discussion selection and the issue-less task case. Collection reads truncate once and append subsequent repositories, stopping on failure.
- Planning publication commits only its record folder and stops on a non-fast-forward push.

These are review obligations for the final conversion, not completed verification results.
