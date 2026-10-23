# Per-File Compilation Settings

W04 applies captured metadata to compilation for epic #218. Coverage: AC8 destination-owned settings across selection paths, AC9 atomic deterministic group-depth conflicts, AC10 structural settings exclusively from source metadata. The user authorizes delivery. W03 is merged in PR #223.

## Delivery

- Component: `src/prosiform/cli.py` and directly affected grouping, candidate validation, fixtures and interface documentation.
- Task branch: `i01/e06/w04-per-file-compilation-settings`.
- Epic base: `i01/e06/main`, targeting `main`.
- Worktree: `.worktrees/i01/e06/w04-per-file-compilation-settings`.
- Target contract: W01 at `91eecd4`, on epic base `i01/e06/engineering`.
- Board: Bundling project 18; epic #218 remains In Progress.
- Repository automatic issue closure is confirmed disabled for this session.
- Draft reviews #220 and #222 are Development-linked to #218.

## Artifacts

- [Work item](w04.md)
- [Validation](validation.md)
- [Plan changes](changes.md)
- [Compilation contract](design.md) — the complete W01 target contract with the installed entry point stated inline; this delivery pins its published revision for strict conformance checks.

## Progress

- [x] Verify W03 delivery and reserve W04.
- [x] Implement and validate metadata-driven compilation.
- [x] Publish, merge and record W04 delivery.

## Result

[PR #224](https://github.com/m2ux/prosiform/pull/224) merged into `i01/e06/main` at `4bb6f261475340f0ea2338c7107c88c942c878fe`. The tested head is `f139b253ab954bb2f2241a8d3d428e03600b35da`. AC8–AC10 are verified and W04 is Done. Draft runtime review #222 includes the delivered behavior and all three merged runtime tasks. Epic #218 remains open and In Progress; W05 is the remaining task.
