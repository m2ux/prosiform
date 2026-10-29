# Validation — I05:E06 W06

## Delivery Checkpoint

- Base revision: `c5056b8b` on `i05/e06/w06-artifact-inputs-and-outputs`.
- Validated revision: `4053b77d5cb8949acdd2e0426d3e545159c0f65b`; artifact contracts are committed in `966961a1`, followed by the regenerated fixtures.
- The resumed worktree holds the prior session's edits to 30 artifact files.
- Scope: I05:E06 W06, covering AC6. Command placement remains W07; mode and protocol conversion remains W08.

## Review

The review checks each operation's boundary values against its steps and the linked contract. It also compares the diff with the base for conditions lost from prose Inputs declarations. The resolved findings include missing contract anchors, a merge-authorization definition that changed the existing approval rule, and prerequisites placed after their governed action. The approved placement sample has two links narrowed to the canonical issue-record contract; its structure and procedure are preserved.

## Checks

| Check | Required result | Result |
| --- | --- | --- |
| Artifact Inputs and Outputs | No findings in `example/work-planner/artifacts/` | Pass: zero Inputs and Outputs findings |
| Contract links | Every boundary value links its defining contract | Pass: 122 operations and 692 boundary links, no unresolved target; consumer walkthrough |
| Bundle anchors | Every regenerated local fragment resolves | Pass: 2,308 anchors in 14 regenerated bundles, no unresolved target |
| Steps | `make steps` passes | Pass: 59 documents |
| Links | `make links` passes | Pass: every reference in 107 documents |
| Corpus | `make corpus` passes with the worktree build | Pass: 342 fixtures, no failures or awaited results |
| Repository checks | Every `make check` target passes with the worktree build | Pass after the network-dependent bootstrap tests were retried |

### Authoring Scope

`make authoring` reports zero Inputs and Outputs findings in every area. Its overall exit status remains nonzero for 184 findings: 17 Commands sections and 163 command placements in artifacts, and one Commands section and three command placements in modes. Those are W07/W08 scope, so the overall authoring command is not reported as passing. AC6's category passes.

### Repository Check Execution

Commands use `UV_CACHE_DIR=/tmp/w06-uv-cache` and `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen pf"` for this task's worktree.

- `make check` passed lock, lint, format and type checks, then passed 1,289 build tests. Thirteen bootstrap tests errored in fixture setup because sandboxed DNS prevented `uv pip install` from downloading the installed wheel's dependencies from PyPI.
- With network access, `uv run --frozen pytest tests/test_linked_bootstrap.py` from `src/` passed all 13 tests. No product change was needed for that setup failure.
- `make harness smoke layout tables vocabulary invocation conformance independence` passed with network access. The harness passed 758 tests; the smoke check exercised the installed wheel; invocation checked 29 documented statements.
- `make corpus` passed all 342 fixtures after the final regeneration. `make links` passed with network access, and `make steps` passed.
- `git diff --check` passed.

These are local results. They do not claim GitHub CI execution. The initial `make check` command failed at test setup; the targeted retry and remaining targets together establish the completed check set.

## Consumer Walkthrough

A separate read-only session received three requests without expected reading choices: prepare a board read and status update, prepare a task pull request with no separate task issue, and prepare an epic-delivery recording. It followed the operations' Inputs and Outputs links to their contracts; it made no tracker writes.

The first pass identified four gaps:

1. Read Board State returns a Status field ID, while its declared output linked a full field definition including option IDs.
2. Publish Pull Request linked every task to an issue despite the documented case of task rows without separate issues.
3. The issue-link snapshot contract omitted the array shape and keys its consumer reads.
4. Record Epic Delivery did not state the representation of an empty task-issue collection.

The second and fourth gaps also exist in the base. They are relevant to this conversion because the new boundary declarations must describe those supported cases. The confirmation requirement on task-to-pull-request matches remains in the operation's step.

The session read `guidelines.md#operations`; the requested operations in `board.md`, `pull-request.md` and `epic-issue-body.md`; their linked identity, content, field, record, snapshot and delivery contracts; `configuration.md#status-field`; `repository-labels.md#repository`; `epic.md#task-matches` and `#delivery-findings`; and `delivery-branches.md#project-checkout`. It consulted the corresponding command sections to compare the declared shapes with their actual parameters.

This exercise checks contract usability. It does not measure token savings or claim live tracker execution.

### Recheck

The independent session confirmed the Status ID, no-issue linking guard, explicit snapshot schema and empty task-issue collection corrections. The final publication return step explicitly returns no link snapshot when no issue was linked, and the creation step requires the auto-close setting only on the linking path. The coordinating review read those final statements and confirmed the remaining mismatch resolved.
