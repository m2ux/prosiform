# Findings Scan — I05:E06 W02

The first report of `make authoring` over `example/work-planner/`. The rollout rows W06–W09 start from it.

- **Source.** Taken on `i05/e06/main` at `6dc691dd`, the merge of #377, with the check at `256a032f`.
- **Scope.** 58 documents, 431 findings, exit 1.
- **Concurrent work.** W03, which adds the configuration document and edits bindings, had not merged when this was taken. Its merge may change these counts.

## By Area and Kind

| Area | Inputs and Outputs | Commands section | Command placement | File-relative links | Total |
| --- | --- | --- | --- | --- | --- |
| Modes | 0 | 1 | 3 | 0 | 4 |
| Protocols | 0 | 0 | 0 | 0 | 0 |
| Artifacts | 244 | 18 | 165 | 0 | 427 |
| References | 0 | 0 | 0 | 0 | 0 |
| Entry files | 0 | 0 | 0 | 0 | 0 |
| **Total** | 244 | 19 | 168 | 0 | 431 |

## What Each Count Is

- **Inputs and Outputs (244).**
  - The artifacts hold 122 operations.
  - Each has a prose **Inputs:** line, which is not a list of contract links: 122 findings.
  - Each has no **Outputs:** line: 122 findings.
  - No Inputs line runs onto a second line, and no operation lacks an Inputs line.
  - W06's row.
- **Commands section (19).**
  - 18 artifacts and `modes/revise-mode.md` each carry a `## Commands` section.
  - `guidelines.md` raises none.
  - W07 owns the artifacts and W08 owns `revise-mode.md`.
- **Command placement (168).**
  - Every `bash` fence in the example sits under a Commands section, so each is outside a step.
  - None is indented, and no command yet sits in a step.
  - The count falls as W07 and W08 move each command into the step that runs it.
- **File-relative links (0).**
  - Every cross-file link is already written from its file.
  - The check holds that form through the rollout.

## By File

| File | Inputs and Outputs | Commands section | Command placement | File-relative links |
| --- | --- | --- | --- | --- |
| `artifacts/acceptance-criteria.md` | 10 | 0 | 0 | 0 |
| `artifacts/architecture-overview.md` | 2 | 0 | 0 | 0 |
| `artifacts/board-delivery.md` | 6 | 1 | 2 | 0 |
| `artifacts/board-queue.md` | 4 | 1 | 2 | 0 |
| `artifacts/board.md` | 20 | 1 | 19 | 0 |
| `artifacts/delivery-branches.md` | 16 | 1 | 22 | 0 |
| `artifacts/delivery-brief.md` | 4 | 0 | 0 | 0 |
| `artifacts/delivery-evidence.md` | 4 | 0 | 0 | 0 |
| `artifacts/delivery-plan.md` | 2 | 1 | 2 | 0 |
| `artifacts/dependency-graph.md` | 2 | 1 | 6 | 0 |
| `artifacts/epic-issue-body.md` | 18 | 1 | 8 | 0 |
| `artifacts/epic.md` | 10 | 1 | 2 | 0 |
| `artifacts/goal-trace.md` | 4 | 0 | 0 | 0 |
| `artifacts/initiative-issue-body.md` | 14 | 1 | 6 | 0 |
| `artifacts/initiative.md` | 2 | 0 | 0 | 0 |
| `artifacts/issue-body.md` | 14 | 1 | 2 | 0 |
| `artifacts/issue.md` | 26 | 1 | 32 | 0 |
| `artifacts/placement.md` | 10 | 1 | 2 | 0 |
| `artifacts/plan-change.md` | 6 | 0 | 0 | 0 |
| `artifacts/planning-record.md` | 6 | 1 | 8 | 0 |
| `artifacts/proposal-body.md` | 4 | 0 | 0 | 0 |
| `artifacts/pull-request-body.md` | 8 | 0 | 0 | 0 |
| `artifacts/pull-request.md` | 28 | 1 | 38 | 0 |
| `artifacts/repository-graph.md` | 2 | 1 | 8 | 0 |
| `artifacts/repository-labels.md` | 2 | 1 | 2 | 0 |
| `artifacts/review-finding.md` | 4 | 0 | 0 | 0 |
| `artifacts/standalone-body.md` | 4 | 0 | 0 | 0 |
| `artifacts/standup-report.md` | 2 | 1 | 2 | 0 |
| `artifacts/task-body.md` | 4 | 1 | 2 | 0 |
| `artifacts/technical-debt.md` | 2 | 0 | 0 | 0 |
| `artifacts/work-item.md` | 4 | 0 | 0 | 0 |
| `modes/revise-mode.md` | 0 | 1 | 3 | 0 |

## Size Report

These files are listed for a reviewer to read for a second subject. The list holds no findings. W09 reads each one.

| File | Size | Operations |
| --- | --- | --- |
| `artifacts/board.md` | 14.3 KB | 10 |
| `artifacts/epic-issue-body.md` | 22.2 KB | 9 |
| `artifacts/issue.md` | 20.6 KB | 13 |
| `artifacts/pull-request.md` | 27.6 KB | 14 |
| `guidelines.md` | 24.3 KB | 0 |

`guidelines.md` is expected here, as W01 recorded.
