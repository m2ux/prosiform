# Pick Heading Candidate Results

Candidate a5a98d94faccc5dc3b4e0ea480bd0a8c3682025f against main 61ddc5aa1a89ddf3f83a5d78a450ccec428aaabf. The local candidate uses the pf 0.34.0 package profile. The installed compiler remains separate.

## Compiler Tests

- The synthetic regression reproduced three identical generic headings before the fix, both with and without briefs: two expected failing tests.
- The corrected regression retains three distinct operation names, matching local graph targets and all nine choice links.
- Focused dispatch, brief and CLI checks: 568 passed.
- Complete compiler suite: 2,310 passed in the sandbox; thirteen packaging tests could not write its read-only uv cache. Those thirteen passed when rerun with host access. All 2,323 distinct tests therefore pass across the two observed runs.
- Collision coverage includes picks sharing a name for different selections, pick/brief collisions in either order and authored heading collisions. The former fixed heading is available as an ordinary authored dispatch name.

## Fixture Corpus

- 708 fixtures pass, with no awaited or unexpected-pass fixtures.
- Seven snapshots change only generated section names and their local anchors. Two manifests retain their collision code and refusal while matching the shared naming diagnostic.
- The initial corpus setup used an unsupported module invocation; all failures belonged to that setup. The corrected console invocation exposed two old message expectations. Both transcripts are retained separately from the final result under /tmp during this session.

## Source And Documentation

- Ruff formatting and lint pass for all changed Python files.
- Mypy passes for the three changed Python files.
- Every reference in the changed dispatch document resolves.
- Repository layout, command tables and vocabulary checks pass.
- The task worktree is clean at the named commit. The candidate branch is published for issue #846; the delivering pull request is draft.
