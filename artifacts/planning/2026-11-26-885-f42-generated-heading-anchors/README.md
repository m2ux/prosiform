# F42: Generated Heading Anchors

[Hot-fix #885](https://github.com/m2ux/prosiform/issues/885) targets main.

## Scope

Generated dispatch headings and authored headings may share visible text. Renderer-order anchors and source identities keep their links distinct. Different dispatch selections sharing a generated name remain refused, as do composition scope conflicts and excessive heading depth.

The public reproduction uses synthetic sources only.

## Delivery

- Branch: f42-generated-heading-anchors
- Base: 6eb02cb5c44bf8942ad16e5c4e6104438a969438
- Worktree: .worktrees/f42-generated-heading-anchors
- State: Done; [PR #887](https://github.com/m2ux/prosiform/pull/887) merged into main at b1c369cb833aa0b92fb88536fd65cd320b6f0ab6. Issue #885 is closed as completed.

## Checks

Corpus fixtures exercise authored/generated ordering, ordinary links, Mermaid dispatch links, sets and picks. Existing negative cases retain genuine ambiguity refusals. Complete repository checks and revision-bound review precede ready state.

## Before and After

[Local review specimens](specimens/README.md) provide identical source, the original refusal, and the actual fixed bundles for both heading orders.
