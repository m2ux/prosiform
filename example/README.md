# Example

The example tree the [design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md)'s usage examples name, so every published invocation runs against something this repository carries.

[`work-tracker/`](work-tracker/SKILL.md) is a skill in the shape agent skills take: a routing document, a mode procedure beneath `modes/`, and the artifact documents that procedure reaches beneath `artifacts/`. Its prose is taken from the closure of one real skill procedure and renamed. **The tree is a copy. It does not track its source, mirrors no other repository, and is maintained here when the contract changes.**

## What it shows

Its references carry every answer position gives, so a reader sees the differences in one place:

- **Linked where the material is required.** A link resolving to a document under the root is a dependency: `modes/plan-mode.md` links the two artifact documents its procedure reads, and `artifacts/epic-issue-body.md` links the section of `artifacts/epic.md` whose findings it returns. Each is bundled.
- **Marked where it is reached later.** `modes/plan-mode.md` links the routing document it was reached through and opens that link's text with `¬`, which defers it: `[¬ SKILL.md](../SKILL.md)`. The document is confirmed to exist and carried nowhere, and the bundle publishes the link with its mark and with `SKILL.md`, the target's path from the root, so an agent holding the bundle compiles it in a run of its own.
- **Named where it is only cited.** A document outside the root is text wherever a source names it, and this tree's own `README.md` cites the design that way. Material a bundling only names therefore stays out of the bundle.

## What runs against it

The `usage-example/` family of the [fixture corpus](../fixtures/README.md) bundles this tree through each invocation the design publishes, so an example that stops being a valid invocation fails a run rather than going quietly stale. Each of those fixtures reaches the tree through a `source` symbolic link, so the corpus and the design name one tree rather than copies of it.
