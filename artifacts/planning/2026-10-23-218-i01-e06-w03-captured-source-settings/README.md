# Captured Source Settings

W03 connects the bounded metadata decoder to captured source reads for epic #218. Coverage: AC5 immutable per-source settings, AC6 metadata separation from Markdown, AC7 original byte accounting and coordinates. The user authorizes delivery. W02 is merged in PR #221.

## Delivery

- Component: `src/prosiform/source.py` and directly affected callers, fixtures and diagnostics.
- Task branch: `i01/e06/w03-captured-source-settings`.
- Epic base: `i01/e06/main`, targeting `main`.
- Worktree: `.worktrees/i01/e06/w03-captured-source-settings`.
- Contract: W01 at `91eecd4`, on epic base `i01/e06/engineering`.
- Board: Bundling project 18; epic #218 remains In Progress.
- Repository automatic issue closure is confirmed disabled for this session.
- Draft reviews #220 and #222 are Development-linked to #218.

## Artifacts

- [Work item](w03.md)
- [Validation](validation.md)
- [Delivery decisions](changes.md)
- [Complete checks log](checks.log)
- [Delivered source contract](design.md) — full conformance snapshot for the W03 runtime, combining the established grouping interface with validated captured metadata. The build pins this snapshot by commit; the W01 contract remains the complete epic's target.

## Progress

- [x] Verify W02 delivery and reserve W03.
- [x] Implement and validate source integration.
- [x] Publish, merge and record W03 delivery.

## Delivered

[PR #223](https://github.com/m2ux/prosiform/pull/223) merges verified head `65eaabda7238536694b4e7d9289329e6736f07ca` into `i01/e06/main` at `dd2e087060701f8472cfa9a8d2c2b81bea0a437f`. W03 and AC5–AC7 are complete on epic #218. [Draft review #222](https://github.com/m2ux/prosiform/pull/222) describes the actual W02 and W03 merges and retains its Development link to the epic. The epic remains In Progress, with W04 next. No epic review is merged.

The sync script reports engineering review #220 as in flight because the main workspace branch registry names only `main` and `workspace`; #220 remains the already recorded engineering-base review, not an extra task. Its state and target are preserved.
