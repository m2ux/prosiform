# Example

The example tree the [design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md)'s usage examples name, so every published invocation runs against something this repository carries.

[`work-tracker/`](work-tracker/SKILL.md) is a skill in the shape agent skills take: a routing document, a mode procedure beneath `modes/`, and the artifact documents that procedure reaches beneath `artifacts/`. Its prose is taken from the closure of one real skill procedure and renamed. **The tree is a copy. It does not track its source, mirrors no other repository, and is maintained here when the contract changes.**

## What it shows

Its references carry both halves of the marking rule, so a reader sees the difference in one place:

- **Marked where the material is required.** A link whose text opens with `¬` is a dependency: `modes/plan-mode.md` marks the two artifact documents its procedure reads, and `artifacts/epic-issue-body.md` marks the section of `artifacts/epic.md` whose findings it returns. Each is bundled.
- **Unmarked where it is cited.** `modes/plan-mode.md` cites the routing document it was reached through, and `artifacts/epic-issue-body.md` cites, in its opening prose, the same document it requires further down. A citation carries nothing into the bundle and is emitted as its author wrote it.

## What runs against it

The `usage-example/` family of the [fixture corpus](../fixtures/README.md) bundles this tree through each invocation the design publishes, so an example that stops being a valid invocation fails a run rather than going quietly stale. Each of those fixtures reaches the tree through a `source` symbolic link, so the corpus and the design name one tree rather than copies of it.
