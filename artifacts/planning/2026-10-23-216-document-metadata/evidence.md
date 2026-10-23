# Evidence and Decisions

## Baseline

- Repository: `m2ux/prosiform`.
- Current GitHub main, fetched 2026-10-23: `cd3d8e635b8db500ceb7230b26209bdd37f637da`.
- Workspace: `959dbc6`; engineering record worktree initially `c4ce561`.
- `.project/main/AGENTS.md` is absent. The provided workspace instructions and `.engineering/AGENTS.md` govern this planning record.
- Existing user changes in `cursor.code-workspace` and untracked `.wp/` directories are outside this request.

## Code Evidence

Links are pinned to the fetched main revision; the source and grouping implementation was also independently inspected in existing implementation worktrees.

| Concern | Evidence |
| --- | --- |
| Structural CLI | [cli.py, group option](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/cli.py#L533-L541) |
| Discarded frontmatter and line mapping | [source.py, Source and content](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/source.py#L173-L255) |
| Captured source read | [cli.py, source preprocessing](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/cli.py#L806-L846) |
| Directory-based membership | [cli.py, membership](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/cli.py#L1412-L1427) |
| Shared group depth | [grouping.py, merged](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/grouping.py#L405-L441) |
| Runtime dependency inventory | [pyproject.toml](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/pyproject.toml#L14-L16) |
| Verification entry points | [Makefile](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/Makefile#L44-L94) |

The official Agent Skills specification was read on 2026-10-23. Its `metadata` field is a mapping of strings to strings and recommends distinct keys. The draft therefore uses flat namespaced string fields; a nested object under `metadata.prosiform` would not satisfy that convention.

## Decisions

- **Confirmed by user:** settings are per file, rather than owned by the compilation entry.
- **Requested scope:** plan the refactor using work-planner; implementation is not requested.
- **Proposed design:** explicit group membership, paired group/depth fields, equal depths within each group, individual grouping when fields are absent, operational controls on the CLI.
- **Proposed simplification:** remove global grouping flags and directory inference; no backward-compatibility path.
- **User direction:** plan a new epic. Continue directly to the epic; proposal #216 remains unplaced.
- **Tracker home:** new epic I01 E06 under Field Refinement #20. The existing initiative is extended only for this requirement. Priority 4 is recommended after Section Composition at 5; user confirmation is pending.

## Related Work

Read the repository's issues across all states before selecting proposal prefix `P05`. No existing frontmatter-conversion proposal was found. Relevant open work is #196 (nested grouping), #215 (section composition), #208 (authoring skill), #20 (Field Refinement), and #10 (Rust compiler).

## Validation

- Proposal body passed `skills/work-planner/scripts/format.py`: zero fixes, metadata changes or content decisions.
- Proposal #216 was created with `type:proposal` and `enhancement`, without an assignee, then read back for comparison.
- Compiler tests are not run for this planning-only change. The design names implementation verification and its required baseline.

## Planning Progress

- [x] Confirm per-file ownership.
- [x] Inspect the current compiler, metadata convention and related issues.
- [x] Validate and publish the scoped proposal.
- [x] Draft the design, implementation sequence and verification matrix.
- [x] Resolve proposal workflow through the user's request for a new epic.
- [x] Draft and validate the epic and its five work items.
- [ ] Confirm epic priority and publish the reviewed breakdown.
- [x] Commit and push this planning record.
