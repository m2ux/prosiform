# Decisions

- The polymorphic root rule is a new epic, I01 E08, titled Inherited Roots. Implementation is deferred. No resolver, test, or authoring file changes with this plan.
- Document Metadata, issue 218, stays the delivered contract in review. Its criteria and review are unchanged.
- E05 is closed as Deferred Debt, issue 206. This epic takes E08 so that closed identity stays put. E07 remains the freeze.
- The epic issue is [233](https://github.com/m2ux/prosiform/issues/233), opened at priority 6, the same priority as Document Metadata. Implementation stays deferred: no delivery base, no task session, and the review of issue 218 is unchanged. Its board status is Backlog.
- Held finding, not applied: the freeze's tagging row should consume this epic before the specification is tagged. Issue 23 is unchanged until that handoff is confirmed.
- W01, W02, and W03 are a chain. No pair is free of a dependency, so no pair shares a pull request. See joins.md.
- Group and group-depth do not follow the root. A blank `root` value stays invalid. A declared root resolves from the file that writes it. Two parents that resolve to one root produce one rendering.
