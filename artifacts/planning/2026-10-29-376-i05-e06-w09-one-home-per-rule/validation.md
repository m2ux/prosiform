# Validation — I05:E06 W09

Base: `38fda13465b524a25e152f324e787d91f7660b2c` (`i05/e06/main`).
Validated tree: `3849ae8e`, the example change and its regenerated bundles committed on `i05/e06/w09-one-home-per-rule`.

Every check below ran from the worktree against that tree. Corpus, invocation, conformance and independence ran with `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen pf"`. `make links`, `make smoke` and the corpus run needed the network and ran unsandboxed; the rest ran sandboxed.

## Ownership Matrix

The rule, its one home, and what now links it instead of restating it.

| Rule | Owning home | Restatements removed |
| --- | --- | --- |
| How a command's result is read | [Command result](../example/work-planner/conventions.md#command-result) | 61 identical step sentences, plus 28 step-specific reads in `board.md`, `board-delivery.md`, `board-queue.md`, `delivery-branches.md`, `delivery-plan.md`, `dependency-graph.md`, `epic.md`, `initiative-issue-body.md`, `issue-body.md`, `issue.md`, `planning-record.md`, `pull-request.md`, `repository-labels.md`, `standup-report.md` and `task-body.md` |
| How a helper's result is read and published | [Helper result](../example/work-planner/conventions.md#helper-result) | 6 identical sentences in `epic-issue-body.md` and `initiative-issue-body.md` |
| A board list read lagging a write | [Write Confirmation](../example/work-planner/conventions.md#write-confirmation) | 4 statements: `board-delivery.md` twice, `board-queue.md` once, `board.md` once |
| How a call is made and returned, and what a `⇉` or `⫽` call is | [Execution](../example/work-planner/rules.md#execution) | The guidelines' Modes section, which restated it and added the dispatch parenthetical |
| Breakdown prose belongs in Proposal | [Breakdown Prose](../example/work-planner/artifacts/issue-body.md#breakdown-prose) | Two identical field sections, in `epic-issue-body.md` and `initiative-issue-body.md` |
| One board copy from an open template | [Copy Board Template](../example/work-planner/artifacts/board.md#copy-board-template) | Two copies of the template-find, copy and link sequence, in `Create Proposals Board` and `Create Theme Board` |
| One available-work computation | [Run Delivery Planner](../example/work-planner/artifacts/delivery-plan.md#run-delivery-planner) | Two copies of the command block, its flag list and its parameter note, in `Plan Available Work` |
| One standup render | [Render Standup Report](../example/work-planner/artifacts/standup-report.md#render-standup-report) | Three copies of the command block, its flag list and its example combinations, in `Compose Standup Report` |
| One closure gate invocation | [Run Closure Gate](../example/work-planner/artifacts/issue.md#run-closure-gate) | Two copies of the command block and its exit-code note, in `Close Tracker Issue` and `Close as Completed` |
| Reading the delivery branch collections | [Read Delivery Branches](../example/work-planner/artifacts/delivery-branches.md#read-delivery-branches) | `Prepare Delivery Bases` restated the branch-name read, its flags and its epic-base listing |

Operative conditions were kept where they bind. `Prepare Delivery Bases` keeps its unevaluable-configuration report and its prerequisite requirement as its own steps; `board-delivery.md` and `board-queue.md` keep "repeat its write" and "repeat the same item read" as the step-local actions the shared rule now governs; `standup-report.md` keeps its repeat-while-unresolved condition.

`conventions.md` and `rules.md` gained sections because a link must name an owning anchor: their entries were bolded bullets and generated no fragment. Every link that used to open the file now names the entry it means.

## Subject Review (AC10)

The size report still names all five files, so each is recorded with the subject found and the reason it is not split.

| File | Size / operations | Subject found | Disposition |
| --- | --- | --- | --- |
| `artifacts/board.md` | 18.4 KB / 11 | One theme or proposals board: its identity, its selection, its creation from a template, and its items' status. | One subject, no split. Every operation consumes or produces [Board Identity](../example/work-planner/artifacts/board.md#board-identity); the copy operations were the only repeated sequence and became one shared operation. The file is named now for its operation count, not its bytes. |
| `artifacts/epic-issue-body.md` | 25.2 KB / 9 | One epic issue body: populating it, recording delivery and criteria in it, reserving and releasing its rows, validating it, revising its rows and placing a gap row. | One subject, no split. The operations divide into populate, record, reserve and revise, but each reads or writes [Body File](../example/work-planner/artifacts/epic-issue-body.md#body-file) and the [Work Breakdown](../example/work-planner/artifacts/epic-issue-body.md#work-breakdown) contract, and the recording group applies the revision group; no cut leaves operations that share no contract. |
| `artifacts/issue.md` | 27.2 KB / 14 | One tracker issue: its identity and record, its comments, its Development links, its completion and closure, and the repository-level reads that supply those identities. | One subject, no split. The candidate cut is between the lifecycle operations and `Read Repository Issues`, `Locate Initiative Issue` and `Select Tracker Number`, which look like discovery. It is not a cut: all three consume [Tracker Repository](../example/work-planner/artifacts/issue.md#tracker-repository) and [Tracker Prefix](../example/work-planner/artifacts/issue.md#tracker-prefix), the contracts the lifecycle operations return and consume, and `Select Tracker Number` is the creation path a new issue takes. Splitting would move contracts away from the operations that produce them. |
| `artifacts/pull-request.md` | 33.2 KB / 14 | One pull request: its identity, its snapshot and supporting evidence, its publication, its Development links, its base alignment and its merge. | One subject, no split. The candidate cut is between the Development-link operations and the merge operations. It is not a cut: the link operations produce [Issue-Link Snapshot](../example/work-planner/artifacts/pull-request.md#issue-link-snapshot) and [Pull Request Records](../example/work-planner/artifacts/pull-request.md#pull-request-records), which the merge, readiness and alignment operations consume, so the two groups apply across the boundary. |
| `guidelines.md` | 23.7 KB / 0 | The authoring rules for this example, one section per file kind and per cross-cutting concern, read whole by whoever changes a file. | One subject, no split. Its operation count is zero, so it is named on size alone. Its sections are the rules for one kind each, and a change author needs the shared sections, the kind's section and the Changes section together; a split would separate rules from the routing that says which applies. The shared skill guidelines keep the cross-skill rules, so this file holds one concern already. |

No file was split for size alone. The two files that gained an operation gained it by consolidation, not by new work.

## Repository Checks

| Command | Result |
| --- | --- |
| `make authoring` | 59 documents, 0 findings in modes, protocols, artifacts, references and entry files. Size report names the five files above. |
| `make steps` | Every procedure in 59 documents writes its steps as `N. Action` sub-sections. |
| `make links` | 107 documents, every reference resolved. Ran unsandboxed; the network and `gh` credentials were needed. |
| `make tables` | 19 commands and 8 declarations, each declared by the project and named by a table. |
| `make vocabulary` | 44 contract terms marked in the design, every one defined in `docs/glossary.md`, every definition carried across 24 sources. |
| `make corpus` | 342 fixtures, 342 pass, 0 fail, 0 awaited, 0 unexpected pass. Ran unsandboxed with `PROSIFORM_BUILD` set. |
| `make harness` | 758 passed. |
| `make test` | 1302 passed in 42.13s. |
| `make smoke` | Installed command named on the path, independent of the working directory and of the repository. Ran unsandboxed. |
| `make lint` | All checks passed. |
| `make format-check` | 69 files already formatted. |
| `make typecheck` | No issues in 68 source files. |
| `make lock-check` | 24 packages resolved. |
| `make layout` | 3 trees present. |
| `make invocation` | Documented invocation holds against the build under test. |
| `make conformance` | 303 clauses, 55 covered by no fixture, 0 declaration naming no clause, 0 declared code the build reports nowhere, 0 reported code the contract declares nowhere. |
| `make independence` | Every word of every fixture declaration and report entry is one the contract states. |

`make check` is not run as one target: `authoring` sits outside it by design and `links`, `smoke` and `corpus` need the network, so the set above is its constituent targets run individually. Each target passed on its own.

## Fixtures

Ten usage-example bundles were rewritten by the corpus tooling, not by hand: the seven fixture sets whose entry or closure reaches an edited file. Regeneration ran `pf` from the build under test over each manifest's source and wrote the produced bundle bytes into `expected/`, then removed the run folder. `make corpus` then passed over all 342 fixtures.

## Delivery Evidence

- [Task pull request #394](https://github.com/m2ux/prosiform/pull/394) merges the validated head `3849ae8eb8d998d44aec8c61cee029febd9ba484` into `i05/e06/main` at `2602d4540ed5ae0f218b8bb29a317f1eea3eb91c`.
- GitHub check `Checks` passed for the validated head (`123460013135`). The epic base carried no branch protection and no active rules, and the pull request was clean and mergeable.
- The comparison of the validated head against the merge commit reports no changed file, so the merge commit carries the validated tree alone.
- Epic #376 links W09 to pull request #394. W09 has no separate task issue.

